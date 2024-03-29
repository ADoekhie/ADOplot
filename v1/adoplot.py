import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilenames, askopenfilename, asksaveasfile
import tkinter.messagebox as tk_message_box
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import json

file_info = {}  # this is the main dictionary where all imported data will be stored and JSON exported capability
graph_labels = {"labels": []}  # separate dictionary with labels list for easy JSON export


class MyFrame(tk.Tk):  # The window frame this program runs in
    def __init__(self):
        super().__init__()  # initialise all tkinter functions

        # window frame settings
        self.file_info = file_info
        self.original_dpi = 143.858407079646
        self.dpi = self.winfo_fpixels('1i')
        self.scale = self.dpi / self.original_dpi
        self.w = 800 * self.scale
        self.h = 650 * self.scale
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_margin = (self.screen_width - self.w) / 2
        self.y_margin = (self.screen_height - self.h) / 2
        self.x_margin_pop = (self.screen_width - self.w) / 1.5
        self.y_margin_pop = (self.screen_height - self.h) / 1.5
        self.my_line_colors = ['Black', 'Blue', 'Green', 'Red', 'Cyan', 'Magenta', 'Yellow', 'White']
        self.columnconfigure((0, 20), weight=1)
        self.par = {}
        self.graph_settings = {  # graphs settings for matplot lib
            "x_var": tk.StringVar(),
            "y_var": tk.StringVar(),
            "line_color": tk.StringVar(),
            "x_min_var": tk.StringVar(),
            "x_max_var": tk.StringVar(),
            "fit": tk.StringVar(),
            "y_min_var": tk.StringVar(),
            "y_max_var": tk.StringVar(),
            "plot_mode": tk.StringVar(),
            "plot_color": tk.StringVar(),
            "scale_mode": tk.StringVar(),
            "x_axis_spine_color": tk.StringVar(),
            "y_axis_spine_color": tk.StringVar(),
            "top_spine_color": tk.StringVar(),
            "right_spine_color": tk.StringVar(),
            "x_axis_spine_line_width": tk.StringVar(),
            "y_axis_spine_line_width": tk.StringVar(),
            "top_spine_line_width": tk.StringVar(),
            "right_spine_line_width": tk.StringVar(),
            "legend_pos": tk.StringVar(),
            "legend_box": tk.BooleanVar(),
            "show_legend": tk.BooleanVar(),
            "figure_height": tk.IntVar(),
            "figure_width": tk.IntVar(),
            "x_scale": tk.StringVar(),
            "y_scale": tk.StringVar(),
            "fit_color": tk.StringVar(),
            "bar": tk.IntVar(),
            "plotted": [],
            "x_label_font": tk.IntVar(),
            "y_label_font": tk.IntVar(),
            "x_tick_size": tk.IntVar(),
            "y_tick_size": tk.IntVar(),
            "interactive": tk.IntVar(),
            "dpi": tk.IntVar(),
            "custom_eq": tk.StringVar(),
            "custom_par": tk.StringVar(),
            "use_data_for_fit_color": tk.BooleanVar(),
        }

        self.default_graph_var = {  # default vars that can be initialised upon program start
            "x_var": 'test',
            "y_var": 'test',
            "legend_box": False,
            "figure_height": 6,
            "figure_width": 8,
            "x_scale": "linear",
            "y_scale": "linear",
            "x_axis_spine_color": 'Black',
            "y_axis_spine_color": 'Black',
            "x_axis_spine_line_width": 1.25,
            "y_axis_spine_line_width": 1.25,
            "plot_mode": "Line",
            "top_spine_color": "White",
            "right_spine_color": "White",
            "top_spine_line_width": 1.25,
            "right_spine_line_width": 1.25,
            "x_label_font": 10,
            "y_label_font": 10,
            "x_tick_size": 10,
            "y_tick_size": 10,
            "interactive": 0,
            "legend_pos": 'best',
            "show_legend": True,
            "fit_color": 'Black',
            "dpi": 96,
            "use_data_for_fit_color": False,
        }

        self.my_markers = {  # marker options list
            "none": "",
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

        self.grid_opt = {"sticky": "ew",  # standard arguements for the GRID widget manager
                         }

        self.grid_opt_prop = {"sticky": "ew",  # standard arguements for the GRID widget manager
                              "padx": 10,
                              "pady": 5,
                              }

        self.grid_opt_prop_cont = {"sticky": "ew",  # standard arguements for the GRID widget manager
                                   "padx": 10,
                                   "pady": 10,
                                   }

        self.grid_pad = {"padx": 10, "pady": 5, "ipady": 5}

        self.grid_pad_file = {"padx": 10, "pady": 5, "sticky": "w"}

        self.grid_frame_opt = {
            "sticky": "nsew",
            "ipady": 5,
            "pady": 15,
        }

        self.grid_frame_opt_lab = {
            "sticky": "w",
            "ipady": 0,
            "pady": 5,
            "padx": 10,
        }

        self.annos = {}  # empty dictionary for storing annotations

        self.anno_opt = {  # annotation options for placing text and arrows
            "title": tk.StringVar(),
            "x1": tk.StringVar(),
            "y1": tk.StringVar(),
            "x2": tk.StringVar(),
            "y2": tk.StringVar(),
        }

        self.anno_labels = ["Annotation label",  # labels for defining the variables to enter
                            "label (start) point x-axis",
                            "label (start) point y-axis",
                            "end point x-axis (use for arrow annotation)",
                            "end point y-axis (use for arrow annotation)"]
        self.my_fit_grid_opt_but = {"sticky": "nsew", "padx": 5, "pady": 2.5}
        self.my_fit_grid_opt_lab = {"sticky": "w", "padx": 5, "pady": 0}

        for var in self.default_graph_var:  # loop over the default vars and place them in the active used dictionary
            self.graph_settings[var].set(self.default_graph_var[var])

        self.title('ADO plot')
        # You can set the geometry attribute to change the root ado_plots size
        self.geometry("+%d+%d" % (self.x_margin, self.y_margin))  # You want the size of the app to be 500x500
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction

        self.frame = tk.Frame(self)  # start main frame
        self.menu()  # call the top window menu
        self.frame.figure1 = None
        self.frame.over_view = tk.Frame(self.frame).grid()
        self.tab_main = ttk.Notebook(self.frame.over_view)  # initialise the Notebook
        self.tab_data = ttk.Frame(self.tab_main)
        self.tab_graph = ttk.Frame(self.tab_main)
        self.tab_script = ttk.Frame(self.tab_main)
        self.tab_main.add(self.tab_data, text='Data')
        self.tab_main.add(self.tab_graph, text='Graph')
        # self.tab_main.add(self.tab_script, text='Script')
        self.tab_main.grid()
        self.graph = self.graph_settings

        # tab data labelframe and grid
        self.spacer(self.tab_data, 1, 1)
        self.tab_data_ls = tk.LabelFrame(self.tab_data, text="Options")
        self.tab_data_ls.grid(row=1, column=2, **self.grid_frame_opt)
        self.spacer(self.tab_data, 1, 3)
        self.tab_data_rs = tk.LabelFrame(self.tab_data, text="Data View")
        self.tab_data_rs.grid(row=1, column=4, **self.grid_frame_opt)
        self.spacer(self.tab_data, 1, 5)

        # tab graph labelframe and grid
        self.spacer(self.tab_graph, 1, 1)
        self.tab_graph_ls = tk.LabelFrame(self.tab_graph, text="Options")
        self.tab_graph_ls.grid(row=1, column=2, **self.grid_frame_opt)
        self.spacer(self.tab_graph, 1, 3)
        self.tab_graph_rs = tk.LabelFrame(self.tab_graph, text="Graph Labels")
        self.tab_graph_rs.grid(row=1, column=4, **self.grid_frame_opt)
        self.spacer(self.tab_graph, 1, 5)
        self.tab_graph_rs1 = tk.LabelFrame(self.tab_graph, text="Advanced")
        self.tab_graph_rs1.grid(row=1, column=6, **self.grid_frame_opt)
        self.spacer(self.tab_graph, 1, 7)
        self.my_tabs()
        self.my_file_header()
        self.window, self.ax1, self.figure1, self.bar1 = None, None, None, None

    def my_tabs(self):
        # tab data buttons
        self.frame.b1 = self.my_button(loc=self.tab_data_ls, text='Load File(s)', cm=lambda: Import(), y=1)
        self.frame.b1b = self.my_button(loc=self.tab_data_ls, text='New Dataset', cm=lambda: NewFile(), y=2)

        # tab graph buttons
        self.frame.b3 = self.my_button(loc=self.tab_graph_ls, text="Plot Graph", cm=lambda: self.plot(), y=1)
        self.frame.b4 = self.my_button(loc=self.tab_graph_ls, text="Set Type", cm=lambda: self.graph_type(), y=2)
        self.frame.b5 = self.my_button(loc=self.tab_graph_ls, text="Set X/Y", cm=lambda: self.x_y(), y=3)

        self.frame.b6a = self.my_button(loc=self.tab_graph_rs1, text="Fit Options", cm=lambda: self.my_fit(), y=1)
        self.frame.b6b = self.my_button(loc=self.tab_graph_rs1, text="Font Style", cm=lambda: self.my_font(), y=2)
        self.frame.b7 = self.my_button(loc=self.tab_graph_rs1, text="Set Spines", cm=lambda: self.my_spines(), y=3)
        self.frame.b8 = self.my_button(loc=self.tab_graph_ls, text="Set Legend", cm=lambda: self.my_legend(), y=4)
        self.frame.b8a = self.my_button(loc=self.tab_graph_ls, text="Annotate", cm=lambda: self.my_annotate(), y=5)
        self.frame.b8 = self.my_button(loc=self.tab_graph_rs1, text="Set Figure", cm=lambda: self.my_figure_size(), y=4)
        self.frame.b8b = self.my_button(loc=self.tab_graph_rs1, text="Edit Figure", cm=lambda: self.edit_picture(), y=5)

        # label entries for graph
        ttk.Label(self.tab_graph_rs, text="X-Label:").grid(row=1, column=1, **self.grid_frame_opt_lab)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["x_var"], width=35).grid(
            row=1, column=2, columnspan=3, **self.grid_frame_opt_lab)
        ttk.Label(self.tab_graph_rs, text="Y-Label:").grid(row=2, column=1, **self.grid_frame_opt_lab)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["y_var"], width=35).grid(
            row=2, column=2, columnspan=3, **self.grid_frame_opt_lab)

    def my_file_header(self):  # Header row for loaded files
        loc = self.tab_data_rs
        opt = self.grid_pad_file
        tk.Canvas(loc, bg="#ccc", height=2, width=450).grid(row=0, column=1, columnspan=5, pady=5, padx=10)
        ttk.Label(loc, text="#").grid(row=1, column=1, **opt)
        ttk.Label(loc, text="File:").grid(row=1, column=2, **opt)
        ttk.Label(loc, text="Properties:").grid(row=1, column=3, **opt)

    @staticmethod
    def spacer(lc, r, c):
        _ = ttk.Label(lc, text=" ", width=1)
        _.grid(row=r, column=c)
        return _

    def del_all(self):  # delete all data function
        file_info.clear()
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
        self.list_my_dataset()

    def get_script(self):
        store = self.script.get("1.0", "end-1c")
        return store

    def list_my_dataset(self):  # list all data files loaded into the main dictionary
        if not file_info:
            pass
        elif len(file_info) == 0:
            pass
        else:
            self.my_file_header()

            def place_buttons(my_file, b):  # create the buttons that can set, edit and view data
                plc = self.tab_data_rs
                d = my_file
                cms = [self.my_properties, self.show_data, self.relist_my_dataset]
                grid_opt = {"padx": 10, "pady": 5}
                grid_opt_b = {"sticky": "w", "padx": 10, "pady": 5}
                ttk.Checkbutton(plc, offvalue="no", onvalue="yes", variable=file_info[d]["active"],
                                state=NORMAL).grid(row=b, column=1, sticky="w", **grid_opt)
                ttk.Label(plc, text=file_info[my_file]["name"]).grid(row=b, column=2, sticky="w", **grid_opt)
                ttk.Button(plc, text="Set", command=lambda: cms[0](d)).grid(row=b, column=3, **grid_opt_b)
                ttk.Button(plc, text="View Data", command=lambda: cms[1](d)).grid(row=b, column=4, **grid_opt_b)
                ttk.Button(plc, text="Delete", command=lambda: cms[2](d)).grid(row=b, column=5, **grid_opt_b)

            ab = 2
            for my_file1 in file_info:
                place_buttons(my_file1, ab)
                ab += 1
        self.after(50)

    def relist_my_dataset(self, file):  # remove a file from the main dictionary and loop again to refersh file list
        file_info.pop(file)
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
        self.list_my_dataset()

    def x_auto(self):  # This function autmatically sets the x/y limits based on the fractions chosen
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

    def my_button(self, loc, text, y, cm, x=1):
        _ = ttk.Button(master=loc, text=text, command=cm)
        _.grid(row=y, column=x, **self.grid_pad, sticky="nsew")
        return _

    def menu(self):  # Top window menu call function
        # Declare Menu
        self.frame.menu_bar = Menu(self.frame)

        # File Menu
        self.frame.file_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.file_menu.add_command(label="Delete all data", command=self.del_all)
        self.frame.file_menu.add_command(label="Exit", command=self.quit)
        self.frame.menu_bar.add_cascade(label="File", menu=self.frame.file_menu)

        # Data Menu
        self.frame.data_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.data_menu.add_command(label="Save Project", command=self.save_config)
        self.frame.data_menu.add_command(label="Load Project", command=self.load_config)
        self.frame.menu_bar.add_cascade(label="Save/Load", menu=self.frame.data_menu)

        # Help menu
        self.frame.help_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.help_menu.add_command(label="Help", command=self.help)
        self.frame.help_menu.add_command(label="About...", command=self.my_about)
        self.frame.menu_bar.add_cascade(label="Help", menu=self.frame.help_menu)
        self.config(menu=self.frame.menu_bar)
        self.frame.grid()

    def call_ado_plot(self, title):  # Standard toplevel window function for other functions to use
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
        text_col = ['X Data ', "\t", 'Y Data', "\t", 'Y Error', "\t", 'X Error', "\n"]

        for head in text_col:
            self.frame.text.insert(INSERT, head)

        for x in range(len(file_info[file]["x_data"])):
            self.frame.text.insert(INSERT, file_info[file]["x_data"][x])
            self.frame.text.insert(INSERT, "\t")
            self.frame.text.insert(INSERT, file_info[file]["y_data"][x])
            self.frame.text.insert(INSERT, "\t")
            try:
                self.frame.text.insert(INSERT, file_info[file]["y_error"][x])
                self.frame.text.insert(INSERT, "\t")
            except IndexError:
                self.frame.text.insert(INSERT, "\t")
                pass
            try:
                self.frame.text.insert(INSERT, file_info[file]["x_error"][x])
                self.frame.text.insert(INSERT, "\t")
            except IndexError:
                self.frame.text.insert(INSERT, "\t")
                pass
            self.frame.text.insert(INSERT, "\n")

        self.frame.text.grid(row=1, column=1)

    def graph_type(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set graph type")
        graph_type_grid_opt = {"sticky": "ew", "row": 1, "padx": 5, "pady": 5}
        graph_type_grid_opt_but = {"sticky": "nsew", "padx": 5, "pady": 5}
        graph_type_list = ["Graph Type", "Scale Type X", "Scale Type Y"]

        # check buttons for graph type
        graph_type = ['Line', 'Scatter', 'Bar', 'X_log', 'Y_log']
        scale_type = ['linear', 'log', 'symlog', 'logit', 'reverse']
        type_list = [graph_type, scale_type, scale_type]
        graph_type_var = [self.graph_settings["plot_mode"],
                          self.graph_settings["x_scale"],
                          self.graph_settings["y_scale"]]

        for gtype, col, tl, gtv in zip(graph_type_list, range(1, 4, 1), type_list, graph_type_var):
            gt = tk.LabelFrame(self.frame.window, text=gtype)
            gt.grid(column=col, **graph_type_grid_opt)
            ttk.Combobox(gt, state="readonly", values=tl,
                         justify="left", textvariable=gtv,
                         width=10).grid(column=col, **graph_type_grid_opt)

        ttk.Button(self.frame.window, text="OK",
                   command=lambda: self.frame.window.destroy()).grid(row=2, column=1, **graph_type_grid_opt_but)
        ttk.Button(self.frame.window, text="Cancel",
                   command=lambda: self.frame.window.destroy()).grid(row=2, column=2, **graph_type_grid_opt_but)

    def my_font(self):
        # open new window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Font")
        main = self.frame.window
        opt_f = {"sticky": "nsew", "padx": 5, "pady": 5, "ipady": 5}
        opt_c = {"sticky": "ew", "padx": 5, "pady": 5}

        font_options = tk.LabelFrame(self.frame.window, text="Font Options")
        font_options.grid(row=1, column=1, **opt_f)

        my_font_dict = {
            "X Label Font Size": "x_label_font",
            "Y Label Font Size": "y_label_font",
            "X Tick Font Size": "x_tick_size",
            "Y Tick Font Size": "y_tick_size",
        }

        a = 1
        for fo in my_font_dict:
            ttk.Label(font_options, text=fo).grid(row=a, column=1, **opt_c)
            ttk.Entry(font_options, textvariable=self.graph_settings[my_font_dict[fo]], width=3).grid(
                row=a, column=2, **opt_c)
            a += 1

        # close window
        ttk.Button(main, text="OK", command=lambda: main.destroy()).grid(row=a, column=1, **opt_f)

    def my_properties(self, my_file):
        # open window and set variables
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Properties")
        kw = self.grid_opt_prop
        kw_c = self.grid_opt_prop_cont
        lab_opt = {}
        fym = file_info[my_file]
        main = self.frame.window

        self.frame.color = tk.LabelFrame(self.frame.window, text="Line Color", **lab_opt)
        self.frame.line = tk.LabelFrame(self.frame.window, text="Line Style", **lab_opt)
        self.frame.marker = tk.LabelFrame(self.frame.window, text="Markers", **lab_opt)

        for f in [self.frame.color, self.frame.line, self.frame.marker]:
            f.grid(column=1, **kw)

        if self.graph_settings["fit"].get():
            self.frame.dcolor = tk.LabelFrame(self.frame.window, text="fit color", **lab_opt)
            self.frame.dcolor.grid(row=1, column=2, **kw)
            ttk.Checkbutton(self.frame.dcolor, onvalue=True, offvalue=False,
                            variable=self.graph_settings["use_data_for_fit_color"]).grid(column=2, **kw_c)

        for err, err_bar, r in zip(["y_error", "x_error"], ["y_error_bar", "x_error_bar"], [0, 1]):
            if len(fym[err]) > 0:
                self.frame.err = tk.LabelFrame(self.frame.window, text=err + "bars", **lab_opt)
                ser = self.frame.err
                ser.grid(row=r, column=2, **kw)
                ttk.Checkbutton(ser, onvalue=1, offvalue=0, variable=fym[err_bar]).grid(row=1, column=1, **kw_c)
                ttk.Label(ser, text="Cap Size").grid(row=1, column=2, **kw)
                ttk.Entry(ser, textvariable=fym["cap_size"], width=2).grid(row=1, column=3, **kw_c)
            else:
                pass
        if len(file_info[my_file]["x_error"]) > 0 or len(file_info[my_file]["y_error"]) > 0:
            self.frame.err = tk.LabelFrame(self.frame.window, text="Error Bar Color", **lab_opt)
            self.frame.err.grid(row=2, column=2, **kw)
            # set colors in labelframe
            ttk.Combobox(self.frame.err, state="readonly", values=self.my_line_colors, justify="left",
                         textvariable=fym["error_color"], width=10).grid(row=2, column=1, columnspan=3, **kw_c)
        else:
            pass

        ttk.Combobox(self.frame.color, state="readonly", values=self.my_line_colors, justify="left",
                     textvariable=fym["color"], width=10).grid(row=1, column=1, **kw_c)  # set colors in labelframe

        my_line_options = ['solid', 'dashed', 'dashdot', 'dotted', 'none']  # set line options for data

        ttk.Combobox(self.frame.line, state="readonly", values=my_line_options, justify="left",
                     textvariable=fym["line_style"], width=10).grid(row=1, column=1, **kw_c)

        my_marker_list = ["point", "pixel", "circle", "triangle_down", "triangle_up", "tri_down", "tri_up",
                          "octagon", "square", "pentagon", "star", "hexagon1", "hexagon2", "plus",
                          "x", "diamond", "none", ]

        ttk.Combobox(self.frame.marker, state="readonly", values=my_marker_list, justify="left",
                     textvariable=fym["marker"], width=10).grid(row=1, column=1, **kw_c)
        ttk.Button(main, text="Set", command=lambda: main.withdraw()).grid(row=5, column=1, **kw)
        ttk.Button(main, text="Close", command=lambda: main.destroy()).grid(row=5, column=2, **kw)

    def my_fit(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Choose fit")
        my_fit_grid_opt_but = {"sticky": "nsew", "padx": 5, "pady": 2.5}
        my_fit_grid_opt_lab = {"sticky": "w", "padx": 5, "pady": 0}
        main = self.frame.window

        my_fit_window = tk.LabelFrame(self.frame.window, text="Choose fit")
        my_fit_window.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5, ipady=5)

        # set new frame in window
        my_fits = {
            1: {"name": "Linear Regression", "var": "lin_reg"},
            2: {"name": "Four Parameter Logistic", "var": "fpl"},
            3: {"name": "Find Peaks", "var": "f_peaks"},
            4: {"name": "UV Thermal", "var": "uv_gibbs"},
            5: {"name": "CD two state", "var": "cd_two_state"},
            6: {"name": "CD two state lin corr", "var": "cd_two_state_lin"},
            7: {"name": "Custom Equation", "var": "custom_eq"}
        }

        # run through all available fit options
        for fits in my_fits:
            ttk.Checkbutton(my_fit_window, text=my_fits[fits]["name"], onvalue=my_fits[fits]["var"], offvalue="",
                            variable=self.graph_settings["fit"]).grid(column=1, **my_fit_grid_opt_but)

        # button for custom equations that will popup a new window
        custom_fit = ttk.Button(self.frame.window, text="Set Custom Equation", command=lambda: self.my_custom_eq())
        custom_fit.grid(row=2, column=1, **my_fit_grid_opt_but)

        my_other_fit_window = tk.LabelFrame(self.frame.window, text="Additional Options")
        my_other_fit_window.grid(row=3, column=1, stick="nsew", padx=5, pady=2.5, ipady=5)
        mo_fw = my_other_fit_window

        ttk.Label(mo_fw, text="Fit Color").grid(column=1, **my_fit_grid_opt_lab)
        # fit line colors
        ttk.Combobox(mo_fw, state="readonly", values=self.my_line_colors, justify="left",
                     textvariable=self.graph_settings["fit_color"]).grid(
            column=1, columnspan=2, **my_fit_grid_opt_but)
        ttk.Button(main, text="Set", command=lambda: main.destroy()).grid(column=1, **my_fit_grid_opt_but)

    def my_custom_eq(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Input custom equation")
        data = self.graph_settings
        main = self.frame.window

        lf1 = ttk.LabelFrame(self.frame.window, text="Input equation")
        lf1.grid(row=1, **self.grid_frame_opt_lab)
        ttk.Entry(lf1, textvariable=data["custom_eq"], width=20).grid(row=1, **self.my_fit_grid_opt_but)
        ttk.Label(lf1, text="Define Parameters").grid(row=2, **self.my_fit_grid_opt_lab)
        ttk.Entry(lf1, textvariable=data["custom_par"], width=20).grid(row=3, **self.my_fit_grid_opt_but)
        ttk.Button(lf1, text="Set", command=lambda: main.destroy()).grid(row=4, **self.my_fit_grid_opt_but)

    def my_legend(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Add data labels")

        grid_opt_but = {"sticky": "nsew", "padx": 10, "pady": 5}  # button grid options
        grid_opt_lab = {"sticky": "w", "padx": 10, "pady": 2.5}  # label grid options

        legend_loc = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
                      'center right', 'lower center', 'upper center', 'center']

        my_leg = tk.LabelFrame(self.frame.window, text="Legend Labels")
        my_leg.grid(row=1, column=1, sticky="nsew", **self.grid_pad)
        if not graph_labels["labels"]:
            ttk.Label(my_leg, text="No data loaded").grid(**grid_opt_lab)

        # set new frame in window
        a = 1
        for item in file_info:
            data = file_info[item]
            ttk.Label(my_leg, text=data["name"]).grid(row=a, column=1)
            ttk.Entry(my_leg, textvariable=data["legend"]).grid(row=a, column=2)
            a += 1

        # Another label frame to hold legend options
        my_leg_opt = tk.LabelFrame(self.frame.window, text="Legend Options")
        my_leg_opt.grid(row=2, column=1, sticky="nsew", **self.grid_pad)
        # Box on or off button
        ttk.Checkbutton(my_leg_opt, text="Box On/Off", onvalue=1, offvalue=0,
                        variable=self.graph_settings["legend_box"]).grid(row=1, column=1, **grid_opt_but)
        ttk.Checkbutton(my_leg_opt, text="Show Legend", onvalue=True, offvalue=False,
                        variable=self.graph_settings["show_legend"]).grid(row=2, column=1, **grid_opt_but)
        # Combobox legend location
        ttk.Label(my_leg_opt, text="Set Legend Location:").grid(row=3, column=1, **grid_opt_lab)
        ttk.Combobox(my_leg_opt, textvariable=self.graph_settings["legend_pos"], values=legend_loc,
                     state="readonly", justify="left").grid(row=4, column=1, columnspan=2, **grid_opt_but)
        # Close window button 'OK'
        ttk.Button(self.frame.window, text="Set",
                   command=lambda: self.frame.window.destroy()).grid(row=3, column=1, **grid_opt_but)

    def my_figure_size(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Figure Size")
        main = self.frame.window
        info = self.graph_settings
        my_leg = tk.LabelFrame(self.frame.window, text="Figure Size")
        my_leg.grid(row=1, column=1, sticky="ew", **self.grid_pad)

        table = {
            0: {"label": "Height (inches):", "info": info["figure_height"],
                "cm": "= " + str(info["figure_height"].get() * 2.54) + " cm", "row": 1},
            1: {"label": "Width (inches):", "info": info["figure_width"],
                "cm": "= " + str(info["figure_width"].get() * 2.54) + " cm", "row": 2},
            2: {"label": "Resolution:", "info": info["dpi"],
                "cm": "dpi", "row": 3},
        }

        for n in table:
            t = table[n]
            ttk.Label(my_leg, text=t["label"]).grid(row=t["row"], column=1, **self.grid_pad)
            ttk.Entry(my_leg, textvariable=t["info"], width=3).grid(row=t["row"], column=2, **self.grid_pad)
            ttk.Label(my_leg, text=t["cm"]).grid(row=t["row"], column=3, **self.grid_pad)

        ttk.Button(main, text="OK", command=lambda: main.destroy()).grid(
            row=3, column=1, padx=10, pady=5, sticky="nsew")

    def my_spines(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Spines")
        main = self.frame.window
        my_spin = tk.LabelFrame(self.frame.window, text="Set Spines")
        my_spin.grid(row=1, column=1, sticky="ew", padx=5, pady=2.5, ipady=5)
        opt = {"sticky": "nsew", "padx": 5, "pady": 2.5}
        # set new frame in window
        my_spines_dict = {
            1: {"label1": "X Axis Color:", "var1": self.graph_settings["x_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": self.graph_settings["x_axis_spine_line_width"], "r": 1},
            2: {"label1": "Y Axis Color:", "var1": self.graph_settings["y_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": self.graph_settings["y_axis_spine_line_width"], "r": 2},
            3: {"label1": "Top Spine Color:", "var1": self.graph_settings["top_spine_color"],
                "label2": "Top Spine Line Width:", "var2": self.graph_settings["top_spine_line_width"], "r": 3},
            4: {"label1": "Right Spine Color:", "var1": self.graph_settings["right_spine_color"],
                "label2": "Right Spine Line Width:", "var2": self.graph_settings["right_spine_line_width"], "r": 4}
        }

        for spines in my_spines_dict:
            ms = my_spines_dict[spines]
            ttk.Label(my_spin, text=ms["label1"]).grid(row=ms["r"], column=1, **opt)
            ttk.Combobox(my_spin, state="readonly", values=self.my_line_colors, justify="left", textvariable=ms["var1"],
                         width=7).grid(row=ms["r"], column=2, **opt)
            ttk.Label(my_spin, text=ms["label2"]).grid(row=ms["r"], column=3, **opt)
            ttk.Entry(my_spin, textvariable=ms["var2"], width=5).grid(row=ms["r"], column=4, **opt)

        ttk.Button(main, text="OK", command=lambda: main.destroy()).grid(row=5, column=1, **opt)

    def relist_anno(self, an, window):
        self.annos.pop(an)
        window.destroy()
        self.my_annotate()

    def my_annotate(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Annotations")
        anno_frame = tk.LabelFrame(self.frame.window, text="List of annotations")
        g_a = {
            "padx": 5,
            "pady": 5,
            "sticky": "ew",
        }
        anno_frame.grid(row=1, column=1, **g_a)
        ttk.Label(anno_frame, text="Index").grid(row=1, column=1, **g_a)
        ttk.Label(anno_frame, text="Label").grid(row=1, column=2, **g_a)

        b = 2
        try:
            for a in self.annos:
                ttk.Label(anno_frame, text=a).grid(row=b, column=1, **g_a)
                ttk.Label(anno_frame, text=self.annos[a]["title"]).grid(row=b, column=2, **g_a)
                ttk.Button(anno_frame, text='Delete', command=lambda: self.relist_anno(a, self.frame.window)).grid(
                    row=b, column=4, **g_a)
                b += 1
        except IndexError or KeyError:
            pass

        anno_frame2 = tk.LabelFrame(self.frame.window, text="Add annotation")
        anno_frame2.grid(row=1, column=2, **g_a)
        anno_frame3 = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        anno_frame3.grid(row=b, column=1, **g_a)

        def adding():
            self.frame.window.destroy()
            self.add_annotate()

        ttk.Button(anno_frame2, text="Add", command=lambda: adding()).grid(row=1, column=1, **g_a)

    def add_annotate(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Add Annotate")
        anno_frame = tk.LabelFrame(self.frame.window, text="Annotate")
        g_a = {
            "padx": 5,
            "pady": 5,
            "sticky": "nsew",
        }
        anno_frame.grid(row=1, column=1, ipady=5, **g_a)

        def add_anno():
            ind = len(self.annos) + 1
            self.annos[ind] = {}
            for opt2 in self.anno_opt:
                self.annos[ind][opt2] = self.anno_opt[opt2].get()
            self.frame.window.destroy()
            self.my_annotate()

        a = 1
        for opt, labs in zip(self.anno_opt, self.anno_labels):
            ttk.Label(anno_frame, text=opt).grid(row=a, column=1, **g_a)
            ttk.Entry(anno_frame, textvariable=self.anno_opt[opt], width=10).grid(row=a, column=2, **g_a)
            ttk.Label(anno_frame, text=labs).grid(row=a, column=3, **g_a)
            a += 1
        ttk.Button(self.frame.window, text="Add to Figure", command=lambda: add_anno()).grid(column=1, **g_a)

    def x_y(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set X/Y limits")

        opt_label = {"sticky": "nsew", "padx": 10, "pady": 2.5, "ipady": 5}
        opt_content = {"sticky": "ew", "padx": 10, "pady": 5}

        my_x_y = {
            'x_min': {'name': 'x min:', 'var': self.graph_settings["x_min_var"],
                      'row': 2, "label_col": 1, "entry_col": 2},
            'x_max': {'name': 'x max:', 'var': self.graph_settings["x_max_var"],
                      'row': 3, "label_col": 1, "entry_col": 2},
            'y_min': {'name': 'y min:', 'var': self.graph_settings["y_min_var"],
                      'row': 4, "label_col": 1, "entry_col": 2},
            'y_max': {'name': 'y max:', 'var': self.graph_settings["y_max_var"],
                      'row': 5, "label_col": 1, "entry_col": 2},
        }

        x_y_type = tk.LabelFrame(self.frame.window, text="Set Limits")
        x_y_type.grid(row=1, column=1, **opt_label)
        ttk.Label(x_y_type, text="Entered values are automatically applied.\n"
                                 "Press auto X/Y to generate approximate values.").grid(row=1, column=1, columnspan=3,
                                                                                        **opt_content)

        for pos in my_x_y:
            ttk.Label(x_y_type, text=my_x_y[pos]['name']).grid(
                row=my_x_y[pos]['row'], column=my_x_y[pos]['label_col'], **opt_content)
            ttk.Entry(x_y_type, width=15, textvariable=my_x_y[pos]['var']).grid(
                row=my_x_y[pos]['row'], column=my_x_y[pos]['entry_col'], **opt_content)

        #  auto limits
        ttk.Button(self.frame.window, text="Auto X/Y limits", command=lambda: self.x_auto()).grid(
            row=5, column=1, **opt_label)

    def plot(self):
        if not file_info.keys():
            tk.messagebox.showerror("No data loaded", "Please load a data file or select one active.")
        else:
            graph_labels["labels"].clear()
            # open window
            self.frame.window, self.frame.frame = self.call_ado_plot("Plot")
            self.frame.frame.grid()

            # Declare Menu
            self.frame.menu_bar = Menu(self.frame.window)

            # File Menu
            self.frame.file_menu = Menu(self.frame.menu_bar, tearoff=0)
            self.frame.file_menu.add_command(label="Export", command=lambda: self.save_plot())
            self.frame.menu_bar.add_cascade(label="File", menu=self.frame.file_menu)
            self.frame.window.config(menu=self.frame.menu_bar)

            # create canvas
            if self.graph_settings["interactive"].get() == 1:
                print("code reached")
                plt.ion()
            self.figure1 = plt.Figure(figsize=(self.graph_settings["figure_width"].get(),
                                               self.graph_settings["figure_height"].get()),
                                      dpi=96, constrained_layout=False,
                                      frameon=True, tight_layout={"rect": (0, 0, .95, .95)})
            self.ax1 = self.figure1.add_subplot(1, 1, 1, clip_on="off")
            self.bar1 = FigureCanvasTkAgg(self.figure1, self.frame.frame)
            self.bar1.get_tk_widget().grid()
            p_mode2 = self.graph_settings["plot_mode"].get()  # what type of plot is it

            def in_plot(my_file):
                p_mode = self.graph_settings["plot_mode"].get()  # what type of plot is it

                # gather all variables
                data = file_info[my_file]

                if data["active"].get() == 'yes':
                    graph_labels["labels"].append(data["legend"].get())
                    x = data["x_data"]
                    y = data["y_data"]
                    color = data["color"].get()
                    l_style = data["line_style"].get()
                    pre_m_style = data["marker"].get()
                    m_style = self.my_markers[pre_m_style]
                    plotting_mode = {
                        "Line": {"type": self.ax1.plot,
                                 "params": {"c": color, "linestyle": l_style, "marker": m_style}},
                        "Scatter": {"type": self.ax1.scatter,
                                    "params": {"c": color}},
                        "X_log": {"type": self.ax1.semilogx,
                                  "params": {"c": color, "linestyle": l_style}},
                        "Y_log": {"type": self.ax1.semilogy,
                                  "params": {"c": color, "linestyle": l_style}},
                    }
                    if p_mode != "Bar":
                        plotting_mode[p_mode]["type"](x, y, **plotting_mode[p_mode]["params"])
                    if p_mode == "Line":
                        if self.graph_settings["x_scale"].get() != 'reverse':
                            self.ax1.set_xscale(self.graph_settings["x_scale"].get())
                        if self.graph_settings["y_scale"].get() != 'reverse':
                            self.ax1.set_yscale(self.graph_settings["y_scale"].get())
                    if p_mode == "Bar":
                        width = 0.35
                        if self.graph_settings["bar"].get() != 0:
                            self.ax1.bar(x + width / 2, y, width=width, label=my_file)
                        else:
                            self.ax1.bar(x - width / 2, y, width=width, label=my_file)
                            self.graph_settings["bar"].set(1)
                    if self.graph_settings["fit"].get():
                        f_mode = self.graph_settings["fit"].get()
                        mode = {
                            "lin_reg": self.lin_plot,
                            "fpl": self.fpl_plot,
                            "f_peaks": self.f_peaks,
                            "uv_gibbs": self.uv_gibbs_plot,
                            "cd_two_state": self.cd_two_state,
                            "cd_two_state_lin": self.cd_two_state_lin,
                            "custom_eq": self.custom_plot,
                        }
                        mode[f_mode](my_file)

                    error_bar_opt = {
                        "c": color,
                        "ecolor": file_info[my_file]["error_color"].get(),
                        "linestyle": "none",
                        "capsize": data["cap_size"].get(),
                        "marker": m_style,
                        "barsabove": False,
                    }
                    if data["y_error_bar"].get() == 1 and data["x_error_bar"].get() == 0:
                        y_error = data["y_error"]
                        self.ax1.errorbar(x, y, yerr=y_error, **error_bar_opt)
                    if data["x_error_bar"].get() == 1 and data["y_error_bar"].get() == 0:
                        x_error = data["x_error"]
                        self.ax1.errorbar(x, y, xerr=x_error, **error_bar_opt)
                    if data["y_error_bar"].get() == 1 and data["x_error_bar"].get() == 1:
                        y_error = data["y_error"]
                        x_error = data["x_error"]
                        self.ax1.errorbar(x, y, yerr=y_error, xerr=x_error, **error_bar_opt)
                    if len(self.annos) > 0:
                        for ent in self.annos:
                            text = self.annos[ent]["title"]
                            xy = (float(self.annos[ent]["x1"]), float(self.annos[ent]["y1"]))
                            try:
                                xytext = (float(self.annos[ent]["x2"]), float(self.annos[ent]["y2"]))
                            except ValueError:
                                xytext = 0
                                pass
                            if xytext != 0:
                                self.ax1.annotate(text=text, xy=xy, xytext=xytext, arrowprops={'arrowstyle': '->'})
                            else:
                                self.ax1.annotate(text=text, xy=xy)
                else:
                    pass

            for my_file1 in file_info:
                in_plot(my_file1)

            my_spine_dict = {
                "top": {"color": self.graph_settings["top_spine_color"].get(),
                        "line_w": float(self.graph_settings["top_spine_line_width"].get())},
                "right": {"color": self.graph_settings["right_spine_color"].get(),
                          "line_w": float(self.graph_settings["right_spine_line_width"].get())},
                "left": {"color": self.graph_settings["y_axis_spine_color"].get(),
                         "line_w": float(self.graph_settings["y_axis_spine_line_width"].get())},
                "bottom": {"color": self.graph_settings["x_axis_spine_color"].get(),
                           "line_w": float(self.graph_settings["x_axis_spine_line_width"].get())},
            }

            for pos in my_spine_dict:
                self.ax1.spines[pos].set_linewidth(my_spine_dict[pos]["line_w"])
                self.ax1.spines[pos].set_color(my_spine_dict[pos]["color"])

            if p_mode2 != "Bar":
                if not self.graph_settings["x_min_var"].get():
                    self.x_auto()
                else:
                    pass

                x_lim_min = float(self.graph_settings["x_min_var"].get())
                y_lim_min = float(self.graph_settings["y_min_var"].get())
                x_lim_max = float(self.graph_settings["x_max_var"].get())
                y_lim_max = float(self.graph_settings["y_max_var"].get())

                if self.graph_settings["y_scale"].get() == 'reverse':
                    self.ax1.set_ylim(y_lim_max, y_lim_min)
                elif self.graph_settings["y_scale"].get() == "log":
                    self.ax1.set_ylim(abs(y_lim_min), abs(y_lim_max))
                else:
                    self.ax1.set_ylim(y_lim_min, y_lim_max)

                if self.graph_settings["x_scale"].get() == 'reverse':
                    self.ax1.set_xlim(x_lim_max, x_lim_min)
                elif self.graph_settings["x_scale"].get() == "log":
                    self.ax1.set_xlim(abs(x_lim_min), abs(x_lim_max))
                else:
                    self.ax1.set_xlim(x_lim_min, x_lim_max)

            x_label_font = self.graph_settings["x_label_font"].get()
            y_label_font = self.graph_settings["y_label_font"].get()
            if not self.graph_settings["legend_pos"].get():
                l_pos = 'best'
            else:
                l_pos = self.graph_settings["legend_pos"].get()
            if self.graph_settings["show_legend"].get():
                self.ax1.legend(graph_labels["labels"], frameon=self.graph_settings["legend_box"].get(), loc=l_pos)
            self.ax1.set_xlabel(self.graph_settings["x_var"].get(), fontsize=x_label_font)
            self.ax1.set_ylabel(self.graph_settings["y_var"].get(), fontsize=y_label_font)
            self.ax1.minorticks_on()
            self.ax1.tick_params(axis="x", labelsize=self.graph_settings["x_tick_size"].get())
            self.ax1.tick_params(axis="y", labelsize=self.graph_settings["y_tick_size"].get())
            self.graph_settings["bar"].set(0)

    @staticmethod
    def data_check(info):
        data_y = file_info[info]["y_data"]

        if max(data_y) < 0 and min(data_y) < 0:
            mi_lb = 1.1
            mi_ub = 0.9
            ma_lb = 1.1
            ma_ub = 0.9
        elif max(data_y) > 0 and min(data_y) > 0:
            mi_lb = 0.9
            mi_ub = 1.1
            ma_lb = 0.9
            ma_ub = 1.1
        elif max(data_y) > 0 and min(data_y) < 0:
            mi_lb = 1.1
            mi_ub = 0.9
            ma_lb = 0.9
            ma_ub = 1.1
        elif max(data_y) < 0 and min(data_y) > 0:
            mi_lb = 0.9
            mi_ub = 1.1
            ma_lb = 1.1
            ma_ub = 0.9
        else:
            mi_lb = 1
            mi_ub = 1
            ma_lb = 1
            ma_ub = 1
        return mi_lb, mi_ub, ma_lb, ma_ub

    def lin_plot(self, info):
        print(type(file_info[info]["x_data"]))

        def func(a, x, b):
            return a * x + b

        data_x = file_info[info]["x_data"]
        data_y = file_info[info]["y_data"]
        p_opt, p_cov = curve_fit(func, data_x, data_y)
        self.ax1.plot(data_x, func(data_x, *p_opt), color=self.graph_settings["fit_color"].get(), linestyle='--')
        graph_labels["labels"].append('fit: a=%5.3f, b=%5.3f' % tuple(p_opt))

    def custom_plot(self, info):
        # custom equation function
        equ = self.graph_settings["custom_eq"].get()  # input equation
        par = self.graph_settings["custom_par"].get()  # input parameters

        the_eq = 'def func(' + par + '):\n    return ' + equ + ''  # parse the inputted equation using exec
        print(the_eq)
        exec(the_eq, globals())  # make the custom equation globally available

        data_x = file_info[info]["x_data"]  # retrieve dataset variables
        data_y = file_info[info]["y_data"]
        p_opt, p_cov = curve_fit(func, data_x, data_y)  # run the curve fit
        self.ax1.plot(data_x, func(data_x, *p_opt), color=self.graph_settings["fit_color"].get(), linestyle='--')
        par_l1 = [n for n in par.split(",")]
        par_l2 = []
        for i in par_l1:
            if i != "x":
                par_l2.append(i)
        par_t = tuple(par_l2)
        par_str = ''
        for p in par_t:
            par_str = par_str + p + '=%5.3f '
        full_par_str = 'fit: ' + par_str
        graph_labels["labels"].append(full_par_str % tuple(p_opt))
        # graph_labels["labels"].append('fit: a=%5.3f, b=%5.3f' % tuple(p_opt))

    def uv_gibbs_plot(self, info):
        def func(v, u, lo, tm, h):
            m = (tm + 273.15)
            t = (v + 273.15)
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = (k / (1 + k))
            return ((u - lo) * y) + lo

        data_x = file_info[info]["x_data"]
        data_y = file_info[info]["y_data"]

        print(file_info[info].get("uv thermal"))
        if file_info[info].get("uv thermal") is None:
            mi_lb, mi_ub, ma_lb, ma_ub = self.data_check(info)
            p_opt, p_cov = curve_fit(func,
                                     data_x,
                                     data_y,
                                     bounds=([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                                             [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000]),
                                     method="trf")
            file_info[info]["uv thermal"] = {}
            file_info[info]["uv thermal"]["p_opt"] = p_opt
            file_info[info]["uv thermal"]["p_cov"] = p_cov
            print(p_opt)
            y_new = []
            for x in data_x:
                y_new.append(func(x, *p_opt))
            file_info[info]["uv thermal"]["y_new"] = y_new

            # print(p_opt) for debugging only
            self.ax1.plot(data_x, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append('fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f' % tuple(p_opt))
        else:
            p_opt = file_info[info]["uv thermal"]["p_opt"]
            y_new = file_info[info]["uv thermal"]["y_new"]

            self.ax1.plot(data_x, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append('fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f' % tuple(p_opt))

    def cd_two_state(self, info):
        def func(v, u, lo, tm, h):
            m = (tm + 273.15)
            t = (v + 273.15)
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = (k / (1 + k))
            return ((u - lo) * y) + lo

        data_x = file_info[info]["x_data"]
        data_y = file_info[info]["y_data"]

        print(file_info[info].get("cd two state"))
        if file_info[info].get("cd two state") is None:
            mi_lb, mi_ub, ma_lb, ma_ub = self.data_check(info)
            p_opt, p_cov = curve_fit(func,
                                     data_x,
                                     data_y,
                                     bounds=([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                                             [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000]),
                                     method="trf")
            file_info[info]["cd two state"] = {}
            file_info[info]["cd two state"]["p_opt"] = p_opt
            file_info[info]["cd two state"]["p_cov"] = p_cov

            y_new = []
            x_new = np.arange(min(data_x), max(data_x), 1)
            par = file_info[info]["cd two state"]["p_opt"]
            for x in x_new:
                y_new.append(func(x, *par))
            file_info[info]["cd two state"]["y_new"] = y_new
            file_info[info]["cd two state"]["x_new"] = x_new

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append('fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f' % tuple(p_opt))
        else:
            p_opt = file_info[info]["cd two state"]["p_opt"]
            y_new = file_info[info]["cd two state"]["y_new"]
            x_new = file_info[info]["cd two state"]["x_new"]

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append('fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f' % tuple(p_opt))

    def cd_two_state_lin(self, info):
        # A two-state transition of a monomer between folded and unfolded forms with correcting the data for pre- and
        # post-transition linear changes in ellipticity as a function of temperature.
        def func(v, u, lo, tm, h, u1, l1):
            m = tm + 273.15
            t = v + 273.15
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = k / (1 + k)
            return y * ((u + (u1 * v)) - (lo + (l1 * v))) + (lo + (l1 * v))

        data_x = file_info[info]["x_data"]
        data_y = file_info[info]["y_data"]

        print(file_info[info].get("cd two state lin"))
        if file_info[info].get("cd two state lin") is None:
            mi_lb, mi_ub, ma_lb, ma_ub = self.data_check(info)
            p_opt, p_cov = curve_fit(func,
                                     data_x,
                                     data_y,
                                     bounds=([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000, -1, -1],
                                             [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000, 1, 1]),
                                     method="trf")
            file_info[info]["cd two state lin"] = {}
            file_info[info]["cd two state lin"]["p_opt"] = p_opt
            file_info[info]["cd two state lin"]["p_cov"] = p_cov

            y_new = []
            x_new = np.arange(min(data_x), max(data_x), 1)
            par = file_info[info]["cd two state lin"]["p_opt"]
            for x in x_new:
                y_new.append(func(x, *par))
            file_info[info]["cd two state lin"]["y_new"] = y_new
            file_info[info]["cd two state lin"]["x_new"] = x_new

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append(
                'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, u1=%5.3f, l1=%5.3f' % tuple(p_opt))
        else:
            p_opt = file_info[info]["cd two state lin"]["p_opt"]
            y_new = file_info[info]["cd two state lin"]["y_new"]
            x_new = file_info[info]["cd two state lin"]["x_new"]

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append(
                'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, u1=%5.3f, l1=%5.3f' % tuple(p_opt))

    def fpl_plot(self, info):
        def func(xe, a, b, cc, d):
            return d + ((a - d) / (1 + ((xe / cc) ** b)))

        data_y = file_info[info]["y_data"]
        data_x = file_info[info]["x_data"]

        if file_info[info].get("fpl") is None:
            mi_lb, mi_ub, ma_lb, ma_ub = self.data_check(info)

            p_opt, p_cov = curve_fit(func, data_x, data_y, bounds=(
                [min(data_y) * mi_lb, -np.inf, min(data_x), max(data_y) * ma_lb],
                [min(data_y) * mi_ub, np.inf, max(data_x), max(data_y) * ma_ub]), method="trf")
            file_info[info]["fpl"] = {}
            file_info[info]["fpl"]["p_opt"] = p_opt
            file_info[info]["fpl"]["p_cov"] = p_cov
            y_new = []
            x_new = np.arange(min(data_x), max(data_x), abs(min(data_x)))
            par = file_info[info]["fpl"]["p_opt"]
            for x in x_new:
                y_new.append(func(x, *par))

            if self.graph_settings["use_data_for_fit_color"].get() is True:
                f_c = file_info[info]["color"].get()
            else:
                f_c = self.graph_settings["fit_color"].get()

            self.ax1.plot(x_new, y_new, color=f_c, linestyle='--')
            graph_labels["labels"].append('fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f' % tuple(par))

            file_info[info]["fpl"]["x_new"] = x_new
            file_info[info]["fpl"]["y_new"] = y_new
        else:

            if self.graph_settings["use_data_for_fit_color"].get() is True:
                f_c = file_info[info]["color"].get()
            else:
                f_c = self.graph_settings["fit_color"].get()

            p_opt = file_info[info]["fpl"]["p_opt"]
            x_new = file_info[info]["fpl"]["x_new"]
            y_new = file_info[info]["fpl"]["y_new"]

            self.ax1.plot(x_new, y_new, color=f_c, linestyle='--')
            graph_labels["labels"].append('fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f' % tuple(p_opt))

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

    def edit_picture(self):
        self.graph_settings["interactive"].set(1)
        self.plot()

    def save_plot(self):  # function to save the displayed graph
        try:  # attempt to save the image based on the following data formats
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt'),
                     ('Portable Image', '*.png'),
                     ('Document Image', '*.tif')]
            self.frame.save_file = asksaveasfile(filetypes=files, defaultextension=files)
            self.figure1.savefig(self.frame.save_file.name, dpi=self.graph_settings["dpi"].get())
        except AttributeError:  # pass when cancel is pressed
            pass

    def load_config(self):
        x = askopenfilename()  # open directory file dialog and select one config file
        split_file_string = x.split('.')  # parse the file string
        file_ext = split_file_string[1]  # extract the extension
        if file_ext == 'cfg':  # check if the file extension matches the config file format
            f = open(x)  # open the config file
            f_first_line = f.readline()  # read the first line dictionary string
            f_info = json.loads(f_first_line)  # parse the JSON string into a dict
            y = f_info  # use short variable for loop
            for fl in f_info:  # for each file name
                MyFile(fl).run_cfg()  # create an instance with tk.StringVars so we can edit the loaded config
                for k, v in y[fl].items():  # run through each subsequent key and value
                    try:
                        if k in file_info[fl]:  # if the key already exists then set the vakue
                            file_info[fl][k].set(v)
                        else:  # if it doesnt exist then try to create the key and set the type for the key before
                            # adding in the actual value
                            try:
                                file_info[fl][k] = type(v)  # set the type
                                file_info[fl][k].set(v)  # set the value(s)
                            except AttributeError:  # unless there is an attribute error
                                file_info[fl][k] = v  # accept the value as is
                    except AttributeError:  # unless there is an attribute error
                        file_info[fl][k] = v  # accept the value as is

            f_second_line = f.readline()
            y = json.loads(f_second_line)
            for d, v in y.items():
                try:
                    self.graph_settings[d].set(v)
                except AttributeError:
                    self.graph_settings[d] = v
            f.close()  # close the config file
        else:
            tk_message_box.showerror("File error", "Please load a .cfg config file format.")
        print(file_info)

    def save_config(self):
        data = [('adoconf (*.cfg)', '*.cfg')]
        x = asksaveasfile(filetypes=data, defaultextension=data)
        # several types of data formats to compare before processing in JSON
        n64 = np.int64(64)
        n32 = np.int64(32)
        nda = np.ndarray([1, 2, 4], dtype=np.int64)
        test = tk.StringVar()
        test2 = [1, 2, 3]
        test3 = tk.IntVar()

        # convert dictionary stringvar data into JSON compatible format
        def dict_json(my_data):
            data_store = {}
            if my_data == file_info:
                for info in my_data:
                    data_store[info] = {}
                    for d, v in my_data[info].items():
                        try:
                            if isinstance(v, type(n64)) or isinstance(v, type(n32)) or isinstance(v, type(nda)):
                                data_store[info][d] = v.tolist()
                            if isinstance(v, type(test)) or isinstance(v, type(test3)):
                                data_store[info][d] = v.get()
                            if isinstance(v, type(test2)):
                                data_store[info][d] = v
                        except AttributeError:
                            data_store[info][d] = v
            if my_data == self.graph_settings or self.annos:
                for d, v in my_data.items():
                    try:
                        data_store[d] = v.get()
                    except AttributeError:
                        data_store[d] = v
            if my_data == graph_labels:
                data_store["labels"] = graph_labels["labels"]
            return data_store

        # Store data in a .cfg file based on the list variables processed using the dict_json function
        if x.name and x.name is not None:
            f = open(x.name, "w")
            to_save = [file_info, self.graph_settings, graph_labels, self.annos]
            for dm in to_save:
                f.write(json.dumps(dict_json(dm)) + "\n")
            f.close()

    @staticmethod
    def do_nothing():
        pass

    @staticmethod
    def my_about():
        tk_message_box.showinfo("About",
                                "This program was made by Dr A. Doekhie. Use is purely intended for academic purposes.")

    @staticmethod
    def help():
        tk_message_box.showinfo("Help",
                                "Load one or multiple .csv/.dat files containing purely one set of x and y data.\n\n"
                                "Optionally you can added y or x error bar data"
                                "in a third or fourth column respectively.\n\n"
                                "In the data tab you can set their visual properties like color and line style.\n\n"
                                "In the graph tab you can plot the data and optimise the plot format.\n\n"
                                "Advanced fitting options are present for use but limited at this stage.\n\n"
                                "Please request more functionality on the GitHub page.\n")


class Import:
    def __init__(self):
        self.filename = askopenfilenames()
        if len(self.filename) > 1:
            for file in self.filename:
                MyFile(file).run_all()
        elif len(self.filename) == 1:
            MyFile(self.filename[0]).run_all()
        else:
            pass


class MyFile:
    def __init__(self, file):
        self.filename = file
        if self.filename is not None:
            self.extension = self.filename.split('.')
            self.ext = self.extension[1]
        self.data, self.spectra, self.x, self.y = None, None, None, None
        self.x_err, self.y_err = None, None
        self.identifier, self.length, self.name = None, None, None

    def run_all(self):
        if self.process_file():
            self.file_type()
            self.file_id()
            self.set_var()

    def run_cfg(self):
        self.file_id()
        self.set_var()

    def process_file(self):
        # try to process if possible and check for file type
        message = "Please use x/y data in .csv or .dat file type only."
        try:
            if not self.filename:
                pass
            if self.ext == "csv" or self.ext == "dat":
                if self.filename in file_info:
                    pass
                else:
                    return True
            else:
                tk_message_box.showerror("File error", message)
                return False
        except NameError:
            pass

    def file_type(self):
        # process CSV file
        if self.filename.find(".csv") > 0:
            f = open(self.filename, "r")
            f_first = f.readline()
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            header = None
            for letter in alphabet:
                if f_first.find(letter) > 0:
                    header = 0
                    # print("found letter!") # for debugging file headers
                    break
                else:
                    header = None
            self.data = pd.read_csv(self.filename, sep=',', header=header)
            self.spectra = self.data.values
            self.x = self.spectra[:, 0]
            self.y = self.spectra[:, 1]
            try:
                self.y_err = self.spectra[:, 2]
            except IndexError:
                self.y_err = []
                pass
            try:
                self.x_err = self.spectra[:, 3]
            except IndexError:
                self.x_err = []
                pass
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
                        pass
                    try:
                        self.y_err.append(float(test[var][3]))
                    except KeyError:
                        pass
                    try:
                        self.x_err.append(float(test[var][4]))
                    except KeyError:
                        pass
            f.close()  # close openend file
            self.file_id()

    def file_id(self):
        # set file parameters
        self.identifier = self.filename.split('/')
        self.length = len(self.identifier)
        self.name = self.identifier[self.length - 1]

    def set_var(self):
        # convert list to ndarray
        try:
            if type(self.x) is list:
                temp = np.asarray(self.x)
                self.x = temp
                temp = np.asarray(self.y)
                self.y = temp
        except TypeError:
            pass
        # set variables in app data array file_info
        file_info[self.filename] = {
            "color": tk.StringVar(),
            "legend": tk.StringVar(),
            "x_data": self.x,
            "y_data": self.y,
            "name": self.name,
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
        }
        try:
            d = file_info[self.filename]
            d["x_min"] = min(self.x)
            d["x_max"] = max(self.x)
            d["y_min"] = min(self.y)
            d["y_max"] = max(self.y)
        except TypeError or ValueError:
            d = file_info[self.filename]
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
        }

        for var1 in default_var:
            file_info[self.filename][var1].set(default_var[var1])

        ado_plot.list_my_dataset()


class NewFile(MyFile):

    def __init__(self):
        super().__init__(None)
        self.x = []
        self.y = []
        self.y_err = []
        self.x_err = []
        self.x_str = tk.StringVar()
        self.y_str = tk.StringVar()
        self.name = tk.StringVar()
        self.y_err_str = tk.StringVar()
        self.x_err_str = tk.StringVar()
        self.frame = tk.Toplevel(ado_plot)
        self.frame.geometry("+%d+%d" % (ado_plot.x_margin_pop, ado_plot.y_margin_pop))
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

        ttk.Button(self.frame.frame, text="Set", command=lambda: self.do_store()).grid(
            row=6, column=1, stick="ew", padx=5, pady=2.5)

    def do_store(self):
        # this function grabs the strings and converts them into lists for iteration and plotting
        if not self.name:
            pass
        else:
            # convert x/y string submitted data into x/y data lists
            d_list = [self.x, self.y]
            d_str_list = [self.x_str, self.y_str]
            for d_str, d_data in zip(d_list, d_str_list):
                f = [float(ele) for ele in str(d_data.get()).split(",")]
                for vl in f:
                    d_str.append(vl)
            # then check if x and y are same length
            if len(self.x) != len(self.y):
                tk_message_box.showerror("Data entry error", "X/Y values do not have the same amount of numbers,"
                                                             " please check your entry and try again.")
            # retrieve inputted data for x/y errors
            erc_str = [self.x_err_str, self.y_err_str]
            erc_val = [self.x_err, self.y_err]
            for check, val, comp in zip(erc_str, erc_val, d_list):
                try:
                    f = [float(ele) for ele in str(check.get()).split(",")]
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
                except ValueError:
                    pass
            # after successfully entering the new data set, close the window and return to the overview
            # by processing this in the super class
            self.frame.destroy()
            self.filename = self.name.get()
            self.file_id()
            self.set_var()


if __name__ == '__main__':
    ado_plot = MyFrame()
    ado_plot.mainloop()
