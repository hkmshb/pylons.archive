import os
from setuptools import setup, find_packages



## META
__version__ = '0.0'
__description__ = 'Pylons'
__long_description__ = \
'''Pylons is a web-based Electric Utility Information Management System for
maintaining a comprehensive database of the entire principal electric facilities,
devices and equipment, powerlines and assets within an Electric utility network.
'''

requires = [
    'cornice',
    'elixr2[utils]',
    'plaster_pastedeploy',
    'pyramid >= 1.9.1',
    'pyramid_jinja2',
    'pyramid_jwt',
    'pyramid_multiauth',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

dev_require = [
    'pyramid_debugtoolbar',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='pylons',
    version=__version__,
    description=__description__,
    long_description=__long_description__,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Abdul-Hakeem Shaibu',
    author_email='s.abdulhakeem@hotmail.com',
    url='https://bitbucket.org/hazeltek-dev/pylons.git',
    keywords='web pylons electric utility facilities assets equipment IMS',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'dev': dev_require,
        'test': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = pylons:main',
        ],
        'console_scripts': [
        ],
    },
)
