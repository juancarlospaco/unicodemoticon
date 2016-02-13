#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import functools
import logging as log
import os
import signal
import sys

from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from getpass import getuser
from json import dumps, loads
from platform import platform, python_version
from shutil import disk_usage, make_archive, rmtree
from tempfile import gettempdir
from urllib import request
from webbrowser import open_new_tab

from . import __doc__, __source__, __url__

try:
    import resource
except ImportError:
    resource = None  # MS Window dont have resource


CONFIG = None
start_time = datetime.now()


# Force CTRL+C to work to quit the app
signal.signal(signal.SIGINT, signal.SIG_DFL)


def make_logger(name=str(os.getpid())):
    """Build and return a Logging Logger."""
    if not sys.platform.startswith("win") and sys.stderr.isatty():
        def add_color_emit_ansi(fn):
            """Add methods we need to the class."""
            def new(*args):
                """Method overload."""
                if len(args) == 2:
                    new_args = (args[0], copy(args[1]))
                else:
                    new_args = (args[0], copy(args[1]), args[2:])
                if hasattr(args[0], 'baseFilename'):
                    return fn(*args)
                levelno = new_args[1].levelno
                if levelno >= 50:
                    color = '\x1b[31;5;7m\n '  # blinking red with black
                elif levelno >= 40:
                    color = '\x1b[31m'  # red
                elif levelno >= 30:
                    color = '\x1b[33m'  # yellow
                elif levelno >= 20:
                    color = '\x1b[32m'  # green
                elif levelno >= 10:
                    color = '\x1b[35m'  # pink
                else:
                    color = '\x1b[0m'  # normal
                try:
                    new_args[1].msg = color + str(new_args[1].msg) + ' \x1b[0m'
                except Exception as reason:
                    print(reason)  # Do not use log here.
                return fn(*new_args)
            return new
        log.StreamHandler.emit = add_color_emit_ansi(log.StreamHandler.emit)
    log_file = os.path.join(gettempdir(), str(name).lower().strip() + ".log")
    log.basicConfig(level=-1, filemode="w", filename=log_file)
    log.getLogger().addHandler(log.StreamHandler(sys.stderr))
    adrs = "/dev/log" if sys.platform.startswith("lin") else "/var/run/syslog"
    try:
        handler = log.handlers.SysLogHandler(address=adrs)
    except Exception:
        log.debug("Unix SysLog Server not found, ignored Logging to SysLog.")
    else:
        log.getLogger().addHandler(handler)
    log.debug("Logger created with Log file at: {0}.".format(log_file))
    return log


def make_root_check_and_encoding_debug():
    """Debug and Log Encodings and Check for root/administrator,return Bool."""
    log.info(__doc__)
    log.debug("Python {0} on {1}.".format(python_version(), platform()))
    log.debug("STDIN Encoding: {0}.".format(sys.stdin.encoding))
    log.debug("STDERR Encoding: {0}.".format(sys.stderr.encoding))
    log.debug("STDOUT Encoding:{}".format(getattr(sys.stdout, "encoding", "")))
    log.debug("Default Encoding: {0}.".format(sys.getdefaultencoding()))
    log.debug("FileSystem Encoding: {0}.".format(sys.getfilesystemencoding()))
    log.debug("PYTHONIOENCODING Encoding: {0}.".format(
        os.environ.get("PYTHONIOENCODING", None)))
    os.environ["PYTHONIOENCODING"], sys.dont_write_bytecode = "utf-8", True
    if not sys.platform.startswith("win"):  # root check
        if not os.geteuid():
            log.warning("Runing as root is not Recommended !.")
            return False
    elif sys.platform.startswith("win"):  # administrator check
        if getuser().lower().startswith("admin"):
            log.warning("Runing as Administrator is not Recommended !.")
            return False
    return True


def set_process_name_and_cpu_priority(name):
    """Set process name and cpu priority."""
    try:
        os.nice(19)  # smooth cpu priority
        libc = cdll.LoadLibrary("libc.so.6")  # set process name
        buff = create_string_buffer(len(name.lower().strip()) + 1)
        buff.value = bytes(name.lower().strip().encode("utf-8"))
        libc.prctl(15, byref(buff), 0, 0, 0)
    except Exception:
        return False  # this may fail on windows and its normal, so be silent.
    else:
        log.debug("Process Name set to: {0}.".format(name))
        return True


