from pystray import MenuItem, Icon
from PIL import Image, ImageDraw


def quit_program(icon, item):

    icon.stop()


def menu1(icon, item):
    print("menu1")

def menu2(icon, item):
    print("menu2")
      
def menu3(icon, item):
    print("menu3")



#----------------------------------------------
#       通知領域のアイコンを常駐させる
#----------------------------------------------
menu = (    
            MenuItem('アイコンクリック', menu1, default=True, visible=False),
            MenuItem('ウィンドウ表示', menu1),
            MenuItem('ウィンドウ消す', menu2),
            MenuItem('アイコン化',     menu3),
            MenuItem('終了',           quit_program)   )

image = Image.new('RGB', (64, 64), color='blue')
icon  = Icon("name", image, "title", menu)

# アイコンを実行
icon.run()





