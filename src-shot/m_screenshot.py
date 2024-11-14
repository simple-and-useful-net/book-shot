
from PIL import Image, ImageDraw, ImageGrab
from m_get_filename import get_filename
from  m_get_cursor import get_cursor


#--------------------------------------------------------
# スクリーンショット
#     (左上座標 x1, y1 右下座標 x2, y2)
#--------------------------------------------------------
def screenshot( x1, y1, x2, y2, fname=None, disp=True, bwidth=0, bcolor="red"):
    
    # スクリーンショット
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    #カーソル表示
    # ~ cursor, (hotspotx, hotspoty), pos = get_cursor()
    # ~ screenshot.paste(cursor, pos, cursor)
    
    
    # 枠追加
    if bwidth != 0:
      draw = ImageDraw.Draw(screenshot)
      draw.rectangle([0, 0, screenshot.width - 1, screenshot.height - 1], outline=bcolor, width=bwidth)
    
    # ファイル保存
    if fname == None:
      fname = get_filename("capture","png")

    print("filename",fname)
    screenshot.save( fname )

    # 表示
    if disp:
      screenshot.show()

    return fname

if __name__ == "__main__":

    x1, y1, x2, y2 = 0, 0, 700, 700
    screenshot( x1, y1, x2, y2, bcolor="green", bwidth=10 )
  
