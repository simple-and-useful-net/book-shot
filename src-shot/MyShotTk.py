import tkinter as tk
from PIL import ImageGrab, Image, ImageDraw  # Pillowから必要なモジュールをインポート
from PIL import Image, ImageDraw
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageGrab

import pyperclip
import win32clipboard
import io
import math

sub_win_disp=False
subwindow =None




"""
def show_subwindow():

    global sub_win_disp, subwindow

    sub_win_disp= True
    flt.overrideredirect(False)  # ウィンドウ枠を削除
    root.attributes('-fullscreen', False)
    flt.wm_attributes("-alpha", 1)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。

    # メインウィンドウを隠す
    # root.withdraw()
    # サブウィンドウを作成
    subwindow = tk.Toplevel()
    subwindow.title("サブウィンドウ")
    
    # サブウィンドウ内のエントリーボックスで入力された情報を取得する関数
    def get_info():
        sub_info = entry.get()
        # 取得した情報をメインウィンドウのラベルに表示
        #info_label.config(text=f"サブウィンドウの情報: {sub_info}")

    # サブウィンドウを閉じるボタンのアクションを設定
    def close_subwindow():
        sub_win_disp= False
        subwindow.destroy()
        # メインウィンドウを再表示
        # root.deiconify()

        flt.overrideredirect(True)  # ウィンドウ枠を削除
        root.attributes('-fullscreen', True)
        flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
    
    # サブウィンドウにエントリーボックスとボタンを追加
    entry_label = tk.Label(subwindow, text="情報を入力:")
    entry_label.pack()
    entry = tk.Entry(subwindow)
    entry.pack()
    submit_button = tk.Button(subwindow, text="情報を送信", command=get_info)
    submit_button.pack()
    
    # サブウィンドウに閉じるボタンを追加
    close_button = tk.Button(subwindow, text="閉じる", command=close_subwindow)
    close_button.pack()
"""


en_no = 0

def draw_smooth_circle(canvas, text,center_x, center_y, radius):

    global en_no
    
    num_segments = 50  # 円を近似するための線分の数

    angle = 2 * math.pi / num_segments
    points = []

    for i in range(num_segments):
        x = center_x + radius * math.cos(i * angle)*0.7
        y = center_y + radius * math.sin(i * angle)*0.7
        points.extend([x, y])

    # 多角形として円を描画
    canvas.create_polygon(points, smooth=True,outline="gray", width=1, fill="red", tag= f"en{en_no}")

    font = ("Meiryo", 18)  # フォント名、サイズ、太さを指定
    # font = ("Yu Gothic", 22)  # フォントの種類とサイズを設定

    # テキストを描画して円の中央に配置
    text_x = center_x  # 円の中心X座標に配置
    text_y = center_y+2  # 円の中心Y座標に配置
    canvas.create_text(text_x, text_y, text=text, font=font, tag= f"en{en_no}")

    en_no += 1


def draw_text_in_circle(canvas, text, center_x, center_y, circle_radius):
    # フォント設定
    font = ("Helvetica", 24)  # フォントの種類とサイズを設定
    font = ("Yu Gothic", 24)  # フォントの種類とサイズを設定
    font = ("Meiryo", 24, "bold")  # フォント名、サイズ、太さを指定
    # 円を描画
    canvas.create_oval(
        center_x - circle_radius, center_y - circle_radius,
        center_x + circle_radius, center_y + circle_radius,
        width=5,  # 外枠の太さ
        outline="black",
        fill="red",
        tag="en_no"
    )

    # テキストを描画して円の中央に配置
    text_x = center_x  # 円の中心X座標に配置
    text_y = center_y  # 円の中心Y座標に配置
    canvas.create_text(text_x, text_y, text=text, font=font, tag="en_no")


