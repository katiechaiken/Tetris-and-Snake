#I used a mix of the starter code that was already on the notes on the website 
# and the code we developed in class
#https://pd43.github.io/notes/notes4-4.html
from tkinter import *
import random

def rgbString(red, green, blue): 
    return "#%02x%02x%02x" % (red, green, blue)
    
scoreSave = [] #global variable so the score is not reset each restart

def init(data):
    data.rows = 10
    data.cols = 10
    data.margin = 35
    data.cellSize = 30
    data.direction = (0, -1)
    loadSnakeBoard(data)
    placeFood(data)
    data.gameOver = False
    data.paused = False
    data.debugMode = False
    data.score = 0
    data.moveCount  = 0
    data.poisonCount = 0
    data.wallPresent = False
    data.wallCount = 0
    data.level = "1"
    data.timerDelay = 500
 
def loadSnakeBoard(data):
    data.board = []
    for row in range(data.rows): data.board += [[0]*data.cols]
    headRow = (len(data.board)) // 2
    headCol = len(data.board[0]) // 2
    data.board[headRow][headCol] = 1
    data.headRow = headRow
    data.headCol = headCol
 
def mousePressed(event, data):
    x=event.x - data.margin
    y=event.y - data.margin
    gridW = (data.width-data.margin)//data.rows
    gridH = (data.height-(data.margin*2))//data.cols
    col=(x//gridW)
    row=(y//(gridH))
    if (data.board[row][col]==0 and (data.paused==True)):
        data.board[row][col]=-3
        data.wallCount += 1
        data.wallPresent = True
    elif (data.board[row][col]==-3 and (data.paused==True)):
        data.board[row][col]=0
        data.wallCount -= 1
        if(data.wallCount > 0): data.wallCount = True
        else: data.wallCount = False
 
def keyPressed(event, data):
    if (event.char == "r"): 
        init(data);
        return
    elif (event.char == "p"): data.paused = not data.paused; return
    elif (event.char == "d"):
        data.debugMode = not data.debugMode
    if (data.gameOver or data.paused): return
    if (event.keysym == "Left"): data.direction = (0, -1)
    elif (event.keysym == "Right"): data.direction = (0,  1)
    elif (event.keysym == "Up"): data.direction = (-1, 0) 
    elif (event.keysym == "Down"): data.direction = ( 1, 0)
    takeStep(data)
 
def timerFired(data):
    if (data.paused or data.gameOver): return
    takeStep(data)
    if(data.score == 3): #level up so snake moves faster with smaller timerDelay
        data.timerDelay = 250 #goes 2x faster than level 1 
        data.level = "2"        
        #when level 1 ends if wall was around for min 20 times get bonus point
        if(data.wallCount >= 20): 
            data.score += 1
            data.wallCount = 0

 
def takeStep(data):
    (drow, dcol) = data.direction
    (headRow, headCol) = (data.headRow, data.headCol)
    (newHeadRow, newHeadCol) = (headRow + drow, headCol + dcol)
    if ((newHeadRow < 0) or (newHeadRow >= data.rows) or
        (newHeadCol < 0) or (newHeadCol >= data.cols) or
        data.board[newHeadRow][newHeadCol] > 0 or
        data.board[newHeadRow][newHeadCol] == -2): #any case the snake dies
            scoreSave.append(data.score)
            data.gameOver = True
    elif (data.board[newHeadRow][newHeadCol] == -1):
        # eat food
        data.board[newHeadRow][newHeadCol]= data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        placeFood(data)
        data.score += 1 #increase score
        if(data.score > 2 and data.poisonCount == 0): 
            placePoison(data)
            data.poisonCount += 1
            #wallCount looks for the 20 times the wall is present without being
            #hit so a bonus may be applied once for each level
        if(data.wallPresent == True): data.wallCount += 1
    elif(data.board[newHeadRow][newHeadCol] == -3):
        if(data.score >= 0):
            data.score -= 1
            data.board[newHeadRow][newHeadCol] = 0
            data.moveCount += 1
            if(data.score == -1):
                scoreSave.append(0)
                data.gameOver = True
            if(data.wallPresent == True): data.wallCount += 1
    else:
        # didn't eat, so remove old tail (move forward)
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        removeTail(data)
        if(data.score > 2 and data.poisonCount == 0): 
            placePoison(data)
            data.poisonCount += 1
        data.moveCount += 1
        if(data.wallPresent == True): data.wallCount += 1

 
def placeFood(data):
    row = random.randint(0, data.rows - 1)
    col = random.randint(0, data.cols - 1)
    while data.board[row][col] != 0:
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)
    data.board[row][col] = -1

def placePoison(data):
    cols=len(data.board[0])
    rows=len(data.board)
    while True:
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)
        if (data.board[row][col]==0 or data.board[row][col]==-1
        or data.board[row][col]==-3):
            break
        elif((abs(data.headRow-row)<=1)and (abs(data.headCol-col)<=1)):
            break #make sure at least one square away fro mhead
    data.board[row][col] = -2
    
