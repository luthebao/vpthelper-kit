import os, subprocess
from ctypes import *
from ctypes.wintypes import *
from ctypes import windll

import uuid, base64, math
import numpy as np
from urllib.parse import urlparse, parse_qs
import random, time, platform
import win32process, win32api, win32con, win32gui, win32ui, sys
import cv2
import PIL.Image
import re, datetime, threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import requests
import functools
import psutil
import pymem as mem
import pymem.process as memprocess
import clr
import json

def Mbox(title, text, style):
    '''
    ##  Styles:
    ##  0 : OK
    ##  1 : OK | Cancel
    ##  2 : Abort | Retry | Ignore
    ##  3 : Yes | No | Cancel
    ##  4 : Yes | No
    ##  5 : Retry | No 
    ##  6 : Cancel | Try Again | Continue
    '''
    return windll.user32.MessageBoxW(0, text, title, style)

MAPS_LIST = {
    1: 'Xuất Vân Thôn',
    2: 'Đông Xuất Vân',
    3: 'Vân Đài',
    4: 'Thiện Tĩnh Địa',
    5: 'Lê Dương Thôn',
    6: 'Lê Dương Nam',
    7: 'Quân Cổ Đạo',
    8: 'Tháp Khắc Nguyên',
    9: 'Đông Huyền Thành',
    10: 'Tinh Linh Thành',
    11: 'Linh Vũ Tộc',
    12: 'Bàn Địa Tộc',
    13: 'Liêu Vân Tộc',
    14: 'Hư Không Mạc',
    15: 'Lê Dương Bắc',
    16: 'Ngọc Phong Lâm',
    17: 'Lê Dương Đảo',
    18: 'Kỳ Thạch Địa',
    19: 'Linh Lan',
    20: 'Thánh Ước Địa',
    21: 'Chỉ Phong Cốc',
    22: 'Tuyết Lâm',
    23: 'Phục Ma Cốc',
    24: 'Hộ Chi Địa',
    25: 'Lưu Hỏa Tộc',
    26: 'Quang Bình Nguyên',
    27: 'Trầm Thụy Lâm',
    28: 'Vân Lộc Sơn',
    29: 'Mê Quang Tự',
    30: 'Quyến Cố Thành',
    31: 'Tiên Lạp Thành',
    32: 'Thiên Khung Tộc',
    33: 'Lạp Tuyết Địa',
    34: 'Anh Vũ Cảnh',
    35: 'Băng Tuyết Nguyên',
    36: 'Thần Di Cảnh',
    37: 'Cổ Thành',
    38: 'Bàng Bối Thành',
    39: 'Huyền Lâm Tộc',
    40: 'Thiên Lục Châu',
    41: 'Kỵ Bình Nguyên',
    42: 'Cổ Đạo',
    43: 'Đoạn Cốc',
    44: 'Đăng Vân Địa',
    45: 'Tử Mộng Cảnh',
    46: 'Kiếm Hồn Cảnh',
    47: 'Không Gian Ma Chiến',
    48: 'Trấn Ma Tháp',
    49: 'Bang Hội',
    50: 'Khoáng Động',
    51: 'Bảo Tàng Mật Thất',
    52: 'Tầng 50 Trấn Ma Tháp',
    53: 'Tân Tuyết Địa',
    54: 'Chiến Trường Bang Hội',
    55: 'Điêu Linh Thôn',
    56: 'Mị Hoặc Lâm',
    57: 'Nông Trường Số 1',
    58: 'Nông Trường Số 2',
    59: 'Giác Đấu Đông Huyền',
    60: 'Chiến Trường Achilles',
    61: 'Tử Tức Đảo',
    62: 'Bản đồ mới ++2',
    63: 'Lễ Đường Hôn Lễ Cao Cấp',
    64: 'Lễ Đường Hôn Lễ Thông Thường',
    65: 'Lễ Đường Hôn Lễ Quý Giá',
    66: 'Khu Hoang Mạc',
    67: 'Vĩnh Dạ Cảng',
    68: 'Phong Bạo Cốc',
    69: 'Phụ Bản Quỷ Hút Máu',
    70: 'Mã Thạch Tuyết',
    71: 'Thiên Đường Thần Thánh',
    72: 'Đấu Trường Bánh Kem',
    73: 'Chiến Trường Dũng Sĩ',
    75: 'Đấu Trường Tranh Bá',
    76: 'Quảng Trường Kỳ Thạch',
    77: 'Phòng Trò Chuyện',
    78: 'Chiến Trường Tula',
    79: 'Hành Lang Vô Tận  - Khởi Trình',
    80: 'Hành Lang Vô Tận  - Hỏa Diệm',
    81: 'Hành Lang Vô Tận  - Băng Lửa',
    82: 'Hành Lang Vô Tận  - Quyết Định',
    83: 'Hành Lang Vô Tận  - Đoạn Không',
    84: 'Hành Lang Vô Tận  - Địa Ngục',
    85: 'Hành Lang Vô Tận  - Thâm Uyên',
    86: 'Hành Lang Vô Tận  - Luân Hồi',
    87: 'Ảo Địa Tiêu Trừ',
    88: 'Thiên Không Thành',
    101: 'Đấu Trường Đoạt Bảo',
    102: 'Nơi Thi Câu Cá',
    110: 'Huyết Sắc Cổ Bích',
    500: 'Tầng 1 Kho Báu Đại Mạc',
    501: 'Tầng 2 Kho Báu Đại Mạc',
    502: 'Tầng 3 Kho Báu Đại Mạc',
    503: 'Tầng 4 Kho Báu Đại Mạc',
    504: 'Tầng 5 Kho Báu Đại Mạc',
    505: 'Tầng 1 Lục Tiên Cảnh',
    506: 'Tầng 2 Lục Tiên Cảnh',
    507: 'Tầng 3 Lục Tiên Cảnh',
    508: 'Tầng 4 Lục Tiên Cảnh',
    509: 'Tầng 5 Lục Tiên Cảnh',
    510: 'Tầng 1 Lang Huyệt Động',
    511: 'Tầng 2 Lang Huyệt Động',
    512: 'Tầng 3 Lang Huyệt Động',
    513: 'Tầng 3 Lang Huyệt Động',
    514: 'Tầng 4 Lang Huyệt Động',
    515: 'Ảo Ma Tháp',
    516: 'Tầng 1 Không Gian Đa Chiều',
    517: 'Tầng 1 Liệt Diễm Thâm Uyên',
    518: 'Tầng 2 Liệt Diễm Thâm Uyên',
    519: 'Tầng 3 Liệt Diễm Thâm Uyên',
    520: 'Tầng 4 Liệt Diễm Thâm Uyên',
    521: 'Tầng 1 Thế Giới Hải Dương',
    522: 'Tầng 2 Thế Giới Hải Dương',
    523: 'Tầng 3 Thế Giới Hải Dương',
    524: 'Tầng 4 Thế Giới Hải Dương',
    525: 'Thành Phố Chìm',
    526: 'Quỷ Môn Quan',
    527: 'Học Viện Đông Huyền',
    528: 'Đảo Thần Bí',
    529: 'Đông Võ Đài Đông Huyền',
    530: 'Tây Võ Đài Đông Huyền',
    531: 'Tầng 5 Thế Giới Hải Dương',
    532: 'Hội Trường Phân Chia',
    533: 'Ký Ức Tinh Linh Thành',
    534: 'Sào Huyệt Vua Người Tuyết',
    535: 'Phòng Chờ 1',
    536: 'Phòng Chờ 2',
    537: 'Phòng Chờ 3',
    538: 'Ào Cảnh Tầng 1',
    539: 'Ào Cảnh Tầng 2',
    540: 'Ào Cảnh Tầng 3',
    541: 'Ào Cảnh Tầng 4',
    542: 'Ào Cảnh Tầng 5',
    543: 'Ào Cảnh Tầng 6',
    544: 'Ào Cảnh Tầng 7',
    545: 'Ào Cảnh Tầng 8',
    546: 'Ào Cảnh Tầng 9',
    547: 'Ào Cảnh Tầng 10',
    548: 'Ào Cảnh Tầng 11',
    549: 'Ào Cảnh Tầng 12',
    550: 'Ào Cảnh Tầng 13',
    551: 'Ào Cảnh Tầng 14',
    552: 'Ào Cảnh Tầng 15',
    553: 'Ào Cảnh Tầng 16',
    554: 'Ào Cảnh Tầng 17',
    555: 'Ào Cảnh Tầng 18',
    556: 'Ào Cảnh Tầng 19',
    557: 'Ào Cảnh Tầng 20',
    558: 'Không Gian Luân Hồi',
    559: 'Không Gian Tín Niệm',
    560: 'Không Gian Vận Mệnh',
    561: 'Không Gian Dũng Khí',
    562: 'Tầng 1 Không Gian Mê Đồ',
    563: 'Tầng 2 Không Gian Mê Đồ',
    564: 'Tầng 3 Không Gian Mê Đồ',
    565: 'Tầng 4 Không Gian Mê Đồ',
    566: 'Tầng 5 Không Gian Mê Đồ',
    567: 'Tầng 6 Không Gian Mê Đồ',
    568: 'Tầng 7 Không Gian Mê Đồ',
    569: 'Tầng 8 Không Gian Mê Đồ',
    570: 'Tầng 9 Không Gian Mê Đồ',
    571: 'Tầng 10 Không Gian Mê Đồ',
    572: 'Tầng 11 Không Gian Mê Đồ',
    573: 'Tầng 12 Không Gian Mê Đồ',
    574: 'Tầng 13 Không Gian Mê Đồ',
    575: 'Tầng 14 Không Gian Mê Đồ',
    576: 'Tầng 15 Không Gian Mê Đồ',
    577: 'Tầng 2 Không Gian Đa Chiều',
    578: 'Rừng Rậm Số',
    579: 'Thế Giới Chân Lý',
    580: 'Ác Ma Đảo',
    581: 'Hàng Lang Nguyên Tố',
    582: 'Vùng Đất Cạm Bẫy',
    583: 'Không Gian Bí Mật',
    584: 'Hành Lang Nguy Hiểm',
    585: 'Tiểu Đảo Cô Lập',
    586: 'Tháp Trí Tuệ',
    587: 'Không Gian Tĩnh Mịch',
    588: 'Thủ Vệ Viễn Cổ',
    2000: 'Cạnh Kỹ Trường',
    2001: 'Tầng 1 Mê Huyễn Động',
    2002: 'Tầng 2 Mê Huyễn Động',
    2003: 'Tầng 3 Mê Huyễn Động',
    2004: 'Tầng 4 Mê Huyễn Động',
    2005: 'Chu Ma Điện',
    2006: 'Địa Ngục Dung Nham',
    2007: 'Mê Trận',
    2008: 'Mê Trận',
    2009: 'Mê Trận',
    2010: 'Tầng 1 Sào Huyệt Cương Thi',
    2011: 'Tầng 2 Sào Huyệt Cương Thi',
    2012: 'Tầng 3 Sào Huyệt Cương Thi',
    2013: 'Xuất Vân Trong Mộng',
    2014: 'Vân Đài Trong Mộng',
    2015: 'Chiến Trường Vĩnh Dạ',
    140104: 'Mật Đạo 3',
    140105: 'Mật Đạo 2',
    140106: 'Mật Đạo 1'
}


