import functools
import logging as log
import os
import signal
import socket
import stat
import sys
import traceback
from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from getpass import getuser
from json import dumps, loads
from platform import platform, python_version
from shutil import disk_usage, make_archive, rmtree
from subprocess import call
from tempfile import gettempdir
from time import sleep
from urllib import request
from webbrowser import open_new_tab

try:
    import resource
except ImportError:
    resource = None  # MS Window dont have resource

from . import __url__, __source__, __doc__

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


def typecheck(f):
    """Decorator for Python3 annotations to type-check inputs and outputs."""
    def __check_annotations(tipe):
        _type, is_ok = None, isinstance(tipe, (type, tuple, type(None)))
        if is_ok:  # Annotations can be Type or Tuple or None
            _type = tipe if isinstance(tipe, tuple) else tuple((tipe, ))
            if None in _type:  # if None on tuple replace with type(None)
                _type = tuple([_ if _ is not None else type(_) for _ in _type])
        return _type, is_ok

    @functools.wraps(f)  # wrap a function or method to Type Check it.
    def decorated(*args, **kwargs):
        msg = "Type check error: {0} must be {1} but is {2} on function {3}()."
        notations, f_name = tuple(f.__annotations__.keys()), f.__code__.co_name
        for i, name in enumerate(f.__code__.co_varnames):
            if name not in notations:
                continue  # this arg name has no annotation then skip it.
            _type, is_ok = __check_annotations(f.__annotations__.get(name))
            if is_ok:  # Force to tuple
                if i < len(args) and not isinstance(args[i], _type):
                    log.critical(msg.format(repr(args[i])[:50], _type,
                                            type(args[i]), f_name))
                elif name in kwargs and not isinstance(kwargs[name], _type):
                    log.critical(msg.format(repr(kwargs[name])[:50], _type,
                                            type(kwargs[name]), f_name))
        out = f(*args, **kwargs)
        _type, is_ok = __check_annotations(f.__annotations__.get("return"))
        if is_ok and not isinstance(out, _type) and "return" in notations:
            log.critical(msg.format(repr(out)[:50], _type, type(out), f_name))
        return out    # The output result of function or method.
    return decorated  # The decorated function or method.


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
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.dont_write_bytecode = True
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
            start_file.write(desktop_file_content)
    apps_dir = os.path.join(os.path.expanduser("~"),
                            ".local", "share", "applications")
    desktop_file = os.path.join(apps_dir, app + ".desktop")
    if os.path.isdir(apps_dir) and not os.path.isfile(desktop_file):
        log.info("Writing Desktop Launcher file: " + desktop_file)
        with open(desktop_file, "w", encoding="utf-8") as desktop_file_obj:
            desktop_file_obj.write(desktop_file_content)
    return desktop_file


def log_exception():
    """Log Exceptions but pretty printing with more info, return string."""
    unfriendly_names = {"<module>": "Unnamed Anonymous Module Function",
                        "<stdin>": "System Standard Input Function"}
    line_tpl = "    |___ {key} = {val}  # Type: {t}, Size: {s}Bytes, ID: {i}\n"
    body_tpl = """
    ################################ D E B U G ###############################
    Listing all Local objects by context frame, ordered by innermost last:
    {body}
    Thats all we know about the error, check the LOG file and StdOut.
    ############################### D E B U G #############################"""
    tb, body_txt, whole_txt = sys.exc_info()[2], "", ""
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    for frame in stack:
        if frame.f_code.co_name in unfriendly_names.keys():
            fun = unfriendly_names[frame.f_code.co_name]
        else:
            fun = "Function {0}()".format(frame.f_code.co_name)
        body_txt += "\nThe {nm} from file {fl} at line {ln} failed!.".format(
            nm=fun, fl=frame.f_code.co_filename, ln=frame.f_lineno)
        body_txt += "\n    {}\n    |\n".format(fun)
        for key, value in frame.f_locals.items():
            whole_txt += line_tpl.format(key=key, val=repr(value)[:50],
                                         t=str(type(value))[:25],
                                         s=sys.getsizeof(key), i=id(value))
    result = body_tpl.format(body=body_txt + whole_txt)
    log.debug(result)
    return result


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
    except Exception:
        log_exception()
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


def watch(file_path, callback=None):
    """Watch a file path for changes run callback if modified. A WatchDog."""
    log.debug("Watching for changes on path: {0}.".format(file_path))
    previous = int(os.stat(file_path).st_mtime)
    while True:
        actual = int(os.stat(file_path).st_mtime)
        if previous == actual:
            sleep(60)
        else:
            previous = actual
            log.debug("Modification detected on {0}.".format(file_path))
            return callback(file_path) if callback else file_path


def beep(waveform=(79, 45, 32, 50, 99, 113, 126, 127)):
    """Cross-platform Sound Playing with StdLib only,No Sound file required."""
    wavefile = os.path.join(gettempdir(), "beep.wav")
    if not os.path.isfile(wavefile) or not os.access(wavefile, os.R_OK):
        with open(wavefile, "w+") as wave_file:
            for sample in range(0, 1000, 1):
                for wav in range(0, 8, 1):
                    wave_file.write(chr(waveform[wav]))
    if sys.platform.startswith("linux"):
        return call("chrt -i 0 aplay '{fyle}'".format(fyle=wavefile), shell=1)
    if sys.platform.startswith("darwin"):
        return call("afplay '{fyle}'".format(fyle=wavefile), shell=True)
    if sys.platform.startswith("win"):  # FIXME: This is Ugly.
        return call("start /low /min '{fyle}'".format(fyle=wavefile), shell=1)


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


