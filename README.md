# RobinGame
Object-oriented tools for PyGame projects :) 

Todo: 
- Make EventQueue instance-based instead of class-based (or at least allow multiple instances to be created with separate contents, so you can have multiple event queues if you want)
- Input / controller overhaul
  - Do we need the is_pressed / is_released stuff? Can we use keyup / down events instead? 
  - Perhaps the relevant classes can implement the event-based method under the hood, so the interface doesn't change.