def make_post_execution_message(app=__doc__.splitlines()[0].strip()):
    """Simple Post-Execution Message with information about RAM and Time."""
    use, al = 0, 0
    if sys.platform.startswith("linux"):
        use = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss *
                  resource.getpagesize() / 1024 / 1024 if resource else 0)
        al = int(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') /
                 1024 / 1024 if hasattr(os, "sysconf") else 0)
    msg = "Total Maximum RAM Memory used: ~{0} of {1}MegaBytes".format(use, al)
    log.info(msg)
    if start_time and datetime:
        log.info("Total Working Time: {0}".format(datetime.now() - start_time))
    print("Thanks for using this App,share your experience! {0}".format("""
    Twitter: https://twitter.com/home?status=I%20Like%20{n}!:%20{u}
    Facebook: https://www.facebook.com/share.php?u={u}&t=I%20Like%20{n}
    G+: https://plus.google.com/share?url={u}
    Send BitCoins !:
    https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877
    """.format(u=__url__, n=app)))  # see the message, but dont get on logs.
    return msg


def get_or_set_config_folder(appname):
    """Get config folder cross-platform, try to always return a path."""
    if sys.platform.startswith("darwin"):  # Apples Macos
        config_path = os.path.expanduser("~/Library/Preferences")
    elif sys.platform.startswith("win"):  # Windown
        config_path = os.getenv("APPDATA", os.path.expanduser("~/.config"))
    else:
        config_path = os.getenv("XDG_CONFIG_HOME",
                                os.path.expanduser("~/.config"))
    if appname and len(appname) and isinstance(appname, str):
        config_path = os.path.join(config_path, appname.strip())
    log.debug("Config folder for {0} is: {1}".format(appname, config_path))
    if not os.path.isdir(config_path):
        log.debug("Creating new Config folder: {0}.".format(config_path))
        os.makedirs(config_path)
    return config_path


def get_or_set_temp_folder(appname):
    """Get a temp Sub-folder for this App only, cross-platform, return path."""
    if appname and len(appname) and isinstance(appname, str):
        temp_path = os.path.join(gettempdir(), appname.strip().lower())
    log.debug("Temp folder for {0} is: {1}.".format(appname, temp_path))
    if not os.path.isdir(temp_path):
        log.debug("Creating new Temp folder: {0}.".format(temp_path))
        os.makedirs(temp_path)
    return temp_path


def add_desktop_files(app, desktop_file_content):
    """Add to autostart of the Desktop."""
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "autostart")
    autostart_file = os.path.join(config_dir, app + ".desktop")
    if os.path.isdir(config_dir) and not os.path.isfile(autostart_file):
        log.info("Writing Auto-Start file: " + autostart_file)
        with open(autostart_file, "w", encoding="utf-8") as start_file:
            start_file.write(str(desktop_file_content))
    apps_dir = os.path.join(os.path.expanduser("~"),
                            ".local", "share", "applications")
    desktop_file = os.path.join(apps_dir, app + ".desktop")
    if os.path.isdir(apps_dir) and not os.path.isfile(desktop_file):
        log.info("Writing Desktop Launcher file: " + desktop_file)
        with open(desktop_file, "w", encoding="utf-8") as desktop_file_obj:
            desktop_file_obj.write(str(desktop_file_content))
    return desktop_file


def check_working_folder(folder_to_check=os.path.expanduser("~")):
    """Check working folder,passed argument,for everything that can go wrong.
    >>> check_working_folder()
    True
    """
    folder_to_check = os.path.abspath(folder_to_check)  # More Safe on WinOS
    log.debug("Checking the Working Folder: '{0}'".format(folder_to_check))
    # What if folder is not a string.
    if not isinstance(folder_to_check, str):
        log.critical("Folder {0} is not String type!.".format(folder_to_check))
        return False
    elif os.path.isfile(folder_to_check):
        log.info("Folder {0} is File or Relative Path".format(folder_to_check))
        return True
    # What if folder is not a folder.
    elif not os.path.isdir(folder_to_check):
        log.critical("Folder {0} does not exist !.".format(folder_to_check))
        return False
    # What if destination folder is not Readable by the user.
    elif not os.access(folder_to_check, os.R_OK):
        log.critical("Folder {0} not Readable !.".format(folder_to_check))
        return False
    # What if destination folder is not Writable by the user.
    elif not os.access(folder_to_check, os.W_OK):
        log.critical("Folder {0} Not Writable !.".format(folder_to_check))
        return False
    elif disk_usage and os.path.exists(folder_to_check):
        hdd = int(disk_usage(folder_to_check).free / 1024 / 1024 / 1024)
        if hdd:  # > 1 Gb
            log.info("Total Free Space: ~{0} GigaBytes.".format(hdd))
            return True
        else:  # < 1 Gb
            log.critical("Total Free Space is < 1 GigaByte; Epic Fail !.")
            return False
    return False


