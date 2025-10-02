import os    #import sys allows the program to read input from the command line


print(os.getcwd())  # Get the current working directory (cwd)
print(os.listdir())  # Get the list of all files and directories in the cwd

if(os.path.exists("maze.txt")):    
    print("maze.txt , is present")
else:
    print("maze.txt , is missing")

class Node():      
    def __init__(self,state, parent ,action):
        self.state=state
        self.parent=parent
        self.action = action

class StackFrontier():
    def __init__(self):
        """This frontier is like a to do list of nodes to explore
        Here we use a python list to store nodes."""
        self.frontier=[]

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self,state):
        """
        check if a given state (row,col) is already in the frontier .
        Prevents adding duplication nodes.
        """
        #return any(node.state == state for node in self.frontier)
        for node in self.frontier:         # har node ko frontier me dekho
            if node.state == state:        # agar uska state given state ke barabar hai
                return True                # matlab already frontier me hai
            return False                       # agar kahin match na mile to False


    def empty(self):
        """check if a frontier is empty or not."""
        return len(self.frontier) == 0

    def remove (self):
        """
        Remove and return the last node .
        """
        if self.empty():
            raise ValueError("empty Frontier")
        else:
            node=self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
          
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise ValueError("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self,filename):

        with open(filename) as f:
            contents=f.read()
    
        if contents.count("A") != 1:
            raise ValueError ("Maze must have exactly on start point ")
        if contents.count("B") != 1:
            raise ValueError("Maze must have exactly one gole")
    
        #determine heighte and width of maze
        #first split the maze into lines
    
        contents=contents.splitlines()
    
        #get height(rows) & width (column)
    
        self.height=len(contents)
        self.width= max(len(line) for line  in contents)
    
        #Bulit a 20 grid of walls
        #True = wall
        #False = freespace
        #Slove the position of A.(Start) and B (gole)

        self.wall=[]
    
        #Loop over every row of maze.txt file
    
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j] =="A":
                        self.state=(i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:  #wall
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.wall.append(row)
        self.solution = None


    def print_maze(self):
            if self.solution is not None:
                solution = self.solution[1]
            else:
                solution = None
        
            print()
            for i, row in enumerate(self.wall):
                for j, col in enumerate(row):
                    if col:
                        print("█", end="")
                    elif (i, j) == self.state:
                        print("A", end="")
                    elif (i, j) == self.goal:
                        print("B", end="")
                    elif solution is not None and (i, j) in solution:
                        print("*", end="")
                    else:
                        print(" ", end="")
                print()
            print()

    def neighbors(self, state):
        row, col = state   #if  state is (2, 3) then row =2, col = 3
        candidates = [  #up, down, left, or right  store as tuple
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.wall[r][c]:# not self.walls[r][c]target cell is not a wall
                result.append((action, (r, c)))
        return result
    
    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.state, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new("RGBA", (self.width * cell_size, self.height * cell_size), "black")
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.wall):
            for j, col in enumerate(row):
                
                if col:
                    fill = (40, 40, 40)        # wall → dark gray
                elif (i, j) == self.state:
                    fill = (255, 0, 0)         # start (A) → red
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)        # goal (B) → green
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)     # solution path → yellow
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)       # explored nodes → orange
                else:
                    fill = (237, 240, 252)     # empty cell → light gray   
                    # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill                )

        img.save(filename)

# Maze object ko apni file se load karo
maze_file = "maze.txt"   # make sure ye file tumhare notebook ke folder me ho
m = Maze(maze_file)
print("Maze:")
m.print_maze()
print("Solving...")
m.solve()
print("Solution:")
m.print_maze()
# Maze ki image save + show
m.output_image("maze.png", show_explored=True)
from IPython.display import Image
Image("maze.png")
