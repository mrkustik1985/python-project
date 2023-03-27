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

        # add text about last action down page editor
        self.last_action = StringVar()
        self.last_action_bar = Label(self.root,textvariable=self.last_action,font=("times new roman",15,"bold"),bd=4, relief=GROOVE)
        self.last_action_bar.pack(side=BOTTOM,fill=BOTH)
        self.last_action.set("welcome to text editor")

        # create main menu
        self.main_menu = Menu(self.root, font=("times new roman",12,"bold"))
        self.root.config(menu=self.main_menu)

        # create menu to work with file
        self.file_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), tearoff=0)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save as", accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",accelerator="Ctrl+E",command=self.exit)

        # create menu to work with edit (to do function for hot keys)
        self.edit_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), tearoff=0)
        # adding cut text command
        self.edit_menu.add_command(label="Cut",accelerator="Ctrl+X")
        # adding copy text command
        self.edit_menu.add_command(label="Copy",accelerator="Ctrl+C")
        # adding paste text command
        self.edit_menu.add_command(label="Paste",accelerator="Ctrl+V")
        # adding seprator
        self.edit_menu.add_separator()
        # adding undo text Command
        self.edit_menu.add_command(label="Undo",accelerator="Ctrl+U")

        # creating help menu

        self.help_menu = Menu(self.main_menu, font=("times new roman",12,"bold"), tearoff=0)
        self.help_menu.add_command(label="About")

        self.main_menu.add_cascade(label="File",menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.main_menu.add_cascade(label="Help",menu=self.help_menu)

        self.scrollbar = Scrollbar(self.root)
        self.text = Text(self.root,
                        font=("times new roman",15,"bold"), 
                        bd = 2,
                        bg = 'black',
                        fg = 'lime', 
                        padx = 10,
                        pady = 10, 
                        wrap = WORD,
                        insertbackground = "white",
                        yscrollcommand=self.scrollbar.set
                        )
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.text.pack(fill=BOTH,expand=1)
        self.add_hot_key()

    # print file name TOP page
    def is_open_file(self):
        if self.filename!= None:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")
    
    def new_file(self, *args):
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

    def exit(self, *args):
        op = messagebox.askyesno("WARNING","Your Unsaved Data May be Lost!!")
        if op>0:
            self.root.destroy()
        else:
            return
        
    def add_hot_key(self):
        self.text.bind("<Control-e>",self.exit)
        self.text.bind("<Control-n>",self.new_file)
        self.text.bind("<Control-o>",self.open_file)

root = Tk()
TextEditor(root)
root.mainloop()