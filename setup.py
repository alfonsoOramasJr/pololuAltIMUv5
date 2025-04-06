from setuptools import setup, find_packages

setup(name='pololuAltIMUv5',
      version='0.1',
      packages=find_packages(),
      install_requires=[
          'AHRS>=0.3.1'
      ]
      )
