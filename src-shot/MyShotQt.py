import sys
from PyQt5 import QtWidgets, QtGui, QtCore

import ctypes
import win32gui
import win32con
import win32api

from  m_screenshot  import screenshot
from  m_screenshot2 import screenshot2,moni_info

# g_mon_no      = int(input("モニタ番号"))
# g_screen_all  = input("スクリーン全体 (y/n)")

g_mon_no      = 0

'''
マルチモニタの構成
 モニタは2で、 右側には サブモニタ 左側には メインモニタ

'''

'''
エスケープキーが押された場合は、画面をキャプチャーします。

  キャプチャーする範囲は次のようになります 

 そして プログラムを終了させます。
    
'''

from PIL import Image
import win32clipboard
import io

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



class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setGeometry(100, 100, 1000, 800)
        self.setMouseTracking(True)

        # マウス操作のためのフラグ
        self.is_resizing        = False
        self.drag_start_position= None
        self.dire               = None

        # リサイズ領域のマージン
        self.margin = 10

        # 中央の移動領域
        self.center_rect_size = 30  # 中央に描画する四角のサイズ
        self.center_dragging = False  # 中央の四角をドラッグしているかどうかのフラグ

        self.menu = self.create_menu()
        self.menu_visible = False  # メニューの表示状態を管理

        self.show_rect = True

        # タイマーの設定
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_window)
        self.tm_sw  = False
        self.tm     = 0
        self.fname  = ""
        
        # ~ ダブルクリックによりウィンドウを小さくする
        self.dbl_size   = 0
        self.dbl_x      = 0
        self.dbl_y      = 0
        self.dbl_x2     = 0
        self.dbl_y2     = 0
        
        # ~ 図形モード   (図形、撮影)
        self.モード     = "撮影"
        self.rect_sw= False
        self.rect_x = []
        self.rect_y = []
        self.rect_w = []
        self.rect_h = []

        # 枠の太さ
        self.waku_w =10
        self.waku   =  self.waku_w -1

        self.file_img_sw = False


    def openImage(self, filepath):
        img = QtGui.QImage()
        
        # 画像ファイルの読み込み
        if not img.load(filepath):
            return False

        # QImage -> QPixmap
        self.pixmap = QtGui.QPixmap.fromImage(img)
        return True
        
    def start_timer(self, tm ):

        self.tm = tm
        self.tm_sw = True
        self.fname = ""
        
        self.timer.start(1000)  # 1000msごとにウィンドウを更新
        # ~ QtCore.QTimer.singleShot( (tm+1)*1000, self.stop_timer)  # 5秒後に停止
        print("start_timer", self.tm, self.tm_sw)

    def update_window(self):
        self.update()  # ウィンドウを更新
        print("kita", self.tm)
        if self.fname != "":
            self.stop_timer()
            
    def stop_timer(self):
        self.timer.stop()  # タイマーを停止
        self.tm_sw = False
        print("stop_timer", self.tm, self.tm_sw)
                
    def keyPressEvent(self, event):
        # Escキーを検知
        # ~ if event.key() == QtCore.Qt.Key_Escape:
            # ~ self.close()  # ウィンドウを閉じる（アプリを終了させる）
        self.図形編集()


    def clr_menu_visible(self):
        self.menu_visible = False  # メニューの表示状態(非表示)

    def shot(self, disp, wait):
        x1, y1, x2, y2  = self.get_size()
        # ~ self.fname = screenshot( x1, y1, x2, y2, disp=disp, fname="cap.png")        
        # ~ self.fname = screenshot( x1, y1, x2, y2, disp=disp, bwidth=90, bcolor="red")  
        self.fname = screenshot( 
            x1+ self.waku, y1+ self.waku, x2- self.waku, y2- self.waku, disp=disp)  
        to_clip(self.fname)
        
        if wait:
            self.openImage(self.fname)
            self.file_img_sw = False
            
            self.図形編集()
            self.show_rect = True
        else:
            self.show_rect = True
            self.update()
            
        self.menu_visible = False  # メニューの表示状態を管理
            

    def capture(self, disp=False, wait=False):

        # ~ 画面更新（いらないものを消す作業）に時間が係るために
        self.show_rect = False
        self.tm_sw     = False   
        self.update()

        # QTimerの設定
        QtCore.QTimer.singleShot(10, lambda: self.shot(disp,wait))
        # ~ QtCore.QTimer.singleShot(10, lambda:self.clr_menu_visible())

    def wait_capture(self):

        # QTimerの設定
        tm = 5
        self.start_timer(tm)
        QtCore.QTimer.singleShot( tm*1000, lambda: self.capture(disp=False,wait=True))
        # ~ QtCore.QTimer.singleShot(10, lambda:self.clr_menu_visible())

        
    def clr_file_name(self):
        
        self.rect_x.clear()
        self.rect_y.clear()
        self.rect_w.clear()
        self.rect_h.clear()

        self.fname = ""
        self.update()
        QtCore.QTimer.singleShot(10, lambda:self.clr_menu_visible())
        

    def cap_edit(self):
        if self.file_img_sw:
            self.file_img_sw = False
            self.zuke.setText("Capture")  # Change the label dynamically
        else:
            self.file_img_sw = True
            self.zuke.setText("図形編集")  # Change the label dynamically
        
        self.update()
        QtCore.QTimer.singleShot(10, lambda:self.clr_menu_visible())
        
    def 図形編集(self):
        
        text = self.zuke.text()     # Get the current text of the QAction
        if text == "図形編集":
            print("図形編集")
            self.zuke.setText("Capture")  # Change the label dynamically
            self.update()            
        else:
            print("Capture")
            self.zuke.setText("図形編集")  # Change the label dynamically

            self.file_img_sw =False

            self.rect_x.clear()
            self.rect_y.clear()
            self.rect_w.clear()
            self.rect_h.clear()

            self.fname = ""
            self.update()            

        QtCore.QTimer.singleShot(10, lambda:self.clr_menu_visible())

    def create_menu(self):
        """メニューを作成する"""
        menu = QtWidgets.QMenu(self)
        menu.addAction("キャプチャ",         lambda:self.capture())
        menu.addAction("キャプチャ(表示)",   lambda:self.capture(True))
        menu.addAction("キャプチャ(遅延)",   lambda:self.wait_capture())
        menu.addAction("遅延画像の編集",     lambda:self.cap_edit())
        
        self.zuke = menu.addAction("図形編集",     lambda:self.図形編集())
        menu.addAction("クリア",               lambda:self.clr_file_name())
        menu.addAction("終了",                self.close)
        return menu







    """ 描画   """
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # 画像を描画する
        if self.file_img_sw and self.fname != "":
            painter.drawPixmap(0, 0, self.pixmap)

        # ここで図形を表示させる
        painter.setPen(QtGui.QPen(QtGui.QColor("red"), 3))
        l = len( self.rect_x )
        for i in range(l):    
            painter.drawRect( self.rect_x[i], self.rect_y[i], self.rect_w[i], self.rect_h[i])

        if self.zuke.text()  == "Capture":
            # 外枠の描画
            # 背景はイベント取得が可能（図形描画用）
            painter.setPen(QtGui.QPen(QtGui.QColor("pink"), self.waku_w))
            painter.setBrush(QtGui.QColor(255, 255, 255, 1))  # 透明
            painter.drawRect(0, 0, self.width(), self.height())
        else:
            # 透明（範囲指定）
            painter.setPen(QtGui.QPen(QtGui.QColor("palegreen"), self.waku_w))
            painter.setBrush(QtCore.Qt.NoBrush)  # NoBrush for no fill            
            painter.drawRect(0, 0, self.width(), self.height())


        if self.show_rect:  #　描画
            if self.zuke.text()  == "Capture":
                # 背景はイベント取得が可能（図形描画用）
                pass
            else:
                # 透明（範囲指定）
                # 中央の四角の描画
                center_x = (self.width() - self.center_rect_size) // 2
                center_y = (self.height() - self.center_rect_size) // 2
                
                painter.setPen(QtCore.Qt.NoPen)  # ペンなし（枠なし）        
                color = QtGui.QColor("palegreen")
                # ~ color.setAlpha(100)  # アルファ値（透明度）を100に設定            
                painter.setBrush( color ) 
                painter.drawRect(center_x, center_y, self.center_rect_size, self.center_rect_size)

                if self.fname  != "":
                    color = QtGui.QColor("black")
                    painter.setBrush( color ) 
                    painter.drawRect(center_x-100, center_y+50, 300, self.center_rect_size)

                    time_text = f"saveOK ({self.fname})"

                else:                            
                    time_text = ""

                # QFontを設定
                font = QtGui.QFont("Arial", 16)     # フォント名とサイズ
                font.setBold(True)                  # 太字に設定
                painter.setFont(font)               # painterにフォントを設定            
                painter.setPen(QtGui.QColor("white"))  # テキストの色を黒に設定
                painter.drawText(center_x-100, center_y+50, 300, self.center_rect_size, QtCore.Qt.AlignCenter, time_text)


        print("------------------------self.tm =", self.tm, self.tm_sw )
        if self.tm_sw:
            # タイマーの表示時間

            # 中央の四角の描画
            center_x = (self.width() - self.center_rect_size) // 2
            center_y = (self.height() - self.center_rect_size) // 2

            # QFontを設定
            font = QtGui.QFont("Arial", 16)     # フォント名とサイズ
            font.setBold(True)                  # 太字に設定
            painter.setFont(font)               # painterにフォントを設定            
            painter.setPen(QtGui.QColor("black"))  # テキストの色を黒に設定

            if self.tm >= 0:            
                time_text = str( self.tm )
                painter.drawText(center_x, center_y, self.center_rect_size, self.center_rect_size, QtCore.Qt.AlignCenter, time_text)
                self.tm -= 1



    def mouseDoubleClickEvent( self, event):
        
        print("------------------mouseDoubleClickEvent", event)


        if self.dbl_size  == 0:
            self.dbl_size =1
            self.dbl_x, self.dbl_y, self.dbl_x2, self.dbl_y2 = self.get_size()
            self.setGeometry(10, 10, 50, 50)
        else:
            self.dbl_size =0
            w = self.dbl_x2 - self.dbl_x
            h = self.dbl_y2 - self.dbl_y
            self.setGeometry(self.dbl_x, self.dbl_y, w, h)
        
    """     マウスクリック    """
    def mousePressEvent(self, event):

        print("mousePressEvent", event)
        self.is_resizing        = False
        self.center_dragging    = False

        # 左クリック        
        if event.button() == QtCore.Qt.LeftButton:

            if self.menu_visible:
                print("メニューが表示中に右クリック（消える）")
                self.menu_visible =False
                return

            # ~ 図形編集の場合は、
            if self.zuke.text() == "Capture":
                self.rect_sw = True

                x = event.globalPos().x()  - self.frameGeometry().topLeft().x()
                y = event.globalPos().y()  - self.frameGeometry().topLeft().y()
                self.rect_x.append(x) 
                self.rect_y.append(y) 
                self.rect_w.append(0) 
                self.rect_h.append(0) 
                print("----- move", self.rect_x, self.rect_y, self.rect_w, self.rect_h)
            else:
                self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()

                if self.chk_center_rect(event.pos()):
                    self.center_dragging = True
                else:
                    self.dire = self.resize_dire(event.pos())
                    if self.dire:
                        self.is_resizing = True

        # 右クリック （メニューをpopup）       
        if event.button() == QtCore.Qt.RightButton:
            
            if self.menu_visible:
                print("menu.close")
                self.menu.close()
                self.menu_visible = False
            else:
                print("menu.exec")
                menu_pos = self.mapToGlobal(QtCore.QPoint(
                                        (self.width() - self.center_rect_size) // 2  +25, 
                                        (self.height() - self.center_rect_size) // 2 + 25))
                self.menu.exec_(menu_pos)
                self.menu_visible = True


    """     マウス移動    """
    def mouseMoveEvent(self, event):
        print("mouseMoveEvent", self.center_dragging)

        # ~ 図形編集の場合は、
        if self.zuke.text() == "Capture":

            if self.rect_sw:
                l = len(self.rect_x)
                w = event.globalPos().x() - self.rect_x[l-1]  - self.frameGeometry().topLeft().x()          
                h = event.globalPos().y() - self.rect_y[l-1]  - self.frameGeometry().topLeft().y()    
                print("----- move", self.rect_x,l,w,h)
                self.rect_w[l-1]    = w
                self.rect_h[l-1]    = h
                    
                self.update()
        else:
        
            if self.center_dragging:
                self.move(event.globalPos() - self.drag_start_position)

            elif self.is_resizing and self.dire:
                self.resize_window(event.globalPos())

            else:
                print("mouseMoveEvent-2", event.pos())


    """     マウス　リリース    """
    def mouseReleaseEvent(self, event):

        print("mouseReleaseEvent", event)
        self.is_resizing        = False
        self.center_dragging    = False

        self.rect_sw             = False


    """ 領域の出入でカーソルを変更   """
    def enterEvent(self, event):
        
        if self.zuke.text() == "Capture":
            self.setCursor(QtCore.Qt.ArrowCursor)  # マウスボタンを離したらカーソルを戻す
        else:
            """中央の四角にマウス 移動カーソル"""
            if self.chk_center_rect(event.pos()):
                self.setCursor(QtCore.Qt.OpenHandCursor)  # 移動カーソル
            else:    
                self.dire = self.resize_dire(event.pos())
                if self.dire != None:
                    self.update_cursor( self.dire )

    def leaveEvent(self, event):
        if self.zuke.text() == "Capture":
            self.setCursor(QtCore.Qt.ArrowCursor)  # マウスボタンを離したらカーソルを戻す
        else:
            self.setCursor(QtCore.Qt.BlankCursor)  # カーソルなし


    """ リサイズ方向を取得  """
    def resize_dire(self, pos):

        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        margin = self.margin

        if x <= margin and y <= margin:
            return '左上'
        elif x >= w - margin and y <= margin:
            return '右上'
        elif x <= margin and y >= h - margin:
            return '左下'
        elif x >= w - margin and y >= h - margin:
            return '右下'

        elif y <= margin:
            return '上横'
        elif y >= h - margin:
            return '下横'
        elif x <= margin:
            return '左縦'
        elif x >= w - margin:
            return '右縦'
        else:
            return None

    """ リサイズ方向によりカーソル変更"""
    def update_cursor(self, direction):
        
        if direction in ['左上', '右下']:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif direction in ['右上', '左下']:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif direction in ['上横', '下横']:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif direction in ['左縦', '右縦']:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)


    """ リサイズ処理      """
    def resize_window(self, global_pos):

        new_rect = self.frameGeometry()

        if self.dire == '左上':
            new_rect.setTopLeft(global_pos)
        elif self.dire == '右上':
            new_rect.setTopRight(global_pos)
        elif self.dire == '左下':
            new_rect.setBottomLeft(global_pos)
        elif self.dire == '右下':
            new_rect.setBottomRight(global_pos)
        elif self.dire == '上横':
            new_rect.setTop(global_pos.y())
        elif self.dire == '下横':
            new_rect.setBottom(global_pos.y())
        elif self.dire == '左縦':
            new_rect.setLeft(global_pos.x())
        elif self.dire == '右縦':
            new_rect.setRight(global_pos.x())

        self.setGeometry(new_rect)


    """     中央四角の判定     """
    def chk_center_rect(self, pos):

        center_x = (self.width() - self.center_rect_size) // 2
        center_y = (self.height() - self.center_rect_size) // 2
        crect = QtCore.QRect(center_x, center_y, self.center_rect_size, self.center_rect_size)
        return crect.contains(pos)

    """     領域サイズ取得    """
    def get_size(self):
        rect = self.frameGeometry()
        
        # 左上の座標
        top_x = rect.topLeft().x()
        top_y = rect.topLeft().y()        
        # 右下の座標
        bottom_x = rect.bottomRight().x()
        bottom_y = rect.bottomRight().y()        
        
        return top_x,top_y, bottom_x,bottom_y



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()

    sys.exit(app.exec_())
