# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:33:33 2018

@author: ajdin
"""
import numpy as np
import unittest

from net3 import NeuralNetwork3


class TestNeuralNetwork(unittest.TestCase):
  """
  Unit tests to test instances and methods used from the NeuralNetwork class.
  """
  def __init__(self, *args, **kwargs):
    super(TestNeuralNetwork, self).__init__(*args, **kwargs)
    self.nn5by5 = NeuralNetwork3(inputcount=5, hiddencount=0, outputcount=5)
  
  def test_neuralnetwork(self):
    last_layer = self.nn5by5.layers[-1]
    cap = self.nn5by5.weight_cap
    weights = last_layer.weights
    all_elements_equal = np.all([-cap<=x for x in weights]) and np.all([x<=cap for x in weights])
    self.assertTrue(all_elements_equal)

    
  def test_propagatesignal(self):
    
    pass
  
  

if __name__ == '__main__':
  unittest.main()