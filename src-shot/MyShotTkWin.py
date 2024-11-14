import tkinter as tk
from PIL import ImageGrab, Image, ImageDraw  # Pillowから必要なモジュールをインポート
from PIL import Image, ImageDraw
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageGrab

import pyperclip
import win32clipboard
import io
import math
import time
import threading


def cap_proc():
    
    global canvas, filename

    cap_image()
    # on_s_escape()

    on_s_escape()        
    w,h=load_image_to_canvas(canvas, filename)

    root.geometry(f"{w+10}x{h+40}")
        
    
def load_image_to_canvas(canvas, file_path):
    """
    指定されたファイルパスから画像を読み込み、Canvasに表示する関数。
    すでに画像が表示されている場合、古い画像を削除して新しい画像を表示する。

    Args:
        canvas (tk.Canvas): 画像を表示するCanvasオブジェクト。
        file_path (str): 読み込む画像ファイルのパス。
    """
    # 前回の画像を削除
    if hasattr(canvas, 'image_id'):
        canvas.delete(canvas.image_id)

    # 画像を読み込み、PhotoImageに変換
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)

    # 画像をCanvasに表示し、そのIDを保持
    canvas.image_id = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # 画像の参照を保持（これをしないと画像が表示されない）
    canvas.image = photo

    # 画像をCanvasの最下層に配置
    canvas.tag_lower(canvas.image_id)
    
    # 画像の幅と高さを取得
    width, height = image.size
    return width, height
    
    

def edit2():

    global canvas, filename

    w,h=load_image_to_canvas(canvas, filename)
    
    # load_image_to_canvas(canvas, "test.png")

def edit2_clr():

    global canvas, filename

    on_s_escape()
    # if hasattr(canvas, 'image_id'):
        # canvas.delete(canvas.image_id)

    global cap_befor_x
    global cap_befor_y
    global cap_befor_w
    global cap_befor_h
    
    cap_befor_x,cap_befor_y,cap_befor_w,cap_befor_h = get_uin()


import win32gui
import win32ui
import win32con
import win32api

def capture_cursor():
    # カーソル情報を取得
    flags, hcursor, (x, y) = win32gui.GetCursorInfo()

    # カーソルアイコンを取得
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hcursor, 32, 32, 0, None, win32con.DI_NORMAL)

    # PILイメージに変換
    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)
    cursor_img = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA', 0, 1)
    
    return cursor_img, x, y



sub_win_disp=False
subwindow =None





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


msg_disp_stat = False
rect_id       = None
text_id       = None


def get_text_size(text_id2):
    global text_id
    
    bbox = canvas.bbox(text_id)
    if bbox:
        # bbox は (x1, y1, x2, y2) の形式
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    return 0, 0

px, py = 0,0 
   
def get_mouse_position(event):

    global px, py
    # ウインドウの左上を基準とした相対的なマウスの座標を取得
    x_root = event.widget.winfo_pointerx()
    y_root = event.widget.winfo_pointery()
    px = x_root - root.winfo_rootx()
    py = y_root - root.winfo_rooty()
    
    # print(f"Absolute Position: ({x_root}, {y_root})")
    # print(f"Relative Position: ({px}, {py})")
    
        
def show_msg( msg ):

    global rect_id, text_id, canvas
    global px, py

    if text_id != None:
        print("msg ari")
        return
        
    msg_x= 500
    msg_y= 200

    if px < 500:
        px =500
        
    if py <300:
        py =300
        
    msg_x= px
    msg_y= py
    
    text_id = canvas.create_text( msg_x, msg_y, text=msg, font=("Arial", 24), fill="white")

    text_width, text_height = get_text_size(text_id)
    print(f"テキストの幅: {text_width}, 高さ: {text_height}")

    # 矩形を描画（テキストサイズに合わせて調整する場合）
    rect_id = canvas.create_rectangle(  msg_x - text_width // 2 - 10, msg_y - text_height // 2 - 10, 
                                        msg_x + text_width // 2 + 10, msg_y + text_height // 2 + 10, 
                                        tag="rect_bk", fill="black", outline="black")
    canvas.lower( "rect_bk" )

def clr_msg():
    
    
    global rect_id, text_id, canvas

    print("clr_msg",rect_id, text_id)
    if text_id != None:
        canvas.delete(text_id)  # 背景矩形を削除
        print("canvas.delete(text_id)  OK")

    if rect_id != None:
        canvas.delete(rect_id)  # 背景矩形を削除
        print("canvas.delete(rect_id)  OK")
        
    rect_id, text_id = None,None
    print("clr_msg_end",rect_id, text_id)



