# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 17:30:23 2018

@author: ajdin
"""
import numpy as np

class NoveltyBuffer:
  
  def __init__(self, bufferSize):
    self.bufferSize = bufferSize
    self.buffer = [[None, 0]]*self.bufferSize
    
  def computeNoveltyScore(self, new_experience):
    new_experience = np.array(new_experience)
    distances = []
    for experience, noveltyScore  in self.buffer:
      if experience is not None:
        distance = np.linalg.norm(experience - new_experience)
        distances.append(distance)
    noveltyScore = sum(sorted(distances)[0:20])
    return noveltyScore
    
  def updateBuffer(self, new_experience):
    noveltyScore = self.computeNoveltyScore(new_experience)
    minNoveltyIndex = np.argmin([score for exp, score in self.buffer])
    if noveltyScore >= self.buffer[minNoveltyIndex][1]:
      self.buffer.pop(minNoveltyIndex)
      self.buffer.append([np.array(new_experience), noveltyScore])
      
    