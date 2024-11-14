

from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

state1 = True
state2 = False
state3 = False


def on_clicked1(icon, item):
    global state1
    state1 = not item.checked

def on_clicked2(icon, item):
    global state2
    state2 = not item.checked

def on_clicked3(icon, item):
    global state3
    state3 = not item.checked

def disp_val(icon, item):
    print("state1=", state1)
    print("state2=", state2)
    print("state3=", state3)


menu = Menu(
    MenuItem('表示',  disp_val,visible=False, default=True),

    MenuItem('check1',on_clicked1, checked=lambda item: state1),
    MenuItem('check2',on_clicked2, checked=lambda item: state2),
    MenuItem('check3',on_clicked3, checked=lambda item: state3),
)

image = Image.new('RGB', (64, 64), color='blue')
icon = Icon("test_icon", image, "My Tray Icon", menu)
icon.run()


