class State:
    def __init__(self, left, right, umbrella, time_elapsed):
        self.left = left
        self.right = right
        self.umbrella = umbrella
        self.time_elapsed = time_elapsed

    def goalTest(self):
        return len(self.left) == 0

    def moveGen(self):
        children = []
        if self.umbrella == 'L':
            source = self.left
            dest = self.right
            new_umbrella = 'R'
        else:
            source = self.right
            dest = self.left
            new_umbrella = 'L'

        for i in range(len(source)):
            for j in range(i, len(source)):
                moving = [source[i]]
                if i != j:
                    moving.append(source[j])

                time_taken = max(times[p] for p in moving)
                new_time_elapsed = self.time_elapsed + time_taken
                if new_time_elapsed > 60:
                    continue

                if self.umbrella == 'L':
                    new_left = [p for p in self.left if p not in moving]
                    new_right = self.right + moving
                else:
                    new_right = [p for p in self.right if p not in moving]
                    new_left = self.left + moving

                child = State(new_left, new_right, new_umbrella, new_time_elapsed)
                children.append(child)

        return children

    def __str__(self):
        return (f"Left: {sorted(self.left)} | Right: {sorted(self.right)} | "
                f"Umbrella: {self.umbrella} | Time elapsed: {self.time_elapsed}")

    def __eq__(self, other):
        return (sorted(self.left) == sorted(other.left) and
                sorted(self.right) == sorted(other.right) and
                self.umbrella == other.umbrella and
                self.time_elapsed == other.time_elapsed)

    def __hash__(self):
        return hash((tuple(sorted(self.left)), tuple(sorted(self.right)), self.umbrella, self.time_elapsed))


times = {
    'Amogh': 5,
    'Ameya': 10,
    'Grandfather': 25,
    'Grandmother': 20
}

class Search:
    def removeSeen(self, children, open, closed):
        open_nodes = [node for node, _ in open]
        closed_nodes = [node for node, _ in closed]
        return [node for node in children if node not in open_nodes and node not in closed_nodes]

    def reconstructPath(self, node_pair, closed):
        path = []
        node, parent = node_pair
        parent_map = {n: p for n, p in closed}
        path.append(node)
        while parent is not None:
            path.insert(0, parent)
            parent = parent_map.get(parent)
        print("\nSolution path:")
        for state in path:
            print(state)
        print(f"\nMinimum time taken: {path[-1].time_elapsed} minutes\n")
        return path

    def bfs(self, start):
        open = [(start, None)]
        closed = []

        while open:
            node_pair = open.pop(0)
            node, parent = node_pair
           

            if node.goalTest():
                print("Goal found!")
                return self.reconstructPath(node_pair, closed)
            else:
                closed.append(node_pair)
                children = node.moveGen()
                new_nodes = self.removeSeen(children, open, closed)
                node_pairs = [(child, node) for child in new_nodes]
                open = open + node_pairs

        print("Goal not found")

 
start_node = State(
    left=['Ameya', 'Amogh', 'Grandfather', 'Grandmother'],
    right=[],
    umbrella='L',
    time_elapsed=0
)

search = Search()
path = search.bfs(start_node)
