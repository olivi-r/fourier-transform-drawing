import json, tkinter
from os import sep

def start_drag(e):
    global points
    points = [[e.x, e.y]]


def drag(e):
    points.append([e.x, e.y])


def end_drag(e):
    def map(point):
        x = y = 0
        scl = min(dimensions)

        x = 2 * (point[0] - dimensions[0] / 2) / scl
        y = 2 * (point[1] - dimensions[1] / 2) / scl

        return [x, y]

    with open("points.json", "w+") as fp:
        json.dump([map(i) for i in points], fp, separators=(",", ":"))


def draw_loop():
    display.delete("all")
    if points:
        prev = points[0]
        for point in points:
            display.create_line(prev[0], prev[1], point[0], point[1])
            prev = point

    display.after(20, draw_loop)


dimensions = [600, 400]
root = tkinter.Tk()
root.title("Line drawer")
root.geometry(f"{dimensions[0]}x{dimensions[1]}")
root.resizable(0, 0)


dragging = False
points = []
display = tkinter.Canvas(root, highlightthickness=0, bg="#ffffff")
root.bind("<ButtonPress-1>", start_drag)
root.bind("<B1-Motion>", drag)
root.bind("<ButtonRelease-1>", end_drag)

display.pack(fill="both", expand=1)
display.after_idle(draw_loop)
root.mainloop()
