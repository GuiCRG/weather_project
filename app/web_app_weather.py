# %%


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))



# %%
import streamlit as st
from tools.functions import *
from app.layout import site_style
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import re
import plotly.express as px
from ollama import chat
from ollama import ChatResponse
import pandas as pd


## Init layout of the web and sessions states 

try:  ## first try/expect: error geral, error #000, check 

    init_states()
    site_style()

except NameError:
    st.error("Something gonne wrong, don't worry, we working to fix #000 ")

except Exception as e:
    # Registra o erro real no console para você debugar, mas mostra algo amigável
    st.error("Something gonne wrong, don't worry, we working to fix #000 ")
    print(f"Error details: {e}")




try: ## loading dados and creation colunms
    col1top, col2top = st.columns([0.2,0.4],vertical_alignment='center')
    df_cidades = carregar_dados_locais() ## Load of cities data


except NameError:
    st.error("Something gonne wrong, don't worry, we working to fix #001 ")

except Exception as e:
    # Registra o erro real no console para você debugar, mas mostra algo amigável
    st.error("Something gonne wrong, don't worry, we working to fix #001 ")
    print(f"Error details: {e}")
    # st.write(df_cidades) Debbuging 





with col1top:
    city = st.text_input('Insert a city:',placeholder='New York',icon='🔎')
    df_filtrado = sugestion_cities(city,df_cidades)
    st.session_state["df_filtrado"] = df_filtrado
    # st.write(df_filtrado)




try:

    city_country = get_city()

except NameError:
    st.error("Something gonne wrong, don't worry, we working to fix #002 ")

except Exception as e:
    # Registra o erro real no console para você debugar, mas mostra algo amigável
    st.error("Something gonne wrong, don't worry, we working to fix #002 ")
    print(f"Error details: {e}")




lo_la = get_lo_la(city_country[0])
print('loading step 2')

try:
    city_name = lo_la[0]['name']
    country_name = lo_la[0]['country']
    state_code = lo_la[0]['state']


    try: ##Conection to api and response
        dados = get_weather(lo_la[0]['lat'],lo_la[0]['lon'])
        current_info = get_current_infos(dados)
        hour_forecast = get_hourly(dados)
        daily_forecast = get_daily(dados)

    except NameError:
        st.error("Something gonne wrong, don't worry, we working to fix #003 ")

    except Exception as e:
        # Registra o erro real no console para você debugar, mas mostra algo amigável
        st.error("Something gonne wrong, don't worry, we working to fix #003 ")
        print(f"Error details: {e}")



    time = conversor_hour_date(dados['current']['dt'],dados['timezone'])


    emoji_weather = get_icon(dados['current']['weather'][0]['icon'])
    description_weather = dados['current']['weather'][0]['description']
    # st.write(description_weather) Debbuging

    daily_min,daily_max = get_max_min_daily(dados)
    alertas = get_alerts(dados)
    summary_weather = dados['daily'][0]['summary']
    # st.write(summary_weather) Debbuging


    icones_daily = get_icons_4_daily(dados)


    if not 'state' in lo_la[0]:
        state_name = ' '

    else:
        state_name =lo_la[0]['state']

except:
    city_name = ''
    country_name = ''
    state_name = ''
    dt_sp = ''
    time = ['','']
    emoji_weather = ''
    event = ''
    description_weather = ''
    dados=''
    daily_forecast = ''
    estado_selecionado = ''




# %%


with col2top:

  if city:
        st.write('Suggestions')
        buttons_cities_sugestion()


try:
    
    respose_llm = llm_ollma(city_name,description_weather,summary_weather,current_info["temp"])

except NameError:
    st.error("Something gonne wrong, don't worry, we working to fix #004 ")

except Exception as e:
    st.error("Something gonne wrong, don't worry, we working to fix #004 ")
    print(f"Error details: {e}")



col_card_esq, col_card_dir = st.columns([1, 2])



