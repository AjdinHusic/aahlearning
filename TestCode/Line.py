# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:09:18 2018

@author: ajdin
"""
import numpy as np

#def slope(p1, p2) :
#  min_allowed = 1e-5 #guard againts overflow
#  if (p2[0] - p1[0]) < min_allowed:
#    x = min_allowed
#  else:
#    x = (p2[0] - p1[0])
#  return (p2[1] - p1[1]) * 1. / (x)
#   
#def y_intercept(slope, p1) :
#  return p1[1] - 1. * slope * p1[0]
 
def distance(p1 , p2):
  return ((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)**(1/2)

def get_line_coeff(p1, p2):
  a = p2[1] - p1[1]
  b = p1[0] - p2[0]
  c = a*p1[0] + b*p1[1]
  return a, b, c

class Line(object):
  
  def __init__(self, pos, rel_pos):
    self.pos = pos
    self.rel_pos = rel_pos
    self.length = distance(self.pos, self.rel_pos)
    
#  def intersect(self, line):
#    min_allowed = 1e-5 #guard againts overflow
#    big_value = 1e10 #use instead (if overflow would have occured)
#    m1 = slope(self.pos, self.rel_pos)
#    b1 = y_intercept(m1, self.pos)
#    m2 = slope(line.pos, line.rel_pos)
#    b2 = y_intercept(m2, line.pos)
#    if abs(m1 - m2) < min_allowed:
#      x = big_value
#    else:
#      x = (b2 - b1) / (m1 - m2)
#    y = m1*x + b1
#    return (int(x), int(y))
  
  def intersect2(self, line):
    a1, b1, c1 = get_line_coeff(self.pos, self.rel_pos)
    a2, b2, c2 = get_line_coeff(line.pos, line.rel_pos)
    if a1*b2 == a2*b1:
      return None
    a = np.array(( (a1, b1), (a2, b2)))
    b = np.array((c1, c2))
    x, y = np.linalg.solve(a, b)
    return x, y
  
  def segment_intersect(self, line2) :
   intersection_pt = self.intersect2(line2)
   minx1 = min(self.pos[0], self.rel_pos[0])
   maxx1 = max(self.pos[0], self.rel_pos[0])
   minx2 = min(line2.pos[0], line2.rel_pos[0])
   maxx2 = max(line2.pos[0], line2.rel_pos[0])
   miny1 = min(self.pos[1], self.rel_pos[1])
   maxy1 = max(self.pos[1], self.rel_pos[1])
   miny2 = min(line2.pos[1], line2.rel_pos[1])
   maxy2 = max(line2.pos[1], line2.rel_pos[1])
   
   tol = 0.1
   if intersection_pt:
     outXbounds = intersection_pt[0] < max(minx1, minx2)-tol or intersection_pt[0] > min(maxx1, maxx2)+tol
     outYbounds = intersection_pt[1] < max(miny1, miny2)-tol or intersection_pt[1] > min(maxy1, maxy2)+tol
     if outXbounds or outYbounds:
       return 0
  #   return True
  #   if (self.pos[0] < self.rel_pos[0]) :
  #      if intersection_pt[0] < self.pos[0] or intersection_pt[0] > self.rel_pos[0] :
  #         return 0
  #   else :
  #      if intersection_pt[0] > self.pos[0] or intersection_pt[0] < self.rel_pos[0] :
  #         return 0
  #         
  #   if (line2.pos[0] < line2.rel_pos[0]) :
  #      if intersection_pt[0] < line2.pos[0] or intersection_pt[0] > line2.rel_pos[0] :
  #         return 0
  #   else :
  #      if intersection_pt[0] > line2.pos[0] or intersection_pt[0] < line2.rel_pos[0] :
  #         return 0
     return 1 - distance(self.pos, intersection_pt)/self.length
   return 0
 
  def angle_between(self, line2):
    vector1 = (self.rel_pos[0] - self.pos[0], self.rel_pos[1] - self.pos[1])
    vector2 = (line2.rel_pos[0] - line2.pos[0], line2.rel_pos[1] - line2.pos[1])
    inner_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
    len1 = np.linalg.norm(vector1)
    len2 = np.linalg.norm(vector2)
    return np.degrees(np.arccos(inner_product/(len1*len2)))