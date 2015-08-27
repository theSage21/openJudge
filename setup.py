from setuptools import setup
import openjudge

version = '.'.join(map(str, openjudge.__version__))
long_desc = '''
Openjudge is a LAN based programming judge implementation in Python3.

Features

    - Multi language support(Py2, Py3, C, C++, Java)
    - Scalable
    - Interface independent
    - New languages can be added as and when required
    - Complete control via interface, ie. Django admin for default interface
    - Logging
    - Tracebacks
    - Timeouts


The default interface is available at --http://theSage21.github.io/judge-interface/
'''

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
