
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from  m_screenshot  import screenshot
from  m_range_qt    import RangeQt


# ~ スクリーンショット
def scrn_shot( e ):
    
    print("scrn_shot", e)

    def wait_shot():
        pos = x1, y1, x2, y2 = window.get_size()
        fn = screenshot(  x1, y1, x2, y2, disp=True )

        # ~ 中央四角をDisp
        window.capture_paint(False)
        

    # 右クリック        
    if e.button() == QtCore.Qt.RightButton:

        # ~ 中央四角を消す
        window.capture_paint(True)
        QtCore.QTimer.singleShot(10, lambda: wait_shot())



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = RangeQt()
    
    # ~ ショット関数を設定
    window.setClickFunc( scrn_shot )
    window.show()

    sys.exit(app.exec_())
