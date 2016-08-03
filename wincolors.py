__author__ = 'encode'

class colors:
    BACKGROUND_BLACK    = 0x0000
    BACKGROUND_BLUE    = 0x0011
    BACKGROUND_GREEN   = 0x0022
    BACKGROUND_CYAN    = 0x0033
    BACKGROUND_RED    = 0x0044
    BACKGROUND_PINK   = 0x0055
    BACKGROUND_YELLOW    = 0x0066
    BACKGROUND_WHITE    = 0x0077
    BACKGROUND_GRAY    = 0x0088
    BACKGROUND_LBLUE    = 0x0099
    BACKGROUND_LGREEN    = 0x00AA
    BACKGROUND_LCYAN    = 0x00BB
    BACKGROUND_LRED    = 0x00CC
    BACKGROUND_LPINK    = 0x00DD
    BACKGROUND_LYELLOW    = 0x00EE
    BACKGROUND_LWHITE    = 0x00FF


    FOREGROUND_BLACK    = 0x0000
    FOREGROUND_BLUE    = 0x0001
    FOREGROUND_GREEN   = 0x0002
    FOREGROUND_CYAN    = 0x0003
    FOREGROUND_RED    = 0x0004
    FOREGROUND_PINK   = 0x0005
    FOREGROUND_YELLOW    = 0x0006
    FOREGROUND_WHITE    = 0x0007
    FOREGROUND_GRAY    = 0x0008
    FOREGROUND_LBLUE    = 0x0009
    FOREGROUND_LGREEN    = 0x000A
    FOREGROUND_LCYAN    = 0x000B
    FOREGROUND_LRED    = 0x000C
    FOREGROUND_LPINK    = 0x000D
    FOREGROUND_LYELLOW    = 0x000E
    FOREGROUND_LWHITE    = 0x000F

    WARNING = 0x000C
    ERROR = 0x0004
    INFO = 0x0009
    SUCCESS = 0x000E


def get_csbi_attributes(handle):
    import ctypes
    import struct
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    assert res

    (bufx, bufy, curx, cury, wattr,
    left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    return wattr

def reset():
    import ctypes
    STD_OUTPUT_HANDLE = -11
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    reset = get_csbi_attributes(handle)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)

def paint(color):
    import ctypes
    STD_OUTPUT_HANDLE = -11
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)