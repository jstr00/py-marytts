#!/usr/bin/env python

from setuptools import setup, find_packages

EXCLUDED = ['*.tests', '*.tests.*', 'tests.*', 'tests']

setup(name                 ='py-marytts',
      version              ='0.1.1',
      description          ='Python interface for Mary TTS',
      long_description     = open('README.md').read(),
      author               = 'Guenter Bartsch',
      author_email         = 'guenter@zamia.org',
      maintainer           = 'Guenter Bartsch',
      maintainer_email     = 'guenter@zamia.org',
      url                  = 'https://github.com/gooofy/py-marytts',
      classifiers          = [
                              'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
                              'Topic :: Multimedia :: Sound/Audio :: Speech',
                              'Operating System :: POSIX :: Linux',
                              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                              'Programming Language :: Python :: 2',
                              'Programming Language :: Python :: 2.7',
                              'Programming Language :: Python :: 3',
                              'Programming Language :: Python :: 3.4',
                             ],
      platforms            = 'Linux',
      license              = 'LGPLv3',
      package_dir          = {'marytts': 'marytts'},
      test_suite           = 'tests',
      packages             = find_packages('.', EXCLUDED),
      )

