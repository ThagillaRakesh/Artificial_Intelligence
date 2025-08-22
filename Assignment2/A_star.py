
import heapq
import math

def heuristic(a, b):

    return math.hypot(a[0] - b[0], a[1] - b[1])

def neighbors(pos, n):
    i, j = pos
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                yield (ni, nj)

def reconstruct_path(came_from, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur, None)
    path.reverse()
    return path

def a_star_search(grid):

    n = len(grid)
    if n == 0:
        return None, -1

    start = (0, 0)
    goal = (n - 1, n - 1)


    if grid[0][0] != 0 or grid[goal[0]][goal[1]] != 0:
        return None, -1

    if start == goal:
        return [start], 1

    open_heap = []
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    heapq.heappush(open_heap, (f_score[start], start))
    came_from = {start: None}
    closed = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return path, len(path)

        closed.add(current)

        for nb in neighbors(current, n):
            i, j = nb
            if grid[i][j] != 0:
                continue  

            tentative_g = g_score[current] + 1  

            if nb in closed and tentative_g >= g_score.get(nb, float('inf')):
                continue

            if tentative_g < g_score.get(nb, float('inf')):
                came_from[nb] = current
                g_score[nb] = tentative_g
                f_score[nb] = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_heap, (f_score[nb], nb))

    return None, -1

if __name__ == "__main__":
    tests = [
        ([[0,1],[1,0]], "Example 1"),
        ([[0,0,0],[1,1,0],[1,1,0]], "Example 2"),
        ([[1,0,0],[1,1,0],[1,1,0]], "Example 3")
    ]

    for grid, title in tests:
        print("\n" + title)

        g = [[int(x) for x in row] for row in grid]
        path, length = a_star_search(g)
        if path is None:
            print("A* Search → Path length: -1, Path: []")
        else:
            print("A* Search → Path length: {}, Path: {}".format(length, path))
