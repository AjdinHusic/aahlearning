# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 20:08:34 2018

@author: ajdin
"""
from RangeFinder import RangeFinder

class RangeFinderGroup(list):
  
  def __init__(self, car, size=11):
    self.car = car
    self.count = size
    self.activations = []
    self.configure()    
    
  def configure(self, default_length=350, angleOffset=-90, angle_between=18):
    self.default_length = default_length
    self.startAngle = angleOffset
    self.angleSpacing = angle_between
    
    for i in range(self.count):
      relativeAngle = self.startAngle + (self.angleSpacing*i)
      self.append(RangeFinder(self.car, self.default_length, relativeAngle))
      self.activations.append(self[i].activation)
    
  def update(self, walls):
    for i in range(self.count):
      self[i].update(walls)
      self.activations[i] = self[i].activation
      
  def draw(self, display, options):
    for i in range(self.count):
      self[i].draw(display, options)
        
      