#adapted and modified from https://github.com/AustinOwens/odrive_config/
# to run: python motor_control_velocity.py --axis_num [0 or 1] --velocity [int value] or
# for idle mode, python motor_control_velocity.py --axis_num [0 or 1] --idle_mode


#!/usr/bin/env python3

import argparse
import sys
import time
import os.path

import odrive
from odrive.enums import *


class MotorConfig:
    """
    Class for configuring an Odrive axis for a motor.
    Only works with one Odrive at a time.
    """

    # Motor Kv
    MOTOR_KV = 700

    # Min/Max phase inductance of motor
    MIN_PHASE_INDUCTANCE = 0
    MAX_PHASE_INDUCTANCE = 0.001

    # Min/Max phase resistance of motor
    MIN_PHASE_RESISTANCE = 0
    MAX_PHASE_RESISTANCE = 0.5

    # Tolerance for encoder offset float
    ENCODER_OFFSET_FLOAT_TOLERANCE = 0.05

    CALIBRATION_FILE = "calibration_done.flag"

    def __init__(self, axis_num, erase_config):
        """
        Initalizes HBMotorConfig class by finding odrive, erase its
        configuration, and grabbing specified axis object.

        :param axis_num: Which channel/motor on the odrive your referring to.
        :type axis_num: int (0 or 1)
        :param erase_config: Erase existing config before setting new config.
        :type erase_config: bool (True or False)
        """

        self.axis_num = axis_num

        self.erase_config = erase_config

        # Connect to Odrive
        print("Looking for ODrive...")
        self._find_odrive()
        print("Found ODrive.")

        #check if calibration has been done previously
        self.calibration_done = os.path.isfile(self.CALIBRATION_FILE)

    def _find_odrive(self):
        # connect to Odrive
        self.odrv = odrive.find_any()
        self.odrv_axis = getattr(self.odrv, "axis{}".format(self.axis_num))

    def configure(self, control_mode):
        #if calibration has not been previously done
        if not self.calibration_done:
                    """
                    Configures the odrive device for a motor.
                    """

                    if self.erase_config:
                        # Erase pre-exsisting configuration
                        print("Erasing pre-exsisting configuration...")
                        try:
                            self.odrv.erase_configuration()
                        except Exception:
                            pass

                    self._find_odrive()

                    # Set this to True if using a brake resistor
                    self.odrv.config.enable_brake_resistor = True


                    self.odrv_axis.motor.config.pole_pairs = 7


                    self.odrv_axis.motor.config.resistance_calib_max_voltage = 2
                    self.odrv_axis.motor.config.requested_current_range = 20
                    self.odrv_axis.motor.config.current_control_bandwidth = 100

                    self.odrv_axis.motor.config.torque_constant = 8.27 / self.MOTOR_KV

        
                    self.odrv_axis.encoder.config.mode = ENCODER_MODE_INCREMENTAL

        
                    self.odrv_axis.encoder.config.cpr = 2000

                    self.odrv_axis.encoder.config.bandwidth = 3000
                    self.odrv_axis.controller.config.vel_limit = 50
                    self.odrv_axis.controller.config.vel_gain = 0.02
                    self.odrv_axis.controller.config.vel_integrator_gain = 0.2
                    if control_mode == "velocity":
                        self.odrv_axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                        self.odrv_axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
                        self.odrv_axis.controller.config.vel_ramp_rate = 3
                    elif control_mode == "position":
                        self.odrv_axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
                        self.odrv_axis.controller.config.pos_gain = 30
                        self.odrv_axis.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
                        self.odrv_axis.trap_traj.config.vel_limit = 30
                        self.odrv_axis.trap_traj.config.accel_limit = 5
                        self.odrv_axis.trap_traj.config.decel_limit = 5                    

                    # Motors must be in IDLE mode before saving
                    self.odrv_axis.requested_state = AXIS_STATE_IDLE
                    try:
                        print("Saving manual configuration and rebooting...")
                        is_saved = self.odrv.save_configuration()
                        if not is_saved:
                            print("Error: Configuration not saved. Are all motors in IDLE state?")
                        else:
                            print("Calibration configuration saved.")

                        print("Manual configuration saved.")
                    except Exception as e:
                        pass

                    self._find_odrive()

                    input("Make sure the motor is free to move, then press enter...")

                    print("Calibrating Odrive for hoverboard motor (you should hear a " "beep)...")

                    self.odrv_axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION

                    # Wait for calibration to take place
                    time.sleep(10)

                    if self.odrv_axis.motor.error != 0:
                        print(
                            "Error: Odrive reported an error of {} while in the state "
                            "AXIS_STATE_MOTOR_CALIBRATION. Printing out Odrive motor data for "
                            "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
                        )

                        sys.exit(1)

                    if (
                        self.odrv_axis.motor.config.phase_inductance <= self.MIN_PHASE_INDUCTANCE
                        or self.odrv_axis.motor.config.phase_inductance >= self.MAX_PHASE_INDUCTANCE
                    ):
                        print(
                            "Error: After odrive motor calibration, the phase inductance "
                            "is at {}, which is outside of the expected range. Either widen the "
                            "boundaries of MIN_PHASE_INDUCTANCE and MAX_PHASE_INDUCTANCE (which "
                            "is between {} and {} respectively) or debug/fix your setup. Printing "
                            "out Odrive motor data for debug:\n{}".format(
                                self.odrv_axis.motor.config.phase_inductance,
                                self.MIN_PHASE_INDUCTANCE,
                                self.MAX_PHASE_INDUCTANCE,
                                self.odrv_axis.motor,
                            )
                        )

                        sys.exit(1)

                    if (
                        self.odrv_axis.motor.config.phase_resistance <= self.MIN_PHASE_RESISTANCE
                        or self.odrv_axis.motor.config.phase_resistance >= self.MAX_PHASE_RESISTANCE
                    ):
                        print(
                            "Error: After odrive motor calibration, the phase resistance "
                            "is at {}, which is outside of the expected range. Either raise the "
                            "MAX_PHASE_RESISTANCE (which is between {} and {} respectively) or "
                            "debug/fix your setup. Printing out Odrive motor data for "
                            "debug:\n{}".format(
                                self.odrv_axis.motor.config.phase_resistance,
                                self.MIN_PHASE_RESISTANCE,
                                self.MAX_PHASE_RESISTANCE,
                                self.odrv_axis.motor,
                            )
                        )

                        sys.exit(1)

                    # If all looks good, then lets tell ODrive that saving this calibration
                    # to persistent memory is OK
                    self.odrv_axis.motor.config.pre_calibrated = True

                    print("Calibrating Odrive for incremental encoder...")
                    self.odrv_axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION

                    # Wait for calibration to odrv0.axis1.controller.input_pos = 50o take place
                    time.sleep(15)

                    if self.odrv_axis.encoder.error != 0:
                        print(
                            "Error: Odrive reported an error of {} while in the state "
                            "AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION. Printing out Odrive encoder "
                            "data for debug:\n{}".format(
                                self.odrv_axis.encoder.error, self.odrv_axis.encoder
                            )
                        )

                        sys.exit(1)

                    print("Calibrating Odrive for encoder offset...")
                    self.odrv_axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
                    self.odrv_axis.config.startup_encoder_offset_calibration = True

                    
                    time.sleep(30)

                    if self.odrv_axis.encoder.error != 0:
                        print(
                            "Error: Odrive reported an error of {} while in the state "
                            "AXIS_STATE_ENCODER_OFFSET_CALIBRATION. Printing out Odrive encoder "
                            "data for debug:\n{}".format(
                                self.odrv_axis.encoder.error, self.odrv_axis.encoder
                            )
                        )

                        sys.exit(1)

                    # If all looks good, then lets tell ODrive that saving this calibration
                    # to persistent memory is OK
                    self.odrv_axis.encoder.config.pre_calibrated = True

                    if self.odrv_axis.controller.error != 0:
                        print(
                            "Error: Odrive reported an error of {} while performing "
                            "start_anticogging_calibration(). Printing out Odrive controller "
                            "data for debug:\n{}".format(
                                self.odrv_axis.controller.error, self.odrv_axis.controller
                            )
                        )

                        sys.exit(1)

                    # Motors must be in IDLE mode before saving
                    self.odrv_axis.requested_state = AXIS_STATE_IDLE
                    try:
                        print("Saving calibration configuration and rebooting...")

                        self.odrv.save_configuration()
           
                        if not is_saved:
                            print("Error: Configuration not saved. Are all motors in IDLE state?")
                        else:
                            print("Calibration configuration saved.")
                    except Exception as e:
                        pass
                    
                    self._find_odrive()

                    print("Odrive configuration finished.")
                    with open(self.CALIBRATION_FILE, "w") as f:
                        f.write("Calibration done")
                    
            


    def mode_idle(self):
        """
        Puts the motor in idle (i.e. can move freely).
        """

        self.odrv_axis.requested_state = AXIS_STATE_IDLE

    def mode_close_loop_control(self):
        """
        Puts the motor in closed loop control.
        """

        self.odrv_axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def move_input_pos(self, position):
        """
        Puts the motor at a certain angle.
        :param angle: Angle you want the motor to move.
        :type angle: int or float
        """
        if not self.calibration_done:
            print("Calibration has not been done. Run Configuration first")
            return
        
        self.mode_close_loop_control()
        self.odrv_axis.controller.input_pos = position
    
    def move_velocity_control(self, velocity):
        """
        Runs motor at the set velocity
        : param velocity; Velocity you want to set motor to
        : type velocity: int or float
        """

        if not self.calibration_done:
            print("Calibration has not been done. Run Configuration first")
            return
        
        
        self.odrv_axis.controller.input_vel = velocity
        self.mode_close_loop_control()
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Calibration and Running")

    # Argument for axis_num
    parser.add_argument(
        "--axis_num",
        type=int,
        choices=[0, 1],  # Only allow 0 or 1
        required=True,
        help="Motor axis number which can only be 0 or 1.",
    )

    # Argument for erase_config
    parser.add_argument(
        "--erase_config",
        action="store_true",  # If present, set to True. If absent, set to False.
        help="Flag to determine if the config should be erased.",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--position",
        type=float,  # number of position in float.
        help="Number of positions/rotations of motor",
    )

    group.add_argument(
        "--velocity",
        type = float,
        help = "Number of turns per seconds of motor"
    )

    group.add_argument(
        "--idle_mode",
        action = "store_true",
        help="Flag to determine if the config should be erased.",
    )

    args = parser.parse_args()

    motor_config = MotorConfig(
        axis_num=args.axis_num, erase_config=args.erase_config
    )

    if args.idle_mode:
        motor_config.mode_idle()
    elif args.position is not None:
        motor_config.configure("position")
        motor_config.move_input_pos(args.position)
    elif args.velocity is not None:
        motor_config.configure("velocity")
        motor_config.move_velocity_control(args.velocity)

