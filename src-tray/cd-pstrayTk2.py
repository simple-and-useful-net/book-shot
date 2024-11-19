
import tkinter as tk


def close_window():

    print("close_window IN")
    # ~ window.quit()       
    # ~ window.destroy()       
    # ~ window.mainloop()

    # ~ window.withdraw()       
    # ~ 5秒後にウィンドウを表示
    # ~ window.after(5000, window.deiconify)


#----------------------------------------------
#       Tkウィンドウ
#----------------------------------------------
window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', close_window)

# ~ window.withdraw()        #タイトルバーからも消す

# ~ 5秒後にウィンドウを表示
# ~ window.after(5000, window.deiconify)
window.mainloop()
