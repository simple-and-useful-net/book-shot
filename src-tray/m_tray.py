"""
------------------------------------------------------------------------
    


------------------------------------------------------------------------
"""
from pystray import Icon, Menu, MenuItem
from PIL import Image



class tray():

    def __init__(self, image, menu_item, icon_func=None, menu_func=None ):
        

        def on_clicked(icon, item):
            
            # ~ メニュー番号順に処理を作成したいなら、次のコードを使うと便利
            l = len(icon.menu.items)
            for i in range(l):
                # ~ print(i, icon.menu.items[i].text, item.text)
                if icon.menu.items[i].text == item.text:
                    # print("選択された項目,No",item.text, i)
                    break

            if i == 0:
                if icon_func:
                    icon_func()
                else:
                    menu_func( item.text, i )
            else:
                menu_func( item.text, i )

            


        # メニューを定義

        # new_items = [MenuItem( menu_item[i], on_clicked) for i in range( len(menu_item))]
        # 空のリストに MenuItem を動的に追加

        menu_items = []
        
        # アイコンがクリックされた
        if icon_func:
            menu_items.append( MenuItem( '', on_clicked, default=True, visible=False) )
            
        if menu_func:
            for i in range( len(menu_item) ):
                menu_items.append( MenuItem( menu_item[i], on_clicked) )
        

        icon = Icon( "test_icon", image, "My Tray Icon", menu=menu_items)
        # アイコンをバックグラウンド実行
        icon.run_detached()
        
        self.icon = icon        


    def end(self):
        self.icon.stop()



if __name__ == "__main__":

    import subprocess

    def ifunc():
        print("アイコンがクリックされた")
        exe = r'C:\Users\kobay\AppData\Local\Programs\Python\Python311\pythonw.exe "C:\Users\kobay\ok-cap-qt\qt01.py"'
        
        subprocess.run(exe)


        
    def ev_func( name, no ):
        
        print( "menyu-no", no)
        if name == "終了":
            inst.end()
            
        if name == "run1":

            exe = "test.bat"
            exe = r"C:\Users\kobay\Desktop\ok-cap.exe"
            subprocess.run(exe)



        if name == "run2":

            exe = r'C:\Users\kobay\AppData\Local\Programs\Python\Python311\pythonw.exe "C:\Users\kobay\ok-cap-qt\qt01.py"'
            subprocess.run(exe)



    # アイコンをトレイに表示
    image = Image.new('RGB', (64, 64), color='blue')
    mn = [  
            "run1",
            "run2",
            "item30",
            "終了"
            ]
            
    inst = tray( image, mn, icon_func= ifunc, menu_func=ev_func )
    # inst = tray( image, mn, icon_func= ifunc)
    # inst = tray( image, mn, menu_func=ev_func )
        
