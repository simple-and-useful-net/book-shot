from PIL import ImageGrab

# スクリーンショットの範囲を指定しない場合は、画面全体をキャプチャ
screenshot = ImageGrab.grab()
screenshot.save("full.jpg")

# キャプチャ範囲の指定 (左上の座標 x1, y1 と 右下の座標 x2, y2)
x1, y1, x2, y2 = 100, 100, 500, 400
screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    
# スクリーンショットを保存
screenshot.save("test.png")

import datetime
now = datetime.datetime.now()
fname = f"{now:%y%m%d-%H%M%S}"
print(fname)
screenshot.save(fname + ".bmp")
