# Import turtle module to draw graphics
import turtle


# This function draws one side of the shape using recursion
# length = how long the line is
# depth = how many times the pattern repeats
def draw_side(length, depth):

    # If depth is 0, stop recursion and draw a straight line3
    if depth == 0:
        turtle.forward(length)

    else:
        # Divide the line into three equal parts
        part = length / 3

        # Draw first small part
        draw_side(part, depth - 1)

        # Turn left to start inward triangle
        turtle.left(60)
        draw_side(part, depth - 1)

        # Turn right to complete the triangle
        turtle.right(120)
        draw_side(part, depth - 1)

        # Turn back to original direction
        turtle.left(60)
        draw_side(part, depth - 1)


# -------- USER INPUT SECTION --------

# Ask user for number of sides
sides = int(input("Enter number of sides: "))
while sides < 3:
    print("A polygon must have at least 3 sides.")
    sides = int(input("Enter number of sides: "))

# Ask user for side length
length = int(input("Enter side length: "))
while length <= 0:
    print("Length must be positive.")
    length = int(input("Enter side length: "))

# Ask user for recursion depth
depth = int(input("Enter recursion depth: "))
while depth < 0:
    print("Depth cannot be negative.")
    depth = int(input("Enter recursion depth: "))


# -------- TURTLE SETUP --------

# Create drawing screen
screen = turtle.Screen()
screen.bgcolor("white")

# Set turtle settings
turtle.speed(0)
turtle.pensize(2)
turtle.hideturtle()

# Turn off animation to draw faster
turtle.tracer(0, 0)


# Move turtle to a better starting position (centered)
turtle.penup()
turtle.goto(-length / 2, -length / 2)
turtle.pendown()


# -------- DRAW THE SHAPE --------

# Calculate turning angle for polygon
angle = 360 / sides

# Draw each side of the polygon
for i in range(sides):
    draw_side(length, depth)   # Draw one recursive side
    turtle.left(angle)         # Turn for next side


# Show the final drawing
turtle.update()

# Keep the window open until user closes it
turtle.done()
