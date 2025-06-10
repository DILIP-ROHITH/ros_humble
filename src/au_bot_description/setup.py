from setuptools import setup
import os
from glob import glob

package_name = 'au_bot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        # Resource index
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),

        # Install package.xml
        ('share/' + package_name, ['package.xml']),

        # Install launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),

        # Install URDF and Xacro files
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf') + glob('urdf/*.xacro') + glob('urdf/*.trans') + glob('urdf/*.gazebo')  + glob('urdf/*.ros2control')),

        # Install world files
        (os.path.join('share', package_name, 'world'), glob('world/*.world')),

        #Install Mesh files
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),

        # Install RViz and YAML config files
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz') + glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rohith',
    maintainer_email='rohithkarella@gmail.com',
    description='The ' + package_name + ' package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
