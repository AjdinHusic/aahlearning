
import numpy as np
from collections import deque

from Modulation import ModulationScheme, ModulationSignal
from NeuronGroup import NeuronGroup
from ConnectionGroup import ConnectionGroup
from RaahnXmlConfig import NeuralNetworkConfig
from TrainingMethod import TrainingMethod
from Activation import Activation


class NeuralNetwork:
  """
  creates a NeuralNetwork, consisting of three possible types:
    inputlayers, hidden layers and outputlayers.
  """
  # Number of nearest neighbors to use for novelty score calculations.
  N_NEAREST = 20;
  # How many distances to keep for each experience.
  N_KEEP = N_NEAREST + 20;
  DEFAULT_NOISE_MAGNITUDE = 1.0;
  DOUBLE_MAGNITUDE = 2.0;
  WEIGHT_RANGE_SCALE = 6.0;
  DOUBLE_WEIGHT_RANGE = 2.0;
  DEFAULT_LEARNING_RATE = 0.1
  NEURON_GROUP_TYPES = ['Input', 'Hidden', 'Output']
  UNIQUE_GROUP_TYPES = 3
  AUTOENCODER_TRAIN = 'Autoencoder'
  HEBBIAN_TRAIN = 'Hebbian'

  def __init__(self, output_noise_mag=DEFAULT_NOISE_MAGNITUDE, weight_noise_mag=DEFAULT_NOISE_MAGNITUDE):
    self.output_noise_magnitude = output_noise_mag
    self.weight_noise_magnitude = weight_noise_mag
    self.output_noise_range = self.output_noise_magnitude * self.DOUBLE_MAGNITUDE
    self.weight_noise_range = self.weight_noise_magnitude * self.DOUBLE_MAGNITUDE
    self.weight_cap = 10
    self.average_error = 0.0
    self.input_groups = []
    self.hidden_groups = []
    self.output_groups = []
    # Collect all the NeuronGroups
    self.all_groups = []
    self.all_groups.append(self.input_groups)
    self.all_groups.append(self.hidden_groups)
    self.all_groups.append(self.output_groups)
    self.learning_rate = self.DEFAULT_LEARNING_RATE
    self.ordered_group_ids = [[] for _ in range(self.UNIQUE_GROUP_TYPES)]
    self.activation = Activation.logistic
    self.activation_derivative = Activation.logisticDerivative
    self.modulation_functions = []
    self.modulation_scheme = ModulationScheme
    self.mod_signal = ModulationSignal()
    self.use_history = False

  def configure(self):
    network_config = NeuralNetworkConfig()
    self.output_noise_magnitude = 0.1
    self.output_noise_range = self.output_noise_magnitude * self.DOUBLE_MAGNITUDE
    self.weight_noise_magnitude = 0.1
    self.weight_noise_range = self.weight_noise_magnitude * self.DOUBLE_MAGNITUDE
    self.weight_cap = network_config.weight_cap
    if network_config.historyBufferSize > 0:
      self.use_history = True
      self.history_buffer = deque()
      self.current_buffer_length = network_config.historyBufferSize
    neuron_groups = network_config.neuron_groups
    neuron_group_ids = []
    # Add each neuron group.    
    for i in range(len(network_config.neuron_groups)):
      type_ = self.get_grouptype_from_string(neuron_groups[i].type_)
      index = self.add_neuron_group(neuron_groups[i].count, type_)
      neuron_group_ids.append(index)
      self.ordered_group_ids[type_].append(index)      
    # Add each connection group
    for i in range(len(network_config.connection_group_configs)):
      connection_config = network_config.connection_group_configs[i]
      input_group_index = self.get_id_index(connection_config.input_group_id, neuron_groups)
      output_group_index = self.get_id_index(connection_config.output_group_id, neuron_groups)     
      input_type_string = neuron_groups[input_group_index].type_
      input_group = NeuronGroup.Identifier(neuron_group_ids[input_group_index],\
                                          self.get_grouptype_from_string(input_type_string))          
      output_type_string = neuron_groups[output_group_index].type_
      output_group = NeuronGroup.Identifier(neuron_group_ids[output_group_index],\
                                           self.get_grouptype_from_string(output_type_string))      
      training_method = self.get_method_from_string(connection_config.training_method)    
      mod_descriptors = [ModulationScheme.get_scheme_from_string(scheme) for scheme \
                         in connection_config.modulation_schemes]
      mod_functions = [ModulationScheme.SCHEMES[descriptor] for descriptor in mod_descriptors]   
      mod_signals = []
      for function in mod_functions:
        self.modulation_functions.append(function)
        mod_signals.append(self.mod_signal.add_signal())
      self.connect_groups(input_group, output_group, training_method, mod_signals,\
                         connection_config.samplesPerTick, connection_config.learning_rate,\
                         connection_config.use_bias)
        
  def addExperience(self, new_experience):
    ## complement code
    self.set_experience(new_experience)
    if self.use_history:
      self.history_buffer.append(new_experience)
      while len(self.history_buffer) > self.current_buffer_length:
        if len(self.history_buffer) < 2:
          break
        self.history_buffer.popleft()

  def set_experience(self, *args):
    sample= None
    data_count = 0
    sample_index = None
    if len(args)==1 and isinstance(args[0], int):
      sample_index = args[0]
    elif len(args)==1 and isinstance(args[0], list):
      sample = args[0]
      
    data_count = len(sample)
    sample_index = 0
    for x in range(len(self.input_groups)):
      if data_count <= 0:
        # print('Data count not larger than zero')
        break
      neuron_count = len(self.input_groups[x].neurons)   
      if data_count < neuron_count:
        neuron_count = data_count
      for y in range(neuron_count):
        self.input_groups[x].neurons[y] = sample[sample_index]
        sample_index += 1
      data_count -= neuron_count

  def propagate_signal(self):
    # Reset the computed state of hidden layer neurons
    # Also reset the values for hidden and output neurons
    for i in range(len(self.hidden_groups)):
      self.hidden_groups[i].computed = False
      self.hidden_groups[i].reset()
    for i in range(len(self.output_groups)):
      self.output_groups[i].reset()  
    for i in range(len(self.output_groups)):
      self.output_groups[i].compute_signal()

  def add_neuron_group(self, neuron_count, type_):
    new_neuron_group = NeuronGroup(neuron_count, self, type_)
    if type_ == 0:
      self.input_groups.append(new_neuron_group)
      group_index = len(self.input_groups) - 1
      new_neuron_group.index = group_index
      return group_index
    elif type_ == 1:
      self.hidden_groups.append(new_neuron_group)
      group_index = len(self.hidden_groups) - 1
      new_neuron_group.index = group_index
      return group_index
    elif type_ == 2:
      self.output_groups.append(new_neuron_group)
      group_index = len(self.output_groups) - 1
      new_neuron_group.index = group_index
      return group_index
    else:
      return -1
  
  def get_grouptype_from_string(self, type_):
    for i in range(len(self.NEURON_GROUP_TYPES)):
      if type_ == self.NEURON_GROUP_TYPES[i]:
        return i
    return -1
  
  def get_method_from_string(self, method):
    if method == self.AUTOENCODER_TRAIN:
      return
    else:
      return TrainingMethod.hebbianTrain
  
  def get_id_index(self, id_, neuron_groups):
    for i in range(len(neuron_groups)):
      if id_ == neuron_groups[i].id :
        return i
    #Return the first index if the id is not found.  
    return 0
    
  def connect_groups(self, input_group, output_group, training_method, mod_indices, sample_count,\
                     learning_rate, use_bias):
    in_group = self.all_groups[input_group.type_][input_group.index]
    out_group = self.all_groups[output_group.type_][output_group.index]
    connection_group = ConnectionGroup(self, in_group, out_group, use_bias)
    connection_group.sample_count = sample_count
    connection_group.learning_rate = learning_rate
    connection_group.training_method = training_method
    connection_group.mod_indices = mod_indices
    total_neuron_count = len(in_group.neurons) + len(out_group.neurons)
    if use_bias:
      total_neuron_count += 1
    for x in range(len(in_group.neurons)):
      # Randomize weights
      for y in range(len(out_group.neurons)):
        Range = np.sqrt(self.WEIGHT_RANGE_SCALE / total_neuron_count)
        # Keep in the range of [-Range, Range]
        weight = np.random.uniform()*Range*self.DOUBLE_WEIGHT_RANGE - Range
        connection_group.add_connection(x, y, weight)   
    if use_bias:
      pass
    # sample count of zero refers to training off of the most recent experience.
    in_group.add_out_going_group(connection_group, sample_count == 0)
    out_group.add_incoming_group(connection_group)
    return True
  
  def get_output_value(self, group_index, index):
    return self.output_groups[group_index].neurons[index]
  
  def set_output(self, group_index, index, value):
    self.output_groups[group_index].neurons[index] = value
    return True
  
  def train(self):
    error = 0.0
    for i in range(len(self.input_groups)):
      error += self.input_groups[i].train_recent()      
    for i in range(len(self.hidden_groups)):
      error += self.hidden_groups[i].train_recent()      
    for i in range(len(self.input_groups)):
      error += self.input_groups[i].train_several()     
    for i in range(len(self.hidden_groups)):
      error += self.hidden_groups[i].train_several()      
    self.update_online_error(error)
    
  def update_online_error(self, current_error):
    pass
  
  def get_all_weights(self):
    weights = []
    for group in self.input_groups:
      for outgoing in group.outgoing_groups:
        layer_weights = [connection.weight for connection in outgoing.connections]
        weights.append(layer_weights)
    return weights
  


