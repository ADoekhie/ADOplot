from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import numpy as np
import pandas as pd
from _data import *


class Import:
    def __init__(self):
        self.filename = askopenfilenames()
        if len(self.filename) > 1:
            for file in self.filename:
                MyFile(file).run_all()
        elif len(self.filename) == 1:
            MyFile(self.filename[0]).run_all()
        else:
            return


class MyFile:
    def __init__(self, file):
        self.filename = file
        if self.filename is not None:
            self.extension = self.filename.split('.')
            self.ext = self.extension[1]
        self.data, self.spectra, self.x, self.y = None, None, None, None
        self.x_err, self.y_err = [], []
        self.data_val = {}
        self.multi = False
        self.identifier, self.length, self.name = None, None, None

    def run_all(self):
        if self.process_file():
            self.file_type()
            self.file_id()
            self.set_var(self)

    def run_cfg(self):
        self.file_id()
        self.set_var(self)

    def process_file(self):
        # try to process if possible and check for file type
        message = "Please use x/y data in .csv or .dat file type only."
        try:
            if not self.filename:
                return
            if self.ext == "csv" or self.ext == "dat":
                if self.filename in MySettings.file_info:
                    return
                else:
                    return True
            else:
                tk_message_box.showerror("File error", message)
                return False
        except NameError:
            return

    def file_type(self):
        # process CSV file
        if self.filename.count(".csv") > 0:
            f = open(self.filename, "r")
            f_first = f.readline()
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            header = None
            for letter in alphabet:
                if f_first.count(letter) != 0:
                    header = 0
                    # print("found letter!") # for debugging file headers

            if f_first.count(",") > 1:
                self.data = pd.read_csv(self.filename, sep=',', header=header)
                self.spectra = self.data.values
                self.x = self.spectra[:, 0]
                self.y = []
                col = 1
                self.multi = True
                print("br1")
                for c in range(1, len(self.data.columns), 1):
                    self.data_val[c] = self.spectra[:, col]
                    col += 1

            if f_first.count(",") == 1:
                self.data = pd.read_csv(self.filename, sep=',', header=header)
                self.spectra = self.data.values
                self.x = self.spectra[:, 0]
                self.y = self.spectra[:, 1]
                try:
                    self.y_err = self.spectra[:, 2]
                except IndexError:
                    self.y_err = []
                    return
                try:
                    self.x_err = self.spectra[:, 3]
                except IndexError:
                    self.x_err = []
                    return

        # process space-spaced .dat file
        if self.filename.find(".dat") > 0:
            self.x = []
            self.y = []
            self.y_err = []
            self.x_err = []
            f = open(self.filename, "r")
            test = {}
            # loop through opened .dat file into test dictionary
            a = 1
            for ly in f:
                test[a] = {}
                ar = ly.split()
                b = 1
                for n in ar:
                    test[a][b] = n
                    b += 1
                a += 1
                #   pass values test dict to self.x and self.y array
                for var in test:
                    try:
                        self.x.append(float(test[var][1]))
                        self.y.append(float(test[var][2]))
                    except ValueError:
                        return
                    try:
                        self.y_err.append(float(test[var][3]))
                    except KeyError:
                        return
                    try:
                        self.x_err.append(float(test[var][4]))
                    except KeyError:
                        return
            f.close()  # close openend file
            self.file_id()

    def file_id(self):
        # set file parameters
        self.identifier = self.filename.split('/')
        self.length = len(self.identifier)
        self.name = self.identifier[self.length - 1]

    @staticmethod
    def set_var(self):
        if self.multi:
            # print("br3")
            data_range = len(self.data_val)
            # print(self.data_val)
        else:
            data_range = 1

        if type(self.x) is list:
            temp = np.asarray(self.x)
            self.x = temp

        for a in range(1, data_range+1, 1):
            print(a)
            #  convert list to ndarray
            try:
                if data_range > 1:
                    # print("br4")
                    hold = self.data_val[a]
                    # print(hold)
                    temp = np.asarray(hold)
                    self.y = temp
                else:
                    temp = np.asarray(self.y)
                    self.y = temp
                    # print(self.y)
            except ValueError:
                return
            # set variables in app data array MySettings.file_info
            MySettings.file_info[self.filename + str(a)] = {
                "color": tk.StringVar(),
                "legend": tk.StringVar(),
                "x_data": self.x,
                "y_data": self.y,
                "name": self.name + "-col " + str(a),
                "active": tk.StringVar(),
                "line_style": tk.StringVar(),
                "marker": tk.StringVar(),
                "y_error": self.y_err,
                "x_error": self.x_err,
                "error_bar_color": tk.StringVar(),
                "y_error_bar": tk.IntVar(),
                "x_error_bar": tk.IntVar(),
                "cap_size": tk.IntVar(),
                "error_color": tk.StringVar(),
                "use_data_for_fit_color": tk.BooleanVar(),
            }
            try:
                d = MySettings.file_info[self.filename + str(a)]
                d["x_min"] = min(self.x)
                d["x_max"] = max(self.x)
                d["y_min"] = min(self.y)
                d["y_max"] = max(self.y)
            except TypeError or ValueError:
                d = MySettings.file_info[self.filename + str(a)]
                d["x_min"] = 0
                d["x_max"] = 1
                d["y_min"] = 0
                d["y_max"] = 1

            default_var = {
                "error_color": "Black",
                "color": "black",
                "legend": "data",
                "active": "yes",
                "line_style": "solid",
                "marker": "none",
                "use_data_for_fit_color": False,
            }

            for var1 in default_var:
                MySettings.file_info[self.filename + str(a)][var1].set(default_var[var1])

            Data.x_auto()


