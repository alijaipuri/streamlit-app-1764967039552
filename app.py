import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='Currency Converter', page_icon='💸')

st.title('💰 Currency Converter')
st.markdown('Convert between USD, EUR, GBP, and INR with real-time exchange rates')

# Function to get exchange rates
def get_exchange_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        return data['rates']
    except requests.exceptions.RequestException as e:
        st.error('Failed to retrieve exchange rates')
        return None

# Get exchange rates
exchange_rates = get_exchange_rates()

# Check if exchange rates are available
if exchange_rates is not None:
    # Create a DataFrame for the exchange rates
    exchange_rate_df = pd.DataFrame({
        'Currency': ['EUR', 'GBP', 'INR'],
        'Exchange Rate': [exchange_rates['EUR'], exchange_rates['GBP'], exchange_rates['INR']]
    })

    # Display exchange rates
    with st.expander('Exchange Rates'):
        st.write(exchange_rate_df)

    # Create a form for the conversion
    with st.form('conversion_form'):
        st.header('Conversion Form')
        amount = st.number_input('Amount', min_value=0.0)
        from_currency = st.selectbox('From', ['USD', 'EUR', 'GBP', 'INR'])
        to_currency = st.selectbox('To', ['USD', 'EUR', 'GBP', 'INR'])
        submit_button = st.form_submit_button('Convert')

    # Convert the currency
    if submit_button:
        if from_currency == to_currency:
            st.info('Source and destination currencies are the same')
        else:
            try:
                # Convert from USD to the destination currency
                if from_currency == 'USD':
                    if to_currency == 'EUR':
                        result = amount * exchange_rates['EUR']
                    elif to_currency == 'GBP':
                        result = amount * exchange_rates['GBP']
                    elif to_currency == 'INR':
                        result = amount * exchange_rates['INR']
                    else:
                        result = amount

                # Convert from EUR to the destination currency
                elif from_currency == 'EUR':
                    if to_currency == 'USD':
                        result = amount / exchange_rates['EUR']
                    elif to_currency == 'GBP':
                        result = amount * exchange_rates['GBP'] / exchange_rates['EUR']
                    elif to_currency == 'INR':
                        result = amount * exchange_rates['INR'] / exchange_rates['EUR']
                    else:
                        result = amount

                # Convert from GBP to the destination currency
                elif from_currency == 'GBP':
                    if to_currency == 'USD':
                        result = amount / exchange_rates['GBP']
                    elif to_currency == 'EUR':
                        result = amount * exchange_rates['EUR'] / exchange_rates['GBP']
                    elif to_currency == 'INR':
                        result = amount * exchange_rates['INR'] / exchange_rates['GBP']
                    else:
                        result = amount

                # Convert from INR to the destination currency
                elif from_currency == 'INR':
                    if to_currency == 'USD':
                        result = amount / exchange_rates['INR']
                    elif to_currency == 'EUR':
                        result = amount * exchange_rates['EUR'] / exchange_rates['INR']
                    elif to_currency == 'GBP':
                        result = amount * exchange_rates['GBP'] / exchange_rates['INR']
                    else:
                        result = amount

                st.success(f'{amount} {from_currency} is equal to {result:.2f} {to_currency}')
            except Exception as e:
                st.error('Failed to perform conversion')
else:
    st.error('Failed to retrieve exchange rates')