IMAGES_LIST = {
    "tudo": "iVBORw0KGgoAAAANSUhEUgAAABUAAAALCAIAAAAfqVEqAAAB90lEQVQoFaXBQUhTYRwA8P8H8qbmw8OHjjdwsULMlgx9f+gV6CHw8GA8BP8ievJdPImI5EX4TrsESoR8hyCoTnUZGtGKUuoQwg7jxbxIeVPoz5rjNXOXMVAYPBCiU7+fuGiuQxsS9z7I1D+XS3kLibtuDZj3huEvv158KuUtiAjb8+Efum5fN8fvQKQVnodv9i+aLQBwMoZWEomF7fn9y1ON0tFI40gricTX7qdHGkdaSSTuX56CSPVp4e6w0EpCBImF7fnxtZnfb4ujnRWtJBLHhgZGOytaSSSOr81AW6t2Vnv+sZS3Xr07f/zyj5MxtJJILGzPDxYnUnuHrlnXSiJxeKPPNetaSSQOFiegLbV36Jp1rSQSA4CTMbSSSCxszw9WJlOFA7c71EoicTgYd7tDrSQSByuT0Db2ZHd1wZzP9iBxOBh3u0OtJBIL2/OD9WxqJ3CNU60kEgOAkzG0kkgcrGehLbUTuMapVhKJAcDJGFpJJBa25we56fjX79OVH1rJpVytWG6W8hYAIHGQm4a2WPUsvbVbyltLuVqx3Nze6ksmOpBY2J4fbM7FKvX0xvvtrb5kogMAjn+2kokOJA425yAy9vD16oI5n+2BCBKL5Majk1kHAKzCN+vDAVxRHR86mXUg0ls+vvnsC1xRHR8SorIP/+ES5tzLb08tRO4AAAAASUVORK5CYII=",
}

