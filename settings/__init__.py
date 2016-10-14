"""
This package is responsible for working with windows registry
"""
import winreg
REG_PATH = r'Software\OS_CW\Settings'

default_settings = {
    'fullscreen': False,
    'type_of_interpolation': 'string',
    'int': 14,
    'float': '2.456'
}


def edit_setting(name, value):
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
    type_reg = None
    if isinstance(value, int):
        type_reg = winreg.REG_DWORD
        value = int(value)
    elif isinstance(value, str):
        type_reg = winreg.REG_SZ
        value = str(value)
    winreg.SetValueEx(key, name, 0, type_reg, value)
    winreg.CloseKey(key)
    return value


def get_settings():
    settings = {}
    for setting_name, default_value in default_settings.items():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, setting_name)
            winreg.CloseKey(key)
        except WindowsError:
            value = edit_setting(setting_name, default_value)
        settings[setting_name] = value
    return settings


def restore_default():
    for setting_name, default_value in default_settings.items():
        edit_setting(setting_name, default_value)