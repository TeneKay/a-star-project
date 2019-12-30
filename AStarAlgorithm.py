import pygame, sys, random, math, time, random, traceback

#   What is this?
#   It's just a project I've been working on for a couple of days now after I got intrigued by pathfinding algorithms.
#   I also wanted to put my Python skills to the test.
#   @author : Gabriel A.

# Node represents each individual Node on the grid
# I also refer to this as 'Node' in other parts of the code

# Colours
class Colours:
    obstacleColour = (30, 30, 30)
    normalColour = (255, 255, 255)
    startNodeColour = (0, 255, 255)
    endNodeColour = (255, 255, 0)
    openListColour = (0, 255, 0)
    pathColour = (255, 0, 0)

class Node:
    def __init__(self, position, parent=None):
        self.g = 0
        self.h = 0
        self.f = 0
        self.obstacle = False
        self.colour = (255,255,255)
        self.position = position
        self.parent = parent
        self.important = False
        self.name = None

    # @override
    def __str__(self):
        if self.important == True:
            return str(self.name)
        else:
            return str(self.f)

    # Calculate g, h, f costs for the current Node
    def calculateCosts(self, parentNode, endNode):
        # Get the tuple-difference between the current Node and parent / end Node
        pDiff = (abs(self.position[0] - parentNode.position[0]), abs(self.position[1] - parentNode.position[1]))
        eDiff = (abs(endNode.position[0] - self.position[0]), abs(endNode.position[1] - self.position[1]))

        # Perform pythagoras theorem to find the distances and assign accordingly
        self.g = parentNode.g + round(math.sqrt((pDiff[0] ** 2) + (pDiff[1] ** 2)), 1) * 10
        self.h = round(math.sqrt((eDiff[0] ** 2) + (eDiff[1] ** 2)), 1) * 10
        self.f = self.g + self.h

        # testing
        # print("Node: {0} has g: {1}, h: {2}, f: {3}".format(self.position, self.g, self.h, self.f))

class Grid:
    def __init__(self, w, h, s, m):
        self.width = w
        self.height = h
        self.blockSize = s
        self.blockMargin = m
        self.inArray = [[Node((j,i)) for i in range(self.width)] for j in range(self.height)]

        # Fix the hard-coding after testing
        self.startNode = self.inArray[random.randint(0, h-1)][random.randint(0, w-1)]
        self.startNode.colour = Colours.startNodeColour
        self.startNode.important = True
        self.startNode.name = "START"
        self.endNode = self.inArray[random.randint(0, h-1)][random.randint(0, w-1)]
        self.endNode.colour = Colours.endNodeColour
        self.endNode.important = True
        self.endNode.name = "END"

class GUI:
    def __init__(self, grid, width, height, blocksize, margin):
        pygame.init()
        pygame.display.set_caption('A* Pathfinding Algorithm')
        pygame.font.init()
        # Colours
        self.font = pygame.font.SysFont("Comic Sans MS", 10)

        self.window = pygame.display.set_mode((width * (blocksize + margin), height * (blocksize + margin)))
        self.window.fill((0, 0, 102))
        self.drawGrid(grid)

    def drawGrid(self, grid):
        for i in range(grid.height):
            for j in range(grid.width):
                # Draw the square Node
                Node = grid.inArray[i][j]
                square = pygame.Rect(i * (grid.blockSize + grid.blockMargin), j * (grid.blockSize + grid.blockMargin), grid.blockSize, grid.blockSize)
                pygame.draw.rect(self.window, Node.colour, square)

                if Node.f == 0 and Node.important == False:
                    continue
                # Draw font
                textSurface = self.font.render(str(Node), False, (0,0,0))
                self.window.blit(textSurface, square)
        pygame.display.update()

    def mainLoop(self, grid, w, h):
        self.drawGrid(grid)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    x = (mousePos[0]) // (grid.blockSize + grid.blockMargin)
                    y = (mousePos[1]) // (grid.blockSize + grid.blockMargin)
                    #print("w: " + str(mousePos[0]), ", h: " + str(mousePos[1]))
                    self.updateGrid(grid, x, y, w, h)
                    self.drawGrid(grid)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        AStar(grid, grid.startNode, grid.endNode)
                    if event.key == pygame.K_ESCAPE:
                        grid.__init__(grid.width, grid.height, grid.blockSize, grid.blockMargin)
                    self.drawGrid(grid)

    def changeColour(Node, colour):
        if Node.important == False:
            Node.colour = colour
        else:
            return
    # Allows placement of obstacles
    def updateGrid(self, grid, x, y, w, h):
        if x >= w: x -= 1
        if y >= h: y -= 1
        Node = grid.inArray[x][y]
        if Node.important == True:
            return
        if Node.obstacle == False:
            Node.obstacle = True
            Node.colour = Colours.obstacleColour
        else:
            Node.obstacle = False
            Node.colour = Colours.normalColour

