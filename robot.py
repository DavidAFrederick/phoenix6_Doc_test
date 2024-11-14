#!/usr/bin/env python3
import wpilib
from commands2 import (
    TimedCommandRobot,
    CommandScheduler,
    Command,
    PrintCommand,
    RunCommand,
    cmd,
)
from commands2.button import CommandXboxController
# import navx
import drivetrain
from ledsubsystem import LEDSubsystem
from  setledlightsflash import SetLEDlightsFlash
from setledlightson import SetLEDlightsOn

from typing import Tuple, List
from drivedistance import DriveDistance
from driveheading import DriveHeading
from drivedistancepid import DriveDistancePID
from driveheadingpid import DriveHeadingPID

class MyRobot(TimedCommandRobot):
    """Class that defines the totality of our Robot"""

    def robotInit(self) -> None:
        """
        This method must eventually exit in order to ever have the robot
        code light turn green in DriverStation. So, this will create an
        instance of the Robot that contains all the subsystems,
        button bindings, and operator interface pieces like driver
        dashboards
        """
        # self._gyro = navx.AHRS.create_spi()

        # Setup the operator interface (typically CommandXboxController)
        self._driver_controller = CommandXboxController(0)

        # Instantiate any subystems
        self._drivetrain = drivetrain.DriveTrain()
        self.led = LEDSubsystem()
        # self.led.setDefaultCommand(SetLEDlightsFlash(self.led) )
        # self.led.setDefaultCommand(SetLEDlightsOn(self.led) )




# Measured results with Gamepad on Windows VM with Drivers Station
# Forward:  Axis 1 -1
# Back:    Axis 1 +1

# Left Axis 0 -1
# Right Axis 0 + 1
#
#  2024 Cresendo   First parameter is forward then turn  
#                    


        # Setup the default commands for subsystems
        self._drivetrain.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            # Raw Axis 0 turns robot left (-1) and right (+1)
            # Raw Axix 1 moves robot forward (-1) and backward (+1)
            RunCommand(
                lambda: self._drivetrain.drive_manually(
                    -self._driver_controller.getRawAxis(1),      ##  THESE ARE BACKWARDS 
                    -self._driver_controller.getRawAxis(0),      # was positive 
                ),
                self._drivetrain,
            )
        )

        # # Drive forward at half speed for three seconds
        # self._driver_controller.a().onTrue(
        #     cmd.run(
        #         lambda: self._drivetrain.drive_manually(0.2, 0),
        #         self._drivetrain,
        #     ).withTimeout(3)
        # )
        # # Drive backward at half speed for three seconds
        # self._driver_controller.b().onTrue(
        #     cmd.run(
        #         lambda: self._drivetrain.drive_manually(-0.2, 0),
        #         self._drivetrain,
        #     ).withTimeout(3)
        # )
        self._driver_controller.a().onTrue( DriveHeading(self._drivetrain, -45, 0.5) )
        self._driver_controller.b().onTrue( DriveHeadingPID(self._drivetrain, 45, 0.3) )

        self._driver_controller.y().onTrue( DriveDistance(self._drivetrain, 7, 0.5) )
        self._driver_controller.x().onTrue( DriveDistancePID(self._drivetrain, 2, 0.3))

        self._auto_command = None

    def getAutonomousCommand(self) -> Command:
        return PrintCommand("Default auto selected")

    def teleopInit(self) -> None:
        if self._auto_command is not None:
            self._auto_command.cancel()
        self._drivetrain.zeroEncoders()
        self.led.setDefaultCommand(SetLEDlightsOn(self.led) )



    def testInit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
        self.led.setDefaultCommand(SetLEDlightsOn(self.led) )


    def autonomousInit(self) -> None:
        self._auto_command = self.getAutonomousCommand()

        if self._auto_command is not None:
            self._auto_command.schedule()

        self.led.setDefaultCommand(SetLEDlightsFlash(self.led) )


    def disabledPeriodic(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def testPeriodic(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        return super().teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