with col_card_esq:

    try:
        st.markdown(f"""
            <div class="main-left-card">
            <div class="weather-emoji">{emoji_weather}</div>
            <span>{description_weather}</span>
            <h2>{city_name}, {state_name}</h2>
            <h5>{time[0]}</h5>
            <h5>{time[1]}</h5>
            <h1>{current_info["temp"]} °C</h1>
            </div>
        """, unsafe_allow_html=True)


        b1, b2 = st.columns([0.3,0.7])


        if alertas:
            st.write('⚠️  Weather Warnings:')
            for aviso in alertas: 
                st.error(aviso)

        else:
            with b1:
                st.space('xxsmall')
                st.write('Daily:')
                st.markdown(f"""
                <div class="weather-card">
                    <div class="temp-section">
                        <div><strong>Max:</strong> ↑ {daily_max}°C</div>
                        <div><strong>Min:</strong> ↓ {daily_min}°C</div>
                </div>
                """, unsafe_allow_html=True)

            with b2:
                st.space('xxsmall')
                st.write('Information:')
                st.markdown(f"""
                    <div class="weather-card ">
                        <div>{respose_llm}</div>
                    </div>
                    """, unsafe_allow_html=True)


                coluna_info_personal,c2,c3 = st.columns([0.5,0.2,0.2])

                with coluna_info_personal:
                    st.space('xxsmall')
                    st.write('Maded by Guilherme Carvalho')


                with c2:
                    st.space('xxsmall')
                    st.page_link(label='Linkedin',page='https://www.linkedin.com/in/guilherme-carvalho-85a479218/')

                with c3:
                    st.space('xxsmall')
                    st.page_link(label='Github',page='https://github.com/GuiCRG')
        

    except NameError:
        with b2:
            st.error("Anything gonne wrong, don't worry, we working to fix #005 ")

    except Exception as e:
        with b2:
            st.error("Anything gonne wrong, don't worry, we working to fix #005 ")
            print(f"Error details: {e}")






with col_card_dir:

    try:
        st.write('Current Forecast')
        st.markdown(f"""
        <div class="right-card">
        <div class="metrics">
        <div class="metric-item">
            <div class="metric-icon">🌡️</div>
            <div class="metric-label">Feels Like</div>
            <div class="metric-value">{current_info['feels']} °C</div>
        </div>
        <div class="metric-item">
            <div class="metric-icon">💨</div>
            <div class="metric-label">Wind</div>
            <div class="metric-value">{current_info['wind']} km/h</div>
        </div>
        <div class="metric-item">
            <div class="metric-icon">👁️</div>
            <div class="metric-label">Visibility</div>
            <div class="metric-value">{current_info['vis']/1000} km</div>
        </div>
        <div class="metric-item">
            <div class="metric-icon">💧</div>
            <div class="metric-label">Humidity</div>
            <div class="metric-value">{current_info['humidity']}%</div>
        </div>
        <div class="metric-item">
            <div class="metric-icon">🧭</div>
            <div class="metric-label">Pressure</div>
            <div class="metric-value">{current_info['press']} hPa</div>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    except NameError:
        st.error("Anything gonne wrong, don't worry, we working to fix #006 ")

    except Exception as e:
        # Registra o erro real no console para você debugar, mas mostra algo amigável
        st.error("Anything gonne wrong, don't worry, we working to fix #006 ")
        print(f"Error details: {e}")




    try:
        char_hour_forecast = px.line(hour_forecast,x='hour',y='temp',height=300, labels={'hour':'Local Hour','temp':'Temp (C)'},title='Hour Forecast',text='temp')

        char_hour_forecast.update_layout(
            yaxis_range=[daily_min-2,daily_max+5], 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )



        char_hour_forecast.update_traces(textposition='top right',
                                    texttemplate='%{text}°C'
                                )



        char_hour_forecast.update_yaxes(visible=False)


        st.plotly_chart(char_hour_forecast, use_container_width=True)





        char_daily_forecast = px.line(daily_forecast,x='data',y='temp',height=300, labels={'data':'Date','temp':'Temp (C)'},title='Daily Forecast',text='temp')

        char_daily_forecast = px.line(
            daily_forecast, 
            x='data', 
            y='temp', 
            height=300, 
            labels={'data': 'Date', 'temp': 'Temp (C)'}, 
            title='Daily Forecast'
        )

        char_daily_forecast.update_layout(
            yaxis_range=[daily_min - 10, daily_max + 10],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            xaxis=dict(showgrid=False)
            )

        char_daily_forecast.update_traces(
            mode='lines+markers+text', 
            textposition='top center',   
            marker=dict(color='deepskyblue', size=8) 
        )



        char_daily_forecast.update_yaxes(visible=False)

        # Adicionando os ícones em sequência
        for data, temp, icones_daily in zip(daily_forecast['data'], daily_forecast['temp'], icones_daily):
            char_daily_forecast.add_annotation(
            x=data,
            y=temp,
            text=f"{icones_daily}<br>{int(temp)}°C ",
            showarrow=False,
            yshift=30,  
            font=dict(size=13)
            )

        st.plotly_chart(char_daily_forecast, use_container_width=True)

    except NameError:
        st.error("Anything gonne wrong, don't worry, we working to fix #007 ")

    except Exception as e:
    # Registra o erro real no console para você debugar, mas mostra algo amigável
        st.error("Anything gonne wrong, don't worry, we working to fix #007 ")
        print(f"Error details: {e}")







# %%



