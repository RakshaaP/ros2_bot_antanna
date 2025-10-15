#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarTest(Node):

    def __init__(self):
        super().__init__('lidar_test')
        self.subscription = self.create_subscription(
            LaserScan,
            '/gazebo_ros_lidar_controller/out',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info(f"Received lidar scan with {len(msg.ranges)} range values.")
        # Print the first 10 range values to avoid flooding the console
        self.get_logger().info(f"First 10 ranges: {msg.ranges[:10]}")

def main(args=None):
    rclpy.init(args=args)
    lidar_test = LidarTest()
    rclpy.spin(lidar_test)
    lidar_test.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
