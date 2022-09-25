import re
import tkinter as tk
from tkinter import BitmapImage, PhotoImage, ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo, askyesno, showerror
import os
import pandas as pd
import numpy as np
import vobject
import qrcode
from PIL import Image


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Address Book')
        self.geometry('1000x600')
        self.resizable(False, False)
        self.config(
            background='#3d3846'
        )
        p1 = tk.PhotoImage(file=f'{os.path.dirname(__file__)}/ph.png')
        self.data = pd.DataFrame(columns=['Imie', 'Nazwisko', 'Tel', 'Email', 'Zawód'], index=None)
        self.iconphoto(False, p1)
        self.__setUP()
    
    def __setUP(self):
        self.frameIn = tk.Frame(self, name='frameIn', highlightbackground="black", highlightthickness=2)
        self.frameIn.place(x=10, y=10, width=200, height=580)
        self.frameIn.config(bg='#5e5c64')
        
        self.frameLine = tk.Frame(self, name='frameLine', highlightbackground="black", highlightthickness=2)
        self.frameLine.place(x=220, y=10, width=765, height=150)
        self.frameLine.config(bg='#5e5c64')

        
        self.frameShow = tk.Frame(self, name='frameShow', borderwidth = 0, highlightthickness = 0)
        self.frameShow.place(x=220, y=170, width=765, height=419)
        #self.frameShow.config(bg='#5e5c64')
        

        label = tk.Label(self.frameIn, text='Load/Save Data')
        label.grid(row=0, columnspan=2)
        label.config(bg='#5e5c64', font=('Arial-Bold', 15))
        del label

        style = ttk.Style()
        style.configure('TButton',
            width=9,
            background='#a4b0be',
            activebackground='#f1f2f6', 
            relief="flat",
            font=("Arial", 11,"bold")
        )
        self.LoadButton = ttk.Button(self.frameIn, name='loadBut', text='Load', command=self.load_file)
        self.LoadButton.grid(column=0, row=1, padx=4, pady=4)
        
        self.SaveButton = ttk.Button(self.frameIn, name='saveBut', text='Save', command=self.save_file)

        self.SaveButton.grid(column=1, row=1, padx=4, pady=4)

        label = tk.Label(self.frameIn, text='-'*27)
        label.config(bg='#5e5c64', font=('Arial', 15, 'bold'))
        label.grid(row=2, columnspan=2)

        label = tk.Label(self.frameIn, text='Add/Remove Person')
        label.grid(row=3, columnspan=2)
        label.config(bg='#5e5c64', font=('Arial-Bold', 14))
        del label
        
        self.AddButton = ttk.Button(self.frameIn, name='addBut', text='Add', command=self.add_person)

        self.AddButton.grid(column=0, row=4, padx=4, pady=4)
        
        self.RemoveButton = ttk.Button(self.frameIn, name='removeBut', text='Remove', state='disabled', command=self.remove_row)
        self.RemoveButton.grid(column=1, row=4, padx=4, pady=4)

        label = tk.Label(self.frameIn, text='-'*27)
        label.config(bg='#5e5c64', font=('Arial', 15, 'bold'))
        label.grid(columnspan=2, row=5)

        label = tk.Label(self.frameIn, text='Edit Row')
        label.grid(row=6, columnspan=2)
        label.config(bg='#5e5c64', font=('Arial-Bold', 14))
        
        self.EditRow = ttk.Button(self.frameIn, name='editRow', text='Edit', state='disabled', command=self.edit)
        self.EditRow.grid(columnspan=2, row=7, padx=4, pady=4)
        self.Accept = ttk.Button(self.frameIn, name='accepRow', text='Accept', command=self.acceptrow)


        label = tk.Label(self.frameIn, text='-'*27)
        label.config(bg='#5e5c64', font=('Arial', 15, 'bold'))
        label.grid(columnspan=2, row=8)

        label = tk.Label(self.frameIn, text='Clear Data')
        label.grid(row=9, columnspan=2)
        label.config(bg='#5e5c64', font=('Arial-Bold', 14))
        
        self.ClearDataButton = ttk.Button(self.frameIn, name='clearDataButton', text='Clear Data', state='disabled', command=self.cleardata)
        self.ClearDataButton.grid(columnspan=2, row=10, padx=4, pady=4)


        self.tree_view()
           
        self.label('Imie:', 10, 35)
        self.InputName = tk.Entry(self.frameLine, name='nameInput')
        self.InputName.place(x=10, y=65, height=40, width=120)
        self.InputName.configure(background='#EDE9E8',foreground='#000', borderwidth=1, highlightbackground='#3d3846', highlightthickness='2')

        self.label('Nazwisko:', 145, 35)
        self.InputLast = tk.Entry(self.frameLine, name='lastInput')
        self.InputLast.place(x=145, y=65, height=40, width=140)
        self.InputLast.configure(background='#EDE9E8',foreground='#000', borderwidth=1, highlightbackground='#3d3846', highlightthickness='2')

        self.label('Telefon:', 295, 35)
        self.InputPhone = tk.Entry(self.frameLine, name='phoneInput')
        self.InputPhone.place(x=295, y=65, height=40, width=100)
        self.InputPhone.configure(background='#EDE9E8',foreground='#000', borderwidth=1, highlightbackground='#3d3846', highlightthickness='2')
        
        self.label('Email:', 405, 35)
        self.InputCity = tk.Entry(self.frameLine, name='cityInput')
        self.InputCity.place(x=405, y=65, height=40, width=180)
        self.InputCity.configure(background='#EDE9E8',foreground='#000', borderwidth=1, highlightbackground='#3d3846', highlightthickness='2')

        self.label('Zawód:', 595, 35)
        self.InputJob = tk.Entry(self.frameLine, name='jobInput')
        self.InputJob.place(x=595, y=65, height=40, width=150)
        self.InputJob.configure(background='#EDE9E8',foreground='#000', borderwidth=1, highlightbackground='#3d3846', highlightthickness='2')

        self.QrCan = tk.Canvas(self.frameIn, width=194, height=194)
        self.QrCan.place(x=0, y=380)

        frame = tk.Frame(self.frameLine, highlightbackground="black", highlightthickness=2)
        frame.place(x=670, y=110, width=87, height=33)
        self.ClearBut = ttk.Button(frame, name='clearButton', text='Clear', command=lambda: [x.delete(0, 'end') for x in self.frameLine.children.values() if x.winfo_class() == 'Entry'])
        self.ClearBut.place(x=0, y=0)
        self.SwapButtons = [self.RemoveButton, self.ClearDataButton, self.EditRow]
    
    def cleardata(self):
        self.data = self.data.drop(list(self.data.index), axis=0)
        self.update_tree()
        self.swap(self.SwapButtons)
        self.EditRow['text'] = 'Edit'
        self.EditRow['command'] = self.edit

    def acceptrow(self):
        person = [x.get() for x in self.frameLine.children.values() if x.winfo_class() == 'Entry']
        if not self.check(person):
            return
        self.data.at[int(self.selected[1:], 16)-1, list(self.data.columns)] = person
        self.data = self.data.reset_index(drop=True)
        self.update_tree()
        self.EditRow['text'] = 'Edit'
        self.EditRow['command'] = self.edit

    def edit(self):
        if not self.tree.selection():
            return
        [x.delete(0, 'end') for x in self.frameLine.children.values() if x.winfo_class() == 'Entry']
        self.selected = self.tree.focus()
        self.values = self.tree.item(self.selected, 'values')
        value = 0
        for x in self.frameLine.children.values():
            if x.winfo_class() == 'Entry':
                x.insert('end', self.values[value])
                value+=1
        self.EditRow['text'] = 'Accept'
        self.EditRow['command'] = self.acceptrow

    def label(self, text, x, y):
        label = tk.Label(self.frameLine, text=text)
        label.place(x=x, y=y)
        label.config(bg='#5e5c64', font=('Arial-Bold', 14))

    def tree_view(self):    
        col = ['Imie', 'Nazwisko', 'Tel', 'Email', 'Zawód']
        self.tree = ttk.Treeview(self.frameShow, columns=col, height=20)
        col.insert(0, '#0')
        for column in col:
            col_width = 141
            if column == '#0':
                col_width = 62
            elif column == 'Tel':
                col_width = 100
            elif column == 'Email':
                col_width = 180
            self.tree.column(column, anchor='w', width=col_width, minwidth=col_width)
            if column == '#0':
                self.tree.heading(column, text='ID', anchor='center')
            else:
                self.tree.heading(column, text=column, anchor='center')
        self.tree.bind('<ButtonRelease-1>', self.create_qrcode)
        
        style = ttk.Style()
        style.configure('Treeview',
            background='#EDE9E8',
            fieldbackground='#3d3846'
        )
        style.configure('Treeview.Heading',
            background='#a4b0be',
            relief='flat'
        )
        self.tree.column('#0', anchor='w')
        self.tree.place(x = -1, y = -1)
                 
        

    def create_qrcode(self, e):
        if not self.tree.selection():
            return
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        dic = f'Imie: {values[0]},\nNazwisko: {values[1]},\nTel: +48 {values[2]},\nEmail: {values[3]},\nZawód: {values[4]}'
        self.qr = qrcode.make(dic)
        self.qr.save('Qr.png')
        self.im= Image.open('Qr.png').resize([200, 200])
        self.im.save('Qr.png')
        self.img = PhotoImage(file='Qr.png')
        self.QrCan.create_image(100, 100, image=self.img)
        

    def update_tree(self):
        self.tree_view()
        for value, row in enumerate(self.data.values):
            self.tree.insert('', 'end', text= value+1,values=list(row))

       

    def add_person(self):
        person = [x.get().capitalize() for x in self.frameLine.children.values() if x.winfo_class() == 'Entry']
        if not self.check(person):
            return
        top_row = pd.DataFrame(np.array(person).reshape((1,5)), columns=list(self.data.columns),index=None)
        self.data = pd.concat([top_row, self.data]).reset_index(drop=True)
        self.update_tree()
        self.swap(self.SwapButtons)
        for x in self.frameLine.children.values():
            if x.winfo_class() == 'Entry':
                x.delete(0, 'end')

    def check(sefl, person):
        errors = []
        regex = re.compile(r'[A-Za-z]*[.]*[ ]*[A-Za-z]*')
        if len(person[0]) < 2 or not re.fullmatch(regex, person[0]):
            errors.append(['Błąd importu', 'Podaj poprawne imię'])
        if len(person[1]) < 2 or not re.fullmatch(regex, person[1]):
            errors.append(['Błąd importu', 'Podaj poprawne nazwisko'])
        
        try:
            int(person[2])
        except ValueError or TypeError:
            errors.append(['Błąd importu', 'Podaj poprawny numer telefonu'])
        regex_em = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex_em, person[3]):
            errors.append(['Błąd importu', 'Podaj poprawny adres email'])
        person[3] = person[3].lower()
        if len(person[-1]) < 2 or not re.fullmatch(regex, person[-1]):
            errors.append(['Błąd importu', 'Podaj poprawne zawód'])
        if not len(errors) == 0:
            for error in errors:
                showerror(error[0], error[1])
            return False
        return True

    def remove_row(self):
        index = self.tree.selection()
        if not index:
            return
        self.data = self.data.drop(index=int(index[0][1:], 16)-1)
        self.data = self.data.reset_index(drop=True)
        self.tree.delete(index)
        self.update_tree()
        if not self.tree.selection():
            self.swap(self.SwapButtons)


    def swap(self, buttons):
        for button in buttons:
            if len(self.tree.get_children()) == 0:
                button['state'] = 'disabled'
            else:
                button['state'] = 'normal'

    def load_file(self):
        path = Application.select_file('load')
        if not path:
            return
        self.data = pd.read_csv(path, sep=',', encoding='utf-8')
        del self.tree
        self.update_tree()
        self.swap(self.SwapButtons)

    def save_file(self):
        if not self.tree.get_children():
            if not askyesno('Błąd', 'Baza danych jest Pusta\nCzy mimo to chcesz zapisać plik?'):
                return
        path = Application.select_file('save')
        if not path:
            return
        self.data.to_csv(path, sep=';', encoding='utf-8')
        

    @staticmethod
    def select_file(type):
        filetypes = (
            ('CSV', '*.csv'),
            ('All files', '*.*')
        )
        if type == 'load':
            file =filedialog.askopenfilename(
                title='Open a file',
                initialdir=f'{os.path.dirname(__file__)}',
                filetypes=filetypes)
        elif type == 'save':
            file = filedialog.asksaveasfile(
                title='Open a file',
                initialdir=f'{os.path.dirname(__file__)}',
                filetypes=filetypes)
        if file == '':
                return False
        return file

if __name__ == '__main__':
    app = Application()
    app.mainloop()
    #5e5c64