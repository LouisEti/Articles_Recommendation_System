import streamlit as st 
import numpy as np 
import requests
import jsonpickle
import logging

# url = 'http://127.0.0.1:5000/recommendation'
# url = 'http://localhost:7071/Rocmmendation_Laptop'
# url = 'http://localhost:7071/recommendation'
url = 'https://recommendation-serverless.azurewebsites.net/recommendation'


user_id_input = st.number_input("Enter a user id", value=0)

response_object={'user_id': user_id_input}

response = requests.post(url, data=response_object)
recommendation = jsonpickle.decode(response.text)

if st.button("Make recommendation"):
    st.write(f'First article recommended : N° {recommendation[0]}')
    st.write(f'Second article recommended : N° {recommendation[1]}')
    st.write(f'Third article recommended : N° {recommendation[2]}')
    st.write(f'Fourth article recommended : N° {recommendation[3]}')
    st.write(f'Fifth article recommended : N° {recommendation[4]}')

