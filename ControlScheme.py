class ControlScheme:
  
  @staticmethod
  def range_finder_control(network, rangefinder_group, angle_control=True, acceleration_control=True):
    inputs = rangefinder_group.activations
    network.add_experience(inputs)
    network.propagate_signal()
    output = float(network.activations[-1][0])
    if angle_control:
      rangefinder_group.car.angle += (output*rangefinder_group.car.ROTATE_RANGE) \
                                    - rangefinder_group.car.ROTATE_SPEED
      rangefinder_group.car.angle = rangefinder_group.car.angle % 360
    if acceleration_control:
      if len(network.activations[-1]) > 1:
        rangefinder_group.car.acceleration = float(network.activations[-1][1])
    return output
    

    

