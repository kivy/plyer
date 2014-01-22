from plyer import systray
from functools import partial

def my_callback(name):
    print 'Option called:', name

def on_show_settings():
    # add a submenu
    global menu
    systray.menu.insert(1, ('Settings', None, (
        ('Change Color', None, partial(my_callback, 'color')),
        ('Change Size', None, partial(my_callback, 'size')),
        ('Change Pos', None, partial(my_callback, 'pos')))))

    # configure again the systray
    systray.configure(menu=systray.menu)


# show initial menu
def run_systray(*args):
    menu = [
        ('Show settings', None, on_show_settings),
        ('Quit', None, systray.quit)]

    systray.configure(menu=menu, hover_text='Hello cursor!')
    systray.run()


# without threads
#run_systray()

# with threads
import threading
thread = threading.Thread(target=run_systray)
thread.daemon = True
thread.start()
thread.join()

