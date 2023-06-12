import tkinter.messagebox as tk_message_box
from _vars import *


class Data:

    @staticmethod
    def data_check(info):
        data_y = MySettings.file_info[info]["y_data"]
        a = 0.5
        b = 1.5

        if max(data_y) < 0 and min(data_y) < 0:
            mi_lb = b
            mi_ub = a
            ma_lb = b
            ma_ub = a
        elif max(data_y) > 0 and min(data_y) > 0:
            mi_lb = a
            mi_ub = b
            ma_lb = a
            ma_ub = b
        elif max(data_y) > 0 and min(data_y) < 0:
            mi_lb = b
            mi_ub = a
            ma_lb = a
            ma_ub = b
        elif max(data_y) < 0 and min(data_y) > 0:
            mi_lb = a
            mi_ub = b
            ma_lb = b
            ma_ub = a
        else:
            mi_lb = 1
            mi_ub = 1
            ma_lb = 1
            ma_ub = 1
        return mi_lb, mi_ub, ma_lb, ma_ub

    @staticmethod
    def x_auto():  # This function autmatically sets the x/y limits based on the fractions chosen
        if not MySettings.file_info:
            tk_message_box.showerror("Error", "Please load a data file")
            pass
        else:
            m_list = list(MySettings.file_info.keys())
            data = MySettings.file_info[m_list[0]]
            x_max, x_min, y_max, y_min = data["x_max"], data["x_min"], data["y_max"], data["y_min"]
            f1 = 1.1
            f2 = 0.9
            minmax_list = {
                1: {"name": x_max, "var": MySettings.graph_settings["x_max_var"], "factor1": f1, "factor2": f2},
                2: {"name": y_max, "var": MySettings.graph_settings["y_max_var"], "factor1": f1, "factor2": f2},
                3: {"name": x_min, "var": MySettings.graph_settings["x_min_var"], "factor1": f2, "factor2": f1},
                4: {"name": y_min, "var": MySettings.graph_settings["y_min_var"], "factor1": f2, "factor2": f1},
            }

            for m_max in minmax_list:
                if minmax_list[m_max]["name"] >= 0:
                    minmax_list[m_max]["var"].set(float(minmax_list[m_max]["name"] * minmax_list[m_max]["factor1"]))
                elif minmax_list[m_max]["name"] <= 0:
                    minmax_list[m_max]["var"].set(float(minmax_list[m_max]["name"] * minmax_list[m_max]["factor2"]))
                else:
                    return
