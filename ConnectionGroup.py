
class ConnectionGroup:
  """
  Connects neurons from a neural network, using the interior Connection class, serving as 
  containers for the network's weights and indices connecting said neurons between adjacent 
  layers.
  
  """
  DEFAULT_LEARNING_RATE = 0.1
  
  class Connection:
    """
    Contains a connection and and stores its weight and indices that connect between said weight 
    within two adjacent layers.
    """
        
    def __init__(self, i=0, o=0, w=0.0):
      self.input = i
      self.output = o
      self.weight = w

  
  def __init__(self, network, input_group, output_group, use_bias):
    self.sample_count = None
    self.mod_indices = None
    self.learning_rate = self.DEFAULT_LEARNING_RATE
    self.connections = []
    self.ann = network
    # Define neuron groups which interconnect SELF (connectiongroup)
    self.input_group = input_group
    self.output_group = output_group
    self.training_method = None
    self.use_bias = use_bias
    if use_bias:
      self.bias_weights = []
    else:
      self.bias_weights = None    
      
  def add_connection(self, input_index, output_index, weight):
    self.connections.append(self.Connection(input_index, output_index, weight))

  def propagate_signal(self):
    # Make sure the input group is computed
    if not self.input_group.computed:
      self.input_group.compute_signal()
    for connection in self.connections:
      self.output_group.neurons[connection.output] += \
      self.input_group.neurons[connection.input]*connection.weight
    if self.use_bias:
      for i in range(len(self.bias_weights)):
        self.output_group.neurons[i] += self.bias_weights[i]
        
  def train(self):
    return self.training_method(self.mod_indices, self.learning_rate, self.ann, self.input_group,\
                                self.output_group, self.connections, self.bias_weights)


############################################################
if __name__ == "__main__":
  connectionGroup = ConnectionGroup(None, None, None, False)
  connectionGroup.add_connection(2, 2, 2)
  print(connectionGroup.connections)




