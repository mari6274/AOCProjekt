#!/usr/bin/python
__author__ = 'mario'

import inimage
import invideo
import Tkinter

window = Tkinter.Tk()
window.minsize(width=300, height=0)
window.wm_title("Wstawianie wideo do...")
b1 = Tkinter.Button(window, text="obrazu", command=inimage.go)
b1.pack()
b2 = Tkinter.Button(window, text="wideo", command=invideo.go)
b2.pack()

window.mainloop()
