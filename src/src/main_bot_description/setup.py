from setuptools import setup

package_name = 'main_bot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'tf_transformations'],
    zip_safe=True,
    maintainer='r2',
    maintainer_email='robotengineer2@careyu.ai',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'antenna_controller = main_bot_description.antenna_controller:main',
            'lidar_test = main_bot_description.lidar_test:main',
            'line_of_sight_controller = main_bot_description.line_of_sight_controller:main',
        ],
    },
)
