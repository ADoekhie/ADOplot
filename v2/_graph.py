from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from _vars import MySettings
import matplotlib.pyplot as plt
from _data import Data
from _functions import MyFunction


class MyGraph:

    def __init__(self, window):
        self.frame = window  # create canvas
        if MySettings.graph_settings["interactive"] == 1:  # if MySettings.graph_settings["interactive"] == 1:
            plt.ion()

        self.figure1 = plt.Figure(figsize=(MySettings.graph_settings["figure_width"].get(),
                                           MySettings.graph_settings["figure_height"].get()),
                                  dpi=96, frameon=True, tight_layout={"rect": (0, 0, .95, .95)})
        self.ax1 = self.figure1.add_subplot(1, 1, 1, clip_on="off")
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.frame.frame)
        self.bar1.get_tk_widget().grid()
        p_mode2 = MySettings.graph_settings["plot_mode"]  # what type of plot is it

        # print(MySettings.file_info)

        def in_plot(my_file):
            p_mode = MySettings.graph_settings["plot_mode"].get()  # what type of plot is it

            # gather all variables
            data = MySettings.file_info[my_file]

            if data["active"].get():
                if data["use_legend"].get():
                    MySettings.graph_labels["labels"].append(data["legend"].get())
                else:
                    MySettings.graph_labels["labels"].append("_")
                x = data["x_data"]
                y = data["y_data"]
                color = data["color"].get()
                l_style = data["line_style"].get()
                pre_m_style = data["marker"].get()
                m_style = MySettings.my_markers[pre_m_style]
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
                    if MySettings.graph_settings["x_scale"].get() != 'reverse':
                        self.ax1.set_xscale(MySettings.graph_settings["x_scale"].get())
                    if MySettings.graph_settings["y_scale"].get() != 'reverse':
                        self.ax1.set_yscale(MySettings.graph_settings["y_scale"].get())
                if p_mode == "Bar":
                    width = float(MySettings.graph_settings["bar_width"].get())

                    if not MySettings.graph_settings["bar"].get():
                        MySettings.graph_settings["x_min_var"].set(0)
                        MySettings.graph_settings["y_max_var"].set(max(y) * 1.1)
                        MySettings.graph_settings["y_min_var"].set(min(y))
                        MySettings.graph_settings["bar"].set(True)

                        for i, a in enumerate(x):
                            self.ax1.bar(i + 1, y[i], width=width, label=my_file)
                            MySettings.graph_settings["x_max_var"].set(i + 1)
                            # print(i,a,y[i])

                    if MySettings.graph_settings["bar"].get():
                        for i, a in enumerate(x):
                            self.ax1.bar(i + 1, y[i], width=width, label=my_file)

                error_bar_opt = {
                    "c": color,
                    "ecolor": MySettings.file_info[my_file]["error_color"].get(),
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

                if MySettings.graph_settings["fit"].get():
                    try:
                        f_mode = MySettings.graph_settings["fit"].get()
                        mode = "" + MySettings.my_fits[f_mode]["mode"] + "('" + my_file + "')"
                        exec(mode)
                    except KeyError:
                        return

                if len(MySettings.annos) > 0:
                    for ent in MySettings.annos:
                        text = MySettings.annos[ent]["title"]
                        xy = (float(MySettings.annos[ent]["x1"]), float(MySettings.annos[ent]["y1"]))
                        try:
                            xy_text = (float(MySettings.annos[ent]["x2"]),
                                       float(MySettings.annos[ent]["y2"]))
                        except ValueError:
                            xy_text = 0
                            pass
                        if xy_text != 0:
                            self.ax1.annotate(text=text, xy=xy, xytext=xy_text, arrowprops={'arrowstyle': '->'})
                        else:
                            self.ax1.annotate(text=text, xy=xy)

            else:
                return

        for my_file1 in MySettings.file_info:
            in_plot(my_file1)

        my_spine_dict = {
            "top": {"color": MySettings.graph_settings["top_spine_color"].get(),
                    "line_w": float(MySettings.graph_settings["top_spine_line_width"].get())},
            "right": {"color": MySettings.graph_settings["right_spine_color"].get(),
                      "line_w": float(MySettings.graph_settings["right_spine_line_width"].get())},
            "left": {"color": MySettings.graph_settings["y_axis_spine_color"].get(),
                     "line_w": float(MySettings.graph_settings["y_axis_spine_line_width"].get())},
            "bottom": {"color": MySettings.graph_settings["x_axis_spine_color"].get(),
                       "line_w": float(MySettings.graph_settings["x_axis_spine_line_width"].get())},
        }

        for pos in my_spine_dict:
            self.ax1.spines[pos].set_linewidth(my_spine_dict[pos]["line_w"])
            self.ax1.spines[pos].set_color(my_spine_dict[pos]["color"])

        if p_mode2 != "Bar":
            if not MySettings.graph_settings["x_min_var"]:
                if KeyError:
                    Data.x_auto()
            else:
                pass

        x_lim_min = float(MySettings.graph_settings["x_min_var"].get())
        y_lim_min = float(MySettings.graph_settings["y_min_var"].get())
        x_lim_max = float(MySettings.graph_settings["x_max_var"].get())
        y_lim_max = float(MySettings.graph_settings["y_max_var"].get())

        if MySettings.graph_settings["y_scale"].get() == 'reverse':
            self.ax1.set_ylim(y_lim_max, y_lim_min)
        elif MySettings.graph_settings["y_scale"].get() == "log":
            self.ax1.set_ylim(abs(y_lim_min), abs(y_lim_max))
        else:
            self.ax1.set_ylim(y_lim_min, y_lim_max)

        if MySettings.graph_settings["x_scale"].get() == 'reverse':
            self.ax1.set_xlim(x_lim_max, x_lim_min)
        elif MySettings.graph_settings["x_scale"].get() == "log":
            self.ax1.set_xlim(abs(x_lim_min)+0.001, abs(x_lim_max))
        else:
            self.ax1.set_xlim(x_lim_min, x_lim_max)

        x_label_font = MySettings.graph_settings["x_label_font"].get()
        y_label_font = MySettings.graph_settings["y_label_font"].get()
        l_font = MySettings.graph_settings["legend_font"].get()
        if not MySettings.graph_settings["legend_pos"].get():
            l_pos = 'best'
        else:
            l_pos = MySettings.graph_settings["legend_pos"].get()

        if MySettings.graph_settings["Grid X-axis"].get() and MySettings.graph_settings["Grid Y-axis"].get():
            self.ax1.grid(which="both", color='0.85')
        elif MySettings.graph_settings["Grid X-axis"].get():
            self.ax1.grid(which="both", axis='x', color='0.85')
        elif MySettings.graph_settings["Grid Y-axis"].get():
            self.ax1.grid(which="both", axis='y', color='0.85')

        if MySettings.graph_settings["show_legend"].get():
            self.ax1.legend(MySettings.graph_labels["labels"],
                            frameon=MySettings.graph_settings["legend_box"].get(),
                            loc=l_pos, fontsize=l_font)
        self.ax1.set_xlabel(MySettings.graph_settings["x_var"].get(), fontsize=x_label_font)
        self.ax1.set_ylabel(MySettings.graph_settings["y_var"].get(), fontsize=y_label_font)
        self.ax1.minorticks_on()
        self.ax1.tick_params(axis="x", labelsize=MySettings.graph_settings["x_tick_size"].get())
        self.ax1.tick_params(axis="y", labelsize=MySettings.graph_settings["y_tick_size"].get())
        plt.rcParams["font.family"] = "sans-serif"
