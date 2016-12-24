"""
This package is responsible for working with windows registry
"""
import winreg
REG_PATH = r'Software\OS_CW\Settings'

def str2bool(str):
    return True if str == 'True' else False

default_settings = {
    'fullscreen': (False, str2bool),
    'poly_n': (1, int),
    'autoplay': (True, str2bool)
}


class Settings:
    def __init__(self):

        for key, (val, type_) in default_settings.items():
            try:
                val = type_(self.get_setting(key))
            except ValueError:
                self.set_setting(key, val)
            self.__dict__[key] = val
        print(self.__dict__)

    def set_setting(self, name, value):
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        value = str(value)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)

    def get_setting(self, name):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
        except WindowsError:
            raise ValueError
        return value

    def __setattr__(self, name, val):
        self.set_setting(name, val)
        self.__dict__[name] = val
