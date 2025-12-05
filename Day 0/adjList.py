n = int(input("Enter number of nodes: "))
matrix = [[] for _ in range(n+1)]
e = int(input("Enter number of edges: "))
for i in range(e):
  u,v = map(int, input("Enter edge (u v): ").split())
  matrix[u].append(v)
  # matrix[v].append(u) # For undirected graph
print("Adjacency List:")
for row in matrix:
    print(f"Node {matrix.index(row)}: ", end='')
    for val in row:
        print(val, end=' ')
    print()