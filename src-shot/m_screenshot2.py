
from    PIL import Image, ImageDraw

import  mss
from    m_get_filename  import  get_filename
from    m_get_cursor import get_cursor



'''
--------------------------------------------------------
   (マルチモニタ)の情報を取得
   引数
       0:すべtのモニタ
        1:メインモニタ
        2以降がサブモニタ
        
   返却値  モニタの　左上座標（ｘ、ｙ）と 幅、高さ
--------------------------------------------------------
'''
def moni_info( mon_no = 0):

    with mss.mss() as sct:
        
        
        monitor = sct.monitors[mon_no] 
        print(f"  左上座標: ({monitor['left']}, {monitor['top']})")
        print(f"  解像度: {monitor['width']}x{monitor['height']}")

        return  monitor['left'],monitor['top'], monitor['width'], monitor['height']



#--------------------------------------------------------
# スクリーンショット
#   (マルチモニタ)

'''
    引数
        左ＸＹ座標
        右下ＸＹ座標
        mon_no
            0:すべtのモニタ
            1:メインモニタ
            2以降がサブモニタ

        disp:
            画像の表示
        fname:
            ファイル名        
'''
#--------------------------------------------------------
def screenshot2( x1, y1, x2=0, y2=0, mon_no= 0, disp=False, fname=None ):

    
    # (マルチモニタ) スクリーンショット
    # 0:すべtのモニタ、1:メインモニタ、2以降がサブモニタ

    with mss.mss() as sct:
        # モニタ情報を取得
        monitor = sct.monitors[mon_no]  
        print(f"  左上の座標: ({monitor['left']}, {monitor['top']})")
        print(f"  解像度: {monitor['width']}x{monitor['height']}")
        
        # 切り取る領域の座標を定義 (左上X, 左上Y, 右下X, 右下Y)
        if x2==0 and y2==0:
            crop_area = {
                "left":   monitor['left'],    # 左上X
                "top":    monitor['top'],     # 左上Y
                "width":  monitor['width'],   # キャプチャする幅
                "height": monitor['height'],  # キャプチャする高さ
            } 
        else:
            x1 += monitor['left']
            x2 += monitor['left']
            y1 += monitor['top']
            y2 += monitor['top']
            print(" x1, y1, x2, y2 == ",  x1, y1, x2, y2 )
            crop_area = {
                "left":   int(x1),     # 左上X
                "top":    int(y1),     # 左上Y
                "width":  int(x2 -x1), # キャプチャする幅
                "height": int(y2-y1), # キャプチャする高さ
            }

        # 指定した範囲をキャプチャ
        screenshot = sct.grab(crop_area)
        # スクリーンショットをPillow Imageに変換
        screenshot = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)

        # カーソルを付ける
        # ~ cursor, (hotspotx, hotspoty), pos = get_cursor()
        # ~ screenshot.paste(cursor, pos, cursor)
    
    
    # 枠（ボーダー）
    border_color = "red"
    border_width = 1
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle([0, 0, screenshot.width - 1, screenshot.height - 1], outline=border_color, width=border_width)
    
    # save file
    if fname == None:
      fname = get_filename("cap","png")
    
    print("filename",fname)
    screenshot.save( fname )

    # スクリーンショットを表示
    if disp:
      screenshot.show()
    
    

if __name__ == "__main__":

    x1, y1, x2, y2 = 0, 0, 700, 700
    screenshot2( x1, y1, x2, y2, mon_no=1 )
  
