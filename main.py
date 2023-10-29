from typing import List, Tuple
import math, random
from dataclasses import dataclass
import pygame

TICK_MAX = 100

@dataclass
class Automaton:
    rule: int
    width: int

def generateAutomaton():
    rule = random.randrange(0, 256)
    width = random.randrange(3, 20)

    return Automaton(rule, width)

def applyRule(ruleArray, left, middle, right):
        index = 0b000
        if left:   index ^= 0b001  # 0b000 -> 0b001
        if middle: index ^= 0b010  # 0b000 -> 0b010
        if right:  index ^= 0b100  # 0b000 -> 0b100
        return ruleArray[index], index

@dataclass
class Event:
    pass

@dataclass
class Simulation:
    width: int
    height: int
    enemyGrid: List[List[int]]
    automatonGrid: List[List[int]]
    automaton: Automaton
    cooldown: int
    wall: int

    def __init__(self, gridWidth: int, gridHeight: int):
        self.width = gridWidth
        self.height = gridHeight
        self.automaton = generateAutomaton()
        self.enemyGrid = [[0 for _ in range(gridHeight + 1)] for _ in range(gridHeight + 1)]
        self.automatonGrid = [[0 for _ in range(gridHeight + 1)] for _ in range(gridHeight + 1)]
        self.cooldown = 0
        self.wall = 5

    def tickSimulation(self, mousePos: None | Tuple[int, int], hasClicked: bool, tick: int):
        self.automatonGrid = [[0 for _ in range(self.width + 1)] for _ in range(self.height + 1)]
        if (tick % 5 == 0):
            for col in range(1, self.width + 1):
                for row in range(self.height + 1):
                    self.enemyGrid[col - 1][row] = self.enemyGrid[col][row]
            
            enemies = 0
            for row in range(self.height + 1):
                enemies += self.enemyGrid[self.wall - 1][row]

            if (enemies != 0):
                self.wall += 1
            
        self.enemyGrid[self.wall+1]



        if (tick % 2 == 0):
            if (random.random() > 0.5):
                enemyRow = random.randrange(self.height // 2, self.height)
                self.enemyGrid[self.width-1][enemyRow] = 1
        
        self.cooldown = max(0, self.cooldown - 1)
        # Setup Automaton

        if (mousePos and self.cooldown == 0):

            (gx, gy) = mousePos 

            for xpos in range(gx - (self.automaton.width - 1)//2, gx +  self.automaton.width //2):
                if (self.width > xpos >= 0):
                    self.automatonGrid[xpos][0] = 1

            ruleArray = [self.automaton.rule >> i & 1 for i in range(8)]
            # print(self.automaton.rule, self.automaton.width, ruleArray)

            for row in range(1, self.height+1):
                for col in range(0, self.width):
                    left = middle = right = 0
                    if col - 1 >= 0:
                        left = self.automatonGrid[col-1][row - 1]

                    middle = self.automatonGrid[col][row - 1]

                    if col + 1 < self.width:
                        right = self.automatonGrid[col + 1][row - 1]
                    
                    cellState, index = applyRule(ruleArray, left, middle, right)
                    # print(((row, col), left, middle, right, cellState, index), " ", end="")
                    self.automatonGrid[col][row] = cellState

                    if cellState and hasClicked:
                        self.enemyGrid[col][row] = 0
        
        if (hasClicked):
            self.cooldown = 10
            self.automaton = generateAutomaton()


                
def printGrid(sim: Simulation):
    for row in range(sim.width + 1):
        for col in  range(sim.height + 1):
            print(sim.grid[row][col], end="")
        print()

COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (30, 30, 30)
COLOR_RED_GREY = (50, 30, 30)
COLOR_RED = (255, 000, 000)
COLOR_BLACK = (000, 000, 000)

# ff8274
COLOR_LIGHT_PINK = (255, 130, 116)
# d53c6a
COLOR_PINK = (213, 60, 106)

#7c183c
COLOR_DARK_PINK = (124, 24, 60)

#460e2b
COLOR_PURPLE = (70, 14, 43)

#31051e
COLOR_DARK_PURPLE = (49, 5, 30)

#1f0510
COLOR_DARKER_PURPLE = (31, 5, 16)

#130208
COLOR_DARKEST_PURPLE = (19, 2, 8)

def main():

    gridWidth = 50
    gridHeight = 50

    cellWidth = 10
    cellHeight = 10

    headerHeight =  0
    
    pygame.init()
    pygame.display.set_caption("The Automaton")
    window = pygame.display.set_mode((gridWidth * cellWidth, cellHeight * gridHeight + headerHeight))

    running = True
    clock = pygame.time.Clock()

    sim = Simulation(gridWidth, gridHeight)

    def renderSimulation(sim):
        for row in range(sim.width):
            for col in range(sim.height):
                cellValue = sim.automatonGrid[row][col]
                rectCoords = (row * cellWidth, col * cellHeight + headerHeight, cellWidth, cellWidth) 
                color = COLOR_DARKEST_PURPLE
                if cellValue:
                    if hasClicked:
                        color = COLOR_DARK_PINK 
                    else:
                        color = COLOR_DARK_PURPLE
                pygame.draw.rect(window, color, rectCoords)

                if (sim.enemyGrid[row][col]):
                    pygame.draw.rect(window, COLOR_LIGHT_PINK, rectCoords)

                if (row < sim.wall):
                    pygame.draw.rect(window, COLOR_PINK, rectCoords)


    tick = 0


    while running:
        clock.tick(10)
        pos = pygame.mouse.get_pos()
        mousePos = (math.floor(pos[0] / cellWidth), math.floor((pos[1] - headerHeight) / cellHeight))
        hasClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hasClicked = True

        tick+= 1
        tick %= TICK_MAX 

        sim.tickSimulation(mousePos, hasClicked, tick)
        renderSimulation(sim)

        pygame.display.update()

        
        


if __name__ == "__main__":
    main()