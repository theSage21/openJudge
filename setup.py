from setuptools import setup
from openjudge import __version__
__version__ = list(map(str, __version__))
setup(name='openjudge',
      version='.'.join(__version__),
      description='Programming contest Judging Program',
      url='http://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      license='MIT',
      packages=['openjudge'],
      include_package_data=True,
      install_requires=['bottle'],
      entry_points={'console_scripts': ['openjudge=openjudge.cli:main']},
      package_data={'openjudge': ['templates/*', 'static/*']},
      zip_safe=False)
