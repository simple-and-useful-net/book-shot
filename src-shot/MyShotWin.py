'''
------------------------------------------------------------------------
ウィンドウを使ってキャプチャ

    ウィンドウ内の範囲をキャプチャします
    ウィンドウ内の構成は、キャプチャ範囲とボタン

        Dispボタン：    キャプチャ内容を表示（保存あり）
        Captureボタン： ファイルに保存のみ    
        
------------------------------------------------------------------------
'''
import tkinter as tk
from  m_screenshot  import screenshot


'''
------------------------------------------------------------------------
ウィンドウを使ってキャプチャー

作成されたウィンドウ内をキャプチャーする

    ぐろーばる

------------------------------------------------------------------------
'''
def capture( win_disp=False ):
    # Canvasのグローバル座標（左上の位置）
    x1 = canvas.winfo_rootx()
    y1 = canvas.winfo_rooty()
    
    # Canvasの幅と高さ
    x2 = x1 + canvas.winfo_width()
    y2 = y1 + canvas.winfo_height()

    fn = screenshot(  x1, y1, x2, y2, disp=win_disp )
    root.title( f"{fn}" )    


'''
------------------------------------------------------------------------
    ウインドウサイズが小さくなった場合は、一度アイコン化する
    （ウィンドウ内を透明にしているので、フォーカスが移ってしまう）

------------------------------------------------------------------------
'''
def win_resize(_):

    global previous_width, previous_height

    # ウインドウサイズを取得
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    
    # ウインドウサイズが小さくされたかどうかを判定
    if current_width < previous_width or \
        current_height < previous_height:

            print("ウィンドウが小さくなった")
            root.iconify()                      # 最小化
            root.deiconify()                    # 復元


    # サイズを保存
    previous_width = current_width
    previous_height = current_height




"""
------------------------------------------------------------------------
    メイン処理

    transparentcolor（透明色）を指定して、その色を
------------------------------------------------------------------------
"""
透明色="green"

root = tk.Tk()
root.title( "Capture" )    
root.geometry( f"{400}x{300}+{100}+{100}" )
root.attributes('-topmost', True)
root.wm_attributes("-transparentcolor", 透明色)
root.bind("<Configure>",        win_resize)


# 余白サイズ
padding_x = 5
padding_y = 5

# Canvasの作成
canvas = tk.Canvas( root, bg=透明色 )
canvas.grid(row=0, column=0, padx=padding_x, pady=(0, padding_y), sticky="nsew" )  # 余白を持たせて配置


# Frame作成
bottom_frame = tk.Frame(root, bg="lightgray")
bottom_frame.grid(row=1, column=0, padx=padding_x, pady=(0, padding_y), sticky="ew")  # 余白を持たせて配置

# Frame内に部品配置
show_button = tk.Button(bottom_frame, text="Disp", command= lambda :capture(True))
show_button.pack(side=tk.LEFT, padx=5)

cap_button = tk.Button(bottom_frame, text="Capture", command= lambda :capture())
cap_button.pack(side=tk.LEFT, padx=5)

# Frame幅をウィンドウ幅に
bottom_frame.columnconfigure(0, weight=1)

# 行と列を拡張可能に
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ウィンドウの初期サイズ保存
previous_width = root.winfo_width()
previous_height = root.winfo_height()

root.mainloop()
