
from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class RangeQt(QtWidgets.QWidget):
    def __init__(self):
        
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # ~ self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setGeometry(100, 200, 600, 600)
        # ~ mouseMoveした場合の位置を知りたい場合はTrueにする
        # ~ 指定が無い場合は、ドラッグ移動の場合だけ、mouseMoveEventが発生
        # ~ self.setMouseTracking(True)

        # マウス操作のためのフラグ
        self.is_resizing        = False
        self.center_offset= None
        
        # ~ ポンターが外枠のどの部分にいるか判定
        # ~ 場所により、上下左右、四隅（４箇所）を漢字で設定
        self.resize_point       = None

        # リサイズ領域のマージン
        self.margin = 10
        
        # 枠の幅
        self.waku_w = 8

        # 中央の移動領域
        self.center_rect_size = 20  # 中央に描画する四角のサイズ
        self.is_moving = False  # 中央の四角をドラッグしているかどうかのフラグ

        # ~ ショット時に、中央四角は表示させない
        self.shot_sw    = False
        
        # ~ クラス外の関数の設定
        self.func =None


    '''
        ショットでは中央の四角は消します
        その為のメソッド

        capture_paint(True)

        wait（再描画に時間がかかる）
        ショット関数

        capture_paint(False)
    '''
    def capture_paint(self, flag=True):
        
        self.shot_sw = flag
        self.update()
                

    """ 描画   """
    def paintEvent(self, event):
        
        # ~ print( "shot_sw=", self.shot_sw )
        painter = QtGui.QPainter(self)

        color = QtGui.QColor("palegreen")
        color.setAlpha(200)                              # アルファ値（透明度）を100に設定 （0:透明）           
        # 外枠
        pen = QtGui.QPen(color, self.waku_w)  # 線で太さ waku_w の線        
        # ~ pen.setStyle(QtCore.Qt.DotLine)     # 点線に設定
        painter.setPen( pen )
        painter.drawRect(0, 0, self.width(), self.height())


        if self.shot_sw:
            # ~ print("paint Capture")
            return
            

        # 中央の四角の描画
        center_x = (self.width() - self.center_rect_size) // 2
        center_y = (self.height() - self.center_rect_size) // 2
        
        painter.setPen(QtCore.Qt.NoPen)     # ペンなし（枠なし）        
        painter.setBrush( color )           # 塗りつぶし
        painter.drawRect(center_x, center_y, self.center_rect_size, self.center_rect_size)


    def setClickFunc(self, func):
        
        self.func = func


    # ~ ダブルクリックで終了
    def mouseDoubleClickEvent( self, event):
        self.close()
        
        
        
    """     マウスクリック    """
    '''
        中央の四角の領域でクリックされたら、is_moving Trueにする
        リサイズの方向（リサイズのカーソルが現れている状態）は
        is_resizing　がTrue
    '''
    def mousePressEvent(self, event):

        print("mousePressEvent", event)

        if self.func != None:
            self.func(event)
            
        self.is_resizing        = False
        self.is_moving    = False

        # 左クリック        
        if event.button() == QtCore.Qt.LeftButton:

                if self.chk_center_rect(event.pos()):
                    self.is_moving = True
                    self.center_offset = event.globalPos() - self.frameGeometry().topLeft()
                else:
                    # ~ self.resize_point = self.chk_outer_frame(event.pos())
                    # ~ resize_pointはクリック前に設定されているはず
                    if self.resize_point:
                        self.is_resizing = True



    """     マウス移動    """
    '''
        このイベントはドラッグしている場合に発生
        ウィンドウ移動の場合は、is_moving がTrue
        resizeの場合は、is_resizing がTrue
    '''
    def mouseMoveEvent(self, event):
            print("mouseMoveEvent", event)

            # ~ print("mouseMoveEvent", self.is_moving)
            # ~ print("event.globalPos()=", event.globalPos())
            # ~ print("event.pos()=", event.pos())
        
            if self.is_moving:
                move_pos = event.globalPos() - self.center_offset
                # ~ print("self.center_offset=", self.center_offset)
                # ~ print("move_pos=", move_pos)
                self.move( move_pos )

            elif self.is_resizing:
                self.resize_window(event.globalPos())

            # ~ else:
                # ~ print("mouseMoveEvent-2", event.pos())


    """     マウス　リリース    """
    def mouseReleaseEvent(self, event):

            print("mouseReleaseEvent", event)
            self.is_resizing        = False
            self.is_moving    = False



    """ 領域の出入でカーソルを変更   """
    '''
        中央の四角に入ったら、マウスを移動カーソルにする
        外枠の場合は、どの部分にいるかを判定してから、
        カーソル形状を変更
        
    '''
    def enterEvent(self, event):
        
        print( "enterEvent", event )
        print( "pos,(type)", event.pos(), type(event.pos()) )
        print( "x,y(type)=", event.pos().x(), event.pos().y(), type(event.pos().y()))
        print( "globalPos,(type)", event.globalPos(), type(event.globalPos()) )
        print( "x,y=", event.globalPos().x(), event.globalPos().y(), type(event.globalPos().y()))

        """中央の四角にマウス 移動カーソル"""
        if self.chk_center_rect(event.pos()):
            self.setCursor(QtCore.Qt.OpenHandCursor)  # 移動カーソル
        else:    
            self.resize_point = self.chk_outer_frame(event.pos())
            print( "resize_point", self.resize_point )
            if self.resize_point:
                self.update_cursor( self.resize_point )

    def leaveEvent(self, event):
        
        print( "leaveEvent", event )
        self.setCursor(QtCore.Qt.BlankCursor)  # カーソルなし


    '''
        カーソル位置から、外枠のどの部分なのかを判定する
    　（左、右、上、下、四隅）
    '''
    def chk_outer_frame(self, pos):

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
            return '上'
        elif y >= h - margin:
            return '下'
        elif x <= margin:
            return '左'
        elif x >= w - margin:
            return '右'
        else:
            return None

    """ カーソル形状の変更"""
    def update_cursor(self, resize_point):
        
        if resize_point in ['左上', '右下']:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif resize_point in ['右上', '左下']:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif resize_point in ['上', '下']:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif resize_point in ['左', '右']:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)


    """ リサイズ処理      """
    def resize_window(self, global_pos):

        new_rect = self.frameGeometry()
        # ~ print("new_rect", new_rect, new_rect.height())
        # ~ print(self.resize_point, global_pos.y())
        
        if self.resize_point == '左上':
            new_rect.setTopLeft(global_pos)
        elif self.resize_point == '右上':
            new_rect.setTopRight(global_pos)
        elif self.resize_point == '左下':
            new_rect.setBottomLeft(global_pos)
        elif self.resize_point == '右下':
            new_rect.setBottomRight(global_pos)
        elif self.resize_point == '上':
            new_rect.setTop(global_pos.y())
        elif self.resize_point == '下':
            new_rect.setBottom(global_pos.y())
        elif self.resize_point == '左':
            new_rect.setLeft(global_pos.x())
        elif self.resize_point == '右':
            new_rect.setRight(global_pos.x())

        if new_rect.height() < self.center_rect_size*2:
                print("NG-height")
                return
        if new_rect.width() < self.center_rect_size*2:
                print("NG-width")
                return

        self.setGeometry(new_rect)


    """     中央領域内の判定     """
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

    window = RangeQt()
    window.show()

    sys.exit(app.exec_())
