import streamlit as st

def site_style()-> None:
    st.markdown(    
        """
        <style>
        /* =====================
        SIDEBAR
        ===================== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #4A6FA5, #6FA3D9);
            color: #F5F7FA;
        }

        section[data-testid="stSidebar"] div.stMarkdown span,
        section[data-testid="stSidebar"] div.stMarkdown p {
            color: #F5F7FA !important;
        }

        section[data-testid="stSidebar"] h1 {
            color: #F2C97D !important; /* sol */
        }

        /* =====================
        FUNDO PRINCIPAL
        ===================== */
        section[data-testid="stMain"] {
            background-color: #F5F7FA !important;
        }

        section[data-testid="stMain"] h1, 
        section[data-testid="stMain"] h2, 
        section[data-testid="stMain"] p, 
        section[data-testid="stMain"] li {
            color: #1F2933 !important;
        }

        /* Labels dos Widgets */
        label[data-testid="stWidgetLabel"] p {
            color: #4B5563 !important;
            font-weight: 600;
        }

        /* =====================
        HEADER / TOOLBAR
        ===================== */
        header[data-testid="stHeader"] {
            background-color: #F5F7FA !important;
        }

         header[data-testid="stHeader"] span {
            color: #000000 !important;
        }

        /* =====================
        INPUTS
        ===================== */


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
        

        /* Text input */
        div[data-testid="stTextInput"] input {
            color: #006773 !important;
            -webkit-text-fill-color:  #006773 !important;
            background-color: #ADC4F0 !important;
            border-radius: 15px;
            border: none !important;
            caret-color: #4A6FA5 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color:##618E8F !important;
            -webkit-text-fill-color: #618E8F !important;
            opacity: 1 !important;
        }

        /* Select Box input */
        div[data-testid="stSelectbox"] > div {
            color: #000000 !important ;
            border-radius: 15px;
            background-color: #ADC4F0 !important;
        }

        div[data-testid="stSelectbox"]
        div[data-baseweb="select"] > div {
            color: #006773 !important;   /* "placeholder" */
        }

        div[data-testid="stSelectbox"]
        div[data-baseweb="select"] span {
            color: #618E8F !important;   /* selecionado */
        }



                /* Number input */
        div[data-testid="stNumberInput"] input {
            color: #006773 !important;
            -webkit-text-fill-color:  #006773 !important;
            background-color: #ADC4F0 !important;
            border-radius: 15px;
            border: none !important;
            caret-color: #4A6FA5 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color:##618E8F !important;
            -webkit-text-fill-color: #618E8F !important;
            opacity: 1 !important;
        }






        </style>
        """,
        unsafe_allow_html=True
    )