def AStar(grid, startNode, endNode):
    print("Starting A*..."); print("Starting Timer...")
    startTime = time.time()

    # Lists storing all Nodes / Nodes of interest
    open = []
    closed = []
    adjacentNodes = []

    # Begin with the start Node
    open.append(startNode)
    startNode.calculateCosts(startNode, endNode)

    # A* will run while we still have Nodes to look at
    while len(open) > 0:
        currentNode = open[0]
        currentIndex = 0

        # Loop through the open list of Nodes,
        # Then select the one with the lowest f-cost.
        # If currentNode's f-cost is the same as the openNode's f-cost,
        # Then pick the one with the lowest h-cost.
        for i in range(len(open)):
            if open[i].f < currentNode.f:
                currentNode = open[i]
                currentIndex = i
            elif open[i].f == currentNode.f:
                if open[i].g < currentNode.g:
                    currentNode = open[i]
                    currentIndex = i


        # Pop from open list, add to closed list
        open.pop(currentIndex)
        closed.append(currentNode)

        # If we have reached the end Node, back-track and display the path
        if currentNode == endNode:
            ptr = currentNode
            while ptr != None:
                GUI.changeColour(ptr, Colours.pathColour)
                ptr = ptr.parent
            print("A* runtime: {0} seconds".format(time.time() - startTime))
            return

        for adjacentNode in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:

            node0 = currentNode.position[0] + adjacentNode[0]
            node1 = currentNode.position[1] + adjacentNode[1]
            # Stay within range
            if (node0 >= 0 and node0 < len(grid.inArray[0])) and (node1 >= 0 and node1 < len(grid.inArray)):
                # Get the grid-node associated with each adjacent node tuple
                newNode = grid.inArray[currentNode.position[0] + adjacentNode[0]][currentNode.position[1] + adjacentNode[1]]

                if newNode.obstacle == True: continue
                adjacentNodes.append(newNode)

        # For every adjacent node, if we hven't checked it before
        # Then calculate the costs and visually represent it
        for node in adjacentNodes:
            if (previouslyChecked(node, closed, open)):
                continue
            node.calculateCosts(currentNode, endNode)
            GUI.changeColour(node, Colours.openListColour)
            for i in range(len(open)):
                if node == open[i] and node.g > open[i].g:
                    continue
            node.parent = currentNode
            open.append(node)
    print("Path not found")

# Checks if node is within open or closed list
def previouslyChecked(node, closed, open):
    for a in closed:
        if node == a:
            return True
    for a in open:
        if node == a:
            return True

def main():
    # Constants
    WIDTH = 20
    HEIGHT = 20
    BLOCKSIZE = 40
    MARGIN = 2

    ans = input("\nDo you want to enter custom Grid Values? Y/N\n")
    if ans.lower() == "y" or ans.lower() == "yes":
        WIDTH = int(input("\nPlease enter width amount (x-axis range. Default is 20): \n"))
        HEIGHT = int(input("\nPlease enter height amount (y-axis range. Default is 20): \n"))
        BLOCKSIZE = int(input("\nPlease enter blocksize (size of each individual cell. Default is 20): \n"))
        MARGIN = int(input("\nPlease enter the margin amount (how much space between each cell. Default is 2): \n"))
    else:
        print("\nGoing to take default values.\n")
        print("\nControls:\n\n\nClick to place/delete obstacles.\nSpace to start A* Algorithm.\nEscape to clear screen.\n")
        time.sleep(5)

    try:
        grid = Grid(WIDTH, HEIGHT, BLOCKSIZE, MARGIN)
        gui = GUI(grid, WIDTH, HEIGHT, BLOCKSIZE, MARGIN)

        gui.mainLoop(grid, WIDTH, HEIGHT)
    except:
        logfile = open("mostRecentCrash.txt", "w")
        traceback.print_exc(file=logfile)
    finally:
        pygame.quit()
        sys.exit()

# Run it!
if __name__ == "__main__":
    main()
