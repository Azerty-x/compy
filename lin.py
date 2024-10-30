from btk.btk import *


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
        for i in range(2, self.lines+1):
            self.edlines.insert(END, "\n"+str(i))
            self.insert(END, "\n")
        return 0
    
    def save_file(self, filename):
        # line_list = self.get('1.0', 'end').split('\n') # METTRE DANS UN FICHIER LES LIGNES
        return 0



class Onglet(Canvas):
    inst_list = []
    txt = []
    elts = {}
    def __init__(self, master, text, img, close_img, **kwargs):
        super().__init__(master, width=len(text)*10+50, height=30, background="#21232F", highlightthickness=0, cursor="hand2", **kwargs)
        Onglet.txt.append(text)
        self.detail = Onglet.inst_list[-1]+len(Onglet.txt[len(Onglet.inst_list)-1])*10+50 if len(Onglet.inst_list) > 0 else 0
        Onglet.inst_list.append(self.detail)
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
        
        # if self.isMouseMoving: # NE PAS SUPPRIMER
        #     self.isMouseMoving = False
        #     pos_x, pos_y = (event.x*-1), event.y
        #     value_sest = [i for i in Onglet.inst_list if i != self.detail]
        #     r = min(value_sest, key=lambda x:[abs(x-(self.detail-pos_x))])
        #     if r > (self.detail-pos_x):
        #         r = value_sest[value_sest.index(r)-1]
        #     print(Onglet.inst_list[value_sest.index(r)])
        #     for elt in Onglet.elts.items():
        #         print(elt[1] > r, elt[1], r)
        #         if elt[1] > r or r == 0:
        #             elt[0].pack_forget()
        #     for elt in Onglet.elts.items():
        #         print(elt[1] > r, elt[1], r)
        #         if elt[1] == self.detail:
        #             elt[0].pack(side=LEFT)
        #             print(r, elt)
        #     for elt in Onglet.elts.items():
        #         if elt[1] != self.detail:
        #             elt[0].pack(side=LEFT)
            


    
    def delete_onglet(self):
        self.destroy()
    
    def move_onglet(self, event):
        self.isMouseMoving = True
        # self.place(x=event.x, y=event.y)