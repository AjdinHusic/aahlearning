# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 16:16:47 2018

@author: ajdin
"""

import numpy as np
from scipy.special import expit as sigmoid
  
  
def linu(args):
  return args

class NeuralNetwork:
  
  def __init__(self, size=None, nonlins=None, tied=False):
    if not size:
      self.size = (1, 1)
    else:
      self.size = size
    self.countLayers = len(self.size)
    if not nonlins:
      self.nonlins = []
      for index in range(self.countLayers-1):
        self.nonlins.append(linu)
    else:
      self.nonlins = nonlins
    self.weight_cap = 5
    self.tied = tied
    self.weights = [None]*(self.countLayers-1)
    for index in range(self.countLayers-1):
      if not self.tied:
        self.weights[index] = np.random.uniform(-self.weight_cap, self.weight_cap, (self.size[index+1], self.size[index]) )
      else:
        if index < self.countLayers/2:
          self.weights[index] = np.random.uniform(-self.weight_cap, self.weight_cap, (self.size[index+1], self.size[index]) )
          self.weights[self.countLayers-index-2] = self.weights[index].T 
      
      
  def compute(self, excitation):
    output = [np.reshape(excitation, (self.size[-1], -1) )]
    for index in range(self.countLayers-1):
      output.append(self.nonlins[index](self.weights[index] @ output[index]))
    return output    

  def getSaturated(self):
    countWeights = 0
    countSaturated = 0
    for index in self.weights:
      countWeights += np.prod(np.size(self.weights[index]))
      countSaturated += len(np.where(np.abs(self.weights[index]) > 1.99)[1])
    return countSaturated/countWeights
  
  

class Autoencoder(NeuralNetwork):
  
  def __init__(self, size=(11, 5, 11), nonlins=(sigmoid, sigmoid), tied=True):
    super().__init__(size, nonlins, tied)
    self.error = None
    
  def train(self, rate, excitation):
    outputs, error = self.getError(excitation)
    weightUpdate = [None]*(self.countLayers-1)
    for index in range(self.countLayers-1):
      if not self.tied:
        weightUpdate[index] = rate*(outputs[index+1] @ error.T)
        self.weights[index] += weightUpdate[index]
      else:
        if index < (self.countLayers-1)/2:
          weightUpdate[index] = rate*(outputs[index+1] @ error.T)
          weightUpdate[self.countLayers-index-2] = weightUpdate[index].T
          self.weights[index] += weightUpdate[index]
          self.weights[self.countLayers-index-2] += weightUpdate[index].T
    return outputs

  def getError(self, excitation):
    outputs = self.compute(excitation)
    self.error = outputs[0] - outputs[-1]
    return outputs, self.error


    
class HebbianAgent(NeuralNetwork):
  
  def __init__(self, size=(5, 11), nonlins=(sigmoid), tied=False):
    super().__init__(size, nonlins, tied)
    self.modulation = 0
    
  def train(self, rate, excitation):
    outputs = self.compute(excitation)
    weightUpdate = [None]*(self.countLayers-1)
    for index in range(self.countLayers)-1:
      weightUpdate[index] = rate*self.modulation*(outputs[index+1] @ outputs[index])
      self.weights[index] = np.clip(self.weights[index]+weightUpdate[index], -self.weight_cap, self.weight_cap) 
  
  def getModulation(self, prev_measurements, measurements, actions):
    self.modulation = prev_measurements[5]-measurements[5]
    return self.modulation
  


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    