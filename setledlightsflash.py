import wpilib
import commands2
from ledsubsystem import LEDSubsystem

class SetLEDlightsFlash(commands2.CommandBase):
   def __init__(self, led: LEDSubsystem) -> None:      
       super().__init__()

       self.led = led
       self.addRequirements(led)
       self.flashcounter = 0
       self.orangeOn = True

   def initialize(self) -> None:
       pass       #  This function is not being used.
       self.flashcounter = 0

   def execute(self) -> None:
       self.flashcounter = self.flashcounter + 1
       if (self.flashcounter > 40):
           self.flashcounter = 0
           self.orangeOn = not self.orangeOn
      
       if (self.orangeOn):
            self.led.setTaillightOrange()
       else:
            self.led.setTaillightBlack()
           

   def end(self, interrupted: bool) -> None:
       pass       #  This function is not being used.

   def isFinished(self) -> bool:
       return False
