# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:33:33 2018

@author: ajdin
"""
from NeuralNetwork import NeuralNetwork

import unittest

class TestNeuralNetwork(unittest.TestCase):
  """
  Unit tests to test instances and methods used from the NeuralNetwork class.
  """
  def __init__(self, *args, **kwargs):
    super(TestNeuralNetwork, self).__init__(*args, **kwargs)
    self.ann = NeuralNetwork()
    self.ann.configure()
    self.weights = [x.weight for x in self.ann.input_groups[0].outgoing_groups[0].connections]
  
  def test_neuralnetwork(self):
    self.assertTrue([-self.ann.weight_cap]*len(self.weights) <=\
                    self.weights <= [self.ann.weight_cap]*len(self.weights))
    
  def test_propagatesignal(self):
    pass
  
  

if __name__ == '__main__':
  unittest.main()