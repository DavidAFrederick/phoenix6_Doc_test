import wpilib.drive
from commands2 import Subsystem, Command
from phoenix6.configs import TalonFXConfiguration, TalonFXConfigurator
from phoenix6.hardware.talon_fx import TalonFX
from phoenix6.controls.follower import Follower
from phoenix6.signals.spn_enums import (
    InvertedValue,
    NeutralModeValue,
    FeedbackSensorSourceValue,
)
from phoenix6.sim import ChassisReference
from phoenix6.controls import DutyCycleOut

import navx  # Import the Gyro Vendor library

import constants
import math
import wpimath
import wpilib
if wpilib.RobotBase.isSimulation():
    from pyfrc.physics.units import units

class DriveTrain(Subsystem):
    DT_TICKS_PER_MOTOR_REV = int(2048)
    if wpilib.RobotBase.isSimulation():
        DT_TICKS_PER_INCH = (DT_TICKS_PER_MOTOR_REV * constants.DT_HIGH_GEAR_RATIO) / (
            (2 * math.pi) * constants.DT_WHEEL_DIAMETER.m_as(units.inch)
        )

    def __init__(self) -> None:
        super().__init__()

        self._gyro = navx.AHRS.create_spi()        # Instantate the Gyro

        self._left_leader = TalonFX(constants.DT_LEFT_LEADER)
        self._left_follower = TalonFX(constants.DT_LEFT_FOLLOWER)
        self._right_leader = TalonFX(constants.DT_RIGHT_LEADER)
        self._right_follower = TalonFX(constants.DT_LEFT_FOLLOWER)

        self.__configure_left_side_drive()
        self.__configure_right_side_drive()

        self._left_duty_cyle: DutyCycleOut = DutyCycleOut(0, enable_foc=False)
        self._left_duty_cyle.update_freq_hz = 0
        self._right_duty_cycle: DutyCycleOut = DutyCycleOut(0, enable_foc=False)
        self._right_duty_cycle.update_freq_hz = 0

        self._left_follower.set_control(Follower(self._left_leader.device_id, False))
        self._right_follower.set_control(Follower(self._right_leader.device_id, False))

         # PID Specific Updates
        # proportional speed constant
        self.kP = 0.5
        # integral speed constant
        self.kI = 0.0
        # derivative speed constant
        self.kD = 0.0 
        self.targetEncoderValue = 0
        self.pidController = wpimath.controller.PIDController(self.kP, self.kI, self.kD)


         # PID Specific Updates
        # proportional speed constant
        self.gyro_kP = 0.4
        # integral speed constant
        self.gyro_kI = 0.0
        # derivative speed constant
        self.gyro_kD = 0.05 
        self.targetGyroValue = 0
        self.gyro_pidController = wpimath.controller.PIDController(self.gyro_kP, self.gyro_kI, self.gyro_kD)

    def __configure_left_side_drive(self) -> None:
        # Applying a new configuration will erase all other config settings since we start with a blank config
        # so each setting needs to be explicitly set here in the config method
        config = TalonFXConfiguration()

        # Set the left side motors to be counter clockwise positive

        ## TRYING  CHANGE FOR SIMULATION
        # config.motor_output.inverted = InvertedValue.COUNTER_CLOCKWISE_POSITIVE

        #  REAL ROBOT
        config.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE    #Verified on real Robot

        # Set the motors to electrically stop instead of coast
        config.motor_output.neutral_mode = NeutralModeValue.BRAKE
        # PID controls will use integrated encoder
        config.feedback.feedback_sensor_source = FeedbackSensorSourceValue.ROTOR_SENSOR
        config.feedback.sensor_to_mechanism_ratio = 10

        # Apply the configuration to the motors
        self._left_leader.configurator.apply(config)
        self._left_follower.configurator.apply(config)

        self._left_leader.sim_state.Orientation = (
            ChassisReference.CounterClockwise_Positive
        )
        self._left_follower.sim_state.Orientation = (
            ChassisReference.CounterClockwise_Positive
        )

        # https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/simulation/simulation-intro.html

        # self._left_leader.sim_state.Orientation = (ChassisReference.CounterClockwise_Positive)
        # self._left_follower.sim_state.Orientation = (ChassisReference.CounterClockwise_Positive)
        

    def __configure_right_side_drive(self) -> None:
        # Applying a new configuration will erase all other config settings since we start with a blank config
        # so each setting needs to be explicitly set here in the config method
        config = TalonFXConfiguration()

        # Set the left side motors to be counter clockwise positive
        #  REAL ROBOT
        # config.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE
        config.motor_output.inverted = InvertedValue.COUNTER_CLOCKWISE_POSITIVE   #Verified on real Robot  5

        # Set the motors to electrically stop instead of coast
        config.motor_output.neutral_mode = NeutralModeValue.BRAKE
        # PID controls will use integrated encoder
        config.feedback.feedback_sensor_source = FeedbackSensorSourceValue.ROTOR_SENSOR
        config.feedback.sensor_to_mechanism_ratio = 10

        # Apply the configuration to the motors
        self._right_leader.configurator.apply(config)
        self._right_follower.configurator.apply(config)

        self._right_leader.sim_state.Orientation = ChassisReference.Clockwise_Positive
        self._right_follower.sim_state.Orientation = ChassisReference.Clockwise_Positive


    # def drive_manually(self, forward: float, turn: float) -> None:
    #     self._left_duty_cyle.output = forward - turn
    #     self._right_duty_cycle.output = forward + turn

    #     self._left_leader.set_control(self._left_duty_cyle)
    #     self._right_leader.set_control(self._right_duty_cycle)


                ###  The parameters are reversed as compared to 2024 Cresendo
                ###   def drive_teleop(self, forward: float, turn: float, percent_out=False):
    # def drive_manually(self, turn: float, forward: float) -> None:    #  Code as per Phoenix6
    def drive_manually(self, forward: float, turn: float) -> None:

        REDUCTION = 0.4
        forward = forward * REDUCTION
        turn = turn * REDUCTION

        # self._left_duty_cyle.output = forward + turn
        # self._right_duty_cycle.output = forward - turn

        self._left_duty_cyle.output = forward - turn    # Verifed on real hardware   5
        self._right_duty_cycle.output = forward + turn

        self._left_leader.set_control(self._left_duty_cyle)
        self._right_leader.set_control(self._right_duty_cycle)

        print ("Manual: Fwd: %5.2f  Turn: %5.2f  L-Encoder %6.0f  Speed  L: %5.2f  R: %5.2f  Gyro: %4.1f    " %
              (forward, turn, self.get_left_encoder_value(), self._left_duty_cyle.output,
               self._right_duty_cycle.output,  self.get_gyro_heading()))

    def get_left_encoder_value(self) -> float:
       return self._left_leader.get_position().value


    def get_right_encoder_value(self) -> float:
       return self._right_leader.get_position().value


    def zeroLeftEncoder(self):
       self._left_leader.set_position(0)


    def zeroRightEncoder(self):
       self._right_leader.set_position(0)


    def zeroEncoders(self):
        self.zeroLeftEncoder()
        self.zeroRightEncoder()

    def setPIDcontrollerSetPoint (self, setpoint : float):
       self.targetEncoderValue = setpoint

    def getPIDcontrollerStatus (self) -> bool:
       return self.pidController.atSetpoint()


    def drive_PID(self, max_speed : float) -> None:

       left_encoder = self.get_left_encoder_value()
       target_count = self.targetEncoderValue
       forward = self.pidController.calculate( left_encoder, target_count)   

       forward = self.clamp(forward,-max_speed, max_speed)

       print ("PID: Left Encoder %7.2f    Forward: %4.2f     L: %5.2f  R: %5.2f    Target  %6.0f  " %
              (self.get_left_encoder_value(), forward, self._left_duty_cyle.output,
               self._right_duty_cycle.output,  target_count), self.pidController.atSetpoint())
      
       self._left_duty_cyle.output = forward
       self._right_duty_cycle.output = -forward


       self._left_leader.set_control(self._left_duty_cyle)
       self._right_leader.set_control(self._right_duty_cycle)

    def clamp(self, n, min, max):
       if n < min:
           return min
       elif n > max:
           return max
       else:
           return n
# - - - - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  
    def reset_gyro(self)->None:
        self._gyro.reset()

    def get_gyro_heading(self) -> float:
        angle = math.fmod(-self._gyro.getAngle(), 360)

        if angle < 0:
            return angle if angle >= -180 else angle + 360
        else:
            return angle if angle <= 180 else angle - 360
        

    def setGyroPIDcontrollerSetPoint (self, setpoint : float):
       self.targetGyroValue = setpoint

    def getGyroPIDcontrollerStatus (self) -> bool:
       return self.gyro_pidController.atSetpoint()

    def turn_PID(self, max_speed : float) -> None:

       current_gyro_heading = self.get_gyro_heading()
       target_heading = self.targetGyroValue
       turn = self.gyro_pidController.calculate( current_gyro_heading, target_heading)   

       turn = self.clamp(turn,-max_speed, max_speed)

       print ("Turn PID: Current Heading %5.2f    Turn: %4.2f     L: %5.2f  R: %5.2f    Target  %6.0f  " %
              (current_gyro_heading, turn, self._left_duty_cyle.output,
               self._right_duty_cycle.output,  target_heading), self.gyro_pidController.atSetpoint())
      

       self._left_duty_cyle.output = 0 - turn    # Verifed on real hardware   5
       self._right_duty_cycle.output = 0 + turn

       self._left_leader.set_control(self._left_duty_cyle)
       self._right_leader.set_control(self._right_duty_cycle)
