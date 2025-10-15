#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
import math

class LineOfSightController(Node):
    def __init__(self):
        super().__init__('line_of_sight_controller')

        # Constants
        self.tower_position = (0.0, 0.0, 5.0) # X, Y, Z of the tower's sensor
        self.antenna_raised_position = 0.5
        self.antenna_lowered_position = 0.0

        # State variables
        self.robot_position = None
        self.robot_orientation = None
        self.antenna_is_raised = False
        self.signal_lost = False

        # Subscribers
        self.tower_scan_sub = self.create_subscription(
            LaserScan, '/tower/scan', self.tower_scan_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

        # Publisher to control the antenna
        self.antenna_pub = self.create_publisher(
            JointTrajectory, '/antenna_controller/joint_trajectory', 10)

    def odom_callback(self, msg):
        self.robot_position = msg.pose.pose.position
        self.robot_orientation = msg.pose.pose.orientation

    def tower_scan_callback(self, msg):
        if self.robot_position is None:
            return

        # Calculate direct distance and angle from tower to robot
        dx = self.robot_position.x - self.tower_position[0]
        dy = self.robot_position.y - self.tower_position[1]
        distance_to_robot = math.sqrt(dx**2 + dy**2)
        angle_to_robot = math.atan2(dy, dx)

        # Find the specific ray from the tower's scan that points to the robot
        angle_increment = msg.angle_increment
        start_angle = msg.angle_min
        ray_index = int((angle_to_robot - start_angle) / angle_increment)

        if 0 <= ray_index < len(msg.ranges):
            distance_from_tower_ray = msg.ranges[ray_index]

            # Check for Line of Sight
            # Add a small buffer to account for float inaccuracies
            if distance_from_tower_ray < distance_to_robot - 0.1:
                # Signal is blocked
                if not self.signal_lost:
                    self.get_logger().info('SIGNAL LOST! Obstacle detected. Raising antenna.')
                    self.move_antenna(self.antenna_raised_position)
                    self.signal_lost = True
                    self.antenna_is_raised = True
            else:
                # Signal is clear
                if self.signal_lost:
                    self.get_logger().info('SIGNAL RE-ACQUIRED at new height.')
                    # Optional: Add logic to lower antenna if original path is clear
                self.signal_lost = False
                # Simple logic to lower antenna if it's raised and path is clear
                if self.antenna_is_raised:
                     self.get_logger().info('Path is clear, lowering antenna.')
                     self.move_antenna(self.antenna_lowered_position)
                     self.antenna_is_raised = False

    def move_antenna(self, position):
        traj = JointTrajectory()
        traj.joint_names = ['antenna_joint']
        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start.sec = 1
        traj.points.append(point)
        self.antenna_pub.publish(traj)

def main(args=None):
    rclpy.init(args=args)
    controller = LineOfSightController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
