import requests # wykonywania zapytań HTTP
import pandas as pd # przetwarzania danych
import plotly.express as px # do tworzenia wykresów

class CurrencyConverter():
    ''''Przeliczanie aktualnej ceny waluty na złotówki,
    przyjmuje kod waluty jako argument i korzysta z NBP  API do pobrania informacji o 
    kursie waluty w formacie JSON'''
    
    def __init__(self, code) -> None:
        self.code = code # trzyliterowy kod waluty 
        self.url = f'http://api.nbp.pl/api/exchangerates/rates/a/{self.code}/?format=json' 

        self.request = requests.get(self.url)
    
        try:
            self.currencyInfo = self.request.json() # pobieranie kursów walut w formacie json
        except Exception as ex: 
            print(f'Niestety nie można znaleźć danego kursu {self.code.upper()} dla PLN: {ex}')

    def getCurrencyToPLN(self) -> float:
        return self.currencyInfo['rates'][0]['mid'] # wyciągnięcie aktualnej ceny

    def getCurrencyName(self) -> str:
        return self.currencyInfo['currency'] # odczytanie nazwy waluty

class CurrentExchangeRates():

    '''Umożliwia użytkownikom pobranie listy nazw i kodów 
    wszystkich walut dostępnych w API NBP.'''

    def __init__(self) -> None:
        self.url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
        request = requests.get(self.url)

        try:
            self.data = request.json()        
        except Exception as ex:  # w przypadku braku połączenia z API wyświetlam informację o błędzie.
            print(f'Niestety nie można znaleźć aktualnych kursow')

    def getCurrencyNames(self):
        '''Zwraca listę nazw walut dostępnych w API NBP, nazwy walut są zwracane z pierwszą literą dużą'''
        self.currencies = []

        for currency in self.data[0]['rates']:
            names = currency['currency'].capitalize()
            self.currencies.append(names)

        return self.currencies

    def getCurrencyCodes(self):
        '''Zwraca listę kodów walut dostępnych w API NBP'''
        self.codes = []

        for currency in self.data[0]['rates']:
            code = currency['code']
            self.codes.append(code)

        return self.codes

    def getAllInfo(self):
        return self.data


class CurrencyLastRates():
    '''Umożliwia użytkownikom pobranie informacji o kursach wybranej waluty w określonym okresie czasu,
     przyjmuje kod waluty oraz liczbę dni, dla których użytkownik chce pobrać informacje o kursach'''

    def __init__(self, code, days=30) -> None:
        self.code = code # trzyliterowy kod waluty 
        self.days = days # ile ostatnich dni chcesz uwzględnić w informacjach o kursach wybranej waluty, default - 30, max - 255

        self.url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{days}/?format=json'

        self.request = requests.get(self.url)
    
        try:
            self.currencyData = self.request.json()
            self.currencyDataFrame = pd.DataFrame(self.currencyData['rates'])
            self.currencyDataFrame.drop(columns='no', inplace=True)
        except Exception as ex: 
            print(f'Niestety nie można znaleźć danego kursu {self.code.upper()} dla PLN: {ex}')

    def getCurrencyData(self):
        '''Zwraca DataFrame z kursami waluty w danym przedziale czasowym.'''

        self.currencyDataFrame = pd.DataFrame(self.currencyData['rates'])
        self.currencyDataFrame.drop(columns='no', inplace=True)
        return self.currencyDataFrame
    
    def historicalExchangeRates(self):
        '''Tworzy wykres liniowy przedstawiający zmiany kursu waluty w czasie.'''

        currencyName = self.currencyData['currency']  # wyciąganie nazwy waluty z JSON
        currencyCode = self.currencyData['code']  # wyciąganie kodu waluty z JSON

        plotCurrencyRates = px.line(x=self.currencyDataFrame['effectiveDate'], 
            y=self.currencyDataFrame['mid'], 
            labels={'x': 'Data', 'y': f'Exchange Rates ({currencyCode})'}, 
            title=f'Kursy waluty {currencyName.capitalize()} w czasie'
        )

        return plotCurrencyRates



