import streamlit as st

    
def site_style()-> None:
    """Definition of page layout and configs"""
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        /* Estilo do fundo da página */
        .stApp {
            background-color: #090e29;
            padding: 30px;
            border-radius: 20px;
        }

        .custom-card h1 a, .custom-card h2 a {
            display: none !important;
        }


        /* =====================
            HEADER / TOOLBAR
        ===================== */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        header[data-testid="stHeader"] span {
            display: none !important;
        }

                
        .custom-card:hover {
        transform: translateY(-10px) !important; /* Move para cima */
        border-color: #6F87A6 !important;       /* Muda a cor da borda para vermelho */
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4) !important; /* Adiciona sombra ao flutuar */
        background-color: #2D2F33 !important;    /* Clareia levemente o fundo */
        }

        
                /* Remoção de bordas */
        div[data-testid="stNumberInput"] > div, 
        div[data-testid="stTextInput"] > div, 
        div[data-testid="stSelectbox"] > div {
            background-color: #E1E5EB !important; /* Sua cor de fundo (nuvem) */
            border-radius: 20px !important;
            border: 1px solid #FFFFFF !important;
            overflow: hidden !important; /* Corta as quinas pretas residuais */
        }



        div[data-baseweb="input"], 
        div[data-baseweb="input"] > div, 
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] {
            background-color: transparent !important;
            border: none !important;
        }

        div[data-testid="stTextInput"] > div {
        background-color: #C2D4D3 !important;
        border: none !important;
        }      

        

        div[data-testid="stTextInput"] input {
            color: #C2D4D3 !important;
            -webkit-text-fill-color:  #006773 !important;
            background-color: #C2D4D3 !important;
            border-radius: 15px;
            border: none !important;
            caret-color: #4A6FA5 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color:##618E8F !important;
            -webkit-text-fill-color: #618E8F !important;
            opacity: 1 !important;
        }
                

        div[data-testid="select"] input {
            color: #C2D4D3 !impordtant;
            -webkit-text-fill-color:  #006773 !important;
            background-color: #C2D4D3 !important;
            border-radius: 15px;
            border: none !important;
            caret-color: #4A6FA5 !important;
        }

        div[data-testid="select"] input::placeholder {
            color:##618E8F !important;
            -webkit-text-fill-color: #618E8F !important;
            opacity: 1 !important; 
        }

        
    .weather-emoji {
        font-size: 150px; /* Tamanho GIGANTE do ícone */
        line-height: 1;
        margin-bottom: 10px;
        margin-top: 20px;
        filter: drop-shadow(0px 15px 20px rgba(0,0,0,0.4)); 
    }      
        
    .main-left-card {
        background: linear-gradient(180deg, #0b1028, #0f1b4d);
        border-radius: 20px;
        padding: 60px;
        padding-top: 350px;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
        height: 51vh;    
        padding: 30px;
        width: 100% !important;
        
    }
                
                
                    
        /* Força os textos a ficarem com a cor certa e sem margens gigantes */
        .main-left-card h1, 
        .main-left-card h2, 
        .main-left-card h3, 
        .main-left-card h4, 
        .main-left-card p {{
            margin: 6px 0; /* Espaço pequeno e uniforme entre os textos */
            color: #FFFFFF; /* Garante que o texto fique branco no fundo escuro */
        }}

        .main-left-card h1 {{
            font-size: 10rem; /* Deixa a temperatura bem grande */
        }}


        .right-card {
            background: linear-gradient(180deg, #0b1028, #0f1b4d);
            border-radius: 18px;
            padding: 50px;
            margin-top: 20px;
            margin-bottom: 10px;
            color: white;

        }


        .metrics {
            display: grid;
            grid-template-columns: repeat(5, 5fr);
            gap: 130px;
            text-align: center;
        }

        .metric-item {
        padding-top: 20px;
        padding-bottom: 40px;
        height: 40px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
        }

        .metric-icon {
        height: -50px;
        padding-top: 10px;
        font-size: 40px;
        opacity: 0.9;
        line-height: -1;
        }

        .metric-label {
        font-size: 13px;
        color: #c7d2fe;
        }

        .metric-value {
        font-size: 14px;
        font-weight: 600;
        }        

        .block-container {
            padding-top: 2rem !important; /* Ajuste esse valor para subir ou descer tudo de uma vez */
            padding-bottom: 1rem !important;
            margin-top: 0 !important;
        }     

                
            /* Ajusta o container da lista de sugestões para ser absoluto */
        div[data-baseweb="popover"] {
            position: absolute !important;
            z-index: 9999 !important;
        }
            
                

        .weather-card {
            color: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #1a2a40;
            display: flex;   
            align-items: center;    
            font-family: sans-serif;
            height: 10vh;
            align-items: center;
            gap: 20px;
            margin-top: -5px;   
        }

                
                
        .text-section {
            border-left: 1px solid #2d3e5e;
            padding-left: 20px;
            flex: 1;
            display: flex;
            align-items: center; 
        }



        </style>
                
        """, unsafe_allow_html=True)

    