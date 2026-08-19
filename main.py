"""
PhotoShow —— 一个极简 Kivy 示例应用

启动后显示一张照片，5 秒后自动退出（点击屏幕也可立即退出）。
把照片放在项目根目录并命名为以下任意一个即可被自动加载：
    photo.jpg / photo.png / app_image.png / image.jpg
如果没有找到照片，会自动生成一张占位图用于演示。
"""

import os
import struct
import zlib

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

# 显示时长（秒）
SHOW_SECONDS = 5

# 优先加载的照片文件名（按顺序查找）
PHOTO_CANDIDATES = ("photo.jpg", "photo.png", "app_image.png", "image.jpg")


def make_solid_png(path, width, height, rgb):
    """仅用标准库生成一张纯色 PNG，作为找不到照片时的占位图。"""
    def chunk(tag, data):
        block = tag + data
        return struct.pack(">I", len(data)) + block + struct.pack(
            ">I", zlib.crc32(block) & 0xFFFFFFFF
        )

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    row = b"\x00" + bytes(rgb) * width
    idat = chunk(b"IDAT", zlib.compress(row * height))
    iend = chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(signature + ihdr + idat + iend)


class PhotoApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        layout = FloatLayout()

        # 查找照片
        source = next((name for name in PHOTO_CANDIDATES if os.path.exists(name)), None)
        placeholder = False
        if source is None:
            source = "placeholder.png"
            make_solid_png(source, 480, 640, (70, 130, 180))  # 淡蓝色占位图
            placeholder = True

        image = Image(source=source, allow_stretch=True, keep_ratio=True)
        layout.add_widget(image)

        if placeholder:
            tip = Label(
                text="[b]占位图[/b]\n把 photo.jpg 放到项目目录即可显示你的照片",
                markup=True,
                font_size=18,
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=120,
                pos_hint={"center_x": 0.5, "center_y": 0.12},
            )
            layout.add_widget(tip)

        return layout

    def on_start(self):
        # 5 秒后自动关闭应用
        Clock.schedule_once(lambda dt: self.stop(), SHOW_SECONDS)

    def on_touch_down(self, touch):
        # 点击任意位置立即退出
        self.stop()
        return True


if __name__ == "__main__":
    PhotoApp().run()
