unicodemoticon
==============


[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=plastic)](http://opensource.org/licenses/GPL-3.0) [![LGPL License](http://img.shields.io/badge/license-LGPL-blue.svg?style=plastic)](http://opensource.org/licenses/LGPL-3.0) [![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic)](http://python.org) [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif "Donate with or without Credit Card")](http://goo.gl/cB7PR)


![screenshot](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/temp.jpg "UnicodEmoticon on Linux")


- Trayicon with Unicode Emoticons using Python3 Qt5.
- StandAlone, single-file, easy to use.
- Set its own Process name and show up on Process lists.
- Can check for updates for itself.
- Smooth CPU usage.
- HTML5 Entities, eg. `&copy;` and Multiple characters Emoticons, eg. `¯\_(ツ)_/¯`.


# Try it !: 
*(Without installing anything)*
```
wget -O - https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py | python3
```

# Install permanently on the system:

**PIP:** *(Recommended!)*
```
sudo apt-get install python3-pyqt5 ttf-ancient-fonts  
#  sudo yum install python3-pyqt5 ttf-ancient-fonts
#  sudo pacman -Syu python-qt5 ttf-ancient-fonts
sudo pip3 install unicodemoticon
```

**PIP from Git:**
```
sudo pip3 install git+https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py
```

**WGET:**
```
sudo wget -O /usr/bin/unicodemoticon.py https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py
sudo chmod +x /usr/bin/unicodemoticon.py
unicodemoticon.py
```

**MANUALLY:**

- Save [this file](https://raw.githubusercontent.com/juancarlospaco/unicodemoticon/master/unicodemoticon.py) and run it with Python3.


# Why?:

- I wanted a quick and simple Menu organized by categories to copy Emoticons for the whole desktop.
- Like a Color Picker but for Unicode Emoticons.


# Requisites:

- **Linux / Os X** *(No MS Window)*
- [Python 3.x](https://www.python.org "Python Homepage") *(No Python2)*
- [PyQt 5.x](http://www.riverbankcomputing.co.uk/software/pyqt/download5 "PyQt5 Homepage")
- ttf-ancient-fonts *(Linux Package)*

[Oxygen](https://www.google.com/fonts/specimen/Oxygen) and [Ubuntu](https://www.google.com/fonts/specimen/Ubuntu) Fonts Recommended but Optional.


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


# Ethics and Humanism Policy:
- May this FLOSS be always Pristine and Clean, No AdWare, No Spamm, No BundleWare, No Infomercial, No MalWare.
- This project is [LGBTQQIAAP friendly](http://www.urbandictionary.com/define.php?term=LGBTQQIAAP "Whats LGBTQQIAAP").


Donate, Charityware :
---------------------

- [Charityware](https://en.wikipedia.org/wiki/Donationware) is a licensing model that supplies fully operational unrestricted software to the user and requests an optional donation be paid to a third-party beneficiary non-profit. The amount of donation may be left to the discretion of the user. Its GPL-compatible and Enterprise ready.
- If you want to Donate please [click here](http://www.icrc.org/eng/donations/index.jsp) or [click here](http://www.atheistalliance.org/support-aai/donate) or [click here](http://www.msf.org/donate) or [click here](http://richarddawkins.net/) or [click here](http://www.supportunicef.org/) or [click here](http://www.amnesty.org/en/donate)