def disp_msg( msg, tm=0 ):

    # return
    global text_id
    
    if text_id != None:
        return
        
    show_msg( msg )
     
    if tm != 0:
        threading.Timer( tm, clr_msg ).start()

    

def show_help(event):
    global rect_id, text_id
    global msg_disp_stat

    msg = '''
キャプチャー範囲       ：ドラッグ
赤枠                  ：Shift  + ドラッグ                     
矢印                  ：ALT    + ドラッグ
数字                  ：Ctrl   + クリック
'''

    if msg_disp_stat == False:
        # disp_msg( msg,10 )
        show_msg( msg )
        msg_disp_stat = True
    else:
        clr_msg()
        msg_disp_stat = False



amode_sw = False
nmode_sw = False
wmode_sw = False
rmode_sw = False

def n_mode(event):

    global nmode_sw, amode_sw, wmode_sw
    
    amode_sw = False
    # nmode_sw = False
    wmode_sw = False
    clr_msg()

    if nmode_sw:
        nmode_sw = False
    else:    
        nmode_sw = True
        msg = "数字モード（クリックして下さい）\n(e:終了, c:キャプチャ)"
        show_msg( msg )


def a_mode(event):

    global nmode_sw, amode_sw, wmode_sw
    
    # amode_sw = False
    nmode_sw = False
    wmode_sw = False
    clr_msg()

    if amode_sw:
        amode_sw = False
    else:    
        amode_sw = True
        msg = "矢印モード（ドラッグして下さい）\n(e:終了, c:キャプチャ)"

        show_msg( msg )


def w_mode(event):

    global nmode_sw, amode_sw, wmode_sw
    
    amode_sw = False
    nmode_sw = False
    # wmode_sw = False
    clr_msg()

    if wmode_sw:
        wmode_sw = False
    else:    
        wmode_sw = True
        msg = "四角モード（ドラッグして下さい）\n(e:終了, c:キャプチャ)"

        show_msg( msg )


def r_mode(event):

    global nmode_sw, amode_sw, wmode_sw, rmode_sw
    
    clr_msg()

    if rmode_sw:
        rmode_sw = False
    else:    
        rmode_sw = True
        msg = "キャプチャ範囲の指定"

        show_msg( msg )




'''
    枠を設定している（グリーンで幅４）
    "screenshot.png"のファイルに保存

'''
rect = None
filename    =""