def walkdir_to_filelist(where, target, omit):
    """Perform full walk of where, gather full path of all files."""
    log.debug("Scan {},searching {},ignoring {}".format(where, target, omit))
    return tuple([os.path.join(r, f)
                  for r, d, fs in os.walk(where, followlinks=True)
                  for f in fs if not f.startswith('.') and
                  not f.endswith(omit) and
                  f.endswith(target)])  # only target files,no hidden files


def check_for_updates():
    """Method to check for updates from Git repo versus this version."""
    try:
        last_version = str(request.urlopen(__source__).read().decode("utf8"))
        this_version = str(open(__file__).read())
    except Exception as e:
        log.warning(e) if log else print(e)
    else:
        if this_version != last_version:
            msg = "Theres a new Version!, update the App from: " + __source__
            log.warning(msg)
        else:
            msg = "No new updates!, You have the latest version of this app."
            log.info(msg)
        return msg


def json_pretty(json_dict: dict) -> str:
    """Pretty-Printing JSON data from dictionary to string."""
    _json = dumps(json_dict, sort_keys=1, indent=4, separators=(",\n", ": "))
    posible_ends = tuple('true false , " ] 0 1 2 3 4 5 6 7 8 9 \n'.split(" "))
    max_indent, justified_json = 1, ""
    for json_line in _json.splitlines():
        if len(json_line.split(":")) >= 2 and json_line.endswith(posible_ends):
            lenght = len(json_line.split(":")[0].rstrip()) + 1
            max_indent = lenght if lenght > max_indent else max_indent
            max_indent = max_indent if max_indent <= 80 else 80  # Limit indent
    for line_of_json in _json.splitlines():
        condition_1 = max_indent > 1 and len(line_of_json.split(":")) >= 2
        condition_2 = line_of_json.endswith(posible_ends) and len(line_of_json)
        if condition_1 and condition_2:
            propert_len = len(line_of_json.split(":")[0].rstrip()) + 1
            xtra_spaces = " " * (max_indent + 1 - propert_len)
            xtra_spaces = ":" + xtra_spaces
            justified_line_of_json = ""
            justified_line_of_json = line_of_json.split(":")[0].rstrip()
            justified_line_of_json += xtra_spaces
            justified_line_of_json += "".join(
                line_of_json.split(":")[1:len(line_of_json.split(":"))])
            justified_json += justified_line_of_json + "\n"
        else:
            justified_json += line_of_json + "\n"
    return str("\n\n" + justified_json if max_indent > 1 else _json)


def make_config(app):
    """Make a global config object."""
    global CONFIG
    config_file = os.path.join(get_or_set_config_folder(app), "config.json")
    if not os.path.isfile(config_file):
        log.debug("Creating a new JSON Config file: " + config_file)
        with open(config_file, "w", encoding="utf-8") as config_object:
            config_object.write("{}\n")
    with open(config_file, "r", encoding="utf-8") as config_object:
        log.debug("Reading JSON Config file: " + config_file)
        CONFIG = loads(config_object.read().strip())


def view_config(app):
    """Open the JSON config file for app."""
    return open_new_tab(
        os.path.join(get_or_set_config_folder(app), "config.json"))


def autosave_config(app):
    log.debug("Cleaning up, AutoSaving Configs and Shutting Down...")
    config_file = os.path.join(get_or_set_config_folder(app), "config.json")
    with open(config_file, "w", encoding="utf-8") as config_object:
        config_object.write(json_pretty(CONFIG))


def delete_config(app):
    """Delete config folder."""
    return rmtree(get_or_set_config_folder(app), ignore_errors=True)


def backup_config(app):
    """AutoBackup config settings to a compressed ZIP."""
    output_file = os.path.join(os.path.expanduser("~"), app)
    make_archive(output_file, 'zip', get_or_set_config_folder(app), logger=log)
    return output_file + ".zip"


def about_python():
    """Open Python official homepage."""
    return open_new_tab('https://python.org')


def about_self():
    """Open this App homepage."""
    return open_new_tab(__url__)


def view_code():
    """Open this App local Python source code."""
    return open_new_tab(__file__)


def report_bug():
    """Open this App Bug Tracker."""
    return open_new_tab(__url__ + "/issues/new")
