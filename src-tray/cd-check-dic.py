

from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# check状態を管理
states = {'check1': False, 'check2': True, 'check3': True}  


def on_clicked(icon, item):
    # item.textでメニューアイテムの名前を取得
    # check状態をトグルする
    states[item.text] = not states[item.text]

def is_checked(item):
    # メニューアイテムの状態を返す
    return states[item.text]

def disp_val(icon, item):
    print("states=", states)



menu = Menu(
    MenuItem('表示',  disp_val,visible=False, default=True),

    MenuItem('check1', on_clicked, checked=is_checked),
    MenuItem('check2', on_clicked, checked=is_checked),
    MenuItem('check3', on_clicked, checked=is_checked)
)

image = Image.new('RGB', (64, 64), color='blue')
icon = Icon("test_icon", image, "My Tray Icon", menu)
icon.run()