def removeTail(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] > 0:
                data.board[row][col] -= 1
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawSnakeCell(canvas, data, row, col)

#finds the max 3 highest scores and orders them from greatest to least
def highScore(score):
    scoreSave.sort()
    while(len(scoreSave) > 3):
        scoreSave.pop(0)
    scoreSave.reverse()
#formats the high scores for when they are printed when the game ends
def formatHighScore(score):
    result = ""
    for i in range(len(scoreSave)):
        result = result + str(scoreSave[i]).strip("[]") + "\n"
    return result
def drawSnakeCell(canvas, data, row,col):
    gridWidth,gridHeight=data.width - 2*data.margin, data.height - 2*data.margin
    cellWidth, cellHeight = gridWidth / data.cols, gridHeight / data.rows
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
    if(data.paused):
        canvas.create_rectangle(x0, y0, x1, y1,fill=rgbString(242, 242, 242),
        outline=rgbString(38,38,38))
    if data.board[row][col] > 0:
        # draw snake body
        canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline = "blue")
        if(data.paused): 
            canvas.create_rectangle(x0, y0, x1, y1, fill=rgbString(0,38,153))
    if data.board[row][col] == -1:
        # draw food
        canvas.create_rectangle(x0, y0, x1, y1,fill="green", outline = "black")
        if(data.paused):
           canvas.create_rectangle(x0, y0, x1, y1,fill=rgbString(0, 204, 0))
    if data.board[row][col] == -2:
        # draw food
        canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline = "black")
        if(data.paused):
           canvas.create_rectangle(x0, y0, x1, y1, fill=rgbString(204, 41, 0))
    if (data.board[row][col]==-3):
        #draw wall
        canvas.create_rectangle(x0, y0, x1, y1, fill = rgbString(153, 77, 0))
        if(data.paused):
            canvas.create_rectangle(x0,y0,x1,y1, fill = rgbString(128, 64, 0))
    if (data.debugMode):
        canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
                           text=str(data.board[row][col]),
                           font=("Helvetica", 14, "bold"))

def redrawAll(canvas, data):
    if (data.gameOver):
        highScore(scoreSave)
        canvas.create_text(data.width/2, data.height/6, text="Game Over!", 
                           font=("Helvetica", 40, "bold"))
        canvas.create_text(data.width/2, data.height/3, text="High Scores", 
                           font=("Helvetica", 32, "bold underline"))
        canvas.create_text(data.width/2, data.height/1.6,
        text = formatHighScore(scoreSave), font=("Helvetica", 29, "bold"), 
        anchor = "center")
        canvas.create_text(data.width/2, data.height/1.1,
        text = "Press 'r' to restart", font =("Helvetica", 16))
    else:
        drawBoard(canvas, data)
        canvas.create_text(data.width//3, data.margin, text = "Score: " +
        str(data.score), anchor = "s", font = ("Helvetica", 30))
        canvas.create_text((2*data.width)//3, data.margin,text = "Level: " +
        data.level, anchor = "s", font = ("Helvetica", 30))
        canvas.create_text(data.width//2, data.height-20, 
        text = "Press 'p' to pause, 'r' to restart, and 'd' for debug mode", 
        font = ("Helvetica", 20), anchor = "center")


 
####################################
# use the run function as-is
####################################
 
def run(width=600, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.timerDelay = 500 # milliseconds
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
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

 
run()