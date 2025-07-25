class State:
    times = {
        'Amogh': 5,
        'Ameya': 10,
        'Grandmother': 20,
        'Grandfather': 25
    }

    def __init__(self, left, right, umbrella, time_elapsed=0):
        self.left = left
        self.right = right
        self.umbrella = umbrella
        self.time_elapsed = time_elapsed

    def goalTest(self):
        return len(self.left) == 0 and self.umbrella == 'R'

    def moveGen(self):
        children = []
        if self.umbrella == 'L':
          
            side_from = self.left
            side_to = self.right
            new_umbrella = 'R'
        else:
             
            side_from = self.right
            side_to = self.left
            new_umbrella = 'L'

        
        movers = []
        for i in range(len(side_from)):
            movers.append([side_from[i]])
        for i in range(len(side_from)):
            for j in range(i + 1, len(side_from)):
                movers.append([side_from[i], side_from[j]])

        for move in movers:
            time_to_cross = max(State.times[person] for person in move)
            new_time = self.time_elapsed + time_to_cross
            if new_time > 60:
                continue   

            new_left = self.left[:]
            new_right = self.right[:]

            if self.umbrella == 'L':
              
                for person in move:
                    new_left.remove(person)
                    new_right.append(person)
            else:
                 
                for person in move:
                    new_right.remove(person)
                    new_left.append(person)

            child = State(sorted(new_left), sorted(new_right), new_umbrella, new_time)
            children.append(child)

        return children

    def __str__(self):
        return (f"Left: {self.left} | Right: {self.right} | "
                f"Umbrella: {self.umbrella} | Time elapsed: {self.time_elapsed}")

    def __eq__(self, other):
        return (self.left == other.left and
                self.right == other.right and
                self.umbrella == other.umbrella and
                self.time_elapsed == other.time_elapsed)

    def __hash__(self):
        return hash((tuple(self.left), tuple(self.right), self.umbrella, self.time_elapsed))


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

    def dfs(self, start):
        open = [(start, None)]
        closed = []

        while open:
            node_pair = open.pop(0)
            node, parent = node_pair

            if node.goalTest():
                print("Goal found!")
                self.reconstructPath(node_pair, closed)
                return
            else:
                closed.append(node_pair)
                children = node.moveGen()
                new_nodes = self.removeSeen(children, open, closed)
                node_pairs = [(child, node) for child in new_nodes]
                open = node_pairs + open

        print("Goal not found")


start_state = State(['Ameya', 'Amogh', 'Grandfather', 'Grandmother'], [], 'L', 0)
search = Search()
search.dfs(start_state)
