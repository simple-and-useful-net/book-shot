from pystray import Icon, Menu, MenuItem
import pystray
from PIL import Image, ImageDraw


def on_clicked(icon, item):
    print( item.text )
    pass
    



# サブメニューの作成
submenu = Menu(
    MenuItem('Sub1', on_clicked),
    MenuItem('Sub2', on_clicked),
    MenuItem('Sub3', on_clicked)
    )
menu = Menu(
    MenuItem('表示1', on_clicked),
    MenuItem('表示2', on_clicked),
    MenuItem('表示3', on_clicked),
    pystray.Menu.SEPARATOR,                 # 区切り線   
    MenuItem('サブメニュー', submenu),
    )

image = Image.new('RGB', (64, 64), color='blue')
icon = Icon( "test_icon", image, "My Tray Icon", menu)
icon.run()
