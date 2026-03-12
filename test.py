row = [0] * 5
matrix = []
for i in range(5):
    matrix.append(row[:])

for i in range(5):
    for j in range(5):
        print(f"Enter element at ({i},{j}): ")
        matrix[i][j] = int(input())
print("--Matrix--")
for row in matrix:
    print(row)

x = int(input("Enter x coordinate: "))
y = int(input("Enter y coordinate: "))
dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]
neighbours = []
for dx, dy in dir:
    nx, ny = x + dx, y + dy
    if 0 <= nx < 5 and 0 <= ny < 5:
        neighbours.append(matrix[nx][ny])
print(f"Neighbours: {neighbours}")
