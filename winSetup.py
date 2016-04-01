#!/usr/bin/env python
#-*- coding:utf-8 -*-

import _winreg
import os
import sys
import re

REGEX_PATH = re.compile(r"^[A-Z]{1}:(\\[A-Za-z\s]+){0,5}\\?$")
REGEX_FONT = re.compile(r"^SourceCodePro.*\.ttf$")


class BadPathFormat(Exception):
    _info = """
	INSTALLATION FAILED:
	Bad format of installation path, the following format is recommended:
		Drive:\sub_directory1\sub_directory2
	"""


class FontRelyError(Exception):
    _info = """
	INSTALLATION FAILED:
	Font <<Source Code Pro>> is needed,please install the font first.
	"""


class PackageInstall:

    def __init__(self, path="C:\\"):
        if REGEX_PATH.search(path):
            self.abspath = path.rstrip("\\")
            self.hkeypath = path.rstrip("\\").replace("\\", "_")
        else:
            raise BadPathFormat(BadPathFormat._info)

    def _fontRegister(self):
        _fontList = os.listdir("C:\\Windows\\Fonts")

        _flag = False
        for font in _fontList:
            if REGEX_FONT.search(font):
                _flag = True
                break
        if not _flag:
            raise FontRelyError(FontRelyError._info)

        _sub_key = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Console\\TrueTypeFont"
        try:
            _preKeyHandle = _winreg.OpenKey(
                _winreg.HKEY_LOCAL_MACHINE, _sub_key, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.SetValueEx(
                _preKeyHandle,
                "000",
                0,
                _winreg.REG_SZ,
                "Source Code Pro")
        except WindowsError as err:
            print str(err)
            sys.exit(2)
        finally:
            _winreg.CloseKey(_preKeyHandle)

    def _copyFiles(self):
        _dir = self.abspath + "\\" + "MACQuery"

        try:
            os.mkdir(_dir)
        except (IOError, OSError) as err:
            print str(err)
            sys.exit(2)
        try:
            os.system("xcopy * %s /Y /EXCLUDE:exList.txt" % _dir)
        except (IOError, OSError) as err:
            print str(err)
            sys.exit(2)

    def _mainRegister(self):
        _pairs = [("CodePage", _winreg.REG_DWORD, 850),
                  ("ScreenBufferSize", _winreg.REG_DWORD, 19660909),
                  ("WindowSize", _winreg.REG_DWORD, 2293869),
                  ("FontSize", _winreg.REG_DWORD, 1179648),
                  ("FontFamily", _winreg.REG_DWORD, 54),
                  ("FontWeight", _winreg.REG_DWORD, 400),
                  ("FaceName", _winreg.REG_SZ, "Source Code Pro"),
                  ]

        _suffix = "_MACQuery_main.exe"
        _hkey = self.hkeypath + _suffix

        try:
            _preKeyHandle = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER, "Console", 0, _winreg.KEY_ALL_ACCESS)
            _newKeyHandle = _winreg.CreateKey(_preKeyHandle, _hkey)

            for _name, _type, _value in _pairs:
                _winreg.SetValueEx(_newKeyHandle, _name, 0, _type, _value)
        except WindowsError as err:
            print str(err)
            sys.exit(2)
        finally:
            _winreg.CloseKey(_newKeyHandle)
            _winreg.CloseKey(_preKeyHandle)

    def packed(self):
        self._fontRegister()
        self._copyFiles()
        self._mainRegister()


if __name__ == "__main__":
    _install_dir = raw_input("INSTALL DIRECTORY:")
    try:
        handler = PackageInstall(_install_dir)
        handler.packed()
    except BadPathFormat as err:
        print str(err)
    except FontRelyError as err:
        print str(err)
