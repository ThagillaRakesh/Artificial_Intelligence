class State:
    def __init__(self, config, parent=None):
        self.config = config
        self.parent = parent

    def goalTest(self):
        return self.config == ['W', 'W', 'W', '_', 'E', 'E', 'E']

    def moveGen(self):
        children = []
        i = self.config.index('_')

        # E moves right: from left into empty spot at i
        if i > 0 and self.config[i - 1] == 'E':
            new = self.config.copy()
            new[i], new[i - 1] = new[i - 1], new[i]
            children.append(State(new, self))

        if i > 1 and self.config[i - 2] == 'E' and self.config[i - 1] != '_':
            new = self.config.copy()
            new[i], new[i - 2] = new[i - 2], new[i]
            children.append(State(new, self))

        # W moves left: from right into empty spot at i
        if i < len(self.config) - 1 and self.config[i + 1] == 'W':
            new = self.config.copy()
            new[i], new[i + 1] = new[i + 1], new[i]
            children.append(State(new, self))

        if i < len(self.config) - 2 and self.config[i + 2] == 'W' and self.config[i + 1] != '_':
            new = self.config.copy()
            new[i], new[i + 2] = new[i + 2], new[i]
            children.append(State(new, self))

        return children

    def __eq__(self, other):
        return isinstance(other, State) and self.config == other.config

    def __hash__(self):
        return hash(tuple(self.config))

    def __str__(self):
        return ' '.join(self.config)


class Search:
    def reconstructPath(self, goal_state):
        path = []
        while goal_state:
            path.insert(0, goal_state)
            goal_state = goal_state.parent
        print("\nSolution path:")
        for state in path:
            print(state)

    def dfs(self, start):
        stack = [start]
        visited = set([start])

        while stack:
            node = stack.pop()
            if node.goalTest():
                print("Goal found!")
                self.reconstructPath(node)
                return
            for child in reversed(node.moveGen()):
                if child not in visited:
                    visited.add(child)
                    stack.append(child)
        print("Goal not found")


initial_config = ['E', 'E', 'E', '_', 'W', 'W', 'W']
start_state = State(initial_config)
search = Search()

print("DFS Solution:")
search.dfs(start_state)
