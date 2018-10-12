# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 15:12:41 2018

@author: ajdin
"""
#import numpy as np
import pygame
from Line import Line
from RangeFinder import RangeFinder
from Car import Car

import xml.etree.ElementTree as ET
wallMap = ET.parse('Maps/XMap.xml').getroot()
walls = []      

#
#scaleX = a
#scaleY = c
#translateX = b
#translateY = d
#rotation = 180

scaleX = 0.2184233207295375
scaleY = 0.22767977831846448
translateX = 133.81512733541817
translateY = 138.1115070345661
rotation = 180

maxX, maxY = (0,0)
minX, minY = (5000, 5000)
for element in wallMap:
  if element.tag == 'Robot':
    carX = float(element[0].text)
    carY = float(element[1].text)
    carAngle = float(element[2].text)
    newCarX = scaleX*carX+translateX
    newCarY = scaleY*carY+translateY
    newCarAngle = carAngle+rotation
  elif element.tag == 'Entity':
    
    if element.attrib['Type'] == 'Wall':
      posX = float(element[0].text)
      posY = float(element[1].text)
      rel_posX = posX + float(element[2].text) 
      rel_posY = posY + float(element[3].text)
      newX = scaleX*posX + translateX
      newY = scaleY*posY + translateY
      new_relX = scaleX*rel_posX + translateX
      new_relY = scaleY*rel_posY + translateY
      walls.append(Line((newX, newY),(new_relX, new_relY)))
    if element.attrib['Type'] == 'Point':
      midPointX = float(element[0].text)
      midPointY = float(element[1].text)
      
sensorConfig = ET.parse('Sensors/Default.xml').getroot()
rangefinderSensors = []
for element in sensorConfig:
    sensorCount = int(element[0].text)
    rangefinderLength = int(element[1].text)
    angleOffset = int(element[2].text)
    angle_between = int(element[3].text)
    
#%%

from CarMazeEnv import CarMazeEnv

#pygame.init()

display_width = 1000
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
redcolor = (0xff,0,0)



game_display = pygame.display.set_mode((display_width, display_height))
screen_rect = game_display.get_rect()
pygame.display.set_caption('Car Maze')
clock = pygame.time.Clock()

carImg = pygame.image.load('Textures/CarResized.png')

def draw_car(car):
  x = car.pos[0]
  y = car.pos[1]
  angle = car.angle
  angle %= 360
  rotated_img = pygame.transform.rotate(carImg, angle)
  original_rect = carImg.get_rect(center=(x,y))
  rotated_rect = rotated_img.get_rect(center=original_rect.center)
  game_display.blit(rotated_img, rotated_rect)
  
def draw_walls(walls):
  for wall in walls:
    pygame.draw.aaline(game_display, black, wall.pos, wall.rel_pos)
    
def draw_sensors(sensors, intensities):
  for i in range(len(sensors)):
    color = tuple([intensities[i]*x for x in (255, 80, 0)])
    pygame.draw.aaline(game_display, color, sensors[i].pos, sensors[i].rel_pos)


def main():
  x = (display_width*0.45)
  y = (display_height*0.6)
  angle = 0
  rangeFinderLength = 70
  car = Car((newCarX, newCarY), newCarAngle)
  env = CarMazeEnv()
  rangefinderSensors = []
  for el in range(sensorCount):
    rangefinderSensors.append(RangeFinder(car, rangeFinderLength, angleOffset+el*angle_between))
  angle_change = 0
  
  game_ext = False
  #env = CarMazeEnv()
  RUNNING, PAUSE = 0, 1 
  state = RUNNING
  action = 0.5
  while not game_ext:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_ext = True
        #env.close()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p and state == RUNNING: state = PAUSE
        elif event.key == pygame.K_p and state == PAUSE: state = RUNNING
          
        if event.key == pygame.K_LEFT:
          #angle_change = 2
          action = 0
          #angle_change = -(action*4-2)
        if event.key == pygame.K_RIGHT:
          #angle_change = -2
          action = 1
          #angle_change = -(action*4-2)
        
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          angle_change = 0
          action = 0.5
          angle_change = -(action*4-2)
      
#    game_display.fill(white)
    if state == RUNNING:
      env.step(action)
#      angle_change = -(action*4-2)
#      car.updateMovability(walls)
#      car.update(angle_change)
      #env.step(action)
      #print(env.measurements)
#      intensities = []
#      for rangefinder in rangefinderSensors:
#        rangefinder.update()
#        intensities.append(rangefinder.sense(walls))
#      print(intensities)
      
#    env.cars = [car]
#    env.rangeFinders = rangefinderSensors
#    env.measurements = intensities
#    env.clock = clock
    
#    game_display.fill(white)
#    draw_walls(walls)
#    draw_car(car)    
#    pygame.draw.circle(game_display, redcolor, tuple(int(x) for x in car.pos), car.RADIUS, 2)
#    draw_sensors(rangefinderSensors, intensities)
#    
#    pygame.display.flip()
#    clock.tick(30)
    env.render()
    
  
main()
pygame.quit()
#quit()




