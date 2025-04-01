adj matrix: a   b   c   d   
        a   0   3   4   2   

        b   3   0   1   3   

        c   4   1   0   5   

        d   2   3   5   0   


dict on four nodes ( 12 total node subsets):
1   dist(a,b)(b)=>      starts at a, visits a,b, and ends at b
2   dist(a,c)(c)=>      starts at a, visits a,c, and ends at c
3   dist(a,d)(d)=>      starts at a, visits a,d, and ends at d
*4   dist(a,b,c)(a)=>    starts at a, visits a,b,c, and ends at a
5   dist(a,b,c)(b)=>    starts at a, visits a,b,c, and ends at b
*6   dist(a,b,d)(a)=>    starts at a, visits a ,b,d, and ends at a
7   dist(a,b,d)(b)=>    starts at a, visit a,b,d and ends at d
8   dist(a,c,d)(c)=>    starts at a, visits a,c,d, and ends at c
9   dist(a,c,d)(d)=>    starts at a, visits a,c,d, and ends at d
*10  dist(a,b,c,d)(a)=>  starts at a, visits, a,b,c,d, and ends at a
11  dist(a,b,d,c)(b)=>  starts at a, visits a,b,c,d, and ends at b
12  dist(a,b,c,d)(d)=>  starts at a, visits a,b,c,d, and ends at d