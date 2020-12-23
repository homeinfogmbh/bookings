#! /usr/bin/env python3

from setuptools import setup


setup(
    name='bookings',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    install_requires=[
        'configlib',
        'emaillib',
        'functoolsplus',
        'his',
        'mdb',
        'notificationlib',
        'peewee',
        'peeweeplus',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    packages=['bookings'],
    description='HOMEINFO bookings API.'
)
