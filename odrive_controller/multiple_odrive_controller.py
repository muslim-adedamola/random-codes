
import argparse
from typing import Dict, Tuple, Any, Union
import odrive
from odrive.enums import *
from odrive.utils import dump_errors
import sys
import time

class Odrive_Arm:
    """
    Wrapper for the two odrive controllers.
    """

    def __init__(self, serial_X: str, serial_YZ: str):
        self.serial_X = serial_X
        self.serial_YZ = serial_YZ
        self.axes = {}  # Initialize axes dictionary
        self._connect_to_odrive()
        self._configure_for_velocity()

    def _configure_for_velocity(self):
        for axis in self.axes.values():
            axis.controller.config.vel_ramp_rate = 3
            axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
            self.odrv_YZ.save_configuration()
            self.odrv_X.save_configuration()

    def _connect_to_odrive(self):
        print("finding YZ odrive...")
        self.odrv_YZ = odrive.find_any(serial_number=self.serial_YZ)
        assert self.odrv_YZ is not None and not isinstance(self.odrv_YZ, list)

        print("finding X odrive...")
        self.odrv_X = odrive.find_any(serial_number=self.serial_X)
        assert self.odrv_X is not None and not isinstance(self.odrv_X, list)

        self.axes = {
            "X": self.odrv_X.axis0,
            "A": self.odrv_X.axis1,
            "Y": self.odrv_YZ.axis1,
            "Z": self.odrv_YZ.axis0
        }
        print("ODrives are connected, dumping previous errors")
        print("YZ Odrive Errors:")
        dump_errors(self.odrv_YZ, True)
        print("X Odrive Errors:")
        dump_errors(self.odrv_X, True)
        print("\n\n")
        for axis_id in self.axes:
            self._set_state(axis_id, AXIS_STATE_CLOSED_LOOP_CONTROL)

    def _check_connected(self):
        assert self.odrv_X is not None and not isinstance(self.odrv_X, list)
        assert self.odrv_YZ is not None and not isinstance(self.odrv_YZ, list)
        assert self.axes is not None

    def move_axis(self, axis_id: str, velocity: float):
        assert axis_id in self.axes
        self.axes[axis_id].controller.input_vel = velocity

    def move(self, vel: Tuple[float, float, float, float]):
        for axis_id, velocity in zip(self.axes.keys(), vel):
            self.move_axis(axis_id, velocity)

    def _set_state(self, axis_id: str, state):
        assert axis_id in self.axes
        axis = self.axes[axis_id]
        axis.requested_state = state
    
    def _hold(self):
        for axis_id in self.axes:
            self._set_state(axis_id, AXIS_STATE_IDLE)

def main():
    parser = argparse.ArgumentParser(description='Odrive Arm Control')
    parser.add_argument('--serial_X', type=str, required=True, help='Serial number for ODrive X')
    parser.add_argument('--serial_YZ', type=str, required=True, help='Serial number for ODrive YZ')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--velocity',
        type=float,
        nargs=4,
        help='Velocities for X, A, Y, Z axes respectively'
    )
    
    group.add_argument(
        '--hold',
        action="store_true",
        help='Determine if motor should be stopped'
    )

    
    args = parser.parse_args()

    arm = Odrive_Arm(args.serial_X, args.serial_YZ)

    if args.velocity:
        arm.move(args.velocity)
    elif args.velocity is not None:
        arm._hold()

if __name__ == "__main__":
    main()
