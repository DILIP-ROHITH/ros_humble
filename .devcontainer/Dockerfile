FROM osrf/ros:humble-desktop-full

# Add ubuntu user with same UID and GID as your host system, if it doesn't already exist
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if ! id -u $USER_UID >/dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME && \
        useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

# Add user to necessary groups and sudo support (do this as root before switching user)
RUN apt-get update && \
    apt-get install -y sudo && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    usermod --append --groups video,dialout,plugdev,tty $USERNAME

# Clean up ALL conflicting keyrings and repository configurations
RUN rm -rf /etc/apt/sources.list.d/ros2* && \
    rm -rf /usr/share/keyrings/ros* && \
    apt-get clean && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and upgrade packages, then install required packages in one layer
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    python3-pip \
    python3-serial \
    python3-rosdep \
    software-properties-common \
    net-tools \
    kmod \
    iproute2 \
    git \
    ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control \
    ros-humble-teleop-twist-keyboard \
    ros-humble-slam-toolbox \
    ros-humble-ros2-control ros-humble-ros2-controllers \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-joint-state-publisher-gui \
    ros-humble-twist-mux && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Initialize and update rosdep (as root)
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then \
        rosdep init; \
    fi && \
    rosdep update

# Switch to user
USER $USERNAME

# Source the ROS setup file for the user
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# Update rosdep for the user (optional, but recommended)
RUN rosdep update

################################
## ADD ANY CUSTOM SETUP BELOW ##
################################