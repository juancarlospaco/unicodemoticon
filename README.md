.. ..

 # Unicodemoticon


 [![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=plastic)](http://opensource.org/licenses/GPL-3.0) [![LGPL License](http://img.shields.io/badge/license-LGPL-blue.svg?style=plastic)](http://opensource.org/licenses/LGPL-3.0) [![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic)](http://python.org) [![Code Issues](http://www.quantifiedcode.com/api/v1/project/378c3f56d270475a8dff5660772fc2f9/badge.svg)](http://www.quantifiedcode.com/app/project/378c3f56d270475a8dff5660772fc2f9)

 [![Donate BitCoins](https://www.coinbase.com/assets/buttons/donation_large-5cf4f17cc2d2ae2f45b6b021ee498297409c94dcf0ba1bbf76fd5668e80b0d02.png)](https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877 "Donate Bitcoins") [![Subscribe with BitCoins](https://www.coinbase.com/assets/buttons/subscription_large-11d991f628216af05156fae88a48ce25c0cb36447a265421a43a62e572af3853.png)](https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877 "Subscribe with BitCoins") [![Pay with BitCoins](https://www.coinbase.com/assets/buttons/buy_now_large-6f15fa5979d25404827a7329e8a5ec332a42cf4fd73e27a2c3ccda017034e1b0.png)](https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877 "Pay with BitCoins") [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif "Donate with or without Credit Card")](http://goo.gl/cB7PR)


 ![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp.jpg "UnicodEmoticon on Linux")


 ![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp2.jpg "UnicodEmoticon on Linux")


 ![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp3.jpg "UnicodEmoticon on Linux")


 https://pypi.python.org/pypi/unicodemoticon
 https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=unicodemoticon
 
 
 - **Standalone**, uses ONLY Standard Libraries, built-in on Python 3.
 - **Python3 ready**, it will only work with Python >= 3, instead of soon to be deprecated *(year 2020)* python2.
 - **Unicode ready**, it should handle correctly any kind of character that `UTF-8` can support without escaping.
 - Tabbed Window and Trayicon with Unicode Emoticons using Python3 Qt5.
 - easy to use
 - Set its own Process name and show up on Process lists, GUI Customization via CSS, Icon Customization.
 - Can check for updates for itself, Sets Smooth CPU usage, Colored Logging, Single Instance via Sockets.
 - Menu is Semi-Transparent with particles and Rounded Corners with On Mouse Hover Previews.
 - HTML5 Entities, eg. `&copy;` and Multiple characters Emoticons, eg. `¯\_(ツ)_/¯`.
 - Alternating CamelCase for clipboard text, eg. `AlTeRnAtInG CaMeLcAsE FoR ClIpBoArD TeXt`.
 - Base64, ROT-13, URL Encode, and more.


 # Try it !:
 *(Without installing anything)*
 ```
 wget -O https://github.com/juancarlospaco/unicodemoticon/releases/download/2.1.0/unicodemoticon-2.1.0.pyz
 python3 unicodemoticon-2.1.0.pyz
 ```

 # Install permanently on the system:

 **PIP:** *(Recommended!)*
 ```
 sudo apt-get install python3-pyqt5 ttf-ancient-fonts sni-qt
 #  sudo yum install python3-pyqt5 ttf-ancient-fonts
 #  sudo pacman -Syu python-pip python-pyqt5 ttf-ancient-fonts
 sudo pip3 install unicodemoticon
 ```

 **PIP from Git:**
 ```
 sudo pip3 install git+git://github.com/juancarlospaco/unicodemoticon.git
 ```

 **MANUALLY:**

 - Save [this file](https://github.com/juancarlospaco/unicodemoticon/releases/download/2.1.0/unicodemoticon-2.1.0.pyz) and run it with Python3. (Your OS probably already uses python3 to open it when you click on it)


 # Why?:

 - I wanted a quick and simple Menu organized by categories to copy Emoticons for the whole desktop.
 - Like a Color Picker but for Unicode Emoticons.


 # Requisites:

 - **Linux / Os X** *(No MS Window)*
 - [Python 3.x](https://www.python.org "Python Homepage") *(No Python2)*
 - [PyQt 5.x](http://www.riverbankcomputing.co.uk/software/pyqt/download5 "PyQt5 Homepage") *(No Qt4)*

 **Optionals:**
 - **ttf-ancient-fonts** *(Linux Package with Fonts that support Emoji)*
 - noto-fonts-emoji: Another font with emoji *(Linux Package with Fonts that support Emoji)*
 - ttf-symbola: Font with emoji *(Linux Package with Fonts that support Emoji)*
 - noto-fonts: Fonts designed to cover a wide unicode range *(Linux Package with Fonts that support Emoji)*
 - ttf-freefont: Another font covering a wide unicode range *(Linux Package with Fonts that support Emoji)*
 - [QDarkStyleSheet *(CSS base for Qt5)*](https://github.com/ColinDuquesnoy/QDarkStyleSheet#qdarkstylesheet) `sudo pip3 install qdarkstyle`


# Windows

Support is very limited by Windows itself for Unicode.
Install all these fonts as admin and reboot the system:

 - ttf-ancient-fonts: https://launchpad.net/ubuntu/+archive/primary/+files/ttf-ancient-fonts_2.59.orig.tar.xz
 - noto-fonts-emoji: https://github.com/googlei18n/noto-emoji/blob/master/fonts/NotoEmoji-Regular.ttf


 # Vim:

 - Add in your `~/.vimrc` file this lines:

 ```
 :set encoding=utf-8
 :set termencoding=utf-8
 ```


 # Coding Style Guide:

 - Lint, [PEP-8](https://www.python.org/dev/peps/pep-0008), [PEP-257](https://www.python.org/dev/peps/pep-0257), [PyLama](https://github.com/klen/pylama#-pylama), [iSort](https://github.com/timothycrosley/isort) must Pass Ok. `pip install pep8 pep257 pylama isort`
 - If theres any kind of Tests, they must Pass Ok, if theres no Tests, its ok, if Tests provided, is even better.


 # Contributors:

 - **Please Star this Repo on Github !**, it helps to show up faster on searchs.
 - **Ad-Hocracy Meritocracy**: 3 Pull Requests Merged on Master you become Repo Admin. *Join us!*
 - [Help](https://help.github.com/articles/using-pull-requests) and more [Help](https://help.github.com/articles/fork-a-repo) and Interactive Quick [Git Tutorial](https://try.github.io).


 # Licence:

 - GNU GPL Latest Version *AND* GNU LGPL Latest Version *AND* any Licence [YOU Request via Bug Report](https://github.com/juancarlospaco/unicodemoticon/issues/new).


 # Ethics and Humanism Policy:
 - May this FLOSS be always Pristine and Clean, No AdWare, No Spamm, No BundleWare, No Infomercial, No MalWare.
 - This project is [LGBTQQIAAP friendly](http://www.urbandictionary.com/define.php?term=LGBTQQIAAP "Whats LGBTQQIAAP").


 Donate, Charityware :
 ---------------------

 - [Charityware](https://en.wikipedia.org/wiki/Donationware) is a licensing model that supplies fully operational unrestricted software to the user and requests an optional donation be paid to a third-party beneficiary non-profit. The amount of donation may be left to the discretion of the user. Its GPL-compatible and Enterprise ready.
 - If you want to Donate please [click here](http://www.icrc.org/eng/donations/index.jsp) or [click here](http://www.atheistalliance.org/support-aai/donate) or [click here](http://www.msf.org/donate) or [click here](http://richarddawkins.net/) or [click here](http://www.supportunicef.org/) or [click here](http://www.amnesty.org/en/donate)

.. ..

<!--- unicodemoticon
==============

|GPL License| |LGPL License| |Python Version| |Code Issues|

|Donate BitCoins| |Subscribe with BitCoins| |Pay with BitCoins| |Donate|

https://pypi.python.org/pypi/unicodemoticon

|screenshot|

-  **Standalone**, uses ONLY Standard Libraries, built-in on Python 3.
-  **Single-File**, everything is just 1 file, with PEP-8, Lint and
   other Python Best Practices, very readable.
-  **Python3 ready**, it will only work with Python >= 3, instead of
   soon to be deprecated *(year 2020)* python2.
-  **Minimalism**, do 1 thing do it awesome, is tiny and simple,
   K.I.S.S., its < 1.000 lines.
-  Tabbed Window and Trayicon with Unicode Emoticons and text tools
   using Python3 Qt5.
-  StandAlone, single-file, easy to use.
-  Pretty-Printed colored Logging to Standard Output and Log File on OS
   Temporary Folder.
-  No Dependencies at all, just needs Python Standard Built-in Libs.
-  Set its own Process name and show up on Process lists.
-  Can check for updates for itself.
-  Full Unicode/UTF-8 support.
-  Smooth CPU usage.
-  GUI Customization via CSS, Icon Customization.
-  Single Instance via Sockets.
-  On Mouse Hover Previews.
-  HTML5 Entities, eg. ``&copy;`` and Multiple characters Emoticons, eg.
   ``¯\_(ツ)_/¯``.
-  Alternating CamelCase for clipboard text, eg.
   ``AlTeRnAtInG CaMeLcAsE FoR ClIpBoArD TeXt``.
-  Base64, URL Encode, ROT-13, and more.
-  `*Your Feature or idea here…*`_


Try it !:
=========

*(Without installing anything)*

::

    wget -O - https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py | python3


Install permanently on the system:
==================================

**PIP:** *(Recommended!)*

::

    sudo apt-get install python3-pyqt5 ttf-ancient-fonts sni-qt
    #  sudo yum install python3-pyqt5 ttf-ancient-fonts
    #  sudo pacman -S python-pip python-pyqt5 ttf-symbola
    sudo pip3 install unicodemoticon

\*\*PIP from Git:**

::

    sudo pip3 install git+https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py

**WGET:**

::

    sudo wget -O /usr/bin/unicodemoticon.py https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py
    sudo chmod +x /usr/bin/unicodemoticon.py
    unicodemoticon.py

**MANUALLY:**

-  Save `this file`_ and run it with Python3.


Why?:
=====

-  I wanted a quick and simple Menu organized by categories to copy
   Emoticons for the whole desktop.
-  Like a Color Picker but for Unicode Emoticons.


Requisites:
===========

-  **Linux / Os X** *(No MS Window)*
-  `Python 3.x`_ *(No Python2)*
-  `PyQt 5.x`_ *(No Qt4)*

**Optionals:**

-  **ttf-ancient-fonts** *(Linux Package with Fonts that support Emoji,
   A.K.A. ttf-symbola)*
-  `QDarkStyleSheet *(CSS base for Qt5)*`_
   ``sudo pip3 install qdarkstyle``


Vim:
====

-  Add in your ``~/.vimrc`` file this lines:

::

    :set encoding=utf-8
    :set termencoding=utf-8


Coding Style Guide:
===================

-  Lint, `PEP-8`_, `PEP-257`_, `PyLama`_, `iSort`_ must Pass Ok.
   ``pip install pep8 pep257 pylama isort``
-  If theres any kind of Tests, they must Pass Ok, if theres no Tests,
   its ok, if Tests provided, is even better.


Contributors:
=============

-  **Please Star this Repo on Github !**, it helps to show up faster on
   searchs.
-  **Ad-Hocracy Meritocracy**: 3 Pull Requests Merged on Master you
   become Repo Admin. *Join us!*
-  `Help`_ and more
   `Help <https://help.github.com/articles/fork-a-repo>`__ and
   Interactive Quick `Git Tutorial`_.


Licence:
========

-  GNU GPL Latest Version *AND* GNU LGPL Latest Version *AND* any
   Licence `YOU Request via Bug Report`_.


Ethics and Humanism Policy:
===========================

-  May this FLOSS be always Pristine and Clean, No AdWare, No Spamm, No
   BundleWare, No Infomercial, No MalWare.
-  This project is `LGBTQQIAAP friendly`_.


Donate, Charityware :
---------------------

-  `Charityware`_ is a licensing model that supplies fully operational
   unrestricted software to the user and requests an optional donation
   be paid to a third-party beneficiary non-profit. The amount may be
   left to discretion of the user.
-  If you want to Donate please `click here`_ or `click
   here <http://www.atheistalliance.org/support-aai/donate>`__ or `click
   here <http://www.msf.org/donate>`__ or `click
   here <http://richarddawkins.net/>`__ or `click
   here <http://www.supportunicef.org/>`__ or `click
   here <http://www.amnesty.org/en/donate>`__ or `click
   here <http://www.rescue.org/irc-fast-facts>`__




.. _PEP-8: https://www.python.org/dev/peps/pep-0008
.. _PEP-257: https://www.python.org/dev/peps/pep-0257
.. _PyLama: https://github.com/klen/pylama#-pylama
.. _iSort: https://github.com/timothycrosley/isort
.. _Help: https://help.github.com/articles/using-pull-requests
.. _Git Tutorial: https://try.github.io
.. _YOU Request via Bug Report: https://github.com/juancarlospaco/unicodemoticon/issues/new
.. _LGBTQQIAAP friendly: http://www.urbandictionary.com/define.php?term=LGBTQQIAAP
.. _Charityware: https://en.wikipedia.org/wiki/Donationware
.. _click here: http://www.icrc.org/eng/donations/index.jsp
.. _this file: https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py
.. _Python 3.x: https://www.python.org
.. _PyQt 5.x: http://www.riverbankcomputing.co.uk/software/pyqt/download5
.. _QDarkStyleSheet *(CSS base for Qt5)*: https://github.com/ColinDuquesnoy/QDarkStyleSheet#qdarkstylesheet
.. _*Your Feature or idea here…*: https://github.com/juancarlospaco/unicodemoticon/pulls
.. |GPL License| image:: http://img.shields.io/badge/license-GPL-blue.svg?style=plastic
   :target: http://opensource.org/licenses/GPL-3.0
.. |LGPL License| image:: http://img.shields.io/badge/license-LGPL-blue.svg?style=plastic
   :target: http://opensource.org/licenses/LGPL-3.0
.. |Python Version| image:: https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic
   :target: http://python.org
.. |Code Issues| image:: http://www.quantifiedcode.com/api/v1/project/378c3f56d270475a8dff5660772fc2f9/badge.svg
   :target: http://www.quantifiedcode.com/app/project/378c3f56d270475a8dff5660772fc2f9
.. |Donate BitCoins| image:: https://www.coinbase.com/assets/buttons/donation_large-5cf4f17cc2d2ae2f45b6b021ee498297409c94dcf0ba1bbf76fd5668e80b0d02.png
   :target: https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877
.. |Subscribe with BitCoins| image:: https://www.coinbase.com/assets/buttons/subscription_large-11d991f628216af05156fae88a48ce25c0cb36447a265421a43a62e572af3853.png
   :target: https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877
.. |Pay with BitCoins| image:: https://www.coinbase.com/assets/buttons/buy_now_large-6f15fa5979d25404827a7329e8a5ec332a42cf4fd73e27a2c3ccda017034e1b0.png
   :target: https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877
.. |Donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif
   :target: http://goo.gl/cB7PR
.. |screenshot| image:: https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp.jpg

..  --->
