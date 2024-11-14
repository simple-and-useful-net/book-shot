'''
------------------------------------------------------------------------
    ラジオボタン
------------------------------------------------------------------------
'''

from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


food = "カレー"

def set_state(v):
    def inner(icon, item):
        global food
        food = v
    return inner

def get_state(v):
    def inner(item):
        return food == v
    return inner

def disp_val(icon, item):
    print("food=", food)


menu = Menu(
        MenuItem('表示',  disp_val,visible=False, default=True),

        MenuItem('カレー', set_state("カレー"),       checked=get_state("カレー"), radio=True),
        MenuItem('ラーメン', set_state("ラーメン"),   checked=get_state("ラーメン"), radio=True),
        MenuItem('やきそば', set_state("やきそば"),   checked=get_state("やきそば"), radio=True),
)

# アイコンの生成と実行
image = Image.new('RGB', (64, 64), color='blue')
icon = Icon('test', icon=image, menu=menu)
icon.run()

