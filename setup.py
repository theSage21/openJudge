import sys
from setuptools import setup
__version__ = list(map(str, [3, 0, 2]))

if sys.version_info < (3, 5):
    raise Exception('You require Python3.5 or above to run OpenJudge')

setup(name='openjudge',
      version='.'.join(__version__),
      description='LAN Programming Contest Judging Program',
      url='http://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      license='MIT',
      packages=['openjudge'],
      include_package_data=True,
      install_requires=['motor', 'aiohttp',
                        'aiohttp-jinja2', 'aiohttp-cors'],
      entry_points={'console_scripts': ['openjudge=openjudge.cli:main']},
      package_data={'openjudge': ['templates/*', 'staticfiles/*', 'wrappers.json']},
      keywords=['openjudge', 'lan', 'programming', 'programming', 'contest'],
      zip_safe=False)
