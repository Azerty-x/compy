from btk.btk import *
import os
import winpty
import queue
import re
import lin

os.environ['HOME'] = f'/home/{os.getlogin()}'

class Client(BTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.state("zoomed")
        self.config(bg="#303445")


root = Client()

linux_logo = PhotoImage(file="./assets/linux.png")
git_logo = PhotoImage(file="./assets/git.png")
code_logo = PhotoImage(file="./assets/code.png")
app_logo = PhotoImage(file="./assets/logo.png")
settings_logo = PhotoImage(file="./assets/settings.png")
folder_bloc_img = PhotoImage(file="./assets/folder.png")
chevrondown = PhotoImage(file="./assets/chevrondown.png")
esd = PhotoImage(file="./assets/py.png")
x = PhotoImage(file="./assets/x.png")

right_bloc = Frame(root, width=1920-370, height=1010, bg="#303445")

terminal_fr = Frame(right_bloc, width=1920-370, height=370, bg="#292C3B")
terminal_fr.pack(side=BOTTOM, anchor=SE)
text = lin.LinuxShell(terminal_fr)
text.pack(side=BOTTOM)


onglets = Frame(right_bloc, width=1920-370, height=30, bg="#292C3B")
onglets.pack(side=TOP, anchor=N)

ee = ["test.py", "patate.py", "cxv.py", "aze", "sqddsqdqsd"]
r = 0


for e in range(len(ee)):
    r += len(ee[e-1])*10+50 if e > 0 else 0
    onglet = lin.Onglet(onglets, text=ee[e], img=esd, close_img=x)
    onglet.pack(side=LEFT)

# for e in range(len(ee)):
#     onglet = Canvas(onglets, width=len(ee[e])*10+50, height=30, background="#21232F", highlightthickness=0, cursor="hand2")
#     r += len(ee[e-1])*10+50 if e > 0 else 0
#     print(r, ee[e-1])
#     onglet.place(x=r if e > 0 else 0, y=0)
#     onglet.create_image(15, 15 , image=esd)
#     onglet.create_text(30, 15, text=ee[e], fill="white", font=("Monospace", 10), anchor=W)
#     onglet.create_image((len(ee[e])*10+50)-15, 16, image=x) # EN PAUSE
#     onglet.bind("<Enter>", lambda event, f=onglet: hover(event, f, bg="#444757"))
#     onglet.bind("<Leave>", lambda event, f=onglet: hover(event, f, bg="#21232F"))

editor_fr = Frame(right_bloc, width=1920-370, height=1010-400, bg="#303445")
editor_fr.pack(side=TOP, anchor=N)

left_bloc = Frame(root, background="#232633", width=70, height=1280)


file_bloc = Frame(root, width=300, height=1010, background="#292C3B")


left_bloc.pack(side=LEFT, anchor=W)
file_bloc.pack(side=LEFT,anchor=W)
right_bloc.pack(side=RIGHT)




editor = lin.Editor(editor_fr)
editor.pack(fill='both', expand=True)

files = ["C:/truc/truc/truc/test.py", "C:/truc/truc/truc/index.html", "C:/truc/truc/truc/style.css", "C:/truc/truc/truc/index.js"]



folder_bloc = Frame(file_bloc, width=300, height=50, background="#353744")
folder_bloc.pack()

folder_label = folder_bloc.cwidget(Label, text="v1", bg="#353744", fg="white", font=("Monospace", 14, "bold"))
folder_label.place(x=50, y=12)

folder_bloc_img_cnv = folder_bloc.cwidget(Canvas, width=30, height=30, highlightthickness=0, bg="#353744")
folder_bloc_img_cnv.create_image(15, 15, image=folder_bloc_img)
folder_bloc_img_cnv.place(x=10, y=10)

chevrondown_cnv = folder_bloc.cwidget(Canvas, width=24, height=24, highlightthickness=0, bg="#353744", cursor="hand2")
chevrondown_cnv.create_image(12, 12, image=chevrondown)
chevrondown_cnv.place(x=260, y=15)


logo_cnv = left_bloc.cwidget(Canvas, width=70, height=70, highlightthickness=0, bg="#232633")
logo_cnv.create_image(35, 35, image=app_logo)
logo_cnv.pack()

settings_logo_cnv = left_bloc.cwidget(Canvas, width=70, height=70, highlightthickness=0, bg="#232633", cursor="hand2")
settings_logo_cnv.create_image(35, 35, image=settings_logo)
settings_logo_cnv.pack(side=BOTTOM, anchor="e", pady=10)


code_logo_cnv = left_bloc.cwidget(Canvas, width=70, height=70, highlightthickness=0, bg="#232633", cursor="hand2")
code_logo_cnv.create_image(35, 35, image=code_logo)
code_logo_cnv.pack()

git_logo_cnv = left_bloc.cwidget(Canvas, width=70, height=70, highlightthickness=0, bg="#232633", cursor="hand2")
git_logo_cnv.create_image(35, 35, image=git_logo)
git_logo_cnv.pack()

linux_logo_cnv = left_bloc.cwidget(Canvas, width=70, height=70, highlightthickness=0, bg="#232633", cursor="hand2")
linux_logo_cnv.create_image(35, 35, image=linux_logo)
linux_logo_cnv.pack()


lang_img = {}
for file in files:
    file = file.split("/")
    ext = file[-1].split(".")[-1]
    lang_img[ext] = PhotoImage(file=f"./assets/{ext}.png")
    f = file_bloc.cwidget(Canvas, width=300, height=25, bg="#292C3B", highlightthickness=0, cursor="hand2")
    f.pack()
    f.create_text(50, 12, text=file[-1], fill="white", font=("Monospace", 12), anchor=W)
    f.create_image(25, 12, image=lang_img[ext], anchor=W)

    f.bind("<Enter>", lambda event, f=f: hover(event, f, bg="#444757"))
    f.bind("<Leave>", lambda event, f=f: hover(event, f, bg="#292C3B"))





def on_resize(event):
    # print(event.width)
    # print(root.winfo_width())
    pass

lines = []


root.bind("<Configure>", on_resize)

code_logo_cnv.bind("<Enter>", lambda event: hover(event, code_logo_cnv, bg="#393E53"))
code_logo_cnv.bind("<Leave>", lambda event: hover(event, code_logo_cnv, bg="#232633"))
code_logo_cnv.bind("<Button-1>", lambda event: on_click(event, code_logo_cnv, bg="#2B2F41"))
code_logo_cnv.bind("<ButtonRelease-1>", lambda event: on_click(event, code_logo_cnv, bg="#393E53"))

git_logo_cnv.bind("<Enter>", lambda event: hover(event, git_logo_cnv, bg="#393E53"))
git_logo_cnv.bind("<Leave>", lambda event: hover(event, git_logo_cnv, bg="#232633"))
git_logo_cnv.bind("<Button-1>", lambda event: on_click(event, git_logo_cnv, bg="#2B2F41"))
git_logo_cnv.bind("<ButtonRelease-1>", lambda event: on_click(event, git_logo_cnv, bg="#393E53"))

linux_logo_cnv.bind("<Enter>", lambda event: hover(event, linux_logo_cnv, bg="#393E53"))
linux_logo_cnv.bind("<Leave>", lambda event: hover(event, linux_logo_cnv, bg="#232633"))
linux_logo_cnv.bind("<Button-1>", lambda event: on_click(event, linux_logo_cnv, bg="#2B2F41"))
linux_logo_cnv.bind("<ButtonRelease-1>", lambda event: on_click(event, linux_logo_cnv, bg="#393E53"))

settings_logo_cnv.bind("<Enter>", lambda event: hover(event, settings_logo_cnv, bg="#393E53"))
settings_logo_cnv.bind("<Leave>", lambda event: hover(event, settings_logo_cnv, bg="#232633"))
settings_logo_cnv.bind("<Button-1>", lambda event: on_click(event, settings_logo_cnv, bg="#2B2F41"))
settings_logo_cnv.bind("<ButtonRelease-1>", lambda event: on_click(event, settings_logo_cnv, bg="#393E53"))

chevrondown_cnv.bind("<Enter>", lambda event: hover(event, chevrondown_cnv, bg="#444757"))
chevrondown_cnv.bind("<Leave>", lambda event: hover(event, chevrondown_cnv, bg="#353744"))
chevrondown_cnv.bind("<Button-1>", lambda event: on_click(event, chevrondown_cnv, bg="#2B2F41"))
chevrondown_cnv.bind("<ButtonRelease-1>", lambda event: on_click(event, chevrondown_cnv, bg="#444757"))

root.mainloop()