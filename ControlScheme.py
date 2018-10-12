import pygame


class ControlScheme:
  
  
  def __init__(self, ann, car):
    self.brain = ann
    self.car = car
    self.userControl = False
    
  def userControlled(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          self.brain.set_output(0, 0, 0.0)
          self.userControl == True
        elif event.key == pygame.K_RIGHT:
          self.brain.set_output(0, 0, 1.0)
          self.userControl == True
      elif event.type == pygame.KEYUP:
        self.userControl = False
          
  def rangeFinderControl(self, rangefinder_group, angle_control=True, acceleration_control=True):
    self.userControl = False
    inputs = rangefinder_group.activations
    self.brain.addExperience(inputs)
    self.brain.propagate_signal()
    output = self.brain.get_output_value(0,0)
    output2 = self.brain.get_output_value(0,1)
    if angle_control:
      self.car.angle += (output*self.car.ROTATE_RANGE) - self.car.ROTATE_SPEED
      self.car.angle = self.car.angle % 360
    #self.car.acceleration = 0
    if acceleration_control:
      self.car.acceleration = (output2*self.car.ACCELERATION_RANGE) - self.car.ACCELERATION
    return self.userControl

    