def to_clip(fname):
    # Open the image file
    img = Image.open( fname )

    output = io.BytesIO()
    img.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    # クリップボードをクリアして、データをセットする
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData( win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def show_msg( msg ):
    global rect_id, text_id

    msg_x= 500
    msg_y= 200
    text_id = canvas.create_text( msg_x, msg_y, text=msg, font=("Arial", 24), fill="white")

    text_width, text_height = get_text_size(text_id)
    print(f"テキストの幅: {text_width}, 高さ: {text_height}")

    # 矩形を描画（テキストサイズに合わせて調整する場合）
    rect_id = canvas.create_rectangle(  msg_x - text_width // 2 - 10, msg_y - text_height // 2 - 10, 
                                        msg_x + text_width // 2 + 10, msg_y + text_height // 2 + 10, 
                                        tag="rect_bk", fill="black", outline="black")
    canvas.lower( "rect_bk" )

def clr_msg():
    global rect_id, text_id

    if text_id != None:
        canvas.delete(text_id)  # 背景矩形を削除

    if rect_id != None:
        canvas.delete(rect_id)  # 背景矩形を削除
        
    rect_id, text_id = None,None



'''
    枠を設定している（グリーンで幅４）
    "screenshot.png"のファイルに保存

'''
def cap_image():
        # 赤枠の座標を取得
        if rect == None:
            print("外枠が選択されていません")
            return
        
        # canvas.itemconfig(text_id, text="")
        # clr_msg()
        x1, y1, x2, y2 = canvas.coords(rect)
            
        # 画面全体から赤枠内の領域をキャプチャ
        flt.wm_attributes("-alpha", 0)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
        
        # Pillowを使用してキャプチャした画像に枠を描画
        #screenshotWaku = ImageGrab.grab(bbox=(x1-0, y1-0, x2+1, y2+1))
        img_with_frame = Image.new("RGB", screenshot.size)
        img_with_frame.paste(screenshot, (0, 0))
        draw = ImageDraw.Draw(img_with_frame)
        draw.rectangle([(0, 0), img_with_frame.size], outline="lightgreen", width=2)

        # self.root.wm_attributes('-transparentcolor', 'white')  # 白色を透明とする（適宜色を変更できます）            
        # キャプチャした画像をファイルに保存
        img_with_frame.save("screenshot.png")
        to_clip("screenshot.png")
        print("キャプチャした画像を保存しました：captured_image.png")




sx =None
sy =None
rect2 =None

start_x =None
start_y =None

drawing =None
rect =None
rect_no=0
en_no = 0
arrow_no,rect3,sx3,sy3 = 0, None, None, None



def move_mouse_to_sub_window(sub_window):
    # サブウィンドウの位置とサイズを取得
    sub_window.update()  # ウィンドウのサイズと位置を最新にする
    x = sub_window.winfo_x()
    y = sub_window.winfo_y()
    width = sub_window.winfo_width()
    height = sub_window.winfo_height()
    
    print(x,y,width,height)
    # マウスポインターをサブウィンドウの中央に移動
    center_x = x + width // 2
    center_x = x + 20
    center_y = y + height // 2
    center_y = y + 50
    pyautogui.moveTo(center_x, center_y)
    # pyautogui.moveTo(30,50)
    
# エスケープキー

def on_s_escape( event ):
    global en_no
    
    canvas.delete("all")
    en_no = 0

def on_root_escape( event ):
    
    print("kitayo")
    btn_click()

def on_escape( event ):
    
    global sub_win_disp,flt
    global btn
    
    sub_win_disp= True
    # flt.overrideredirect(False)  # ウィンドウ枠を削除
    # root.attributes('-topmost', False)
    root.attributes('-fullscreen', False)
    flt.wm_attributes("-alpha", 1)  # ウィンドウ表示
    # サブウィンドウにフォーカスを設定
    root.focus_set()
    
    root.update_idletasks()  # ウィンドウのサイズと位置を最新にする
    x = root.winfo_x()
    y = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()
    
    print(x,y,width,height)
    # マウスポインターをサブウィンドウの中央に移動

    move_mouse_to_sub_window(root)    



def on_key_press(event):
    if event.keysym == "Escape":
        if event.state & 0x4:  # Ctrlキーが押されている場合
            print("Ctrl+Escapeが押されました")
            # tag = "en_no"
            # canvas.delete( tag )

        elif event.state & 0x20000:  # Altキーが押されている場合
            print("Alt+Escapeが押されました")
        else:
            print("Escapeが押されました")



# マウス中央がクック（保存）
# 指定枠がキャプチャされます

def on_press2(event):
    cap_image()


# マウス右がクリック
# キャンセル処理

# Ctrl　円のキャンセル
# Alt   矢印
# Shift  四角枠
# グローバル変数でマウスポインターの元の位置を保持
original_position = None

def on_press3(event):
    global drawing,rect,start_x,start_y
    global rect2,sx,sy
    global en_no
    global arrow_no,rect3,sx3,sy3

    # shift
    # 赤の四角をキャンセル
    if event.state & 0x01:
        global rect_no

        if rect_no > 0:
            rect_no -= 1        
        
        tag = "rect%d" %rect_no
        canvas.delete( tag )

    # Ctrl
    # 円のキャンセル
    elif event.state & 0x04:  

        if en_no > 0:
            en_no -= 1        

        tag = f"en{en_no}"
        canvas.delete( tag )


    # Altが押されました
    elif event.state & 0x20000:
        tag = "arrow_all"
        canvas.delete( tag )
        arrow_no = 0
    else:
        global original_position

        if rect != None:
            cap_image()

            # 現在のマウスポインターの位置を保存
            original_position = pyautogui.position()        
            
            on_escape( None )




#----------------------------------------
#   クリック
#----------------------------------------
def on_press(event):

    global drawing
    global en_no, arrow_no
    
    global rect,sx,sy
    global rect2,sx2,sy2
    global rect3,sx3,sy3

    if sub_win_disp:
        return
    
    # ドラッグ中かを判定する
    drawing = True

    if event.state & 0x1:  # 0x1はShiftキーの状態を表します
        print("Shiftキーが押された状態で左クリックされました")

        sx2 = canvas.canvasx(event.x)
        sy2 = canvas.canvasx(event.y)
        if rect2:
            canvas.delete("rect_drag")
            rect2 = None


    # 円数字の表示（コントロールキー）
    elif event.state & 0x4:  # 0x4はCtrlキーの状態を表します
        print("Ctrlキーが押されながらクリックされました")
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        draw_smooth_circle(canvas, str(en_no+1), x, y, 20)
        # ドラッグ中かを判定する
        drawing = False

    # 矢印の表示（Altキー）
    elif event.state & 0x20000:
        print("Altキーが押されながらクリックされました")
        sx3 = canvas.canvasx(event.x)
        sy3 = canvas.canvasx(event.y)
        if rect3:
            canvas.delete("arrow_drag")
            rect3 = None
    else:
        sx = canvas.canvasx(event.x)
        sy = canvas.canvasy(event.y)
        # キャプチャ範囲は１つだけ
        # if rect:
            # canvas.delete("capRange")
            # rect = None

#----------------------------------------
# ドラッグ
#----------------------------------------
def on_drag(event):

    global drawing
    global en_no, arrow_no
    

    if sub_win_disp:
        return
    if not drawing:
        return

    # 画面キャプチャー
    def drag_capture():
        global rect,sx,sy
        
        if rect:
            canvas.delete("capRange")

        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        rect = canvas.create_rectangle( sx, sy, x,y, tag="capRange", outline="lightgreen", width=2)
        return

    # 四角形
    def drag_rect():
        global rect2,sx2,sy2

        if rect2:
            canvas.delete("rect_drag")

        x = canvas.canvasx(event.x)
        y = canvas.canvasx(event.y)
        rect2 = canvas.create_rectangle(sx2, sy2, x,y, 
                                        tag="rect_drag",
                                        outline='red', width=2)  # 四角形を描画
        canvas.lower( "rect_drag" )
        return

    # 矢印
    def drag_arrows():
        global rect3,sx3,sy3

        if rect3:
            canvas.delete( rect3 )

        x = canvas.canvasx(event.x)
        y = canvas.canvasx(event.y)
        rect3 = canvas.create_line( sx3, sy3, x,y, 
                            arrow=tk.LAST,
                            arrowshape=(24, 30, 9),
                            width=10, fill="#ff00ff",
                            tag="arrow_all")
        return

        
    # Shiftキーの状態を表します
    # 四角枠の表示
    if event.state & 0x1:  
        # print("Shiftキーが押")
        drag_rect()

    # Altキー
    # 矢印の表示
    elif event.state & 0x20000:
        drag_arrows()


    # キャプチャ範囲の枠
    else:
        drag_capture()


#----------------------------------------
#       リリース
#----------------------------------------
def on_release(event):

    global subwindow,sub_win_disp
    global drawing
    global en_no, arrow_no
    
    global rect,sx,sy
    global rect3,sx3,sy3


    print("on_release", start_x,start_y)

    if sub_win_disp:
        # subwindow.destroy()
        # メインウィンドウを再表示
        root.deiconify()

        return

    if not drawing:
        return
    else:
        # ドラッグ中かを判定
        drawing = None


    # 四角形の確定
    def release_rect():
        global rect2
        global rect_no

        if rect2:
            x1, y1, x2, y2 = canvas.coords(rect2)

            canvas.delete("rect_drag")
            rect2 = canvas.create_rectangle(x1, y1, x2, y2, 
                                        tag="rect%d" %rect_no,
                                        outline='red', width=3) 
            canvas.lower( rect2 )

            print("tag","rect%d" %rect_no)
            rect_no +=1
            return
        
        
        
    # 赤の四角枠の確定
    # 枠は最下位（円があるため）
    # Shiftキーの状態
    if event.state & 0x1:  
        release_rect()
        return
       
    elif event.state & 0x20000:  # 0x20 [Alt]
        return

    # キャプチャーする
    else:
        if rect != None:
            cap_image()
        return





# サイズと位置をrootの背後に設定
def flt_track( arg ):
    flt.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_rootx()}+{root.winfo_rooty()}")
    flt.lower(root)



