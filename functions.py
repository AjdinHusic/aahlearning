# -*- coding: utf-8 -*-
import numpy as np

class Activation:
  
  @staticmethod
  def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))
  
  #Takes the already computed value of sigmoid
  @staticmethod
  def logistic_derivative(x):
    return x * (1.0 - x)