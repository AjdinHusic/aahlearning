# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:28:13 2018

@author: ajdin
"""
import numpy as np

import xml.etree.ElementTree as ET
import pygame
import buffer
import visualnet

from controllers import ControlScheme as control
from Car import CarConfig, Car
from rangefinder import RangeFinderGroup as sensors
from net3 import NeuralNetwork3 as nn3
from Wall import EntityConfig, Wall
from modulation import ModulationScheme

###########################################################

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
redcolor = (0xff,0,0)

def drawText(font, text, pos, display):
  textSurf = font.render(text, False, black)
  display.blit(textSurf, pos)
  
def drawCenter(pos, display, options):
  x_scale = options['x_scale']
  x_translate = options['x_translate']
  position = tuple(int(x_scale*x+x_translate) for x in pos)
  pygame.draw.circle(display, redcolor, position, 5, 2)

class MapConfig:
  ROOT = ET.parse('Maps/XMap.xml').getroot()
  def __init__(self, root=ROOT):
    self.carConfig = CarConfig(root.find('Robot'))
    self.entities = [EntityConfig(x) for x in root.findall('Entity')]


class MapBuilder:
  def __init__(self):
    self.mapConfig = MapConfig()
    self.carConfig = self.mapConfig.carConfig
    self.entities = self.mapConfig.entities
    self.setUp()
    
  def setUp(self):
    carX = self.carConfig.x
    carY = self.carConfig.y
    carAngle = self.carConfig.angle
    self.car = Car((carX, carY), carAngle)    
    walls = []
    for entity in self.entities:
      if entity.type_ == 'Wall':
        posX = entity.x
        posY = entity.y
        relX = entity.relX
        relY = entity.relY
        walls.append(Wall((posX, posY),(posX+relX, posY+relY)))
      if entity.type_ == 'Point':
        pointX = entity.x
        pointY = entity.y
    self.point = (pointX, pointY)
    self.walls = walls


class CarMazeEnv:
  MAP_BUILDER = MapBuilder()
  DISPLAY_WIDTH = 1000
  DISPLAY_HEIGHT = 800
  OPTIONS = {'x_scale': 0.2184233207295375,
             'yScale': 0.22767977831846448,
             'x_translate': 133.81512733541817,
             'yTranslate': 138.1115070345661,
             'rotation': 180}
  
  def __init__(self):
    # initialize map objects
    self.car = self.MAP_BUILDER.car
    self.walls = self.MAP_BUILDER.walls
    self.rangefinder_group = sensors(self.car)
    self.center_point = self.MAP_BUILDER.point
    # initialize game variables
    self.resolution = (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
    self.clock = pygame.time.Clock()
    self.game_ext = False
    self.performance = 0
    self.ticks = 0
    # initialize algorithm settings
    self.network = nn3(inputcount=11, hiddencount=5, outputcount=1)
    self.mod_scheme = ModulationScheme(self.rangefinder_group, self.walls)
    self.mod_buffer = buffer.Buffer(self.network.initlen, maxlen=self.network.maxlen, \
                                    growth_fact=self.network.growth)
    # Initialize visual settings
    self.options = self.OPTIONS
    self.game_display = None
    self.font = None
    self.bounds = None
    self.calculate_bounds()
    self.network_visualizer = visualnet.NetworkVisualizer(self.network,
                                                          [self.bounds[0], 0, 1600, self.bounds[1]])
    pygame.init()
    pygame.font.init()
      
  def step(self, training=True):
    control.range_finder_control(self.network, self.rangefinder_group, angle_control=True)
    last_position = self.car.center
    self.car.update(self.walls)

    self.handle_training(training=True)
    self.rangefinder_group.update(self.walls)    
    self.performance += self.car.update_score(last_position, self.center_point) / 360
    reward = None
    done = False
    info = {'position': self.car.center, 
            'orientation': self.car.angle, 
            'can move': self.car.can_move, 
            'time tick': self.ticks}
    self.ticks += 1
    return self.rangefinder_group.activations, reward, done, info
  
  def handle_training(self, training=True):
    if training:
      self.mod_scheme.wall_avoidance()
      self.mod_buffer.add_sample(self.mod_scheme.modulations[0])
      if self.mod_buffer.isfull:
        modulation = np.mean(self.mod_buffer.samples)
        self.network.modulation_signal.set_signal(0, modulation)
        print('tick: ', self.ticks, ' modulation: ', modulation)
      self.network.train()
      
        
  def reset(self):
    self.__init__()
    return self.rangefinder_group.activations
  
  def render(self, size=(None)):
    # Draw the display and objects
    if self.game_display is None:
      if size is None:
        size = self.resolution
      self.game_display = pygame.display.set_mode(size)
      pygame.display.set_caption('raahn-simulation')
      if self.font is None:
        self.font = pygame.font.SysFont('Arial', 30)
    self.game_display.fill(white)
    for wall in self.walls:
      wall.draw(self.game_display, self.options)
    self.rangefinder_group.draw(self.game_display, self.options)
    self.car.draw(self.game_display, self.options)
    # Draw the texts
    drawText(self.font, 'tick: '+str(self.ticks), (10, 10), self.game_display)
    drawText(self.font, 'FPS: '+"%.1f" % self.clock.get_fps(), (200, 10), self.game_display)
    drawText(self.font, 'Performance: '+ '%.2f' % self.performance, (400, 10), self.game_display)
    drawText(self.font, 'Forward velocity: '+ '%.1f' % np.linalg.norm(list(self.car.speed)), 
             (700, 10), self.game_display)
    drawCenter(self.center_point, self.game_display, self.options)
    # Visualize the networks
    self.visualize_network(self.game_display, self.options)
    # Render the next frame
    pygame.display.flip()
    self.clock.tick(40)
  
  def close(self):
    self.game_ext = True
    pygame.quit()
    
  def calculate_bounds(self):
    if not self.bounds:
      xbound = 0
      ybound = 0
      for wall in self.walls:
        maxboundWallx = max(wall.startPoint[0], wall.endPoint[0])
        maxboundWally = max(wall.startPoint[1], wall.endPoint[1])
        xbound = max(xbound, maxboundWallx)
        ybound = max(ybound, maxboundWally)
      xbound = self.options['x_scale']*xbound+self.options['x_translate']
      ybound = self.options['x_scale']*ybound+self.options['x_translate']
      self.bounds = (xbound, ybound)    
 
  def visualize_network(self, display, options):
    self.network_visualizer.visualize(display)
      

  
