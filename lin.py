import winpty
import queue
import threading
import os
import re
import signal
from btk.btk import *

class LinuxShell(Text):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=1920-370, height=15, background="#2C3040", selectbackground= '#62697F', fg="white", selectforeground="#DBE8E7", highlightthickness = 0, border=0, font=("Consolas", 14), insertbackground="white")
        self.insert(END, os.getlogin()+":~$ ", "prompt")
        
        self.bind("<Return>", self.handle_send)
        self.bind("<Control-Key>", self.handle_control)
        self.bind("<Tab>", self.tab_complete)
        
        self.tag_configure("prompt", foreground="#65E250")
        self.tag_configure("output", foreground="white")
        
        self.executed_commands = []
        self.process = self.init_terminal()
        self.queue = queue.Queue()
        self.main_thread = threading.Thread(target=self.read_in_process, daemon=True)
        self.main_thread.start()
    
    def init_terminal(self):
        self.process = winpty.PtyProcess.spawn([r'C:\Users\minil\Documents\travail\python\projet\v1\cygwin64\bin\bash.exe', '--login', '-i'])
        self.process.read()
        return self.process
    
    def delete_terminal(self):
        self.process.close()
        self.process.terminate(True)
    
    def handle_control(self, event):
        # r = {
        #     "s": self.insert(END, "CTRL+S")
        # }
        if event.keysym == "c":
            self.process.write("\x16"), "\x16"
        return event
    
    def tab_complete(self, event):
        t = self.get("end-1c linestart", "end-1c lineend").split("$ ")
        
        
        return "break"
    
    def handle_send(self, event):
        t = self.get("end-1c linestart", "end-1c lineend").split("$ ")
        self.send_command(t[-1].strip())
    
    def clean_output(self, output):
        es = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        out = es.sub('', output)
        form = out.split('\r\n')
        return form
    
    def send_command(self, cmd:str):
        if cmd.lower() == "clear":
            self.delete("1.0", END)
            self.insert("1.0", os.getlogin()+"~$ ", "prompt")
        else:
            self.executed_commands.append(cmd)
            self.process.write(cmd+"\n")
            self.after(100, self.read_queue)
    
    def read_in_process(self):
        while True:
            try:
                output = self.process.read()
                output = self.clean_output(output)
                if output:
                    self.queue.put(output)
            except Exception as e:
                print(e)
                break
        return

    def read_queue(self):
        while not self.queue.empty():
            output = self.queue.get_nowait()
            print(output)
            for elt in output:
                if elt != self.executed_commands[-1] and len(elt)>0:
                    if elt == os.getlogin()+":~$":
                        if elt == os.getlogin()+":~$\n": # because return a la ligne alors que je veux pas pourtant le return c'est ça “gapplication help COMMAND” to get detailed help.', '\nminil:~$'] et try avec gapplication mais fait help avant
                            elt = elt[-2:]
                        elt += " "
                    self.insert(END, elt+"\n" if "$ " != elt[-2:] else elt, "prompt" if "$ " == elt[-2:] else "output")
                    self.see(END)
        self.after(100, self.read_queue)