class NewFile:

    def __init__(self):
        self.x = []
        self.y = []
        self.multi = False
        self.y_err = []
        self.x_err = []
        self.x_str = tk.StringVar()
        self.y_str = tk.StringVar()
        self.name = tk.StringVar()
        self.var = tk.StringVar()
        self.y_err_str = tk.StringVar()
        self.x_err_str = tk.StringVar()
        self.frame = tk.Toplevel()
        self.filename = ""
        # self.frame.geometry("+%d+%d" % (ado_plot.x_margin_pop, ado_plot.y_margin_pop))
        self.frame.title("New DataSet")
        self.frame.resizable(0, 0)

        # set new frame in window
        self.frame.frame = ttk.LabelFrame(self.frame, text="New Data Set")
        self.frame.frame.grid(row=1, column=1, stick="ew", padx=5, pady=2.5)

        label_entries = {
            0: {"type": "lab", "t": "Enter comma separated values", "r": 0},
            1: {"type": "lab", "t": "Name (string)", "r": 1},
            2: {"type": "lab", "t": "X (e.g: 1,2,3)", "r": 2},
            3: {"type": "lab", "t": "Y (e.g: 1,2,3)", "r": 3},
            4: {"type": "lab", "t": "Y Error (optional)", "r": 4},
            41: {"type": "lab", "t": "X Error (optional)", "r": 5},
            5: {"type": "ent", "v": self.name, "r": 1},
            6: {"type": "ent", "v": self.x_str, "r": 2},
            7: {"type": "ent", "v": self.y_str, "r": 3},
            8: {"type": "ent", "v": self.y_err_str, "r": 4},
            81: {"type": "ent", "v": self.x_err_str, "r": 5},
        }

        for ele in label_entries:
            e = label_entries[ele]
            if e["type"] == "lab":
                ttk.Label(self.frame.frame, text=e["t"]).grid(
                    row=e["r"], column=1, stick="ew", padx=5, pady=2.5)
            if e["type"] == "ent":
                ttk.Entry(self.frame.frame, textvariable=e["v"]).grid(
                    row=e["r"], column=2, stick="ew", padx=5, pady=2.5)

        ttk.Button(self.frame.frame, text="Set", command=self.do_store).grid(
            row=6, column=1, stick="ew", padx=5, pady=2.5)

        self.frame.wait_window(self.frame)

    def do_store(self):
        # this function grabs the strings and converts them into lists for iteration and plotting
        if not self.name:
            return
        else:
            # convert x/y string submitted data into x/y data lists
            d_list = [self.x, self.y]
            d_str_list = [self.x_str, self.y_str]
            f = []
            for d_str, d_data in zip(d_list, d_str_list):
                if str(d_data.get()) != '':
                    if '.' in str(d_data.get()):
                        f = [float(ele) for ele in str(d_data.get()).split(",")]
                    if '.' not in str(d_data.get()):
                        f = [float(ele) for ele in str(d_data.get()).split(",")]
                    for vl in f:
                        d_str.append(vl)
                else:
                    return
            # then check if x and y are same length
            if len(self.x) != len(self.y):
                tk_message_box.showerror("Data entry error", "X/Y values do not have the same amount of numbers,"
                                                             " please check your entry and try again.")
            # retrieve inputted data for x/y errors
            erc_str = [self.x_err_str, self.y_err_str]
            erc_val = [self.x_err, self.y_err]
            for check, val, comp in zip(erc_str, erc_val, d_list):
                if str(check.get()) != '':
                    if '.' in str(check.get()):
                        f = [float(ele) for ele in str(check.get()).split(",")]
                    if '.' not in str(check.get()):
                        f = [int(ele) for ele in str(check.get()).split(",")]
                    for vl in f:
                        val.append(vl)
                    # check if there are any variables and if so compare to the length of x/y
                    # to make sure they're the same
                    if len(val) > 1:
                        # print(val)
                        if len(val) != len(comp):
                            tk_message_box.showerror("Data entry error",
                                                     "Entered  values " + str(val) + " do not have the same "
                                                                                     "amount of numbers, "
                                                                                     "please "
                                                                                     "check your "
                                                                                     "entry and "
                                                                                     "try "
                                                                                     "again.")
                else:
                    pass
            # after successfully entering the new data set, close the window and return to the overview
            # by processing this in the super class
            self.frame.destroy()
            self.filename = self.name.get()
            self.name = self.name.get()
            MyFile.set_var(self)
