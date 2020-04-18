import flask
from flask import jsonify
from datetime import datetime
import pandas as pd
import json
import requests
from statsmodels.tsa.arima_model import ARMA, ARIMA


app = flask.Flask(__name__)




api_url_base = 'http://smartenvirontment.online/webapi/'

headers = {'Content-Type': 'application/json'}


def get_ispu_info(kecamatan):
    now = datetime.now()
    tanggal = now.strftime("%Y-%m-%d")

    api_url = '{0}ispu/wilayah?kecamatan={2}&tanggal=2020-03-01;{1}'.format(api_url_base, tanggal,kecamatan)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def ramal(listnya):

    # fit model
    model = ARMA(listnya, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(listnya), len(listnya))
    print(yhat)

    return yhat


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/forecast/<kecamatan>', methods=['GET'])
def api_all(kecamatan):
    ispu_info = get_ispu_info(kecamatan)

    pm10 = []
    co = []
    no2 = []
    so2 = []
    o3 = []

    if ispu_info is not None:
        print("Here's your info: ")
        for i in range(len(ispu_info['detail_ispu'])):
            data_pm10 = [float(ispu_info['detail_ispu'][i]['pm10'])]
            pm10.append(data_pm10)
            data_co = [float(ispu_info['detail_ispu'][i]['co'])]
            co.append(data_co)
            data_no2 = [float(ispu_info['detail_ispu'][i]['no2'])]
            no2.append(data_no2)
            data_so2 = [float(ispu_info['detail_ispu'][i]['so2'])]
            so2.append(data_so2)
            data_o3 = [float(ispu_info['detail_ispu'][i]['o3'])]
            o3.append(data_o3)

        df_pm10 = pd.DataFrame(pm10)
        pm10_series = (df_pm10 != 0).any(axis=1)
        new_df = df_pm10.loc[pm10_series]

        clean_pm10 = new_df.values.tolist()
        print(clean_pm10)

        df_co = pd.DataFrame(co)
        co_series = (df_co != 0).any(axis=1)
        new_df = df_co.loc[co_series]

        clean_co = new_df.values.tolist()
        print(clean_co)

        df_no2 = pd.DataFrame(no2)
        no2_series = (df_no2 != 0).any(axis=1)
        new_df = df_no2.loc[no2_series]

        clean_no2 = new_df.values.tolist()
        print(clean_no2)

        df_so2 = pd.DataFrame(so2)
        so2_series = (df_so2 != 0).any(axis=1)
        new_df = df_so2.loc[so2_series]

        clean_so2 = new_df.values.tolist()
        print(clean_so2)

        df_o3 = pd.DataFrame(o3)
        o3_series = (df_o3 != 0).any(axis=1)
        new_df = df_o3.loc[o3_series]

        clean_o3 = new_df.values.tolist()
        if(len(clean_o3)<7):
            imputasi = [[0.0012114894706711], [0.00097603240734926],[ 0.0012114894706711], [0.00097603240734926],
                        [0.0012114894706711], [0.00097603240734926], [0.0012114894706711],[0.0012114894706711], [0.00097603240734926],[ 0.0012114894706711], [0.00097603240734926],
                        [0.0012114894706711], [0.00097603240734926], [0.0012114894706711],[0.0012114894706711], [0.00097603240734926],[ 0.0012114894706711], [0.00097603240734926],
                        [0.0012114894706711], [0.00097603240734926], [0.0012114894706711],[0.0012114894706711], [0.00097603240734926],[ 0.0012114894706711], [0.00097603240734926],
                        [0.0012114894706711], [0.00097603240734926], [0.0012114894706711], [0.00097603240734926], [0.0012114894706711]]
            for z in range (30-len(clean_o3)):
                clean_o3.append(imputasi[z])

        print(clean_o3)

        print("Here's your forecasting pm10 MA: ")
        fut_pm10=ramal(clean_pm10)
        print(fut_pm10)

        print("Here's your forecasting co MA: ")
        fut_co = ramal(clean_co)
        print(fut_co)

        print("Here's your forecasting no2 MA: ")
        fut_no2 = ramal(clean_no2)
        print(fut_no2)

        print("Here's your forecasting so2 MA: ")
        fut_so2 = ramal(clean_so2)
        print(fut_so2)

        print("Here's your forecasting o3 MA: ")
        fut_o3 = ramal(clean_o3)
        print(fut_o3)

        ispu_forecast = [
            {'tanggal': "2020-04-01",
             'kecamatan':kecamatan,
             'pm10': fut_pm10[0],
             'o3': fut_o3[0],
             'co': fut_co[0],
             'no2': fut_no2[0],
             'so2': fut_so2[0]
             }
        ]

        return jsonify(ispu_forecast), 200

    else:
        print('[!] Request Failed')


if __name__ == '__main__':
    app.run()