def cap_image(event=None):
        
        global canvas,rect
        global save_x1, save_y1, save_x2, save_y2
        global root, flt
        global filename
        global captm, fname
        
        # 赤枠の座標を取得
        # time.sleep(5)
        
        
        
        if rect == None:
            msg = "ウインドウ内キャプチャOK"
        else:
            msg= "キャプチャ画像を保存しました(captured_image.png)"


        root.title(msg)  # タイトルを変更する
        # disp_msg( msg,1 )
        # print("dbg1")
    
        geometry = flt.geometry()
        width, height, x, y = map(int, geometry.replace('x', '+').split('+'))
        # Canvasの現在の幅と高さを取得
        cwidth  = canvas.winfo_width()
        cheight = canvas.winfo_height()
 
        if rect == None:
            # x1 = x +10
            x1 = x +5
            y1 = y +0
            x2 = x1 + cwidth
            y2 = y1 + cheight
            print(f"幅: {width}, 高さ: {height}, x座標: {x1}, y座標: {y1}")

          # cap_befor_x,cap_befor_y,cap_befor_w,cap_befor_h = x1,y1, x2-x1, y2-y1
               
        else:
            x1, y1, x2, y2 = canvas.coords(rect)
            x1 += (x-2)
            y1 += (y-2)
            x2 += (x+5)
            y2 += (y+5)
            bbox = canvas.bbox("capRange")
            x1 = bbox[0]
            x2 = bbox[2]
            y1 = bbox[1]
            y2 = bbox[3]
            # x1 += (x+6)
            # y1 += (y+6)
            # x2 += (x+5)
            # y2 += (y+5)

            x1 += (x+5)
            y1 += (y+0)
            x2 += (x+5)
            y2 += (y+0)
            # x1 += (x+10)
            # y1 += (y)
            # x2 += (x+9)
            # y2 += (y+1)

            
        # time.sleep(3)
        # clr_msg()
        # time.sleep(1)
        # canvas.itemconfig(text_id, text="")
        # clr_msg()
        
        # save_x1, save_y1, save_x2, save_y2 = canvas.coords(rect)
        # root.geometry()は'widthxheight+x+y'という形式の文字列を返す
        
        # 画面全体から赤枠内の領域をキャプチャ
        flt.wm_attributes("-alpha", 0)  # ウィンドウを透明にする
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        flt.wm_attributes("-alpha", 0.002)  #すこし透明にする
         
        # Pillowを使用してキャプチャした画像に枠を描画
        #screenshotWaku = ImageGrab.grab(bbox=(x1-0, y1-0, x2+1, y2+1))
        img_with_frame = Image.new("RGB", screenshot.size)
        img_with_frame.paste(screenshot, (0, 0))
        draw = ImageDraw.Draw(img_with_frame)
        # print("img_with_frame.size=", img_with_frame.size)
        # draw.rectangle([(10, 0), img_with_frame.size], outline="lightgreen", width=2)

        # カーソルの形状と位置を取得
        cursor_img, cursor_x, cursor_y = capture_cursor()

        # カーソルをスクリーンショットに合成
        img_with_frame.paste(cursor_img, (cursor_x, cursor_y), cursor_img)


        # self.root.wm_attributes('-transparentcolor', 'white')  # 白色を透明とする（適宜色を変更できます）            
        # キャプチャした画像をファイルに保存
        # 現在の日時を取得し、フォーマットする
        import datetime

        now = datetime.datetime.now()
        # timestamp = now.strftime("%Y%m%d_%H%M%S")  # YYYYMMDD_HHMMSS の形式でフォーマット
        timestamp = now.strftime("%H%M%S")  # YYYYMMDD_HHMMSS の形式でフォーマット

        # ファイル名を生成
        grp = fname.get()
        filename = f"{grp}_{timestamp}.png"

        img_with_frame.save(filename)
        to_clip(filename)
        print( f"キャプチャした画像を保存しました：{filename}")
        root.title( f"save={filename}" )


import threading

    




drawing =None

en_no, arrow_no, rect_no    = 0,0,0
    
rect,   sx,sy       = None, None,None
rect2,  sx2,sy2     = None, None,None
rect3,  sx3,sy3     = None, None,None


    
# エスケープキー

def on_s_escape( event=None ):

    global en_no, arrow_no, rect_no
    global rect
    global amode_sw, wmode_sw, nmode_sw, rmode_sw
    
    canvas.delete("all")
    en_no, arrow_no, rect_no    = 0,0,0
    rect = None
    amode_sw, wmode_sw, nmode_sw = False, False, False

def on_root_escape( event ):
    
    print("kitayo")
    btn_click()

def on_escape( event=None ):

    global rect
    
    if rect:
        canvas.delete("capRange")
        rect = None
    return
    
    



# マウス中央がクック（保存）
# 指定枠がキャプチャされます
tm =3
def disp_sec():

    global root,flt,tm

    for i in range(tm):
        msg = f"Shotまで{tm-i}秒"
        root.title( msg )
        print(msg)
        time.sleep(1)
    
def on_press2(event=None,ct=1):
    
    global root,flt,no, tm
    global captm

    tm = int(captm.get() )
    no = 1
    
    def f():
        global root,flt, no
        global filename

        edit()
        cap_image()
        # flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明

        msg= f"ShotOK ({filename})"
        root.title(msg )
        # threading.thread( 0.5, disp_sec).start()
        # widget=root1.focus_get()
        # print(widget)
        no += 1
        if no ==ct+1:
            
            ensure_focus(root)
            edit2()
            return
        else:    
            root.title( f"cap start {no}")
            flt.wm_attributes("-alpha", 0)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
            root.after( tm* 1000, f)
        
    root.title( f"cap start {no}")
    # flt.wm_attributes("-alpha", 0)  # ウィンドウを透明
    no_edit()
    thread = threading.Thread(target=disp_sec, daemon=True)
    thread.start()    
    root.after( tm*1000, f)


# マウス右がクリック
# キャンセル処理

# Ctrl　円のキャンセル
# Alt   矢印
# Shift  四角枠
# グローバル変数でマウスポインターの元の位置を保持
original_position = None

