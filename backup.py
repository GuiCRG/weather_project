# %%

import streamlit as st
from functions import temp_convertor, sugestion_cities, carregar_dados_locais
from functions import buttons_cities_sugestion,get_city, init_states, get_lo_la
from layout import site_style
from APIS import consult_temp
from dotenv import load_dotenv
import os
import asyncio


# %%
init_states()
site_style()


col1, col2 = st.columns([0.2,0.4],vertical_alignment='center')
df_cidades = carregar_dados_locais()

# 4. Testando o visual em cada coluna
with col1:
    city = st.text_input('Insert a city:',placeholder='New York',icon='🔎')
    df_filtrado = sugestion_cities(city,df_cidades)
    st.session_state["df_filtrado"] = df_filtrado

    city_country = get_city()

    try:
        lo_la = get_lo_la(city_country[0])
        city_name = lo_la[0]['name']
        country_name = lo_la[0]['country']
        if not 'state' in lo_la[0]:
            state_name = ' '
        else:
            state_name =lo_la[0]['state']

    except:
        city_name = ''
        country_name = ''
        state_name = ''
    

    st.markdown(f"""
        <div class="custom-card">
            <h1 style='margin: 10px 0;'>{city_name} </h1>
            <h2 style='margin: 10px 0;'>{country_name} </h2>
            <h3 style='margin: 10px 0;'>{state_name} </h3>
            <p style='color: #808495; font-size: 0.9rem;'>Temperature</p>
            <h1 style='margin: 10px 0;'>53</h1>
            <p style='color: #00d488; font-weight: bold;'>Good</p>
        </div>
    """, unsafe_allow_html=True)

    with col2:
        buttons_cities_sugestion()
        col_in1,col_in2,col_in3,col_in4,col_in5 = st.columns(5)
        colteste = st.columns(1)



        with col_in1:

            st.markdown("""
                <div class="custom-card1">
                    <p style='color: #808495; font-size: 0.9rem;'>UV Index</p>
                    <h1 style='margin: 10px 0;'>3</h1>
                    <p style='color: #feb63d; font-weight: bold;'>Moderate</p>
                </div>
            """, unsafe_allow_html=True)



    




  
    
    



# %%



