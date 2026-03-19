import heapq, time, random, matplotlib.pyplot as plt
import numpy as np
from collections import deque

GRID_SIZE = 20
START = (0, 0)
GOAL = (GRID_SIZE - 1, GRID_SIZE - 1)
random.seed(42)


def generate_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) not in (START, GOAL) and random.random() < 0.25:
                grid[r][c] = 1
    return grid


def get_neighbors(pos, grid):
    r, c = pos
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] == 0:
            result.append((nr, nc))
    return result


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct(came_from, start, goal):
    path, node = [], goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    return list(reversed(path))


# ── Algorithms ────────────────────────────────────────────────────────────────
def bfs(grid):
    q = deque([START])
    cf = {START: None}
    vis = []
    t0 = time.perf_counter()
    while q:
        n = q.popleft()
        vis.append(n)
        if n == GOAL:
            break
        for nb in get_neighbors(n, grid):
            if nb not in cf:
                cf[nb] = n  # pyright: ignore[reportArgumentType]
                q.append(nb)
    t = time.perf_counter() - t0
    path = reconstruct(cf, START, GOAL) if GOAL in cf else None
    return path, vis, len(vis), t * 1000


def dfs(grid):
    stack = [START]
    cf = {START: None}
    vis = []
    t0 = time.perf_counter()
    while stack:
        n = stack.pop()
        if n in vis:
            continue
        vis.append(n)
        if n == GOAL:
            break
        for nb in get_neighbors(n, grid):
            if nb not in cf:
                cf[nb] = n  # type: ignore
                stack.append(nb)
    t = time.perf_counter() - t0
    path = reconstruct(cf, START, GOAL) if GOAL in cf else None
    return path, vis, len(vis), t * 1000


def bibfs(grid):
    fq, bq = deque([START]), deque([GOAL])
    fv, bv = {START: None}, {GOAL: None}
    vis = []
    meeting = None
    t0 = time.perf_counter()
    while fq and bq:
        n = fq.popleft()
        vis.append(n)
        if n in bv:
            meeting = n
            break
        for nb in get_neighbors(n, grid):
            if nb not in fv:
                fv[nb] = n  # type: ignore
                fq.append(nb)
        if not fq:
            break
        n = bq.popleft()
        vis.append(n)
        if n in fv:
            meeting = n
            break
        for nb in get_neighbors(n, grid):
            if nb not in bv:
                bv[nb] = n
                bq.append(nb)
    t = time.perf_counter() - t0
    if not meeting:
        return None, vis, len(vis), t * 1000
    p1 = reconstruct(fv, START, meeting)
    p2 = reconstruct(bv, GOAL, meeting)
    path = p1 + list(reversed(p2))[1:]
    return path, vis, len(vis), t * 1000


def ucs(grid):
    pq = [(0, START)]
    cf = {START: None}
    gs = {START: 0}
    vis = []
    t0 = time.perf_counter()
    while pq:
        cost, n = heapq.heappop(pq)
        vis.append(n)
        if n == GOAL:
            break
        for nb in get_neighbors(n, grid):
            nc = cost + 1
            if nb not in gs or nc < gs[nb]:
                gs[nb] = nc
                cf[nb] = n  # type: ignore
                heapq.heappush(pq, (nc, nb))
    t = time.perf_counter() - t0
    path = reconstruct(cf, START, GOAL) if GOAL in cf else None
    return path, vis, len(vis), t * 1000


def bestfirst(grid):
    pq = [(heuristic(START, GOAL), START)]
    cf = {START: None}
    vis = []
    t0 = time.perf_counter()
    while pq:
        _, n = heapq.heappop(pq)
        if n in vis:
            continue
        vis.append(n)
        if n == GOAL:
            break
        for nb in get_neighbors(n, grid):
            if nb not in cf:
                cf[nb] = n  # type: ignore
                heapq.heappush(pq, (heuristic(nb, GOAL), nb))
    t = time.perf_counter() - t0
    path = reconstruct(cf, START, GOAL) if GOAL in cf else None
    return path, vis, len(vis), t * 1000


def astar(grid):
    pq = [(heuristic(START, GOAL), 0, START)]
    cf = {START: None}
    gs = {START: 0}
    vis = []
    t0 = time.perf_counter()
    while pq:
        f, g, n = heapq.heappop(pq)
        if n in vis:
            continue
        vis.append(n)
        if n == GOAL:
            break
        for nb in get_neighbors(n, grid):
            ng = g + 1
            if nb not in gs or ng < gs[nb]:
                gs[nb] = ng
                cf[nb] = n  # type: ignore
                heapq.heappush(pq, (ng + heuristic(nb, GOAL), ng, nb))
    t = time.perf_counter() - t0
    path = reconstruct(cf, START, GOAL) if GOAL in cf else None
    return path, vis, len(vis), t * 1000


# ── Run all algorithms ────────────────────────────────────────────────────────
grid = generate_grid()
OPTIMAL_LEN = (GRID_SIZE - 1) * 2 + 1  # 39 for 20x20

algo_fns = {
    "BFS": bfs,
    "DFS": dfs,
    "Bi-BFS": bibfs,
    "UCS": ucs,
    "Best-First": bestfirst,
    "A*": astar,
}

results = {}
for name, fn in algo_fns.items():
    path, vis, nodes, ms = fn(grid)
    plen = len(path) if path else None
    results[name] = {
        "path": path,
        "vis": vis,
        "nodes": nodes,
        "time_ms": ms,
        "plen": plen,
        "optimal": plen == OPTIMAL_LEN if plen else False,
    }

names = list(results.keys())
colors = ["#2196F3", "#FF5722", "#9C27B0", "#009688", "#FFC107", "#4CAF50"]
c_map = dict(zip(names, colors))

# FIGURE 1 — Grid path visualizations (2×3 subplots)
fig1, axes = plt.subplots(2, 3, figsize=(15, 10))
fig1.suptitle("Search Algorithm — Paths on 20×20 Grid", fontsize=14, fontweight="bold")

grid_arr = np.array(grid)

for ax, (name, res) in zip(axes.flatten(), results.items()):
    # Base grid: white=free, gray=obstacle
    display = np.ones((GRID_SIZE, GRID_SIZE, 3))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 1:
                display[r, c] = [0.3, 0.3, 0.3]  # obstacle = dark gray

    ax.imshow(display, interpolation="nearest")

    # Draw path
    if res["path"]:
        pr = [p[0] for p in res["path"]]
        pc = [p[1] for p in res["path"]]
        ax.plot(pc, pr, color=c_map[name], linewidth=2.5, zorder=3)

    # Start / Goal
    ax.plot(START[1], START[0], "go", markersize=9, zorder=5, label="Start")
    ax.plot(GOAL[1], GOAL[0], "r*", markersize=12, zorder=5, label="Goal")

    plen_txt = str(res["plen"]) if res["plen"] else "None"
    opt_txt = "Optimal ✔" if res["optimal"] else "Non-Optimal ✘"
    ax.set_title(
        f"{name}  |  Nodes: {res['nodes']}  |  Path: {plen_txt}  |  {opt_txt}",
        fontsize=8.5,
        color=c_map[name],
        fontweight="bold",
    )
    ax.set_xticks([])
    ax.set_yticks([])

handles = [
    plt.Line2D(  # type: ignore
        [0], [0], marker="o", color="w", markerfacecolor="green", markersize=8, label="Start"
    ),
    plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="red", markersize=10, label="Goal"),  # type: ignore
    plt.Line2D([0], [0], color="gray", linewidth=8, label="Obstacle"),  # type: ignore
]
fig1.legend(handles=handles, loc="lower center", ncol=3, fontsize=10, bbox_to_anchor=(0.5, 0.01))
plt.tight_layout(rect=[0, 0.05, 1, 1])  # type: ignore
plt.savefig("outputs/fig1_grid_paths.png", dpi=130, bbox_inches="tight")
print("Saved fig1")

# FIGURE 2 — Bar charts: nodes, time, path length
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle("Algorithm Performance Comparison", fontsize=13, fontweight="bold")

bar_colors = [c_map[n] for n in names]
nodes_vals = [results[n]["nodes"] for n in names]
time_vals = [results[n]["time_ms"] for n in names]
plen_vals = [results[n]["plen"] or 0 for n in names]

# -- Nodes explored
ax = axes2[0]
bars = ax.bar(names, nodes_vals, color=bar_colors, edgecolor="black", linewidth=0.8)
ax.set_title("Nodes Explored", fontweight="bold")
ax.set_ylabel("Count")
for bar, val in zip(bars, nodes_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 3,
        str(val),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax.set_ylim(0, max(nodes_vals) * 1.18)
ax.tick_params(axis="x", labelsize=9)

# -- Time taken
ax = axes2[1]
bars = ax.bar(names, time_vals, color=bar_colors, edgecolor="black", linewidth=0.8)
ax.set_title("Time Taken (ms)", fontweight="bold")
ax.set_ylabel("Milliseconds")
for bar, val in zip(bars, time_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(time_vals) * 0.01,
        f"{val:.3f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax.set_ylim(0, max(time_vals) * 1.22)
ax.tick_params(axis="x", labelsize=9)

# -- Path length + optimality badge
ax = axes2[2]
bars = ax.bar(names, plen_vals, color=bar_colors, edgecolor="black", linewidth=0.8)
ax.set_title("Solution Path Length", fontweight="bold")
ax.set_ylabel("Steps")
for bar, name, val in zip(bars, names, plen_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.4,
        str(val),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
    badge = "✔ Optimal" if results[name]["optimal"] else "✘ Sub-opt"
    badge_color = "green" if results[name]["optimal"] else "red"
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        -4.5,
        badge,
        ha="center",
        va="top",
        fontsize=7.5,
        color=badge_color,
        fontweight="bold",
    )
ax.set_ylim(-7, max(plen_vals) * 1.18)
ax.tick_params(axis="x", labelsize=9)

plt.tight_layout()
plt.savefig("outputs/fig2_bar_charts.png", dpi=130, bbox_inches="tight")
print("Saved fig2")

# FIGURE 3 — Radar (spider) chart
fig3, ax3 = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
fig3.suptitle(
    "Multi-Metric Radar Comparison\n(higher = better in each dimension)",
    fontsize=12,
    fontweight="bold",
)

metrics = ["Speed\n(inv. time)", "Efficiency\n(inv. nodes)", "Path Quality", "Optimality"]
N = len(metrics)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

max_nodes = max(r["nodes"] for r in results.values())
max_time = max(r["time_ms"] for r in results.values())
max_plen = max(r["plen"] or 0 for r in results.values())

for name, color in zip(names, colors):
    r = results[name]
    speed = 1 - r["time_ms"] / max_time
    effic = 1 - r["nodes"] / max_nodes
    qual = 1 - (r["plen"] or max_plen) / max_plen
    optim = 1.0 if r["optimal"] else 0.0
    vals = [speed, effic, qual, optim] + [speed]  # close polygon
    ax3.plot(angles, vals, color=color, linewidth=2, label=name)
    ax3.fill(angles, vals, color=color, alpha=0.15)

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(metrics, fontsize=11)
ax3.set_ylim(0, 1)
ax3.set_yticks([0.25, 0.5, 0.75, 1.0])
ax3.set_yticklabels(["0.25", "0.5", "0.75", "1.0"], fontsize=8, color="gray")
ax3.legend(loc="upper right", bbox_to_anchor=(1.3, 1.15), fontsize=10)
plt.tight_layout()
plt.savefig("outputs/fig3_radar.png", dpi=130, bbox_inches="tight")
print("Saved fig3")

# FIGURE 4 — Summary table
fig4, ax4 = plt.subplots(figsize=(13, 3.5))
ax4.axis("off")
fig4.suptitle("Algorithm Summary Table", fontsize=13, fontweight="bold", y=1.02)

complexity = {
    "BFS": "O(b^d)",
    "DFS": "O(b^m)",
    "Bi-BFS": "O(b^(d/2))",
    "UCS": "O(b^(1+C*/ε))",
    "Best-First": "O(b^m)",
    "A*": "O(b^d)",
}
complete_map = {
    "BFS": "Yes",
    "DFS": "Yes",
    "Bi-BFS": "Yes",
    "UCS": "Yes",
    "Best-First": "No",
    "A*": "Yes",
}

col_labels = [
    "Algorithm",
    "Nodes Explored",
    "Time (ms)",
    "Path Length",
    "Optimal?",
    "Complete?",
    "Time Complexity",
]
table_data = []
for name in names:
    r = results[name]
    table_data.append(
        [
            name,
            str(r["nodes"]),
            f"{r['time_ms']:.4f}",
            str(r["plen"]) if r["plen"] else "N/A",
            "Yes ✔" if r["optimal"] else "No ✘",
            complete_map[name],
            complexity[name],
        ]
    )

tbl = ax4.table(cellText=table_data, colLabels=col_labels, loc="center", cellLoc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 2.0)

for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor("#DDEEFF")
        cell.set_text_props(fontweight="bold")
    else:
        name = names[row - 1]
        if col == 0:
            cell.set_facecolor(colors[row - 1])
            cell.set_text_props(color="white", fontweight="bold")
        elif col == 4:  # Optimal
            txt = table_data[row - 1][4]
            cell.set_facecolor("#CCFFCC" if "Yes" in txt else "#FFCCCC")
        else:
            cell.set_facecolor("#F9F9F9" if row % 2 == 0 else "white")

plt.tight_layout()
plt.savefig("outputs/fig4_summary_table.png", dpi=130, bbox_inches="tight")
print("Saved fig4")
print("\nDone.")
