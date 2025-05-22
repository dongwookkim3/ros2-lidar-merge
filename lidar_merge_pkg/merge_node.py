import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class LidarMerger(Node):
    def __init__(self):
        super().__init__('lidar_merger')

        self.scan1 = None
        self.scan2 = None

        self.subscription1 = self.create_subscription(
            LaserScan,
            '/rplidar1/scan',
            self.scan1_callback,
            10)
        self.subscription2 = self.create_subscription(
            LaserScan,
            '/rplidar2/scan',
            self.scan2_callback,
            10)

        self.publisher = self.create_publisher(LaserScan, '/scan_merged', 10)

    def scan1_callback(self, msg):
        self.scan1 = msg
        self.try_publish()

    def scan2_callback(self, msg):
        self.scan2 = msg
        self.try_publish()

    def try_publish(self):
        if self.scan1 is None or self.scan2 is None:
            return

        merged_scan = LaserScan()
        merged_scan.header.stamp = self.get_clock().now().to_msg()
        merged_scan.header.frame_id = self.scan1.header.frame_id

        # 라이다 기본 설정 복사
        merged_scan.angle_min = self.scan1.angle_min
        merged_scan.angle_max = self.scan1.angle_max
        merged_scan.angle_increment = self.scan1.angle_increment
        merged_scan.time_increment = self.scan1.time_increment
        merged_scan.scan_time = self.scan1.scan_time
        merged_scan.range_min = self.scan1.range_min
        merged_scan.range_max = self.scan1.range_max

        # 뒤 라이다 데이터 180도 뒤집기
        reversed_ranges = list(reversed(self.scan2.ranges))

        merged_ranges = []
        for r1, r2 in zip(self.scan1.ranges, reversed_ranges):
            if math.isinf(r1) and math.isinf(r2):
                merged_ranges.append(float('inf'))
            elif math.isinf(r1):
                merged_ranges.append(r2)
            elif math.isinf(r2):
                merged_ranges.append(r1)
            else:
                merged_ranges.append(min(r1, r2))

        merged_scan.ranges = merged_ranges
        self.publisher.publish(merged_scan)

def main(args=None):
    rclpy.init(args=args)
    node = LidarMerger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