def on_press3(event):

    global drawing
    global en_no, arrow_no, rect_no
    
    global rect,sx,sy
    global rect2,sx2,sy2
    global rect3,sx3,sy3
    global amode_sw, wmode_sw, nmode_sw, rmode_sw

    # shift
    # 赤の四角をキャンセル
    if (event.state & 0x01) or (wmode_sw):
        global rect_no

        if rect_no > 0:
            rect_no -= 1        
        
        tag = "rect%d" %rect_no
        canvas.delete( tag )

    # Ctrl
    # 円のキャンセル
    elif (event.state & 0x04) or (nmode_sw):  

        if en_no > 0:
            en_no -= 1        

        tag = f"en{en_no}"
        canvas.delete( tag )


    # Altが押されました
    elif (event.state & 0x20000) or (amode_sw):
        tag = "arrow_all"
        canvas.delete( tag )
        arrow_no = 0
    else:
        global original_position

        cap_image()
        # if rect != None:
            # cap_image()
            # return

            # 現在のマウスポインターの位置を保存
            # original_position = pyautogui.position()        
            
            # on_escape( None )




#----------------------------------------
#   クリック
#----------------------------------------
def on_press(event):

    print("-----------------------> on_press")

    global drawing
    global en_no, arrow_no, rect_no
    
    global rect,sx,sy
    global rect2,sx2,sy2
    global rect3,sx3,sy3
    global amode_sw, wmode_sw, nmode_sw, rmode_sw
    global button2

    print("-----------------------> on_press2", sub_win_disp)
    if sub_win_disp:
        return
    
    # ドラッグ中かを判定する
    drawing = True

    # 0x1はShiftキー
    # 赤枠
    if (event.state & 0x1) or ( wmode_sw):  
        print("Shiftキーが押された状態で左クリックされました")

        sx2 = canvas.canvasx(event.x)
        sy2 = canvas.canvasx(event.y)
        if rect2:
            canvas.delete("rect_drag")
            rect2 = None


    # 円数字の表示（コントロールキー）
    elif (event.state & 0x4) or (nmode_sw):  # 0x4はCtrlキーの状態を表します
        print("Ctrlキーが押されながらクリックされました")
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        draw_smooth_circle(canvas, str(en_no+1), x, y, 20)
        # ドラッグ中かを判定する
        drawing = False

    # 矢印の表示（Altキー）
    elif (event.state & 0x20000) or (amode_sw):
        print("Altキーが押されながらクリックされました")
        sx3 = canvas.canvasx(event.x)
        sy3 = canvas.canvasx(event.y)
        if rect3:
            canvas.delete("arrow_drag")
            rect3 = None
    else:
        global button2
        
        current_text = button2.config('text')[-1]
        if current_text != '範囲中！':
            return
            

        print("押tenai")
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
    global en_no, arrow_no, rect_no
    
    global rect,sx,sy
    global rect2,sx2,sy2
    global rect3,sx3,sy3
    global button2

   

    if sub_win_disp:
        return
    if not drawing:
        return

    # 画面キャプチャー
    def drag_capture():
        global rect,sx,sy
        global button2
        
        current_text = button2.config('text')[-1]
        if current_text  != "範囲中！":
            return
        
        if rect:
            canvas.delete("capRange")

        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        # rect = canvas.create_rectangle( sx, sy, x,y, tag="capRange", outline="lightgreen", width=1)
        # rect = canvas.create_rectangle( sx, sy, x,y, tag="capRange", outline="lightgreen", width=2)
        rect = canvas.create_rectangle( sx, sy, x,y, tag="capRange", outline="lightgreen", width=4)
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
        # canvas.lower( "rect_drag" )
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

        
    global amode_sw, wmode_sw, nmode_sw, rmode_sw
    # Shiftキーの状態を表します
    # 四角枠の表示
    if (event.state & 0x1) or (wmode_sw):  
        # print("Shiftキーが押")
        drag_rect()

    # Altキー
    # 矢印の表示
    elif (event.state & 0x20000) or(amode_sw):
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
    global en_no, arrow_no, rect_no
    
    global rect,sx,sy
    global rect2,sx2,sy2
    global rect3,sx3,sy3
    global amode_sw, wmode_sw, nmode_sw
    global button2

    print("on_release")

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
            # canvas.lower( rect2 )

            print("tag","rect%d" %rect_no)
            rect_no +=1
            return
        
        
        
    # 赤の四角枠の確定
    # 枠は最下位（円があるため）
    # Shiftキーの状態
    if (event.state & 0x1) or (wmode_sw):  
        release_rect()
        return
       
    elif (event.state & 0x20000):  # 0x20 [Alt]
        return

    # キャプチャーする
    else:
        print("release - cap_image ")
        current_text = button2.config('text')[-1]
        if current_text  != "範囲中！":
            return

        cap_image()
        toggle_button()
        return





