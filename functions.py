# %%

import streamlit as st
import requests
from requests.exceptions import HTTPError, Timeout
import logging
from dotenv import load_dotenv
import os
import pandas as pd
from requests.exceptions import Timeout,RequestException
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import re
import plotly.express as px
from google import genai
from streamlit_searchbox import st_searchbox

# %%

def temp_convertor(temp:str, temperature_convert:str, value:int)-> int:
    
    match (temp,temperature_convert):
        case ('Celsius','Fahereiunt'):
            result = value * 1.8 + 32
            return result
        
        case ('Celsius','Kelvin'):
            result = value +273.15
            return result

        case ('Fahereiunt','Celsius'):
            result = (value - 32 )/1.8
            return result

        case ('Fahereiunt','Kelvin'):
            result = (value - 32 )*5/9+273.15
            return result

        case ('Kelvin','Celsius'):
            result = value - 273.15
            return result

        case ('Kelvin','Fahereiunt'):
            result = (value - 273.15)*1.8+ 32
            return result

        case _: 
            return None

# %%
def get_lo_la(city:str,iso_country):
    ##This function returns long and latitude of city type on input
    load_dotenv()

    api_url = os.getenv('API_URL_GEO')
    api_key = os.getenv('OPENWEATHER_API_KEY')
    params = {
        "q": {city,iso_country},
        "appid": api_key

    }

    if not api_url or not api_key:
        raise ValueError("API_URL_GEO ou OPENWEATHER_API_KEY não definidos")
    
    logging.info(f"Parâmetros enviados para a API: {params}")

    try:
        
        response = requests.get(api_url,params=params,timeout=5)
        response.raise_for_status()
        data = response.json()
        return data

    except Timeout:
        logging.warning('Timeout')
        return None


    except RequestException as e:
        logging.error(f"Erro na requisição para {city}: {e}")
        return None






    
    # try:
    #     response = requests.get(api_url,params=params,timeout=5)
    #     response.raise_for_status()
    #     data = response.json()
    #     logging.info(f"Dados recebidos para {city}")

    

    # except Timeout:
    #     logging.warning(f"Timeout na requisição para {city}")


# %%
def get_weather(lat:int,lo:int) -> int:
    ##This function returns long and latitude of city type on input
    load_dotenv()

    api_url = os.getenv('API_URL_WEATHER')
    api_key = os.getenv('OPENWEATHER_API_KEY')
    params = {
        "lat": lat,
        'lon': lo,
        "appid": api_key,
        'units':'metric'

    }

    if not api_url or not api_key:
        raise ValueError("API_URL_WEATHER ou OPENWEATHER_API_KEY não definidos")
    
    logging.info(f"Parâmetros enviados para a API: {params}")

    try:
        
        response = requests.get(api_url,params=params,timeout=5)
        response.raise_for_status()
        data = response.json()
        return data

    except Timeout:
        logging.warning('Timeout')
        return None


    except RequestException as e:
        logging.error(f"Erro na requisição para {lat} e {lo} : {e}")
        return None


# %%
@st.cache_data
def carregar_dados_locais():
    # O Pandas já abre o arquivo direto, não precisa do 'with open'
    return pd.read_csv('worldcities.csv')

# %%

def sugestion_cities(query:str,df:pd.DataFrame)-> pd.DataFrame:
    ##Function to sugestion a city to user.
    ## Need pandas to work

    if not query or not query.strip():
        return pd.DataFrame()
    
    if query:
    # 1. Filtramos o DataFrame completo
        mask = df['city'].str.contains(query, case=False, na=False)
        df_filtrado = df[mask].head(5) # Pegamos os 5 primeiros resultados completos
        return df_filtrado
    

def buttons_cities_sugestion () -> None:
    if 'df_filtrado' in st.session_state:
        if not st.session_state['df_filtrado'].empty:

            # Criando o grid de blocos (5 colunas)
            cols = st.columns(5)
        else:
            st.empty()

        for i, (index, row) in enumerate(st.session_state['df_filtrado'].iterrows()):
            cidade = row['city']
            pais = row['country']
            
            with cols[i %5]:
                # Criando o texto do botão combinando Nome e País
                label_botao = f"{cidade}, {pais}"
                
                if st.button(label_botao, key=f"btn_{index}", use_container_width=True):
                    # Salvamos a seleção (pode salvar só o nome ou o dicionário todo)
                    st.session_state["city_country_selected"] = f"{cidade}, {pais}"
                    st.rerun()
                    

    else:
        st.empty()
        # for i, cidade in enumerate(resultados):
        #     with cols[i %5]:
        #         # Adicionamos o índice {i} para garantir que a key seja ÚNICA
        #         if st.button(cidade, key=f"btn_{cidade}_{i}", use_container_width=True):
        #             st.session_state["city_selected"] = cidade 
        #             st.rerun()


        # 2. Iteramos pelas linhas do DataFrame filtrado
  

# %%

def get_city() -> list[str]:

    if st.session_state['city_country_selected'] != 'Please select a city':
        cidade = st.session_state['city_country_selected']
        try:
            if st.session_state['city_country_selected'] is not None:
                city,country = str.split(cidade,',')
                lista = []
                lista.append(city)
                lista.append(country)
                return lista
        except:
                lista = []
                lista.append('São Paulo')
                lista.append('Brazil')
                st.session_state['city_country_selected'] = 'São Paulo, Brazil'
                return lista
        
# %%