class Convert:
    def __init__(self, img: any) -> None:
        self.img = img
    
    def img_to_b64(self):
        _, im_arr = cv2.imencode('.png', self.img)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        return str(im_b64.decode("utf-8"))

class HelperKit:
    def __init__(self, title: str) -> None:
        self.title = title
        self.pid = None
        self.mem = None
        self.game_module = None
        self.big = 9000
        self.small = 8999
        self.FLASH_POINTER = (0x508544)
        self.OFFSET_FPS = [0x34, 0x2E4, 0x5C, 0x208]
        self.OFFSET_MAIN = [0x3C, 0x10, 0x138, 0x7C, 0x4, 0x144]
        self.hWnd = win32gui.FindWindow(None, self.title)
        
        self.reconnect()
        
        self.OFFSET_X = self.OFFSET_MAIN + [0x150]
        self.OFFSET_Y = self.OFFSET_MAIN + [0x108]
        self.OFFSET_MAP = self.OFFSET_MAIN + [0x1D0]
        self.OFFSET_LEVEL = self.OFFSET_MAIN + [0x40]
        self.OFFSET_INBATTLE = self.OFFSET_MAIN + [0x70]
        self.OFFSET_BAY = self.OFFSET_MAIN + [0x3C]
        self.OFFSET_VIP = self.OFFSET_MAIN + [0x1C8]
        self.OFFSET_MANA = self.OFFSET_MAIN + [0xD0]
             
    def test(self):
        return self.mem.read_double(self.getPointerAddress(self.OFFSET_MAIN))

    def reconnect(self):
        try: 
            self.pid = win32process.GetWindowThreadProcessId(win32gui.FindWindow(None, self.title))[-1]
            self.mem = mem.Pymem(self.pid)
            self.game_module = memprocess.module_from_name(self.mem.process_handle, "flash.exe").lpBaseOfDll
            try:
                self.FLASH_POINTER = (0x508544)
                self.OFFSET_FPS = [0x34, 0x2E4, 0x5C, 0x208]
                self.OFFSET_MAIN = [0x3C, 0x10, 0x138, 0x7C, 0x4, 0x144]
                print(self.FLASH_POINTER, self.getfps())
            except:
                self.FLASH_POINTER = (0x51B448)
                self.OFFSET_FPS = [0x78, 0x24, 0x5C, 0x208]
                self.OFFSET_MAIN = [0xC0, 0x44, 0x2B8, 0x78, 0xA4, 0x144]
                print(self.FLASH_POINTER, self.getfps())
        except:
            self.reconnect()

    def close_mem(self):
        self.mem.close_process()
    
    def getPointerAddress(self, offsets=[]):
        h_process = windll.kernel32.OpenProcess(win32con.PROCESS_VM_READ, False, self.pid)
        data = c_uint(0)
        bytesRead = c_uint(0)
        current_address = self.game_module + self.FLASH_POINTER
        for offset in offsets:
            windll.kernel32.ReadProcessMemory(h_process, current_address, byref(data), sizeof(data), byref(bytesRead))
            current_address = data.value + offset
        windll.kernel32.CloseHandle(h_process)
        return current_address
    
    def distanceto(self, Cord1):
        if len(Cord1) != 2:
            return -1
        return math.sqrt(math.pow(Cord1[0] - self.getcord()[0], 2) + math.pow(Cord1[1] - self.getcord()[1], 2))

    def getcord(self) -> list[float]:
        return [
            self.mem.read_double(self.getPointerAddress(self.OFFSET_X)),
            self.mem.read_double(self.getPointerAddress(self.OFFSET_Y))
        ]
    
    def getmap(self) -> int:
        return int(self.mem.read_double(self.getPointerAddress(self.OFFSET_MAP)))
    
    def getlevel(self) -> int:
        return int(self.mem.read_int(self.getPointerAddress(self.OFFSET_LEVEL)))
    
    def inbattle(self) -> bool:
        return int(self.mem.read_int(self.getPointerAddress(self.OFFSET_INBATTLE))) == 1
    
    def getfps(self) -> int:
        return int(self.mem.read_double(self.getPointerAddress(self.OFFSET_FPS)))
    
    def isfly(self) -> bool:
        return int(self.mem.read_int(self.getPointerAddress(self.OFFSET_BAY))) == 2
    
    def getvip(self) -> int:
        return int(self.mem.read_double(self.getPointerAddress(self.OFFSET_VIP)))
    
    def getmana(self) -> int:
        return int(self.mem.read_double(self.getPointerAddress(self.OFFSET_MANA)))

    def setcord(self, x: float, y: float) -> bool:
        try:
            for _ in range(50):
                self.mem.write_double(self.getPointerAddress(self.OFFSET_X), x * 1.0)
                self.mem.write_double(self.getPointerAddress(self.OFFSET_Y), y * 1.0)
            return True
        except Exception as e:
            print("setcord err", e)
            return False
        
    def setbattle(self, inbattle: bool) -> bool:
        try:
            self.mem.write_int(self.getPointerAddress(self.OFFSET_INBATTLE), 1 if inbattle else 0)
            return True
        except Exception as e:
            print("setbattle err", e)
            return False
    
    def setfps(self, value: int) -> bool:
        try:
            self.mem.write_double(self.getPointerAddress(self.OFFSET_FPS), float(value))
            return True
        except Exception as e:
            print("setFPS err", e)
            return False
        
    def setfly(self, isfly: bool) -> bool:
        try:
            self.mem.write_int(self.getPointerAddress(self.OFFSET_BAY), 2 if isfly else 0)
            return True
        except Exception as e:
            print("setfly err", e)
            return False
    
    def setfly1(self, state: int) -> bool:
        try:
            self.mem.write_int(self.getPointerAddress(self.OFFSET_BAY), state)
            return True
        except Exception as e:
            print("setfly err", e)
            return False
        
    def SearchMemory1(self, value, type:str = "string" or "int" or "double", hard: bool = True):
        try:
            clr.AddReference(f'{os.getcwd()}/lib/Scan.dll')
            from Scan import ScanAddress
            list2 = ScanAddress(str(self.pid), str(value), type, "hard" if hard else "normal").GetListAddressArrayByte().Result
            return [x for x in list2]
        except Exception as e:
            print("SearchInt err", e)
            return [] 

    def SearchMemory(self, value, type:str = "string" or "int" or "double", hard: bool = True):
        try:
            clr.AddReference(f'{os.getcwd()}/lib/Scan.dll')
            from Scan import ScanAddress
            ttt = datetime.datetime.now()
            scaninit = ScanAddress(str(self.pid), str(value), type, "hard" if hard else "normal")
            virtualMemorySize64 = 0
            if hard:
                virtualMemorySize64 = scaninit.process.PeakVirtualMemorySize
            else:
                virtualMemorySize64 = scaninit.process.VirtualMemorySize64
            num = (virtualMemorySize64 / self.big - self.small) / self.big + 1
            tasks: list[threading.Thread] = []
            results = []

            def scan1(num1, num2):
                for x in scaninit.GetListAddressArrayByteFromTo(num1, num2):
                    results.append(x)

            for i in range(int(num)):
                num1 = self.big * i
                num2 = self.big * i + self.small
                tasks.append(threading.Thread(target=scan1, args=(num1, num2)))
            for x in tasks:
                x.start()
            for x in tasks:
                x.join()
            print(datetime.datetime.now() - ttt)
            return results
        except Exception as e:
            print(f"SearchMemory {type} err", e)
            return []
        
    def ReadString(self, address, length: int = 50) -> str:
        result = ""
        for i in range(1, length):
            try:
                arr = self.mem.read_bytes(address, i)
                result = arr.decode(errors="replace")
            except Exception as e:
                print("ReadString err", e)
        return result

    def press_number(self, strings, delay=0.01):
        hWnd = win32gui.FindWindow(None, self.title)
        letter = list(strings)
        for i in letter:
            time.sleep(delay)
            if i == "0":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x30, 0)
            elif i == "1":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x31, 0)
            elif i == "2":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x32, 0)
            elif i == "3":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x33, 0)
            elif i == "4":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x34, 0)
            elif i == "5":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x35, 0)
            elif i == "6":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x36, 0)
            elif i == "7":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x37, 0)
            elif i == "8":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x38, 0)
            elif i == "9":
                win32api.PostMessage(hWnd, win32con.WM_CHAR, 0x39, 0)

    def click(self, num: int, x: int, y: int):
        hWnd = win32gui.FindWindow(None, self.title)
        lParam = win32api.MAKELONG(x, y)
        for n in range(num):
            win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
    
    def tesc(self):
        hWnd = win32gui.FindWindow(None, self.title)
        for _ in range(3):
            win32gui.SendMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
            win32gui.SendMessage(hWnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
    
    def capture(self):
        try: 
            hwnd = win32gui.FindWindow(None, self.title)
            # Change the line below depending on whether you want the whole window
            # or just the client area. 
            #left, top, right, bot = win32gui.GetClientRect(hwnd)
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            w = right - left
            h = bot - top
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            # Change the line below depending on whether you want the whole window
            # or just the client area. 
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im = PIL.Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        except:
            return None

    def printc(self):
        hwnd = win32gui.FindWindow(None, self.title)
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = PIL.Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        return im
    
    def printh(self):
        hwnd = win32gui.FindWindow(None, self.title)
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = PIL.Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        return im

    def ImgSearch(self, image_path, precision: float = 0.8, version: int = 1) -> list[int]:
        try:
            im = self.printc() if version == 1 else self.printh()
            img_rgb = np.array(im)
            # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            # template = cv2.imread(image, 0)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            template = cv2.imread(image_path)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < precision:
                return [-1, -1]
            return max_loc
        except: return [-1, -1]

    def ImgSearchB64(self, img_base64, precision: float = 0.8, version: int = 1) -> list[int]:
        try:
            im = self.printc() if version == 1 else self.printh()
            img_rgb = np.array(im)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR) # old: COLOR_BGR2GRAY
            im2 = cv2.imdecode(np.frombuffer(base64.b64decode(img_base64), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
            # template = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
            template = im2
            # template = cv2.cvtColor(np.array(cv2.imdecode(np.frombuffer(base64.b64decode(img_base64), dtype=np.uint8), flags=cv2.IMREAD_COLOR)), cv2.COLOR_BGR2GRAY)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < precision:
                return [-1, -1]
            return max_loc
        except Exception as e:
            print(e) 
            return [-1, -1]

    def ImgSearch_area(self, image_path, cord1: list[int], cord2: list[int], precision: float = 0.8, version: int = 1) -> list[int]:
        try:
            im = self.printc() if version == 1 else self.printh()
            im = im.crop((cord1[0], cord1[1], cord2[0], cord2[1]))
            img_rgb = np.array(im)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(image_path, 0)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < precision:
                return [-1, -1]
            return max_loc
        except: return [-1, -1]
    
    def ImgSearchB64_area(self, img_base64, cord1: list[int], cord2: list[int], precision: float = 0.8, version: int = 1) -> list[int]:
        try:
            im = self.printc() if version == 1 else self.printh()
            im = im.crop((cord1[0], cord1[1], cord2[0], cord2[1]))
            img_rgb = np.array(im)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            im2 = cv2.imdecode(np.frombuffer(base64.b64decode(img_base64), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
            template = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < precision:
                return [-1, -1]
            return max_loc
        except: return [-1, -1]
    
    def ImgSearchAll(self, image_path, precision: float = 0.8, version: int = 1) -> list[list[int]]:
        result = []
        try:
            im = self.printc() if version == 1 else self.printh()
            img_rgb = np.array(im)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(image_path, 0)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= precision)
            for pt in zip(*loc[::-1]): 
                result.append(pt)
            return result
        except: return result

    def ImgSearchB64All(self, img_base64, precision: float = 0.8, version: int = 1) -> list[int]:
        result = []
        try:
            im = self.printc() if version == 1 else self.printh()
            img_rgb = np.array(im)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR) # old: cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            im2 = cv2.imdecode(np.frombuffer(base64.b64decode(img_base64), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
            template = im2 # old: cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
            assert not isinstance(template,type(None)), 'image not found'
            template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= precision)
            for pt in zip(*loc[::-1]): 
                result.append(pt)
            return result
        except: return result

    def click_img(self, image_path, precision: float = 0.8, version: int = 1) -> int:
        img = cv2.imread(image_path)
        height, width, channels = img.shape
        pos = self.ImgSearch(image=image_path, precision=precision, version=version)
        if pos[0] > 0:
            if version == 1:
                self.click(1, pos[0] + round(width/2) - 8, pos[1] + round(height/2) - 30)
            else:
                self.click(1, pos[0] + round(width/2), pos[1] + round(height/2))
            return 1
        else:
            return 0
    
    def click_img2(self, image_path, clicknum=1, precision: float = 0.8, version: int = 1) -> int:
        img = cv2.imread(image_path)
        height, width, channels = img.shape
        pos = self.ImgSearch(image=image_path, precision=precision, version=version)
        if pos[0] > 0:
            if version == 1:
                self.click(clicknum, pos[0] + round(width/2) - 8, pos[1] + round(height/2) - 30)
            else:
                self.click(clicknum, pos[0] + round(width/2), pos[1] + round(height/2))
            return 1
        else:
            return 0
    
    def click_img_b64(self, image, num = 1, precision: float = 0.8, version: int = 1) -> int:
        img = cv2.imdecode(np.frombuffer(base64.b64decode(image), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        height, width, channels = img.shape
        pos = self.ImgSearchB64(img_base64=image, precision=precision, version=version)
        if pos[0] > 0:
            if version == 1:
                self.click(num, pos[0] + round(width/2) - 8, pos[1] + round(height/2) - 30)
            else:
                self.click(num, pos[0] + round(width/2), pos[1] + round(height/2))
            return 1
        else:
            return 0

    def reloadtele(self, x=1000, y=1000, reload_loop=3, click_num=3):
        time.sleep(0.5)
        ## start reload tele
        self.tesc()
        for _ in range(reload_loop):
            if self.ImgSearchB64(IMAGES_LIST["tudo"])[0] > 0:
                self.setcord(float(x), float(y))
                time.sleep(0.5)
                for _ in range(click_num):
                    self.click(1, 181, 239)
                    time.sleep(0.1)
                    self.click(1, 181, 239)
                    time.sleep(0.3)
                break
            else:
                self.click(1, 713, 652) # mo nhan vat expand
                time.sleep(0.2)
        self.tesc()

    def hide(self):
        win32gui.ShowWindow(self.hWnd, win32con.SW_MINIMIZE)
        
    def show(self):
        win32gui.ShowWindow(self.hWnd, win32con.SW_SHOWDEFAULT)

class AccountInfo:
    def __init__(self, link: str = "", username: str = "", account_path:str = "./acc.txt") -> None:
        self.CREATE_NO_WINDOW = 0x08000000
        self.link = link
        self.username = username
        self.account_path = account_path
        if len(username) == 0:
            self.username = self.getuser(link)
        elif len(link) == 0:
            self.link = self.getlink(username)
        self.password = self.getpass(self.link)
        self.server = self.getserver(self.link)
        self.originallink = f"https://s3-vuaphapthuat.goplay.vn/s/{self.server}/GameLoaders.swf?user={self.getuser(self.link)}&pass={self.password}"

    def getuser(self, link: str) -> str:
        parsed_url = urlparse(link)
        if "user" in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)['user'][0]
        else:
            return "###"
    
    def getpass(self, link: str) -> str:
        parsed_url = urlparse(link)
        if "pass" in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)['pass'][0]
        else:
            return "###"
    
    def getnhanvat(self) -> int:
        parsed_url = urlparse(self.link)
        if "nv" in parse_qs(parsed_url.query):
            return int(parse_qs(parsed_url.query)['nv'][0])
        else:
            return 1
    
    def getserver(self, link: str) -> str:
        if re.search(r"s/s\d{1,2}", link):
            return re.search(r"s/s\d{1,2}", link).group(0).replace(r"s/", "")
        else:
            return "s32"
        
    def getlink(self, user: str) -> str:
        with open(self.account_path, "r") as f_2:
            l_acc2 = f_2.readlines()
        l_acc2 = [x.strip() for x in l_acc2]
        acc_to_del = "###"
        for i in range(len(l_acc2)):
            if AccountInfo(link=l_acc2[i]).username == user:
                acc_to_del = l_acc2[i]
        return acc_to_del
    
    def logsmall(self):
        subprocess.Popen("./flash.exe " + self.originallink)
        while True:
            findh = win32gui.FindWindow(None, 'Adobe Flash Player 10')
            if findh != 0:
                win32gui.SetWindowText(findh, self.username)
                break
            else:
                time.sleep(0.01)
    
    def logbig(self):
        subprocess.Popen("./flash.exe " + self.originallink + "&isExpand=true")
        while True:
            findh = win32gui.FindWindow(None, 'Adobe Flash Player 10')
            if findh != 0:
                win32gui.SetWindowText(findh, self.username)
                break
            else:
                time.sleep(0.01)
    
    def flash(self):
        subprocess.call('taskkill /fi "WINDOWTITLE eq Adobe Flash Player 10"', creationflags=self.CREATE_NO_WINDOW)
        subprocess.call('taskkill /fi "WINDOWTITLE eq "'+ self.username, creationflags=self.CREATE_NO_WINDOW)
        while True:
            findh = win32gui.FindWindow(None, self.username)
            if findh != 0:
                subprocess.call('taskkill /fi "WINDOWTITLE eq "'+ self.username, creationflags=self.CREATE_NO_WINDOW)
                time.sleep(0.3)
            else:
                break
        time.sleep(0.2)
        subprocess.Popen("./flash.exe " + self.originallink)
        while True:
            findh = win32gui.FindWindow(None, 'Adobe Flash Player 10')
            if findh != 0:
                win32gui.SetWindowText(findh, self.username)
                break
            else:
                time.sleep(0.01)
                
                
                