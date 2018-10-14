
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 15:12:41 2018

@author: ajdin
"""
import pygame

from CarMazeEnv import CarMazeEnv

display_width = 1600
display_height = 1440

res = (display_width, display_height)


simul = None
  
def main():
  global simul
  simul = CarMazeEnv()

  RUNNING, PAUSE = 0, 1 
  state = RUNNING
  
  while not simul.game_ext:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        simul.close()
        return

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p and state == RUNNING: state = PAUSE
        elif event.key == pygame.K_p and state == PAUSE: state = RUNNING        
      
    if state == RUNNING:
      simul.step()
    simul.render(res)
    
  
  
main()
pygame.quit()
#quit()