def pdb_on_exception(debugger="pdb", limit=100):
    """Install handler attach post-mortem pdb console on an exception."""
    pass

    def pdb_excepthook(exc_type, exc_val, exc_tb):
        traceback.print_tb(exc_tb, limit=limit)
        __import__(str(debugger).strip().lower()).post_mortem(exc_tb)

    sys.excepthook = pdb_excepthook

ipdb_on_exception = pdb_on_exception


def write_atomic(dest_path, **kwargs):
    """A convenient interface to AtomicWriter type."""
    return AtomicWriter(dest_path, **kwargs)


def rename_atomic(path, new_path, overwrite=False):
    """Atomic rename of a path."""
    if overwrite:
        os.rename(path, new_path)
    else:
        os.link(path, new_path)
        os.unlink(path)


_TEXT_OPENFLAGS = os.O_RDWR | os.O_CREAT | os.O_EXCL
if hasattr(os, 'O_NOINHERIT'):
    _TEXT_OPENFLAGS |= os.O_NOINHERIT
if hasattr(os, 'O_NOFOLLOW'):
    _TEXT_OPENFLAGS |= os.O_NOFOLLOW
_BIN_OPENFLAGS = _TEXT_OPENFLAGS
if hasattr(os, 'O_BINARY'):
    _BIN_OPENFLAGS |= os.O_BINARY

try:
    import fcntl as fcntl
except ImportError:
    def set_cloexec(fd):
        "Dummy set_cloexec for platforms without fcntl support."
        pass
else:
    def set_cloexec(fd):
        """Does a best-effort fcntl.fcntl call to set a fd to be
        automatically closed by any future child processes."""
        try:
            flags = fcntl.fcntl(fd, fcntl.F_GETFD, 0)
        except IOError:
            pass
        else:
            flags |= fcntl.FD_CLOEXEC  # flags read successfully, modify
            fcntl.fcntl(fd, fcntl.F_SETFD, flags)


class AtomicWriter(object):

    """context manager with a writable file which will be moved into place
    as long as no exceptions are raised within the context manager's block.
    These "part files" are created in the same directory as the destination
    path to ensure atomic move operations. Similar to Chrome Downloads.

    Args:
        dest_path (str): The path where the completed file will be written.
        overwrite (bool): overwrite destination file if exists. Defaults True.
        delete_part_if_fail (bool): Move *.part to temp folder if exception.
    """

    def __init__(self, dest_path, **kwargs):
        super(AtomicWriter, self).__init__(dest_path, **kwargs)
        self.dest_path = dest_path
        self.overwrite = kwargs.pop('overwrite', True)
        self.delete_part_if_fail = kwargs.pop('delete_part_if_fail', True)
        self.text_mode = kwargs.pop('text_mode', False)  # for windows
        self.dest_path = os.path.abspath(self.dest_path)
        self.dest_dir = os.path.dirname(self.dest_path)
        self.part_path = dest_path + '.part'
        self.mode = 'w+' if self.text_mode else 'w+b'
        self.open_flags = _TEXT_OPENFLAGS if self.text_mode else _BIN_OPENFLAGS
        self.part_file = None

    def _open_part_file(self):
        do_chmod = True
        try:
            stat_res = os.stat(self.dest_path)  # copy from file being replaced
            file_perms = stat.S_IMODE(stat_res.st_mode)
        except (OSError, IOError):
            file_perms = 0o644  # default if no file exists
            do_chmod = False  # respect the umask
        fd = os.open(self.part_path, self.open_flags, file_perms)
        set_cloexec(fd)
        self.part_file = os.fdopen(fd, self.mode, -1)
        if do_chmod:  # if default perms are overridden by the user or
            try:  # previous dest_path chmod away the effects of the umask
                os.chmod(self.part_path, file_perms)
            except (OSError, IOError):
                self.part_file.close()
                raise

    def setup(self):
        """Called on context manager entry (the with statement)."""
        if os.path.lexists(self.dest_path):
            if not self.overwrite:
                raise OSError('File already exists!: ' + self.dest_path)
        if os.path.lexists(self.part_path):
            os.unlink(self.part_path)
        self._open_part_file()

    def __enter__(self):
        self.setup()
        return self.part_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.part_file.close()
        tmp_file = os.path.join(gettempdir(), os.path.basename(self.part_path))
        if exc_type:
            if self.delete_part_if_fail:
                try:
                    rename_atomic(self.part_path, tmp_file, True)  # os.unlink
                except:
                    pass
            return
        try:
            rename_atomic(self.part_path, self.dest_path,
                          overwrite=self.overwrite)
        except OSError:
            if self.delete_part_if_fail:
                rename_atomic(self.part_path, tmp_file, True)  # os.unlink()
            raise  # could not save destination file
