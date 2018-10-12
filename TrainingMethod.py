import numpy as np
from Modulation import ModulationSignal

class TrainingMethod(object):
  HEBBIAN_SCALE = 2.0
  HEBBIAN_OFFSET = HEBBIAN_SCALE / 2.0
  NO_ERROR = 0.0
  
  @staticmethod
  def sparseAutoEncoderTrain(mod_indices, learning_rate, ann, input_group, output_group, connections,\
                             bias_weights):
    pass

  @staticmethod
  def hebbianTrain(mod_indices, learning_rate, ann, input_group, output_group, connections, bias_weights):
      mod_signals = [ann.mod_signal.getSignal(modIndex) for modIndex in mod_indices]
#      if modSig == ModulationSignal.NO_MODULATION:
#          return TrainingMethod.NO_ERROR

      weight_cap = ann.weight_cap
      for i in range(len(connections)):
          normalizedInput = input_group.neurons[connections[i].input]
          normalizedOutput = output_group.neurons[connections[i].output]*TrainingMethod.HEBBIAN_SCALE - TrainingMethod.HEBBIAN_OFFSET
          noise = np.random.uniform()*ann.weight_noise_range - ann.weight_noise_magnitude
          
          modSig = mod_signals[connections[i].output]
          if modSig == ModulationSignal.NO_MODULATION:
            continue
          weightDelta = (modSig * learning_rate * normalizedInput * normalizedOutput) + noise
          connections[i].weight = np.clip(connections[i].weight + weightDelta, -weight_cap, weight_cap)
      return TrainingMethod.NO_ERROR
    
  @staticmethod
  def hebbianBatchesTrain(mod_indices, learning_rate, ann, input_buffer, output_buffer, 
                          connections, bias_weights):
    mod_signals = [ann.mod_signal.getSignal(modIndex) for modIndex in mod_indices]
    weight_cap = ann.weight_cap
    for sample in input_buffer:
      pass
    for i in range(len(connections)):
      normalized_inputs = []       
      pass