import pyautogui

def btn_click():
    
    global sub_win_disp
    global original_position

    if original_position:
        # 保存された位置にマウスポインターを戻す
        pyautogui.moveTo(original_position)
        original_position = None
        
    sub_win_disp= False
    # root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)
    flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。





root = tk.Tk()

# 現在の画面のサイズを取得
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# root.geometry("200x30+200+" + str(screen_height-100))
root.geometry("200x30+10+10")
root.title("Capture")

# CanvasをFrame内に配置
canvas = tk.Canvas(root, 
                   background="yellow",  
                   width=screen_width, 
                   height=screen_height)
canvas.pack()
canvas.place(x=-1, y=-1)


root.attributes('-topmost', True)
root.attributes('-fullscreen', True)
root.wm_attributes("-transparentcolor", "yellow")
root.resizable(0, 0)

flt = tk.Toplevel(root)     # 別ウィンドウを作成
flt.overrideredirect(True)  # ウィンドウ枠を削除
flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。

# flt.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_rootx()}+{root.winfo_rooty()}")
# flt.lower(root)

flt.bind("<ButtonPress-1>",  on_press)
flt.bind("<ButtonPress-2>",  on_press2)
flt.bind("<ButtonPress-3>",  on_press3)
flt.bind("<B1-Motion>",      on_drag)
flt.bind("<ButtonRelease-1>",on_release)

