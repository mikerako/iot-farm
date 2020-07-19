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
<<<<<<< HEAD
    packages=['iot-farm'],
    install_requires=['twilio'],
=======
<<<<<<< HEAD
    install_requires=['twilio', 'python-dotenv', 'sendgrid'],
>>>>>>> 7b61f0db702cfd3841b2c90e69779ad6f4a24d9f
    scripts=[]
=======
    install_requires=['twilio', 'python-dotenv'],
    scripts=[],
    python_requires='>=3.6',
>>>>>>> 927e824774f9b4e5f1951c3f873f1c3646176adb
)