def init_states() -> None:
    ## Function to iniate states for avoid key erros in refresh page
    defaults = {
        "sugestions_cities": "",
        "city_country_selected": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# %%


def data_hour_tratment(Timestamp:str) -> list:
    regex = r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})'
    m = re.search(regex, Timestamp)

    if m:
        data = f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
        hora = f"{m.group(4)}:{m.group(5)}"
        return [data,hora]

# %%



def conversor_hour_date(time:int,Zone:str) -> str:
    dt_utc = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=time)
    dt_sp = str(dt_utc.astimezone(ZoneInfo(Zone)))
    hour_clean = data_hour_tratment(dt_sp)

    return hour_clean
# %%


def get_icon(codigo_api):
    """
    Mapeia os códigos oficiais da OpenWeatherMap para Emojis modernos.
    """
    icones = {
        "01d": "☀️", # Dia limpo
        "01n": "🌙", # Noite limpa
        "02d": "🌤️", # Poucas nuvens (dia)
        "02n": "☁️", # Poucas nuvens (noite)
        "03d": "⛅", # Nuvens dispersas
        "03n": "☁️", # Nuvens dispersas (noite)
        "04d": "☁️", # Nublado
        "04n": "☁️", # Nublado
        "09d": "🌧️", # Chuva rápida
        "09n": "🌧️", # Chuva rápida
        "10d": "🌦️", # Chuva com sol
        "10n": "🌧️", # Chuva (noite)
        "11d": "⛈️", # Tempestade
        "11n": "⛈️", # Tempestade
        "13d": "❄️", # Neve
        "13n": "❄️", # Neve
        "50d": "🌫️", # Neblina
        "50n": "🌫️"  # Neblina
    }
    
    # Se por acaso a API mandar um código novo, retorna um ícone genérico de planeta
    return icones.get(codigo_api, "🌍")



# %%


def get_alerts(dados_clima: dict) -> list:
    """
    Busca os alertas na API e retorna no máximo 2 descrições 
    em formato de lista de strings.
    """
    lista_descricoes = []
    
    if 'alerts' in dados_clima and dados_clima['alerts']:
    
        # O fatiamento [:2] garante que pegaremos apenas os 2 primeiros alertas
        for alerta in dados_clima['alerts'][:2]:
            
            descricao = alerta.get('description','Alerta meteorológico sem descrição detalhada.')
            
            lista_descricoes.append(descricao)



            
    return lista_descricoes



# %%

def get_hourly(dados_clima: dict) -> pd.DataFrame:
    """
    Busca um forecast de 6 horas para frente
    """
    if 'hourly' in dados_clima and dados_clima['hourly']:
        lista_clima_unix= []


    for ponto in dados_clima['hourly'][0:20]:
        
        hour = conversor_hour_date(ponto.get('dt'),dados_clima['timezone'])
        temp = round(ponto.get('temp'),0)
        caldo = [hour[0],hour[1],temp]

        
        
        lista_clima_unix.append(caldo)
        df_clima = pd.DataFrame(lista_clima_unix)
        df_clima  = df_clima.rename(columns={0:'data',1:'hour',2:'temp'})


    return df_clima



# %%


def get_current_infos(dados:dict) -> dict:

    dici = dict()

    try:
        
        cur_temp = round(dados['current'].get('temp'))
        cur_feels = round(dados['current'].get('feels_like'))
        cur_press = dados['current'].get('pressure')
        cur_humidity = (dados['current'].get('humidity'))
        cur_wind = round(dados['current'].get('wind_speed'))
        cur_vis = dados['current'].get('visibility')

        dici = {'temp':cur_temp,
                'feels':cur_feels,
                'press':cur_press,
                'humidity':cur_humidity,
                'wind':cur_wind,
                'vis':cur_vis
            }   
        
        return dici



    except:
        st.error('Error, need check')

        



# %%
def llm_gemini(cidade, temp, condicao):
    
    client = genai.Client()
    prompt = (f"""
            O clima em {cidade} agora é de {temp}°C com {condicao}.
            Dê uma sugestão de vestuário ou atividade de apenas 1 frase curta e amigável.
            """)
    

    response = client.models.generate_content(
        model="Gemini 2.5 Flash", contents=prompt
    )
    return (response.text)


# %%

def get_daily(dados_clima: dict) -> pd.DataFrame:
    """
    Busca um forecast de 20 dias para frente
    """
    if 'daily' in dados_clima and dados_clima['daily']:
        lista_clima_unix= []


    for ponto in dados_clima['daily'][0:20]:
        hour = conversor_hour_date(ponto.get('dt'),dados_clima['timezone'])
        temp = round(ponto['temp'].get('day'),0)
        caldo = [hour[0],hour[1],temp]

        
        lista_clima_unix.append(caldo)
        df_dias = pd.DataFrame(lista_clima_unix)
        df_dias  = df_dias.rename(columns={0:'data',1:'hour',2:'temp'})


    return df_dias


# %%
def get_country_iso(df, country_name='Brazil', iso_type="iso3"):
    """
    Busca o código ISO com base no nome do país.
    
    :param df: O DataFrame contendo os dados das cidades.
    :param country_name: Nome do país (ex: 'France', 'Brazil').
    :param iso_type: 'iso2' ou 'iso3' (padrão 'iso2').
    :return: O código ISO encontrado ou None.
    """
    # Filtra onde o país bate com o nome (usando case=False para ignorar maiúsculas/minúsculas)
    result = df[df['country'].str.contains(country_name, case=False, na=False)]
    
    if not result.empty:
        # Pega o primeiro registro encontrado e extrai o ISO correspondente
        return result.iloc[0][iso_type]
    
    return None