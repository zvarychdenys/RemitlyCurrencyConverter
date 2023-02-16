import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px



class CurrencyConverter():

    def __init__(self, code) -> None:
        self.code = code # trzyliterowy kod waluty (standard ISO 4217)
        self.url = f'http://api.nbp.pl/api/exchangerates/rates/a/{self.code}/?format=json'

        self.request = requests.get(self.url)
    
        try:
            self.currencyInfo = self.request.json()

        except Exception as ex: 
            print(f'Niestety nie można znaleźć danego kursu {self.code.upper()} dla PLN: {ex}')

    
    def getCurrencyToPLN(self) -> float:
        return self.currencyInfo['rates'][0]['mid'] # wyciagam aktualna cene

    def getCurrencyName(self) -> str:
        return self.currencyInfo['currency'] # wyciagam nazwe waluty

class CurrentExchangeRates():

    def __init__(self) -> None:
        self.url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
        request = requests.get(self.url)

        try:
            self.data = request.json()        
        except Exception as ex: 
            print(f'Niestety nie można znaleźć aktualnych kursow')


    def getCurrencyNames(self):
         
        self.currencies = []

        for currency in self.data[0]['rates']:
            names = currency['currency'].capitalize()
            self.currencies.append(names)

        return self.currencies

    def getCurrencyCodes(self):
         
        self.codes = []

        for currency in self.data[0]['rates']:
            code = currency['code']
            self.codes.append(code)

        return self.codes

    def getAllInfo(self):
        return self.data


class CurrencyLastRates():

        def __init__(self, code, days=30) -> None:
            self.code = code # trzyliterowy kod waluty (standard ISO 4217)
            self.days = days # za ile ostatnich dni chcemy wiedziec informacje o walucie. default - 10, max - 255

            self.url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{days}/?format=json'
            #  self.url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{int(days.split(" ")[0])}/?format=json'

            self.request = requests.get(self.url)
        
            try:
                self.currencyData = self.request.json()
                self.currencyDataFrame = pd.DataFrame(self.currencyData['rates'])
                self.currencyDataFrame.drop(columns='no', inplace=True)
            except Exception as ex: 
                print(f'Niestety nie można znaleźć danego kursu {self.code.upper()} dla PLN: {ex}')

        def getCurrencyData(self):
            
            # self.currencyDataFrame = pd.DataFrame(self.currencyData['rates']).set_index('effectiveDate')
            self.currencyDataFrame = pd.DataFrame(self.currencyData['rates'])
            self.currencyDataFrame.drop(columns='no', inplace=True)
            return self.currencyDataFrame 
        
        def historicalExchangeRates(self):
            currencyName = self.currencyData['currency'] # wyciagam imie waluty z json pliku
            currencyCode = self.currencyData['code'] # wyciagam cod waluty z json pliku

            plotCurrencyRates = px.line(x=self.currencyDataFrame['effectiveDate'], 
                y=self.currencyDataFrame['mid'], 
                labels={'x': 'Data', 'y': f'Exchange Rates ({currencyCode})'}, 
                title=f'Kursy waluty {currencyName.capitalize()} w czasie'
            )

            return plotCurrencyRates



