from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.messagebox as tk_message_box
from tkinter import *
import json
from _file_processing import *
from _graph import *
from _stats import *


class MyFrame(tk.Tk):  # The window frame this program runs in

    def __init__(self):
        super().__init__()  # initialise all tkinter functions

        self.file_info = MySettings.file_info   # window frame settings
        MySettings.set_var()     # initialise program dynamic variables
        self.graph_set = MySettings.graph_settings
        self.graph_lab = MySettings.graph_labels
        self.ann = MySettings.annos
        self.original_dpi = 143.858407079646    # dpi of the screen this program was made on
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
        self.my_line_colors = MySettings.line_colors
        self.par = {}
        self.error_message = ""
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
        self.tab_stats = ttk.Frame(self.tab_main)
        self.tab_main.add(self.tab_data, text='Data')
        self.tab_main.add(self.tab_graph, text='Graph')
        # self.tab_main.add(self.tab_stats, text='Stats')
        # self.tab_main.add(self.tab_script, text='Script')
        self.tab_main.grid()
        self.graph = MySettings.graph_settings

        # tab data labelframe and grid
        # self.spacer(self.tab_data, 1, 1)
        self.tab_data_ls = tk.LabelFrame(self.tab_data, text="Options")
        self.tab_data_ls.grid(row=1, column=0, **MySettings.grid_frame_opt)
        # self.spacer(self.tab_data, 1, 3)
        self.tab_data_rs = tk.LabelFrame(self.tab_data, text="Data View")
        self.tab_data_rs.grid(row=1, column=1, columnspan=3, **MySettings.grid_frame_opt)
        # self.spacer(self.tab_data, 1, 5)
        self.tab_data.grid_columnconfigure(0, weight=1, uniform="u")

        # tab graph labelframe and grid
        # self.spacer(self.tab_graph, 1, 1)
        self.tab_graph_ls = tk.LabelFrame(self.tab_graph, text="Options")
        self.tab_graph_ls.grid(row=1, column=0, **MySettings.grid_frame_opt)
        # self.spacer(self.tab_graph, 1, 3)
        self.tab_graph_rs = tk.LabelFrame(self.tab_graph, text="Graph Labels")
        self.tab_graph_rs.grid(row=1, column=1, columnspan=3, **MySettings.grid_frame_opt)
        # self.spacer(self.tab_graph, 1, 5)
        self.tab_graph_rs1 = tk.LabelFrame(self.tab_graph, text="Advanced")
        self.tab_graph_rs1.grid(row=1, column=4, **MySettings.grid_frame_opt)
        # self.spacer(self.tab_graph, 1, 7)

        # tab stats labelframe and grid
        # self.spacer(self.tab_stats, 1, 1)
        # self.tab_stats_ls = tk.LabelFrame(self.tab_stats, text="Statistics")
        # self.tab_stats_ls.grid(row=1, column=2, **MySettings.grid_frame_opt)

        # self.spacer(self.tab_stats, 1, 3)
        # self.tab_stats_md = tk.LabelFrame(self.tab_stats, text="Description")
        # self.tab_stats_md.grid(row=1, column=4, **MySettings.grid_frame_opt)

        # invoke all options
        self.my_tabs()
        self.my_file_header()
        self.window, self.ax1, self.figure1, self.bar1 = None, None, None, None

    def my_tabs(self):
        tabs = {  # tab data buttons
            1: {"loc": self.tab_data_ls, "text": "Load File(s)", "cm": self.my_import, "y": 1, "cst": 5},
            2: {"loc": self.tab_data_ls, "text": "New Dataset", "cm": self.my_new_dataset, "y": 2, "cst": 2},
            3: {"loc": self.tab_graph_ls, "text": "Plot Graph", "cm": self.plot, "y": 1},
            4: {"loc": self.tab_graph_ls, "text": "Set Type", "cm": self.graph_type, "y": 2},
            5: {"loc": self.tab_graph_ls, "text": "Set X/Y", "cm": self.x_y, "y": 3},
            6: {"loc": self.tab_graph_rs1, "text": "Fit Options", "cm": self.my_fit, "y": 1},
            7: {"loc": self.tab_graph_rs1, "text": "Font Style", "cm": self.my_font, "y": 2},
            8: {"loc": self.tab_graph_rs1, "text": "Set Spines", "cm": self.my_spines, "y": 3},
            9: {"loc": self.tab_graph_ls, "text": "Set Legend", "cm": self.my_legend, "y": 4},
            10: {"loc": self.tab_graph_ls, "text": "Annotate", "cm": self.my_annotate, "y": 5},
            11: {"loc": self.tab_graph_rs1, "text": "Set Figure", "cm": self.my_figure_size, "y": 4},
            12: {"loc": self.tab_graph_rs1, "text": "Edit Figure", "cm": self.edit_picture, "y": 5},
            # 13: {"loc": self.tab_stats_ls, "text": "Choose test", "cm": self.my_stats, "y": 1},
            # 14: {"loc": self.tab_stats_ls, "text": "Run test", "cm": self.my_run_stats, "y": 2},
        }
        for t in tabs:
            try:
                self.my_button(loc=tabs[t]["loc"], text=tabs[t]["text"], cm=tabs[t]["cm"], y=tabs[t]["y"],
                               columnspan=tabs[t]["cst"])
            except KeyError:
                self.my_button(loc=tabs[t]["loc"], text=tabs[t]["text"], cm=tabs[t]["cm"], y=tabs[t]["y"])

        self.tab_graph_ls.grid_columnconfigure(0, weight=1, uniform="u")

        # label entries for graph
        ttk.Label(self.tab_graph_rs, text="X-Label:").grid(row=1, column=1, **MySettings.grid_frame_opt_lab)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["x_var"], width=35).grid(
            row=1, column=2, columnspan=3, **MySettings.grid_frame_opt_lab)
        ttk.Label(self.tab_graph_rs, text="Y-Label:").grid(row=2, column=1, **MySettings.grid_frame_opt_lab)
        ttk.Entry(self.tab_graph_rs, textvariable=self.graph["y_var"], width=35).grid(
            row=2, column=2, columnspan=3, **MySettings.grid_frame_opt_lab)

    def my_file_header(self):  # Header row for loaded files
        loc = self.tab_data_rs
        opt = MySettings.grid_pad_file
        # tk.Canvas(loc, bg="#ccc", height=2, width=450).grid(row=0, column=1, columnspan=5, pady=5, padx=10)
        tk.Canvas(loc, bg="#ccc", height=2).grid(row=0, column=0, columnspan=5, pady=2.5, padx=2.5)
        ttk.Label(loc, text="#").grid(row=1, column=0, **opt)
        ttk.Label(loc, text="File \t").grid(row=1, column=1, **opt)
        ttk.Label(loc, text="Properties").grid(row=1, column=2, **opt)
        tk.Canvas(loc, bg="#ccc", height=2).grid(row=2, column=0, columnspan=5, pady=2.5, padx=2.5)

    @staticmethod
    def spacer(lc, r, c):
        _ = ttk.Label(lc, text=" ", width=1)
        _.grid(row=r, column=c)
        return _

    def del_all(self):  # delete all data function
        MySettings.file_info.clear()
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
        self.list_my_dataset()

    def get_script(self):
        store = self.script.get("1.0", "end-1c")
        return store

    def list_my_dataset(self):  # list all data files loaded into the main dictionary
        if not MySettings.file_info:
            return
        elif len(MySettings.file_info) == 0:
            return
        else:
            self.my_file_header()

            def place_buttons(my_file, b):  # create the buttons that can set, edit and view data
                plc = self.tab_data_rs
                d = my_file
                cms = [self.my_properties, self.show_data, self.relist_my_dataset]
                grid_opt = {"sticky": "w", "padx": 2.5, "pady": 5}
                grid_opt_b = {"sticky": "w", "padx": 2.5, "pady": 5}
                ttk.Checkbutton(plc, offvalue="no", onvalue="yes", variable=MySettings.file_info[d]["active"],
                                state=NORMAL).grid(row=b, column=0, **grid_opt)
                ttk.Label(plc, text=MySettings.file_info[my_file]["name"]).grid(row=b, column=1, **grid_opt)
                ttk.Button(plc, text="Set", command=lambda: cms[0](d)).grid(row=b, column=2, **grid_opt_b)
                ttk.Button(plc, text="View Data", command=lambda: cms[1](d)).grid(row=b, column=3, **grid_opt_b)
                ttk.Button(plc, text="Delete", command=lambda: cms[2](d)).grid(row=b, column=4, **grid_opt_b)

            ab = 3
            for my_file1 in MySettings.file_info:
                place_buttons(my_file1, ab)
                ab += 1

    def relist_my_dataset(self, file):  # remove a file from the main dictionary and loop again to refersh file list
        MySettings.file_info.pop(file)
        for widgets in self.tab_data_rs.winfo_children():
            widgets.destroy()
        self.my_file_header()
        self.list_my_dataset()

    @staticmethod
    def my_button(loc, text, cm, y, x=1, **columnspan):
        _ = ttk.Button(master=loc, text=text, command=cm)
        _.grid(row=y, column=x, **MySettings.grid_pad, sticky="nsew", **columnspan)
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
        self.frame.help_menu.add_command(label="Help", command=self.my_help)
        self.frame.help_menu.add_command(label="About...", command=self.my_about)
        self.frame.menu_bar.add_cascade(label="Help", menu=self.frame.help_menu)
        self.config(menu=self.frame.menu_bar)
        self.frame.grid()

    def call_ado_plot(self, title):  # Standard toplevel window function for other functions to use
        # open new window
        self.frame.window = tk.Toplevel(self)
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

        # print((MySettings.file_info[file]["y_error"]))
        # print((MySettings.file_info[file]["x_error"]))

        for x in range(len(MySettings.file_info[file]["x_data"])):
            self.frame.text.insert(INSERT, MySettings.file_info[file]["x_data"][x])
            self.frame.text.insert(INSERT, "\t")
            self.frame.text.insert(INSERT, MySettings.file_info[file]["y_data"][x])
            self.frame.text.insert(INSERT, "\t")
            if len(MySettings.file_info[file]["y_error"]) > 0:
                try:
                    self.frame.text.insert(INSERT, MySettings.file_info[file]["y_error"][x])
                    self.frame.text.insert(INSERT, "\t")
                except IndexError or TypeError as error_message:
                    self.my_debug(str(error_message))
                    self.frame.text.insert(INSERT, "\t")
                    pass
            if len(MySettings.file_info[file]["x_error"]) > 0:
                try:
                    self.frame.text.insert(INSERT, MySettings.file_info[file]["x_error"][x])
                    self.frame.text.insert(INSERT, "\t")
                except IndexError or TypeError as error_message:
                    self.my_debug(str(error_message))
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
        graph_type_var = [MySettings.graph_settings["plot_mode"],
                          MySettings.graph_settings["x_scale"],
                          MySettings.graph_settings["y_scale"]]

        for gtype, col, tl, gtv in zip(graph_type_list, range(1, 4, 1), type_list, graph_type_var):
            gt = tk.LabelFrame(self.frame.window, text=gtype)
            gt.grid(column=col, **graph_type_grid_opt)
            ttk.Combobox(gt, state="readonly", values=tl,
                         justify="left", textvariable=gtv,
                         width=10).grid(column=col, **graph_type_grid_opt)

        if MySettings.graph_settings["plot_mode"].get() == "Bar":
            ttk.Label(self.frame.window, text="Bar Width").grid(row=2, column=1, **graph_type_grid_opt_but)
            ttk.Entry(self.frame.window,
                      textvariable=MySettings.graph_settings["bar_width"]).grid(
                row=2, column=2, **graph_type_grid_opt_but)

        ttk.Button(self.frame.window, text="OK",
                   command=lambda: self.frame.window.destroy()).grid(row=3, column=1, **graph_type_grid_opt_but)
        ttk.Button(self.frame.window, text="Cancel",
                   command=lambda: self.frame.window.destroy()).grid(row=3, column=2, **graph_type_grid_opt_but)

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
            "legend Font Size": "legend_font",
        }

        for a, fo in enumerate(my_font_dict):
            ttk.Label(font_options, text=fo).grid(row=a, column=1, **opt_c)
            ttk.Entry(font_options, textvariable=MySettings.graph_settings[my_font_dict[fo]], width=3).grid(
                row=a, column=2, **opt_c)

        # close window
        ttk.Button(main, text="OK", command=lambda: main.destroy()).grid(column=1, **opt_f)

    def my_properties(self, my_file):
        # open window and set variables
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Properties")
        kw = MySettings.grid_opt_prop
        kw_c = MySettings.grid_opt_prop_cont
        lab_opt = {}
        fym = MySettings.file_info[my_file]
        main = self.frame.window

        self.frame.color = tk.LabelFrame(self.frame.window, text="Line Color", **lab_opt)
        self.frame.line = tk.LabelFrame(self.frame.window, text="Line Style", **lab_opt)
        self.frame.marker = tk.LabelFrame(self.frame.window, text="Markers", **lab_opt)

        for f in [self.frame.color, self.frame.line, self.frame.marker]:
            f.grid(column=1, **kw)

        if MySettings.graph_settings["fit"]:
            self.frame.dcolor = tk.LabelFrame(self.frame.window, text="fit color", **lab_opt)
            self.frame.dcolor.grid(row=0, column=2, **kw)
            ttk.Checkbutton(self.frame.dcolor, onvalue=True, offvalue=False,
                            variable=fym["use_data_for_fit_color"]).grid(column=2, **kw_c)

        for err, err_bar, r in zip(["y_error", "x_error"], ["y_error_bar", "x_error_bar"], [1, 2]):
            try:
                if len(fym[err]) > 0:
                    self.frame.err = tk.LabelFrame(self.frame.window, text=err + " bars", **lab_opt)
                    ser = self.frame.err
                    ser.grid(row=r, column=2, **kw)
                    ttk.Checkbutton(ser, onvalue=1, offvalue=0, variable=fym[err_bar]).grid(row=1, column=1, **kw_c)
                    ttk.Label(ser, text="Cap Size").grid(row=1, column=2, **kw)
                    ttk.Entry(ser, textvariable=fym["cap_size"], width=2).grid(row=1, column=3, **kw_c)
            except ValueError:
                pass

        if len(MySettings.file_info[my_file]["x_error"]) > 0 or len(MySettings.file_info[my_file]["y_error"]) > 0:
            self.frame.err = tk.LabelFrame(self.frame.window, text="Error Bar Color", **lab_opt)
            self.frame.err.grid(row=4, column=2, **kw)
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
        my_fits = MySettings.my_fits

        # run through all available fit options
        for r, fits in enumerate(my_fits):
            ttk.Checkbutton(my_fit_window, text=my_fits[fits]["name"], onvalue=my_fits[fits]["var"], offvalue="",
                            variable=MySettings.graph_settings["fit"]).grid(row=r, column=1, **my_fit_grid_opt_but)
            ttk.Button(my_fit_window, text="info",
                       command=lambda i=my_fits[fits]: self.my_fit_info(i)).grid(row=r, column=2, **my_fit_grid_opt_but)

        # set fitting algorithm
        my_fit_window2 = tk.LabelFrame(self.frame.window, text="Set Algorithm")
        my_fit_window2.grid(row=1, column=3, stick="nsew", padx=5, pady=2.5, ipady=5)
        ttk.Combobox(my_fit_window2, state="readonly", values=MySettings.fit_alg, justify="left",
                     textvariable=MySettings.graph_settings["fit_alg"]).grid(
            column=1, **my_fit_grid_opt_but)

        # add fit description
        ttk.Label(my_fit_window2, text=MySettings.fit_description).grid(
            column=1)

        # button for custom equations that will popup a new window
        custom_fit = ttk.Button(self.frame.window, text="Set Custom Equation",
                                command=lambda: self.my_custom_eq())
        custom_fit.grid(row=2, column=1, **my_fit_grid_opt_but)

        my_other_fit_window = tk.LabelFrame(self.frame.window, text="Additional Options")
        my_other_fit_window.grid(row=3, column=1, stick="nsew", padx=5, pady=2.5, ipady=5)
        mo_fw = my_other_fit_window

        ttk.Label(mo_fw, text="Fit Color").grid(column=1, **my_fit_grid_opt_lab)
        # fit line colors
        ttk.Combobox(mo_fw, state="readonly", values=self.my_line_colors, justify="left",
                     textvariable=MySettings.graph_settings["fit_color"]).grid(
            column=1, columnspan=2, **my_fit_grid_opt_but)
        ttk.Button(main, text="Set", command=lambda: main.destroy()).grid(column=1, **my_fit_grid_opt_but)

    def my_fit_info(self, ind):
        self.frame.window, self.frame.frame = self.call_ado_plot("Detailed Information")
        data = MySettings.graph_settings
        main = self.frame.window

        my_fit_info_window = tk.LabelFrame(self.frame.window, text="Model description")
        my_fit_info_window.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5, ipady=5)

        ttk.Label(my_fit_info_window, text=ind["desc"]).grid()

    def my_stats(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Statistics")
        my_fit_grid_opt_but = {"sticky": "nsew", "padx": 5, "pady": 2.5}
        # my_fit_grid_opt_lab = {"sticky": "w", "padx": 5, "pady": 0}
        main = self.frame.window

        my_fit_window = tk.LabelFrame(self.frame.window, text="Select Test")
        my_fit_window.grid(row=1, column=1, stick="nsew", padx=5, pady=2.5, ipady=5)

        # set new frame in window
        my_stats = MySettings.my_stats

        # run through all available fit options
        for fits in my_stats:
            ttk.Checkbutton(my_fit_window, text=my_stats[fits]["name"], onvalue=my_stats[fits]["var"], offvalue="",
                            variable=MySettings.graph_settings["stats_test"]).grid(column=1, **my_fit_grid_opt_but)

        ttk.Button(main, text="Set", command=lambda: main.destroy()).grid(column=1, **my_fit_grid_opt_but)

    @staticmethod
    def my_run_stats():
        y = [1, 4, 1, 3, 2, 17, 15, 14, 15, 1, 15, 14]

        my_stat = Stats.t_test(y, 10)
        # print(my_stat)

    def my_custom_eq(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Input custom equation")
        data = MySettings.graph_settings
        main = self.frame.window

        lf1 = ttk.LabelFrame(self.frame.window, text="Input equation")
        lf1.grid(row=1, **MySettings.grid_frame_opt_lab)
        ttk.Entry(lf1, textvariable=data["custom_eq"], width=20).grid(row=1, **MySettings.my_fit_grid_opt_but)
        ttk.Label(lf1, text="Define Parameters").grid(row=2, **MySettings.my_fit_grid_opt_lab)
        ttk.Entry(lf1, textvariable=data["custom_par"], width=20).grid(row=3, **MySettings.my_fit_grid_opt_but)
        ttk.Button(lf1, text="Set", command=lambda: main.destroy()).grid(row=4, **MySettings.my_fit_grid_opt_but)

    def my_legend(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Add data labels")

        grid_opt_but = {"sticky": "nsew", "padx": 10, "pady": 5}  # button grid options
        grid_opt_lab = {"sticky": "w", "padx": 10, "pady": 2.5}  # label grid options

        legend_loc = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
                      'center right', 'lower center', 'upper center', 'center']

        my_leg = tk.LabelFrame(self.frame.window, text="Legend Labels")
        my_leg.grid(row=1, column=1, sticky="nsew", **MySettings.grid_pad)
        if not MySettings.graph_labels["labels"]:
            ttk.Label(my_leg, text="No data loaded").grid(**grid_opt_lab)

        # set new frame in window
        for a, item in enumerate(MySettings.file_info):
            data = MySettings.file_info[item]
            ttk.Label(my_leg, text=data["name"]).grid(row=a, column=1, **grid_opt_but)
            ttk.Entry(my_leg, textvariable=data["legend"]).grid(row=a, column=2, **grid_opt_but)
            ttk.Checkbutton(my_leg, text="Display", onvalue=True, offvalue=False,
                            variable=data["use_legend"]).grid(row=a, column=3, **grid_opt_but)

        # Another label frame to hold legend options
        my_leg_opt = tk.LabelFrame(self.frame.window, text="Legend Options")
        my_leg_opt.grid(row=2, column=1, sticky="nsew", **MySettings.grid_pad)
        # Box on or off button
        ttk.Checkbutton(my_leg_opt, text="Box On/Off", onvalue=1, offvalue=0,
                        variable=MySettings.graph_settings["legend_box"]).grid(row=1, column=1, **grid_opt_but)
        ttk.Checkbutton(my_leg_opt, text="Show Legend", onvalue=True, offvalue=False,
                        variable=MySettings.graph_settings["show_legend"]).grid(row=2, column=1, **grid_opt_but)
        # Combobox legend location
        ttk.Label(my_leg_opt, text="Set Legend Location:").grid(row=3, column=1, **grid_opt_lab)
        ttk.Combobox(my_leg_opt, textvariable=MySettings.graph_settings["legend_pos"], values=legend_loc,
                     state="readonly", justify="left").grid(row=4, column=1, columnspan=2, **grid_opt_but)
        # Close window button 'OK'
        ttk.Button(self.frame.window, text="Set",
                   command=lambda: self.frame.window.destroy()).grid(row=3, column=1, **grid_opt_but)

    def my_figure_size(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set Figure Size")
        main = self.frame.window
        info = MySettings.graph_settings
        my_leg = tk.LabelFrame(self.frame.window, text="Figure Size")
        my_leg.grid(row=1, column=1, sticky="ew", **MySettings.grid_pad)

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
            ttk.Label(my_leg, text=t["label"]).grid(row=t["row"], column=1, **MySettings.grid_pad)
            ttk.Entry(my_leg, textvariable=t["info"], width=3).grid(row=t["row"], column=2, **MySettings.grid_pad)
            ttk.Label(my_leg, text=t["cm"]).grid(row=t["row"], column=3, **MySettings.grid_pad)

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
            1: {"label1": "X Axis Color:", "var1": MySettings.graph_settings["x_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": MySettings.graph_settings["x_axis_spine_line_width"], "r": 1},
            2: {"label1": "Y Axis Color:", "var1": MySettings.graph_settings["y_axis_spine_color"],
                "label2": "Y Axis Line Width:", "var2": MySettings.graph_settings["y_axis_spine_line_width"], "r": 2},
            3: {"label1": "Top Spine Color:", "var1": MySettings.graph_settings["top_spine_color"],
                "label2": "Top Spine Line Width:", "var2": MySettings.graph_settings["top_spine_line_width"], "r": 3},
            4: {"label1": "Right Spine Color:", "var1": MySettings.graph_settings["right_spine_color"],
                "label2": "Right Spine Line Width:", "var2": MySettings.graph_settings["right_spine_line_width"],
                "r": 4}
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
        MySettings.annos.pop(an)
        window.destroy()
        self.my_annotate()

    def my_annotate(self):
        # open windo
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

        try:
            for b, a in enumerate(MySettings.annos):
                ttk.Label(anno_frame, text=a).grid(row=b, column=1, **g_a)
                ttk.Label(anno_frame, text=MySettings.annos[a]["title"]).grid(row=b, column=2, **g_a)
                ttk.Button(anno_frame, text='Delete', command=lambda: self.relist_anno(a, self.frame.window)).grid(
                    row=b, column=4, **g_a)
        except IndexError or KeyError:
            return

        anno_frame2 = tk.LabelFrame(self.frame.window, text="Add annotation")
        anno_frame2.grid(row=1, column=2, **g_a)
        anno_frame3 = ttk.Button(self.frame.window, text="OK", command=lambda: self.frame.window.destroy())
        anno_frame3.grid(column=1, **g_a)

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
            ind = len(MySettings.annos) + 1
            MySettings.annos[ind] = {}
            for opt2 in MySettings.anno_opt:
                MySettings.annos[ind][opt2] = MySettings.anno_opt[opt2].get()

            self.frame.window.destroy()
            self.my_annotate()

        a = 1
        for opt, labs in zip(MySettings.anno_opt, MySettings.anno_labels):
            ttk.Label(anno_frame, text=opt).grid(row=a, column=1, **g_a)
            ttk.Entry(anno_frame, textvariable=MySettings.anno_opt[opt], width=10).grid(row=a, column=2, **g_a)
            ttk.Label(anno_frame, text=labs).grid(row=a, column=3, **g_a)
            a += 1
        ttk.Button(self.frame.window, text="Add to Figure", command=lambda: add_anno()).grid(column=1, **g_a)

    def x_y(self):
        # open window
        self.frame.window, self.frame.frame = self.call_ado_plot("Set X/Y limits")

        opt_label = {"sticky": "nsew", "padx": 10, "pady": 2.5, "ipady": 5}
        opt_content = {"sticky": "ew", "padx": 10, "pady": 5}

        my_x_y = {
            'x_min': {'name': 'x min:', 'var': MySettings.graph_settings["x_min_var"],
                      'row': 2, "label_col": 1, "entry_col": 2},
            'x_max': {'name': 'x max:', 'var': MySettings.graph_settings["x_max_var"],
                      'row': 3, "label_col": 1, "entry_col": 2},
            'y_min': {'name': 'y min:', 'var': MySettings.graph_settings["y_min_var"],
                      'row': 4, "label_col": 1, "entry_col": 2},
            'y_max': {'name': 'y max:', 'var': MySettings.graph_settings["y_max_var"],
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
        ttk.Button(self.frame.window, text="Auto X/Y limits", command=lambda: Data.x_auto()).grid(
            row=5, column=1, **opt_label)

    def plot(self):
        if not MySettings.file_info.keys():
            tk.messagebox.showerror("No data loaded", "Please load a data file or select one active.")
        else:
            MySettings.graph_labels["labels"].clear()
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
            MySettings.the_graphs.append(MyGraph(self.frame))

    def edit_picture(self):
        MySettings.graph_settings["interactive"].set(1)
        self.plot()

    def save_plot(self):  # function to save the displayed graph
        try:  # attempt to save the image based on the following data formats
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt'),
                     ('Portable Image', '*.png'),
                     ('Document Image', '*.tif')]
            self.frame.save_file = asksaveasfile(filetypes=files, defaultextension=files)
            # print(MySettings.the_graphs[0].ax1)
            MySettings.the_graphs[-1].figure1.savefig(self.frame.save_file.name,
                                                      dpi=MySettings.graph_settings["dpi"].get())
        except AttributeError as error_message:  # return when cancel is pressed
            self.my_debug(error_message)
            return

    def load_config(self):
        try:
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
                            if k in MySettings.file_info[fl]:  # if the key already exists then set the vakue
                                MySettings.file_info[fl][k].set(v)
                            else:  # if it doesnt exist then try to create the key and set the type for the key before
                                # adding in the actual value
                                try:
                                    MySettings.file_info[fl][k] = type(v)  # set the type
                                    MySettings.file_info[fl][k].set(v)  # set the value(s)
                                except AttributeError:  # unless there is an attribute error
                                    MySettings.file_info[fl][k] = v  # accept the value as is
                        except AttributeError:  # unless there is an attribute error
                            MySettings.file_info[fl][k] = v  # accept the value as is
                try:
                    f_second_line = f.readline()
                    y = json.loads(f_second_line)
                except json.decoder.JSONDecodeError:
                    return

                for d, v in y.items():
                    try:
                        MySettings.graph_settings[d].set(v)
                    except AttributeError:
                        MySettings.graph_settings[d] = v
                f.close()  # close the config file
                self.list_my_dataset()
            else:
                tk_message_box.showerror("File error", "Please load a .cfg config file format.")
            # print(MySettings.file_info)
        except IndexError:
            return

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
            if my_data == MySettings.file_info:
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
            if my_data == MySettings.graph_settings:
                for d, v in my_data.items():
                    try:
                        if isinstance(v, type(n64)) or isinstance(v, type(n32)) or isinstance(v, type(nda)):
                            data_store[d] = v.tolist()
                        if isinstance(v, type(test)) or isinstance(v, type(test3)):
                            data_store[d] = v.get()
                        if isinstance(v, type(test2)):
                            data_store[d] = v
                    except AttributeError:
                        data_store[d] = v
            if my_data == MySettings.annos:
                for d, v in my_data.items():
                    try:
                        data_store[d] = v
                    except AttributeError:
                        data_store[d] = v
            if my_data == MySettings.graph_labels:
                data_store["labels"] = MySettings.graph_labels["labels"]
            return data_store

        # Store data in a .cfg file based on the list variables processed using the dict_json function
        try:
            if x.name and x.name is not None:
                f = open(x.name, "w")
                to_save = [self.file_info, self.graph_set, self.graph_lab, self.ann]
                for dm in to_save:
                    f.write(json.dumps(dict_json(dm)) + "\n")
                    #  print(dict_json(dm))
                f.close()
        except AttributeError:
            return

    def my_import(self):
        Import()
        self.list_my_dataset()

    def my_new_dataset(self):
        NewFile()
        self.list_my_dataset()

    @staticmethod
    def do_nothing():
        return

    @staticmethod
    def my_about():
        tk_message_box.showinfo("About",
                                "This program was made by Dr A. Doekhie. "
                                "Use is purely intended for data visualisation and statistics. "
                                "This program comes with absolutely NO WARRANTY.")

    @staticmethod
    def my_help():
        tk_message_box.showinfo("Help",
                                "Load one or multiple .csv/.dat files containing purely one set of x and y data.\n\n"
                                "Optionally you can added y or x error bar data"
                                "in a third or fourth column respectively.\n\n"
                                "In the data tab you can set their visual properties like color and line style.\n\n"
                                "In the graph tab you can plot the data and optimise the plot format.\n\n"
                                "Advanced fitting options are present for use but limited at this stage.\n\n"
                                "Please request more functionality on the GitHub page.\n")

    @staticmethod
    def my_debug(message):
        tk_message_box.showerror("error", message)


if __name__ == '__main__':
    ado_plot = MyFrame()
    ado_plot.mainloop()
