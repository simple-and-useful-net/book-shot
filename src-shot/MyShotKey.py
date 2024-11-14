
import  tkinter as tk
from    m_screenshot import screenshot

'''
キャプチャ範囲を指定する場合は、マウス移動だけでクリックしない事！
クリックするとフォーカスが移動されて、本プログラムが動作しなくなる
'''
x1,y1,x2,y2=0,0,0,0

'''
    左シフト
    シフトキーが押下されると呼ばれる関数
    現在のマウスの位置を取得してグローバル変数にセット
'''
def on_shift_L(event):
        global x1,y1,x2,y2
        
        x1 = root.winfo_pointerx()
        y1 = root.winfo_pointery()
        label.config( text= f"x1,y1 -  x2,y2 = ({x1}, {y1}) - ({x2}, {y2})" )
        print(x1,y1,x2,y2)

#   右シフト
def on_shift_R(event):
        global x1,y1,x2,y2
        
        x2 = root.winfo_pointerx()
        y2 = root.winfo_pointery()
        label.config( text= f"x1,y1 -  x2,y2 = ({x1}, {y1}) - ({x2}, {y2})" )
        print(x1,y1,x2,y2)


def shot(x1,y1,x2,y2):
    root.after( 5000, lambda: screenshot(x1,y1,x2,y2) )


root = tk.Tk()
root.geometry("300x200")

label_help1= tk.Label(root, text="左上座標は、マウス移動して左シフト")
label_help2= tk.Label(root, text="右下座標は、マウス移動して右シフト")

#座標位置の表示
label     = tk.Label(root, text="Press the Shift Key")
# screen shot button
# ~ st_button = tk.Button(root, text="Shot", command=lambda: screenshot(x1,y1,x2,y2) )
st_button = tk.Button(root, text="Shot", command=lambda: shot(x1,y1,x2,y2) )

label_help1.pack()
label_help2.pack()
label.pack()
st_button.pack()

# シフトキー押下時に関数を呼び出す
root.bind('<KeyPress-Shift_L>', on_shift_L)
root.bind('<KeyPress-Shift_R>', on_shift_R)

root.mainloop()
