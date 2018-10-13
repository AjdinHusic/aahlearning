# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:52:38 2018

@author: ajdin
"""
import numpy as np

# from RaahnXmlConfig import NeuralNetworkConfig, LayerConfig
from Activation import Activation
from TrainingMethod import TrainingMethod
from Modulation import ModulationScheme, ModulationSignal

class NeuralNetwork3:
    """
    Creates a NeuralNetwork that strictly uses three layers at max: inputlayer, hiddenlayer, 
    and outputlayer. hiddenlayer is optional.
    parameters (optional keyword arguments): 
      inputcount: number of neurons in the input layer
      hiddencount: number of neurons in the hidden layer.
      outputcount: number of neurons in the output layer 
   
    attributes:
      activations: list of neuron values for each layer
      layers: list of NetworkLayers containing the neuron connections
      output_noise_mag: magnitude of random noise to be applied after computing activation
      weight_noise_mag: magnitude of random noise to be applied after updating weights
      weight_cap: weights will not grow beyond upper limit weight_cap and lower limit -weight_cap.
      # use_novelty: boolean determing whether a novelty buffer will be used.
    
    methods:
      set_up: initializes the NeuralNetwork3 layers based on parameters arguments.
      configure: configures hyper-parameters of the network, based on RaahnXmlConfig.
      init_neurons: returns numpy array of neurons with values 0.0
      add_experience: adds a sample experience to the network's input layer
      propagate_signal: maps the input activation to the output activation
      train: trains all connections that are present within the network
    """    
    WEIGHT_SCALE = 6.0
    ACTIVATION = Activation.logistic
    TRAINING_METHODS = {'Hebbian': TrainingMethod.hebbian_learning,
                        'SparseAutoencoder': TrainingMethod.sparseAutoEncoderTrain,
                        'HebbianBatches': TrainingMethod.hebbianBatchesTrain}
    MOD_SCHEMES = {'WallAvoidance': ModulationScheme.wall_avoidance}
    
    def __init__(self, **kwargs):
      self.activations = []
      self.layers = []
      # set up the layers if specified
      self.set_up(**kwargs)
      # configure hyper-parameters of the network.
      self.configure()
      # ready up for training
      self.compile_network()
      
    def set_up(self, **kwargs):  
      inputcount = kwargs.get('inputcount')
      hiddencount = kwargs.get('hiddencount')
      outputcount = kwargs.get('outputcount')
      if self.valid_neuron_count(inputcount) and self.valid_neuron_count(outputcount):
        self.activations.append(self.init_neurons(inputcount))
        if self.valid_neuron_count(hiddencount):
          self.activations.append(self.init_neurons(hiddencount))
          add_layer = NetworkLayer(self, hiddencount)
          self.layers.append(add_layer)
        self.activations.append(self.init_neurons(outputcount))
        add_layer = NetworkLayer(self, outputcount)
        self.layers.append(add_layer)
    
    def valid_neuron_count(self, count):
      if isinstance(count, int):
        if count > 0:
          return True
      return False
        
    def configure(self, output_noise_mag=0.1, weight_noise_mag=0.1):
      self.output_noise_mag = output_noise_mag
      self.weight_noise_mag = weight_noise_mag
      self.weight_cap = 10.0
      self.modulation_signal = ModulationSignal()
      self.modulation_signal.add_signal()
    
    def init_neurons(self, count):
      return np.ones(count)*0.0
      
    def add_experience(self, experience):
      # adds experience to input layer, and to any buffers if specified
      self.activations[0] = np.array(experience)
    
    def propagate_signal(self):
      for layer in self.layers:
        layer.propagate_signal()
        
    def compile_network(self, training_method='Hebbian', modulation_scheme='WallAvoidance'):
      for layer in self.layers:
        layer.training_method = NeuralNetwork3.TRAINING_METHODS[training_method]
        layer.modulation_scheme = NeuralNetwork3.MOD_SCHEMES[modulation_scheme] 
        
    def train(self):
      for layer in self.layers:
        layer.train()


class NetworkLayer:
  """
  Creates a fully connected NetworkLayer in a given NeuralNetwork3
  parameters: 
    network: NeuralNetwork3 in which the NetworkLayer is added
    neuron_count: number of neurons in current layer
    learning_rate: sets the learning rate for training (optional), default is 1.0
    training_method: set the training method for current layer, None value averts training
    
  attributes:
    current_layer: denotes the index of the current layer
    shape: denotes the dimension that the weights Matrix will assume
    weights: weight matrix, used to map the preceding neurons linearly to the current neurons
  
  """
  def __init__(self, network, neuron_count, learning_rate=1.0, training_method=None):
    self.network = network
    self.current_layer = len(self.network.layers)
    self.neuron_count = neuron_count
    self.learning_rate = learning_rate
    self.training_method = training_method
    # initialize the weights
    self.init_weights()
    
  def init_weights(self):
    input_count = len(self.network.activations[self.current_layer])
    self.shape = (self.neuron_count, input_count)
    total_neurons = sum(self.shape)
    range_ = np.sqrt(self.network.WEIGHT_SCALE / total_neurons)
    self.weights = np.random.uniform(-range_, range_, self.shape)
    
  def propagate_signal(self):
    forwarded_activation = self.weights @ self.network.activations[self.current_layer]
    magnitude = self.network.output_noise_mag
    noise = np.random.uniform(-magnitude, magnitude, forwarded_activation.shape)
    forwarded_activation = NeuralNetwork3.ACTIVATION(forwarded_activation) + noise
    self.network.activations[self.current_layer + 1] = forwarded_activation
    
  def train(self):
    if self.training_method:
      self.training_method(self, self.network.modulation_signal.getSignal(0))
    else:
      return

      