import networkx as nx
import torch
import torch.nn.functional as F
from torch_geometric.utils import from_networkx
from torch_geometric.nn import GCNConv
from torch_geometric.data import DataLoader

# Function to generate a random complete graph and its Hamiltonian cycle
def generate_graph_and_hamiltonian(num_nodes):
    G = nx.complete_graph(num_nodes)
    
    # Assign random weights to edges
    for u, v in G.edges():
        G[u][v]['weight'] = torch.randint(1, 10, (1,)).item()
    
    # Approximate a Hamiltonian cycle (using TSP solution as an approximation)
    cycle = list(nx.algorithms.approximation.traveling_salesman_problem(G))
    
    # Generate Hamiltonian cycle graph
    H = nx.Graph()
    for i in range(len(cycle) - 1):
        u, v = cycle[i], cycle[i + 1]
        H.add_edge(u, v, weight=G[u][v]['weight'])
    H.add_edge(cycle[-1], cycle[0], weight=G[cycle[-1]][cycle[0]]['weight'])
    
    return G, H

# Generate data
num_samples = 100
num_nodes = 10
original_graphs = []
hamiltonian_graphs = []

for _ in range(num_samples):
    G, H = generate_graph_and_hamiltonian(num_nodes)
    original_graphs.append(from_networkx(G))  # Convert to PyTorch Geometric format
    hamiltonian_graphs.append(from_networkx(H))

# Define a simple GCN model for predicting Hamiltonian cycle weights
class HamiltonianGNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super(HamiltonianGNN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.fc = torch.nn.Linear(hidden_channels, 1)  # Predicts edge weights

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        
        # Final layer to output edge weights
        return self.fc(x)

# Prepare data and model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = HamiltonianGNN(in_channels=num_nodes, hidden_channels=32).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(100):
    total_loss = 0
    for i in range(num_samples):
        data = original_graphs[i].to(device)
        target = hamiltonian_graphs[i].edge_attr.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        output = model(data.x.float(), data.edge_index)
        
        # Compute loss between predicted and actual Hamiltonian edges
        loss = F.mse_loss(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    print(f'Epoch {epoch+1}, Loss: {total_loss/num_samples}')

# Example inference
data = original_graphs[0].to(device)
output = model(data.x.float(), data.edge_index)

# Output can be reshaped into a predicted adjacency matrix
predicted_weights = output.detach().cpu().numpy()
print("Predicted Weights (Hamiltonian Cycle Approx):", predicted_weights)
