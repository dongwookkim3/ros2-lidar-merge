from setuptools import find_packages, setup

package_name = 'lidar_merge_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dongwook',
    maintainer_email='dongwook.3.kim@gmail.com',
    description='Merge two LIDARs mounted at front and back',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'merge_node = lidar_merge_pkg.merge_node:main',  # 여기 꼭 추가
        ],
    },
)