# サイズと位置をrootの背後に設定
# def flt_track( arg ):
    # flt.geometry(f"{canvas.winfo_width()}x{canvas.winfo_height()}+{canvas.winfo_rootx()}+{canvas.winfo_rooty()}")
    # print("flt_track", canvas.winfo_width(), canvas.winfo_rootx())
    # flt.lower(root)

def rere(root):

    global flt

    root.deiconify
    print("Window size reduced-3")
    # root.focus_force()
    # flt.focus_force()
    
    # flt.wm_attributes("-alpha", 0.002)
    

def minimize_and_restore(root):
    global flt, initSW

    import win32gui
    import win32con

    # hwnd = win32gui.GetForegroundWindow()
    # hwnd = win32gui.GetParent(root.winfo_id())
    
    # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # win32gui.SetForegroundWindow(hwnd)
    # print("Window size reduced-222")
    # return
    initSW = 1

    root.update()  # ウインドウの表示を更新
    root.iconify()  # 最小化
    root.after(200, root.deiconify)  # 200ミリ秒後に復元
    # root.after(2000, lambda: rere(root))  # 200ミリ秒後に復元
    print("Window size reduced-2")
    initSW = 0
    # root.after(300, lambda: flt.wm_attributes("-alpha", 0.002))

    # root.focus_force()
    # flt.focus_force()
    # flt.wm_attributes("-alpha", 0.002)

# 変更されるたびにサイズと位置をrootに合わせて、rootの背後に置く
initSW = 0
def flt_track(_):

    global previous_width, previous_height
    global root, flt, initSW
    
    print("initSW=", initSW)    
    # root.update_idletasks() # mainloopの前に設定値の更新
    flt.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_rootx()}+{root.winfo_rooty()}")
    flt.lower(root)

    # 現在のウインドウサイズを取得
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    
    # ウインドウサイズが小さくされたかどうかを判定
    if current_width < previous_width or current_height < previous_height:
        if initSW==0:
            print("Window size reduced")
            minimize_and_restore(root)
            # initSW=1

        # root.update_idletasks() # mainloopの前に設定値の更新

    # 現在のサイズを保存
    previous_width = current_width
    previous_height = current_height




import pyautogui

def focus_and_restore_alpha():

    global flt,root
    # 一時的に透明度を上げてフォーカスを設定
    flt.wm_attributes("-alpha", 0.5)
    flt.focus_set()

    # 再び透明度を下げる
    flt.wm_attributes("-alpha", 0.002)
    
def btn_click():
    
    global sub_win_disp
    global original_position
    global flt
    """
    if original_position:
        # 保存された位置にマウスポインターを戻す
        pyautogui.moveTo(original_position)
        original_position = None
    """
        
    sub_win_disp= False
    # root.attributes('-topmost', True)
    # flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
    # flt.focus_set()
    
    
    # root.attributes('-fullscreen', True)
    root.attributes('-fullscreen', False)
    focus_and_restore_alpha()

        

root = None
rect = None

def on_closing():

    global thread,rect
    
    thread =None
    rect =None
    # time.sleep(1)
    # time.sleep(1)
    threading.Timer( 0.1, root.focus_force).start()
    threading.Timer( 0.1, root.quit).start()

    # pass  # キャンセルされたら何もしない

def edit():
    
    global root, flt
    # 背景色の設定
    root.configure(bg="lightgray")  # ここで背景色を変更します
    flt.wm_attributes("-alpha", 0.002)
    chg_state( tk.NORMAL )

def no_edit():

    global root, flt
    # 背景色の設定
    root.configure(bg="green")  # ここで背景色を変更します
    flt.wm_attributes("-alpha", 0)
    chg_state( tk.HIDDEN )

def chg_state( sta ):

    canvas.itemconfig(rect, state=sta)
    canvas.itemconfig("arrow_all", state=sta)

    for i in range( en_no ):
        canvas.itemconfig( f"en{i}", state=sta)
    for i in range( rect_no ):
        canvas.itemconfig( f"rect{i}", state=sta)

    

