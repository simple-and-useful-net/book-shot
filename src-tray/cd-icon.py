"""
------------------------------------------------------------------------

アイコンを変更する

アイコンをクリックするとアイコンのイメージが変わる

アイコンのイメージをトグル（ON・OFF）で切替える

右クリックのメニュは、1つのメニュー項目があるが非表示設定の為に表示されません

menu = Menu(
    MenuItem('',   on_clicked, default=True, visible=False),
    )


visible=Falseによりメニューは何も無くなります
------------------------------------------------------------------------
"""


from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# 表示アイコンの画像
# imageは青四角
# imageは赤四角
image = Image.new('RGB', (64, 64), color='blue')
image2= Image.new('RGB', (64, 64), color='red')



def on_clicked(icon, item):
    
    if item.default:
        if icon.icon == image2:
            icon.icon = image
        else:
            icon.icon = image2

# メニューを定義
menu = Menu(
    MenuItem('',on_clicked, default=True, visible=False),
    )



icon = Icon( name="test_icon", icon=image, title="My Tray Icon", menu=menu)
icon.run()
