from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("1200x700")
        self.filename = None
        # add file name
        self.title = StringVar()# help to inspect changes
        self.title_bar = Label(self.root,textvariable=self.title,font=("times new roman",15,"bold"),bd=2,relief=GROOVE)
        # print titlebar to root window
        self.title_bar.pack(side=TOP,fill=BOTH)
        self.is_open_file() # now untitled

        # add text about last action down page editorh
        self.last_action = StringVar()
        self.last_action_bar = Label(self.root,textvariable=self.last_action,font=("times new roman",15,"bold"),bd=4, relief=GROOVE)
        self.last_action_bar.pack(side=BOTTOM,fill=BOTH)
        self.last_action.set("welcome to text editor")

        self.frame = Frame(self.root)
        
        Label(self.frame, text ='Find').pack(side = LEFT)
        self.edit_find = Entry(self.frame)
        self.edit_find.pack(side = LEFT, fill=BOTH, expand=1)
        self.edit_find.focus_set()
        self.find = Button(self.frame, text="Find", command=self.find)
        self.find.pack(side = LEFT)

        Label(self.frame, text ='Replace').pack(side = LEFT)
        self.edit_replace = Entry(self.frame)
        self.edit_replace.pack(side = LEFT, fill=BOTH, expand=1)
        self.edit_replace.focus_set()
        self.replace = Button(self.frame, text="Replace", command=self.find_replace)
        self.replace.pack(side = LEFT)

        self.frame.pack(side = TOP, fill = BOTH)

        # create main menu
        self.main_menu = Menu(self.root, font=("times new roman",12,"bold"), activebackground="skyblue")
        self.root.config(menu=self.main_menu)

        # create menu to work with file
        self.file_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), activebackground="skyblue", tearoff=0)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command = self.save_file)
        self.file_menu.add_command(label="Save as", accelerator="Ctrl+A", command=self.first_save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",accelerator="Ctrl+E",command=self.exit)

        # create menu to work with edit (to do function for hot keys)
        self.edit_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), activebackground="skyblue", tearoff=0)
        # adding cut text command
        self.edit_menu.add_command(label="CutWord",accelerator="Ctrl+X", command=self.delete_currently_word)
        # adding copy text command
        self.edit_menu.add_command(label="Copy",accelerator="Ctrl+C", command=self.copy)
        # adding paste text command
        self.edit_menu.add_command(label="Paste",accelerator="Ctrl+V", command=self.paste)
        self.edit_menu.add_command(label="Cancel",accelerator="Ctrl+Z", command=self.cancel_action)
        self.edit_menu.add_command(label="DltCrntStr",accelerator="Ctrl+B", command=self.delete_currently_string)
        # adding seprator
        self.edit_menu.add_separator()
        # adding undo text Command
        self.edit_menu.add_command(label="Undo",accelerator="Ctrl+U", command=self.undo)

        # creating help menu

        self.help_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), activebackground="skyblue", tearoff=0)
        self.help_menu.add_command(label="About Text Editor", command=self.info_about_text_editor)
        self.help_menu.add_command(label="About Button", command=self.info_about_button)
        self.help_menu.add_command(label="About HotKeys", command=self.info_about_hot_keys)
        self.help_menu.add_command(label="About Movement fot text", command=self.info_about_text_move)

        self.main_menu.add_cascade(label="File",menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.main_menu.add_cascade(label="Help",menu=self.help_menu)

        self.text = Text(self.root,
                        font=("times new roman",15,"bold"), 
                        bd = 2,
                        bg = 'black',
                        fg = 'lime', 
                        padx = 10,
                        pady = 10, 
                        wrap = WORD,
                        insertbackground = "white",
                        undo=True
                        )
        self.scrollbar = Scrollbar(orient="vertical", command= self.text.yview)
        self.text["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.text.pack(fill=BOTH,expand=1)
        self.add_hot_key()

    def info_about_text_editor(self, *args):
        messagebox.showinfo("About text editor", " Это текстовый редактор!\n Тут вы можете писать текст, открывать и редактировать существующие файлы, и изменять текущие.\n Функционал горячих клавиш описан в другом окне:) Тут есть поддержка выделения текста совмещенная с перемещением по тексту\n")

    def info_about_button(self, *args):
        messagebox.showinfo("About Button with editor and files", " Горячие клавиши и комбинацию к ним также можно найти в других окнах меню.\n cntrl+n - создать новый файл\n cntrl+o - открыть файл\n cntrl+s - сохранить, если не существует файла, то создать\n cntrl+a - сохранить файл как\n cntrl+e - выйти из редактора, перед выходом вас спросят сохранили ли вы файл\n")
        
    def info_about_hot_keys(self, *args):
        messagebox.showinfo("About Hot Keys", " cntrl+x - вырезать слово на котором находится курсор(также работает перед словом и сразу после него)\n cntrl+c - копировать выделенное\n cntrl+v - вставить выделенное\n cntrl+z - отменить последнее действие(редактрование слово, вставку и т.д)\n cntrl+p - удалить строку на которой находится курсор\n cntrl+u - удалить весь текст целиком")

    def info_about_text_move(self, *args):
        messagebox.showinfo("About movement fot text", " cntrl + -> курсор перемщается на 1 слово вправо\n cntrl + <- курсор перемщается на 1 слово влево\n fn + -> перемещается в конец строки\n fn + <- перемещается в начало строки\n")
    def is_open_file(self):
        if self.filename!= None:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")
    
    def new_file(self, *args):
        if self.filename != None:
            self.save_file()
        else:
            self.first_save_file()
        self.text.delete(1.0,END)
        self.filename = None
        self.is_open_file()
        self.last_action.set("new file created")
    
    def open_file(self, *args):
        try:
            filetypes = (
                ('All files', '*.*'),
                ('text files', '*.txt')
            )
            self.filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            if self.filename != None:
                self.text.delete(1.0,END)
                for l in open(self.filename):
                    self.text.insert(END,l)
                self.is_open_file()
                self.last_action.set("file opened")
        except Exception as e:
            messagebox.showerror("ERROR", e)
    
    def save_file(self, *args):
        try:
            if self.filename!= None:
                with open(self.filename, "w") as f:
                    f.write(self.text.get(1.0,END))
                self.last_action.set("file saved")
            else:
                op = messagebox.askyesno("your file is unnamed","save it?")
                if op>0:
                    self.first_save_file()
        except Exception as e:
            messagebox.showerror("ERROR", e)

    def first_save_file(self, *args):
        try:
            f = fd.asksaveasfilename(filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
            if f:
                self.filename = f
                f = open(self.filename, "w")
                f.write(self.text.get(1.0,END))
                f.close()
            self.is_open_file()
            self.last_action.set("saved successfully")
        except Exception as e:
            messagebox.showerror("ERROR", e)

    def exit(self, *args):
        op = messagebox.askyesno("WARNING","Your unsaved data may be lost!! Exit?")
        if op>0:
            self.root.destroy()
        else:
            return

    def copy(self, *args):
        self.text.event_generate("<<Copy>>")

    def paste(self, *args):
        self.text.event_generate("<<Paste>>")

    def undo(self, *args):
        try:
            self.text.delete(1.0,END)
            self.last_action.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception",e)
    
    def cancel_action(self, *args):
        self.text.edit_undo()

    def delete_currently_string(self, *args):
        id_now = self.text.index("insert")
        txt = self.text.get(1.0,END)
        self.text.delete(1.0,END)
        txt = txt.split("\n")
        cnt = 0
        id_now = id_now.split(".")
        id_now = int(id_now[0])
        id_last_not_empty = 0
        cl = 0
        for i in txt:
            cl += 1
            if i != '':
                id_last_not_empty = cl
        for l in txt:
            cnt += 1
            if cnt != id_now and cnt <= id_last_not_empty:
                self.text.insert(END,l + '\n')
    
    def delete_currently_word(self, *args):
        id_now = self.text.index("insert").split(".")
        txt = self.text.get(1.0,END)
        self.text.delete(1.0,END)
        txt = txt.split("\n")
        txt = txt[:-1]
        row = 0
        id_in_row = int(id_now[1])
        id_row = int(id_now[0])
        id_last_not_empty = 0
        cl = 0
        for line in txt:
            cl += 1
            if line != '':
                id_last_not_empty = cl
        for line in txt:
            row += 1
            if row == id_row:
                y = line[:id_in_row].rfind(' ')
                x = line[id_in_row:].find(' ')
                if x == -1:
                    x = len(line)
                self.text.insert(END, line[:y + 1] + line[id_in_row + x:] + '\n')
            elif row <= id_last_not_empty:
                self.text.insert(END, line + '\n')

    def find(self, *args):
        self.text.tag_remove('found', '1.0', END)
        is_find_pressed = self.edit_find.get()
        if is_find_pressed:
            idx = '1.0'
            while 1:
                idx = self.text.search(is_find_pressed, idx, nocase = 1, stopindex = END)
                if not idx: 
                    break
                # last index sum of current index and length of text
                lastidx = '% s+% dc' % (idx, len(is_find_pressed))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground ='red')
        self.edit_find.focus_set()

    def find_replace(self, *args):
        self.text.tag_remove('found', '1.0', END)
        is_pressed_find = self.edit_find.get()
        is_pressed_replace = self.edit_replace.get()
        if is_pressed_find and is_pressed_replace and is_pressed_find!= is_pressed_replace:
            idx = '1.0'
            while 1:
                idx = self.text.search(is_pressed_find, idx, nocase = 1,
							stopindex = END)
                if not idx:
                    break
                lastidx = '% s+% dc' % (idx, len(is_pressed_find))
                self.text.delete(idx, lastidx)
                self.text.insert(idx, is_pressed_replace)
                lastidx = '% s+% dc' % (idx, len(is_pressed_replace))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground ='green', background = 'yellow')
        self.edit_find.focus_set()
        self.edit_replace.focus_set()

    def add_hot_key(self):
        self.text.bind("<Control-e>",self.exit)
        self.text.bind("<Control-n>",self.new_file)
        self.text.bind("<Control-o>",self.open_file)
        self.text.bind("<Control-s>",self.save_file)
        self.text.bind("<Control-a>",self.first_save_file)
        self.text.bind("<Control-x>",self.delete_currently_word)
        self.text.bind("<Control-c>",self.copy)
        self.text.bind("<Control-v>",self.paste)
        self.text.bind("<Control-u>",self.undo)
        self.text.bind("<Control-z>",self.cancel_action)
        self.text.bind("<Control-b>",self.delete_currently_string)

root = Tk()
TextEditor(root)
root.mainloop()