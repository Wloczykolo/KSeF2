#!/usr/bin/env python
# coding: utf-8

import os
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st

def extract_podmiot1_data(xml_file, namespace):
    """
    Extract data from Podmiot1 node
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        podmiot1 = root.find('ns:Podmiot1', namespace)
        if podmiot1 is None:
            return None
        Fa = root.find('ns:Fa', namespace)
        if Fa is None:
            return None

        data = {
            'P_2': Fa.find('ns:P_2', namespace).text if Fa.find('ns:P_2', namespace) is not None else None,
            'PrefiksPodatnika': podmiot1.find('ns:PrefiksPodatnika', namespace).text if \
                podmiot1.find('ns:PrefiksPodatnika', namespace) is not None else None,
            'NrEORI': podmiot1.find('ns:NrEORI', namespace).text if \
                podmiot1.find('ns:NrEORI', namespace) is not None else None,
            'NIP': podmiot1.find('ns:DaneIdentyfikacyjne/ns:NIP', namespace).text if \
                podmiot1.find('ns:DaneIdentyfikacyjne/ns:NIP', namespace) is not None else None,
            'Nazwa': podmiot1.find('ns:DaneIdentyfikacyjne/ns:Nazwa', namespace).text if \
                podmiot1.find('ns:DaneIdentyfikacyjne/ns:Nazwa', namespace) is not None else None,
            'Adres_KodKraju': podmiot1.find('ns:Adres/ns:KodKraju', namespace).text if \
                podmiot1.find('ns:Adres/ns:KodKraju', namespace) is not None else None,
            'Adres_AdresL1': podmiot1.find('ns:Adres/ns:AdresL1', namespace).text if \
                podmiot1.find('ns:Adres/ns:AdresL1', namespace) is not None else None,
            'Adres_AdresL2': podmiot1.find('ns:Adres/ns:AdresL2', namespace).text if \
                podmiot1.find('ns:Adres/ns:AdresL2', namespace) is not None else None,
            'Adres_GLN': podmiot1.find('ns:Adres/ns:GLN', namespace).text if \
                podmiot1.find('ns:Adres/ns:GLN', namespace) is not None else None,
            'AdresKoresp_KodKraju': podmiot1.find('ns:AdresKoresp/ns:KodKraju', namespace).text if \
                podmiot1.find('ns:AdresKoresp/ns:KodKraju', namespace) is not None else None,
            'AdresKoresp_AdresL1': podmiot1.find('ns:AdresKoresp/ns:AdresL1', namespace).text if \
                podmiot1.find('ns:AdresKoresp/ns:AdresL1', namespace) is not None else None,
            'AdresKoresp_AdresL2': podmiot1.find('ns:AdresKoresp/ns:AdresL2', namespace).text if \
                podmiot1.find('ns:AdresKoresp/ns:AdresL2', namespace) is not None else None,
            'AdresKoresp_GLN': podmiot1.find('ns:AdresKoresp/ns:GLN', namespace).text if \
                podmiot1.find('ns:AdresKoresp/ns:GLN', namespace) is not None else None,
            'Email': podmiot1.find('ns:DaneKontaktowe/ns:Email', namespace).text if \
                podmiot1.find('ns:DaneKontaktowe/ns:Email', namespace) is not None else None,
            'Telefon': podmiot1.find('ns:DaneKontaktowe/ns:Telefon', namespace).text if \
                podmiot1.find('ns:DaneKontaktowe/ns:Telefon', namespace) is not None else None,
            'StatusInfoPodatnika': podmiot1.find('ns:StatusInfoPodatnika', namespace).text if \
                podmiot1.find('ns:StatusInfoPodatnika', namespace) is not None else None,
        }

        return data

    except ET.ParseError as e:
        st.error(f"Error parsing {xml_file}: {e}")
        return None

# Streamlit interface
st.title('Parser e-faktur')

uploaded_files = st.file_uploader("Upload XML files", accept_multiple_files=True, type='xml')

if uploaded_files:
    namespace = {'ns': 'http://crd.gov.pl/wzor/2023/06/29/12648/'}
    
    all_data = []

    for uploaded_file in uploaded_files:
        with st.spinner(f'Processing {uploaded_file.name}...'):
            data = extract_podmiot1_data(uploaded_file, namespace)
            if data:
                all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        st.write(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download data as CSV", data=csv, file_name='podmiot1_data.csv', mime='text/csv')
    else:
        st.warning("No data found")

st.write("Adjust the code to process Podmiot2, DaneOgolne, and FaWiersz in a similar manner.")
