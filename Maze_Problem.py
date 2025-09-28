from collections import deque   # deque is used for BFS (queue behavior)
import heapq                    # heapq is used for priority queues (Greedy & A*)
import itertools                # itertools used to generate unique counters for tie-breaking


# Maze class
class Maze:
    def __init__(self, maze_map):
        self.height = len(maze_map)                           # total number of rows in the maze
        self.width = max(len(line) for line in maze_map)      # maximum width of the maze

        self.walls = set()    # set to store wall positions
        self.start = None     # variable to store start point (A)
        self.goal = None      # variable to store goal point (B)

        # loop through each row and column of the maze map
        for i, row in enumerate(maze_map):
            for j, col in enumerate(row):
                if col == "A":             # if current cell is 'A'
                    self.start = (i, j)    # mark it as start
                elif col == "B":           # if current cell is 'B'
                    self.goal = (i, j)     # mark it as goal
                elif col == "#":           # if current cell is '#'
                    self.walls.add((i, j)) # mark this cell as wall

        # validation: both start and goal must exist
        if self.start is None or self.goal is None:
            raise Exception("Maze must have a start (A) and goal (B)")


    # neighbors function: returns all valid moves from a given position
    def neighbors(self, state):
        x, y = state  # current position
        # possible directions with their new coordinates
        candidates = [
            ("up", (x - 1, y)),
            ("down", (x + 1, y)),
            ("left", (x, y - 1)),
            ("right", (x, y + 1)),
        ]

        result = []  # list to store valid neighbors
        for action, (nx, ny) in candidates:
            # check if move is inside the maze and not a wall
            if 0 <= nx < self.height and 0 <= ny < self.width and (nx, ny) not in self.walls:
                result.append((action, (nx, ny)))  # add valid neighbor
        return result


# Node class: represents a state in the search tree
class Node:
    def __init__(self, state, parent, action, cost):
        self.state = state      # current position in the maze
        self.parent = parent    # reference to parent node
        self.action = action    # action taken to reach this state
        self.cost = cost        # cost so far (used in A*)


# heuristic function: Manhattan distance between two points
def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)  # distance = |x1-x2| + |y1-y2|


# solve function: solves the maze using chosen algorithm
def solve(maze, algorithm="bfs"):
    start = maze.start   # starting point
    goal = maze.goal     # goal point
    counter = itertools.count()  # unique counter for tie-breaking in heapq

    # choose data structure for frontier depending on algorithm
    if algorithm == "dfs":
        frontier = [Node(start, None, None, 0)]  # stack for DFS
    elif algorithm == "bfs":
        frontier = deque([Node(start, None, None, 0)])  # queue for BFS
    elif algorithm in ("greedy", "astar"):
        frontier = []  # priority queue
        heapq.heappush(frontier, (0, next(counter), Node(start, None, None, 0)))
    else:
        raise ValueError("Unknown algorithm")  # if algorithm is not recognized

    explored = set()  # set of already visited states

    # loop until frontier is empty
    while frontier:
        # choose node based on algorithm type
        if algorithm == "bfs":
            node = frontier.popleft()       # BFS: remove from front (queue)
        elif algorithm == "dfs":
            node = frontier.pop()           # DFS: remove from end (stack)
        else:
            _, _, node = heapq.heappop(frontier)  # Greedy/A*: remove lowest priority node

        # check if goal is reached
        if node.state == goal:
            actions = []      # list of actions (up, down, left, right)
            path_coords = []  # list of coordinates forming the path
            # backtrack from goal to start
            while node.parent is not None:
                actions.append(node.action)
                path_coords.append(node.state)
                node = node.parent
            actions.reverse()       # reverse because we traced backward
            path_coords.reverse()
            return actions, path_coords  # return solution

        explored.add(node.state)  # mark current node as explored

        # expand neighbors of current node
        for action, neighbor in maze.neighbors(node.state):
            if neighbor not in explored:  # skip already visited
                child = Node(neighbor, node, action, node.cost + 1)  # create child node
                if algorithm == "dfs":
                    frontier.append(child)  # push onto stack
                elif algorithm == "bfs":
                    frontier.append(child)  # enqueue into queue
                elif algorithm == "greedy":
                    priority = heuristic(neighbor, goal)  # greedy uses heuristic only
                    heapq.heappush(frontier, (priority, next(counter), child))
                elif algorithm == "astar":
                    priority = child.cost + heuristic(neighbor, goal)  # A* = cost + heuristic
                    heapq.heappush(frontier, (priority, next(counter), child))

    return None, None  # no solution found


# function to print maze with optional solution path
def print_maze(maze_map, path_coords=None):
    visual = [list(row) for row in maze_map]  # convert maze map to 2D list
    if path_coords:  # if solution path exists
        for x, y in path_coords:
            if visual[x][y] not in ("A", "B"):  # don't overwrite start or goal
                visual[x][y] = "."  # mark solution path with '.'
    # print maze row by row
    for row in visual:
        print("".join(row))
    print("\n")  # extra line for better readability


# main function
def main():
    # maze map design
    maze_map = [
        "##########",
        "#A      B#",
        "#  ##  ###",
        "#        #",
        "##########"
    ]

    maze = Maze(maze_map)  # create Maze object

    # run solver with different algorithms
    for algo in ["dfs", "bfs", "greedy", "astar"]:
        solution, path_coords = solve(maze, algorithm=algo)  # solve maze
        print(f"{algo.upper()} solution: {solution}")        # print solution actions
        print("Path visualization:")
        print_maze(maze_map, path_coords)                    # print maze with path


# run main function
if __name__ == "__main__":
    main()
