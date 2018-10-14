# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 18:40:16 2018

@author: ajdin
"""
from rangefinder import RangeFinder
from lines import get_dist


class ModulationSignal:
  NO_MODULATION = 0.0
  INVALID_INDEX = -1
  
  def __init__(self):
    self.modulations = []
  
  def add_signal(self, *args):
    if len(args) == 0:
      self.modulations.append(self.NO_MODULATION)
    elif len(args) == 1:
      self.modulations.append(args[0])
    return len(self.modulations) - 1

  def getSignal(self, index):
    if index < 0 or index >= len(self.modulations):
      return self.NO_MODULATION
    else:
      return self.modulations[index]
    
  def getSignalCount(self):
    return len(self.modulations)
  
  def set_signal(self, index, value):
    if index >= len(self.modulations):
      return
    self.modulations[index] = value


class ModulationScheme:
  MODULATION_STRENGTH = 1.0
  MODULATION_RESET = 0.0
  MODULATION_NOT_RESET = -1.0
  PERPENDICULAR = 90.0
  SCHEME_STRINGS = ['WallAvoidance', 'Acceleration', 'NaiveWallAvoidance', 'NaiveAcceleration']
  
  def __init__(self, rangefinder_group, walls):
    self.rangefinder_group = rangefinder_group
    self.walls = walls
    self.view_distance = 400.0
    self.viewline = RangeFinder(self.rangefinder_group.car, self.view_distance)
    self.modulations = [0.0]*len(self.SCHEME_STRINGS)
    # Initializes for no former experience
    self.last_angle_between = None
    self.last_wall_in_range = None
    self.compare_wall = None
    self.last_nearest_dist = None
    
  def modulate(self):
    """
    Modulates all schemes ever defined, so that a combination of schemes may be integrated.
    """
    self.viewline.update_position()
    walls_in_bounds = self.viewline.entities_in_bounds(self.walls)
    last_angle = None
    nearest_wall = None
    nearest_dist = self.view_distance
    # Get nearest wall or None
    for wall in walls_in_bounds:
      intersections = self.viewline.intersects(wall)
      if len(intersections) > 0:
        dist = get_dist(self.rangefinder_group.car.center, intersections[0])
        if dist < nearest_dist:
          nearest_dist = dist
          nearest_wall = wall
    
    # No previous wall yields nothing to modulate
    if not self.last_wall_in_range:
        self.modulations[0] = 0.0
        self.modulations[1] = 0.0
    else:
      angle_between = self.viewline.angle_between(self.last_wall_in_range)
      last_intersection = self.viewline.intersects(self.last_wall_in_range)[0]
      distance = get_dist(self.rangefinder_group.car.center, last_intersection)
      delta = angle_between - self.last_angle_between
      gamma = distance - self.last_nearest_dist
      if angle_between > self.PERPENDICULAR:
        modulation1 = self.MODULATION_STRENGTH*delta / self.rangefinder_group.car.ROTATE_SPEED
      else:
        modulation1 = -self.MODULATION_STRENGTH*delta / self.rangefinder_group.car.ROTATE_SPEED 
      modulation2 = self.MODULATION_STRENGTH*gamma / self.rangefinder_group.car.ACCELERATION
      self.modulations[0] = modulation1
      self.modulations[1] = modulation2
      
    # No current wall yields no angle to store
    if nearest_wall:
      last_angle = self.viewline.angle_between(nearest_wall)
    # Store last wall and angle in any case (may be None)
    self.last_angle_between = last_angle
    self.last_nearest_dist = nearest_dist
    self.last_wall_in_range = nearest_wall
    
  def wall_avoidance(self):
    # print('computing wall avoidance modulation: ', self.modulations[0])
    self.viewline.update_position()   
    walls_in_bounds = self.viewline.entities_in_bounds(self.walls)
    compare_wall = None
    nearest_dist = self.viewline.default_length
    # Get the nearest wall in the view_distance if any
    for wall in walls_in_bounds:
      intersections = self.viewline.intersects(wall)
      if len(intersections) > 0:
        dist = get_dist(self.rangefinder_group.car.center, intersections[0])
        if dist < nearest_dist:
          nearest_dist = dist
          compare_wall = wall          
    self.compare_wall = compare_wall
    # The angle to use for modulation. Should never be zero when the angle delta is calculated.
    # If it is, then there must be a bug.
    angle_between = 0.0
    new_last_angle = self.MODULATION_NOT_RESET    
    
    # If there is no nearest wall
    if not compare_wall:
      # If there is no previous wall, set the modulation to zero and reset the last angle
      if not self.last_wall_in_range:
        if self.last_angle_between != self.MODULATION_RESET:
          self.last_angle_between = self.MODULATION_RESET
          self.modulations[0] = 0.0
        # nothing to modulate, and nothing to save, Don't Continue
        return      
      # Just left a wall
      else:
        angle_between = self.viewline.angle_between(self.last_wall_in_range)  
    
    # If the wall has changed
    elif compare_wall != self.last_wall_in_range:
      # There was a last wall that is different from the current wall
      if self.last_wall_in_range:
        angle_between = self.viewline.angle_between(self.last_wall_in_range)
        new_last_angle = self.viewline.angle_between(compare_wall)     
      # It is the first time any wall was hit, don't continue
      # Save the angle between last and current wall
      else:
        angle_between = self.viewline.angle_between(compare_wall)
        self.last_angle_between = angle_between
        self.last_wall_in_range = compare_wall
        return   
    
    # The usual case, the last wall is equal to the current wall
    else:
      angle_between = self.viewline.angle_between(compare_wall)
      new_last_angle = angle_between      
    delta = angle_between - self.last_angle_between
    modulation = self.MODULATION_STRENGTH    
    
    
    if angle_between > self.PERPENDICULAR:
      modulation *= delta / self.rangefinder_group.car.ROTATE_SPEED
    else:
      modulation *= -delta / self.rangefinder_group.car.ROTATE_SPEED      
    self.modulations[0] = modulation    
    self.last_angle_between = new_last_angle
    self.last_wall_in_range = compare_wall
    
  def naive_wall_avoidance(self):
    print(self.modulations)
    self.modulations[0] = self.last_forward_activation - self.rangefinder_group.activations[5]
    self.last_forward_activation = self.rangefinder_group.activations[5]
    pass
     
  def naive_acceleration(self):
    # if self.last_wall_in_range:
    # intersections = self.viewline.intersects(self.last_wall_in_range)
    self.modulations[1] = 1-2*abs(self.modulations[0])
    # print('computing acceleration modulation: ', self.modulations[1])
    return
  
  def acceleration(self):
    # If there is no nearest wall in range
    if not self.last_wall_in_range:
      if self.last_nearest_dist:
        self.last_nearest_dist = None
        self.modulations[1] = 0.0
      return
    else:
      intersection = self.viewline.intersects(self.last_wall_in_range)[0]
      nearest_dist = get_dist(self.rangefinder_group.car.center, intersection)
    
    pass
  
  SCHEMES = [wall_avoidance, acceleration, naive_wall_avoidance, naive_acceleration]
  
  @staticmethod
  def get_scheme_from_string(scheme_string):
    for i in range(len(ModulationScheme.SCHEME_STRINGS)):
      if scheme_string == ModulationScheme.SCHEME_STRINGS[i]:
        return i  
    return -1

  @staticmethod
  def getSchemeFunction(scheme):
    if scheme >= 0 and scheme < len(ModulationScheme.SCHEMES):
      return ModulationScheme.SCHEMES[scheme]
    else:
      return None
    
  def reset(self):
    self.last_angle_between = self.MODULATION_RESET
    self.last_wall_in_range = None

    
    
    
    