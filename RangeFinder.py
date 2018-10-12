# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:11:52 2018

@author: ajdin
"""
from LineSegment import LineSegment
from LineSegment import get_dist

import numpy as np
import pygame

class RangeFinder(LineSegment):
  
  def __init__(self, car, default_length=350, relativeAngle=0):
    self.car = car
    self.default_length = default_length
    self.length = self.default_length
    self.relativeAngle = relativeAngle
    super().__init__(self.getStartPoint(), self.getEndPoint())
    self.activation = 0.0
    
  def getStartPoint(self):
    return self.car.center
    
  def getEndPoint(self):
    rads = np.radians(self.car.angle + self.relativeAngle)
    change = (np.cos(rads), np.sin(rads))
    return tuple(np.add(self.car.center, tuple(x*(self.default_length) for x in change)))
  
  def update_position(self):
    self.startPoint = self.getStartPoint()
    self.endPoint = self.getEndPoint()
    self.setUp()
  
  def update(self, walls):
    self.update_position()
    walls_in_bounds = self.entities_in_bounds(walls)
    nearestWallDistance = self.default_length
    for wall in walls_in_bounds:
      intersections = self.intersects(wall)
      if len(intersections) > 0:
        distance = get_dist(self.car.center, intersections[0])
        nearestWallDistance = min(distance, nearestWallDistance)
    self.length = nearestWallDistance
    self.activation = (self.default_length - self.length) / self.default_length
    
  def draw(self, display, options):
    color = tuple([self.activation*x for x in (255, 80, 0)])
    x_scale = options['x_scale']
    x_translate = options['x_translate']
    startPoint = tuple(x_scale*x+x_translate for x in self.startPoint)
    endPoint= tuple(x_scale*x+x_translate for x in self.endPoint)
    pygame.draw.aaline(display, color, startPoint, endPoint)
    