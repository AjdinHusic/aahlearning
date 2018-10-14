# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 12:28:51 2018

@author: ajdin
"""
from collections import deque

class Buffer:
  """
  Creates a dynamic buffer, that contains a variable amount of samples.
  """
  MIN_SIZE = 1
  
  def __init__(self, initlen, maxlen=None, growth_fact=1.0):
    self.samples = deque(maxlen=maxlen)
    self.isfull = False
    self.growth = growth_fact
    if initlen >= 1:
      self.currentlen = initlen
    else: 
      self.currentlen = Buffer.MIN_SIZE
    
  def __len__(self):
    return len(self.samples)
    
  def __iter__(self):
    return iter(self.samples)
  
  def append(self, value):
    self.samples.append(value)
    self.isfull = False
    if len(self) >= self.currentlen or len(self) >= self.samples.maxlen:
      self.isfull = True
    
  def clear(self):
    self.samples.clear()
    if (1.0 <= self.growth <= 2.0) and not (self.currentlen >= self.samples.maxlen):
      self.currentlen *= self.growth
    
  def add_sample(self, sample):
    self.handle_full_capacity()
    self.append(sample)

  def handle_full_capacity(self):
    if self.isfull:
      self.clear()
      
      
      
    