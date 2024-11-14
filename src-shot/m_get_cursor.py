import ctypes, win32gui, win32ui
from PIL import Image, ImageGrab, ImageDraw

import ctypes
import win32gui
import win32ui
import win32api
import win32con
from PIL import Image



def get_cursor():

    try:    
        hcursor = win32gui.GetCursorInfo()[1]

        # アイコン情報を取得
        icon_info = win32gui.GetIconInfo(hcursor)
        hbmColor = icon_info[4]  # カラービットマップのハンドル
        hbmMask = icon_info[3]   # マスクビットマップのハンドル

        # カラービットマップの情報を取得
        if hbmColor != 0:
            bmp_color = win32ui.CreateBitmapFromHandle(hbmColor)
            bmp_color_info = bmp_color.GetInfo()
            cursor_width = bmp_color_info['bmWidth']
            cursor_height = bmp_color_info['bmHeight']
            print("color")
            cursor_width  *=4
            cursor_height *=4
        else:
            # カラービットマップが無い場合はマスクビットマップを使用
            bmp_mask = win32ui.CreateBitmapFromHandle(hbmMask)
            bmp_mask_info = bmp_mask.GetInfo()
            cursor_width = bmp_mask_info['bmWidth']
            cursor_height = bmp_mask_info['bmHeight']
            print("mask")
            cursor_width  *=4
            cursor_height *=4
            cursor_height = int(cursor_height / 2.0)  # 通常、アイコンの高さは2倍にされることがあるため
        
        # ~ print( "cursor_height", cursor_width, cursor_height)
        

        # カラービットマップがない場合はマスクビットマップを使用
        # ~ if hbmColor == 0:
        # ~ hbmColor = hbmMask

        # ビットマップハンドルが有効か確認
        # ~ if hbmColor == 0:
            # ~ raise Exception("ビットマップハンドルが無効です")


        # カラービットマップのサイズを取得する
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hdc_compatible = hdc.CreateCompatibleDC()

        # カラービットマップの情報を取得
        # ~ bmp = win32ui.CreateBitmapFromHandle(hbmColor)
        # ~ bmpinfo = bmp.GetInfo()
        # ~ cursor_width = bmpinfo['bmWidth']
        # ~ cursor_height = int(bmpinfo['bmHeight'] /2.0)

           
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, cursor_width, cursor_height)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        # ~ hdc.DrawIcon((0,0), hcursor)

        # 背景色を指定
        background_color = win32gui.CreateSolidBrush(win32api.RGB(10, 10, 10))  # 赤色
        # ~ background_color = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))  # 黒
        # ~ win32gui.DrawIconEx(hdc.GetSafeHdc(), 0, 0, hcursor, 0,0, 0, background_color, win32con.DI_IMAGE)
        # ~ win32gui.DrawIconEx(hdc.GetSafeHdc(), 0, 0, hcursor, 36,36, 0, background_color, win32con.DI_NORMAL)
        if hbmColor == 0:
            sx = 0
            sy = 0
        else:
            sx = cursor_width //16
            sy = cursor_height //16
        
        hx,hy= win32gui.GetIconInfo(hcursor)[1:3]
        if hy <2:
            sx =22
            sy =22
        if hy ==9 and hx ==9:
            sx =22
            sy =22
        
        print("sx,sy", sx,sy)
            
        win32gui.DrawIconEx(hdc.GetSafeHdc(), sx, sy, hcursor, cursor_width, cursor_height, 0, background_color, win32con.DI_NORMAL)
        # ~ win32gui.DrawIcon(hdc.GetSafeHdc(), 0, 0, hcursor)

        
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert("RGBA")
        
        # ~ win32gui.DestroyIcon(hcursor)    
        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()




        # ~ im = Image.new('RGB', (500, 300), (128, 128, 128))
        # ~ draw = ImageDraw.Draw(im)
        # ~ draw.ellipse((100, 100, 150, 200), fill=(255, 0, 0), outline=(0, 0, 0))
        # ~ cursor.putalpha(im)




        pixdata = cursor.load()
        width, height = cursor.size
        # ~ print("dbg", width,height)


        '''
        import math
        # 画像の中心を計算
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 3  # 画像の半径の半分程度を円形の半径に設定
        outer_radius = min(width, height) // 2  # 外側の円の半径        
        for y in range(height):
            for x in range(width):
                # ピクセルが円形領域内かどうかを確認
                distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                if distance <= radius:
                    # 条件に合うピクセルを透明度40に変更
                    if pixdata[x, y] == (10, 10, 10, 255):
                        pixdata[x, y] = (100, 100, 100, 200)
                # 内側と外側の円の間の領域を設定
                elif radius < distance <= outer_radius:
                    pixdata[x, y] = (255, 0, 0, 255)  # 色
                        
                else:
                    pixdata[x, y] = (0, 0, 0, 0)
        '''

        width, height = cursor.size
        for y in range(height):
            for x in range(width):

                if pixdata[x, y] == (10, 10, 10, 255):
                    pixdata[x, y] = (0, 0, 0, 0)    # Black


        """
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (10, 10, 10, 255):
                    pixdata[x, y] = (0, 0, 0, 40)    # 白
        
        """
        # 画像サイズを1/2に縮小
        half_size = (cursor.width // 4, cursor.height // 4)
        cursor = cursor.resize(half_size, Image.LANCZOS )  # 高品質な縮小

        # ~ print("hcursor", hcursor)

        hotspot0= win32gui.GetIconInfo(hcursor)


        # ~ print("hotspot0", hotspot0)
        hotspot = hotspot0[1:3]
        
        # ~ x = hotspot[0]
        # ~ y = hotspot[1]

        # 1. 描画用オブジェクトを作成
        # ~ draw = ImageDraw.Draw(cursor, 'RGBA')

        # 2. 円の座標とサイズを設定
        # ~ circle_x0, circle_y0 = x, y  # 円の左上
        # ~ circle_x1, circle_y1 = x+50, y+50  # 円の右下
        # ~ yellow_color = (255, 255, 0, 20)  # 半透明の黄色 (128 は透明度)

        # 3. 円を描画
        # ~ draw.ellipse([circle_x0, circle_y0, circle_x1, circle_y1], fill=yellow_color)



        cursor.save("cursor.png")
        pos_win = win32gui.GetCursorPos()
        (hotspotx, hotspoty) = hotspot
        print( "cursor.width=", cursor.width)
        print( "cursor.height=", cursor.height)
        print( "hotspotx=", hotspotx)
        print( "hotspoty=", hotspoty)
        
        # ~ hotspotx, hotspoty = hotspotx-int(cursor.width/2), hotspoty-int( cursor.heigh/2) 
        # ~ hotspotx, hotspoty = hotspotx-64, hotspoty-64
        # ~ hotspot = hotspotx+32, hotspoty+32

        # ~ pos_win[0] = pos_win[0] 
        # ~ pos_win[1] = pos_win[1]
        ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        pos = (round(pos_win[0]*ratio - (hotspotx *1 )), round(pos_win[1]*ratio - (hotspoty *1)))

    except:
        print("無効なカーソルハンドルです。")
        return None    


    # ~ return (cursor, hotspot)
    return (cursor, hotspot, pos)



if  __name__ == "__main__":


    img = ImageGrab.grab(bbox=None, include_layered_windows=True)

    # ~ pos_win = win32gui.GetCursorPos()
    # ~ cursor, (hotspotx, hotspoty) = get_cursor()
    # ~ cursor.save("cursor.png")

    # ~ ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    # ~ pos = (round(pos_win[0]*ratio - hotspotx), round(pos_win[1]*ratio - hotspoty))
    if get_cursor():
        cursor, (hotspotx, hotspoty), pos = get_cursor()
        img.paste(cursor, pos, cursor)

        img.save("screenshot.png")
