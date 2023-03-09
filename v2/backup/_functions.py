from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from _data import *
import numpy as np
import tkinter.messagebox as tk_message_box


class MyFunction:

    def __init__(self, ax, f_mode):
        self.ax1 = ax
        self.my_alg = MySettings.graph_settings["fit_alg"]
        self.fit = 0
        self.type = f_mode

    def pre_process(self, info):

        mfl = MySettings.file_info[info]
        data_x = mfl["x_data"]
        data_y = mfl["y_data"]

        # protein two state transition function
        def func(v, u, lo, tm, h):
            m = (tm + 273.15)
            t = (v + 273.15)
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = (k / (1 + k))
            return ((u - lo) * y) + lo

        def plot():
            # store fit data
            mfl2["y_new"] = []
            mfl2["x_new"] = np.arange(min(data_x), max(data_x), 1)
            for x in mfl2["x_new"]:
                mfl2["y_new"].append(func(x, *mfl2["p_opt"]))

            # create the plot
            self.ax1.plot(mfl[self.type]["x_new"], mfl["self.type"]["y_new"],
                          color=MySettings.graph_settings["fit_color"].get(), linestyle='--')

            # calculate the residual R2
            residuals = data_y - func(data_x, *mfl[self.type]["p_opt"])
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            # make the labels
            p1 = 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, ' % tuple(mfl[self.type]["p_opt"])
            p2 = 'r\N{SUPERSCRIPT TWO}={var1} ({var2})'.format(var1=round(r_squared, 3), var2=self.my_alg.get())
            p1 += p2
            MySettings.graph_labels["labels"].append(p1)

        if MySettings.file_info[info].get(self.type) is None:
            mfl[self.type] = {}

        # set shortcute variable and bounds
        mfl2 = mfl[self.type]
        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)
        my_bounds = ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                     [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000])

        # if not levenberg marquadt use bounds about for fitting
        if self.my_alg.get() != "lm":
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, bounds=my_bounds,
                                                         method=self.my_alg.get())
            except RuntimeError:
                tk_message_box.showinfo("Fitting Failed",
                                        "Optimal parameters not found:"
                                        "The maximum number of function evaluations is exceeded.")
                return
        else:
            mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, method=self.my_alg.get())

        # if fitting succesfull invoke plot function
        plot()

    def custom_plot(self, info):
        # custom equation function
        equ = MySettings.graph_settings["custom_eq"]  # input equation
        par = MySettings.graph_settings["custom_par"]  # input parameters

        the_eq = 'def func(' + par + '):\n    return ' + equ + ''  # parse the inputted equation using exec
        print(the_eq)
        exec(the_eq, globals())  # make the custom equation globally available

        data_x = MySettings.file_info[info]["x_data"]  # retrieve dataset variables
        data_y = MySettings.file_info[info]["y_data"]
        p_opt, p_cov = curve_fit(func, data_x, data_y)  # run the curve fit
        self.ax1.plot(data_x, func(data_x, *p_opt), color=MySettings.graph_settings["fit_color"], linestyle='--')
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
        MySettings.graph_labels["labels"].append(full_par_str % tuple(p_opt))
        # MySettings.graph_labels["labels"].append('fit: a=%5.3f, b=%5.3f' % tuple(p_opt))

    def uv_gibbs_plot(self, info):
        mfl = MySettings.file_info[info]
        data_x = mfl["x_data"]
        data_y = mfl["y_data"]

        def func(v, u, lo, tm, h):
            m = (tm + 273.15)
            t = (v + 273.15)
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = (k / (1 + k))
            return ((u - lo) * y) + lo

        def plot():
            mfl2["y_new"] = []
            for x in data_x:
                mfl2["y_new"].append(func(x, *mfl2["p_opt"]))

            self.ax1.plot(data_x, mfl2["y_new"], color=MySettings.graph_settings["fit_color"].get(), linestyle='--')
            MySettings.graph_labels["labels"].append('fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f' % tuple(mfl2["p_opt"]))

        if MySettings.file_info[info].get("uv thermal") is None:
            mfl["uv thermal"] = {}

        mfl2 = mfl["uv thermal"]
        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)
        my_bounds = ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                     [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000])

        if self.my_alg.get() != "lm":
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, bounds=my_bounds, method=self.my_alg.get())
            except RuntimeError:
                tk_message_box.showinfo("Fitting Failed",
                                        "Optimal parameters not found:"
                                        "The maximum number of function evaluations is exceeded.")
        else:
            mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, bounds=my_bounds, method=self.my_alg.get())

        plot()

    def cd_two_state(self, info):
        mfl = MySettings.file_info[info]
        data_x = mfl["x_data"]
        data_y = mfl["y_data"]

        # protein two state transition function
        def func(v, u, lo, tm, h):
            m = (tm + 273.15)
            t = (v + 273.15)
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = (k / (1 + k))
            return ((u - lo) * y) + lo

        def plot():
            # store fit data
            mfl2["y_new"] = []
            mfl2["x_new"] = np.arange(min(data_x), max(data_x), 1)
            for x in mfl2["x_new"]:
                mfl2["y_new"].append(func(x, *mfl2["p_opt"]))

            # create the plot
            self.ax1.plot(mfl["cd two state"]["x_new"], mfl["cd two state"]["y_new"],
                          color=MySettings.graph_settings["fit_color"].get(), linestyle='--')

            # calculate the residual R2
            residuals = data_y - func(data_x, *mfl["cd two state"]["p_opt"])
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            # make the labels
            p1 = 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, ' % tuple(mfl["cd two state"]["p_opt"])
            p2 = 'r\N{SUPERSCRIPT TWO}={var1} ({var2})'.format(var1=round(r_squared, 3), var2=self.my_alg.get())
            p1 += p2
            MySettings.graph_labels["labels"].append(p1)

        if MySettings.file_info[info].get("cd two state") is None:
            mfl["cd two state"] = {}

        # set shortcute variable and bounds
        mfl2 = mfl["cd two state"]
        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)
        my_bounds = ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                     [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000])

        # if not levenberg marquadt use bounds about for fitting
        if self.my_alg.get() != "lm":
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, bounds=my_bounds,
                                                         method=self.my_alg.get())
            except RuntimeError:
                tk_message_box.showinfo("Fitting Failed",
                                        "Optimal parameters not found:"
                                        "The maximum number of function evaluations is exceeded.")
                return
        else:
            mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, method=self.my_alg.get())

        # if fitting succesfull invoke plot function
        plot()

    def cd_two_state_lin(self, info):
        mfl = MySettings.file_info[info]
        data_x = mfl["x_data"]
        data_y = mfl["y_data"]

        # protein two state transition with correction of linear slopes
        def func(v, u, lo, tm, h, u1, l1):
            m = tm + 273.15
            t = v + 273.15
            k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
            y = k / (1 + k)
            return y * ((u + (u1 * v)) - (lo + (l1 * v))) + (lo + (l1 * v))

        def plot():
            # store fit data
            mfl2["y_new"] = []
            mfl2["x_new"] = np.arange(min(data_x), max(data_x), 1)
            for x in mfl2["x_new"]:
                mfl2["y_new"].append(func(x, *mfl2["p_opt"]))

            # create the plot
            self.ax1.plot(mfl["cd two state lin"]["x_new"], mfl["cd two state lin"]["y_new"],
                          color=MySettings.graph_settings["fit_color"].get(), linestyle='--')

            # calculate the residual R2
            residuals = data_y - func(data_x, *mfl["cd two state lin"]["p_opt"])
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            # make the labels
            p1 = 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, u1=%5.3f, l1=%5.3f, ' % tuple(
                mfl["cd two state lin"]["p_opt"])
            p2 = 'r\N{SUPERSCRIPT TWO}=%5.3f' % r_squared
            p1 += p2
            MySettings.graph_labels["labels"].append(p1)

        if MySettings.file_info[info].get("cd two state lin") is None:
            mfl["cd two state lin"] = {}

        mfl2 = mfl["cd two state lin"]
        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)
        my_bounds = ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000, -1, -1],
                     [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000, 1, 1])

        if self.my_alg.get() != "lm":
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, bounds=my_bounds,
                                                         method=self.my_alg.get())
            except RuntimeError:
                tk_message_box.showinfo("Fitting Failed",
                                        "Optimal parameters not found:"
                                        "The maximum number of function evaluations is exceeded.")
                return
        else:
            mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func, data_x, data_y, method=self.my_alg.get())

        # if fitting succesfull invoke plot function
        plot()

    def fpl_plot(self, info):
        mfl = MySettings.file_info[info]
        data_y = mfl["y_data"]
        data_x = mfl["x_data"]

        def func(xe, a, b, cc, d):
            return d + ((a - d) / (1 + ((xe / cc) ** b)))

        def color_check():
            if MySettings.graph_settings["use_data_for_fit_color"] is True:
                return MySettings.file_info[info]["color"].get()
            else:
                return MySettings.graph_settings["fit_color"].get()

        def plot():
            mfl["fpl"]["y_new"] = []
            mfl["fpl"]["x_new"] = np.arange(min(data_x), max(data_x), abs(min(data_x)))

            for x in mfl["fpl"]["x_new"]:
                mfl["fpl"]["y_new"].append(func(x, *mfl["fpl"]["p_opt"]))

            self.ax1.plot(mfl["fpl"]["x_new"], mfl["fpl"]["y_new"], color=color_check(), linestyle='--')

            residuals = data_y - func(data_x, *mfl["fpl"]["p_opt"])
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            p1 = 'fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f, ' % tuple(mfl["fpl"]["p_opt"])
            p2 = 'r\N{SUPERSCRIPT TWO}=%5.3f' % r_squared
            p1 += p2
            MySettings.graph_labels["labels"].append(p1)

        if MySettings.file_info[info].get("fpl") is None:
            MySettings.file_info[info]["fpl"] = {}

        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)
        my_bounds = ([min(data_y) * mi_lb, -np.inf, min(data_x), max(data_y) * ma_lb],
                     [min(data_y) * mi_ub, np.inf, max(data_x), max(data_y) * ma_ub])

        if self.my_alg.get() != "lm":
            try:
                mfl["fpl"]["p_opt"], mfl["fpl"]["p_cov"] = curve_fit(func, data_x, data_y,
                                                                     bounds=my_bounds, method=self.my_alg.get())
            except RuntimeError:
                tk_message_box.showinfo("Fitting Failed",
                                        "Optimal parameters not found:"
                                        "The maximum number of function evaluations is exceeded.")
            return
        else:
            mfl["fpl"]["p_opt"], mfl["fpl"]["p_cov"] = curve_fit(func, data_x, data_y, method=self.my_alg.get())

        plot()

    def f_peaks(self, info):
        y = MySettings.file_info[info]["y_data"]
        x = MySettings.file_info[info]["x_data"]
        y2 = 1 / y
        try:
            peaks, _ = find_peaks(y2, width=((max(x) - min(x)) * .01))
        except RuntimeError:
            tk_message_box.showinfo("Fitting Failed",
                                    "Optimal parameters not found:"
                                    "The maximum number of function evaluations is exceeded.")
            return

        self.ax1.plot(x[peaks], 1 / y2[peaks], "x", color=MySettings.graph_settings["fit_color"].get())
        a = 0
        for n in x[peaks]:
            self.ax1.text(n, (1 / y2[peaks][a]) * 0.99, s=str(int(n)))
            a += 1

    def lin_plot(self, info):
        print(type(MySettings.file_info[info]["x_data"]))

        def func(a, x, b):
            return a * x + b

        data_x = MySettings.file_info[info]["x_data"]
        data_y = MySettings.file_info[info]["y_data"]

        try:
            p_opt, p_cov = curve_fit(func, data_x, data_y)
        except RuntimeError:
            tk_message_box.showinfo("Fitting Failed",
                                    "Optimal parameters not found:"
                                    "The maximum number of function evaluations is exceeded.")
            return

        residuals = data_y - func(data_x, *p_opt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        self.ax1.plot(data_x, func(data_x, *p_opt), color=MySettings.graph_settings["fit_color"].get(), linestyle='--')
        p1 = 'fit: a=%5.3f, b=%5.3f, ' % tuple(p_opt)
        p2 = 'r\N{SUPERSCRIPT TWO}=%5.3f' % r_squared
        p1 += p2

        MySettings.graph_labels["labels"].append(p1)