def hide_canvas():
    # global canvas_visible
    
        # canvas.grid_forget()  # Canvasを非表示にする
    # if canvas_visible.get():
        # canvas.grid_forget()  # 非表示にする
        # canvas_visible.set(False)
    # 図形を非表示にする
    chg_state( tk.HIDDEN )


def show_canvas():
    # global canvas_visible
        # canvas.grid(row=0, column=0, padx=padding_x, pady=(0, padding_y))  # Canvasを再表示する
    # if canvas_visible.get():
        # canvas_visible.set(True)
    chg_state( tk.NORMAL )


import win32gui
import win32con

def ensure_focus(root):
    global flt
    # 現在フォーカスを持っているウィンドウのハンドルを取得
    hwnd_focused = win32gui.GetForegroundWindow()

    # Tkinterウィンドウのハンドルを取得
    hwnd_tk = win32gui.GetParent(root.winfo_id())

    if hwnd_focused != hwnd_tk:
        # フォーカスがない場合のみ処理を実行
        # root.update()   # 更新
        root.iconify()  # ウィンドウを最小化
        root.deiconify()  # ウィンドウを元に戻す
        
        print("hwnd_tk=", hwnd_tk)
        # win32gui.SetForegroundWindow(hwnd_tk)
        # win32gui.SetActiveWindow(hwnd_tk)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd_tk)
        pyautogui.moveTo(left+60, top + 10)
        pyautogui.click()        
        # root.after(200, root.deiconify)  # 200ミリ秒後に復元
        
        # root.focus_force()  # フォーカスを強制的に設定
        # flt.focus_force()

def toggle_button():
    global button2
    global cap_befor_w
    global cap_befor_h
    global cap_befor_x
    global cap_befor_y
    
    
    current_text = button2.config('text')[-1]
    
    if current_text == '範囲選択':
        button2.config(text='範囲中！', bg='lightgreen')
    elif current_text == '範囲中！':
        button2.config(text='範囲解除', bg='lightblue')
    else:
        on_s_escape()        
        root.geometry(f"{cap_befor_w}x{cap_befor_h}+{cap_befor_x}+{cap_befor_y}")
        # on_escape()
        button2.config(text='範囲選択', bg='lightcoral' )


