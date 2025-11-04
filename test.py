import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials
# ---------------------------
# GSpread Client from secrets
# ---------------------------
def get_gspread_client():
    try:
        info = st.secrets["gcp_service_account"]["key"]
        info = json.loads(info)
        creds = Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"❌ Error creating GSpread client: {e}")
        st.stop()

# ---------------------------
# Open the form sheet
# ---------------------------
@st.cache_resource
def open_form_sheet(sheet_id):
    client = get_gspread_client()
    try:
        sheet = client.open_by_key(sheet_id).sheet1
        return sheet
    except Exception as e:
        st.error(f"❌ Could not connect to Form Sheet: {e}")
        st.stop()

# ---------------------------
# Test connection
# ---------------------------
SHEET_ID_form = "1wpyHQf51TxG7mUM6MikyGBsz9maN471y1sO03BPOEUo"

sheet = open_form_sheet(SHEET_ID_form)

st.success("✅ Connected to Google Sheet!")
st.write(sheet.get_all_records())  # print all records
