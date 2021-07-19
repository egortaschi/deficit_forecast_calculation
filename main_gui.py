import csv
import tkinter as tk
from tkinter import ttk
import sqlite3
import deficit_calculation


class Main(tk.Frame):
    """main window class"""

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        """function for storing and initializing GUI objects"""

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img_power_station = tk.PhotoImage(file='static/power_station.png')
        self.add_img_x1 = tk.PhotoImage(file='static/x1.png')
        self.add_img_x2 = tk.PhotoImage(file='static/x2.png')
        self.add_img_calc_res = tk.PhotoImage(file='static/calcres.png')
        self.add_img_clear = tk.PhotoImage(file='static/clear.png')

        btn_calc_init_data = tk.Button(toolbar, text='Заполнить исходные данные', command=self.input_data, bg='#d7d8e0',
                                       bd=0, compound=tk.TOP, image=self.add_img_power_station)
        btn_calc_init_data.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Очистить исходные данные', command=self.delete_records, bg='#d7d8e0',
                               bd=0, compound=tk.TOP, image=self.add_img_clear)
        btn_delete.pack(side=tk.LEFT)

        btn_calc_x1 = tk.Button(toolbar, text='Расчет на сутки х+1', command=self.calc_x1, bg='#d7d8e0', bd=0,
                                compound=tk.TOP, image=self.add_img_x1)
        btn_calc_x1.pack(side=tk.LEFT)

        btn_calc_x2 = tk.Button(toolbar, text='Расчет на сутки х+2', command=self.calc_x2, bg='#d7d8e0', bd=0,
                                compound=tk.TOP, image=self.add_img_x2)
        btn_calc_x2.pack(side=tk.LEFT)

        btn_calc_res = tk.Button(toolbar, text='Результаты расчета', command=self.calc_res, bg='#d7d8e0', bd=0,
                                 compound=tk.TOP, image=self.add_img_calc_res)
        btn_calc_res.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'power_s', 'scheme', 'block_s'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('power_s', width=365, anchor=tk.CENTER)
        self.tree.column('scheme', width=150, anchor=tk.CENTER)
        self.tree.column('block_s', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('power_s', text='Генерация электростанции')
        self.tree.heading('scheme', text='Схема сети в ПАР')  # ПАР - послеаварийный режим
        self.tree.heading('block_s', text='Генерация блок-станций')

        self.tree.pack()

    def records(self, power_s, scheme, block_s):
        """function for writing user data to the database"""

        self.db.insert_data(power_s, scheme, block_s)
        self.view_records()

    def view_records(self):
        """function for displaying the contents of the database"""

        self.db.c.execute('''SELECT * FROM temp_db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        """function for deleting records"""
        self.db.c.execute('''DELETE FROM temp_db''')
        self.db.conn.commit()
        self.view_records()

    def input_data(self):
        InputData()

    def calc_x1(self):
        deficit_calculation.deficit_x1()

    def calc_x2(self):
        deficit_calculation.deficit_x2()

    def calc_res(self):
        CalcRes()


class InputData(tk.Toplevel):
    """child window class, where user should
    enter the initial data about planned network scheme,
    the amount of power generation of power plant and
    power generation of stations of industrial enterprises"""

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Parameters')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_power_s = tk.Label(self, text='Генерация электростанций')
        label_power_s.place(x=50, y=50)
        label_select = tk.Label(self, text='Схема сети в ПАР')
        label_select.place(x=50, y=80)
        label_block_s = tk.Label(self, text='Генерация блок-станций')
        label_block_s.place(x=50, y=110)

        self.entry_power_s = ttk.Entry(self)
        self.entry_power_s.place(x=210, y=50)

        self.entry_block_s = ttk.Entry(self)
        self.entry_block_s.place(x=210, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Одна ВЛ 220 кВ', u'Две ВЛ 220 кВ'])
        self.combobox.current(0)
        self.combobox.place(x=210, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Добавить')
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_power_s.get(),
                                                                  self.combobox.get(),
                                                                  self.entry_block_s.get()))

        btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()


class CalcRes(tk.Toplevel):
    """child window class, where user can view the calculation results"""

    def __init__(self):
        super().__init__()
        self.title("Calculation results")

        columns = ("#1", "#2")
        self.tree = ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Час суток")
        self.tree.heading("#2", text="Величина дефицита генерации")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        with open('deficit.csv', newline="") as f:
            for item in csv.reader(f):
                self.tree.insert("", tk.END, values=item)

        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


class DB:
    """class for working with a temporary database"""

    def __init__(self):
        self.conn = sqlite3.connect('temp_db.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS temp_db (id integer primary key, power_s real, scheme text, block_s real)''')
        self.conn.commit()

    def insert_data(self, power_s, scheme, block_s):
        self.c.execute('''INSERT INTO temp_db(power_s, scheme, block_s) VALUES (?, ?, ?)''',
                       (power_s, scheme, block_s))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Deficit forecast")
    root.geometry("750x200+300+200")
    root.resizable(False, False)
    root.iconphoto(True, tk.PhotoImage(file='static/fabric.png'))
    root.mainloop()
