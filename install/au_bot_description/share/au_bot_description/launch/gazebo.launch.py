import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration,PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import AppendEnvironmentVariable, ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from os.path import join

def generate_launch_description():

    # Package Directories
    pkg_path = get_package_share_directory('au_bot_description')

    #Get robot state publisher
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    pkg_path,'launch','display.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # Get the path to your custom world file
    world_file = os.path.join(pkg_path, 'world', 'test.world')

    #Get the path to gazebo parameters
    gazebo_params_file = os.path.join(pkg_path,'config','gazebo_params.yaml')

    # Path to your SLAM Toolbox parameter file
    slam_params_file = os.path.join(pkg_path,
        'config',
        'mapper_params_online_async.yaml'
    )

    #Path to rviz config file
    rviz_config_path = os.path.join(pkg_path,
        "config",
        "drive.rviz",
    )

    twist_mux_params = os.path.join(pkg_path, 'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )
    
    # Start Gazebo Sim
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_file, 'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
    )

    # Spawn Robot in Gazebo   
    spawn = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            "-topic", "/robot_description",
            '-entity', "au_bot",
            "-z", "0.0",
            "-x", "0.0",
            "-y", "0.0",
            "-Y", "0.0"
        ],            
        output='screen',
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    #start rviz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_path],
    )

    # Include SLAM Toolbox online_async_launch.py
    slam_toolbox = Node(
        parameters=[
        slam_params_file],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen'
    )    

    return LaunchDescription(
        [
            rsp,
            twist_mux,
            gazebo,
            spawn,
            diff_drive_spawner,
            joint_broad_spawner,
            slam_toolbox,
            # rviz_node,
        ]
    )
