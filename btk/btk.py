from tkinter import *
import threading

PAGES = []

class BTk(Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        threading.Thread.daemon = True
    
    def create_action(self, function, **kwargs):
        thread = threading.Thread(target=function, **kwargs)
        return thread
    
    def mainloop(self, n: int = 0) -> None:
        for page in PAGES:
            for widget in page.widgets:
                page.widgets[widget][-1] = bool(page.widgets[widget][0].winfo_ismapped()) # Ne marche pas pour l'instant :(
        return super().mainloop(n)

class Frame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.propagate(0)
        self.widgets = {}
        PAGES.append(self)

    def cwidget(self, widget_type, name=False, **kwargs):
        widget = widget_type(self, **kwargs)
        if not name:
            self.widgets[f"w{len(self.widgets)}"] = [widget, {k: v[-1] for k, v in widget.config().items() if k in kwargs.keys()}, False]
        else:
            self.widgets[name] = [widget, {k: v[-1] for k, v in widget.config().items() if k in kwargs.keys()}, False]
        return widget
    

    def refresh(self):
        """
        Reprendre les elements enregistrer dans self.widgets pour refresh la page
        Redonner les paramètres initiales
        """
        for widget in self.widgets.values():
            widget[0].config(**widget[1])
        return True


def on_click(event, element, **kwargs):
    element.config(**kwargs)

def hover(event, element, **kwargs):
    element.config(**kwargs)