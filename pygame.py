import pygame as py
size=(500,400)
screen=py.display.set_mode(size)
while True:
    for event in py.event.get():
        if event.type==py.Mousebuttonup:
            pos=py.mouse.get_pos()
            col=(0.255.255)
            py.draw.circle(screen,col,pos,20,5)
            py.display.update()