#-----------------------------------------------
#       キャプチュー表示
#-----------------------------------------------
def show_cap():

    global root,flt,canvas
    global previous_width, previous_height
    global captm, fname
    global button2
    
    root = tk.Tk()
    root.geometry("500x700+0+0")
    # 現在の画面のサイズを取得
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # root.geometry("200x30+200+" + str(screen_height-100))
    # root.geometry("50x30+0+0")
    root.title("Capture")
    # タイトルバーを非表示にする
    # root.overrideredirect(True)


    # 余白サイズ
    padding_x = 10
    padding_y = 10
    padding_x = 5
    padding_y = 5


    # ボタンの作成
    # button = tk.Button(root, text="クリックしてタイトル変更")
    # button.grid(row=0, column=0, pady=(padding_y, 0))  # 上部に余白を持たせて配置

    # CanvasをFrame内に配置
    canvas = tk.Canvas(root, 
                       background="yellow",  
                       width=screen_width, 
                       height=screen_height)
    # canvas.pack()
    # Gridで配置
    canvas.grid(row=0, column=0, padx=padding_x, pady=(0, padding_y))  # 下部に余白を持たせて配置

    # 下部のFrameを作成
    bottom_frame = tk.Frame(root, bg="lightgray")
    bottom_frame.grid(row=1, column=0, padx=padding_x, pady=(0, padding_y), sticky="ew")  # 下部に余白を持たせて配置

    # Frame内に複数の部品を配置
    show_button = tk.Button(bottom_frame, text="Clr", command=edit2_clr)
    show_button.pack(side=tk.LEFT, padx=5)

    button1 = tk.Button(bottom_frame, text="CAP", command=cap_proc)
    button1.pack(side=tk.LEFT, padx=5)

    captm = tk.Entry(bottom_frame, width=2)
    captm.insert(tk.END, '5')           # 5secを設定
    captm.pack(side=tk.LEFT)
    
    button5 = tk.Button(bottom_frame, text="秒後Cap", command=on_press2)
    button5.pack(side=tk.LEFT, padx=5)

            
    button2 = tk.Button(bottom_frame, text="範囲選択",bg="lightcoral", command=toggle_button)
    button2.pack(side=tk.LEFT, padx=5)


    button3 = tk.Button(bottom_frame, text="Edit", command=edit)
    button3.pack(side=tk.LEFT, padx=5)

    # 
    button4 = tk.Button(bottom_frame, text="Win", command=no_edit)
    button4.pack(side=tk.LEFT, padx=5)

    label = tk.Label(bottom_frame, text="File")
    label.pack(side=tk.LEFT, padx=5)

    fname = tk.Entry(bottom_frame, width=4)
    fname.insert(tk.END, 'cap')           # 
    fname.pack(side=tk.LEFT, padx=5)
    

    # Frameの幅をウィンドウ幅に合わせる
    bottom_frame.columnconfigure(0, weight=1)

    # Canvasの表示状態を管理するための変数
    # canvas_visible = tk.BooleanVar(value=True)




    # Gridの行と列を拡張可能にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.attributes('-topmost', True)
    root.attributes('-fullscreen', False)
    root.wm_attributes("-transparentcolor", "yellow")
    # root.overrideredirect(True)  # ウィンドウ枠を削除
    # root.transient(root)         # タスクバーから消す
    # root.resizable(0, 0)

    flt = tk.Toplevel(root)     # 別ウィンドウを作成
    flt.overrideredirect(True)  # ウィンドウ枠を削除
    flt.transient(root)         # タスクバーから消す

    flt.wm_attributes("-alpha", 0.002)  # すこし透明
    # flt.wm_attributes("-alpha", 0)  # ウィンドウを透明
    # flt.wm_attributes("-alpha", 1)  # 透明解除

    def on_canvas_shown():
        
        global canvas,root,flt
        
        print("Canvas is now visible!")
        # flt.focus_set()
        # canvas.focus_set()
      
    def on_focus_in(event):
        global rect
        print("Window has gained focus!")

    def on_enter_root(event):
        global flt,root
        print("on_enter_root")

    def on_enter(event):
        global flt,root
        print("マウスポインタがウィンドウに入りました。")
        ensure_focus(root)

    def bring_to_front():

        global flt,root,canvas
        # root.lift()
        # flt.attributes('-topmost', True)  # 必要に応じて解除
            # if not flt.focus_get():
                # threading.Timer( 0.5, flt.focus_force).start()
                # print("---- >on_enter root.focus_focus")        

        def f():
            global flt,root,canvas

            threading.Timer( 0.5, flt.focus_force).start()
            # widget=root1.focus_get()
            # print(widget)
        root.after(100, f)
        # root.focus_force()
        # root.attributes('-topmost', True)
        
    def on_enter_canvas(event):
        global flt,root,canvas
        
        print("on_enter_canvasマウスポインタがウィンドウに入りました。")
        # if not root.focus_get():
            # threading.Timer( 0.5, root.focus_force).start()
            # print("on_enter root.focus_focus")        
        # pyautogui.moveTo(100,100)
        # pyautogui.click()

        # for i in range(5):
            # threading.Timer(0.5, bring_to_front).start()
        # if not flt.focus_get():
            # threading.Timer( 0.5, flt.focus_force).start()
            # print("on_enter flt.focus_focus")        

    def on_leave(event):
        print("マウスポインタがウィンドウから出ました。")


    # root.bind("<Enter>", on_enter_root)
    # root.bind("<Leave>", on_leave)
    # canvas.bind_all("<Enter>", on_enter_canvas)

    flt.bind("<FocusIn>", on_focus_in)
    flt.after_idle(on_canvas_shown)
    # 未使用
    # flt.bind("<KeyPress>", on_key_press)  # キー押下（KeyPress）イベントをバインド

    root.bind("<Configure>", flt_track)
    # 「×」ボタンを無効化（カスタム動作を設定）
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # ボタン作成
    # btn = tk.Button(flt, text='Shot', command=btn_click)
    # btn.place(x=0, y=0)

    # 左ボタンの作成と配置
    btn= tk.Button( flt, text='Capture', command=btn_click )
    btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    flt.bind("<ButtonPress-1>",  on_press)
    flt.bind("<ButtonPress-2>",  on_press2)
    flt.bind("<ButtonPress-3>",  on_press3)
    flt.bind("<B1-Motion>",      on_drag)
    flt.bind("<ButtonRelease-1>",on_release)

    root.bind("<Escape>",           on_root_escape)
    flt.bind("<Escape>",            on_escape)
    flt.bind("<Shift-Escape>",      on_s_escape)
    flt.bind('<Motion>',            get_mouse_position)

    canvas.bind("<ButtonPress-1>",  on_press)
    canvas.bind("<ButtonPress-2>",  on_press2)
    canvas.bind("<ButtonPress-3>",  on_press3)
    canvas.bind("<B1-Motion>",      on_drag)
    canvas.bind("<ButtonRelease-1>",on_release)
    # ウィンドウ全体にイベントをバインド
    flt.bind("<Enter>", on_enter)
    canvas.bind("<Enter>", on_enter)


    canvas.bind_all("<h>", show_help)
    canvas.bind_all("<a>", a_mode)
    canvas.bind_all("<n>", n_mode)
    canvas.bind_all("<w>", w_mode)
    canvas.bind_all("<r>", r_mode)

    canvas.bind_all("<e>", on_escape)
    canvas.bind_all("<c>", cap_image)
    
    # root.focus_set()
    # pyautogui.move(0,-100)
    # import time
    # time.sleep(3)
    # pyautogui.move(0,100)

    # 現在のサイズを保存
    # 初期サイズを保存
    previous_width = root.winfo_width()
    previous_height = root.winfo_height()
    root.mainloop()



