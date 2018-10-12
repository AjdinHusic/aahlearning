# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 16:16:47 2018

@author: ajdin
"""

import numpy as np
from scipy.special import expit as sigmoid

def sigmoidPrime(args):
  return sigmoid(args)*(1-sigmoid(args))  
  
def linu(args):
  return args

class NeuralNetwork:
  
  def __init__(self, size=None, nonlins=None):
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
    self.weights = [None]*(self.countLayers-1)
    for index in range(self.countLayers-1):
      self.weights[index] = np.random.uniform(-self.weight_cap, self.weight_cap, (self.size[index+1], self.size[index]) )
      
      
  def compute(self, excitation):
    activations = [np.reshape(excitation, (self.size[0], -1) )]
    for index in range(self.countLayers-1):
      activations.append(self.nonlins[index](self.weights[index] @ activations[index]))
    return activations    

  def getSaturated(self):
    countWeights = 0
    countSaturated = 0
    for index in range(self.countLayers-1):
      countWeights += np.prod(np.size(self.weights[index]))
      countSaturated += len(np.where(np.abs(self.weights[index]) >= self.weight_cap-0.01)[1])
    return countSaturated/countWeights
  
  

class Autoencoder(NeuralNetwork):
  
  def __init__(self, size=(11, 5), nonlins=[sigmoid]):
    super().__init__(size, nonlins)
    self.error = None
    
  def train(self, rate, excitation):
    excitation, forward = self.computeForward(excitation)
    backward = self.computeBackward(forward)[-1]
    error = self.getError(excitation, backward)
    deltas = np.multiply(error, sigmoidPrime(backward))
    deltasBackprop = np.multiply(self.weights[0] @ deltas, sigmoidPrime(forward))
    update = rate*(forward @ deltas.T + deltasBackprop @ excitation.T)
    self.weights[0] = np.clip(self.weights[0] + update, -self.weight_cap, self.weight_cap)
    return forward
  
  def computeForward(self, excitation):
    activations = self.compute(excitation)
    return activations
  
  def computeBackward(self, hidden):
    activations = [np.reshape(hidden, (self.size[-1], -1) )]
    for index in range(self.countLayers-1):
      activations.append(self.nonlins[-1-index](self.weights[-1-index].T @ activations[-1-index]))
    return activations

  def getError(self, excitation, backward):
    self.error = excitation - backward
    return self.error


    
class HebbianAgent(NeuralNetwork):
  
  def __init__(self, size=(5, 1), nonlins=[sigmoid]):
    super().__init__(size, nonlins)
    
  def train(self, rate, modulation, excitation):
    activations = self.compute(excitation)
    weightUpdate = [None]*(self.countLayers-1)
    for index in range(self.countLayers-1):
      noise = np.random.uniform(-0.1, 0.1, (np.shape(weightUpdate[index])) )
      weightUpdate[index] = rate*modulation*(activations[index+1] @ activations[index].T) + noise
      self.weights[index] = np.clip(self.weights[index]+weightUpdate[index], -self.weight_cap, self.weight_cap) 
  
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    