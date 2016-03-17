from setuptools import setup

setup(
    name = 'BiteBack',
    version = '0.1.0',
    description = 'The MONROE node watchdog',
    author = 'Thomas Hirsch',
    author_email = 'thomas.hirsch@celerway.com',
    url = '',
    license = 'All rights reserved',
    packages = ['biteback', 'biteback.modules'],
    entry_points = {'console_scripts': [
        'biteback    = biteback.biteback:main',
    ], },
    data_files = [
    ],
    install_requires = [
    ]
)
