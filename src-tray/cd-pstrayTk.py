'''
　   pstrayをTkinterで使う
    
    トレイアイコンをバックグラウンド実行したい場合は
    「icon.run_detached()」を使う
    
    「run_detached」コードを見るとスレッドで動作している

'''
import tkinter as tk
from pystray import MenuItem, Icon
from PIL import Image, ImageDraw


# タイトルバーの×をクリックでは、プログラムは終了させない
# ウィンドウを非表示にする（タイトルバーからも消す）
def close_window():

    window.withdraw()       


#　pstrayアイコンとTkウィンドウの終了
#   遅延させてから終了しないとうまくいかない(window.after)
def quit_program(icon, item):

    icon.stop()

    # １秒になっているが、このPCでは1ミリ秒でも問題はない
    window.after(1, window.quit)



def menu1(icon, item):
    print("menu1")
    window.deiconify()   

def menu2(icon, item):
    print("menu2")
    close_window()
      
def menu3(icon, item):
    print("menu3")
    window.iconify() 





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

# アイコンをバックグラウンド実行
icon.run_detached()



#----------------------------------------------
#       Tkウィンドウ
#----------------------------------------------
window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', close_window)

window.withdraw()        #タイトルバーからも消す
window.mainloop()
