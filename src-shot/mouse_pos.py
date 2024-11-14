import pyautogui
import keyboard
import time

print("開始位置を設定するには 's' キーを、終了位置を設定するには 'e' キーを押してください。")
print("終了するには Ctrl+C を押してください。")

start_pos = None
end_pos = None

try:
    while True:
        # マウスの現在の位置を取得
        x, y = pyautogui.position()
        
        # 現在のマウス位置を表示
        current_position = f"現在のマウス位置: X={x:04}, Y={y:04}"

        # スタート位置とエンド位置をもとにtop, left, width, heightを計算
        if start_pos and end_pos:
            top = min(start_pos[1], end_pos[1])
            left = min(start_pos[0], end_pos[0])
            width = abs(end_pos[0] - start_pos[0])
            height = abs(end_pos[1] - start_pos[1])
            #positions = f" start(top={top:04}, left={left:04}, width={width:04}, height={height:04})"
            positions = f"{top:04},{left:04},{width:04},{height:04}"
            
            with open("pos.txt", "w") as file:
              file.write(f"{positions}\n")
              file.flush()  # すぐにファイルに書き込む
            break
        else:
            positions = ""

        print(f"{current_position}{positions}", end="\r")
    
    

        # 's' キーが押されたらスタート位置を設定
        if keyboard.is_pressed('s'):
            start_pos = (x, y)
            print(f"\nスタート位置が設定されました: start({x:04}, {y:04})")
            time.sleep(1)  # 再度押されるのを防ぐためのスリープ

        # 'e' キーが押されたらエンド位置を設定
        if keyboard.is_pressed('e'):
            end_pos = (x, y)
            print(f"\nエンド位置が設定されました: end({x:04}, {y:04})")
            time.sleep(1)  # 再度押されるのを防ぐためのスリープ

        time.sleep(0.1)  # CPU使用率を下げるための短いスリープ
except KeyboardInterrupt:
    print("\n終了します。")