class Editor(Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(height=100, background="#2C3040", selectbackground= '#62697F', fg="white", selectforeground="#DBE8E7", highlightthickness = 0, border=0, font=("Consolas", 14), insertbackground="white")
        self.edlines = Text(master, width=5, background="#2C3040", fg="#838CA6", border=0, font=("Consolas", 14), cursor="arrow")
        self.edlines.pack(side=LEFT, fill=Y)
        self.edlines.insert(END, "1")
        
        self.bind("<Return>", self.on_new_line)
        self.bind("<BackSpace>", self.on_line_deleted)
        self.bind("<KeyRelease>", self.on_key_release)
        
        self.lines = 1 # changé les lignes
        self.load_file("er") # adapté par rapport aux lignes, lire le fichier dans cette fonction
        
        # self.tag_configure("selected", background="#3B3F51") # Indisposé pour le moment, ne pas supprimer
        
        self.scrollbar = Scrollbar(self, orient=VERTICAL, cursor="arrow", command=self.scroll_command)
        self.scrollbar.configure(background="#292C3B", troughcolor="blue", width=15)
        
        self.config(yscrollcommand=self.scrollbar.set)
        self.edlines.config(yscrollcommand=self.scrollbar.set, state=DISABLED)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.bind("<MouseWheel>", self.on_scroll)
    
    def on_key_release(self, event):
        self.line_list = self.get('1.0', 'end').split('\n')
        lines = len(self.line_list) - 1
        l = len(self.edlines.get('1.0', 'end').split('\n'))-1
        print(l ,lines)
        while l < lines:
            self.edlines.config(state=NORMAL)
            self.edlines.insert(END, f"\n{self.lines}")
            self.lines += 1
            self.see(END)
            self.edlines.see(END)
            self.edlines.config(state=DISABLED)
            self.line_list = self.get('1.0', 'end').split('\n')
            lines = len(self.line_list) - 1
            l = len(self.edlines.get('1.0', 'end').split('\n'))-1
        while l > lines:
            self.edlines.config(state=NORMAL)
            self.edlines.delete("end-1l", "end")
            self.lines -= 1
            self.edlines.config(state=DISABLED)
            lines = len(self.line_list) - 1
            l = len(self.edlines.get('1.0', 'end').split('\n'))-1
    
    def on_scroll(self, event):
        direction = int(-1 * (event.delta / 120))
        self.yview_scroll(direction, "units")
        self.edlines.yview_scroll(direction, "units")
        return "break"
    
    def scroll_command(self, *args):
        self.yview(*args)
        self.edlines.yview(*args)
    
    def on_new_line(self, event):
        self.edlines.config(state=NORMAL)
        self.lines += 1
        self.edlines.insert(END, f"\n{self.lines}")
        self.see(END)
        self.edlines.see(END)
        self.edlines.config(state=DISABLED)
    
    def on_line_deleted(self, event):
        self.delete("insert -1 chars", "insert")
        self.line_list = self.get('1.0', 'end').split('\n')
        lines = len(self.line_list) - 1
        l = len(self.edlines.get('1.0', 'end').split('\n'))-1
        print(l ,lines)
        if l != lines:
            self.edlines.config(state=NORMAL)
            self.edlines.delete("end-1l", "end")
            self.lines -= 1
            self.edlines.config(state=DISABLED)
        return "break"
    
    def load_file(self, file):
        # CHARGER LE FICHIER
        # self.lines = 15 # METTRE LES LIGNES DEDANS
        print("test")
        for i in range(2, self.lines+1):
            self.edlines.insert(END, "\n"+str(i))
            self.insert(END, "\n")
        return 0
    
    def save_file(self, filename):
        # self.line_list = self.get('1.0', 'end').split('\n') # METTRE DANS UN FICHIER LES LIGNES
        return 0



class Onglet(Canvas):
    inst_list = []
    txt = []
    elts = {}
    def __init__(self, master, text, img, close_img, **kwargs):
        super().__init__(master, width=len(text)*10+50, height=30, background="#21232F", highlightthickness=0, cursor="hand2", **kwargs)
        Onglet.txt.append(text)
        Onglet.inst_list.append(Onglet.inst_list[-1]+len(Onglet.txt[len(Onglet.inst_list)-1])*10+50 if len(Onglet.inst_list) > 0 else 0)
        Onglet.elts[self] = Onglet.inst_list[-1]
        self.create_image(15, 15 , image=img)
        self.create_text(30, 15, text=text, fill="white", font=("Monospace", 10), anchor=W)
        self.create_image((len(text)*10+50)-15, 16, image=close_img)
        
        self.isMouseMoving = False
        
        self.bind("<ButtonRelease-1>", self.handle_click)
        self.bind("<Enter>", lambda event, f=self: hover(event, f, bg="#444757"))
        self.bind("<Leave>", lambda event, f=self: hover(event, f, bg="#21232F"))
        self.bind("<B1-Motion>", self.move_onglet)
    
    def t(self,event):
        print(event)
    
    def handle_click(self, event):
        
        alentour = self.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        if len(alentour) > 0 and alentour[0] == 3:
            self.delete_onglet()
        
        if self.isMouseMoving:
            self.isMouseMoving = False
            pos_x, pos_y = event.x, event.y
            print(Onglet.inst_list)
            i = 0
            j = 1
            print(Onglet.elts)
            print(pos_x)
            # finish = False
            # while not finish:
            #     print(Onglet.inst_list[i], Onglet.inst_list[j])
            #     if pos_x > Onglet.inst_list[i] or pos_x < Onglet.inst_list[j]:
            #         finish = True
            #         print("Onglet.inst_list[i]")
            #         Onglet.elts[i].pack_forget()
            #         self.pack(side=LEFT)
            #         Onglet.elts[i].pack(side=LEFT)
            #         # self.place(x=Onglet.inst_list[i])
            #         print() # par rapport a l'endroit touché
            #     if j == len(Onglet.inst_list)-1:
            #         print("éezr")
            #         finish = True
            #     i += 1
            #     j += 1
            # for elt in Onglet.inst_list:
            #     r += len(elt)*10+50 if elt > 0 else 0
            #     print(len(elt)*10+50)
    
    def delete_onglet(self):
        self.destroy()
    
    def move_onglet(self, event):
        self.isMouseMoving = True