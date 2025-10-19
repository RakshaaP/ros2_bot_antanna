import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

class AntennaController(Node):

    def __init__(self):
        super().__init__('antenna_controller')
        self.subscription = self.create_subscription(
            LaserScan,
            '/demo/scan',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(JointTrajectory, '/antenna_controller/joint_trajectory', 10)

    def listener_callback(self, msg):
        # We are interested in the 90 degree arc in front of the robot.
        # The lidar scans from -90 to +90 degrees, so we take the middle 180 samples.
        front_arc = msg.ranges[90:270]

        # Check if there are any obstacles in the front arc.
        # We filter out any 'inf' values.
        valid_ranges = [r for r in front_arc if r > 0.1 and r < 1.0] # Look for obstacles within 1 meter

        if not valid_ranges:
            # No obstacles, move to default position (0.0)
            self.move_antenna(0.0)
            self.get_logger().info('No obstacles, moving to default position.')
            return

        # For simplicity, we'll just react to the closest obstacle.
        # A more advanced approach would be to calculate the actual height needed.
        closest_obstacle = min(valid_ranges)
        self.get_logger().info(f'Closest obstacle at: {closest_obstacle:.2f}m')

        # Simple proportional control: the closer the obstacle, the higher the antenna.
        # This is a placeholder for a more sophisticated height calculation.
        # If obstacle is at 1m, height is 0. If at 0.1m, height is 0.5.
        desired_height = 0.5 * (1.0 - (closest_obstacle - 0.1) / 0.9)
        desired_height = max(0.0, min(0.5, desired_height)) # Clamp between 0.0 and 0.5

        self.move_antenna(desired_height)
        self.get_logger().info(f'Obstacle detected, moving antenna to {desired_height:.2f}m.')

    def move_antenna(self, position):
        traj = JointTrajectory()
        traj.joint_names = ['antenna_joint']
        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start.sec = 1
        traj.points.append(point)
        self.publisher_.publish(traj)


def main(args=None):
    rclpy.init(args=args)

    antenna_controller = AntennaController()

    rclpy.spin(antenna_controller)

    antenna_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
