
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


"""
------------------------------------------------------------------------

メニュー項目を無効にする

メニュー項目に対して無効、有効（表示、非表示）するのが普通だが、できない模様
・メニューアイテムのプロパティは書き込みできない（エラー発生）
・
メニューを２つ作成切替える
Iconの「menu」プロパティを変更すると可能になる


------------------------------------------------------------------------
"""


def on_clicked(icon, item):
    
    if item.text == "表示":
        print("アイコンがクリックされた")
        

    if item.text == "項目無効":
        icon.menu = menu2
    elif item.text == "項目有効":           
        icon.menu = menu



# メニューを定義
menu = Menu(
    MenuItem('表示',      on_clicked,   enabled=True),
    MenuItem('項目無効',     on_clicked),
    )

menu2 = Menu(
    MenuItem('表示',      on_clicked, enabled=False),
    MenuItem('項目有効',    on_clicked),
    )



# システムトレイに表示するアイコン画像を作成
image = Image.new('RGB', (64, 64), color='blue')

icon = Icon( name="test_icon", icon=image, title="My Tray Icon", menu=menu)


# アイコンをタスクトレイに表示
icon.run()
