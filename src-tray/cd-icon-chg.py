"""
------------------------------------------------------------------------

アイコンを変更する

アイコンをクリックするとアイコンのイメージが変わる

アイコンのイメージは トグルで変わる


------------------------------------------------------------------------
"""


from pystray import Icon, Menu, MenuItem
from PIL import Image


# 表示アイコンの画像
# imageは青四角
image = Image.new('RGB', (64, 64), color='blue')
image2= Image.new('RGB', (64, 64), color='red')


def on_clicked(icon, item):
    
    if item.text == "Item1":
        print("処理1をする")

    if item.text == "Item2":
        print("処理2をする")

    if item.text == "Item3":
        print("処理3をする")
        
    # ~ メニュー番号順に処理を作成したいなら、次のコードを使うと便利
    l = len(icon.menu.items)
    for i in range(l):
        # ~ print(i, icon.menu.items[i].text, item.text)
        if icon.menu.items[i].text == item.text:
            print("選択された項目,No",item.text, i)


# メニューを定義
menu = Menu(
    MenuItem('Item1',   on_clicked),
    MenuItem('Item2',   on_clicked),
    MenuItem('Item3',   on_clicked),
    )



# アイコンをトレイに表示
icon = Icon( name="test_icon", icon=image, title="My Tray Icon", menu=menu)
icon.run()
