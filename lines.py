# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 16:27:41 2018

@author: ajdin
"""
import numpy as np

def get_dist(p1 , p2):
  return ((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)**(1/2)

class LineSegment:
  
  def __init__(self, startPoint, endPoint):
    self.startPoint = startPoint
    self.endPoint = endPoint
    self.setUp()
    
  def setUp(self):
    deltaX = self.endPoint[0] - self.startPoint[0]
    
    #Set up the bounds
    self.upperBoundY = max(self.endPoint[1], self.startPoint[1])
    self.lowerBoundY = min(self.endPoint[1], self.startPoint[1])
    
    self.upperBoundX = max(self.endPoint[0], self.startPoint[0])
    self.lowerBoundX = min(self.endPoint[0], self.startPoint[0])

    #If the change in x is 0, the slope is undefined
    if abs(deltaX) <= 1e-5:
      self.vertical = True
      self.slope = None
      #If the line segment is just a point, it's x coordinate is stored in lowerBounds
      self.lowerBoundX = self.startPoint[0]
    #End if   
    else:
      self.vertical = False
      self.slope = (self.endPoint[1] - self.startPoint[1]) / deltaX
      self.yIntercept = self.startPoint[1] - (self.slope * self.startPoint[0])
  
  def getY(self, x):
    if x >= self.lowerBoundX and x <= self.upperBoundX and not self.vertical:
      return self.slope*x + self.yIntercept
    else:
      return np.inf
    
  def intersects(self, line):
    intersection = []
    bothVertical = self.vertical and line.vertical
    parallel = self.slope == line.slope and not self.vertical and not line.vertical
    
    if bothVertical or parallel:
      if (bothVertical and self.lowerBoundX == line.lowerBoundX) or (parallel and self.yIntercept == line.yIntercept):
        lowerInBounds = self.valueInBounds(self.lowerBoundY, line.lowerBoundY, line.upperBoundY)
        upperInBounds = self.valueInBounds(self.upperBoundY, line.lowerBoundY, line.upperBoundY)
        
        if lowerInBounds and upperInBounds:
          intersection.append((self.lowerBoundX, self.lowerBoundY))
          intersection.append((self.lowerBoundX, self.upperBoundY))
        elif lowerInBounds:
          intersection.append((self.lowerBoundX, self.lowerBoundY))
          intersection.append((self.lowerBoundX, line.upperBoundY))
        elif upperInBounds:
          intersection.append((self.lowerBoundX, line.lowerBoundY))
          intersection.append((self.lowerBoundX, self.upperBoundY))
        elif self.valueInBounds(line.lowerBoundY, self.lowerBoundY, self.upperBoundY) and self.valueInBounds(line.upperBoundY, self.lowerBoundY, self.upperBoundY):
          intersection.append((self.lowerBoundX, line.lowerBoundY))
          intersection.append((self.lowerBoundX, line.upperBoundY))
      return intersection
    elif self.vertical:
      y = line.getY(self.lowerBoundX)
      #Maker sure the returned y is valid
      #GetY not returning infinity makes sure that the point is in bounds of this line
      if y == np.inf or not line.valueInBounds(y, self.lowerBoundY, self.upperBoundY):
        return intersection
      
      intersection.append((self.lowerBoundX, y))
      return intersection
    elif line.vertical:
      y = self.getY(self.lowerBoundX)
      #Make sure the returned y is valid
      #GetY not returning infinity makes sure that the point is in bounds of line
      if y == np.inf or not self.valueInBounds(y, line.lowerBoundY, line.upperBoundY):
        return intersection
      
      intersection.append((line.lowerBoundX, y))
      return intersection
    else:
      intersectionX = (line.yIntercept - self.yIntercept) / (self.slope - line.slope)
      if self.valueInBounds(intersectionX, self.lowerBoundX, self.upperBoundX) and self.valueInBounds(intersectionX, line.lowerBoundX, line.upperBoundX):
        intersection.append(((intersectionX), self.getY(intersectionX)))
          
      return intersection
        
    
  def valueInBounds(self, value, lowerBound, upperBound):
    if value >= lowerBound and value <= upperBound:
      return True
    else:
      return False

  def angle_between(self, line2):
    vector1 = (self.endPoint[0] - self.startPoint[0], self.endPoint[1] - self.startPoint[1])
    vector2 = (line2.endPoint[0] - line2.startPoint[0], line2.endPoint[1] - line2.startPoint[1])
    inner_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
    len1 = np.linalg.norm(vector1)
    len2 = np.linalg.norm(vector2)
    return np.degrees(np.arccos(inner_product/(len1*len2)))
  
  @staticmethod
  def overlapsInDimension(pointsA, pointsB):
    Amin = min(pointsA)
    Amax = max(pointsA)
    Bmin = min(pointsB)
    Bmax = max(pointsB)
    if Amin > Bmax:
      return False
    if Amax < Bmin:
      return False
    return True
  
#  def entities_in_bounds(self, entities):
#    entities_in_bounds = []    
#    for entity in entities:
#      lowerInBoundsY = self.valueInBounds(self.lowerBoundY, entity.lowerBoundY, entity.upperBoundY)
#      upperInBoundsY = self.valueInBounds(self.upperBoundY, entity.lowerBoundY, entity.upperBoundY)
#      lowerInBoundsX = self.valueInBounds(self.lowerBoundX, entity.lowerBoundX, entity.upperBoundX)
#      upperInBoundsX = self.valueInBounds(self.upperBoundX, entity.lowerBoundX, entity.upperBoundX)
#      entityInBounds = lowerInBoundsY or upperInBoundsY or lowerInBoundsX or upperInBoundsX
#      if entityInBounds:
#        entities_in_bounds.append(entity)
#    return entities_in_bounds

  def entities_in_bounds(self, entities):
    entities_in_bounds = [] 
    pointsAx = (self.lowerBoundX, self.upperBoundX)
    pointsAy = (self.lowerBoundY, self.upperBoundY)
    for entity in entities:
      pointsBx = (entity.lowerBoundX, entity.upperBoundX)
      pointsBy = (entity.lowerBoundY, entity.upperBoundY)
      overlapsInX = LineSegment.overlapsInDimension(pointsAx, pointsBx)
      overlapsInY = LineSegment.overlapsInDimension(pointsAy, pointsBy)
      entityInBounds = overlapsInX and overlapsInY
      if entityInBounds:
        entities_in_bounds.append(entity)
    return entities_in_bounds
      
  
