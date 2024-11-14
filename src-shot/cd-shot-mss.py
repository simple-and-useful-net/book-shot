
import mss

# 画面全体のショット
with mss.mss() as sct:

    # 全てのモニター
    # One screen shot per monitor
    for filename in sct.save( output="mon-{mon}" ):
        print(filename)

    # ~ Screen shot of the monitor 1　ファイル名は 'monitor-1.png'
    filename = sct.shot()
    print(filename)


    # ~ Screen shot of the monitor 1
    filename = sct.shot(mon=1, output='m{mon}-{date:%Y%m%d-%H%M%S}-fullscreen.png')
    print(filename)

    filename = sct.shot(mon=2, output='m{mon}-{date:%Y%m%d-%H%M%S}-fullscreen.png')
    print(filename)

    # ~ A screen shot to grab them all
    filename = sct.shot(mon=-1, output='m{mon}-{date:%Y%m%d-%H%M%S}-fullscreen.png')
    print(filename)


# 指定範囲のショット
# grabの範囲しては、マルチ画面の全ての画面を合わせた座標
# 辞書型でなく、タプル（左上、右下）可能

from PIL import Image

with mss.mss() as sct:
    # Get information of monitor 2
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"] + 100,  # 100px from the top
        "left": mon["left"] + 0,  # 100px from the left
        "width": 160,
        "height": 135,
    }

    # Grab the data
    sct_img = sct.grab(monitor)

    # (left, top, right, bottom) の形式 左上 ,右下でも可能
    # ~ monitor = (mon["left"] + 0, mon["top"] + 100, mon["left"] +160, 100+135)

    sct_img = sct.grab(monitor)

    output = "img.png"
    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    
    
    # ピクセルデータをPillowのImageオブジェクトに変換
    img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

    # JPEG形式で保存
    # ~ img.save("screenshot.jpg", quality=85)  # qualityを調整可能
    img.save("screenshot.jpg") 

    # BMP形式で保存
    img.save("screenshot.bmp")

    # PNG形式で保存
    img.save("screenshot.png")

