# import copy
# import sys
# '''
# #import PIL.Image
# #import numpy as np
# #import win32gui, win32ui, win32con
# #import time
# ##from PIL import Image
# #import math
# #import pytesseract
#
#
# class WindowCapture:
#
#     def __init__(self):
#         #pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\Ethan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
#         pass
#
#     class SotCaptureType:
#
#         FULL_SCREEN = 0
#         BOTTOM_TEXT = 1
#         BOTTOM_RIGHT_HAND = 2
#
#     def get_screenshot_2(self, isRgb=True, output_w_h=None, capture_type: int = SotCaptureType.FULL_SCREEN):
#         hwnd_target = self.get_sot_hwnd()  # 0x30dbe # Try SOT?
#
#         left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
#
#         # TODO this is wrong?
#         right = 3840
#         bot = 2160
#
#         w = right - left
#         h = bot - top
#
#         # if capture_type == self.SotCaptureType.FULL_SCREEN:
#         #     pass
#         # elif capture_type == self.SotCaptureType.BOTTOM_TEXT:
#         #     # In this type, we get the bottom 10% of the screen to save compute power
#         #     top = int((bot - top) * 0.9) + top
#         #     h = bot - top
#         # elif capture_type == self.SotCaptureType.BOTTOM_RIGHT_HAND:
#         #     # get the bot right quad
#         #     top = int((bot - top) * 0.5) + top
#         #     h = bot - top
#         #     left = int((right - left) * 0.5) + left
#         #     w = right - left
#
#         # win32gui.SetForegroundWindow(hwnd_target)
#         # time.sleep(1.0)
#
#         hdesktop = win32gui.GetDesktopWindow()
#         hwndDC = win32gui.GetWindowDC(hdesktop)
#         mfcDC = win32ui.CreateDCFromHandle(hwndDC)
#         saveDC = mfcDC.CreateCompatibleDC()
#
#         saveBitMap = win32ui.CreateBitmap()
#         saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
#
#         saveDC.SelectObject(saveBitMap)
#
#         result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
#
#         bmpinfo = saveBitMap.GetInfo()
#         bmpstr = saveBitMap.GetBitmapBits(True)
#
#         # get the image
#         im = Image.frombuffer(
#             'RGB',
#             (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#             bmpstr, 'raw', 'BGRX', 0, 1)
#
#         # cleanup
#         win32gui.DeleteObject(saveBitMap.GetHandle())
#         saveDC.DeleteDC()
#         mfcDC.DeleteDC()
#         win32gui.ReleaseDC(hdesktop, hwndDC)
#
#         # resize if needed
#         if output_w_h is not None:
#             im = im.resize((output_w_h[0], output_w_h[1]))
#
#         # modify colors if needed
#
#         if isRgb:
#             pass
#         else:
#
#             # im = im.convert('1') #THIS converts to 0-255 black white
#
#             white_threshold = 200
#             fn = lambda x: 0 if x > white_threshold else 255
#             im = im.convert('L').point(fn, mode='1')
#
#         return im
#
#     def __list_window_names(self):
#         def winEnumHandler(hwnd, ctx):
#             if win32gui.IsWindowVisible(hwnd):
#                 print(hex(hwnd), win32gui.GetWindowText(hwnd))
#
#         win32gui.EnumWindows(winEnumHandler, None)
#
#     def get_sot_hwnd(self):
#         return win32gui.FindWindow(None, "Sea of Thieves")
#
#     def get_screenshot_bottom_text(self, isRgb=True, output_w_h=(200, 100)):
#         return self.get_screenshot_2(isRgb, output_w_h, self.SotCaptureType.BOTTOM_TEXT)
#
#     def get_bt(self):
#         img = self.get_screenshot_2(False, (1920,1080), self.SotCaptureType.BOTTOM_TEXT)
#         img.save("temp_hand.png")
#         opened = PIL.Image.open("temp_hand.png", 'r')
#         #opened.show()
#         #text = pytesseract.image_to_string(opened, config='--psm 3').lower()
#         return "text"
#
#     def get_screenshot_right_hand(self, isRgb=True, output_w_h=(1920, 1080)):
#         return self.get_screenshot_2(isRgb, output_w_h, self.SotCaptureType.BOTTOM_RIGHT_HAND)
#
#     def get_text_from_screenshgot(self, img):
#         return ""
#         #return pytesseract.image_to_string(img, config='--psm 3').lower()
# '''