import commands2
from drivetrain import DriveTrain
class DriveHeading(commands2.CommandBase):
   def __init__(self, drivetrain:DriveTrain, heading:float, speed:float) -> None:
       super().__init__()
       self.drivetrain = drivetrain
       self.heading = heading
       self.speed = abs(speed)
       
       if self.heading  < 0:
           self.speed = -self.speed
       else:
           self.speed= self.speed
       self.addRequirements(drivetrain)


   def initialize(self) -> None:
       self.drivetrain.zeroEncoders()
       self.drivetrain.reset_gyro()  ## GYRO
    #    if self.heading  < 0:
    #        self.speed = -self.speed
    #    else:
    #        self.speed= self.speed
       
   def execute(self) -> None:

       self.drivetrain.drive_manually(0.0, self.speed)  ### Gyro
       #  Negative turn rotates robot to right
       # Angles are negative right
      
   def isFinished(self) -> bool:
    #    return abs(self.drivetrain.get_gyro_heading()) >= self.heading

       done = (abs(self.drivetrain.get_gyro_heading()) >= abs(self.heading))
       if done:
           print ("DONE   ", self.drivetrain.get_gyro_heading(), "  ", self.heading)
       else:
           print ("NOT DONE    ", self.drivetrain.get_gyro_heading(), "  ",self.heading)
           
       return done

   def end(self, interrupted: bool) -> None:
       self.drivetrain.drive_manually(0.0, 0.0)    # Stop the robot
