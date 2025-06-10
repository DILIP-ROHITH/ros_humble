#!/bin/bash

# NVIDIA Container Toolkit Installation - Modern Approach
# Run these commands in your local terminal before opening folder in container

# Step 1: Clean up any existing conflicting configurations (optional, but recommended)
sudo rm -f /etc/apt/sources.list.d/nvidia-docker.list
sudo rm -f /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo rm -f /etc/apt/sources.list.d/libnvidia-container.list

# Step 2: Get distribution information
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)

# Step 3: Add NVIDIA GPG key (modern method)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# Step 4: Add NVIDIA repository with proper signed-by configuration
echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container \$(ARCH)/" | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Step 5: Update package list
sudo apt-get update

# Step 6: Install NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# Step 7: Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker

# Step 8: Restart Docker service
sudo systemctl restart docker


# Clone the repository to your local system

# Build workspace
colcon build

# Source the workspace
source install/setup.bash

# To launch the robot in simulation 
ros2 launch au_bot_description gazebo.launch.py

>>> To launch the robot in new environment create a new world in gazebo and save the world file in "world" folder and chagne the file name in Gazebo launch file
>>> To map the environment change the mode from localization to mapping in mapper_params_online_async.yaml file and save the map using slamtool box plugin

# For Autonomous Navigation
ros2 launch au_bot_description navigation.launch.py 

# To launch the robot in realworld
ros2 launch au_bot_description launch_robot.launch.py 

>> for navigation in real world launch the following file as well
ros2 launch au_bot_description online_async_launch.py