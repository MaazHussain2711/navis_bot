import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    #INCLUDE THE robot_state_publisher LAUNCH FILE AND FORCE SIM TIME TO BE ENABLED
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name = 'navis_bot'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                    )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    #INCLUDE THE GAZEBO LAUNCH FILE, PROVIDED BY THE gazebo_ros PACKAGE
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )
    
    # RUN THE SPAWNER NODE FOR THE gazebo_ros PACKAGE. THE ENTITY NAME DOES NOT MATTER.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'navis_bot'],
                        output='screen')
    
    #LAUNCH THEM ALL!

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])
