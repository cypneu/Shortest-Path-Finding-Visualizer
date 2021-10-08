import pygame
import bfs, dijkstra, bellman_ford, a_star
from random import randint
from time import sleep
from config import *

class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.y = row * size
        self.x = col * size
        self.color = white
        self.size = size
        
    def addPosCost(self):
        self.cost = randint(0, 999)
    
    def addNegPosCost(self):
        self.cost = randint(-15, 999)

    def display(self, win):
        pygame.draw.rect(win, self.color, (self.y, self.x, self.size, self.size))
    

def drawSquare(win, node):
    node.display(win)
    pygame.draw.line(win, grey, (0, node.col * spacing), (size, node.col * spacing))
    pygame.draw.line(win, grey, (node.row * spacing, 0), (node.row * spacing, size))


def drawBoard(win, board):
    win.fill(white)
    for i in range(rows):
        board[i][0].color = black
        board[0][i].color = black
        board[rows - 1][i].color = black
        board[i][rows - 1].color = black
    
    cntBlacks = 0
    for i in range(rows):
        for j in range(rows):
            node = board[i][j]
            node.display(win)
            if node.color == black:
                cntBlacks += 1
    

    for i in range(rows):
        pygame.draw.line(win, grey, (0, i * spacing), (size, i * spacing))
        pygame.draw.line(win, grey, (i * spacing, 0), (i * spacing, size))

    pygame.display.update()
    return cntBlacks


def clickedPos(pos):
    x, y = pos
    row, col = x // spacing, y // spacing
    return row, col
    


def main():
    pygame.font.init()
    win = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Shortest Path Finding Algorithms")
    board = [[Node(i, j, size // rows) for j in range(rows)] for i in range(rows)]
  

    startNode = None
    endNode = None
    running = True
    while running:
        cntBlacks = drawBoard(win, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed()[0]:
                row, col = clickedPos(pygame.mouse.get_pos())
                node = board[row][col]
                if node.color != black:
                    if not startNode:
                        startNode = node
                        startNode.color = yellow
                    
                    elif not endNode and node != startNode:
                        endNode = node
                        endNode.color = purple

                    elif node != endNode and node != startNode:
                        node.color = black
            
            elif pygame.mouse.get_pressed()[2]:
                row, col = clickedPos(pygame.mouse.get_pos())
                node = board[row][col]
                node.color = white
                if node == startNode:
                    startNode = None
                elif node == endNode:
                    endNode = None

            if event.type == pygame.KEYDOWN:
                if startNode and endNode:
                    foundPath = None
                    if event.key == pygame.K_b: 
                        foundPath = bfs.BFS(lambda: drawBoard(win, board), board, startNode, endNode)

                    elif event.key == pygame.K_d:
                        for i in range(rows):
                            for j in range(rows):
                                board[i][j].addPosCost()
                        foundPath = dijkstra.dijkstra(lambda: drawBoard(win, board), board, startNode, endNode)
                            
                    elif event.key == pygame.K_f:
                        for i in range(rows):
                            for j in range(rows):
                                board[i][j].addNegPosCost()
                        foundPath = bellman_ford.BellmanFord(lambda: drawBoard(win, board), win, board, startNode, endNode, cntBlacks)
                        if foundPath == False:
                            myFont = pygame.font.SysFont("Comic Sans MS", 50)
                            text = myFont.render("The negative cycle has occured!", True, green)
                            win.blit(text, (size // rows + 25 , size // 2))
                            pygame.display.update()
                            sleep(4)

                    
                    if not foundPath:
                        sleep(0.5)
                        startNode, endNode = None, None
                        board = [[Node(i, j, size // rows) for j in range(rows)] for i in range(rows)]
                        

                if event.key == pygame.K_r:
                    startNode, endNode = None, None
                    board = [[Node(i, j, size // rows) for j in range(rows)] for i in range(rows)]

    pygame.quit()



if __name__ == "__main__":
    main()