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

file_info = {}
graph_labels = {"labels": []}


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
        self.my_line_colors = ['Black', 'Blue', 'Green', 'Red', 'Cyan', 'Magenta', 'Yellow', 'White']

        self.graph_settings = {
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
            "legend_box": tk.IntVar(),
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
        }

        self.default_graph_var = {
            "x_var": 'test',
            "y_var": 'test',
            "legend_box": 0,
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
        }

        self.my_markers = {
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

        self.grid_opt = {"sticky": tk.NSEW,
                         "padx": 2.5,
                         "pady": 2.5,
                         "ipadx": 2.5,
                         "ipady": 2.5,
                         }

        self.grid_frame_opt = {
            "sticky": tk.NSEW,
            "padx": 5,
            "pady": 5,
            "ipadx": 5,
            "ipady": 5,
        }

        self.annos = {}

        self.anno_opt = {
            "title": tk.StringVar(),
            "x1": tk.StringVar(),
            "y1": tk.StringVar(),
            "x2": tk.StringVar(),
            "y2": tk.StringVar(),
        }

        self.anno_labels = ["Annotation label",
                            "label (start) point x-axis",
                            "label (start) point y-axis",
                            "end point x-axis (use for arrow annotation)",
                            "end point y-axis (use for arrow annotation)"]

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
        self.tab_data_ls.grid(row=1, column=1, **self.grid_frame_opt)
        self.tab_data_rs = ttk.LabelFrame(self.tab_data, text='Data View')
        self.tab_data_rs.grid(row=1, column=2, **self.grid_frame_opt)

        # tab graph labelframe and grid
        self.tab_graph_ls = ttk.LabelFrame(self.tab_graph, text='Options')
        self.tab_graph_ls.grid(row=1, column=1, **self.grid_frame_opt)
        self.tab_graph_rs = ttk.LabelFrame(self.tab_graph, text='Graph Labels')
        self.tab_graph_rs.grid(row=1, column=2, **self.grid_frame_opt)
        self.tab_graph_rs1 = ttk.LabelFrame(self.tab_graph, text='Advanced')
        self.tab_graph_rs1.grid(row=1, column=3, **self.grid_frame_opt)

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
        ttk.Label(self.tab_graph_rs, text="X-Label:").grid(row=1, column=1, **self.grid_frame_opt)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["x_var"]).grid(
            row=1, column=2, **self.grid_frame_opt)
        ttk.Label(self.tab_graph_rs, text="Y-Label:").grid(row=2, column=1, **self.grid_frame_opt)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["y_var"], width=10).grid(
            row=2, column=2, **self.grid_frame_opt)

    def my_file_header(self):
        ttk.Label(self.tab_data_rs, text="#").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.tab_data_rs, text="File:").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(self.tab_data_rs, text="Properties:").grid(row=1, column=3, padx=5, pady=5)

    def del_all(self):
        file_info.clear()
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
        self.list_my_dataset()

    def list_my_dataset(self):
        if not file_info:
            pass
        elif len(file_info) == 0:
            pass
        else:
            self.my_file_header()

            def place_buttons(my_file, b):
                plc = self.tab_data_rs
                d = my_file
                cms = [self.my_properties, self.show_data, self.relist_my_dataset]
                grid_opt = {"padx": 5, "pady": 5}
                ttk.Checkbutton(plc, offvalue="no", onvalue="yes", variable=file_info[d]["active"],
                                state=NORMAL).grid(row=b, column=1, **grid_opt)
                ttk.Label(plc, text=file_info[my_file]["name"]).grid(row=b, column=2, **grid_opt)
                ttk.Button(plc, text="Set Properties", command=lambda: cms[0](d)).grid(row=b, column=3, **grid_opt)
                ttk.Button(plc, text="View Data", command=lambda: cms[1](d)).grid(row=b, column=4, **grid_opt)
                ttk.Button(plc, text="Delete", command=lambda: cms[2](d)).grid(row=b, column=5, **grid_opt)

            ab = 2
            for my_file1 in file_info:
                place_buttons(my_file1, ab)
                ab += 1
        self.after(50)

    def relist_my_dataset(self, file):
        file_info.pop(file)
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
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

        # Data Menu
        self.frame.data_menu = Menu(self.frame.menu_bar, tearoff=0)
        self.frame.data_menu.add_command(label="Save Config", command=self.save_config)
        self.frame.data_menu.add_command(label="Load Config", command=self.load_config)
        self.frame.menu_bar.add_cascade(label="Config", menu=self.frame.data_menu)

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
        self.frame.text.insert(INSERT, "\t")
        self.frame.text.insert(INSERT, 'X Error')
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

        def set_grid(gr, gc):
            _.grid(sticky="nsew", row=gr, column=gc, padx=5, pady=2.5)

        gtype = ttk.LabelFrame(self.frame.window, text="Graph Type")
        gtype.grid(row=1, column=1, sticky="nsew", padx=5, pady=2.5)

        gtype2 = ttk.LabelFrame(self.frame.window, text="Scale Type X")
        gtype2.grid(row=1, column=2, sticky="nsew", padx=5, pady=2.5)

        gtype3 = ttk.LabelFrame(self.frame.window, text="Scale Type Y")
        gtype3.grid(row=1, column=3, sticky="nsew", padx=5, pady=2.5)

        # check buttons for graph type
        graph_type = ['Line', 'Scatter', 'Bar', 'X_log', 'Y_log']
        scale_type = ['linear', 'log', 'symlog', 'logit', 'reverse']

        _ = ttk.Combobox(gtype,
                         state="readonly",
                         values=graph_type,
                         justify="left",
                         textvariable=self.graph_settings["plot_mode"],
                         width=10)
        set_grid(1, 1)

        _ = ttk.Combobox(gtype2,
                         state="readonly",
                         values=scale_type,
                         justify="left",
                         textvariable=self.graph_settings["x_scale"],
                         width=10)
        set_grid(1, 1)
        _ = ttk.Combobox(gtype3,
                         state="readonly",
                         values=scale_type,
                         justify="left",
                         textvariable=self.graph_settings["y_scale"],
                         width=10)
        set_grid(1, 1)

        _ = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        set_grid(2, 1)

    def my_font(self):
        # open new window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Font")

        # LABEL FRAME
        font_options = ttk.LabelFrame(self.frame.window, text="Font Options")
        font_options.grid(row=1, column=1, padx=5, pady=2.5)

        # Options
        my_font_dict = {
            "X Label Font Size": "x_label_font",
            "Y Label Font Size": "y_label_font",
            "X Tick Font Size": "x_tick_size",
            "Y Tick Font Size": "y_tick_size",
        }

        a = 1
        for fo in my_font_dict:
            ttk.Label(font_options, text=fo).grid(row=a, column=1, sticky="w", padx=5, pady=2.5)
            ttk.Entry(font_options, textvariable=self.graph_settings[my_font_dict[fo]], width=3).grid(
                row=a, column=2, padx=5, pady=2.5)
            a += 1

        # close window
        ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy()).grid(
            row=a, column=1, columnspan=2)

    def my_properties(self, my_file):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Properties")

        def set_grid(gr, gc):
            _.grid(row=gr, column=gc, **self.grid_opt)

        self.frame.color = ttk.LabelFrame(self.frame.window, text="Set Color")
        self.frame.color.grid(row=1, column=1, **self.grid_opt)
        self.frame.line = ttk.LabelFrame(self.frame.window, text="Set Line")
        self.frame.line.grid(row=2, column=1, **self.grid_opt)
        self.frame.marker = ttk.LabelFrame(self.frame.window, text="Set Marker")
        self.frame.marker.grid(row=3, column=1, **self.grid_opt)
        if len(file_info[my_file]["y_error"]) > 0:
            self.frame.err = ttk.LabelFrame(self.frame.window, text="Y Error Bars")
            self.frame.err.grid(row=1, column=2, **self.grid_opt)
            _ = ttk.Checkbutton(self.frame.err, onvalue=1, offvalue=0, variable=file_info[my_file]["y_error_bar"])
            set_grid(1, 1)
            _ = ttk.Label(self.frame.err, text="Cap Size")

            set_grid(1, 2)
            _ = ttk.Entry(self.frame.err, textvariable=file_info[my_file]["cap_size"], width=2)
            set_grid(1, 3)
        else:
            pass
        if len(file_info[my_file]["x_error"]) > 0:
            self.frame.err = ttk.LabelFrame(self.frame.window, text="X Error Bars")
            self.frame.err.grid(row=2, column=2, **self.grid_opt)
            _ = ttk.Checkbutton(self.frame.err, onvalue=1, offvalue=0, variable=file_info[my_file]["x_error_bar"])
            set_grid(1, 1)
            _ = ttk.Label(self.frame.err, text="Cap Size")

            set_grid(1, 2)
            _ = ttk.Entry(self.frame.err, textvariable=file_info[my_file]["cap_size"], width=2)
            set_grid(1, 3)
        else:
            pass
        if len(file_info[my_file]["x_error"]) > 0 or len(file_info[my_file]["y_error"]) > 0:
            self.frame.err = ttk.LabelFrame(self.frame.window, text="Error Bar Color")
            self.frame.err.grid(row=3, column=2, **self.grid_opt)
            # set colors in labelframe
            _ = ttk.Combobox(self.frame.err,
                             state="readonly",
                             values=self.my_line_colors,
                             justify="left",
                             textvariable=file_info[my_file]["error_color"],
                             width=10)
            _.grid(row=2, column=1, columnspan=3, **self.grid_opt)
        else:
            pass
        # set colors in labelframe
        _ = ttk.Combobox(self.frame.color,
                         state="readonly",
                         values=self.my_line_colors,
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
                          "diamond",
                          "none",
                          ]

        _ = ttk.Combobox(self.frame.marker,
                         state="readonly",
                         values=my_marker_list,
                         justify="left",
                         textvariable=file_info[my_file]["marker"],
                         width=10)
        set_grid(1, 1)
        _ = ttk.Button(self.frame.window, text="Set", command=lambda: self.frame.window.withdraw())
        set_grid(5, 1)
        _ = ttk.Button(self.frame.window, text="Close", command=lambda: self.frame.window.destroy())
        set_grid(5, 2)

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

        _ = ttk.Combobox(self.frame.window,
                         state="readonly",
                         values=self.my_line_colors,
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
        _ = ttk.Entry(my_leg, textvariable=info["figure_height"], width=2)
        set_grid(1, 2)
        _ = ttk.Label(my_leg, text="= " + str(info["figure_height"].get() * 2.54) + " cm")
        set_grid(1, 3)
        _ = ttk.Label(my_leg, text="Width (inches):")
        set_grid(2, 1)
        _ = ttk.Entry(my_leg, textvariable=info["figure_width"], width=2)
        set_grid(2, 2)
        _ = ttk.Label(my_leg, text="= " + str(info["figure_width"].get() * 2.54) + " cm")
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
                "label2": "Y Axis Line Width:", "var2": self.graph_settings["y_axis_spine_line_width"]},
            3: {"label1": "Top Spine Color:", "var1": self.graph_settings["top_spine_color"],
                "label2": "Top Spine Line Width:", "var2": self.graph_settings["top_spine_line_width"]},
            4: {"label1": "Right Spine Color:", "var1": self.graph_settings["right_spine_color"],
                "label2": "Right Spine Line Width:", "var2": self.graph_settings["right_spine_line_width"]}
        }

        a = 1

        for spines in my_spines_dict:
            _ = ttk.Label(my_spin, text=my_spines_dict[spines]["label1"])
            set_grid(a, 1)
            _ = ttk.Combobox(my_spin,
                             state="readonly",
                             values=self.my_line_colors,
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

    def relist_anno(self, an, window):
        self.annos.pop(an)
        window.destroy()
        self.my_annotate()

    def my_annotate(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Annotations")
        anno_frame = ttk.LabelFrame(self.frame.window, text="List of annotations")
        g_a = {
            "padx": 5,
            "pady": 5,
            "sticky": tk.NSEW,
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

        anno_frame2 = ttk.LabelFrame(self.frame.window, text="Add annotation")
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
        anno_frame = ttk.LabelFrame(self.frame.window, text="Annotate")
        g_a = {
            "padx": 5,
            "pady": 5,
            "sticky": tk.NSEW,
        }
        anno_frame.grid(row=1, column=1, **g_a)

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
        ttk.Button(anno_frame, text="Add to Figure", command=lambda: add_anno()).grid(column=2)

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
        else:
            pass

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
        self.ax1.legend(graph_labels["labels"], frameon=False, loc="best")
        self.ax1.set_xlabel(self.graph_settings["x_var"].get(), fontsize=x_label_font)
        self.ax1.set_ylabel(self.graph_settings["y_var"].get(), fontsize=y_label_font)
        self.ax1.minorticks_on()
        self.ax1.tick_params(axis="x", labelsize=self.graph_settings["x_tick_size"].get())
        self.ax1.tick_params(axis="y", labelsize=self.graph_settings["y_tick_size"].get())
        self.graph_settings["bar"].set(0)

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

        dat = file_info[info]
        data_y = dat["y_data"]
        data_x = dat["x_data"]

        if dat.get("p_opt") is None:
            try:
                if data_y[0] < data_y[-1]:
                    p_opt, p_cov = curve_fit(func, data_x, data_y, bounds=([-4, -np.inf, min(data_x), min(data_y)],
                                                                           [min(data_y), np.inf, max(data_x),
                                                                            max(data_y)]), method="trf")
                    dat["p_opt"] = p_opt
                    dat["p_cov"] = p_cov

                elif data_y[0] > data_y[-1]:
                    p_opt, p_cov = curve_fit(func, data_x, data_y, bounds=([min(data_y), -np.inf, min(data_x), -4],
                                                                           [max(data_y),
                                                                            np.inf,
                                                                            max(data_x),
                                                                            min(data_y)]), method="trf")
                    dat["p_opt"] = p_opt
                    dat["p_cov"] = p_cov
            except ValueError:
                pass

            y_new = []
            x_new = np.arange(min(data_x), max(data_x), (len(data_x) / 10))

            par = dat["p_opt"]
            for x in x_new:
                y_new.append(func(x, *par))

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
            graph_labels["labels"].append('fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f' % tuple(par))

            dat["x_new"] = x_new
            dat["y_new"] = y_new
        else:
            p_opt = dat["p_opt"]
            x_new = dat["x_new"]
            y_new = dat["y_new"]

            self.ax1.plot(x_new, y_new, color=self.graph_settings["fit_color"].get(), linestyle='--')
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
            self.figure1.savefig(self.frame.save_file.name, dpi=300)
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

    def save_config(self):
        data = [('adoconf (*.cfg)', '*.cfg')]
        x = asksaveasfile(filetypes=data, defaultextension=data)
        n64 = np.int64(64)
        n32 = np.int64(32)
        nda = np.ndarray([1, 2, 4], dtype=np.int64)
        test = tk.StringVar()
        test2 = [1, 2, 3]
        test3 = tk.IntVar()

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
                                "This program was made by A. Doekhie. Use is purely intended for academic purposes.")

    @staticmethod
    def help():
        tk_message_box.showinfo("Help",
                                "Load a or multiple .csv files containing purely one set of x and y data. "
                                "Optionally you can added y or x error bar data "
                                "in a third or fourth column respectively"
                                "In the data tab you can set their visual properties like color and linestyle. "
                                "In the graph tab you can plot the data and optimise the plot format. "
                                "Advanced fitting options are present for use but limited at this stage. "
                                "Please request more functionality on the GitHub page.")


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
            self.data = pd.read_csv(self.filename, sep=',')
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
        except TypeError:
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
        self.frame.frame.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5)

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
                    row=e["r"], column=1, stick="nsew", padx=5, pady=2.5)
            if e["type"] == "ent":
                ttk.Entry(self.frame.frame, textvariable=e["v"]).grid(
                    row=e["r"], column=2, stick="nsew", padx=5, pady=2.5)

        ttk.Button(self.frame.frame, text="Set", command=lambda: self.do_store()).grid(
            row=6, column=1, stick="nsew", padx=5, pady=2.5)

    def do_store(self):
        # this function grabs the strings and converts them into lists for iteration and plotting
        if not self.name:
            pass
        else:
            # conver x/y string submitted data into x/y data lists
            erc_com = [self.x, self.y]
            erc_com_str = [self.x_str, self.y_str]
            for dstr, ddata in zip(erc_com, erc_com_str):
                t_split = str(ddata)
                f = t_split.split(",")
                erc_com = [float(ele) for ele in f]
            # then check if x and y are same length
            if len(self.x) != len(self.y):
                tk_message_box.showerror("Data entry error", "X/Y values do not have the same amount of numbers,"
                                                             " please check your entry and try again.")
            # retrieve inputted data for x/y errors
            erc_str = [self.x_err_str, self.y_err_str]
            erc_val = [self.x_err, self.y_err]
            for check, val, comp in zip(erc_str, erc_val, erc_com):
                try:
                    err_split = str(check.get())
                    err_f = err_split.split(",")
                    val = ([float(ele) for ele in err_f])
                    # check if there are any variables and if so compare to the length of x/y
                    # to make sure they're the same
                    if len(val) > 1:
                        print(val)
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
