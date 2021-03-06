import os
from setuptools import setup, find_packages
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        install_requires = f.read().splitlines()
setup(name="stocks_app",
      author="Jeremy Hitt",
      version=0.1,
      description='Gets data about stocks and visualizes them',
      url='https://github.com/jlhitt1993/stocks_app',
      install_requires=install_requires,
      packages=find_packages()
      )
