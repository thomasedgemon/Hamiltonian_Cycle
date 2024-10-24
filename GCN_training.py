import h5py
import torch
from torch_geometric.data import Data, Dataset, DataLoader
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')  # This will print 'cuda' if a GPU is available

# Limit GPU memory usage to 50%
if device.type == 'cuda':
    torch.cuda.set_per_process_memory_fraction(0.5, 0)

# Limit PyTorch to use only half the CPU threads (adjust number as needed)
torch.set_num_threads(8)  # Adjust to half of your available cores

# Custom PyTorch Dataset for loading graph and cycle pairs from HDF5
class GraphCycleDataset(Dataset):
    def __init__(self, h5_file):
        self.h5_file = h5_file
        with h5py.File(self.h5_file, 'r') as f:
            self.pairs = list(f.keys())  # All graph-cycle pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        with h5py.File(self.h5_file, 'r') as f:
            key = self.pairs[idx]
            graph_matrix = torch.tensor(f[f'{key}/graph_matrix'][:], dtype=torch.float32)
            cycle_matrix = torch.tensor(f[f'{key}/cycle_matrix'][:], dtype=torch.float32)
            optimal_weight = torch.tensor(f[f'{key}/optimal_weight'][()], dtype=torch.float32)  # Load the cycle weight
            
            # Construct edge index for graph from adjacency matrix
            edge_index = (graph_matrix > 0).nonzero(as_tuple=False).t().contiguous()
            
            # Flatten the cycle_matrix to use as the target (since it’s a 10x10 matrix)
            target = cycle_matrix.view(-1)
            
            return Data(x=graph_matrix, edge_index=edge_index), target, optimal_weight


# Create the dataset and data loader
h5_file = 'graph_cycle_pairs.h5'  # Replace with your actual file path
dataset = GraphCycleDataset(h5_file)

# DataLoader for batching, limiting CPU usage with num_workers=4
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

# Define the GCN model
class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return F.sigmoid(x)  # Sigmoid since we’ll compare with binary cycle matrix

# Instantiate the model and move it to the GPU if available
model = GCN(in_channels=10, hidden_channels=16, out_channels=1).to(device)

# Initialize optimizer and loss function
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.BCELoss()

# Training loop
num_epochs = 100  # Number of epochs

def compute_cycle_weight(predicted_cycle, graph_matrix):
    cycle_weight = 0.0
    n = predicted_cycle.size(0)
    for i in range(n - 1):
        cycle_weight += graph_matrix[predicted_cycle[i], predicted_cycle[i + 1]].item()
    return cycle_weight

# Training loop with cycle weight comparison
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    total_correct_weight = 0
    total_cycles = 0
    
    for batch in loader:
        batch_data, batch_target, optimal_weight = batch
        batch_data = batch_data.to(device)
        batch_target = batch_target.to(device)
        optimal_weight = optimal_weight.to(device)
        
        optimizer.zero_grad()
        out = model(batch_data)
        
        loss = criterion(out.view(-1), batch_target.float())  # Binary cross-entropy for the cycle prediction
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()

        # Compute the weight of the predicted cycle
        predicted_cycle = (out > 0.5).float()
        predicted_weight = compute_cycle_weight(predicted_cycle.view(10, 10), batch_data.x)
        
        # Compare predicted cycle weight to optimal weight
        if torch.isclose(predicted_weight, optimal_weight):
            total_correct_weight += 1  # Count correct predictions by weight
        
        total_cycles += 1
    
    accuracy_by_weight = total_correct_weight / total_cycles
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss / len(loader)}, Accuracy by Weight: {accuracy_by_weight * 100:.2f}%")




# Evaluation function to check how close the predicted cycle is to the actual one
def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)  # Move batch to GPU
            out = model(batch)
            predicted = (out > 0.5).float()  # Convert probabilities to 0 or 1
            correct += (predicted.view(-1) == batch.y.to(device)).sum().item()  # Move target to GPU
            total += batch.y.size(0)
    
    accuracy = correct / total
    print(f"Accuracy: {accuracy * 100:.2f}%")

# Evaluate the model after training
evaluate(model, loader)
