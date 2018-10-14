# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 12:51:39 2018

@author: ajdin
"""
import pygame
import numpy as np

RADIUS = 25
THICKNESS = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class NetworkVisualizer:
  FONT = 'Arial'
  FONT_SIZE = 18      
      
  def __init__(self, network, box):
    self.network = network
    self.box = box #(lower_x, lower_y, upper_x, upper_y)
    self.neuron_descriptions = []
    self.connection_descriptions = []
    self.layer_count = len(network.layers) + 1
    
    self.set_up()
    self.set_up_grid()
    self.set_up_connections()
    
    pygame.font.init()
    self.font = pygame.font.SysFont(self.FONT, self.FONT_SIZE, bold=True)
    
  def set_up(self):
    for i in range(self.layer_count):
      neuron_description = NeuronGroupDescription(self.network, i)
      self.neuron_descriptions.append(neuron_description)
      
  def set_up_grid(self):
    y_values = np.linspace(self.box[1], self.box[3], self.layer_count+1, endpoint=False)[1:]
    for i in range(self.layer_count):
      self.neuron_descriptions[i].y_value = y_values[i]
      neuron_count = len(self.neuron_descriptions[i].values)
      self.neuron_descriptions[i].x_values = np.linspace(self.box[0], self.box[2], \
                                                         neuron_count+1, endpoint=False)[1:]
      
  def set_up_connections(self):
    for i in range(self.layer_count - 1):
      connection_description = ConnectionDescription(self.network, i)
      connection_description.input_neuron_description = self.neuron_descriptions[i]
      connection_description.output_neuron_description = self.neuron_descriptions[i+1]
      self.connection_descriptions.append(connection_description)
          
  def visualize(self, display):
    self.draw_connections(display)
    self.draw_neurons(display)
    self.draw_legend(display)
  
  def draw_neurons(self, display):
    for i in range(self.layer_count):
      self.neuron_descriptions[i].draw(display, self.font)
  
  def draw_connections(self, display):
    for i in range(len(self.connection_descriptions)):
      self.connection_descriptions[i].draw(display, self.font)
      
  def draw_legend(self, display):
    y_offset = 50
    bar_length = 400
    box_center = (self.box[0]+self.box[2]) / 2
    x_start = box_center - 1/2*bar_length
    x_end = box_center + 1/2*bar_length
    color_positions = np.arange(x_start, x_end, 1)
    cap = self.network.weight_cap
    color_bar = np.linspace(-cap, cap, len(color_positions)-1 )
    for i in range(len(color_bar)):
      weight = color_bar[i]
      color = [(cap+weight)/(2*cap)*x for x in (255, 80, 0)]
      thickness = 2*weight/cap + 3
      start_point = (color_positions[i], y_offset)
      end_point = (color_positions[i+1], y_offset)
      pygame.draw.line(display, color, start_point, end_point, int(thickness))      
      if i==0 or (i+1)% 50 == 0 or i==398:
        text = '%.1f' % weight
        text_surface = self.font.render(text, False, BLACK)
        display.blit(text_surface, start_point)
    pass
  
      
class NeuronGroupDescription:
  
  def __init__(self, network, values_index):
    self.network = network
    self.idx = values_index
    self.y_value = None
    self.x_values = None
    
  @property  
  def values(self):
    return self.network.activations[self.idx]
    
  def draw(self, display, font):
    color = BLACK
    radius = RADIUS
    thickness = THICKNESS
    values = self.values
    for i in range(len(values)):
      position = (int(self.x_values[i]), int(self.y_value))
      pygame.draw.circle(display, WHITE, position, radius, 0)
      pygame.draw.circle(display, color, position, radius, thickness)
      text = '%.1f' % values[i]
      text_surface = font.render(text, False, BLACK)
      rect = text_surface.get_rect(center=position)
      display.blit(text_surface, rect)
  
    
class ConnectionDescription:
  
  def __init__(self, network, layer_index):
    self.network = network
    self.idx = layer_index
    self.input_neuron_description = None
    self.output_neuron_description = None
    self.cap = self.network.weight_cap
    
  @property
  def connections(self):
    return self.network.layers[self.idx].weights
  
  def draw(self, display, font):
    for i in range(self.connections.shape[0]):
      for j in range(self.connections.shape[1]):
        in_index = j
        out_index = i
        weight = self.connections[i][j]
        start_point = (self.input_neuron_description.x_values[in_index],
                       self.input_neuron_description.y_value)
        end_point = (self.output_neuron_description.x_values[out_index],
                     self.output_neuron_description.y_value)
        color = [(self.cap+weight)/(2*self.cap)*x for x in (255, 80, 0)]
        thick = 2*weight/self.cap + 3
        pygame.draw.line(display, color, start_point, end_point, int(thick))    
