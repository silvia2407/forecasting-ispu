import json
import requests
from datetime import datetime
import pandas as pd
from statsmodels.tsa.arima_model import ARMA, ARIMA

api_url_base = 'http://smartenvirontment.online/webapi/'

headers = {'Content-Type': 'application/json'}

def get_ispu_info():
    now = datetime.now()
    tanggal=now.strftime("%Y-%m-%d")

    api_url = '{0}ispu/wilayah?kecamatan=3273230&tanggal=2020-03-01;{1}'.format(api_url_base, tanggal)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

ispu_info = get_ispu_info()


pm10=[]
co=[]
no2=[]
so2=[]
o3=[]

if ispu_info is not None:
    print("Here's your info: ")
    for i in range(len(ispu_info['detail_ispu'])):
        data_pm10=[float(ispu_info['detail_ispu'][i]['pm10'])]
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

    clean_pm10=new_df.values.tolist()
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
    print(clean_o3)

    print("Here's your forecasting pm10 ARMA: ")
    # fit model
    model = ARMA(clean_pm10, order=(2, 1))
    print(model)
    model_fit = model.fit(disp=False)
    print(model_fit)
    # make prediction
    yhat = model_fit.predict(len(clean_pm10), len(clean_pm10))
    print(yhat)

    print("Here's your forecasting pm10 MA: ")
    # fit model
    model = ARMA(clean_pm10, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(clean_pm10), len(clean_pm10))
    print(yhat)

    print("Here's your forecasting pm10 ARIMA: ")
    model = ARIMA(clean_pm10, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(clean_pm10), len(clean_pm10), typ='levels')
    print(yhat)

else:
    print('[!] Request Failed')

