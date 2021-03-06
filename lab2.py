# -*- encoding: utf-8 -*-
from spyre import server
import pandas as pd
import numpy as np
import os


class StockExample(server.App):
    title = "SpecProgLab2"

    inputs = [{"input_type": 'dropdown',
                    "label": 'Region',
                    "options": [{"label": "Вінницька", "value": "1"},
                                        {"label": "Миколаївська", "value": "13"},
                                        {"label": "Волинська", "value": "2"},
                                        {"label": "Одеська", "value": "14"},
                                        {"label": "Дніпропетровська", "value": "3"},
                                        {"label": "Полтавська", "value": "15"},
                                        {"label": "Донецька", "value": "4"},
                                        {"label": "Рівенська", "value": "16"},
                                        {"label": "Житомирська", "value": "5"},
                                        {"label": "Сумська", "value": "17"},
                                        {"label": "Закарпатська", "value": "6"},
                                        {"label": "Тернопільська", "value": "18"},
                                        {"label": "Запорізька", "value": "7"},
                                        {"label": "Харківська", "value": "19"},
                                        {"label": "Івано-Франківська", "value": "8"},
                                        {"label": "Херсонська", "value": "20"},
                                        {"label": "Київська", "value": "9"},
                                        {"label": "Хмельницька", "value": "21"},
                                        {"label": "Кіровоградська", "value": "10"},
                                        {"label": "Черкаська", "value": "22"},
                                        {"label": "Луганська", "value": "11"},
                                        {"label": "Чернівецька", "value": "23"},
                                        {"label": "Львівська", "value": "12"},
                                        {"label": "Чернігівська", "value": "24"},
                                        {"label": "Республіка Крим", "value": "25"}],
                    "variable_name": 'region',
                    "action_id": "update_data"},
                    {"input_type": 'dropdown',
                    "label": 'Index',
                    "options": [{"label": "VCI", "value": "VCI"},
                                        {"label": "TCI", "value": "TCI"},
                                        {"label": "VHI", "value": "VHI"}],
                    "variable_name": 'index',
                    "action_id": "update_data"},
                    {"input_type": 'slider',
                        "label": 'Year',
                        "min": 1981,
                        "max": 2015,
                        "value": 1981,
                        "variable_name": 'year',
                        "action_id": 'update_data'},
                    {"input_type": "text",
                        "variable_name": "weeks",
                        "label": "Weeks",
                        "value": 20,
                        "action_id": "update_data"}]

    controls = [{"control_type": "hidden",
                    "label": "get historical stock prices",
                    "control_id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"output_type": "plot",
                    "output_id": "plot",
                    "control_id": "update_data",
                    "tab": "Plot",
                    "on_page_load": True},
                {"output_type": "table",
                    "output_id": "table_id",
                    "control_id": "update_data",
                    "tab": "Table",
                    "on_page_load": True}]

    def getData(self, params):
        df = pd.read_csv(os.path.join("data", [x for x in os.listdir('data') if "_{}_".format(params["region"]) in x][0]))
        year_vhi = zip(df["year"], df["week"], df[params["index"]])
        year_d = dict()
        index_v = params["index"]
        for e in year_vhi:
            if not e[0] or e[-1] < 0:
                continue
            if e[0] in year_d:
                year_d[e[0]].append([e[1], e[-1]])
            else:
                year_d[e[0]] = [[e[1], e[-1]]]
        year_d = dict((k, v) for k, v in year_d.items() if k >= int(params["year"]))
        dft = {index_v: [], "week": [], "year": []}
        itera = 0
        for e in year_d:
            for x in year_d[e]:
                if itera == int(params["weeks"]):
                    break
                dft[index_v].append(x[-1])
                dft["week"].append(x[0])
                dft["year"].append(e)
                itera += 1
        return pd.DataFrame.from_dict(dft)

    def getPlot(self, params):
        df = self.getData(params)
        df['new_week'] = pd.Series(list(range(len(df["week"]))))
        plt_obj = df.plot(y=params["index"], x="new_week")
        plt_obj.set_title("graph")
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=9080)