root.bind("<Escape>",           on_root_escape)
flt.bind("<Escape>",           on_escape)
flt.bind("<Shift-Escape>",     on_s_escape)


# 未使用
flt.bind("<KeyPress>", on_key_press)  # キー押下（KeyPress）イベントをバインド

root.bind("<Configure>", flt_track)

# ボタン作成
# btn = tk.Button(flt, text='Shot', command=btn_click)
# btn.place(x=0, y=0)

# 左ボタンの作成と配置
btn= tk.Button( flt, text='Capture', command=btn_click )
btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def get_text_size(text_id2):
    global text_id
    
    bbox = canvas.bbox(text_id)
    if bbox:
        # bbox は (x1, y1, x2, y2) の形式
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    return 0, 0
    
# 右ボタンの作成と配置
# right_button = tk.Button( flt, text="閉じる", command=root.destroy)
# right_button.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
msg_disp_stat = False
rect_id       = None
text_id       = None

    
def show_help(event):
    global rect_id, text_id
    global msg_disp_stat

    msg = '''
マウスクリックしてドラッグ：領域のキャプチャー
コントロールキーを押しながら　ドラッグ：    数字
シフトを押しながら　ドラッグ：    赤枠
'''

    if msg_disp_stat == False:
        show_msg( msg )
        msg_disp_stat = True
    else:
        clr_msg()
        msg_disp_stat = False
        

def clear_text(event):
    global rect_id, text_id
    # キー「c」が押された時にテキストを消去
    # canvas.itemconfig(text_id, text="")
    canvas.delete(text_id)  # 背景矩形を削除
    canvas.delete(rect_id)  # 背景矩形を削除


# 複数行の文字列をキャンバスに描画
# text_id = canvas.create_text(600, 300, text="クリック\nしてください", font=("Arial", 24), fill="white")

# text_bbox = canvas.bbox("insert")  # テキストの外接矩形を取得
# rect_id = canvas.create_rectangle(180, 120, 420, 180, tag="rect_bk" , fill="black", outline="black")  # 背景色を黒に設定
# テキストのサイズを取得
# text_width, text_height = get_text_size(text_id)
# print(f"テキストの幅: {text_width}, 高さ: {text_height}")

# 矩形を描画（テキストサイズに合わせて調整する場合）
# rect_id = canvas.create_rectangle( msg_x - text_width // 2 - 10, msg_y - text_height // 2 - 10, 200 + text_width // 2 + 10, 150 + text_height // 2 + 10, tag="rect_bk", fill="black", outline="black")
# canvas.lower( "rect_bk" )
# キャンバスにキーイベントをバインド
canvas.bind_all("<h>", show_help)
# canvas.bind_all("<c>", clear_text)

root.mainloop()
