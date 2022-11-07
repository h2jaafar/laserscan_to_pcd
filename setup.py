from setuptools import setup
import os
from glob import glob

package_name = 'laserscan_to_pcd'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, "launch"), glob('launch/*.launch.py')),
        # Same with the RViz configuration file.
        (os.path.join('share', package_name, "config"), glob('config/*')),
        # And the ply files.
        (os.path.join('share', package_name, "resource"), glob('resource/*.ply')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hussein',
    maintainer_email='husseinali.jaafar@ryerson.ca',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'scan_subscriber_node = laserscan_to_pcd.scan_subscriber_node:main',
            'pcd_publisher_node = laserscan_to_pcd.pcd_publisher_node:main',
        ],
    },
)
