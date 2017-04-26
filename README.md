# Unicodemoticon


[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=plastic)](http://opensource.org/licenses/GPL-3.0) [![LGPL License](http://img.shields.io/badge/license-LGPL-blue.svg?style=plastic)](http://opensource.org/licenses/LGPL-3.0) [![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic)](http://python.org) [![Code Issues](http://www.quantifiedcode.com/api/v1/project/378c3f56d270475a8dff5660772fc2f9/badge.svg)](http://www.quantifiedcode.com/app/project/378c3f56d270475a8dff5660772fc2f9)

![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp.jpg "UnicodEmoticon on Linux")


![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp2.jpg "UnicodEmoticon on Linux")


![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp3.jpg "UnicodEmoticon on Linux")


![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp4.jpg "As-you-type Emoji Search")


https://pypi.python.org/pypi/unicodemoticon
https://aur.archlinux.org/packages/unicodemoticon


- **Python3 ready**, it will only work with Python >= 3, instead of soon to be deprecated *(year 2020)* python2.
- **Unicode ready**, it should handle correctly any kind of character that `UTF-8` can support without escaping.
- Tabbed Window and Trayicon with Unicode Emoticons using Python3 Qt5.
- easy to use
- Set its own Process name and show up on Process lists, GUI Customization via CSS, Icon Customization.
- Can check for updates for itself, Sets Smooth CPU usage, Colored Logging, Single Instance via Sockets.
- On Mouse Hover Previews.
- HTML5 Entities, eg. `&copy;` and Multiple characters Emoticons, eg. `¯\_(ツ)_/¯`.
- Alternating CamelCase for clipboard text, eg. `AlTeRnAtInG CaMeLcAsE FoR ClIpBoArD TeXt`.
- Base64, ROT-13, URL Encode, and more.

# Install permanently on the system:

**PIP:** *(Recommended!)*
```bash
sudo apt-get install python3-pyqt5 ttf-ancient-fonts sni-qt
#  sudo yum install python3-pyqt5 ttf-ancient-fonts
#  sudo pacman -Syu python-pip python-pyqt5 ttf-ancient-fonts
#  sudo yaourt -Sy emojione-color-font ttf-freefont noto-fonts-emoji
sudo pip3 install unicodemoticon
```

# Why?:

- I wanted a quick and simple Menu organized by categories to copy Emoticons for the whole desktop.
- Like a Color Picker but for Unicode Emoticons.


# Requisites:

- **Linux / Os X / MS Window**
- [Python 3.x](https://www.python.org "Python Homepage") *(No Python2)*
- [PyQt 5.x](http://www.riverbankcomputing.co.uk/software/pyqt/download5 "PyQt5 Homepage") *(No Qt4)*

**Optionals:**
- **ttf-ancient-fonts** *(Linux Package with Fonts that support Emoji)*
- noto-fonts-emoji: Another font with emoji *(Linux Package with Fonts that support Emoji)*
- ttf-symbola: Font with emoji *(Linux Package with Fonts that support Emoji)*
- noto-fonts: Fonts designed to cover a wide unicode range *(Linux Package with Fonts that support Emoji)*
- ttf-freefont: Another font covering a wide unicode range *(Linux Package with Fonts that support Emoji)*
- emojione-color-font: Full-Color Fonts specifically designed for Emoji *(Linux Package with Fonts that support Emoji)*
- [QDarkStyleSheet *(CSS base for Qt5)*](https://github.com/ColinDuquesnoy/QDarkStyleSheet#qdarkstylesheet) `sudo pip3 install qdarkstyle`


# Windows

Support is very limited by Windows itself for Unicode.
Install all these fonts as admin and reboot the system:

- ttf-ancient-fonts: https://launchpad.net/ubuntu/+archive/primary/+files/ttf-ancient-fonts_2.59.orig.tar.xz
- noto-fonts-emoji: https://github.com/googlei18n/noto-emoji/blob/master/fonts/NotoEmoji-Regular.ttf


# Vim:

- Add in your `~/.vimrc` file this lines:

```bash
:set encoding=utf-8
:set termencoding=utf-8
```


# Coding Style Guide:

- Lint, [PEP-8](https://www.python.org/dev/peps/pep-0008), [PEP-257](https://www.python.org/dev/peps/pep-0257), [PyLama](https://github.com/klen/pylama#-pylama), [iSort](https://github.com/timothycrosley/isort) must Pass Ok. `pip install pep8 pep257 pylama isort`
- If theres any kind of Tests, they must Pass Ok, if theres no Tests, its ok, if Tests provided, is even better.


# Contributors:

- **Please Star this Repo on Github !**, it helps to show up faster on searchs.
- [Help](https://help.github.com/articles/using-pull-requests) and more [Help](https://help.github.com/articles/fork-a-repo) and Interactive Quick [Git Tutorial](https://try.github.io).
- Please take special care of NOT breaking any existing emoji before sending a Pull Request.


# Licence:

- GNU GPL Latest Version *AND* GNU LGPL Latest Version *AND* any Licence [YOU Request via Bug Report](https://github.com/juancarlospaco/unicodemoticon/issues/new).


# Ethics and Humanism Policy:

- This project is [LGBTQQIAAP friendly](http://www.urbandictionary.com/define.php?term=LGBTQQIAAP "Whats LGBTQQIAAP").
