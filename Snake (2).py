from tkinter import *
import random

gameWidth = 900
gameHeight = 600
gameSpeed = 100
itemSize = 30
bodyWidth = 2
bodyColor = "lime"
foodColor = "red"
backgroundColor = "black"

def mainLoop():
    global snake, Food, direction, points, pointsIncrement

    def snakeTurn(snake, food):
        a, b = snake.coordonate[0]

        if direction == "up":
            b -= itemSize
        elif direction == "down":
            b += itemSize
        elif direction == "left":
            a -= itemSize
        elif direction == "right":
            a += itemSize

        snake.coordonate.insert(0, (a, b))
        cube = tablou.create_rectangle(a, b, a + itemSize, b + itemSize, fill = bodyColor)
        snake.cubes.insert(0, cube)
        if a == food.coordonate[0] and b == food.coordonate[1]:
            global points
            points += 1
            pointsIncrement.config(text="Points:{}".format(points))
            tablou.delete("food")
            food = Food()

        else:
            del snake.coordonate[-1]
            tablou.delete(snake.cubes[-1])
            del snake.cubes[-1]

        if checkCollisions(snake):
            gameOver()
        else:
            snakeGUI.after(gameSpeed, snakeTurn, snake, food)

    def changeMovement(newDirection):
        global direction

        if newDirection == "left":
            if direction != "right":
                direction = newDirection
        elif newDirection == "right":
            if direction != "left":
                direction = newDirection
        elif newDirection == "up":
            if direction != "down":
                direction = newDirection
        elif newDirection == "down":
            if direction != "up":
                direction = newDirection

    def checkCollisions(snake):
        a, b = snake.coordonate[0]

        if a < 0 or a >= gameWidth:
            return True
        elif b < 0 or b >= gameHeight:
            return True
        for snake_body in snake.coordonate[1:]:
            if a == snake_body[0] and b == snake_body[1]:
                return True

    def gameOver():
        tablou.delete(ALL)
        tablou.create_text(tablou.winfo_width() / 2, tablou.winfo_height() / 2, font=("gameplay", 90), text="GAME OVER",
        fill="red", tag="Game Over")


    class snake:
        def __init__(self):
            self.body_size = bodyWidth
            self.coordonate = []
            self.cubes = []

            for i in range(0, bodyWidth):
                self.coordonate.append([0, 0])

            for a, b in self.coordonate:
                cube = tablou.create_rectangle(a, b, a + itemSize, b + itemSize, fill=bodyColor, tag="snake")
                self.cubes.append(cube)

    class Food:
        def __init__(self):
            a = random.randint(0, (gameWidth / itemSize) - 1) * itemSize
            b = random.randint(0, (gameHeight / itemSize) - 1) * itemSize

            self.coordonate = [a, b]
            tablou.create_oval(a, b, a + itemSize, b + itemSize, fill=foodColor, tag="food")

    snakeGUI = Tk()
    snakeGUI.title("Snake")
    snakeGUI.resizable(False, False)

    points = 0
    direction = "down"

    pointsIncrement = Label(snakeGUI, text = "Score:{}".format(points), font = ("consolas", 40))
    pointsIncrement.pack()

    tablou = Canvas(snakeGUI, bg = backgroundColor, height = gameHeight, width = gameWidth)
    tablou.pack()

    snakeGUI.update()

    snakeGUI_width = snakeGUI.winfo_width()
    snakeGUI_height = snakeGUI.winfo_height()
    screen_width = snakeGUI.winfo_screenwidth()
    screen_height = snakeGUI.winfo_screenheight()

    a = int((screen_width / 2) - (snakeGUI_width / 2))
    b = int((screen_height / 2) - (snakeGUI_height / 2))

    snakeGUI.geometry(f"{snakeGUI_width}x{snakeGUI_height}+{a}+{b}")

    snakeGUI.bind("<Left>", lambda event: changeMovement("left"))
    snakeGUI.bind("<Right>", lambda event: changeMovement("right"))
    snakeGUI.bind("<Up>", lambda event: changeMovement("up"))
    snakeGUI.bind("<Down>", lambda event: changeMovement("down"))

    snake = snake()
    food = Food()

    snakeTurn(snake, food)

    snakeGUI.mainloop()

mainLoop()