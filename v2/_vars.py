import tkinter as tk


class MySettings:
    file_info = {}  # this is the main dictionary
    # where all imported data will be stored and JSON exported capability
    the_graphs = []  # where generated graphs are stored in
    graph_labels = {"labels": []}  # separate dictionary with labels list for easy JSON export
    graph_settings = {}

    my_stats = {
        "t_test": {"name": "T-test",
                   "var": "t_test"}
    }

    my_fits = {
        "lin_reg": {"name": "Linear Regression",
                    "var": "lin_reg",
                    "mode": "MyFunction(self.ax1, f_mode).pre_process"},
        "lin_fpl": {"name": "Four Parameter Logistic",
                    "var": "lin_fpl",
                    "mode": "MyFunction(self.ax1, f_mode).pre_process"},
        "f_peaks": {"name": "Find Peaks",
                    "var": "f_peaks",
                    "mode": "MyFunction(self.ax1, f_mode).f_peaks"},
        "uv_gibbs": {"name": "UV Thermal",
                     "var": "uv_gibbs",
                     "mode": "MyFunction(self.ax1, f_mode).pre_process"},
        "cd two state": {"name": "CD two state",
                         "var": "cd two state",
                         "mode": "MyFunction(self.ax1, f_mode).pre_process"},
        "cd two state lin": {"name": "CD two state lin corr",
                             "var": "cd two state lin",
                             "mode": "MyFunction(self.ax1, f_mode).pre_process"},
        "custom eq": {"name": "Custom Equation",
                      "var": "custom eq",
                      "mode": "MyFunction(self.ax1, f_mode).custom_plot"},
    }

    my_markers = {  # marker options list
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
    grid_opt = {"sticky": "ew",  # standard arguements for the GRID widget manager
                }
    grid_opt_prop = {"sticky": "ew",  # standard arguements for the GRID widget manager
                     "padx": 10,
                     "pady": 5,
                     }
    grid_opt_prop_cont = {"sticky": "ew",  # standard arguements for the GRID widget manager
                          "padx": 10,
                          "pady": 10,
                          }
    grid_pad = {"padx": 10, "pady": 5, "ipady": 5}
    grid_pad_file = {"padx": 2.5, "pady": 2.5, "sticky": "w"}
    grid_frame_opt = {
        "sticky": "nsew",
        "ipady": 5,
        "pady": 15,
    }
    grid_frame_opt_lab = {
        "sticky": "w",
        "ipady": 0,
        "pady": 5,
        "padx": 10,
    }
    annos = {}  # empty dictionary for storing annotations
    anno_opt = {}
    anno_labels = ["Annotation label",  # labels for defining the variables to enter
                   "label (start) point x-axis",
                   "label (start) point y-axis",
                   "end point x-axis (use for arrow annotation)",
                   "end point y-axis (use for arrow annotation)"]
    my_fit_grid_opt_but = {"sticky": "nsew", "padx": 5, "pady": 2.5}
    my_fit_grid_opt_lab = {"sticky": "w", "padx": 5, "pady": 0}
    fit_alg = ["lm", "trf", "dogbox"]
    fit_description = " lm: Levenberg-Marquardt." \
                      "\n Algorithm as implemented in MINPACK. \n Doesn’t handle bounds and sparse Jacobians. \n" \
                      "\n trf: Trust Region Reflective." \
                      "\n Particularly suitable for large sparse problems with bounds.\n" \
                      " Generally robust method.\n" \
                      "\n dogbox: dogleg algorithm with rectangular trust regions. " \
                      "\n Typical use case is small problems with bounds.\n " \
                      "Not recommended for problems with rank-deficient Jacobian. "

    default_graph_var = {  # default vars that can be initialised upon program start
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
        "legend_font": 10,
        "interactive": 0,
        "legend_pos": 'best',
        "show_legend": True,
        "fit_color": 'Black',
        "dpi": 96,
        "fit_alg": "trf",
        "stats_test": None,
    }

    @staticmethod
    def set_var():
        MySettings.graph_settings = {  # graphs settings for matplot lib
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
            "fit_alg": tk.StringVar(),
            "legend_font": tk.IntVar(),
            "stats_test": tk.StringVar(),
        }

        MySettings.anno_opt = {
            # annotation options for placing text and arrows
            "title": tk.StringVar(),
            "x1": tk.StringVar(),
            "y1": tk.StringVar(),
            "x2": tk.StringVar(),
            "y2": tk.StringVar(),
        }

        for var in MySettings.default_graph_var:
            # loop over the default vars and place them in the active used dictionary
            MySettings.graph_settings[var].set(MySettings.default_graph_var[var])
