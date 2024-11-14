import commands2

from drivetrain import DriveTrain

class DriveDistancePID(commands2.CommandBase):
   def __init__(self, drivetrain:DriveTrain, count:float, speed:float) -> None:
       
       super().__init__()
       self.drivetrain = drivetrain
       self.count = count
       self.speed = speed
       self.addRequirements(drivetrain)

   def initialize(self) -> None:
       self.drivetrain.zeroEncoders()
       self.drivetrain.setPIDcontrollerSetPoint(self.count) 



   def execute(self) -> None:
    #    self.drivetrain.drive_manually(self.speed, 0.0)
       self.drivetrain.drive_PID(self.speed)  

      
   def isFinished(self) -> bool:
    #    return self.drivetrain.get_left_encoder_value() >= self.count
       return self.drivetrain.getPIDcontrollerStatus()



   def end(self, interrupted: bool) -> None:
       self.drivetrain.drive_manually(0.0, 0.0)    # Stop the robot
       self.drivetrain.zeroEncoders()
