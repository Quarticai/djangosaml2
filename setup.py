import codecs
import os
from setuptools import setup, find_packages


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames), encoding='utf-8').read()

__version__ = None
exec(open('djangosaml2/_version.py', 'r').read())

setup(
    name='djangosaml2',
    version=__version__,
    description='pysaml2 integration for Django',
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        ],
    keywords="django,pysaml2,sso,saml2,federated authentication,authentication",
    url="https://github.com/Quarticai/djangosaml2",
    download_url="https://pypi.org/project/djangosaml2/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'defusedxml>=0.4.1',
        'pysaml2>=5.3.0',
        ],
    tests_require=[
        # Provides assert_called_once.
        'mock',
    ]
    )
