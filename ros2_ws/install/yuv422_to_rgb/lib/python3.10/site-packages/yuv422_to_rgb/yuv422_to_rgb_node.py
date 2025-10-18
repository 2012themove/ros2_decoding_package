#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class YUV422ToRGBNode(Node):
    def __init__(self):
        super().__init__('yuv422_to_rgb_node')

        self.bridge = CvBridge()

        # Subscribe to input YUV422 topic
        self.subscription = self.create_subscription(
            Image,
            '/hires_small_color',
            self.image_callback,
            10
        )

        # Publisher for RGB topic
        self.publisher = self.create_publisher(Image, '/hires_small_color_rgb', 10)

        self.get_logger().info("✅ YUV422 → RGB8 converter node started (ROS 2 Humble)")

    def image_callback(self, msg):
        try:
            # Convert incoming YUV422 image to OpenCV image
            frame_yuv = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

            # Convert YUV422 to RGB8
            frame_rgb = cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2RGB_UYVY)

            # Convert back to ROS 2 Image
            rgb_msg = self.bridge.cv2_to_imgmsg(frame_rgb, encoding='rgb8')
            rgb_msg.header = msg.header  # preserve timestamp and frame_id

            # Publish
            self.publisher.publish(rgb_msg)
        except Exception as e:
            self.get_logger().error(f"❌ Failed to convert image: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = YUV422ToRGBNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
