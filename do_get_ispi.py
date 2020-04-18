import json
import requests
import pandas as pd
from statsmodels.tsa.arima_model import ARMA, ARIMA

api_url_base = 'http://smartenvirontment.online/webapi/'

headers = {'Content-Type': 'application/json'}

def get_ispu_info():

    api_url = '{0}ispu/wilayah?kecamatan=3273230&tanggal=2020-03-01;2020-03-21'.format(api_url_base)

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
        data_pm10=[ispu_info['detail_ispu'][i]['tanggal'],float(ispu_info['detail_ispu'][i]['pm10'])]
        pm10.append(data_pm10)
        data_co = [ispu_info['detail_ispu'][i]['tanggal'], float(ispu_info['detail_ispu'][i]['co'])]
        co.append(data_co)
        data_no2 = [ispu_info['detail_ispu'][i]['tanggal'], float(ispu_info['detail_ispu'][i]['no2'])]
        no2.append(data_no2)
        data_so2 = [ispu_info['detail_ispu'][i]['tanggal'], float(ispu_info['detail_ispu'][i]['so2'])]
        so2.append(data_so2)
        data_o3 = [ispu_info['detail_ispu'][i]['tanggal'], float(ispu_info['detail_ispu'][i]['o3'])]
        o3.append(data_o3)

else:
    print('[!] Request Failed')

print("Here's your forecasting pm10 ARMA: ")
# fit model
model = ARMA(pm10, order=(2, 1))
print(model)
model_fit = model.fit(disp=False)
print(model_fit)
# make prediction
yhat = model_fit.predict(len(pm10), len(pm10))
print(yhat)

print("Here's your forecasting pm10 MA: ")
# fit model
model = ARMA(pm10, order=(0, 1))
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(pm10), len(pm10))
print(yhat)

print("Here's your forecasting pm10 ARIMA: ")
model = ARIMA(pm10, order=(1, 1, 1))
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(pm10), len(pm10), typ='levels')
print(yhat)