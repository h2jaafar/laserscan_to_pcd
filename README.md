# LaserScan to PointCloud
This is an implementation of a simple LaserScan to 2D PointCloud conversion. 

```
cd ~/dev_ws/src
git clone https://github.com/husseinalijaafar/laserscan-to-pcd
cd ..
colcon build
```
In a new window
```
source ~/dev_ws/install/setup.bash
ros2 launch laserscan_to_pcd laserscan_to_pointcloud.launch.py
```

Make sure the `ROS_DOMAIN_ID` of the turtlebot and computer are the same. 
