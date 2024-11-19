"""
------------------------------------------------------------------------


アイコンクリック処理


    項目の各値を取得ができる
    
    print("item.text= ",        item.text)    
    print("item.default= ",     item.default)    
    print("item.visible= ",     item.visible)    

    設定はできない
        # item.visible=False  

------------------------------------------------------------------------
"""


from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw




def on_clicked(icon, item):

    print("アイコンがクリックされた")    
    print("item.text= ",        item.text)    
    print("item.default= ",     item.default)    

    # item.visible=False  
    print("item.visible= ",     item.visible)  


# メニューを定義
menu = Menu(
    MenuItem('メニュー項目1',on_clicked, default=True, visible=False),
    )



# 表示アイコンの画像
# imageは青四角
image = Image.new('RGB', (64, 64), color='blue')
icon = Icon( name="test_icon", icon=image, title="My Tray Icon", menu=menu)
icon.run()
