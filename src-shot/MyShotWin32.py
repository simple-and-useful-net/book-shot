import ctypes
import win32api
import win32con
import win32gui
import time
import threading


from  m_screenshot  import screenshot


def capture( x1, y1, x2, y2, win_disp=False ):
    fn = screenshot(  x1, y1, x2, y2, disp=win_disp )
    print( "x1, y1, x2, y2=", x1, y1, x2, y2, fn)



class OverlayWindow:
    def __init__(self):
        self.hwnd = None
        self.target_hwnd = None
        self.sv_target_hwnd =None
        
    def create_window(self):
        # ウィンドウクラスを定義
        wnd_class = win32gui.WNDCLASS()
        wnd_class.lpfnWndProc = self.wnd_proc  # ウィンドウプロシージャ
        wnd_class.lpszClassName = "TransparentWindow"
        wnd_class.hInstance = win32api.GetModuleHandle(None)

        # ウィンドウクラスを登録
        win32gui.RegisterClass(wnd_class)

        # スクリーンの幅と高さを取得
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        print(screen_width, screen_height)
        self.sx1= 0
        self.sy1= 0
        self.sx2= screen_width
        self.sy2= screen_height
        
        # ウィンドウを作成
        self.hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
            wnd_class.lpszClassName,
            "OverlayWindow",
            win32con.WS_POPUP,
            0, 0, screen_width, screen_height,
            None, None, wnd_class.hInstance, None
        )

        # ウィンドウを透明にする
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0x000000, 255, win32con.LWA_COLORKEY)

        # ウィンドウを表示
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_ERASEBKGND:
            # 背景の消去を防止
            return 1  # 背景を消さない

        if msg == win32con.WM_PAINT:

            hdc, _ = win32gui.BeginPaint(hwnd)


            rect = win32gui.GetClientRect(hwnd)  # クライアント領域のサイズを取得
            # 背景を塗りつぶす (ウィンドウ全体)
            win32gui.FillRect(hdc, rect, win32gui.GetStockObject(win32con.BLACK_BRUSH))


            if self.target_hwnd:
                # ターゲットウィンドウの座標を取得
                rect = win32gui.GetWindowRect(self.target_hwnd)
                
                # まず白い枠を描画して背景を塗りつぶす
                brush = win32gui.GetStockObject(win32con.BLACK_BRUSH)  # 塗りつぶす
                win32gui.SelectObject(hdc, brush)
                # ~ win32gui.PatBlt(hdc, rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1], win32con.PATCOPY)
                # ~ x1 = self.sx1
                # ~ y1 = self.sy1
                # ~ x2 = self.sx2
                # ~ y2 = self.sy2
                # ~ win32gui.Rectangle(hdc, x1, y1, x2, y2 )

                # その後、赤い枠を描画
                pen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 200, 100))  # 赤い枠線
                win32gui.SelectObject(hdc, pen)
                
                # 対象ウィンドウの外枠に赤い枠線を描画
                win32gui.Rectangle(hdc, rect[0], rect[1], rect[2], rect[3])
                self.sx1= rect[0]
                self.sy1= rect[1]
                self.sx2= rect[2]
                self.sy2= rect[3]

                win32gui.DeleteObject(pen)

            win32gui.EndPaint(hwnd, _)

            # 描画領域を無効化して再描画を強制
            # ~ win32gui.InvalidateRect(hwnd, None, True)
            # ~ win32gui.UpdateWindow(hwnd)
            return 0  # 正常に処理した場合は 0 を返す

        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0  # 正常に処理した場合は 0 を返す
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def track_pointer_position(self):
        while True:
            
            # Shiftキーが押されているか確認
            if win32api.GetAsyncKeyState(win32con.VK_SHIFT) & 0x8000:
                print("Shiftキーが押されています", flush=True)
                r = win32gui.GetWindowRect(self.target_hwnd)

                x1 = r[0]
                y1 = r[1]
                x2 = r[2]
                y2 = r[3]
                capture( x1,y1, x2,y2, win_disp=True )

            # Controlキーが押されているか確認
            if win32api.GetAsyncKeyState(win32con.VK_CONTROL) & 0x8000:
                print("Controlキーが押されています", flush=True)            

            x, y = win32api.GetCursorPos()
            
            
            # ポインター位置下のウィンドウハンドルを取得
            self.target_hwnd = win32gui.WindowFromPoint((x, y))
            if not self.target_hwnd:
                print("ポインター下にあるウィンドウが見つかりません", flush=True)
            else:
                print(f"取得したウィンドウハンドル: {self.target_hwnd}", end ="\r")

                if self.sv_target_hwnd != self.target_hwnd:
                    # 描画領域を無効化して再描画を強制
                    win32gui.InvalidateRect(self.hwnd, None, True)
                    win32gui.UpdateWindow(self.hwnd)
                else:
                    rect = win32gui.GetWindowRect(self.target_hwnd)
                    if rect[0] == self.sx1 and \
                        rect[1] == self.sy1 and \
                        rect[2] == self.sx2 and \
                        rect[3] == self.sy2:
                            pass
                    else:
                        # 描画領域を無効化して再描画を強制
                        win32gui.InvalidateRect(self.hwnd, None, True)
                        win32gui.UpdateWindow(self.hwnd)
                
                self.sv_target_hwnd = self.target_hwnd


            time.sleep(0.1)  # 更新頻度を調整可能

    def run(self):
        # 透過ウィンドウの作成
        self.create_window()

        # 別スレッドでポインター位置の追跡を開始
        tracking_thread = threading.Thread(target=self.track_pointer_position)
        tracking_thread.daemon = True  # メインスレッドが終了したら自動的に終了するように設定
        tracking_thread.start()

        # ウィンドウのメッセージループ
        win32gui.PumpMessages()

# メイン関数
if __name__ == "__main__":
    overlay = OverlayWindow()
    overlay.run()
