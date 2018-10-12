# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 18:49:33 2018

@author: ajdin
"""
import xml.etree.ElementTree as ET

root = ET.parse('Networks/XMapHebbian.xml').getroot()

class NeuralNetworkConfig:
  ROOT = ET.parse('Networks/XMapHebbian.xml').getroot()
  def __init__(self, root=ROOT):
    if root.get('UseNovelty'):
      self.useNovelty = root.get('UseNovelty') == 'true'
    else:
      self.useNovelty = None
    self.historyBufferSize = int(root.find('HistoryBufferSize').text)
    self.weight_cap = float(root.find('WeightCap').text)
    self.output_noise_magnitude = float(root.find('OutputNoiseMagnitude').text)
    self.weight_noise_magnitude = float(root.find('WeightNoiseMagnitude').text)
    self.control_scheme = root.find('ControlScheme').text
    self.parameters = [int(x.text) for x in root.findall('Parameter')]
    self.neuron_groups = [NeuronGroupConfig(x) for x in root.findall('NeuronGroup')]
    self.connection_group_configs = [ConnectionConfig(x) for x in root.findall('ConnectionGroup')]
        
class NeuronGroupConfig:
  NODE = root.find('NeuronGroup')
  
  def __init__(self, node=NODE):
    self.id = int(node.get('Id'))
    self.count = int(node.find('Count').text)
    self.type_ = node.find('Type').text
    
class ConnectionConfig:
  NODE = root.find('ConnectionGroup')
  
  def __init__(self, node=NODE):
    self.input_group_id = int(node.find('InputGroup').text)
    self.output_group_id = int(node.find('OutputGroup').text)
    if node.find('SamplesPerTick') is not None:
      self.samplesPerTick = int(node.find('SamplesPerTick').text)
    else:
      self.samplesPerTick = 0
    self.use_bias = node.get('UseBias') == 'true'
    self.learning_rate = float(node.find('LearningRate').text)
    self.training_method = node.find('TrainingMethod').text
    self.modulation_schemes = [x.text for x in node.findall('ModulationScheme')]
    if node.find('ModulationScheme') is not None:
      self.modulation_scheme = node.find('ModulationScheme').text
    else:
      self.modulation_scheme = None













      