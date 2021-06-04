import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilenames, asksaveasfile
import tkinter.messagebox as tk_message_box
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

file_info = {}
graph_labels = []


class MyFrame(tk.Tk):

    def __init__(self):
        super().__init__()

        self.w = 800
        self.h = 650
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_margin = (self.screen_width - self.w) / 2
        self.y_margin = (self.screen_height - self.h) / 2
        self.x_margin_pop = (self.screen_width - self.w) / 1.5
        self.y_margin_pop = (self.screen_height - self.h) / 1.5

        self.graph_settings = {
            "x_var": tk.StringVar(),
            "y_var": tk.StringVar(),
            "line_color": tk.StringVar(),
            "x_min_var": tk.StringVar(),
            "x_max_var": tk.StringVar(),
            "fit": tk.StringVar(),
            "y_min_var": tk.StringVar(),
            "y_max_var": tk.StringVar(),
            "plot_mode": tk.IntVar(),
            "plot_color": tk.StringVar(),
            "scale_mode": tk.StringVar(),
            "x_axis_spine_color": tk.StringVar(),
            "y_axis_spine_color": tk.StringVar(),
            "x_axis_spine_line_width": tk.StringVar(),
            "y_axis_spine_line_width": tk.StringVar(),
            "legend_pos": tk.StringVar(),
            "legend_box": tk.IntVar(),
            "figure_height": tk.IntVar(),
            "figure_width": tk.IntVar(),
            "x_scale": tk.StringVar(),
            "y_scale": tk.StringVar(),
            "fit_color": tk.StringVar(),
        }

        self.default_graph_var = {
            "x_var": 'test',
            "y_var": 'test',
            "legend_box": 0,
            "figure_height": 6,
            "figure_width": 8,
            "x_scale": "linear",
            "y_scale": "linear",
        }

        self.my_markers = {
            "none": " ",
            "point": ".",
            "pixel": ",",
            "circle": "o",
            "triangle_down": "v",
            "triangle_up": "^",
            "tri_down": "1",
            "tri_up": "2",
            "octagon": "8",
            "square": "s",
            "pentagon": "p",
            "star": "*",
            "hexagon1": "h",
            "hexagon2": "H",
            "plus": "+",
            "x": "x",
            "diamond": "D",
        }

        for var in self.default_graph_var:
            self.graph_settings[var].set(self.default_graph_var[var])

        self.title('ADO plot')
        # You can set the geometry attribute to change the root ado_plots size
        self.geometry("+%d+%d" % (self.x_margin, self.y_margin))  # You want the size of the app to be 500x500
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction

        self.frame = tk.Frame(self)
        self.menu()
        self.frame.figure1 = None
        self.frame.over_view = tk.Frame(self.frame).grid()
        self.tab_main = ttk.Notebook(self.frame.over_view)
        self.tab_data = ttk.Frame(self.tab_main)
        self.tab_graph = ttk.Frame(self.tab_main)
        self.tab_main.add(self.tab_data, text='Data')
        self.tab_main.add(self.tab_graph, text='Graph')
        self.tab_main.grid()
        self.graph = self.graph_settings

        # tab data labelframe and grid
        self.tab_data_ls = ttk.LabelFrame(self.tab_data, text='Options')
        self.tab_data_ls.grid(row=1, column=1, sticky="nsew", ipadx=5, ipady=5, padx=5, pady=5)
        self.tab_data_rs = ttk.LabelFrame(self.tab_data, text='Data View')
        self.tab_data_rs.grid(row=1, column=2, sticky="nsew", ipadx=5, ipady=5, padx=5, pady=5)

        # tab graph labelframe and grid
        self.tab_graph_ls = ttk.LabelFrame(self.tab_graph, text='Options')
        self.tab_graph_ls.grid(row=1, column=1, sticky="nsew", ipadx=5, ipady=5, padx=5, pady=5)
        self.tab_graph_rs = ttk.LabelFrame(self.tab_graph, text='Graph')
        self.tab_graph_rs.grid(row=1, column=2, sticky="nsew", ipadx=5, ipady=5, padx=5, pady=5)
        self.tab_graph_rs1 = ttk.LabelFrame(self.tab_graph, text='Advanced')
        self.tab_graph_rs1.grid(row=1, column=3, sticky="nsew", ipadx=5, ipady=5, padx=5, pady=5)

        self.my_tabs()
        self.my_file_header()
        self.window, self.ax1, self.figure1, self.bar1 = None, None, None, None

    def my_tabs(self):
        # tab data buttons
        self.frame.b1 = self.my_button(loc=self.tab_data_ls, text='Load File(s)', cm=lambda: Import(), y=1)
        self.frame.b1 = self.my_button(loc=self.tab_data_ls, text='New Dataset', cm=lambda: NewFile(), y=2)

        # tab graph buttons
        self.frame.b3 = self.my_button(loc=self.tab_graph_ls, text="Plot Graph", cm=lambda: self.plot(), y=1)
        self.frame.b4 = self.my_button(loc=self.tab_graph_ls, text="Set Type", cm=lambda: self.graph_type(), y=2)
        self.frame.b5 = self.my_button(loc=self.tab_graph_ls, text="Set X/Y", cm=lambda: self.x_y(), y=3)
        self.frame.b6a = self.my_button(loc=self.tab_graph_rs1, text="Fit Options", cm=lambda: self.my_fit(), y=1)
        self.frame.b7 = self.my_button(loc=self.tab_graph_ls, text="Set Spines", cm=lambda: self.my_spines(), y=5)
        self.frame.b8 = self.my_button(loc=self.tab_graph_ls, text="Set Legend", cm=lambda: self.my_legend(), y=6)
        self.frame.b8 = self.my_button(loc=self.tab_graph_ls, text="Set Figure", cm=lambda: self.my_figure_size(), y=7)

        # label entries for graph
        self.frame.x_ent = ttk.Label(self.tab_graph_rs, text="X-Label:")
        self.frame.x_ent.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.frame.x_ent = ttk.Entry(self.tab_graph_rs, textvariable=self.graph["x_var"])
        self.frame.x_ent.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.frame.x_ent = ttk.Label(self.tab_graph_rs, text="Y-Label:")
        self.frame.x_ent.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.frame.x_ent = ttk.Entry(self.tab_graph_rs, textvariable=self.graph["y_var"], width=10)
        self.frame.x_ent.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def my_file_header(self):
        self.frame.l1 = ttk.Label(self.tab_data_rs, text="#")
        self.frame.l1.grid(row=1, column=1, padx=5, pady=5)
        self.frame.l2 = ttk.Label(self.tab_data_rs, text="File:")
        self.frame.l2.grid(row=1, column=2, padx=5, pady=5)
        self.frame.l3 = ttk.Label(self.tab_data_rs, text="Properties:")
        self.frame.l3.grid(row=1, column=3, padx=5, pady=5)

    def del_all(self):
        file_info.clear()
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.list_my_dataset()

    def list_my_dataset(self):
        if not file_info:
            return
        elif len(file_info) == 0:
            return
        else:
            self.my_file_header()

            def place_buttons(my_file, b):
                _ = ttk.Checkbutton(self.tab_data_rs, offvalue="no", onvalue="yes",
                                    variable=file_info[my_file]["active"], state=NORMAL)
                _.grid(row=b, column=1, padx=5, pady=5)
                _ = ttk.Label(self.tab_data_rs, text=file_info[my_file]["name"])
                _.grid(row=b, column=2, padx=5, pady=5)
                _ = ttk.Button(self.tab_data_rs, text="Set Properties", command=lambda: self.my_properties(my_file))
                _.grid(row=b, column=3, padx=5, pady=5)
                _ = ttk.Button(self.tab_data_rs, text="View Data", command=lambda: self.show_data(my_file))
                _.grid(row=b, column=4, padx=5, pady=5)
                _ = ttk.Button(self.tab_data_rs, text="Delete", command=lambda: self.relist_my_dataset(my_file))
                _.grid(row=b, column=5, padx=5, pady=5)

            ab = 2
            for my_file1 in file_info:
                place_buttons(my_file1, ab)
                ab += 1
        self.after(50)

    def relist_my_dataset(self, file):
        file_info.pop(file)
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.list_my_dataset()

    def x_auto(self):
        if not file_info:
            tk_message_box.showerror("Error", "Please load a data file")
            pass
        else:
            m_list = list(file_info.keys())
            data = file_info[m_list[0]]
            x_max, x_min, y_max, y_min = data["x_max"], data["x_min"], data["y_max"], data["y_min"]

            minmax_list = {
                1: {"name": x_max, "var": self.graph_settings["x_max_var"], "factor1": 1.05, "factor2": 0.95},
                2: {"name": y_max, "var": self.graph_settings["y_max_var"], "factor1": 1.05, "factor2": 0.95},
                3: {"name": x_min, "var": self.graph_settings["x_min_var"], "factor1": 0.95, "factor2": 1.05},
                4: {"name": y_min, "var": self.graph_settings["y_min_var"], "factor1": 0.95, "factor2": 1.05},
            }

            for m_max in minmax_list:
                if minmax_list[m_max]["name"] >= 0:
                    minmax_list[m_max]["var"].set(float(minmax_list[m_max]["name"] * minmax_list[m_max]["factor1"]))
                elif minmax_list[m_max]["name"] <= 0:
                    minmax_list[m_max]["var"].set(float(minmax_list[m_max]["name"] * minmax_list[m_max]["factor2"]))
                else:
                    pass

    @staticmethod
    def my_button(loc, text, y, cm):
        _ = ttk.Button(master=loc, text=text, command=cm)
        _.grid(row=y, column=1, ipadx=2, ipady=2, padx=5, pady=5, sticky="nsew")
        return _

    def menu(self):
        # Declare Menu
        self.frame.menu_bar = Menu(self.frame)

        # File Menu
        self.frame.file_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.file_menu.add_command(label="Delete all data", command=self.del_all)
        self.frame.file_menu.add_command(label="Exit", command=self.quit)
        self.frame.menu_bar.add_cascade(label="File", menu=self.frame.file_menu)

        # Help menu
        self.frame.help_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.help_menu.add_command(label="Help", command=self.help)
        self.frame.help_menu.add_command(label="About...", command=self.my_about)
        self.frame.menu_bar.add_cascade(label="Help", menu=self.frame.help_menu)
        self.config(menu=self.frame.menu_bar)
        self.frame.grid()

    def call_ado_plot(self, title):
        # open new window
        self.frame.window = tk.Toplevel(ado_plot)
        self.frame.window.geometry("+%d+%d" % (self.x_margin_pop, self.y_margin_pop))
        self.frame.window.title(title)
        self.frame.window.resizable(0, 0)

        # set new frame in window
        self.frame.frame = tk.Frame(self.frame.window)
        return self.frame.window, self.frame.frame

    def show_data(self, file):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Stored Data")

        # add scrollbar
        scrollbar = Scrollbar(self.frame.window)
        # scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.grid(row=1, column=2, sticky=N)

        # add data contents
        self.frame.text = tk.Text(self.frame.window, yscrollcommand=scrollbar.set)
        self.frame.text.insert(INSERT, 'X Data ')
        self.frame.text.insert(INSERT, "\t")
        self.frame.text.insert(INSERT, 'Y Data')
        self.frame.text.insert(INSERT, "\t")
        self.frame.text.insert(INSERT, 'Y Error')
        self.frame.text.insert(INSERT, "\n")

        for x in range(len(file_info[file]["x_data"])):
            self.frame.text.insert(INSERT, file_info[file]["x_data"][x])
            self.frame.text.insert(INSERT, "\t")
            self.frame.text.insert(INSERT, file_info[file]["y_data"][x])
            self.frame.text.insert(INSERT, "\t")
            try:
                self.frame.text.insert(INSERT, file_info[file]["y_error"][x])
                self.frame.text.insert(INSERT, "\t")
            except IndexError:
                pass
            self.frame.text.insert(INSERT, "\n")

        self.frame.text.grid(row=1, column=1)

    def graph_type(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set graph type")

        def set_grid(gr, gc):
            _.grid(sticky="nsew", row=gr, column=gc, padx=5, pady=2.5)

        gtype = ttk.LabelFrame(self.frame.window, text="Graph Type")
        gtype.grid(row=1, column=1, sticky="nsew", padx=5, pady=2.5)

        gtype2 = ttk.LabelFrame(self.frame.window, text="Scale Type X")
        gtype2.grid(row=1, column=2, sticky="nsew", padx=5, pady=2.5)

        gtype3 = ttk.LabelFrame(self.frame.window, text="Scale Type Y")
        gtype3.grid(row=1, column=3, sticky="nsew", padx=5, pady=2.5)
        # check buttons for graph type
        graph_type = ['Line', 'Scatter', 'Bar', 'X_Log', 'Y_Log']
        scale_type = ['linear', 'log', 'symlog', 'logit', 'reverse']
        a = 1
        for my_type in graph_type:
            _ = ttk.Checkbutton(gtype, text=my_type, onvalue=a, offvalue=0,
                                variable=self.graph_settings["plot_mode"])
            set_grid(a, 1)
            a += 1

        b = 1
        for a_type in scale_type:
            _ = ttk.Checkbutton(gtype2, text=a_type, onvalue=a_type, offvalue="linear",
                                variable=self.graph_settings["x_scale"])
            set_grid(b, 1)
            _ = ttk.Checkbutton(gtype3, text=a_type, onvalue=a_type, offvalue="linear",
                                variable=self.graph_settings["y_scale"])
            set_grid(b, 1)
            b += 1

        _ = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        set_grid(a, 1)

    def my_properties(self, my_file):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Properties")

        def set_grid(gr, gc, s="nsew"):
            _.grid(sticky=s, row=gr, column=gc, padx=5, pady=2.5)

        self.frame.color = ttk.LabelFrame(self.frame.window, text="Set Color")
        self.frame.color.grid(row=1, column=1, sticky=N, padx=5, pady=2.5)
        self.frame.line = ttk.LabelFrame(self.frame.window, text="Set Line")
        self.frame.line.grid(row=1, column=2, sticky=N, padx=5, pady=2.5)
        self.frame.marker = ttk.LabelFrame(self.frame.window, text="Set Marker")
        self.frame.marker.grid(row=2, column=1, sticky=N, padx=5, pady=2.5)
        if len(file_info[my_file]["y_error"]) > 0:
            self.frame.err = ttk.LabelFrame(self.frame.window, text="Show Error Bars")
            self.frame.err.grid(row=2, column=2, sticky=N, padx=5, pady=2.5)
            _ = ttk.Checkbutton(self.frame.err, onvalue=1, offvalue=1, variable=file_info[my_file]["error_bar"])
            set_grid(1, 1)
            _ = ttk.Label(self.frame.err, text="Cap Size")
            set_grid(1, 2)
            _ = ttk.Entry(self.frame.err, textvariable=file_info[my_file]["cap_size"], width=2)
            set_grid(1, 3)
        else:
            pass

        # set colors in labelframe
        my_line_colors = ['Blue', 'Green', 'Red', 'Cyan', 'Magenta', 'Yellow', 'White']

        _ = ttk.Combobox(self.frame.color,
                         state="readonly",
                         values=my_line_colors,
                         justify="left",
                         textvariable=file_info[my_file]["color"],
                         width=10)
        set_grid(1, 1)

        # set line options for data
        my_line_options = ['solid', 'dashed', 'dashdot', 'dotted', 'none']

        _ = ttk.Combobox(self.frame.line,
                         state="readonly",
                         values=my_line_options,
                         justify="left",
                         textvariable=file_info[my_file]["line_style"],
                         width=10)
        set_grid(1, 1)

        my_marker_list = ["point",
                          "pixel", "circle",
                          "triangle_down",
                          "triangle_up",
                          "tri_down",
                          "tri_up",
                          "octagon",
                          "square",
                          "pentagon",
                          "star",
                          "hexagon1",
                          "hexagon2",
                          "plus",
                          "x",
                          "diamond"
                          ]

        _ = ttk.Combobox(self.frame.marker,
                         state="readonly",
                         values=my_marker_list,
                         justify="left",
                         textvariable=file_info[my_file]["marker"],
                         width=10)
        set_grid(1, 1)
        _ = ttk.Button(self.frame.window, text="Set", command=lambda: self.frame.window.withdraw())
        set_grid(3, 1)
        _ = ttk.Button(self.frame.window, text="Close", command=lambda: self.frame.window.destroy())
        set_grid(3, 2)

    def my_fit(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Choose fit")

        def set_grid(gr, gc, s="nsew"):
            _.grid(sticky=s, row=gr, column=gc, padx=5, pady=2.5)

        my_fit_window = ttk.LabelFrame(self.frame.window, text="Choose fit")
        my_fit_window.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5)

        # set new frame in window
        my_fits = {
            1: {"name": "Linear Regression", "var": "lin_reg"},
            2: {"name": "Four Parameter Logistic", "var": "fpl"},
            3: {"name": "Find Peaks", "var": "f_peaks"}
        }
        a = 1
        for fits in my_fits:
            _ = ttk.Checkbutton(my_fit_window, text=my_fits[fits]["name"], onvalue=my_fits[fits]["var"], offvalue="",
                                variable=self.graph_settings["fit"])
            set_grid(a, 1)
            a += 1

        _ = tk.Label(self.frame.window, text="Fit Color")
        set_grid(a, 1, s=tk.W)
        a += 1
        # fit line colors
        my_line_colors = ['Blue', 'Green', 'Red', 'Cyan', 'Magenta', 'Yellow', 'White']

        _ = ttk.Combobox(self.frame.window,
                         state="readonly",
                         values=my_line_colors,
                         justify="left",
                         textvariable=self.graph_settings["fit_color"],
                         width=10)
        set_grid(a, 1)
        a += 1
        _ = ttk.Button(self.frame.window, text="Set", command=lambda: self.frame.window.destroy())
        set_grid(a, 1)

    def my_legend(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Add data labels")

        def set_grid(gr, gc, s="nsew"):
            _.grid(sticky=s, row=gr, column=gc, padx=5, pady=5, ipadx=5, ipady=5)

        my_leg = ttk.LabelFrame(self.frame.window, text="Legend Labels")
        my_leg.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # set new frame in window
        a = 1
        for item in file_info:
            data = file_info[item]
            _ = ttk.Label(my_leg, text=data["name"])
            set_grid(a, 1)
            _ = ttk.Entry(my_leg, textvariable=data["legend"])
            set_grid(a, 2)
            a += 1
        # _ = ttk.Button(self.frame.window, text="Set", command=lambda: set_vars())
        # set_grid(a, 1)
        _ = ttk.Checkbutton(my_leg, text="Box On", onvalue=1, offvalue=0,
                            variable=self.graph_settings["legend_box"])
        set_grid(a, 1)
        _ = ttk.Button(self.frame.window, text="Set", command=lambda: self.frame.window.destroy())
        set_grid(a, 1)

    def my_figure_size(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Figure Size")

        def set_grid(gr, gc, s="nsew"):
            _.grid(sticky=s, row=gr, column=gc, padx=5, pady=5, ipadx=5, ipady=5)

        my_leg = ttk.LabelFrame(self.frame.window, text="Figure Size")
        my_leg.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        info = self.graph_settings

        _ = ttk.Label(my_leg, text="Height (inches):")
        set_grid(1, 1)
        _ = ttk.Entry(my_leg, textvariable=info["figure_height"], width=5)
        set_grid(1, 2)
        _ = ttk.Label(my_leg, text=" " + str(info["figure_height"].get() * 2.54) + " cm")
        set_grid(1, 3)
        _ = ttk.Label(my_leg, text="Width (inches):")
        set_grid(2, 1)
        _ = ttk.Entry(my_leg, textvariable=info["figure_width"], width=5)
        set_grid(2, 2)
        _ = ttk.Label(my_leg, text=" " + str(info["figure_width"].get() * 2.54) + " cm")
        set_grid(2, 3)

        _ = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        set_grid(3, 1)

    def my_spines(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Spines")

        def set_grid(gr, gc, s="nsew"):
            _.grid(sticky=s, row=gr, column=gc, padx=5, pady=2.5)

        my_spin = ttk.LabelFrame(self.frame.window, text="Set Spines")
        my_spin.grid(row=1, column=1, sticky="nsew", padx=5, pady=2.5)

        # set new frame in window
        my_spines_dict = {
            1: {"label1": "X Axis Color:", "var1": self.graph_settings["x_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": self.graph_settings["x_axis_spine_line_width"]},
            2: {"label1": "Y Axis Color:", "var1": self.graph_settings["y_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": self.graph_settings["y_axis_spine_line_width"]}
        }

        a = 1

        my_line_colors = ['Blue', 'Green', 'Red', 'Cyan', 'Magenta', 'Yellow', 'White']

        for spines in my_spines_dict:
            _ = ttk.Label(my_spin, text=my_spines_dict[spines]["label1"])
            set_grid(a, 1)
            _ = ttk.Combobox(my_spin,
                             state="readonly",
                             values=my_line_colors,
                             justify="left",
                             textvariable=my_spines_dict[spines]["var1"],
                             width=7)
            set_grid(a, 2)
            _ = ttk.Label(my_spin, text=my_spines_dict[spines]["label2"])
            set_grid(a, 3)
            _ = ttk.Entry(my_spin, textvariable=my_spines_dict[spines]["var2"], width=5)
            set_grid(a, 4)
            a += 1

        _ = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        set_grid(a, 1)

    def x_y(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set X/Y limits")

        def set_grid(gr, gc):
            _.grid(sticky="nsew", row=gr, column=gc, padx=5, pady=2.5)

        my_x_y = {
            'x_min': {'name': 'x_min', 'var': self.graph_settings["x_min_var"],
                      'row': 1, "label_col": 1, "entry_col": 2},
            'x_max': {'name': 'x_max', 'var': self.graph_settings["x_max_var"],
                      'row': 2, "label_col": 1, "entry_col": 2},
            'y_min': {'name': 'y_min', 'var': self.graph_settings["y_min_var"],
                      'row': 3, "label_col": 1, "entry_col": 2},
            'y_max': {'name': 'y_max', 'var': self.graph_settings["y_max_var"],
                      'row': 4, "label_col": 1, "entry_col": 2},
        }

        x_y_type = ttk.LabelFrame(self.frame.window, text="Set Limits")
        x_y_type.grid(row=1, column=1, padx=5, pady=2.5)

        for pos in my_x_y:
            _ = ttk.Label(x_y_type, text=my_x_y[pos]['name'])
            set_grid(my_x_y[pos]['row'], my_x_y[pos]['label_col'])
            _ = ttk.Entry(x_y_type, width=10, textvariable=my_x_y[pos]['var'])
            set_grid(my_x_y[pos]['row'], my_x_y[pos]['entry_col'])

            #  auto limits
            _ = ttk.Button(self.frame.window, text="Auto X/Y limits", command=lambda: self.x_auto())
            set_grid(5, 1)

    def plot(self):
        if not file_info.keys():
            tk.messagebox.showerror("No data loaded", "Please load a data file or select one active.")
            return
        else:
            pass

        graph_labels.clear()
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Plot")
        self.frame.grid()

        # Declare Menu
        self.frame.menu_bar = Menu(self.frame.window)

        # File Menu
        self.frame.file_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.file_menu.add_command(label="Export", command=lambda: self.save_plot())
        self.frame.menu_bar.add_cascade(label="File", menu=self.frame.file_menu)
        self.frame.window.config(menu=self.frame.menu_bar)

        # create canvas
        self.figure1 = plt.Figure(figsize=(self.graph_settings["figure_width"].get(),
                                           self.graph_settings["figure_height"].get()),
                                  dpi=96, constrained_layout=False, frameon=True)
        self.ax1 = self.figure1.add_subplot(1, 1, 1, clip_on="off")
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.frame.window)
        self.bar1.get_tk_widget().grid()

        def in_plot(my_file):
            data = file_info[my_file]
            x = data["x_data"]
            y = data["y_data"]
            color = data["color"].get()
            l_style = data["line_style"].get()
            pre_m_style = data["marker"].get()
            m_style = self.my_markers[pre_m_style]
            p_mode = self.graph_settings["plot_mode"].get()
            if data["active"].get() == 'yes':
                graph_labels.append(data["legend"].get())
                if p_mode == 1 or p_mode == 0:
                    self.ax1.plot(x, y, c=color, linestyle=l_style, marker=m_style)
                    if self.graph_settings["x_scale"].get() != 'reverse':
                        self.ax1.set_xscale(self.graph_settings["x_scale"].get())
                    if self.graph_settings["y_scale"].get() != 'reverse':
                        self.ax1.set_yscale(self.graph_settings["y_scale"].get())
                if p_mode == 2:
                    self.ax1.scatter(x, y, c=color)
                if p_mode == 3:
                    self.ax1.bar(x, y)
                if p_mode == 4:
                    self.ax1.semilogx(x, y, c=color, linestyle=l_style)
                if p_mode == 5:
                    self.ax1.semilogy(x, y, c=color, linestyle=l_style)
                if not self.graph_settings["fit"].get():
                    pass
                if self.graph_settings["fit"].get() == "lin_reg":
                    self.lin_plot(my_file)
                if self.graph_settings["fit"].get() == "fpl":
                    self.fpl_plot(my_file)
                if self.graph_settings["fit"].get() == "f_peaks":
                    self.f_peaks(my_file)
                if data["error_bar"].get() == 1:
                    y_error = data["y_error"]
                    self.ax1.errorbar(x, y, yerr=y_error, c=color, linestyle="none",
                                      capsize=data["cap_size"].get(), marker=m_style)
            else:
                pass

        for my_file1 in file_info:
            in_plot(my_file1)

        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)

        if not self.graph_settings["y_axis_spine_color"].get():
            self.graph_settings["y_axis_spine_line_width"].set(1.25)
            self.graph_settings["y_axis_spine_color"].set('black')

            self.graph_settings["x_axis_spine_line_width"].set(1.25)
            self.graph_settings["x_axis_spine_color"].set('black')

        self.ax1.spines['left'].set_linewidth(float(self.graph_settings["y_axis_spine_line_width"].get()))
        self.ax1.spines['left'].set_color(self.graph_settings["y_axis_spine_color"].get())

        self.ax1.spines['bottom'].set_linewidth(float(self.graph_settings["x_axis_spine_line_width"].get()))
        self.ax1.spines['bottom'].set_color(self.graph_settings["x_axis_spine_color"].get())

        if not self.graph_settings["x_min_var"].get():
            self.x_auto()
        else:
            pass

        x_lim_min = float(self.graph_settings["x_min_var"].get())
        y_lim_min = float(self.graph_settings["y_min_var"].get())
        x_lim_max = float(self.graph_settings["x_max_var"].get())
        y_lim_max = float(self.graph_settings["y_max_var"].get())

        if self.graph_settings["y_scale"].get() != 'reverse':
            self.ax1.set_ylim(y_lim_min, y_lim_max)
        else:
            self.ax1.set_ylim(y_lim_max, y_lim_min)

        if self.graph_settings["x_scale"].get() != 'reverse':
            self.ax1.set_xlim(x_lim_min, x_lim_max)
        else:
            self.ax1.set_xlim(x_lim_max, x_lim_min)

        self.ax1.legend(graph_labels, frameon=False, loc="best")
        self.ax1.set_xlabel(self.graph_settings["x_var"].get(), fontsize=12)
        self.ax1.set_ylabel(self.graph_settings["y_var"].get(), fontsize=12)

    def lin_plot(self, info):
        def func(a, x, b):
            return a * x + b

        data_x = file_info[info]["x_data"]
        data_y = file_info[info]["y_data"]
        p_opt, p_cov = curve_fit(func, data_x, data_y)
        self.ax1.plot(data_x, func(data_x, *p_opt), color=self.graph_settings["fit_color"].get(), linestyle='--',
                      label='fit: a=%5.3f, b=%5.3f' % tuple(p_opt))
        self.ax1.legend()

    def fpl_plot(self, info):

        def func(xe, a, b, cc, d):
            return d + ((a - d) / (1 + ((xe / cc) ** b)))

        data_y = file_info[info]["y_data"]
        data_x = file_info[info]["x_data"]

        if file_info[info].get("p_opt") is None:
            try:
                if data_y[0] < data_y[-1]:
                    p_opt, p_cov = curve_fit(func, data_x, data_y, bounds=([-4, -np.inf, min(data_x), min(data_y)],
                                                                           [min(data_y), np.inf, max(data_x),
                                                                            max(data_y)]), method="trf")
                    file_info[info]["p_opt"] = p_opt
                    file_info[info]["p_cov"] = p_cov

                elif data_y[0] > data_y[-1]:
                    p_opt, p_cov = curve_fit(func, data_x, data_y, bounds=([min(data_y), -np.inf, min(data_x), -4],
                                                                           [max(data_y),
                                                                            np.inf,
                                                                            max(data_x),
                                                                            min(data_y)]), method="trf")
                    file_info[info]["p_opt"] = p_opt
                    file_info[info]["p_cov"] = p_cov
            except ValueError:
                return

            y_new = []
            x_new = np.arange(min(data_x), max(data_x), (len(data_x) / 10))

            par = file_info[info]["p_opt"]
            for x in x_new:
                y_new.append(func(x, *par))

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels.append('fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f' % tuple(par))

            file_info[info]["x_new"] = x_new
            file_info[info]["y_new"] = y_new
        else:
            p_opt = file_info[info]["p_opt"]
            x_new = file_info[info]["x_new"]
            y_new = file_info[info]["y_new"]

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels.append('fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f' % tuple(p_opt))

    def f_peaks(self, info):
        y = file_info[info]["y_data"]
        x = file_info[info]["x_data"]
        y2 = 1 / y
        peaks, _ = find_peaks(y2, width=((max(x) - min(x)) * .01))
        self.ax1.plot(x[peaks], 1 / y2[peaks], "x", color=self.graph_settings["fit_color"].get())
        a = 0
        for n in x[peaks]:
            self.ax1.text(n, (1 / y2[peaks][a]) * 0.99, s=str(int(n)))
            a += 1

    def save_plot(self):
        try:
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt'),
                     ('Portable Image', '*.png'),
                     ('Document Image', '*.tif')]
            self.frame.save_file = asksaveasfile(filetypes=files, defaultextension=files)
            self.figure1.savefig(self.frame.save_file.name, dpi=300)
        except AttributeError:
            pass

    @staticmethod
    def do_nothing():
        pass

    @staticmethod
    def my_about():
        tk_message_box.showinfo("About",
                                "This program was made by A. Doekhie. Use is purely intended for academic purposes.")

    @staticmethod
    def help():
        tk_message_box.showinfo("Help",
                                "Load a or multiple .csv files containing purely one set of x and y data. "
                                "In the data tab you can set their visual properties like color and linestyle. "
                                "In the graph tab you can plot the data and optimise the plot format. "
                                "Advanced fitting options are present for use but limited at this stage. "
                                "Please request more functionality on the GitHub page.")


class Import:
    def __init__(self):
        self.filename = askopenfilenames()
        if len(self.filename) > 1:
            for file in self.filename:
                MyFile(file)
        elif len(self.filename) == 1:
            MyFile(self.filename[0])
        else:
            return


class MyFile:
    def __init__(self, file):
        self.filename = file
        try:
            if not self.filename:
                pass
            elif self.filename.find(".csv") == -1:
                tk_message_box.showerror("File error", "Please use x/y data in .csv file type only.")
                pass
            elif self.filename in file_info:
                pass
            else:
                # process file
                self.data = pd.read_csv(self.filename, sep=',')
                self.spectra = self.data.values
                self.x = self.spectra[:, 0]
                self.y = self.spectra[:, 1]
                try:
                    self.err = self.spectra[:, 2]
                except IndexError:
                    self.err = []
                    pass
                self.identifier = self.filename.split('/')
                self.length = len(self.identifier)
                self.name = self.identifier[self.length - 1]

                # set variables
                file_info[self.filename] = {
                    "color": tk.StringVar(),
                    "legend": tk.StringVar(),
                    "x_data": self.x,
                    "y_data": self.y,
                    "name": self.name,
                    "x_min": min(self.x),
                    "x_max": max(self.x),
                    "y_min": min(self.y),
                    "y_max": max(self.y),
                    "active": tk.StringVar(),
                    "line_style": tk.StringVar(),
                    "marker": tk.StringVar(),
                    "y_error": self.err,
                    "error_bar_color": tk.StringVar(),
                    "error_bar": tk.IntVar(),
                    "cap_size": tk.IntVar(),
                }
                default_var = {
                    "color": "black",
                    "legend": "data",
                    "active": "yes",
                    "line_style": "solid",
                    "marker": "none",
                }

                for var1 in default_var:
                    file_info[self.filename][var1].set(default_var[var1])

                ado_plot.list_my_dataset()
        except NameError:
            pass


class NewFile:

    def __init__(self):
        self.x_str = tk.StringVar()
        self.y_str = tk.StringVar()
        self.name = tk.StringVar()
        self.err = tk.StringVar()
        self.frame = tk.Toplevel(ado_plot)
        self.frame.geometry("+%d+%d" % (ado_plot.x_margin_pop, ado_plot.y_margin_pop))
        self.frame.title("New DataSet")
        self.frame.resizable(0, 0)

        # set new frame in window
        self.frame.frame = ttk.LabelFrame(self.frame, text="New Data Set")
        self.frame.frame.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Label(self.frame.frame, text="Name")
        _.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Label(self.frame.frame, text="X")
        _.grid(row=2, column=1, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Label(self.frame.frame, text="Y")
        _.grid(row=3, column=1, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Label(self.frame.frame, text="Error")
        _.grid(row=4, column=1, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Button(self.frame.frame, text="Set", command=lambda: self.do_store())
        _.grid(row=5, column=1, stick="nsew", padx=5, pady=2.5)

        _ = ttk.Entry(self.frame.frame, textvariable=self.name)
        _.grid(row=1, column=2, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Entry(self.frame.frame, textvariable=self.x_str, width=10)
        _.grid(row=2, column=2, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Entry(self.frame.frame, textvariable=self.y_str, width=10)
        _.grid(row=3, column=2, stick="nsew", padx=5, pady=2.5)
        _ = ttk.Entry(self.frame.frame, textvariable=self.err, width=10)
        _.grid(row=4, column=2, stick="nsew", padx=5, pady=2.5)

    def do_store(self):
        if not self.name:
            return
        else:
            x_split = str(self.x_str.get())
            y_split = str(self.y_str.get())
            x_f = x_split.split(",")
            x = [float(ele) for ele in x_f]
            y_f = y_split.split(",")
            y = [float(ele) for ele in y_f]
            try:
                err_split = str(self.err.get())
                err_f = err_split.split(",")
                err = [float(ele) for ele in err_f]
            except ValueError:
                err = []

            # set variables
            file_info[str(self.name.get())] = {
                "color": tk.StringVar(),
                "legend": tk.StringVar(),
                "x_data": x,
                "y_data": y,
                "name": str(self.name.get()),
                "x_min": min(x),
                "x_max": max(x),
                "y_min": min(y),
                "y_max": max(y),
                "active": tk.StringVar(),
                "line_style": tk.StringVar(),
                "marker": tk.StringVar(),
                "y_error": err,
                "error_bar_color": tk.StringVar(),
                "error_bar": tk.IntVar(),
                "cap_size": tk.IntVar(),
            }
            default_var = {
                "color": "black",
                "legend": "data",
                "active": "yes",
                "line_style": "solid",
                "marker": "none",
            }

            for var1 in default_var:
                file_info[str(self.name.get())][var1].set(default_var[var1])
            ado_plot.list_my_dataset()


if __name__ == '__main__':
    ado_plot = MyFrame() 
    ado_plot.mainloop()
