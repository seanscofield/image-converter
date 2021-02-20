from setuptools import setup, find_packages

setup(
    name='image-converter',
    version='0.0.1',

    description='application that converts png images to jpeg format',

    packages=find_packages(exclude=['test*']),
    install_requires=[
        'boto3',
        'pillow'
    ],

    entry_points={
        'console_scripts': [
            'image_converter = src.application:main'
        ]
    }
)
