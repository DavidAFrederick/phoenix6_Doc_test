import commands2

from drivetrain import DriveTrain

class DriveHeadingPID(commands2.CommandBase):
   def __init__(self, drivetrain:DriveTrain, targetHeading:float, speed:float) -> None:
       
       super().__init__()
       self.drivetrain = drivetrain
       self.targetHeading = targetHeading
       self.speed = speed
       self.addRequirements(drivetrain)

   def initialize(self) -> None:
       self.drivetrain.reset_gyro()
       self.drivetrain.setGyroPIDcontrollerSetPoint(self.targetHeading) 

   def execute(self) -> None:
       self.drivetrain.turn_PID(self.speed)  

   def isFinished(self) -> bool:
       return self.drivetrain.getGyroPIDcontrollerStatus()

   def end(self, interrupted: bool) -> None:
       self.drivetrain.drive_manually(0.0, 0.0)    # Stop the robot
