from setuptools import setup

with open('README', 'r') as f:
    long_description = f.read()

setup(
    name='iot-farm',
    version='1.0',
    description='Small farming project that relies on feedback from sensors to control parameters for optimal plant growth.',
    license='MIT',
    author='Kevin Kraydich',
    author_email='kevin.kraydich@gmail.com',
    packages=['iot-farm'],
    install_requires=['twilio'],
    scripts=[]
)
