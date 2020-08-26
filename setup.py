'''
IoT Farm Python package configuration.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='iot-farm',
    version='1.0',
    description='Small farming project that relies on feedback from sensors to control parameters for optimal plant growth.',
    license='MIT',
    author='Kevin Kraydich',
    author_email='kevin.kraydich@gmail.com',
    install_requires=[
        'twilio',
        'python-dotenv',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'pydrive',
        'Flask'
    ],
    scripts=[],
    python_requires='>=3.6',
)
