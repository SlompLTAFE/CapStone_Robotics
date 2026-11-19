from setuptools import setup

package_name = "xarm_ros2_node"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Lucas Slomp",
    maintainer_email="20069199@tafe.wa.edu.au",
    description="ROS 2 integration for xarm_toolkit",
    license="MIT",
    entry_points={
        "console_scripts": [
            "click_publisher = xarm_ros2_node.click_publisher:main",
            "xarm_node = xarm_ros2_node.xarm_node:main",
            "simulator_node = xarm_ros2_node.simulator_node:main",
        ],
    },
)

