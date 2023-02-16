import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit.config as config
from parserNbpAPI import CurrentExchangeRates, CurrencyConverter, CurrencyLastRates
 
class StreamlitPageUI():

    def __init__(self) -> None:

        st.set_page_config(
            page_title = 'Remitly currency converter',
            page_icon="🏦",
            layout = "centered"
        )

        # Hide Streamlit menu and footer
        hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        # Disable CORS and other Streamlit settings
        config.set_option('server.enableCORS', False)
        config.set_option('global.developmentMode', False)
        config.set_option('server.useWebsocketCompression', False)

        st.markdown("<h1 style='text-align: center;'>Remitly currency converter</h1>", unsafe_allow_html=True)

        image = self.load_lottieurl()
        st_lottie(image, width=None, height=400, key="ImageIllustration")

        st.markdown("<h2 style='text-align: center;'>Where would you like to send money?</h2>", unsafe_allow_html=True)

    
    def load_lottieurl(self):
        getImage = requests.get('https://assets7.lottiefiles.com/packages/lf20_2AFtKRR44D.json')
        if getImage.status_code != 200:
            return None
        
        return getImage.json()


class RemitlyCurrencyConverter(CurrentExchangeRates):
    
    def __init__(self) -> None:
        with st.form("You send"):

            self.amount = st.number_input("Enter amount to convert:", min_value = .25, step = .25)
            self.select_box1, self.select_box2 = st.columns(2)
            self.select_box1.selectbox('You send', currency_codes, key='send')
            self.select_box2.selectbox('They receive', ['PLN'], key = 'receive')

            self.submitted = st.form_submit_button("Send now")

            self.press_buttons_test()

    def currency_converter(self, amount, from_currency, to_currency):
        
        self.amount  = amount
        self.currency  = from_currency
    
        self.converter = CurrencyConverter(self.currency)
        return round(self.converter.getCurrencyToPLN() * self.amount, 2)

    def calculate_percentage(self,code):
        
        currency_data = CurrencyLastRates(code, days=30)
        curenncy_df = currency_data.getCurrencyData()

        curenncy_df.sort_values(by = 'effectiveDate', inplace=True, ascending=False)
        curenncy_df.reset_index(drop=True, inplace=True)

        self.percentage_diff = round((curenncy_df.iloc[0]['mid'] - curenncy_df.iloc[-1]['mid'])/ curenncy_df.iloc[-1]['mid'] * 100,2)
        return str(self.percentage_diff) + ' %'

    def display_graph(self):

        plot = CurrencyLastRates(st.session_state['send'], days=30)
        plot_line_graph = plot.historicalExchangeRates()

        plot_line_graph.update_layout(
            width=675,
            height=450,
            margin=dict(l=20, r=20, t=20, b=20),    
        )

        st.plotly_chart(plot_line_graph)

    def press_buttons_test(self):

        if self.submitted:
            self.result = self.currency_converter(self.amount, st.session_state['send'], st.session_state['receive'])
            self.rounded_result = round(self.result)
            st.write(f"1 {st.session_state['send']} = {round(self.result/self.amount,2)} {(st.session_state['receive'])}")
            st.success(f"{round(self.amount,2)} {st.session_state['send']} is equal to { self.rounded_result} {st.session_state['receive']} 🇵🇱")

            st.metric(
                label = f'The value of the **{self.converter.getCurrencyName().capitalize()}** changed over the last 30 days to PLN:', 
                value=f'{round(self.result/self.amount,2)} PLN', 
                delta=self.calculate_percentage(st.session_state['send'])
            )

            st.markdown("<h2 style='text-align: center;'>Analysis of the currency trends over the past 30 days</h2>", unsafe_allow_html=True)

            self.display_graph()


t = StreamlitPageUI()

all_data_rates = CurrentExchangeRates()
currency_names = all_data_rates.getCurrencyNames()
currency_codes = all_data_rates.getCurrencyCodes()

t2 = RemitlyCurrencyConverter()


    