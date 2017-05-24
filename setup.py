import sys
from setuptools import setup
from openjudge import __version__
__version__ = list(map(str, __version__))

if sys.version_info < (3, 5):
    raise Exception('You require Python3.5 or above to run OpenJudge')

setup(name='openjudge',
      version='.'.join(__version__),
      description='Programming contest Judging Program',
      url='http://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      license='MIT',
      packages=['openjudge'],
      include_package_data=True,
      install_requires=['bottle', 'bottle-cork'],
      entry_points={'console_scripts': ['openjudge=openjudge.cli:main']},
      package_data={'openjudge': ['templates/*', 'static/*']},
      zip_safe=False)
