from setuptools import setup
import openjudge

version = '.'.join(map(str, openjudge.__version__))
long_desc = '''A Programming Judge for LAN based competitions.
Can also function as a Judge for internet based competitions.
Requires a pluggable interface to work.'''

setup(name='openjudge',
      version=version,
      description='LAN programming judge',
      long_description=long_desc,
      url='https://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='Arjoonn Sharma',
      license='MIT',
      packages=['openjudge'],
      zip_safe=False,
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.4',
                   ],
      keywords='judge programming check proof openjudge'.split(' ')
      )
