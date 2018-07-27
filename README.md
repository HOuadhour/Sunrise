# Sunrise
Sunrise is a schedule and to-do list program, created using Python3 and PyQt5.
We believe that the successful day starts at the Sunrise.
For that reason we have choosed to name the program **Sunrise**.

---
# Getting Started
At the moment we don't have binaries versions neither for GNU/Linux nor Windows.
So no desktop icon shortcuts, all of these steps you have to do it alone.

## Installing Sunrise
Before we start installing the application we must install `git` and `wget`
### Installing git and wget

```bash
$ # Arch users
$ sudo pacman -Sy --needed git wget
```

### Download the install script
```bash
sh -c "$(wget https://raw.githubusercontent.com/HOuadhour/sunrise/master/INSTALL.sh -O -)"
```

---
# Prerequisites
To get this program up and running.
We have to install some programs and libraries, 
* `Python3`
* `PyQt5`
* `PyQtChart5`
* `SIP`
* `Qt5-Charts`

---
## Windows Users
### Installing Python
This program uses the version 3.6.2 of Python.
It is recommended to download the same version or higher, but you can work with other versions
but it must be the version 3.x not the version 2.x.
* We open [Python Website](https://www.python.org/downloads/windows/) and download the corresponding version 32bit or 64bit.

![1](https://s5.postimg.cc/rxg6u25o7/Screenshot_2017-10-09_14-51-34.png)

* After the download process complete, we open the file and Install `Python`.
* After the installation process complete, open your `cmd` and type `python --version`.
* If you get an answer similar to this, we are good to move to the next step.

![2](https://s5.postimg.cc/ie6i0dcyf/Capture.png)

---
### Installing PyQt
PyQt has two version in this program we need to install `PyQt5`.
by opening the `cmd` as an administrator and type this command.
```cmd
pip install PyQt5
```
![3](https://s5.postimg.cc/o2csrc9lz/Capture3.png)
After the download and installation process complete, we move to the next step.

---
### Installing PyQtChart
We open the `cmd` as an administrator and type this command.
```cmd
pip install PyQtChart
```
![4](https://s5.postimg.cc/pu5rm9ntz/Capture4.png)
After we finnish all these steps we are ready to run the program but before that, let's check our installation.

Open `cmd` and type `python`.
Then you will get a screen like this, type the following code.
```python
>>> from PyQt5 import QtChart
>>>
```
![5](https://s5.postimg.cc/kvi97rew7/Capture5.png)
If you get an error, make sure you did all the steps correctly.

---
## Linux & Mac Users
### Installing Python
Most of Linux distrubutions comes with two versions of `python` already installed for you.
#### Arch Linux Users
The default version of `python` for **Arch Linux** unlike other distributions is the version 3.
So if we type:
```bash
$ python3 --version
$ python --version
```
It will give the same result, to get the version of `python2` in **Arch Linux** You have to type:
```bash
python2 --version
```
#### Other Distros
The default version of `python` for **Ubuntu** and others is the version 2.
So if we type:
```bash
$ python3 --version
$ python --version
```
We will get a different result.

---
### Installing PyQt and PyQtChart
To Install `PyQt5` and `PyQtChart` on Linux system we have two methods.
**I recommend Using the first method**
#### First Method (Recommended)
We will install the packages using our package manager in our distro.

We will take Arch as an example, you can use your own distro and your own package manager.

But let's first uninstall the packages with `pip`.
**Run command twice if it's necessary to check if the package is uninstalled**

```bash
$ sudo pip uninstall PyQt5
$ sudo pip uninstall PyQtChart
$ sudo pip uninstall sip
$ sudo pip uninstall PyQt5-sip
```
---

**Run this command again if you get an error.**

```bash
$ sudo pacman -Sy python-pyqt5 sip python-sip python-sip-pyqt5 qt5-charts
```

After this we will have to download the `PyQtChart` source code from the [Official Website](https://www.riverbankcomputing.com/software/pyqtchart/download)
![6](https://s5.postimg.cc/686xaftvr/07272018-094120.png)

After that we will compile our package.

Navigate to where you download the file, let's say the downloads folder.

```bash
$ cd $HOME/Downloads
```
Check for file existance by typing `ls -l`.

Now let's extract, compile and install the package.
**Don't forget to change the name of the file if you have another name or other version**

```bash
$ tar --gzip -xvf PyQtChart_gpl-5.11.2.tar.gz # Extracting files
$ cd PyQtChart_gpl-5.11.2
$ python3 configure.py
$ make
$ sudo make install
```
**Congratulations on installing!**

#### Second Method
To install `PyQt5` we have to run the same commands as windows, but we have first to install `pip`.

#### Installing pip
##### Arch Linux

Installing `pip` by typing this command in the `terminal`.
```bash
$ sudo pacman -Sy --needed python-pip
```

##### Ubuntu & Linux Mint
Installing `pip` by typing this command in the `terminal`.
```bash
$ sudo apt install python3-pip
```

#### Others
You can use your package manager, and install the package.

---
After installing `pip` or we need to do is to run these commands.
We open the `terminal` and type:

```bash
$ sudo pip3 install PyQt5 
$ sudo pip3 install PyQtChart
```

---

### How To Use Sunrise
We have create a simple wiki for you, to illustrate how to use the program.
You can click here [Sunrise Wiki](https://github.com/HOuadhour/Sunrise/wiki)
