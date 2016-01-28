#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# To generate DEB package from Python Package:
# sudo pip3 install stdeb
# python3 setup.py --verbose --command-packages=stdeb.command bdist_deb
#
#
# To generate RPM package from Python Package:
# sudo apt-get install rpm
# python3 setup.py bdist_rpm --verbose --fix-python --binary-only
#
#
# To generate EXE MS Windows from Python Package (from MS Windows only):
# python3 setup.py bdist_wininst --verbose
#
#
# To generate PKGBUILD ArchLinux from Python Package (from PyPI only):
# sudo pip3 install git+https://github.com/bluepeppers/pip2arch.git
# pip2arch.py PackageNameHere
#
#
# To Upload to PyPI by executing:
# python3 setup.py register
# python3 setup.py bdist_egg sdist --formats=bztar,gztar,zip upload --sign


"""Setup.py for Python, as Generic as possible."""


import logging as log
import os
import re

from setuptools import setup

from unicodemoticon import (__author__, __url__, __email__, __license__,
                            __version__)
from unicodemoticon.utils import (make_logger,
                                  make_root_check_and_encoding_debug,
                                  set_process_name_and_cpu_priority)

##############################################################################
# EDIT HERE


DESCRIPTION = ("Like a Color Picker but for Unicode Emoticons. "
               "Trayicon with Unicode Emoticons using Python3 Qt5.")
REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), "requirements.txt")


##############################################################################
# Dont touch below


def parse_requirements(path=REQUIREMENTS_FILE):
    """Rudimentary parser for the requirements.txt file.

    We just want to separate regular packages from links to pass them to the
    'install_requires' and 'dependency_links' params of the 'setup()'.
    """
    log.debug("Parsing Requirements from file {what}.".format(what=path))
    pkgs, links = ["pip"], []
    if not os.path.isfile(path):
        return pkgs, links
    try:
        requirements = map(str.strip, path.splitlines())
    except Exception as reason:
        log.warning(reason)
        return pkgs, links
    for req in requirements:
        if not req:
            continue
        if 'http://' in req.lower() or 'https://' in req.lower():
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{package}=={ver}'.format(package=name, ver=version))
        else:
            pkgs.append(req)
    log.debug("Requirements found: {what}.".format(what=(pkgs, links)))
    return pkgs, links


make_logger()
make_root_check_and_encoding_debug()
set_process_name_and_cpu_priority("setup_py")
install_requires_list, dependency_links_list = parse_requirements()
log.info("Starting build of setuptools.setup().")


##############################################################################
# EDIT HERE


setup(

    name="unicodemoticon",
    version=__version__,

    description=DESCRIPTION,
    long_description=DESCRIPTION,

    url=__url__,
    license=__license__,

    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,

    include_package_data=True,
    zip_safe=True,

    extras_require={"pip": ["pip"]},
    tests_require=['pip'],
    requires=['pip'],

    install_requires=install_requires_list,
    dependency_links=dependency_links_list,
    
    packages=["unicodemoticon"],

    entry_points={
        "console_scripts": ['unicodemoticon=unicodemoticon.__main__:main'],
    },

    keywords=['Unicode', 'Emoticon', 'Smilies', 'Qt', 'HTML5', 'HTML Entity'],

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'Natural Language :: English',

        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',

        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development',

    ],
)


log.info("Finished build of setuptools.setup().")
