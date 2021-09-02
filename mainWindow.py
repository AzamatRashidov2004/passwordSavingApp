from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import webbrowser
from mysql.connector.cursor import _ParamSubstitutor
import logic
import pyperclip
from tkinter import messagebox

class mainWindow:
    def __init__(self, obj):
        self.obj = obj
        self.obj.printSelfId()
        self.root = Tk()
        self.root.title('Password App')
        self.root.resizable(0, 0)
        self.root.geometry(self.centerWindow(700,500))
        self.root['bg'] = 'white'
        self.name = ""
        self.s = ttk.Style()
        self.s.theme_use('default')
        # styles
        self.s.configure('TLabel', background = 'white', foreground = 'black', fieldbackground = 'black')
        self.s.configure('TEntry', insertcolor = 'black')
        self.s.configure('TButton', background = 'white')
        self.s.configure("mystyle.Treeview", font = ('Calibri', 18), rowheight = 30, borderwidth = 1)
        self.s.configure('CustomEntry.TEntry', insertbackground = 'black', background = 'white', foreground = 'black', width = 20)
        self.s.configure('CustomLabel.TLabel', font = ('Calibri', 18))
        self.s.configure('CustomButton.TButton', font = ('Calibri', 18), background = 'white', foreground = 'black')
        self.s.configure('CustomFrame.TFrame', background = 'white')

        # images
        self.img_user = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/user.png')) 
        self.img_menu = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/menu.png'))
        self.img_plus1 = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/plus1.png'))
        self.img_copy = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/copy.png'))
        self.img_delete1 = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/delete1.png'))
        self.img_lupa = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/lupa.png'))
        self.img_edit1 = ImageTk.PhotoImage(Image.open('/Users/azamat/Desktop/Projects/passwordApp/images/edit1.png'))

        
        # Header
        self.header = Frame(self.root, width = 700, height = 50)
        self.header['bg'] = 'white'

        # Header UI
        self.h1 = Label(self.header, bg = "white")
        self.h2 = Label(self.header, bg = "white", image = self.img_user)
        self.h2.bind('<Button-1>', lambda e: self.openMenu())
        # Header postioning
        self.h1.grid(row = 0, column = 0, padx = (0, 200), pady = (25, 0))
        self.h2.grid(row = 0, column = 1, padx = (300, 20), pady = (25, 0))

        # Left Side Bar
        self.leftSidebar = Frame(self.root, width = 100, height = 300)
        self.leftSidebar['bg'] = 'white'

        # Right Side Bar
        self.rightsidebar = Frame(self.root, width = 100, height = 300)
        self.rightsidebar['bg'] = 'white'

        # Search Bar
        self.searchbar = Frame(self.root, width = 500, height = 80)
        self.searchbar['bg'] = 'white'
        self.searchbar.configure(borderwidth = 0)

        # Search Bar UI
        self.e1 = ttk.Entry(self.searchbar, width = 25)
        self.lupa = ttk.Button(self.searchbar, image = self.img_lupa, command = lambda: self.search())
        self.e1.configure(font = ('Calibri', 25))

        # Search Bar Positioning
        self.lupa.grid(row = 0, column = 0, padx = (20, 0), pady = (40, 5))
        self.e1.grid(row = 0, column = 1, padx = (0, 40), pady = (40, 5))
        self.searchbar.grid_propagate(False)

        # Content
        self.content = Frame(self.root, width = 500, height = 220, background = "black", borderwidth = 0)
        self.content.pack_propagate(False)

        # Content UI -> TreeView
        self.tree = ttk.Treeview(self.content, show = "tree", style = "mystyle.Treeview")
        self.tree_scroll = Scrollbar(self.content, command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.tree_scroll.set)
        self.tree['columns'] = ('ID', 'Source', 'Username')
        self.tree.column('#0', anchor = CENTER, width = 0, stretch = NO)
        self.tree.column('ID', anchor = CENTER, width = 0, stretch = NO)
        self.tree.column('Source', anchor = CENTER, width = 250, stretch = NO)
        self.tree.column('Username', anchor = CENTER, width = 250, stretch = NO)

        # Content Positioning
        self.tree_scroll.pack(side = RIGHT, fill = Y)
        self.tree.pack(fill = BOTH)

        # Treeview Entering Data
        dta = self.obj.show_data()
        for cl in dta:
            self.tree.insert(parent = '', index = 'end', values = (cl[0], cl[2], cl[1]))

        # Action
        self.action = Frame(self.root, width = 300, height = 50, borderwidth = 3)
        self.action['bg'] = 'white'

        # Action UI
        self.edit_button = ttk.Button(self.action,image = self.img_edit1, command = lambda: self.editingPasswordWindow())
        self.copy_button = ttk.Button(self.action, image = self.img_copy, command = lambda: self.copyPassword())
        self.delete_button = ttk.Button(self.action, image = self.img_delete1, command = lambda: self.deletingPassword())
        self.add_button = ttk.Button(self.action, image = self.img_plus1, command = lambda: self.addingPasswordWindow())

        # Action Positioning
        self.edit_button.grid(row = 0, column = 0, padx = (50, 35), pady = (5, 5))
        self.copy_button.grid(row = 0, column = 1, padx = (0, 35), pady = (5 , 5))
        self.add_button.grid(row = 0, column = 2, padx = (0, 35), pady = (5, 5))
        self.delete_button.grid(row = 0, column = 3, padx = (0, 60), pady = (5 ,5))
        self.action.grid_propagate(False)

        # Footer
        self.footer = Frame(self.root, width = 700, height = 100)
        self.footer['bg'] = 'white'
        self.footer.pack_propagate(False)

        # Footer UI
        self.link1 = Label(self.footer, text = "Icons from icons8.com")
        self.link1.bind("<Button-1>", lambda e: self.callback("https://icons8.com/", self.link1))
        self.link1['bg'] = 'white'
        self.link1['fg'] = 'black'

        # Footer Positioning
        self.link1.pack(pady = (30, 30))

        # Main Positioning
        self.header.grid(row = 0, column = 0, columnspan = 3)
        self.leftSidebar.grid(row = 1, rowspan = 3, column  = 0)
        self.rightsidebar.grid(row = 1, rowspan = 3, column = 2)
        self.searchbar.grid(row = 1, column = 1)
        self.content.grid(row = 2, column = 1)
        self.action.grid(row = 3, column = 1)
        self.footer.grid(row = 4, column=0, columnspan = 3)
        self.root.mainloop()
    
    def centerWindow(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return (f'{width}x{height}+{int(x)}+{int(y)}')

    def openMenu(self):
        w = Toplevel()
        w.title('Settings')
        w.geometry(self.centerWindow(400, 250))
        w.resizable(0, 0)
        mainFrame = ttk.Frame(w, style = 'CustomFrame.TFrame')
        mainFrame.pack(fill = BOTH, expand = YES)
        mainFrame.pack_propagate(0)
        btn1 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Log Out', width = 20, command = lambda: self.goToLogin())
        btn0 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Change Password', width = 20, command = lambda: self.changeAccountPasswordWindow())
        btn2 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Delete Account', width = 20, command = lambda: self.deleteAccount())
        btn1.grid(row = 0, column = 0, padx = 80, pady = (70, 20))
        btn0.grid(row = 1, column = 0, padx = 80, pady = (0, 20))    
        btn2.grid(row = 2, column = 0, padx = 80, pady = (0, 50))

    def callback(self, url, var):
        webbrowser.open_new_tab(url)
        var['fg'] = '#0b63b5' 

    def quickDelData(self):
        self.tree.delete(self.tree.selection()[0])

    def deletingPassword(self):
        try:
            item = self.tree.item(self.tree.focus())['values'][0] 
            self.obj.delete_passwd(int(item))
            self.quickDelData()
            return 1
        except:
            return None          
        
    def addingPasswordWindow(self):
        w = Toplevel()
        w.title('Add')
        w.geometry(self.centerWindow(400, 250))
        w.resizable(0,0)
        mainFrame = ttk.Frame(w, style = 'CustomFrame.TFrame')
        mainFrame.pack(fill = BOTH, expand = YES)
        mainFrame.pack_propagate(False)
        # Paddings
        paddingX = 80
        paddingY= (5, 0, 20)
        # UI
        lbl0 = ttk.Label(mainFrame, text = 'Source', style = 'CustomLabel.TLabel')
        en0 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
        lbl1 = ttk.Label(mainFrame, text = 'Username', style = 'CustomLabel.TLabel')
        en1 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
        lbl2 = ttk.Label(mainFrame, text = 'Password', style = 'CustomLabel.TLabel')
        en2 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
        btn1 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Confirm', command = lambda: self.addingPasswordToTable(en0, en1, en2))
        # Positioning
        lbl0.grid(row = 0, column = 0, padx = paddingX, pady = (paddingY[2], paddingY[1]))
        en0.grid(row = 1, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1]))
        lbl1.grid(row = 2, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1]))
        en1.grid(row = 3, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1])) 
        lbl2.grid(row = 4, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1])) 
        en2.grid(row = 5, column = 0, padx = paddingX, pady = paddingY[0])
        btn1.grid(row = 6, column = 0, padx = paddingX, pady = (paddingY[1], paddingY[2]))


    def addingPasswordToTable(self, s0, s1, s2):
        source = s0.get()
        username = s1.get()
        passwd = s2.get()
        id = self.obj.insert_passwd(source, username, passwd)
        b = self.tree.insert(parent = '', index = 'end', values = (id, source, username))
        item =  self.tree.item(b)
        self.tree.selection_set(b)

    def editingPasswordWindow(self):
        try:
            w = Toplevel()
            w.title('Edit')
            w.geometry(self.centerWindow(400, 250))
            w.resizable(0,0)

            data = self.getRowData()
            source = data[2]
            name = data[1]
            passwd = data[0]
            mainFrame = ttk.Frame(w, style = 'CustomFrame.TFrame')
            mainFrame.pack(fill = BOTH, expand = YES)
            mainFrame.pack_propagate(False)
            # Paddings
            paddingX = 80
            paddingY= (5, 0, 20)
            # UI
            lbl0 = ttk.Label(mainFrame, text = 'Source', style = 'CustomLabel.TLabel')
            en0 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
            lbl1 = ttk.Label(mainFrame, text = 'Username', style = 'CustomLabel.TLabel')
            en1 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
            lbl2 = ttk.Label(mainFrame, text = 'Password', style = 'CustomLabel.TLabel')
            en2 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
            btn1 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Confirm', command = lambda: self.editPassword(en0, en1, en2))
            en0.insert(0, source)
            en1.insert(0, name)
            en2.insert(0, passwd)
            # Positioning
            lbl0.grid(row = 0, column = 0, padx = paddingX, pady = (paddingY[2], paddingY[1]))
            en0.grid(row = 1, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1]))
            lbl1.grid(row = 2, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1]))
            en1.grid(row = 3, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1])) 
            lbl2.grid(row = 4, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1])) 
            en2.grid(row = 5, column = 0, padx = paddingX, pady = paddingY[0])
            btn1.grid(row = 6, column = 0, padx = paddingX, pady = (paddingY[1], paddingY[2]))
        except:
            pass

    def updateRecord(self, source, username, passwd):
        temp = self.tree.focus()
        self.tree.item(temp, values = (self.tree.item(self.tree.focus())['values'][0], source, username))
    
    def getRowData(self):
        try:
            tmp = self.tree.item(self.tree.focus())
            item = tmp['values'][0]
            data = self.obj.showRowData(int(item))
            return data 
        except:
            return None
            
    def editPassword(self, s0, s1, s2):
        try:
            source = s0.get()
            username = s1.get()
            passwd = s2.get()
            item = self.tree.item(self.tree.focus())['values'][0] 
            self.obj.update_passwd(int(item), source, username, passwd)
            self.updateRecord(source, username, passwd)
        except:
            pass    
    def copyPassword(self):
        try:
            item = self.tree.item(self.tree.focus())['values'][0]
            tmp = self.obj.showRowData(int(item))
            password = tmp[0]
            pyperclip.copy(password)
        except:
            pass
    
    def search(self):
        try:
            query = self.e1.get()
            selections = []
            for child in self.tree.get_children():
                tmp = self.tree.item(child)['values'][1]
                if query.lower() in tmp.lower():
                    selections.append(child)
            self.tree.selection_set(selections)
        except:
            pass
    def goToLogin(self):
        self.root.destroy()
        loginWindow()
    
    def deleteAccount(self):
        messagebox.showinfo('showinfo', 'Your account has been deleted')
        self.obj.unregister()
        self.root.destroy()
        loginWindow()
    
    def changeAccountPassword(self, en0):
        try:
            password = en0.get()
            name = self.obj.returnLoginUsername()
            self.obj.passwordUpdate(name, password)
            messagebox.showinfo('showinfo', 'Password has been changed')
            self.root.destroy()
            loginWindow()
        except:
            pass
    
    def changeAccountPasswordWindow(self):
        try:
            w = Toplevel()
            w.geometry('Password Update')
            w.geometry(self.centerWindow(400, 250))
            w.resizable(0,0)
            mainFrame = ttk.Frame(w, style = 'CustomFrame.TFrame')
            mainFrame.pack(fill = BOTH, expand = YES)
            mainFrame.pack_propagate(False)
            # Paddings
            paddingX = 80
            paddingY= (5, 0, 20)
            # UI
            lbl0 = ttk.Label(mainFrame, text = 'New Password', style = 'CustomLabel.TLabel')
            en0 = ttk.Entry(mainFrame, style = 'CustomEntry.TEntry', font = ('Calibri', 18))
            btn1 = ttk.Button(mainFrame, style = 'CustomButton.TButton', text = 'Confirm', command = lambda: self.changeAccountPassword(en0))
            # Positioning
            lbl0.grid(row = 0, column = 0, padx = paddingX, pady = (paddingY[2], paddingY[1]))
            en0.grid(row = 1, column = 0, padx = paddingX, pady = (paddingY[0], paddingY[1]))
            btn1.grid(row = 2, column = 0, padx = paddingX, pady = (paddingY[1], paddingY[2]))
        except:
            pass
            
    
class loginWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        self.root.resizable(0, 0)
        self.root.geometry(self.centerWindow(400, 250))
        self.s = ttk.Style()
        self.s.theme_use('default')
        self.s.configure('TLabel', background = 'white', foreground = 'black', fielbackground = 'black', font = ('Calibri', 18))
        self.s.configure('TEntry', background = 'white', foreground = 'black', insertcolor = 'black', width = 20)
        self.s.configure('TButton', backround = 'white', foreground = 'black', font = ('Calibri', 14))
        self.s.configure('TFrame', background = 'white')
        self.s.configure('Reg.TLabel', background = 'white', foreground = '#3495eb', font = ('Calibri', 12), fieldbackground = 'black')
        self.mainFrame = ttk.Frame(self.root)
        self.mainFrame.pack(fill = BOTH, expand = YES)
        self.mainFrame.pack_propagate(False)
        self.l1 = ttk.Label(self.mainFrame, text = 'Username')
        self.l2 = ttk.Label(self.mainFrame, text = 'Password')
        self.l3 = ttk.Label(self.mainFrame, text = 'Register', style = 'Reg.TLabel')
        self.e1 = ttk.Entry(self.mainFrame)
        self.e2 = ttk.Entry(self.mainFrame)
        self.b1 = ttk.Button(self.mainFrame, text = 'Login', command = lambda: self.pressed())
        self.paddingX = 100
        self.paddingY = (5, 0, 20, 35)
        self.l1.grid(row = 0, column = 0, padx = self.paddingX, pady = (self.paddingY[3], self.paddingY[0]))
        self.l2.grid(row = 2, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.l3.grid(row = 5, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[2]))
        self.e1.grid(row = 1, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.e2.grid(row = 3, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.b1.grid(row = 4, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.l3.bind('<Button-1>', lambda e: self.openRegister())
        self.root.mainloop()

    def centerWindow(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return (f'{width}x{height}+{int(x)}+{int(y)}')

    def pressed(self):
        try:
            username = self.e1.get()
            password = self.e2.get()
            a = logic.user()
            res = a.login(username, password)
            if res is None:
                return 5/0
            else:
                self.root.destroy()
                b = mainWindow(a)
                return 1

        except:
            messagebox.showinfo('showinfo', 'Incorrect username or password')
            return None

    def openRegister(self):
        try:
            self.root.destroy()
            registerWindow()
        except:
            pass


class registerWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('Register')
        self.root.resizable(0, 0)
        self.root.geometry(self.centerWindow(400, 250))
        self.s = ttk.Style()
        self.s.theme_use('default')
        self.s.configure('TLabel', background = 'white', foreground = 'black', fielbackground = 'black', font = ('Calibri', 18))
        self.s.configure('TEntry', background = 'white', foreground = 'black', insertcolor = 'black', width = 20)
        self.s.configure('TButton', backround = 'white', foreground = 'black', font = ('Calibri', 14))
        self.s.configure('TFrame', background = 'white')
        self.s.configure('Reg.TLabel', background = 'white', foreground = '#3495eb', font = ('Calibri', 12), fieldbackground = 'black')
        self.mainFrame = ttk.Frame(self.root)
        self.mainFrame.pack(fill = BOTH, expand = YES)
        self.mainFrame.pack_propagate(False)
        self.l1 = ttk.Label(self.mainFrame, text = 'Username')
        self.l2 = ttk.Label(self.mainFrame, text = 'Password')
        self.l3 = ttk.Label(self.mainFrame, text = 'Login', style = 'Reg.TLabel')
        self.e1 = ttk.Entry(self.mainFrame)
        self.e2 = ttk.Entry(self.mainFrame)
        self.b1 = ttk.Button(self.mainFrame, text = 'Register', command = lambda: self.pressed1())
        self.paddingX = 100
        self.paddingY = (5, 0, 20, 35)
        self.l1.grid(row = 0, column = 0, padx = self.paddingX, pady = (self.paddingY[3], self.paddingY[0]))
        self.l2.grid(row = 2, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.l3.grid(row = 5, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[2]))
        self.e1.grid(row = 1, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.e2.grid(row = 3, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.b1.grid(row = 4, column = 0, padx = self.paddingX, pady = (self.paddingY[0], self.paddingY[0]))
        self.l3.bind('<Button-1>', lambda e: self.openLogin())
        self.root.mainloop()

    def centerWindow(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return (f'{width}x{height}+{int(x)}+{int(y)}')
    
    def pressed1(self):
            username = self.e1.get()
            password = self.e2.get()
            brain = logic.user()
            res = brain.register(username, password)
            if res == None:
                messagebox.showinfo('showinfo', 'Username is not available')
                return None
            self.root.destroy()
            loginWindow()
            return 1

    def openLogin(self):
        try:
            self.root.destroy()
            loginWindow()
        except:
            pass
        

loginWindow()
        