#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from setuptools import setup,find_packages,Extension
import os.path
import platform
import numpy
import sys

trees_home = os.environ.get('TREESTB_HOME',None)

if not trees_home:
    raise ImportError, "Please set environment variable TREESTB_HOME to src root of treestoolbox (get it at treestoolbox.org)."



setup(
        name='pytreestb',
        version='0.0.1',
        description = 'A python interface to the trees toolbox',
        long_description= "See http://treestoolbox.org",
        packages = find_packages('src'),
        package_dir={'':'src'},
        classifiers=['Development Status :: 3 - Alpha',
                        'Intended Audience :: End Users/Desktop',
                        'Intended Audience :: Developers',
                        'Intended Audience :: Science/Research',
                        'License :: OSI Approved :: GNU General Public License (GPL)',
                        'Operating System :: POSIX',
                        'Programming Language :: C',
                        'Programming Language :: Python',
                          ],
        test_suite='tests.alltests.test_suite',
        url = 'http://neuralensemble.org/trac/pytreestb',
        zip_safe=False,
        author='Eilif Muller',
        author_email='eilif.mueller@epfl.ch',
        install_requires=['setuptools','numpy','pymatlab'],
        #tests_require=['setuptools'],
)

