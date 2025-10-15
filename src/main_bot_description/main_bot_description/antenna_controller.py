#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory

class AntennaController(Node):

    def __init__(self):
        super().__init__('antenna_controller')
        # This node now simply provides the service for the line_of_sight_controller
        # to publish joint trajectory commands to.
        # The publisher is defined in the line_of_sight_controller.
        # This script is kept to satisfy the launch file dependency, but the core logic
        # has been moved.
        self.get_logger().info('AntennaController node started, ready to receive trajectory commands.')


def main(args=None):
    rclpy.init(args=args)
    antenna_controller = AntennaController()
    rclpy.spin(antenna_controller)
    antenna_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()