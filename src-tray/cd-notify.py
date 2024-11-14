
import tkinter as tk
from pystray import MenuItem, Icon
from PIL import Image, ImageDraw


'''
    システムアイコンを作成して表示する
    「run_detached」によりスレッドで実行させる
'''
image   = Image.new('RGB', (64, 64), color='red')
icon    = Icon("test_sys_icon", image)

# システムトレイ アイコンをバックグラウンド実行
icon.run_detached()



'''
    tkのウィンドウボタンによる
    system Icon　の通知テスト
'''
def on_clicked( text ):
    if text == "通知":
        icon.notify('Hello World!')
        # ~ icon.notify('Hello World!',"通知起動")

    if text == "通知終了":
        icon.remove_notification()


window = tk.Tk()

button = tk.Button( window, text="通知", command=lambda txt="通知": on_clicked(txt))
button.pack(pady=5)

button = tk.Button( window, text="通知終了", command=lambda txt="通知終了": on_clicked(txt))
button.pack(pady=5)


window.mainloop()

