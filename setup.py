#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


ROOT_PACKAGE = 'django-domains'
DIR = os.path.dirname(__file__)
VERSION = '0.5.1'


def long_description():
    """
    Returns package long description from README
    """
    def read(what):
        with open(os.path.join(DIR, '%s.rst' % what)) as fp:
            return fp.read()

    return "{README}\n\n{CHANGELOG}".format(README=read('README'),
                                            CHANGELOG=read('CHANGELOG'))


def version():
    """
    Returns package version for package building
    """
    return VERSION


if __name__ == '__main__':
    setup(name=ROOT_PACKAGE,
          description=('An application that allows you to run many '
                       'different sites on one Django instance'),
          author='Mikhail Porokhovnichenko',
          author_email='marazmiki@gmail.com',
          version=version(),
          long_description=long_description(),
          packages=find_packages(),
          include_package_data=True,
          test_suite='tests.main',
          zip_safe=False,
          classifiers=[
              'Environment :: Web Environment',
              'Programming Language :: Python',
              'Framework :: Django'
          ])
