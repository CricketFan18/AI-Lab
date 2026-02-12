n = int(input("Enter number of nodes: "))
matrix = [[0] * (n+1) for _ in range(n+1)]
e = int(input("Enter number of edges: "))
for i in range(e):
  u,v = map(int, input("Enter edge (u v): ").split())
  matrix[u][v] = 1
  matrix[v][u] = 1  # For undirected graph
print("Adjacency Matrix:")
for row in matrix:
    for val in row:
        print(val, end=' ')
    print()