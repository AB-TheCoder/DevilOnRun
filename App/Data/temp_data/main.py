"""main file for my project"""

#------------------------------Imports-------------------------------------------------------------------------------------------------
import PIL
import pygame as py
import sys
import os
from pathlib import Path
from typing import Optional
#-----------------------------------------------------------------------------------------------------
#screen and basic
py.init()
screen = py.display.set_mode((1000,600))
py.display.set_caption('DevilOnRun')

#clock and time
clock = py.time.Clock()
#-------------------------------------------------------------------------------------------------------
#functions
def shutdown() -> None:
    py.quit()
    sys.exit()
    


#----------------------------------------------------------------------------------------------------------
#main game loop
status = True
while status:
    for event in py.event.get():
        if event.type == py.QUIT:shutdown()

    
    screen.fill('white')
    py.display.update()
    clock.tick(40)
            

    