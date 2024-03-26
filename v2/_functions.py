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

    @staticmethod
    # linear regression
    def my_lin_plot(a, x, b):
        return a * x + b

    @staticmethod
    # two state sigmoidal transition using UV vis data
    def my_uv_gibbs_plot(v, u, lo, tm, h):
        m = (tm + 273.15)
        t = (v + 273.15)
        k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
        y = (k / (1 + k))
        return ((u - lo) * y) + lo

    @staticmethod
    # protein two state transition function using circular dichroism data
    def my_cd_two_state(v, u, lo, tm, h):
        m = (tm + 273.15)
        t = (v + 273.15)
        k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
        y = (k / (1 + k))
        return ((u - lo) * y) + lo

    @staticmethod
    # protein two state transtion functiong using circular dichroism data
    # accounting for linear slopes pre and post transition
    def my_cd_two_state_lin(v, u, lo, tm, h, u1, l1):
        m = tm + 273.15
        t = v + 273.15
        k = (np.exp((h / 8.314472 * v) * ((t / m) - 1)))
        y = k / (1 + k)
        return y * ((u + (u1 * v)) - (lo + (l1 * v))) + (lo + (l1 * v))

    @staticmethod
    # four parameter logistics cure
    # standard dose response curve based on data from ELISA
    def my_fpl_plot(xe, a, b, cc, d):
        return d + ((a - d) / (1 + ((xe / cc) ** b)))

    def pre_process(self, info):
        mfl = MySettings.file_info[info]
        use_fit_color = mfl["use_data_for_fit_color"]
        data_x = mfl["x_data"]
        data_y = mfl["y_data"]
        mi_lb, mi_ub, ma_lb, ma_ub = Data.data_check(info)

        if MySettings.file_info[info].get(self.type) is None:
            mfl[self.type] = {}

        if use_fit_color.get() is True:
            MySettings.graph_settings["fit_color"].set(mfl["color"].get())

        # print(use_fit_color.get(), MySettings.graph_settings["fit_color"].get(), mfl["color"].get())

        # set shortcute variable and bounds
        mfl2 = mfl[self.type]

        func = {
            "lin_reg": {
                "f": self.my_lin_plot,
                "b": ([-np.inf, min(data_y) * mi_lb], [np.inf, max(data_y) * ma_ub])},
            "lin_fpl": {
                "f": self.my_fpl_plot,
                "b": ([min(data_y) * mi_lb, -np.inf, min(data_x), max(data_y) * ma_lb],
                      [min(data_y) * mi_ub, np.inf, max(data_x), max(data_y) * ma_ub])},
            "uv_gibbs": {
                "f": self.my_uv_gibbs_plot,
                "b": ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                      [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000])},
            "cd two state": {
                "f": self.my_cd_two_state,
                "b": ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000],
                      [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000])},
            "cd two state lin": {
                "f": self.my_cd_two_state_lin,
                "b": ([max(data_y) * ma_lb, min(data_y) * mi_lb, 0, -100000, -1, -1],
                      [max(data_y) * ma_ub, min(data_y) * mi_ub, 100, 100000, 1, 1])},
        }

        def plot():
            # store fit data
            mfl2["y_new"] = []
            mfl2["x_new"] = np.arange(min(data_x), max(data_x), 1)
            for x in mfl2["x_new"]:
                mfl2["y_new"].append(func[self.type]["f"](x, *mfl2["p_opt"]))

            # create the plot
            self.ax1.plot(mfl[self.type]["x_new"], mfl[self.type]["y_new"],
                          color=MySettings.graph_settings["fit_color"].get(), linestyle='--')

            # calculate the residual R2
            residuals = data_y - func[self.type]["f"](data_x, *mfl[self.type]["p_opt"])
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((data_y - np.mean(data_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            mfl2["r_squared"] = r_squared

            # make the labels
            p1 = func_lab[self.type]["p"] % tuple(mfl2["p_opt"])
            p2 = 'r\N{SUPERSCRIPT TWO}={var1} ({var2})'.format(var1=round(r_squared, 3), var2=self.my_alg.get())
            p1 += p2
            MySettings.graph_labels["labels"].append(p1)

        # if not levenberg marquadt use bounds about for fitting
        if self.my_alg.get() != "lm":
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func[self.type]["f"], data_x, data_y,
                                                         bounds=func[self.type]["b"],
                                                         method=self.my_alg.get())
            except RuntimeError or RuntimeWarning as e:
                tk_message_box.showinfo("Fitting Failed", str(e) + "\nPlease adjust settings and retry.")
                return
        else:
            try:
                mfl2["p_opt"], mfl2["p_cov"] = curve_fit(func[self.type]["f"], data_x, data_y,
                                                     method=self.my_alg.get())
            except RuntimeError or RuntimeWarning as e:
                tk_message_box.showinfo("Fitting Failed", str(e) + "\nPlease adjust settings and retry.")
                return

        func_lab = {
            "lin_reg": {
                "p": 'fit: a=%5.3f, b=%5.3f, '},
            "lin_fpl": {
                "p": 'fit: a=%.1f, b=%.1f, c=%.1f, d=%.1f, '},
            "uv_gibbs": {
                "p": 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f '},
            "cd two state": {
                "p": 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, '},
            "cd two state lin": {
                "p": 'fit: u=%5.3f, lo=%5.3f, tm=%5.3f, h=%5.3f, u1=%5.3f, l1=%5.3f, '}
        }

        # if fitting succesfull invoke plot function
        plot()

    def custom_plot(self, info):
        # custom equation function
        equ = MySettings.graph_settings["custom_eq"].get()  # input equation
        par = MySettings.graph_settings["custom_par"].get()  # input parameters

        try:
            the_eq = 'def func(' + par + '):\n    return ' + equ + ''  # parse the inputted equation using exec
            # print(the_eq)
            exec(the_eq, globals())  # make the custom equation globally available
        except TypeError:
            return

        data_x = MySettings.file_info[info]["x_data"]  # retrieve dataset variables
        data_y = MySettings.file_info[info]["y_data"]
        p_opt, p_cov = curve_fit(func, data_x, data_y)  # run the curve fit
        self.ax1.plot(data_x, func(data_x, *p_opt), color=MySettings.graph_settings["fit_color"].get(), linestyle='--')
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
