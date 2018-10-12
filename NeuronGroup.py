import numpy as np
from TrainingMethod import TrainingMethod

class NeuronGroup:
  DEFAULT_NEURON_VALUE = 0.0
  
  class Identifier:
    def __init__(self, index=0, type_=0):
      self.index = index
      self.type_ = type_


  def __init__(self, count, network, type_):
    self.ann = network
    self.averages = None
    self.computed = True
    self.use_noise = False
    self.neurons = []
    self.add_neurons(count)
    # Define ConnectionGroups surround current NeuronGroup
    self.incoming_groups = []
    self.outgoing_groups = []
    # Define the outgoing_groups that train only off the most recent experience
    self.out_train_recent = []
    # Define the outgoing_groups that train off of several randomly selected experiences
    self.out_train_several = []
    self.type_ = type_
    self.index = None

  def add_neurons(self, count):
    for i in range(count):
      self.neurons.append(self.DEFAULT_NEURON_VALUE)

  def compute_signal(self):
    for group in self.incoming_groups:
      group.propagate_signal()
    # Finish computing the signal by applying the activation function
    #Add noise if Hebbian trained connections are present
    if self.use_noise:
      for i in range(len(self.neurons)):
        noise = np.random.uniform()*self.ann.output_noise_range - self.ann.output_noise_magnitude
        self.neurons[i] = self.ann.activation(self.neurons[i]) + noise
    else:
      for neuron in self.neurons:
        neuron = self.ann.activation(neuron)
    self.computed = True

  def add_incoming_group(self, incoming_group):
    self.incoming_groups.append(incoming_group)
    self.use_noise = True

  def add_out_going_group(self, outgoing_group, most_recent):
    self.outgoing_groups.append(outgoing_group)
    if most_recent:
      self.out_train_recent.append(outgoing_group)
    else:
      self.out_train_several.append(outgoing_group)
      
  def reset(self):
      for i in range(len(self.neurons)):
          self.neurons[i] = 0.0
          
  def train_recent(self):
    if len(self.out_train_recent) < 1:
      return TrainingMethod.NO_ERROR    
    error = 0.0
    for i in range(len(self.out_train_recent)):
      if self.out_train_recent[i].training_method == TrainingMethod.sparseAutoEncoderTrain:
        self.updateAverages()        
      error += self.out_train_recent[i].train()      
    return error
  
  def train_several(self):
    if len(self.out_train_several) < 1:
      return TrainingMethod.NO_ERROR
    pass
  
  def updateAverages(self):
    #decay = 0.0
    pass
          
      




