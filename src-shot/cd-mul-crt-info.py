'''
    マルチモニターの情報の取得

番号  0
左上座標 -1440, 0
解像度　 3360x1080

番号  1
左上座標 0, 0
解像度　 1920x1080

番号  2
左上座標 -1440, 0
解像度　 1440x900

メインモニタ = 1
モニタ数     = 2

'''
import mss

main_moni = None
with mss.mss() as sct:
    # すべてのモニタ情報を取得
    monitors = sct.monitors
    

    # モニタの情報
    # ix=0は全てのモニタをまとめたもの
    # ix=1は、大抵メインモニタ
    for ix, monitor in enumerate(monitors):
        print(f"番号  {ix}" )
        print(f"左上座標 {monitor['left']}, {monitor['top']}")
        print(f"解像度　 {monitor['width']}x{monitor['height']}")
        print()
        # 座標が (0, 0) メインモニタ
        if monitor["left"] == 0 and monitor["top"] == 0:
            main_moni = ix
    
    print("メインモニタ =", main_moni)
    print("モニタ数     =",len(monitors) -1)