thread = None
# thread = threading.Thread(target=show_cap, daemon=True)
# thread.start()



from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk

# グローバル変数としてウィンドウの状態を管理
window = None

# アイコン画像を作成するための関数
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

# 2つの異なるアイコンを作成
icon1_image = create_image(64, 64, 'blue', 'white')
icon2_image = create_image(64, 64, 'red', 'yellow')




def win_start():
    
    global root,flt
    
    root.attributes('-fullscreen', False)
    flt.wm_attributes("-alpha", 1)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
    

import win32gui

def get_window_info(hwnd):
    # ウィンドウの位置とサイズを取得
    rect = win32gui.GetWindowRect(hwnd)
    x, y, width, height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
    return x, y, width, height

def get_foreground_window_info():
    # 現在のフォアグラウンドウィンドウのハンドルを取得
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        return get_window_info(hwnd)
    else:
        return None

def get_uin():
    # 実行例
    window_info = get_foreground_window_info()
    if window_info:
        print(f"X: {window_info[0]}, Y: {window_info[1]}, Width: {window_info[2]}, Height: {window_info[3]}")
        return window_info
    else:
        print("ウィンドウが見つかりませんでした")
        return None



def on_clicked2(icon2, item):
    return

# アイコンをクリックした時のアクション
def on_clicked(icon2, item):

        get_uin()
        
        
        global root,icon,flt
        global thread
        # if root is None:  # ウィンドウが既に存在していないかをチェック
        icon.icon = icon2_image  # アイコンを変更する
        
        
        if thread == None:
            thread = threading.Thread(target=show_cap, daemon=True)
            thread.start()
            print("thread.start")
            # threading.Timer( 0.5, win_start).start()
        else:
            btn_click()
            print("no- - -thread.start")

        # show_window(icon)        # tkinterウィンドウを表示
        # show_cap()
        # thread = threading.Thread(target=show_cap)
        # thread.start()
        # threading.Timer( 0.5, win_start).start()
        # threading.Timer( 0.5, flt.focus_force).start()
        # print("on clicked - on_enter flt.focus_focus")        

        # global flt, sub_win_disp
        # sub_win_disp= False
        # root.attributes('-fullscreen', True)
        # flt.wm_attributes("-alpha", 0.002)  # ウィンドウを透明にする。0にすると完全に透明になるが、クリックが背後に流れてしまう。
        # flt.focus_set()

        return
        
# メニューのアクション
def on_cap_end(icon, item):

    global thread,root

    print("on_cap_end")

    if thread == None:
        return
        
    thread =None
    threading.Timer( 0.1, root.focus_force).start()
    threading.Timer( 0.1, root.quit).start()
    # root.destroy()
    # root.withdraw()

def on_quit(icon, item):
    global root,thread
    
    # root.destroy()
    # root.quit()
    icon.stop()
    thread =None

# アイコンを右クリックしたときのメニューを定義
menu = Menu(
    MenuItem('Capture(ALL)',        on_clicked, default=True),  # デフォルトのクリックアクションを設定
    MenuItem('Capture',             on_clicked2),  # デフォルトのクリックアクションを設定
    MenuItem('Cap終了',             on_cap_end),
    MenuItem('終了',                on_quit)
)

# 初期アイコンを設定してIconオブジェクトを作成
icon = Icon("test_icon", icon1_image, "My Tray Icon", menu)
icon.run()

