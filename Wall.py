# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 13:26:34 2018

@author: ajdin
"""
from LineSegment import LineSegment
import pygame
import xml.etree.ElementTree as ET

root = ET.parse('Maps/XMap.xml').getroot()
ROOT = root.find('Entity')

class EntityConfig:
  def __init__(self, root=ROOT):
    self.x = float(root.find('X').text)
    self.y = float(root.find('Y').text)
    self.relX = float(root.find('RelX').text)
    self.relY = float(root.find('RelY').text)
    self.angle = float(root.find('Angle').text)
    self.type_ = None
    if root.get('Type'):
      self.type_ = root.get('Type')

black = (0, 0, 0)

class Wall(LineSegment):
  def __init__(self, startPoint, endPoint):
    super().__init__(startPoint, endPoint)
    
  def draw(self, display, options):
    x_scale = options["x_scale"]
    x_translate = options["x_translate"]
    startPoint = tuple(x_scale*x+x_translate for x in self.startPoint)
    endPoint = tuple(x_scale*x+x_translate for x in self.endPoint)
    pygame.draw.aaline(display, black, startPoint, endPoint)

    