import logging
from urllib.request import urlopen
import streamlit as st

import azure.functions as func
import pandas as pd
from scipy import sparse
from urllib3 import HTTPResponse
import typing
import json

st.write("""
# My Content

An interactive Web app to help people read more by recommending books that they will love.

""")
clicks = pd.read_csv('./clicks_df.csv')

#function that would clean the data
@st.cache

def main(req: func.HttpRequest,recommendation: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not recommendation or len(recommendation()) == 0:
        logging.warning("Recommendation item not found")
        return func.HttpResponse(
            "Recommendation item not found",
            status_code=404,
        )
    req_body = req.get_json()
    
    return func.HttpResponse({req_body.get(
        # recommendation[selected_user].to_json(),
        # json.dumps(recommendation[selected_user]),
        json.dumps(req_body),
        mimetype="application/json",
        status_code=200,
    )})
    
def get_body(self) -> bytes:
        return self.__body_bytes

def get_json(self) -> typing.Any:
        return json.loads(self.__body_bytes.decode('utf-8'))

    

selected_user = st.selectbox( "Type or select a user from the dropdown",('1', '2', '3','4', '5', '11183'))

st.write('You selected User_ID #:', int(selected_user))

user_id = int(selected_user)

if st.button("Get Recommendation"):
    with st.spinner("Analyzing the library …"):
        API_url = "http://localhost:7071/api/recommendation/" + str(user_id)
        with urlopen(API_url) as f:
            API_data = json.loads(f.read())
        st.write(API_data)
