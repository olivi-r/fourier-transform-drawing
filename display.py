import math
import tkinter
import json


def discrete_fourier_transform(x):
    X = []
    N = len(x)
    for k in range(N):
        X_k = 0
        for n, x_n in enumerate(x):
            theta = 2 * math.pi * k * n / N
            X_k += x_n * (math.cos(theta) - 1j * math.sin(theta))

        X.append([k, X_k/N])

    return X


def draw_loop(display, epicycles):
    global t
    pos = 0

    cx = dimensions[0] / 2
    cy = dimensions[1] / 2

    display.delete("all")
    for f, c in epicycles:
        r = abs(c)
        a = math.atan2(c.imag, c.real)

        # create_lines
        display.create_oval(cx + pos.real - r, cy + pos.imag - r, cx + pos.real + r, cy + pos.imag + r, outline="#cccccc")

        new_pos = pos + r * math.cos(f * t + a) + 1j * r * math.sin(f * t + a)
        display.create_line(cx + pos.real, cy + pos.imag, cx + new_pos.real, cy + new_pos.imag, fill="#cccccc")
        pos = new_pos

    pattern.insert(0, new_pos)
    while len(pattern) > len(epicycles) - len(epicycles) / 10:
        pattern.pop()

    if pattern:
        prev = pattern[0]
        for pos in pattern[1:]:
            display.create_line(cx + prev.real, cy + prev.imag, cx + pos.real, cy + pos.imag, width=2)
            prev = pos

    t += 2 * math.pi / len(epicycles)
    display.after(50, draw_loop, display, epicycles)



dimensions = [600, 400]
root = tkinter.Tk()
root.title("Discrete Fourier Transform Drawing")
root.geometry(f"{dimensions[0]}x{dimensions[1]}")
root.resizable(0, 0)

display = tkinter.Canvas(root, highlightthickness=0, bg="#ffffff")
display.pack(fill="both", expand=1)

t = 0
with open("points.json") as fp:
    points = json.load(fp)

def map(point):
    x = y = 0
    if dimensions[0] < dimensions[1]:
        scl = dimensions[0]
        y += (dimensions[1] - dimensions[0]) / 2

    else:
        scl = dimensions[1]
        x += (dimensions[0] - dimensions[1]) / 2

    x += scl * (point[0] + 1) / 2 - dimensions[0] / 2
    y += scl * (point[1] + 1) / 2 - dimensions[1] / 2
    return [x, y]

skip = 1
points = [points[i] for i in range(0, len(points), skip)]
print(len(points), "points")
points = [map(i) for i in points]
points = discrete_fourier_transform([complex(i[0], i[1]) for i in points])
points = sorted(points, key=lambda x: -abs(x[1]))
# print(points)
pattern = []
display.after_idle(draw_loop, display, points)
root.mainloop()
