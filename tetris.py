import random
import copy
from tkinter import *

#I used initial setup given in instructions
#https://www.cs.cmu.edu/~112/notes/notes-tetris/2_2_CreatingTheBoard.html
def init(data):
    data.rows = 15
    data.cols = 10
    data.margin = 20
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],[ True, True,  True]]
    lPiece = [[ False, False, True],[ True,  True,  True]]
    oPiece =  [[ True, True],[ True, True]]
    sPiece = [[ False, True, True],[ True,  True, False ]]
    tPiece = [[ False, True, False ],[ True,  True, True]]   
    zPiece = [[ True,  True, False ],[ False, True, True]]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    tetrisPieceColors = ["red", "yellow", "magenta", "pink", 
                        "cyan", "green", "orange" ]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors
    newFallingPiece(data)
    data.isGameOver=False
    data.score=0

def getCellBounds(row, col, data):
    #used code from snake demo
    #https://pd43.github.io/notes/notes4-4.html
    gridWidth  =  data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def mousePressed(event, data):
    pass
    
def keyPressed(event, data):
    if event.keysym=="r": init(data) #restart game
    if event.keysym=="Right":moveFallingPiece(data,0,1)
    if event.keysym=="Left":moveFallingPiece(data,0,-1)
    if event.keysym=="Up":rotateFallingPiece(data)
    if event.keysym=="Down":moveFallingPiece(data,1,0)

def timerFired(data):
    if (moveFallingPiece(data,1,0) == False):
        placeFallingPiece(data)
        newFallingPiece(data)
        if fallingPieceIsLegal(data)==False:
            data.isGameOver=True
    removeFullRows(data)

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)

def drawBoard(canvas, data):
    # draw grid
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col,data.board[row][col])

def drawCell(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    margin = 1  #space between cells
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+margin, y0+margin, x1-margin, y1-margin,
    fill=color)

def fallingPieceIsLegal(data):
    row=0
    col=0
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j]==True:
                row=i+data.fallingPieceRow
                col=j+data.fallingPieceCol
                if ((row<0) or (row>=data.rows) or col<0 or col>=data.cols
                   or data.board[row][col]!="blue"):
                    return False
    return True

def rotateFallingPiece(data):
    oldRows = len(data.fallingPiece)
    oldCols = len(data.fallingPiece[0])
    oldFallingPiece = data.fallingPiece
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    data.fallingPiece = [([0] * oldRows) for col in range(oldCols)]
    for row in range(oldRows):
        for col in range(oldCols):
            data.fallingPiece[oldCols-col-1][row]=oldFallingPiece[row][col]
    oldCenterRow = oldRow + (oldRows-1)//2
    oldCenterCol = oldCol + (oldCols-1)//2
    data.fallingPieceRow = oldCenterRow - (oldCols-1)//2
    data.fallingPieceCol = oldCenterCol - (oldRows-1)//2
    if (fallingPieceIsLegal(data) == False):
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
        data.fallingPiece = oldFallingPiece

                    
def moveFallingPiece(data, drow, dcol):
    oldFallingPieceRow=data.fallingPieceRow
    oldFallingPieceCol=data.fallingPieceCol
    data.fallingPieceRow=data.fallingPieceRow+drow
    data.fallingPieceCol=data.fallingPieceCol + dcol
    #if the move will be illegal
    if fallingPieceIsLegal(data)==False:
        data.fallingPieceRow=data.fallingPieceRow-drow
        data.fallingPieceCol=data.fallingPieceCol - dcol
        return False
    return True

def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col]==True: 
                rows=data.fallingPieceRow+row
                cols= data.fallingPieceCol + col
                color=data.fallingPieceColor
                data.board[rows][cols]=color

def removeFullRows(data):
    newRow = data.rows-1
    for oldRow in range(data.rows-1,-1,-1):
        for e in data.board[oldRow]:
            #if not full
            if e =="blue":
                data.board[newRow]=copy.copy(data.board[oldRow])
                newRow= newRow -1
                break
    counter = newRow+1
    data.score = data.score + counter**2
    
def newFallingPiece(data):
    data.fallingPiece= random.choice(data.tetrisPieces)
    data.fallingPieceColor=random.choice(data.tetrisPieceColors)
    data.fallingPieceRow= 0
    #center the piece
    data.fallingPieceCol = ((data.cols//2) - (len(data.fallingPiece[0])//2))

def drawFallingPiece(canvas,data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                #draw the parts of the piece that are blue
                rows=data.fallingPieceRow+row
                cols= data.fallingPieceCol + col
                drawCell(canvas,data,rows,cols,data.fallingPieceColor)  
                     
def drawScore(canvas,data):
    #keeps score
    scoreCount = "Score: " + str(data.score)
    canvas.create_text(data.width/15,data.height/45, text=scoreCount, 
    anchor = "w", font=("Helvetica",15, "bold"), fill = "blue")
    
def redrawAll(canvas, data):
    #as long as game isnt over keep on redrawing it
    if (not data.isGameOver):
        drawGame(canvas, data)
        drawFallingPiece(canvas,data)
        drawScore(canvas,data)
    else:
        canvas.create_text(data.width/2,data.height/2-40,text="Game Over")
        canvas.create_text(data.width/2,data.height/2,text="Press r to restart")



####################################
# use the run function as-is
####################################

def run(width=300, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 300 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")



run()