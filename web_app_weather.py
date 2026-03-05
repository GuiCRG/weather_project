# %%

import streamlit as st
from functions import *
from functions import get_current_infos
from layout import site_style
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



# %%
init_states()
site_style()


col1top, col2top = st.columns([0.2,0.4],vertical_alignment='center')
df_cidades = carregar_dados_locais()
# st.write(df_cidades)


with col1top:
    city = st.text_input('Insert a city:',placeholder='New York',icon='🔎')
    df_filtrado = sugestion_cities(city,df_cidades)
    st.session_state["df_filtrado"] = df_filtrado
    st.write(df_filtrado)

    city_country = get_city()
    iso_pais = get_country_iso(df_cidades,city_country[1])
    
    

    try:
        lo_la = get_lo_la(city_country[0],iso_pais)
        city_name = lo_la[0]['name']
        country_name = lo_la[0]['country']

        try:
            dados = get_weather(lo_la[0]['lat'],lo_la[0]['lon'])
            current_info = get_current_infos(dados)


            hour_forecast = get_hourly(dados)
            daily_forecast = get_daily(dados)
        except:
            st.write('Error Session 1')


        try:
            time = conversor_hour_date(dados['current']['dt'],dados['timezone'])
        
        
            emoji_weather = get_icon(dados['current']['weather'][0]['icon'])
            description_weather = dados['current']['weather'][0]['description']
            # st.write(description_weather) teste -----
            daily_min,daily_max = get_max_min_daily(dados)
            alertas = get_alerts(dados)
            summary_weather = dados['daily'][0]['summary']
            icones_daily = get_icons_4_daily(dados)
            
        except:
            st.write('Error Session 2 ')

        
        linha_df = pd.DataFrame(df_cidades.loc[df_cidades['name'] == city_name])
        # st.write(linha_df)
        estado_selecionado = linha_df.iat[0,3]




        # llm_sugestion = llm_gemini(city_name,infos_curret["temp"], description_weather)



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
    
    response: ChatResponse = chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content':f"""Answer directly, concisely, and informatively. You have a strict limit of 150 characters. Do not exceed this limit under any circumstances.
                        Sugeestion of clothes or activities for the city {city_name}, state of {estado_selecionado}, temperature of {current_info["temp"]}, and weather of {description_weather},
                        based on this summary: {summary_weather}""",
    },
    ])

    resposta = response.message.content

    

col_card_esq, col_card_dir = st.columns([1, 2])



with col_card_esq:


    st.markdown(f"""
    <div class="main-left-card">
        <div class="weather-emoji">{emoji_weather}</div>
        <span>{description_weather}</span>
        <h2>{city_name}, {estado_selecionado}</h2>
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
                    <div>{resposta}</div>
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
        

    
    
with col_card_dir:
        



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




    # Problema daqui para baixo:

    char_daily_forecast = px.line(daily_forecast,x='data',y='temp',height=300, labels={'data':'Date','temp':'Temp (C)'},title='Daily Forecast',text='temp')
    
    char_daily_forecast.update_layout(
        yaxis_range=[daily_min-10,daily_max+10], 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    char_daily_forecast.update_traces(textposition='top right')
    char_daily_forecast.update_yaxes(visible=False)

    st.plotly_chart(char_daily_forecast, use_container_width=True)

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
    mode='lines+markers+text', # Adiciona os pontos
    textposition='top center',    # Centraliza o texto acima do ponto
    marker=dict(color='deepskyblue', size=8) # Define a cor e tamanho do ponto (opcional, para combinar com a imagem)
    )



    char_daily_forecast.update_yaxes(visible=False)

    # Adicionando os ícones em sequência
    # Substitua 'daily_forecast["icone"]' pela lista ou coluna correta dos seus ícones
    for data, temp, icones_daily in zip(daily_forecast['data'], daily_forecast['temp'], icones_daily):
        char_daily_forecast.add_annotation(
            x=data,
            y=temp,
            text=f"{icones_daily}<br>{int(temp)}°C ",
            showarrow=False,
            yshift=30,  # Ajuste para subir o ícone acima do texto de temperatura
            font=dict(size=13)
        )

    st.plotly_chart(char_daily_forecast, use_container_width=True)






# %%



