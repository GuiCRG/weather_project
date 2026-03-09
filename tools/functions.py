# %%
import sys
from pathlib import Path
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
from ollama import chat
from ollama import ChatResponse
import json


# %%



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
def get_lo_la(city:str):
    """This function returns long and latitude of city type on input"""
    load_dotenv()

    api_url = st.secrets["API_URL_GEO"]
    api_key = st.secrets["OPENWEATHER_API_KEY"]
    params = {
        "q": {city},
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



# %%
@st.cache_data
def get_weather(lat:int,lo:int) -> int:
    """"API Requisition to get weather"""
    load_dotenv()

    api_url = st.secrets["API_URL_WEATHER"]
    api_key = st.secrets["OPENWEATHER_API_KEY"]
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

    base_dir = Path(__file__).resolve().parents[1]
    json_path = base_dir / "data" / "city.list.json"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["name"])

    return df



# %%

def sugestion_cities(query:str,df:pd.DataFrame)-> pd.DataFrame:
    """Function to sugestion a city to user,using the caracter in input"""

    if not query or not query.strip():
        return pd.DataFrame()
    
    if query:
        mask = df['name'].str.startswith(query, na=False)
        mask = df['name'].str.lower().str.startswith(query.lower(), na=False)
        df_filtrado = df[mask].head(5) # 5 first results
        
        return df_filtrado
    

def buttons_cities_sugestion () -> None:
    """Function to get the city selected to session state"""
    if 'df_filtrado' in st.session_state:
        if not st.session_state['df_filtrado'].empty:


            cols = st.columns(5)
        else:
            st.empty()

        for i, (index, row) in enumerate(st.session_state['df_filtrado'].iterrows()):
            cidade = row['name']
            pais = row['country']
            
            with cols[i %5]:
                label_botao = f"{cidade}, {pais}"
                
                if st.button(label_botao, key=f"btn_{index}", use_container_width=True):
                    # Salvamos a seleção (pode salvar só o nome ou o dicionário todo)
                    st.session_state["city_country_selected"] = f"{cidade}, {pais}"
                    st.rerun()
                    

    else:
        st.empty()

  

# %%

def get_city() -> list[str]:
    """Get a city and country of session state"""
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
    """Function to iniate states for avoid key erros in refresh page"""
    defaults = {
        "sugestions_cities": "",
        "city_country_selected": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# %%


def data_hour_tratment(Timestamp:str) -> list:
    """Function REGEX to tratment timestamp response of API Weather, return date and hour"""
    regex = r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})'
    m = re.search(regex, Timestamp)

    if m:
        data = f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
        hora = f"{m.group(4)}:{m.group(5)}"
        return [data,hora]

# %%



def conversor_hour_date(time:int,Zone:str) -> str:
    """Function to convert date and hour based in timezone and timestamp, use the another function inside this"""
    dt_utc = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=time)
    dt_sp = str(dt_utc.astimezone(ZoneInfo(Zone)))
    hour_clean = data_hour_tratment(dt_sp)

    return hour_clean
# %%


def get_icon(codigo_api):
    """
    Dict to mapping icons code to convert a unicode caracters. 
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
    Seek alerts in API response, limit 2.
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
    Return a 6 hours foward for hour forecast
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
    """Get current infos of the day, like, temperature,feels like
    pressure, humidity, wind and visibity"""

    dici = dict()

    try:
        
        cur_temp = int(dados['current'].get('temp'))
        cur_feels = int(dados['current'].get('feels_like'))
        cur_press = dados['current'].get('pressure')
        cur_humidity = (dados['current'].get('humidity'))
        cur_wind = int(dados['current'].get('wind_speed'))
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

def get_daily(dados_clima: dict) -> pd.DataFrame:
    """
    Seek a 20 day forwards to daily forecast
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

def get_icons_4_daily(dados_clima: dict) -> list:
    """
    Seek icons for chart daily forecast
    """
    # Acessa a lista 'daily'
    lista_diaria = dados_clima.get('daily', [])
    
    icones = []
    # Itera sobre os dias, limitando a 20 (ou o tamanho da lista, o que for menor)
    for dia in lista_diaria[:20]:
        # Acessa o primeiro elemento da lista 'weather' e pega o 'icon'
        icone = dia['weather'][0]['icon']
        icones.append(get_icon(icone))  # Converte o código do ícone para um emoji usando a função get_icon
        
    return icones
# %%


def get_max_min_daily(dados:dict) -> int|int:

    """" Function to return max and min 
        of current day """
    try:
        daily_max = int(dados['daily'][0]['temp']['max'])
        daily_min = int(dados['daily'][0]['temp']['min'])
    except:
        logging.info('Error in get_max_min_daily')

    return daily_min,daily_max




def llm_ollma(city:str,description_weather:str,summary_weather:str,temp)-> str:
    """Function llm, send a prompt with information weather and retunr suggestion or activieties
        using model gemma3:1b(ollama) working local"""

    response: ChatResponse = chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content':f"""Answer directly,just the information,not answer like: 'Okay, here’s a concise response:' or similar, concisely, and informatively. 
                        You have a strict limit of 150 characters. Do not exceed this limit under any circumstances.
                        Sugeestion of clothes or activities for the city {city}, temperature of {temp}, and weather of {description_weather},
                        based on this summary: {summary_weather}""",
    },
    ])

    resposta = response.message.content

    return resposta

