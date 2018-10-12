# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 21:11:27 2018

@author: ajdin
"""
#from Line import Line

import numpy as np

import xml.etree.ElementTree as ET
import pygame

from LineSegment import LineSegment

redcolor = (0xff,0,0)

class CarConfig:
  """
  Configures initial parameters or constants, used by the Car class.
  """
  root = ET.parse('Maps/XMap.xml').getroot()
  ROOT = root.find('Robot')
  def __init__(self, root=ROOT):
    self.x = float(root.find('X').text)
    self.y = float(root.find('Y').text)
    self.angle = float(root.find('Angle').text)
 

class Car(object):
  """
  Agent that moves through a 2D environment, which can be visualized using a pygame surface.
  
  Parameters
  ----------
  center: tuple, optional. 
    Sets the initial position in a 2D plane using Cartesion coordinates. default is (0,0).
    
  angle: float, optional.
    Sets the initial angle in degrees of the agent relative to a 2D frame. default is 0.
    
  Attributes
  ----------
  center:
    
  velocity:
    
  speed:
    
  acceleration:
  
  image:
    
  angle:
    
  """
  
  CONTROL_THRESHOLD = 0.5
  MIN_SPEED_X = 10.0
  MIN_SPEED_Y = 8.0
  MAX_SPEED_X = 15.0
  MAX_SPEED_Y = 12.0
  MAX_ROTATE = 1.0  
  MIN_ROTATE = 0.0
  ROTATE_SPEED = 2.0
  ROTATE_RANGE = 2.0*ROTATE_SPEED
  ACCELERATION = 0.1
  ACCELERATION_RANGE = 2.0*ACCELERATION
  RADIUS = 3.0
  
  def __init__(self, center=(0,0), angle=0):
    self.center = center
    self.velocity = (0, 0)
    self.speed = (self.MAX_SPEED_X, self.MAX_SPEED_Y)
    self.acceleration = 0
    self.image = pygame.image.load('Textures/CarResized.png')
    self.angle = angle % 360
    self.can_move = True
    self.upper_bounds = (self.MAX_SPEED_X, self.MAX_SPEED_Y)
    self.lower_bounds = (self.MIN_SPEED_X, self.MIN_SPEED_Y)

  def next_pos(self):
    rads = np.radians(self.angle)
    change = (np.cos(rads), -np.sin(rads))
    return tuple(np.add(tuple(x*self.MOVE_SPEED for x in change), self.pos))
        
  def update_score(self, last, center_point):
    vector_last = tuple(np.subtract(last, center_point))
    vector_current = tuple(np.subtract(self.center, center_point))
    delta_angle = np.degrees(+ np.arctan2(vector_current[1], vector_current[0]) \
                             - np.arctan2(vector_last[1], vector_last[0]))
    if np.abs(delta_angle) > 90:
      change = 360 - np.abs(delta_angle)
      if delta_angle < 0.0:
        return change
      else:
        return -change
    return (delta_angle) 
  
  def update(self, walls):
    radians = np.radians(self.angle)
    yx_ratio = self.MAX_SPEED_Y / self.MAX_SPEED_X
    resulting_speed = (self.speed[0] + self.acceleration, self.speed[1] + yx_ratio*self.acceleration)
    self.speed = np.clip(resulting_speed, self.lower_bounds, self.upper_bounds)
    self.velocity = (np.cos(radians)*self.speed[0], np.sin(radians)*self.speed[1])
    original = self.center
    projected = tuple(np.add(original, self.velocity))
    collision_line = LineSegment(original, projected)
    walls_in_bounds = collision_line.entities_in_bounds(walls)
    self.can_move = True
    for wall in walls_in_bounds:
      intersections = collision_line.intersects(wall)
      if  len(intersections) > 0:
        self.can_move = False
        break
    if self.can_move:
      self.center = tuple(np.add(self.center, self.velocity))
    
  def draw(self, display, options):
    x_scale = options['x_scale']
    x_translate = options['x_translate']
    x = self.center[0]*x_scale + x_translate
    y = self.center[1]*x_scale + x_translate
    angle = self.angle
    angle %= 360
    rotated_img = pygame.transform.rotate(self.image, -angle)
    original_rect = self.image.get_rect(center=(x,y))
    rotated_rect = rotated_img.get_rect(center=original_rect.center)
    display.blit(rotated_img, rotated_rect)
    pygame.draw.circle(display, redcolor, tuple(int(i) for i in (x, y)), int(self.RADIUS), 2)
 
    
