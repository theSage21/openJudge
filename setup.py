from setuptools import setup
import openjudge

version = openjudge.__version__

setup(name='openjudge',
      version=version,
      description='LAN programming judge',
      url='https://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='Arjoonn Sharma',
      license='MIT',
      packages=['openjudge'],
      zip_safe=False,
      )
