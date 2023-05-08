#!/usr/bin/env python3

import tkinter as tk

import argv_parse

args, kwargs = argv_parse.parse()

def binary_images(number=None):
    if number is None:
        number = slider_value.get()
    else:
        number = int(number)
        slider_value.set(number)
    assert 0 <= number < 1024, repr(number)
    # print(number, end=' ')
    for bulb, n in digits:
        if number >= bulb.place_value:
            bulb.configure(image=glowing)
            n.set('1')
            number -= bulb.place_value
        else:
            bulb.configure(image=dark)
            n.set('0')

root = tk.Tk()
root.title('Binary Images')
root.geometry('840x230')
root.configure(background='#6ca5a8')

slider_value = tk.IntVar(name='slider', value=0)
scale = tk.Scale(root, from_=0, to=1023, command=binary_images, orient=tk.HORIZONTAL, variable=slider_value)
scale.pack(fill='x')

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, fill='x')

glowing = tk.PhotoImage(file='py/ChessKidAvatars/glowing-bulb.gif')
dark = tk.PhotoImage(file='py/ChessKidAvatars/dark-bulb.gif')
digits = [tk.Label(frame, image=dark, borderwidth=0) for _ in range(10)]
for i, w in enumerate(digits):
    w.grid(row=0, column=i)
    w.place_value = 2 ** (9 - i)
    var = tk.StringVar(name=f'{2 ** (9 - i)}s-place-value', value='0')
    label = tk.Label(frame, textvariable=var)
    label.grid(row=1, column=i)
    digits[i] = (w, var)

if args:
    # slider_value.set(int(sys.argv[1]))
    binary_images(args[0])

def animate(start=None, end=None):
    if start is None or end is None:
        start, end = start or 0, end or 1024
        if args:
            start = args[0]
            if len(args) > 1:
                end = args[1]
    if start == end:
        return
    binary_images(start)
    root.after(300, animate, start + 1, end)

def change_one(event):
    assert event.keysym in {'Right', 'Left'}
    current = slider_value.get()
    change = 1 if event.keysym == 'Right' else -1
    if not 0 <= current + change < 1024:
        return
    binary_images(current + change)

root.bind_all('<Right>', change_one)
root.bind_all('<Left>', change_one)

if kwargs.get('animate'): root.after(1500, animate)
root.mainloop()
