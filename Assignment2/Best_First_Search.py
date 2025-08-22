
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

def best_first_search(grid):
    n = len(grid)
    if n == 0:
        return None, -1

    start = (0, 0)
    goal = (n - 1, n - 1)

    if grid[0][0] != 0 or grid[goal[0]][goal[1]] != 0:
    
        return None, -1

    open_heap = []
    start_h = heuristic(start, goal)

    heapq.heappush(open_heap, (start_h, start))

    came_from = {start: None}
    visited = set()           

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return path, len(path)

        for nb in neighbors(current, n):
            i, j = nb
            if grid[i][j] != 0:
   
                continue
            if nb in visited:
                continue

            if nb not in came_from:
                came_from[nb] = current
                heapq.heappush(open_heap, (heuristic(nb, goal), nb))

    return None, -1

if __name__ == "__main__":
    tests = [
        ([[0,1],[1,0]], "Example 1"),
        ([[0,0,0],[1,1,0],[1,1,0]], "Example 2"),
        ([[1,0,0],[1,1,0],[1,1,0]], "Example 3")
    ]

    for grid, title in tests:
        print("\n" + title)
        path, length = best_first_search(grid)
        if path is None:
            print("Best First Search → Path length: -1, Path: []")
        else:
            print("Best First Search → Path length: {}, Path: {}".format(length, path))
