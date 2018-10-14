import numpy as np

class TrainingMethod(object):
  HEBBIAN_SCALE = 2.0
  HEBBIAN_OFFSET = HEBBIAN_SCALE / 2.0
  NO_ERROR = 0.0
  
  @staticmethod
  def hebbian_learning(layer, modulation):
    normalized_input = layer.network.activations[layer.current_layer]
    normalized_input = np.reshape(normalized_input, (-1, 1))
    normalized_output = layer.network.activations[layer.current_layer + 1]
    normalized_output = normalized_output*TrainingMethod.HEBBIAN_SCALE - TrainingMethod.HEBBIAN_OFFSET
    normalized_output = np.reshape(normalized_output, (-1, 1))
    noise_mag = layer.network.weight_noise_mag
    noise = np.random.uniform(-noise_mag, noise_mag, layer.shape)
    lr = layer.learning_rate
    cap = layer.network.weight_cap
    weight_delta = modulation*lr*(normalized_output @ normalized_input.T) + noise
    layer.weights = np.clip(layer.weights + weight_delta, -cap, cap)
    
  @staticmethod
  def hebbian_history_learning(layer, modulation):
    if layer.history_buffer.isfull:
      for sample in iter(layer.history_buffer):
        normalized_input = np.reshape(sample[0], (-1, 1))
        normalized_output = np.reshape(sample[1], (-1, 1))
        normalized_output = normalized_output*TrainingMethod.HEBBIAN_SCALE - TrainingMethod.HEBBIAN_OFFSET
        noise_mag = layer.network.weight_noise_mag
        noise = np.random.uniform(-noise_mag, noise_mag, layer.shape)
        lr = layer.learning_rate
        cap = layer.network.weight_cap      
        weight_delta = modulation*lr*(normalized_output @ normalized_input.T) + noise
        layer.weights = np.clip(layer.weights + weight_delta, -cap, cap)
        
      



