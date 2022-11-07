import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from std_msgs.msg import String
import std_msgs.msg as std_msgs
import sensor_msgs.msg as sensor_msgs
import numpy as np

import laser_geometry as lg
# not importing properlly
#http://wiki.ros.org/laser_pipeline/Tutorials/IntroductionToWorkingWithLaserScannerData
import math


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        qos_sensor = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1
        )
        self.get_logger().info('Use QoS Sensor')
        self.subscription = self.create_subscription(
            sensor_msgs.LaserScan,
            'scan',
            self.listener_callback,
            qos_profile=qos_sensor)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(sensor_msgs.PointCloud2, 'cloud', qos_sensor)
        timer_period = 1/30.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def listener_callback(self, msg):
        
        self.get_logger().info('Lidar Min angle: "%d"' % msg.angle_min)
        self.ranges = msg.ranges
        self.header = msg.header
        self.scan_time = msg.scan_time
        self.angle_increment = msg.angle_increment
        self.angle_min = msg.angle_min
        self.angle_max = msg.angle_max

        self.pc2_msg = lp.projectLaser(msg)
    
    def timer_callback(self):
            # Here I use the point_cloud() function to convert the numpy array 
            # into a sensor_msgs.PointCloud2 object. The second argument is the 
            # name of the frame the point cloud will be represented in. The default
            # (fixed) frame in RViz is called 'map'
            # self.pcd = self.point_cloud(self.points, 'map')
            # Then I publish the PointCloud2 object 
            self.publisher_s.publish(self.pc2_msg)

    def point_cloud(points, parent_frame):
        ros_dtype = sensor_msgs.PointField.FLOAT32
        dtype = np.float32
        itemsize = np.dtype(dtype).itemsize # A 32-bit float takes 4 bytes.

        data = points.astype(dtype).tobytes() 

        # The fields specify what the bytes represents. The first 4 bytes 
        # represents the x-coordinate, the next 4 the y-coordinate, etc.
        fields = [sensor_msgs.PointField(
            name=n, offset=i*itemsize, datatype=ros_dtype, count=1)
            for i, n in enumerate('xyz')]

        # The PointCloud2 message also has a header which specifies which 
        # coordinate frame it is represented in. 
        header = std_msgs.Header(frame_id=parent_frame)

        return sensor_msgs.PointCloud2(
            header=header,
            height=1, 
            width=points.shape[0],
            is_dense=False,
            is_bigendian=False,
            fields=fields,
            point_step=(itemsize * 3), # Every point consists of three float32s.
            row_step=(itemsize * 3 * points.shape[0]), 
            data=data
        )


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()