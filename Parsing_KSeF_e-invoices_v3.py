#!/usr/bin/env python
# coding: utf-8

# # Parser e-faktur

# Dnia 1 stycznia 2022 r. weszła w życie nowelizacja ustawy VAT, która wprowadziła tzw. dobrowolne e-fakturowanie w ramach Krajowego Systemu e-Faktur (KSeF).
# 
# Początkowo w tym celu wykorzystywano schemę FA(1), jednak od 1 września 2023 r. wprowadzono schemę FA(2).
# 
# Wielokrotnie też przekładano termin wejścia w życie obowiązkowego KSeF. Zgodnie z bieżącymi zapowiedziami Ministerstwa Finansów ma to nastąpić (przynajmniej dla dużych podatników) w dniu 1 lutego 2026 r. 
# 
# Celem poniższego narzędzia jest wyciąganie z e-faktur, pobranych z systemu KSeF i zgodnych ze schemą FA(2), danych dotyczących sprzedawcy, nabywcy, innych danych podstawowych z faktury, a przede wszystkich danych wierszowych.
# 
# Narzędzie zaciąga treść e-faktur zgromadzonych w folderze: "C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/KSeF_faktury_pobrane" i zapisuje dane z tych faktur w plikach .csv. To w jaki sposób dane z faktur zostaną następnie wykorzystane, zależy w pełni od użytkownika narzędzia. Warto natomiast podkreślić, że upowszechnienie się KSeF z czasem doprowadzi do uproszczenia procesów księgowych w firmach.

# ## Parsowanie węzła Podmiot1

# In[22]:


import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_podmiot1_data(xml_file, namespace):
    """
   Kopiuj dane z węzła Podmiot1
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        podmiot1 = root.find('ns:Podmiot1', namespace)
        if podmiot1 is None:
            return None
        Fa=root.find('ns:Fa', namespace)
        if Fa is None:
            return None

        data = {
            'P_2': Fa.find('ns:P_2', namespace).text \
            if Fa.find('ns:P_2', namespace) is not None else None,
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
        print(f"Error parsing {xml_file}: {e}")
        return None

def process_directory(input_folder, output_csv, namespace):
    """
    Przeprocesuj wszystki pliki xml w danej lokalizacji i zapisz dane w pliku csv.
    """
    all_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)
            #print(f"Processing file: {xml_file_path}")
            data = extract_podmiot1_data(xml_file_path, namespace)
            if data:
                all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"Dane zapisane do {output_csv}")
    else:
        print("Brak danych")

# ścieżki
input_folder = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/KSeF_faktury_pobrane'
output_csv = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/CSV/Podmiot1.csv'

# definicja namespace
namespace = {'ns': 'http://crd.gov.pl/wzor/2023/06/29/12648/'}

# folder wejściowy, plik wyjściowy
process_directory(input_folder, output_csv, namespace)


# ## Węzeł Podmiot2

# In[23]:


import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_podmiot2_data(xml_file, namespace):
    """
    Kopiuj dane z węzła Podmiot2
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        podmiot2 = root.find('ns:Podmiot2', namespace)
        if podmiot2 is None:
            return None
        Fa=root.find('ns:Fa', namespace)
        if Fa is None:
            return None
        data = {
            'P_2': Fa.find('ns:P_2', namespace).text \
            if Fa.find('ns:P_2', namespace) is not None else None,
            'NrEORI': podmiot2.find('ns:NrEORI', namespace).text \
            if podmiot2.find('ns:NrEORI', namespace) is not None else None,
            'NIP': podmiot2.find('ns:DaneIdentyfikacyjne/ns:NIP', namespace).text \
            if podmiot2.find('ns:DaneIdentyfikacyjne/ns:NIP', namespace) is not None else None,
            'KodUE': podmiot2.find('ns:DaneIdentyfikacyjne/ns:KodUE', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:KodUE', namespace) is not None else None,
            'NrVatUE': podmiot2.find('ns:DaneIdentyfikacyjne/ns:NrVatUE', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:NrVatUE', namespace) is not None else None,
            'KodKraju': podmiot2.find('ns:DaneIdentyfikacyjne/ns:KodKraju', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:KodKraju', namespace) is not None else None,
            'NrID': podmiot2.find('ns:DaneIdentyfikacyjne/ns:NrID', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:NrID', namespace) is not None else None,
            'BrakID': podmiot2.find('ns:DaneIdentyfikacyjne/ns:BrakID', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:BrakID', namespace) is not None else None,
            'Nazwa': podmiot2.find('ns:DaneIdentyfikacyjne/ns:Nazwa', namespace).text if \
            podmiot2.find('ns:DaneIdentyfikacyjne/ns:Nazwa', namespace) is not None else None,
            'Adres_KodKraju': podmiot2.find('ns:Adres/ns:KodKraju', namespace).text if \
            podmiot2.find('ns:Adres/ns:KodKraju', namespace) is not None else None,
            'Adres_AdresL1': podmiot2.find('ns:Adres/ns:AdresL1', namespace).text if \
            podmiot2.find('ns:Adres/ns:AdresL1', namespace) is not None else None,
            'Adres_AdresL2': podmiot2.find('ns:Adres/ns:AdresL2', namespace).text if \
            podmiot2.find('ns:Adres/ns:AdresL2', namespace) is not None else None,
            'Adres_GLN': podmiot2.find('ns:Adres/ns:GLN', namespace).text if \
            podmiot2.find('ns:Adres/ns:GLN', namespace) is not None else None,
            'AdresKoresp_KodKraju': podmiot2.find('ns:AdresKoresp/ns:KodKraju', namespace).text if \
            podmiot2.find('ns:AdresKoresp/ns:KodKraju', namespace) is not None else None,
            'AdresKoresp_AdresL1': podmiot2.find('ns:AdresKoresp/ns:AdresL1', namespace).text if \
            podmiot2.find('ns:AdresKoresp/ns:AdresL1', namespace) is not None else None,
            'AdresKoresp_AdresL2': podmiot2.find('ns:AdresKoresp/ns:AdresL2', namespace).text if \
            podmiot2.find('ns:AdresKoresp/ns:AdresL2', namespace) is not None else None,
            'AdresKoresp_GLN': podmiot2.find('ns:AdresKoresp/ns:GLN', namespace).text if \
            podmiot2.find('ns:AdresKoresp/ns:GLN', namespace) is not None else None,
            'Email': podmiot2.find('ns:DaneKontaktowe/ns:Email', namespace).text if \
            podmiot2.find('ns:DaneKontaktowe/ns:Email', namespace) is not None else None,
            'Telefon': podmiot2.find('ns:DaneKontaktowe/ns:Telefon', namespace).text if \
            podmiot2.find('ns:DaneKontaktowe/ns:Telefon', namespace) is not None else None,
            'NrKlienta': podmiot2.find('ns:NrKlienta', namespace).text if \
            podmiot2.find('ns:NrKlienta', namespace) is not None else None,
            'IDNabywcy': podmiot2.find('ns:IDNabywcy', namespace).text if \
            podmiot2.find('ns:IDNabywcy', namespace) is not None else None,
        }

        return data

    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def process_directory(input_folder, output_csv, namespace):
    """
    Przeprocesuj wszystki pliki xml w danej lokalizacji i zapisz dane w pliku csv.
    """
    all_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)
            #print(f"Processing file: {xml_file_path}")
            data = extract_podmiot2_data(xml_file_path, namespace)
            if data:
                all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"Dane zapisane do {output_csv}")
    else:
        print("Brak danych")

# ścieżki
input_folder = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/KSeF_faktury_pobrane'
output_csv = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/CSV/Podmiot2.csv'

# definicja namespace
namespace = {'ns': 'http://crd.gov.pl/wzor/2023/06/29/12648/'}

# folder wejściowy, plik wyjściowy
process_directory(input_folder, output_csv, namespace)


# ## Węzeł DaneOgolne

# In[24]:


import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_fa_data(xml_file, namespace):
    """
    Kopiuj dane z węzła Fa
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        fa = root.find('ns:Fa', namespace)
        if fa is None:
            return None

        adnotacje = fa.find('ns:Adnotacje', namespace)

        data = {
            'KodWaluty': fa.find('ns:KodWaluty', namespace).text if fa.find('ns:KodWaluty', namespace) is not None else None,
            'P_1': fa.find('ns:P_1', namespace).text if fa.find('ns:P_1', namespace) is not None else None,
            'P_1M': fa.find('ns:P_1M', namespace).text if fa.find('ns:P_1M', namespace) is not None else None,
            'P_2': fa.find('ns:P_2', namespace).text if fa.find('ns:P_2', namespace) is not None else None,
            'P_6': fa.find('ns:P_6', namespace).text if fa.find('ns:P_6', namespace) is not None else None,
            'P_6_Od': fa.find('ns:P_6_Od', namespace).text if fa.find('ns:P_6_Od', namespace) is not None else None,
            'P_6_Do': fa.find('ns:P_6_Do', namespace).text if fa.find('ns:P_6_Do', namespace) is not None else None,
            'P_13_1': fa.find('ns:P_13_1', namespace).text if fa.find('ns:P_13_1', namespace) is not None else None,
            'P_14_1': fa.find('ns:P_14_1', namespace).text if fa.find('ns:P_14_1', namespace) is not None else None,
            'P_14_1W': fa.find('ns:P_14_1W', namespace).text if fa.find('ns:P_14_1W', namespace) is not None else None,
            'P_13_2': fa.find('ns:P_13_2', namespace).text if fa.find('ns:P_13_2', namespace) is not None else None,
            'P_14_2': fa.find('ns:P_14_2', namespace).text if fa.find('ns:P_14_2', namespace) is not None else None,
            'P_14_2W': fa.find('ns:P_14_2W', namespace).text if fa.find('ns:P_14_2W', namespace) is not None else None,
            'P_13_3': fa.find('ns:P_13_3', namespace).text if fa.find('ns:P_13_3', namespace) is not None else None,
            'P_14_3': fa.find('ns:P_14_3', namespace).text if fa.find('ns:P_14_3', namespace) is not None else None,
            'P_14_3W': fa.find('ns:P_14_3W', namespace).text if fa.find('ns:P_14_3W', namespace) is not None else None,
            'P_13_4': fa.find('ns:P_13_4', namespace).text if fa.find('ns:P_13_4', namespace) is not None else None,
            'P_14_4': fa.find('ns:P_14_4', namespace).text if fa.find('ns:P_14_4', namespace) is not None else None,
            'P_14_4W': fa.find('ns:P_14_4W', namespace).text if fa.find('ns:P_14_4W', namespace) is not None else None,
            'P_13_5': fa.find('ns:P_13_5', namespace).text if fa.find('ns:P_13_5', namespace) is not None else None,
            'P_14_5': fa.find('ns:P_14_5', namespace).text if fa.find('ns:P_14_5', namespace) is not None else None,
            'P_13_6_1': fa.find('ns:P_13_6_1', namespace).text if fa.find('ns:P_13_6_1', namespace) is not None else None,
            'P_13_6_2': fa.find('ns:P_13_6_2', namespace).text if fa.find('ns:P_13_6_2', namespace) is not None else None,
            'P_13_6_3': fa.find('ns:P_13_6_3', namespace).text if fa.find('ns:P_13_6_3', namespace) is not None else None,
            'P_13_7': fa.find('ns:P_13_7', namespace).text if fa.find('ns:P_13_7', namespace) is not None else None,
            'P_13_8': fa.find('ns:P_13_8', namespace).text if fa.find('ns:P_13_8', namespace) is not None else None,
            'P_13_9': fa.find('ns:P_13_9', namespace).text if fa.find('ns:P_13_9', namespace) is not None else None,
            'P_13_10': fa.find('ns:P_13_10', namespace).text if fa.find('ns:P_13_10', namespace) is not None else None,
            'P_13_11': fa.find('ns:P_13_11', namespace).text if fa.find('ns:P_13_11', namespace) is not None else None,
            'P_15': fa.find('ns:P_15', namespace).text if fa.find('ns:P_15', namespace) is not None else None,
            'KursWalutyZ': fa.find('ns:KursWalutyZ', namespace).text if fa.find('ns:KursWalutyZ', namespace) is not None else None,
            'RodzajFaktury': fa.find('ns:RodzajFaktury', namespace).text if fa.find('ns:RodzajFaktury', namespace) is not None else None,
            'P_16': adnotacje.find('ns:P_16', namespace).text if adnotacje is not None and adnotacje.find('ns:P_16', namespace) is not None else None,
            'P_17': adnotacje.find('ns:P_17', namespace).text if adnotacje is not None and adnotacje.find('ns:P_17', namespace) is not None else None,
            'P_18': adnotacje.find('ns:P_18', namespace).text if adnotacje is not None and adnotacje.find('ns:P_18', namespace) is not None else None,
            'P_18A': adnotacje.find('ns:P_18A', namespace).text if adnotacje is not None and adnotacje.find('ns:P_18A', namespace) is not None else None,
            'P_19': adnotacje.find('ns:Zwolnienie/ns:P_19', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:Zwolnienie/ns:P_19', namespace) is not None else None,
            'P_19A': adnotacje.find('ns:Zwolnienie/ns:P_19A', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:Zwolnienie/ns:P_19A', namespace) is not None else None,
            'P_19B': adnotacje.find('ns:Zwolnienie/ns:P_19B', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:Zwolnienie/ns:P_19B', namespace) is not None else None,
            'P_19C': adnotacje.find('ns:Zwolnienie/ns:P_19C', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:Zwolnienie/ns:P_19C', namespace) is not None else None,
            'P_19N': adnotacje.find('ns:Zwolnienie/ns:P_19N', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:Zwolnienie/ns:P_19N', namespace) is not None else None,
            'P_22': adnotacje.find('ns:NoweSrodkiTransportu/ns:P_22', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:NoweSrodkiTransportu/ns:P_22', namespace) \
            is not None else None,
            'P_42_5': adnotacje.find('ns:NoweSrodkiTransportu/ns:P_42_5', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:P_42_5', namespace) is not None else None,
            'P_22N': adnotacje.find('ns:NoweSrodkiTransportu/ns:P_22N', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:NoweSrodkiTransportu/ns:P_22N', namespace) is not None else None,
            'P_23': adnotacje.find('ns:P_23', namespace).text if adnotacje is not None and adnotacje.find('ns:P_23', namespace) is not None else None,
            'P_PMarzy': adnotacje.find('ns:PMarzy/ns:P_PMarzy', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzy', namespace) is not None else None,
            'P_PMarzy_2': adnotacje.find('ns:PMarzy/ns:P_PMarzy_2', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzy_2', namespace) is not None else None,
            'P_PMarzy_3_1': adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_1', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_1', namespace) is not None else None,
            'P_PMarzy_3_2': adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_2', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_2', namespace) is not None else None,
            'P_PMarzy_3_3': adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_3', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzy_3_3', namespace) is not None else None,
            'P_PMarzyN': adnotacje.find('ns:PMarzy/ns:P_PMarzyN', namespace).text \
            if adnotacje is not None and adnotacje.find('ns:PMarzy/ns:P_PMarzyN', namespace) is not None else None,
            
        }

        return data

    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def process_directory(input_folder, output_csv, namespace):
    """
    Przeprocesuj wszystki pliki xml w danej lokalizacji i zapisz dane w pliku csv.
    """
    all_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)
            fa_data = extract_fa_data(xml_file_path, namespace)
            if fa_data:
                all_data.append(fa_data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"Dane zapisane do {output_csv}")
    else:
        print("Brak danych")

# Ścieżki
input_folder = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/KSeF_faktury_pobrane'
output_csv = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/CSV/DaneOgolne.csv'

# Definicja namespace
namespace = {'ns': 'http://crd.gov.pl/wzor/2023/06/29/12648/'}

# folder wejściowy, plik wyjściowy
process_directory(input_folder, output_csv, namespace)


# ## Węzeł FaWiersz

# In[25]:


import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_dane_wierszowe(xml_file, namespace):
    """
    Kopiuj dane z węzła FaWiersz 
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # pole P_2
        p2_elem = root.find('.//ns:P_2', namespace)
        p2_text = p2_elem.text if p2_elem is not None else None

        # dane_wierszowe
        records = root.findall('.//ns:FaWiersz', namespace)  
        all_data = []

        fields = [
            'NrWierszaFa', 'UU_ID', 'P_6A', 'P_7', 'Indeks', 'GTIN', 'PKWiU', 'CN', 'PKOB', 'P_8A', 'P_8B',
            'P_9A', 'P_9B', 'P_10', 'P_11', 'P_11A', 'P_11Vat', 'P_12', 'P_12_XII', 'P_12_Zal_15', 'KwotaAkcyzy',
            'GTU', 'Procedura', 'KursWaluty', 'StanPrzed'
        ]

        for record in records:
            record_data = {'P_2': p2_text}
            for field in fields:
                elem = record.find(f'.//ns:{field}', namespace)
                field_value = elem.text if elem is not None else None
                record_data[field] = field_value
            all_data.append(record_data)

        return all_data
    
    except ET.ParseError as e:
        print(f"Failed to parse {xml_file}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {xml_file}: {e}")
        return None

def process_directory(input_folder, output_csv, namespace):
    """
    Przeprocesuj wszystki pliki xml w danej lokalizacji i zapisz dane w pliku csv.
    """
    all_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)
            data = extract_dane_wierszowe(xml_file_path, namespace)
            if data:
                all_data.extend(data)

    if all_data:
        df = pd.DataFrame(all_data)
        
        # zastąpienie wartości none
        df = df.fillna('')
        
        # wszystkie dane są traktowane jako tekst
        df = df.astype(str)
        
        df.to_csv(output_csv, index=False)
        print(f"Dane zapisane do {output_csv}")
    else:
        print("Brak danych")

# Ścieżki
input_folder = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/KSeF_faktury_pobrane'
output_csv = 'C:/Users/kamil/Documents/Python/KSeF_element_pierwszy/CSV/DaneWierszowe.csv'

# Definicja namespace
namespace = {'ns': 'http://crd.gov.pl/wzor/2023/06/29/12648/'}

# folder wejściowy, plik wyjściowy
process_directory(input_folder, output_csv, namespace)


# In[ ]:




