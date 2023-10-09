from setuptools import setup, find_packages

setup(
    name='simple_alarm',
    version='0.1.0',
    description='Simple alarm application',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    install_requires=[
        # List of dependencies
        'paho-mqtt==1.6.1',
        'pyttsx3==2.90'
    ]
)
