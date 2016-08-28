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
# To generate a zipapp:
# python3 setup.py zipapp
#
#
# To try it locally:
# python3 setup.py install .
#
#
# To Upload to PyPI by executing:
# sudo pip install --upgrade pip setuptools wheel virtualenv
# python3 setup.py register
# python3 setup.py bdist_egg bdist_wheel --universal sdist --formats=bztar,gztar,zip upload --sign


"""Setup.py for Python, as Generic as possible."""


import os
import re

from setuptools import setup, Command
from tempfile import TemporaryDirectory
from shutil import copytree
from zipapp import create_archive

from unicodemoticon import (__author__, __url__, __email__, __license__,
                            __version__)


##############################################################################
# EDIT HERE


DESCRIPTION = ("Like a Color Picker but for Unicode Emoticons. "
               "Trayicon with Unicode Emoticons using Python3 Qt5.")


print("Starting build of setuptools.setup().")


class ZipApp(Command):
    description, user_options = "Creates a zipapp.", []

    def initialize_options(self): pass  # Dont needed, but required.

    def finalize_options(self): pass  # Dont needed, but required.

    def run(self):
        with TemporaryDirectory() as tmpdir:
            copytree('unicodemoticon', os.path.join(tmpdir, 'unicodemoticon'))
            fyle = os.path.join(tmpdir, '__main__.py')
            with open(fyle, 'w', encoding='utf-8') as entry:
                entry.write("import runpy\nrunpy.run_module('unicodemoticon')")
            create_archive(tmpdir, 'unicodemoticon.pyz', '/usr/bin/env python3')


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

    install_requires=['anglerfish'],
    setup_requires=['anglerfish'],
    tests_require=['anglerfish'],
    requires=['anglerfish'],

    packages=["unicodemoticon"],
    package_data={"unicodemoticon": ['unicodemoticon.desktop']},

    entry_points={
        "console_scripts": ['unicodemoticon=unicodemoticon.__main__:main'],
    },

    cmdclass={
        "zipapp": ZipApp,
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
        'Programming Language :: Python :: 3.5',

        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development',

    ],
)


print("Finished build of setuptools.setup().")
