import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÕES DE ESTILO GLOBAL
# =========================
st.set_page_config(page_title="Dashboard - Canais Estratégicos", layout="wide")

# Adicionar CSS personalizado
st.markdown("""
    <style>
        * {font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;}
        
        .main-title {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 20px 0 30px 0;
            letter-spacing: -0.5px;
            position: relative;
            padding: 20px 0;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        }
        
        .main-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 5px;
            background: linear-gradient(90deg, transparent, #790E09, transparent);
            border-radius: 5px;
        }
        
        .main-title::after {
            content: 'CANAL ESTRATÉGICO';
            position: absolute;
            bottom: 5px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: 600;
            color: #666666;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: none;
            -webkit-text-fill-color: #666666;
            opacity: 0.8;
        }
        
        .section-title {
            font-size: 32px;
            font-weight: 700;
            color: #333333;
            margin: 40px 0 25px 0;
            padding: 15px 0 15px 25px;
            position: relative;
            background: linear-gradient(90deg, rgba(121, 14, 9, 0.1) 0%, transparent 100%);
            border-left: 4px solid #790E09;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 4px 12px rgba(121, 14, 9, 0.08);
        }
        
        .section-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #790E09 0%, #5A0A06 100%);
            border-radius: 4px;
        }
        
        .subsection-title {
            font-size: 24px;
            font-weight: 600;
            color: #333333;
            margin: 35px 0 20px 0;
            padding: 12px 0 12px 20px;
            position: relative;
            border-left: 3px solid #790E09;
            background: linear-gradient(90deg, rgba(121, 14, 9, 0.05) 0%, transparent 100%);
            border-radius: 0 6px 6px 0;
        }
        
        .subsection-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 20px;
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, #790E09, transparent);
        }
        
        .card-title {
            font-size: 20px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 20px;
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 12px;
            border: 1px solid #E9ECEF;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            position: relative;
            overflow: hidden;
        }
        
        .card-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
        }
        
        .metric-title {
            font-size: 14px;
            font-weight: 600;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #E9ECEF;
            position: relative;
        }
        
        .metric-title::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 40px;
            height: 2px;
            background: linear-gradient(90deg, #790E09, transparent);
        }
        
        .tab-title {
            font-size: 20px;
            font-weight: 700;
            color: #333333;
            padding: 8px 20px;
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 10px;
            border: 1px solid #E9ECEF;
            display: inline-block;
            margin-bottom: 20px;
            position: relative;
        }
        
        .tab-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 10px;
            border: 2px solid transparent;
            background: linear-gradient(135deg, #790E09, #5A0A06) border-box;
            -webkit-mask: 
                linear-gradient(#fff 0 0) padding-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }
        
        .title-badge {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            position: absolute;
            top: -10px;
            right: -10px;
            box-shadow: 0 2px 8px rgba(121, 14, 9, 0.3);
        }
        
        .highlight-title {
            background: linear-gradient(135deg, rgba(121, 14, 9, 0.05) 0%, rgba(90, 10, 6, 0.05) 100%);
            padding: 20px;
            border-radius: 12px;
            border: 2px solid;
            border-image: linear-gradient(135deg, #790E09, #5A0A06) 1;
            position: relative;
        }
        
        .glow-title {
            text-shadow: 0 0 20px rgba(121, 14, 9, 0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 10px rgba(121, 14, 9, 0.3); }
            to { text-shadow: 0 0 20px rgba(121, 14, 9, 0.5); }
        }
        
        .footer-logo {
            background: linear-gradient(135deg, #000000 0%, #333333 100%);
            padding: 24px;
            text-align: center;
            margin: 40px -20px -20px -20px;
            border-top: 3px solid #790E09;
            position: relative;
        }
        
        .footer-logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, #790E09, transparent);
        }
        
        .logo-text {
            color: #FFFFFF;
            font-size: 14px;
            margin-top: 12px;
            font-family: 'Segoe UI', sans-serif;
            opacity: 0.9;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: #F8F9FA;
            padding: 4px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            color: #666666 !important;
            border: 2px solid transparent !important;
            transition: all 0.3s ease;
            font-size: 16px;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 8px rgba(121, 14, 9, 0.2);
            font-weight: 700;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(121, 14, 9, 0.1) !important;
            color: #790E09 !important;
        }
        
        .kpi-card-premium {
            background: linear-gradient(145deg, #FFFFFF, #F8F9FA);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 
                0 6px 20px rgba(121, 14, 9, 0.08),
                0 2px 8px rgba(0, 0, 0, 0.04),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            margin: 12px 0;
            border: 2px solid #F0F0F0;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .kpi-card-premium:hover {
            transform: translateY(-8px);
            box-shadow: 
                0 12px 30px rgba(121, 14, 9, 0.15),
                0 4px 12px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            border-color: #790E09;
        }
        
        .kpi-card-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 16px 16px 0 0;
        }
        
        .kpi-card-premium::after {
            content: '';
            position: absolute;
            top: 4px;
            left: 4px;
            right: 4px;
            bottom: 4px;
            border: 1px solid rgba(121, 14, 9, 0.05);
            border-radius: 12px;
            pointer-events: none;
        }
        
        .kpi-title-premium {
            font-size: 20px;
            color: #333333;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 700;
            position: relative;
            padding-bottom: 12px;
        }
        
        .kpi-title-premium::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 2px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 2px;
        }
        
        .kpi-section-premium {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            justify-items: stretch;
            align-items: stretch;
        }
        
        .kpi-block-premium {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            border-radius: 12px;
            padding: 18px 12px;
            text-align: center;
            border: 1px solid #E9ECEF;
            box-shadow: 
                0 2px 6px rgba(0, 0, 0, 0.03),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-block-premium:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 4px 12px rgba(121, 14, 9, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            border-color: #790E09;
        }
        
        .kpi-block-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #5A0A06, #790E09);
            opacity: 0.7;
        }
        
        .kpi-block-title-premium {
            font-size: 13px;
            color: #666666;
            margin-bottom: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            display: inline-block;
            padding: 0 8px;
        }
        
        .kpi-block-title-premium::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 50%;
            transform: translateX(-50%);
            width: 20px;
            height: 1px;
            background: #790E09;
            opacity: 0.6;
        }
        
        .kpi-value-premium {
            font-size: 26px;
            color: #333333;
            font-weight: 800;
            margin: 8px 0;
            line-height: 1.2;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }
        
        .kpi-sub-premium {
            font-size: 13px;
            color: #666666;
            margin: 4px 0;
            font-weight: 500;
            opacity: 0.9;
        }
        
        .kpi-variacao-premium {
            font-size: 14px;
            font-weight: 700;
            margin-top: 6px;
            padding: 4px 8px;
            border-radius: 20px;
            display: inline-block;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .variacao-positiva {
            color: #2E7D32 !important;
            background: linear-gradient(135deg, rgba(232, 245, 233, 0.8), rgba(200, 230, 201, 0.9)) !important;
        }
        
        .variacao-negativa {
            color: #C62828 !important;
            background: linear-gradient(135deg, rgba(255, 235, 238, 0.8), rgba(255, 205, 210, 0.9)) !important;
        }
        
        .seta-positiva::before {
            content: '▲';
            margin-right: 4px;
            font-size: 10px;
        }
        
        .seta-negativa::before {
            content: '▼';
            margin-right: 4px;
            font-size: 10px;
        }
        
        .canal-badge {
            position: absolute;
            top: 12px;
            right: 12px;
            background: linear-gradient(135deg, #790E09, #5A0A06);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(121, 14, 9, 0.2);
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
            color: white !important;
            font-weight: 600;
            border-radius: 12px !important;
            padding: 2px 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.3px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(121, 14, 9, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #5A0A06 0%, #3A0704 100%);
            color: white;
            box-shadow: 0 6px 12px rgba(121, 14, 9, 0.3);
            transform: translateY(-1px);
        }
        
        .tab-placeholder {
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, #F8F9FA, #FFFFFF);
            border-radius: 16px;
            margin: 30px 0;
            border: 2px dashed #E9ECEF;
            position: relative;
        }
        
        .tab-placeholder::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border: 2px solid rgba(121, 14, 9, 0.05);
            border-radius: 14px;
            pointer-events: none;
        }
        
        .tab-icon {
            font-size: 64px;
            margin-bottom: 24px;
            color: #790E09;
            opacity: 0.8;
        }
        
        .stSpinner > div {
            border-color: #790E09 !important;
            border-right-color: transparent !important;
        }
        
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E9ECEF;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: #666666;
        }
        
        [data-testid="stMetricValue"] {
            font-weight: 800;
            color: #333333;
            font-size: 28px !important;
        }
        
        [data-testid="stMetricDelta"] {
            font-weight: 700;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #F5F5F5;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            border-radius: 10px;
            border: 2px solid #F5F5F5;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5A0A06 0%, #3A0704 100%);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .kpi-card-premium {
            animation: fadeIn 0.6s ease-out;
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 32px;
            }
            
            .section-title {
                font-size: 24px;
            }
            
            .subsection-title {
                font-size: 20px;
            }
            
            .kpi-section-premium {
                grid-template-columns: 1fr;
            }
            
            .kpi-value-premium {
                font-size: 22px;
            }
        }
        
        .kpi-card-legivel {
            background: linear-gradient(145deg, #FFFFFF, #F8F9FA);
            border-radius: 10px;
            padding: 14px;
            box-shadow: 
                0 4px 10px rgba(121, 14, 9, 0.08),
                0 1px 4px rgba(0, 0, 0, 0.04);
            margin: 6px 0;
            border: 1.5px solid #F0F0F0;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
            min-height: 135px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .kpi-card-legivel:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 6px 16px rgba(121, 14, 9, 0.12),
                0 2px 6px rgba(0, 0, 0, 0.06);
            border-color: #790E09;
        }
        
        .kpi-card-legivel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 10px 10px 0 0;
        }
        
        .kpi-title-legivel {
            font-size: 16px !important;
            color: #333333;
            margin-bottom: 10px !important;
            text-align: center;
            font-weight: 700;
            position: relative;
            padding-bottom: 6px;
        }
        
        .kpi-title-legivel::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 2px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 1px;
        }
        
        .kpi-section-legivel {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            justify-items: stretch;
            align-items: stretch;
        }
        
        .kpi-block-legivel {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            border-radius: 8px;
            padding: 12px 8px;
            text-align: center;
            border: 1px solid #E9ECEF;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            transition: all 0.15s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-block-legivel:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(121, 14, 9, 0.08);
            border-color: #790E09;
        }
        
        .kpi-block-legivel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #5A0A06, #790E09);
            opacity: 0.7;
        }
        
        .kpi-block-title-legivel {
            font-size: 12px !important;
            color: #333333 !important;
            margin-bottom: 6px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            position: relative;
            display: inline-block;
            padding: 0 4px;
        }
        
        .kpi-block-title-legivel::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 50%;
            transform: translateX(-50%);
            width: 15px;
            height: 1px;
            background: #790E09;
            opacity: 0.8;
        }
        
        .kpi-value-legivel {
            font-size: 24px !important;
            color: #333333;
            font-weight: 800;
            margin: 6px 0 !important;
            line-height: 1.2;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }
        
        .kpi-sub-legivel {
            font-size: 12px !important;
            color: #666666;
            margin: 3px 0 !important;
            font-weight: 600;
            opacity: 0.9;
        }
        
        .kpi-sub-legivel.small {
            font-size: 11px !important;
            opacity: 0.8;
        }
        
        .kpi-variacao-legivel {
            font-size: 12px !important;
            font-weight: 700;
            margin-top: 6px !important;
            padding: 3px 8px !important;
            border-radius: 12px;
            display: inline-block;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .canal-badge-legivel {
            position: absolute;
            top: 8px;
            right: 8px;
            background: linear-gradient(135deg, #790E09, #5A0A06);
            color: white;
            padding: 3px 10px !important;
            border-radius: 14px;
            font-size: 11px !important;
            font-weight: 700 !important;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 4px rgba(121, 14, 9, 0.2);
            z-index: 10;
        }
        
        [data-testid="column"] {
            padding: 0 8px !important;
        }
        
        .st-emotion-cache-keje6w {
            padding: 0 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES AUXILIARES
# =========================
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Carrega dados do Excel com tratamento de erros"""
    try:
        df = pd.read_excel(path)
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado!")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.stop()

def export_excel(df: pd.DataFrame) -> BytesIO:
    """Exporta DataFrame para Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados Filtrados')
    return output

@st.cache_data
def process_data_for_charts(df_filtered, mes_atual, mes_anterior):
    """Processa dados para os gráficos principais"""
    # Preparar dados para cards KPI
    canal_list = df_filtered['CANAL_PLAN'].unique()
    cards_data = []
    
    for canal in canal_list:
        canal_data = {'canal': canal, 'plataformas': {}}
        for plataforma in ['CONTA', 'FIXA']:
            atual = df_filtered.query(
                "CANAL_PLAN == @canal and COD_PLATAFORMA == @plataforma and dat_tratada == @mes_atual"
            )['QTDE'].sum()
            anterior = df_filtered.query(
                "CANAL_PLAN == @canal and COD_PLATAFORMA == @plataforma and dat_tratada == @mes_anterior"
            )['QTDE'].sum()
            variacao = ((atual - anterior) / anterior * 100) if anterior > 0 else 0
            
            canal_data['plataformas'][plataforma] = {
                'atual': atual,
                'anterior': anterior,
                'variacao': variacao
            }
        cards_data.append(canal_data)
    
    return cards_data

@st.cache_data
def create_line_chart_data(df_grafico):
    """Cria dados para gráfico de linhas temporal"""
    if 'ANO' not in df_grafico.columns or 'DAT_MÊS' not in df_grafico.columns:
        df_grafico['DAT_MOVIMENTO2'] = pd.to_datetime(df_grafico['DAT_MOVIMENTO2'], errors='coerce')
        df_grafico['ANO'] = df_grafico['DAT_MOVIMENTO2'].dt.year
        df_grafico['DAT_MÊS'] = df_grafico['DAT_MOVIMENTO2'].dt.month
    
    meses_abreviados = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }
    
    dados_grafico = []
    for ano in [2024, 2025, 2026]:
        df_ano = df_grafico[df_grafico['ANO'] == ano]
        for mes_num in range(1, 13):
            df_mes = df_ano[df_ano['DAT_MÊS'] == mes_num]
            if ano in [2024, 2025]:
                valor = df_mes['QTDE'].sum()
            else:
                valor = df_mes['DESAFIO_QTD'].sum()
            
            dados_grafico.append({
                'Ano': str(ano),
                'Mês': meses_abreviados[mes_num],
                'Mês_Num': mes_num,
                'Valor': valor,
                'Tipo': 'Real' if ano in [2024, 2025] else 'Meta'
            })
    
    df_linhas = pd.DataFrame(dados_grafico)
    df_linhas['Mês_Ord'] = df_linhas['Mês_Num']
    df_linhas = df_linhas.sort_values(['Ano', 'Mês_Ord'])
    df_linhas['Valor_Formatado'] = df_linhas['Valor'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
    
    return df_linhas

@st.cache_data
def create_bar_chart_data(df_mes_selecionado):
    """Cria dados para gráfico de barras horizontais"""
    bar_data = df_mes_selecionado.groupby(['CANAL_PLAN', 'COD_PLATAFORMA'], observed=True)['QTDE'].sum().reset_index()
    canal_totals = bar_data.groupby('CANAL_PLAN', observed=True)['QTDE'].sum().sort_values(ascending=False)
    canal_order = canal_totals.index
    
    bar_data['CANAL_PLAN'] = pd.Categorical(bar_data['CANAL_PLAN'], categories=canal_order, ordered=True)
    bar_data = bar_data.sort_values('CANAL_PLAN', ascending=False)
    bar_data['QTDE_Formatado'] = bar_data['QTDE'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
    
    return bar_data, canal_totals

@st.cache_data
def create_pivot_table(df_tabela):
    """Cria tabela pivot para performance regional"""
    regionais = sorted(df_tabela['REGIONAL'].unique())
    pivot_data = []
    
    for regional in regionais:
        df_regional = df_tabela[df_tabela['REGIONAL'] == regional]
        
        total_2024 = df_regional[df_regional['ano'] == '24']['QTDE'].sum()
        total_2025 = df_regional[df_regional['ano'] == '25']['QTDE'].sum()
        
        valores_mensais_2025 = []
        meses_2025 = [f'{mes}/25' for mes in ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']]
        for mes in meses_2025:
            valor = df_regional[df_regional['mes_ano'] == mes]['QTDE'].sum()
            valores_mensais_2025.append(valor)
        
        real_jan_26 = df_regional[df_regional['mes_ano'] == 'jan/26']['QTDE'].sum()
        meta_jan_26 = df_regional[df_regional['mes_ano'] == 'jan/26']['DESAFIO_QTD'].sum()
        
        variacao_2024_2025 = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
        
        dez_25 = df_regional[df_regional['mes_ano'] == 'dez/25']['QTDE'].sum()
        nov_25 = df_regional[df_regional['mes_ano'] == 'nov/25']['QTDE'].sum()
        variacao_mom = ((dez_25 - nov_25) / nov_25 * 100) if nov_25 > 0 else 0
        
        alcance_meta = (((real_jan_26 / meta_jan_26)-1) * 100) if meta_jan_26 > 0 else 0
        
        pivot_data.append({
            'Regional': regional,
            'Total 2024': total_2024,
            **{meses_2025[i]: valores_mensais_2025[i] for i in range(12)},
            'Total 2025': total_2025,
            'Real Jan/26': real_jan_26,
            'Meta Jan/26': meta_jan_26,
            'Alcance Meta': alcance_meta,
            'Var 2025/2024': variacao_2024_2025,
            'Var MoM': variacao_mom
        })
    
    return pivot_data, meses_2025

# =========================
# VALIDAÇÃO DE DADOS
# =========================
def validate_data(df):
    """Valida se as colunas necessárias existem no dataset"""
    required_columns = ['REGIONAL', 'CANAL_PLAN', 'dat_tratada', 'DSC_INDICADOR', 'QTDE', 'COD_PLATAFORMA', 'DAT_MOVIMENTO2', 'DESAFIO_QTD']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Colunas faltando no dataset: {missing_columns}")
        st.stop()
    
    # Verificar valores nulos críticos
    critical_columns = ['REGIONAL', 'CANAL_PLAN', 'dat_tratada', 'QTDE']
    null_counts = df[critical_columns].isnull().sum()
    
    if null_counts.sum() > 0:
        st.warning(f"Valores nulos encontrados:\n{null_counts[null_counts > 0]}")
    
    return True

# =========================
# CARREGAR E VALIDAR DADOS
# =========================
#C:\Users\F270665\OneDrive - Claro SA\Documentos\Extração_VDI\FÍSICOS_MOBILIDADE\
file_path = "base_final_trt_new2.xlsx"
df = load_data(file_path)

# Validar dados
validate_data(df)

# =========================
# FILTROS GERAIS (SIDEBAR)
# =========================
st.sidebar.header("⚙️ FILTROS GERAIS")
st.sidebar.markdown("---")

with st.sidebar:
    st.markdown("**🔍 Filtre os dados abaixo:**")
    
    region_filter = st.multiselect(
        "**Regional:**", 
        options=df['REGIONAL'].unique(), 
        default=df['REGIONAL'].unique(),
        help="Selecione uma ou mais regionais"
    )
    
    canal_filter = st.multiselect(
        "**Canal:**", 
        options=df['CANAL_PLAN'].unique(), 
        default=df['CANAL_PLAN'].unique(),
        help="Selecione um ou mais canais"
    )
    
    data_filter = st.multiselect(
        "**Período:**", 
        options=df['dat_tratada'].unique(), 
        default=df['dat_tratada'].unique(),
        help="Selecione um ou mais períodos"
    )
    
    indicador_filter = st.multiselect(
        "**Indicador:**", 
        options=df['DSC_INDICADOR'].unique(), 
        default=["Instalação", "GROSS LIQUIDO"],
        help="Selecione um ou mais indicadores"
    )
    
    st.markdown("---")
    st.markdown("**ℹ️ Informações:**")
    st.info(f"Total de registros: {len(df):,}")

# Aplicar filtros
df_filtered = df.query(
    "REGIONAL in @region_filter and CANAL_PLAN in @canal_filter and dat_tratada in @data_filter and DSC_INDICADOR in @indicador_filter"
)

# =========================
# TÍTULO PRINCIPAL
# =========================
st.markdown("""
    <div class="main-title">
        CANAIS ESTRATÉGICOS
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <span style="background: linear-gradient(135deg, #790E09, #5A0A06); color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 1px; box-shadow: 0 2px 8px rgba(121, 14, 9, 0.3);">
            📊 DASHBOARD ANALÍTICO
        </span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 5px 0 10px 0; border: 0.3px solid #E9ECEF;'>", unsafe_allow_html=True)

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["📱 Ativados", "📉 Desativados", "📋 Pedidos", "📞 Ligações"])

# =========================
# ABA 1: ATIVADOS
# =========================
with tab1:
    st.markdown("""
        <div style="text-align: center; margin: 15px 0 20px 0;">
            <div style="font-size: 16px; color: #333333; font-weight: 600; margin-bottom: 6px;">📊 PERFORMANCE POR CANAL</div>
            <div style="font-size: 12px; color: #666666; max-width: 500px; margin: 0 auto; line-height: 1.3;">
                Real - MoM - Meta
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filtro de mês para os cards
    col_filtro_mes, col_espaco = st.columns([1, 3])
    
    with col_filtro_mes:
        st.markdown('<div style="font-size: 12px; color: #666666; margin-bottom: 8px; font-weight: 600;">SELECIONE O MÊS</div>', unsafe_allow_html=True)
        
        # Obter meses disponíveis e ordenar cronologicamente
        meses_disponiveis_cards = df_filtered['dat_tratada'].unique()
        
        # Função para converter string 'mes/ano' para objeto datetime
        def mes_ano_para_data(mes_ano_str):
            try:
                meses_pt = {
                    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
                    'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
                }
                mes_str, ano_str = mes_ano_str.lower().split('/')
                mes_num = meses_pt.get(mes_str, 1)
                ano_num = int(f"20{ano_str}")
                return datetime(ano_num, mes_num, 1)
            except:
                return datetime(1900, 1, 1)
        
        # Converter para lista de datas para ordenação
        meses_com_datas = []
        for mes in meses_disponiveis_cards:
            try:
                data = mes_ano_para_data(mes)
                meses_com_datas.append((mes, data))
            except:
                meses_com_datas.append((mes, datetime(1900, 1, 1)))
        
        # Ordenar por data
        meses_com_datas.sort(key=lambda x: x[1])
        meses_ordenados = [mes for mes, _ in meses_com_datas]
        
        # Encontrar índice do mês atual
        if 'dez/25' in meses_ordenados:
            idx_padrao = meses_ordenados.index('dez/25')
        else:
            idx_padrao = len(meses_ordenados) - 1
        
        mes_selecionado_cards = st.selectbox(
            "Selecione o mês para análise",
            options=meses_ordenados,
            index=idx_padrao,
            key="mes_cards_kpi",
            label_visibility="collapsed"
        )
    
    # Encontrar o mês anterior cronologicamente
    if len(meses_ordenados) > 1:
        try:
            idx_mes_atual = meses_ordenados.index(mes_selecionado_cards)
            mes_anterior_cards = meses_ordenados[idx_mes_atual - 1] if idx_mes_atual > 0 else mes_selecionado_cards
        except:
            mes_anterior_cards = meses_ordenados[0] if len(meses_ordenados) > 0 else mes_selecionado_cards
    else:
        mes_anterior_cards = mes_selecionado_cards
    
    # Container informativo
    with col_espaco:
        st.markdown(f"""
            <div style="background: linear-gradient(90deg, #F8F0F0, #FFFFFF); 
                        padding: 12px 16px; border-radius: 8px; border-left: 4px solid #790E09;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 14px; color: #333333; font-weight: 600;">
                        Mês selecionado:
                    </span>
                    <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                background: #F8F0F0; padding: 4px 12px; border-radius: 20px;">
                        {mes_selecionado_cards}
                    </span>
                    <span style="font-size: 12px; color: #666666; margin-left: 10px;">
                        vs {mes_anterior_cards} (MoM - Mês sobre Mês)
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # CSS para cards KPI
    st.markdown("""
        <style>
        .kpi-card-dinamico {
            background: linear-gradient(145deg, #FFFFFF, #F8F9FA);
            border-radius: 10px;
            padding: 14px;
            box-shadow: 
                0 4px 10px rgba(121, 14, 9, 0.08),
                0 1px 4px rgba(0, 0, 0, 0.04);
            margin: 6px 0;
            border: 1.5px solid #F0F0F0;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .kpi-card-dinamico:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 6px 16px rgba(121, 14, 9, 0.12),
                0 2px 6px rgba(0, 0, 0, 0.06);
            border-color: #790E09;
        }
        
        .kpi-card-dinamico::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 10px 10px 0 0;
        }
        
        .kpi-title-dinamico {
            font-size: 16px !important;
            color: #333333;
            margin-bottom: 10px !important;
            text-align: center;
            font-weight: 700;
            position: relative;
            padding-bottom: 6px;
        }
        
        .kpi-title-dinamico::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 2px;
            background: linear-gradient(90deg, #790E09, #5A0A06);
            border-radius: 1px;
        }
        
        .kpi-section-dinamico {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            justify-items: stretch;
            align-items: stretch;
        }
        
        .kpi-block-dinamico {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            border-radius: 8px;
            padding: 12px 8px;
            text-align: center;
            border: 1px solid #E9ECEF;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            transition: all 0.15s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-block-dinamico:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(121, 14, 9, 0.08);
            border-color: #790E09;
        }
        
        .kpi-block-dinamico::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #5A0A06, #790E09);
            opacity: 0.7;
        }
        
        .kpi-block-title-dinamico {
            font-size: 12px !important;
            color: #333333 !important;
            margin-bottom: 8px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            position: relative;
            display: inline-block;
            padding: 0 4px;
        }
        
        .kpi-value-dinamico {
            font-size: 24px !important;
            color: #333333;
            font-weight: 800;
            margin: 6px 0 !important;
            line-height: 1.2;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }
        
        .kpi-info-dinamico {
            font-size: 11px !important;
            color: #666666;
            margin: 4px 0 !important;
            font-weight: 500;
            line-height: 1.4;
        }
        
        .kpi-info-dinamico strong {
            color: #333333;
            font-weight: 600;
        }
        
        .kpi-variacoes-container {
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
            gap: 5px;
        }
        
        .kpi-variacao-item {
            font-size: 11px !important;
            font-weight: 700;
            padding: 3px 8px !important;
            border-radius: 10px;
            display: inline-block;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            flex: 1;
            text-align: center;
            min-height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .meta-na-item {
            font-size: 11px !important;
            font-weight: 600;
            padding: 3px 8px !important;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #F5F5F5 !important;
            color: #666666 !important;
            border: 1px solid #E0E0E0;
            flex: 1;
            min-height: 20px;
        }
        
        .canal-badge-dinamico {
            position: absolute;
            top: 8px;
            right: 8px;
            background: linear-gradient(135deg, #790E09, #5A0A06);
            color: white;
            padding: 3px 10px !important;
            border-radius: 14px;
            font-size: 11px !important;
            font-weight: 700 !important;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 4px rgba(121, 14, 9, 0.2);
            z-index: 10;
        }
        
        .variacao-positiva {
            color: #2E7D32 !important;
            background: linear-gradient(135deg, rgba(232, 245, 233, 0.9), rgba(200, 230, 201, 0.95)) !important;
        }
        
        .variacao-negativa {
            color: #C62828 !important;
            background: linear-gradient(135deg, rgba(255, 235, 238, 0.9), rgba(255, 205, 210, 0.95)) !important;
        }
        
        .seta-positiva::before {
            content: '▲';
            margin-right: 4px;
            font-size: 10px;
            font-weight: 900;
            display: inline-block;
            vertical-align: middle;
            line-height: 1;
        }
        
        .seta-negativa::before {
            content: '▼';
            margin-right: 4px;
            font-size: 10px;
            font-weight: 900;
            display: inline-block;
            vertical-align: middle;
            line-height: 1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Função para calcular métricas
    def calcular_metricas_canal(canal, plataforma, mes_atual, mes_anterior):
        atual = df_filtered.query(
            "CANAL_PLAN == @canal and COD_PLATAFORMA == @plataforma and dat_tratada == @mes_atual"
        )['QTDE'].sum()
        
        anterior = df_filtered.query(
            "CANAL_PLAN == @canal and COD_PLATAFORMA == @plataforma and dat_tratada == @mes_anterior"
        )['QTDE'].sum()
        
        meta = df_filtered.query(
            "CANAL_PLAN == @canal and COD_PLATAFORMA == @plataforma and dat_tratada == @mes_atual"
        )['DESAFIO_QTD'].sum()
        
        variacao_mom = ((atual - anterior) / anterior * 100) if anterior > 0 else 0
        
        if meta > 0:
            desvio_meta = ((atual / meta) - 1) * 100
        else:
            desvio_meta = None
        
        return {
            'atual': atual,
            'anterior': anterior,
            'meta': meta,
            'variacao_mom': variacao_mom,
            'desvio_meta': desvio_meta
        }
    
    # Ordenar canais na ordem especificada
    ordem_desejada = [
        'Televendas Ativo',
        'Televendas Receptivo', 
        'S2S+DAC',
        'E-commerce',
        'Inside Sales',
        'Hospitality'
    ]
    
    todos_canais = df_filtered['CANAL_PLAN'].unique()
    canal_list = []
    for canal in ordem_desejada:
        if canal in todos_canais:
            canal_list.append(canal)
    
    for canal in todos_canais:
        if canal not in canal_list:
            canal_list.append(canal)
    
    num_canais = len(canal_list)
    
    # Renderizar cards KPI
    for i in range(0, num_canais, 3):
        cols = st.columns(3, gap="small")
        canais_linha = canal_list[i:i+3]
        
        for j, canal in enumerate(canais_linha):
            plataformas = ['CONTA', 'FIXA']
            bloco_html = ""
            
            for plataforma in plataformas:
                metricas = calcular_metricas_canal(canal, plataforma, mes_selecionado_cards, mes_anterior_cards)
                
                atual = metricas['atual']
                anterior = metricas['anterior']
                meta = metricas['meta']
                variacao_mom = metricas['variacao_mom']
                desvio_meta = metricas['desvio_meta']
                
                atual_formatado = f"{atual:,.0f}".replace(",", ".")
                anterior_formatado = f"{anterior:,.0f}".replace(",", ".")
                meta_formatado = f"{meta:,.0f}".replace(",", ".")
                
                if variacao_mom >= 0:
                    classe_mom = "variacao-positiva seta-positiva"
                else:
                    classe_mom = "variacao-negativa seta-negativa"
                
                if desvio_meta is not None:
                    if desvio_meta >= 0:
                        classe_meta = "variacao-positiva seta-positiva"
                    else:
                        classe_meta = "variacao-negativa seta-negativa"
                    
                    meta_html = f'<div class="kpi-variacao-item {classe_meta}">{desvio_meta:+.1f}% Meta</div>'
                else:
                    meta_html = '<div class="meta-na-item">Meta N/A</div>'
                
                bloco_html += (
                    f'<div class="kpi-block-dinamico">'
                    f'<div class="kpi-block-title-dinamico">{plataforma}</div>'
                    f'<div class="kpi-value-dinamico">{atual_formatado}</div>'
                    f'<div class="kpi-info-dinamico">'
                    f'<strong>Vs Mês Anterior:</strong> {anterior_formatado} | '
                    f'<strong>Meta:</strong> {meta_formatado}'
                    f'</div>'
                    f'<div class="kpi-variacoes-container">'
                    f'<div class="kpi-variacao-item {classe_mom}">{variacao_mom:+.1f}% MoM</div>'
                    f'{meta_html}'
                    f'</div>'
                    f'</div>'
                )
            
            with cols[j]:
                with st.container():
                    st.markdown(
                        f'<div class="kpi-card-dinamico">'
                        f'<div class="canal-badge-dinamico">{canal}</div>'
                        f'<div class="kpi-title-dinamico">{canal}</div>'
                        f'<div class="kpi-section-dinamico">{bloco_html}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
    
    # Rodapé da seção
    st.markdown(f"""
        <div style="margin-top: 25px; text-align: center; padding: 12px; background: #F8F9FA; border-radius: 8px; border: 1px solid #E9ECEF;">
            <div style="font-size: 12px; color: #666666; margin-bottom: 8px;">
                <span style="color: #790E09; font-weight: 600;">📌</span> 
                Métricas calculadas: <strong>MoM</strong> (Mês sobre mês vs {mes_anterior_cards}) e <strong>% Meta</strong> (Desvio percentual em relação à meta)
            </div>
            <div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 12px; height: 12px; background: #E8F5E9; border-radius: 50%; border: 1px solid #C8E6C9;"></div>
                    <span style="font-size: 12px; color: #666666; font-weight: 600;">Positivo ▲</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 12px; height: 12px; background: #FFEBEE; border-radius: 50%; border: 1px solid #FFCDD2;"></div>
                    <span style="font-size: 12px; color: #666666; font-weight: 600;">Negativo ▼</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 12px; height: 12px; background: #F5F5F5; border-radius: 50%; border: 1px solid #E0E0E0;"></div>
                    <span style="font-size: 12px; color: #666666; font-weight: 600;">Meta não disponível</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas gerais do mês selecionado
    with st.expander("📊 Métricas gerais do mês selecionado", expanded=False):
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        total_atual = df_filtered[df_filtered['dat_tratada'] == mes_selecionado_cards]['QTDE'].sum()
        total_anterior = df_filtered[df_filtered['dat_tratada'] == mes_anterior_cards]['QTDE'].sum()
        total_meta = df_filtered[df_filtered['dat_tratada'] == mes_selecionado_cards]['DESAFIO_QTD'].sum()
        
        variacao_total_mom = ((total_atual - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
        
        if total_meta > 0:
            desvio_total_meta = ((total_atual / total_meta) - 1) * 100
        else:
            desvio_total_meta = None
        
        with col_res1:
            st.metric(
                label=f"Total {mes_selecionado_cards}",
                value=f"{total_atual:,.0f}".replace(",", "."),
                delta=f"{variacao_total_mom:+.1f}% vs {mes_anterior_cards}"
            )
        
        with col_res2:
            if desvio_total_meta is not None:
                st.metric(
                    label=f"Meta {mes_selecionado_cards}",
                    value=f"{total_meta:,.0f}".replace(",", "."),
                    delta=f"{desvio_total_meta:+.1f}% vs meta"
                )
            else:
                st.metric(
                    label=f"Meta {mes_selecionado_cards}",
                    value=f"{total_meta:,.0f}".replace(",", "."),
                    delta="Meta não disponível"
                )
        
        with col_res3:
            canais_ativos = len(df_filtered[df_filtered['dat_tratada'] == mes_selecionado_cards]['CANAL_PLAN'].unique())
            st.metric(
                label="Canais ativos",
                value=canais_ativos
            )
        
        with col_res4:
            plataformas_ativas = len(df_filtered[df_filtered['dat_tratada'] == mes_selecionado_cards]['COD_PLATAFORMA'].unique())
            st.metric(
                label="Plataformas",
                value=plataformas_ativas
            )
    
# =========================
# GRÁFICO DE LINHAS TEMPORAL
# =========================
with st.container():
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <div style="font-size: 18px; color: #333333; font-weight: 600;">
                📈 EVOLUÇÃO MENSAL - COMPARATIVO ANUAL
            </div>
            <div style="font-size: 12px; color: #FF2800; font-weight: 600; padding: 4px 10px; 
                        background: rgba(255, 40, 0, 0.08); border-radius: 4px;">
                ANÁLISE TEMPORAL
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
        
        with col_filtro1:
            st.markdown('<div style="font-size: 12px; color: #666666; margin-bottom: 8px; font-weight: 600;">CANAL</div>', unsafe_allow_html=True)
            canal_selecionado = st.selectbox(
                "Selecione o Canal",
                options=["Todos"] + sorted(df_filtered['CANAL_PLAN'].unique()),
                key="filtro_canal_linhas",
                label_visibility="collapsed"
            )
        
        with col_filtro2:
            st.markdown('<div style="font-size: 12px; color: #666666; margin-bottom: 8px; font-weight: 600;">REGIONAL</div>', unsafe_allow_html=True)
            regional_selecionada = st.selectbox(
                "Selecione a Regional",
                options=["Todos"] + sorted(df_filtered['REGIONAL'].unique()),
                key="filtro_regional_linhas",
                label_visibility="collapsed"
            )
        
        with col_filtro3:
            st.markdown('<div style="font-size: 12px; color: #666666; margin-bottom: 8px; font-weight: 600;">INDICADOR</div>', unsafe_allow_html=True)
            indicador_selecionado = st.selectbox(
                "Selecione o Indicador",
                options=["Todos"] + sorted(df_filtered['DSC_INDICADOR'].unique()),
                key="filtro_indicador_linhas",
                label_visibility="collapsed"
            )
        
        with col_filtro4:
            st.markdown('<div style="font-size: 12px; color: #666666; margin-bottom: 8px; font-weight: 600;">PLATAFORMA</div>', unsafe_allow_html=True)
            plataforma_selecionada = st.selectbox(
                "Selecione a Plataforma",
                options=["Todos"] + sorted(df_filtered['COD_PLATAFORMA'].unique()),
                key="filtro_plataforma_linhas",
                label_visibility="collapsed"
            )
    
    # Aplicar filtros
    df_grafico = df_filtered.copy()
    
    if canal_selecionado != "Todos":
        df_grafico = df_grafico[df_grafico['CANAL_PLAN'] == canal_selecionado]
    if regional_selecionada != "Todos":
        df_grafico = df_grafico[df_grafico['REGIONAL'] == regional_selecionada]
    if indicador_selecionado != "Todos":
        df_grafico = df_grafico[df_grafico['DSC_INDICADOR'] == indicador_selecionado]
    if plataforma_selecionada != "Todos":
        df_grafico = df_grafico[df_grafico['COD_PLATAFORMA'] == plataforma_selecionada]
    
    # Criar dados para gráfico
    df_linhas = create_line_chart_data(df_grafico)
    
    # Criar título dinâmico
    filtros_ativos = []
    if canal_selecionado != "Todos":
        filtros_ativos.append(f"Canal: {canal_selecionado}")
    if regional_selecionada != "Todos":
        filtros_ativos.append(f"Regional: {regional_selecionada}")
    if indicador_selecionado != "Todos":
        filtros_ativos.append(f"Indicador: {indicador_selecionado}")
    if plataforma_selecionada != "Todos":
        filtros_ativos.append(f"Plataforma: {plataforma_selecionada}")
    
    titulo_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Todos os Filtros"
    
    # Criar gráfico
    cores_personalizadas = {
        '2024': '#FF2800',
        '2025': '#790E09',
        '2026': '#5A6268'
    }
    
    fig_linhas = px.line(
        df_linhas,
        x='Mês',
        y='Valor',
        color='Ano',
        title=f'<b>📈 EVOLUÇÃO MENSAL</b><br><span style="font-size: 13px; color: #666666;">Comparativo Anual | {titulo_filtros}</span>',
        labels={'Valor': '', 'Mês': ''},
        markers=True,
        line_shape='spline',
        color_discrete_map=cores_personalizadas,
        text='Valor_Formatado'
    )
    
    fig_linhas.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Segoe UI', size=13, color='#333333'),
        margin=dict(l=40, r=40, t=70, b=60),
        xaxis=dict(
            title='',
            tickmode='array',
            tickvals=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
            tickfont=dict(size=12, color='#666666'),
            showgrid=False,
            linecolor='#E9ECEF',
            linewidth=1,
            mirror=True,
            tickangle=0,
            showline=True,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=12, color='#666666'),
            showgrid=True,
            gridcolor='rgba(233, 236, 239, 0.3)',
            linecolor='#E9ECEF',
            linewidth=1,
            mirror=True,
            showline=True,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#E9ECEF',
            borderwidth=1,
            font=dict(size=12, color='#333333'),
            itemwidth=40,
            itemclick=False,
            itemdoubleclick=False,
            title=None
        ),
        title=dict(
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=16, color='#333333'),
            y=0.95
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Segoe UI',
            bordercolor='#E9ECEF',
            font_color='#333333'
        ),
        height=420
    )
    
    for i, trace in enumerate(fig_linhas.data):
        ano = trace.name
        trace.update(
            mode='lines+markers+text',
            marker=dict(size=9, line=dict(width=1.5, color='white'), symbol='circle', opacity=0.9),
            line=dict(width=3, smoothing=1.3),
            textposition='top center',
            textfont=dict(size=10, color=cores_personalizadas[ano]),  # REMOVI weight='bold'
            hovertemplate=(
                f"<b>%{{x}}/{ano}</b><br>" +
                "Valor: <b>%{y:,.0f}</b><br>" +
                "<extra></extra>"
            )
        )
        
        if ano == '2026':
            trace.update(
                line=dict(width=3, dash='dash', color=cores_personalizadas[ano]),
                marker=dict(size=9, line=dict(width=1.5, color='white'), symbol='diamond', opacity=0.9)
            )
    
    # Container de informações
    st.markdown(f"""
        <div style="background: #F8F9FA; 
                    padding: 8px 12px; 
                    border-radius: 8px; 
                    border: 1px solid #E9ECEF;
                    margin: 10px 0 5px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 13px; color: #333333;">
                    <span style="font-weight: 600;">📊 Dados Filtrados:</span>
                    <span style="color: #FF2800; font-weight: 700; margin-left: 5px;">{len(df_grafico):,}</span>
                </div>
                <div style="font-size: 12px; color: #666666; display: flex; gap: 15px;">
                    <span style="display: inline-flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background: #FF2800; border-radius: 50%; margin-right: 5px;"></div>
                        2024 (Real)
                    </span>
                    <span style="display: inline-flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background: #790E09; border-radius: 50%; margin-right: 5px;"></div>
                        2025 (Real)
                    </span>
                    <span style="display: inline-flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background: #5A6268; border-radius: 50%; margin-right: 5px; border: 1px solid #E9ECEF;"></div>
                        2026 (Meta) <span style="color: #5A6268; margin-left: 3px;">— —</span>
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Exibir gráfico
    st.plotly_chart(fig_linhas, width='stretch')
    
    # Insights
    if not df_linhas.empty:
        df_2024 = df_linhas[df_linhas['Ano'] == '2024']
        df_2025 = df_linhas[df_linhas['Ano'] == '2025']
        df_2026 = df_linhas[df_linhas['Ano'] == '2026']
        
        if not df_2024.empty and not df_2025.empty:
            crescimento_2024_2025 = ((df_2025['Valor'].sum() - df_2024['Valor'].sum()) / df_2024['Valor'].sum() * 100) if df_2024['Valor'].sum() > 0 else 0
            
            st.markdown("""
                <div style="background: #F8F9FA; 
                            padding: 15px; 
                            border-radius: 8px; 
                            border: 1px solid #E9ECEF;
                            margin-top: 10px;">
                    <div style="font-size: 13px; 
                                color: #333333; 
                                font-weight: 600; 
                                margin-bottom: 12px;
                                padding-bottom: 8px;
                                border-bottom: 1px solid #E9ECEF;">
                        💡 INSIGHTS DA ANÁLISE
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_2025 = df_2025['Valor'].sum()
                st.metric(
                    label="Total 2025",
                    value=f"{total_2025:,.0f}".replace(",", "."),
                    delta=f"{crescimento_2024_2025:+.1f}% vs 2024" if crescimento_2024_2025 != 0 else None,
                    label_visibility="visible"
                )
            
            with col2:
                if not df_2026.empty:
                    meta_2026 = df_2026['Valor'].sum()
                    alcance_meta = (df_2025['Valor'].sum() / meta_2026 * 100) if meta_2026 > 0 else 0
                    st.metric(
                        label="Meta 2026",
                        value=f"{meta_2026:,.0f}".replace(",", "."),
                        delta=f"{alcance_meta:.1f}% do alcançado",
                        label_visibility="visible"
                    )
            
            with col3:
                melhor_mes_2025 = df_2025.loc[df_2025['Valor'].idxmax()] if not df_2025.empty else None
                if melhor_mes_2025 is not None:
                    st.metric(
                        label="Melhor Mês 2025",
                        value=f"{melhor_mes_2025['Mês'].title()}",
                        delta=f"{melhor_mes_2025['Valor']:,.0f}".replace(",", "."),
                        label_visibility="visible"
                    )
            
            st.markdown("""
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # =========================
    # GRÁFICO DE BARRAS HORIZONTAIS
    # =========================
    with st.container():
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; 
                        margin-bottom: 15px; padding-bottom: 12px; border-bottom: 2px solid #F0F0F0;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: linear-gradient(135deg, #790E09, #5A0A06); 
                                width: 40px; height: 40px; border-radius: 10px; 
                                display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-size: 20px;">📊</span>
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #333333; font-weight: 700; font-size: 18px;">
                            DISTRIBUIÇÃO POR CANAL E INDICADOR
                        </h3>
                        <p style="margin: 0; color: #666666; font-size: 13px; font-weight: 400;">
                            Análise detalhada por segmento e performance
                        </p>
                    </div>
                </div>
                <div style="background: #F8F0F0; padding: 6px 12px; border-radius: 6px; 
                            border: 1px solid #E9D6D6;">
                    <span style="color: #790E09; font-size: 11px; font-weight: 600; letter-spacing: 0.5px;">
                        VISÃO EXECUTIVA
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background: #F8F9FA; padding: 15px; border-radius: 10px; 
                        margin-bottom: 20px; border: 1px solid #E9ECEF;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #790E09; font-size: 16px;">📅</span>
                        <span style="font-size: 14px; color: #333333; font-weight: 600;">
                            Período de Análise
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #666666;">
                        Selecione o mês para análise detalhada
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_sel1, col_sel2 = st.columns([1, 3])
        
        with col_sel1:
            meses_disponiveis = sorted(df_filtered['dat_tratada'].unique())
            mes_selecionado = st.selectbox(
                "Selecione o Mês",
                options=meses_disponiveis,
                index=len(meses_disponiveis)-1 if 'dez/25' not in meses_disponiveis else list(meses_disponiveis).index('dez/25'),
                key="mes_barra_horizontal",
                label_visibility="collapsed"
            )
        
        with col_sel2:
            st.markdown(f"""
                <div style="background: linear-gradient(90deg, #F8F0F0, #FFFFFF); 
                            padding: 12px 16px; border-radius: 8px; border-left: 4px solid #790E09;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 14px; color: #333333; font-weight: 600;">
                            Mês selecionado:
                        </span>
                        <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                    background: #F8F0F0; padding: 4px 12px; border-radius: 20px;">
                            {mes_selecionado}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1px; background: linear-gradient(90deg, #790E09, #E9ECEF); margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Filtrar dados
        df_mes_selecionado = df_filtered[df_filtered['dat_tratada'] == mes_selecionado]
        
        if not df_mes_selecionado.empty:
            # Criar dados para gráfico
            bar_data, canal_totals = create_bar_chart_data(df_mes_selecionado)
            
            # Definir paleta de cores
            indicadores_unicos = bar_data['COD_PLATAFORMA'].unique()
            
            def gerar_gradiente(cor_base, num_cores, fator_clareamento=0.2):
                import colorsys
                cor_rgb = tuple(int(cor_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                h, l, s = colorsys.rgb_to_hls(cor_rgb[0]/255, cor_rgb[1]/255, cor_rgb[2]/255)
                
                cores_gradiente = []
                for i in range(num_cores):
                    nova_luminosidade = min(0.7, l + (fator_clareamento * i / max(1, num_cores-1)))
                    r, g, b = colorsys.hls_to_rgb(h, nova_luminosidade, s)
                    cor_hex = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
                    cores_gradiente.append(cor_hex)
                
                return cores_gradiente
            
            cores_base = ['#5A0A06', '#790E09', '#9A130C', '#BB1810']
            num_indicadores = len(indicadores_unicos)
            color_map = {}
            
            if num_indicadores <= len(cores_base):
                for i, indicador in enumerate(indicadores_unicos):
                    if i < len(cores_base):
                        color_map[indicador] = cores_base[i]
                    else:
                        color_map[indicador] = cores_base[-1]
            else:
                cores_gradiente = gerar_gradiente('#790E09', num_indicadores)
                for i, indicador in enumerate(indicadores_unicos):
                    color_map[indicador] = cores_gradiente[i]
            
            # Criar gráfico
            fig_bar = px.bar(
                bar_data, 
                y='CANAL_PLAN',
                x='QTDE',
                color='COD_PLATAFORMA',
                text='QTDE_Formatado',
                barmode='stack',
                color_discrete_map=color_map,
                title=f'<b>DISTRIBUIÇÃO POR CANAL</b><br><span style="font-size: 13px; color: #666666;">Análise de {mes_selecionado} - Composição por Indicador</span>',
                labels={'QTDE': 'Volume', 'CANAL_PLAN': 'Canal'},
                orientation='h',
                height=500,
            )
            
            fig_bar.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Segoe UI', size=13, color='#333333'),
                margin=dict(l=10, r=120, t=80, b=50),
                yaxis=dict(
                    title='<b>Canal</b>',
                    title_font=dict(size=14, weight='bold', color='#333333'),
                    tickfont=dict(size=13, color='#666666'),
                    showgrid=False,
                    linecolor='#E9ECEF',
                    linewidth=1,
                    ticksuffix="  ",
                    categoryorder='total ascending'
                ),
                xaxis=dict(
                    title='<b>Volume Total</b>',
                    title_font=dict(size=14, weight='bold', color='#333333'),
                    tickfont=dict(size=12, color='#666666'),
                    gridcolor='rgba(233, 236, 239, 0.6)',
                    showgrid=True,
                    gridwidth=0.5,
                    zeroline=False,
                    showline=True,
                    linecolor='#E9ECEF',
                    linewidth=1
                ),
                legend=dict(
                    title=dict(text='<b>INDICADOR</b>', font=dict(size=13, weight='bold', color='#333333')),
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#E9ECEF',
                    borderwidth=1,
                    font=dict(size=12, color='#333333'),
                    itemwidth=30,
                    traceorder='normal',
                    itemsizing='constant'
                ),
                title=dict(
                    x=0.02,
                    xanchor='left',
                    yanchor='top',
                    font=dict(size=17, color='#333333', weight='bold'),
                    y=0.95
                ),
                hovermode='y unified',
                hoverlabel=dict(
                    bgcolor='white',
                    font_size=13,
                    font_family='Segoe UI',
                    bordercolor='#E9ECEF',
                    font_color='#333333'
                ),
                bargap=0.25,
                bargroupgap=0.05,
                showlegend=True,
                transition=dict(duration=300),
                shapes=[
                    dict(
                        type="rect",
                        xref="paper",
                        yref="paper",
                        x0=0,
                        y0=0,
                        x1=1,
                        y1=1,
                        line=dict(color="#E9ECEF", width=1),
                        fillcolor="rgba(0,0,0,0)",
                    )
                ]
            )
            
            fig_bar.update_traces(
                texttemplate='%{text}',
                textposition='inside',
                textfont=dict(size=11, color='white', weight='bold'),
                marker=dict(line=dict(width=1, color='white'), opacity=0.9),
                hovertemplate=(
                    "<b>Canal: %{y}</b><br>" +
                    "Indicador: <b>%{fullData.name}</b><br>" +
                    "Volume: <b>%{x:,.0f}</b><br>" +
                    "<extra></extra>"
                )
            )
            
            # Adicionar totais
            total_geral = canal_totals.sum()
            for i, canal in enumerate(canal_totals.index):
                total_canal = canal_totals[canal]
                percentual = (total_canal / total_geral * 100) if total_geral > 0 else 0
                
                fig_bar.add_annotation(
                    x=total_canal,
                    y=canal,
                    text=f'<b>{total_canal:,.0f}</b><br><span style="font-size: 11px; color: #666666;">({percentual:.1f}%)</span>',
                    showarrow=False,
                    xshift=50,
                    font=dict(size=12, color='#333333'),
                    align='left',
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='#E9ECEF',
                    borderwidth=1,
                    borderpad=4,
                    width=70
                )
                
                fig_bar.add_shape(
                    type="line",
                    x0=total_canal,
                    y0=i,
                    x1=total_canal + 40,
                    y1=i,
                    line=dict(color="#CCCCCC", width=1, dash="dot"),
                    layer="below"
                )
            
            # Adicionar total geral
            fig_bar.add_annotation(
                xref="paper",
                yref="paper",
                x=1.12,
                y=1.05,
                text=f"<b>TOTAL GERAL</b><br><span style='font-size: 20px; color: #790E09;'>{total_geral:,.0f}</span>",
                showarrow=False,
                font=dict(size=13, color='#333333'),
                align="center",
                bgcolor='#F8F9FA',
                bordercolor='#E9ECEF',
                borderwidth=1,
                borderpad=8
            )
            
            # Exibir gráfico
            st.plotly_chart(fig_bar, width='stretch')
            
            # Insights e KPIs
            with st.container():
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #F8F9FA, #FFFFFF); 
                                padding: 20px; border-radius: 12px; border: 1px solid #E9ECEF; 
                                margin-top: 20px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                            <span style="color: #790E09; font-size: 18px;">💡</span>
                            <span style="font-size: 14px; color: #333333; font-weight: 600;">
                                INSIGHTS E ANÁLISES
                            </span>
                        </div>
                """, unsafe_allow_html=True)
                
                total_por_indicador = bar_data.groupby('COD_PLATAFORMA', observed=True)['QTDE'].sum()
                top_canal = canal_totals.index[0] if len(canal_totals) > 0 else "N/A"
                top_valor = canal_totals.iloc[0] if len(canal_totals) > 0 else 0
                
                if len(total_por_indicador) > 0:
                    top_indicador = total_por_indicador.idxmax()
                    top_indicador_valor = total_por_indicador.max()
                    top_indicador_percent = (top_indicador_valor / total_geral * 100) if total_geral > 0 else 0
                
                col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
                
                with col_kpi1:
                    st.metric(
                        label="Total Geral",
                        value=f"{total_geral:,.0f}".replace(',', '.'),
                        help="Soma total de todos os canais"
                    )
                
                with col_kpi2:
                    if len(canal_totals) > 0:
                        st.metric(
                            label="Canal Líder",
                            value=top_canal,
                            delta=f"{top_valor:,.0f}".replace(',', '.'),
                            delta_color="off"
                        )
                
                with col_kpi3:
                    if len(total_por_indicador) > 0:
                        st.metric(
                            label="Indicador Principal",
                            value=top_indicador,
                            delta=f"{top_indicador_percent:.1f}%",
                            delta_color="normal"
                        )
                
                with col_kpi4:
                    st.metric(
                        label="Canais Analisados",
                        value=len(canal_totals),
                        delta="Segmentos"
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Tabela expandível
            with st.expander("📋 DETALHAMENTO NUMÉRICO COMPLETO", expanded=False):
                st.markdown("""
                    <div style="background: #F8F9FA; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #790E09; font-size: 14px;">🔍</span>
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">
                                Tabela de Composição Detalhada
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                pivot_data = bar_data.pivot_table(
                    index='CANAL_PLAN',
                    columns='COD_PLATAFORMA',
                    values='QTDE',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()
                
                pivot_data['TOTAL'] = pivot_data.sum(axis=1, numeric_only=True)
                
                indicadores = [col for col in pivot_data.columns if col not in ['CANAL_PLAN', 'TOTAL']]
                for indicador in indicadores:
                    pivot_data[f'{indicador} %'] = (pivot_data[indicador] / pivot_data['TOTAL'] * 100).round(1)
                
                pivot_data = pivot_data.sort_values('TOTAL', ascending=False)
                
                def formatar_numero(valor):
                    if isinstance(valor, (int, float)):
                        if valor == int(valor):
                            return f'{int(valor):,}'.replace(',', '.')
                        else:
                            return f'{valor:,.1f}'.replace(',', '.')
                    return valor
                
                for col in pivot_data.columns:
                    if col not in ['CANAL_PLAN', 'TOTAL'] and not col.endswith('%'):
                        pivot_data[col] = pivot_data[col].apply(formatar_numero)
                    elif col == 'TOTAL':
                        pivot_data[col] = pivot_data[col].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
                
                styled_table = pivot_data.style.format({
                    col: '{:.1f}%' for col in pivot_data.columns if col.endswith('%')
                }).apply(lambda x: ['background: #F8F0F0' if x.name == 'TOTAL' else '' for i in x], axis=1)
                
                st.dataframe(styled_table, width='stretch', height=300)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8F0F0, #FFFFFF); 
                            padding: 30px; border-radius: 12px; border: 1px solid #E9D6D6;
                            text-align: center; margin: 20px 0;">
                    <div style="color: #790E09; font-size: 48px; margin-bottom: 15px;">
                        ⚠️
                    </div>
                    <h3 style="color: #333333; margin-bottom: 10px;">
                        Dados Insuficientes para Análise
                    </h3>
                    <p style="color: #666666; margin-bottom: 20px;">
                        Não há dados disponíveis para <strong>{mes_selecionado}</strong> com os filtros atuais.
                    </p>
            """, unsafe_allow_html=True)
            
            if len(meses_disponiveis) > 0:
                st.info(f"**Meses disponíveis para análise:** {', '.join(sorted(meses_disponiveis))}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # =========================
    # TABELA DINÂMICA POR REGIONAL COM MÉTRICAS AVANÇADAS (VERSÃO MELHORADA)
    # =========================
    st.subheader("📊 CANAIS ESTRATÉGICOS - PERFORMANCE POR REGIONAL")
    
    # Adicionar filtros específicos para a tabela
    col_filtro_t1, col_filtro_t2 = st.columns(2)
    
    with col_filtro_t1:
        canal_tabela = st.multiselect(
            "Filtrar por Canal:",
            options=["Todos"] + sorted(df_filtered['CANAL_PLAN'].unique()),
            default=["Todos"],
            key="filtro_canal_tabela"
        )
    
    with col_filtro_t2:
        plataforma_tabela = st.multiselect(
            "Filtrar por Plataforma:",
            options=["Todos"] + sorted(df_filtered['COD_PLATAFORMA'].unique()),
            default=["Todos"],
            key="filtro_plataforma_tabela"
        )
    
    # Aplicar filtros à tabela
    df_tabela = df_filtered.copy()
    
    if "Todos" not in canal_tabela:
        df_tabela = df_tabela[df_tabela['CANAL_PLAN'].isin(canal_tabela)]
    
    if "Todos" not in plataforma_tabela:
        df_tabela = df_tabela[df_tabela['COD_PLATAFORMA'].isin(plataforma_tabela)]
    
    # Extrair ano e mês da coluna dat_tratada
    df_tabela['ano'] = df_tabela['dat_tratada'].str.split('/').str[1]
    df_tabela['mes_ano'] = df_tabela['dat_tratada']
    
    # Definir a ordem dos meses
    meses_ordem = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    meses_2025 = [f'{mes}/25' for mes in meses_ordem]
    
    # FUNÇÃO PARA CRIAR TABELA PIVOT
    @st.cache_data
    def create_pivot_table(df_tabela, meses_2025):
        """
        Função para criar tabela pivot dinâmica
        """
        pivot_data = []
        regionais = sorted(df_tabela['REGIONAL'].unique())
        
        for regional in regionais:
            df_regional = df_tabela[df_tabela['REGIONAL'] == regional]
            
            # Calcular totais por ano
            total_2024 = df_regional[df_regional['ano'] == '24']['QTDE'].sum()
            total_2025 = df_regional[df_regional['ano'] == '25']['QTDE'].sum()
            
            # Calcular valores mensais para 2025
            valores_mensais_2025 = []
            for mes in meses_2025:
                valor = df_regional[df_regional['mes_ano'] == mes]['QTDE'].sum()
                valores_mensais_2025.append(valor)
            
            # Calcular valor REAL de jan/26 (QTDE) - NOVA COLUNA
            real_jan_26 = df_regional[df_regional['mes_ano'] == 'jan/26']['QTDE'].sum()
            
            # Calcular valor de jan/26 (meta) - DESAFIO_QTD
            meta_jan_26 = df_regional[df_regional['mes_ano'] == 'jan/26']['DESAFIO_QTD'].sum()
            
            # Calcular variações
            variacao_2024_2025 = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
            
            # Calcular variação MoM (dez/25 vs nov/25)
            dez_25 = df_regional[df_regional['mes_ano'] == 'dez/25']['QTDE'].sum()
            nov_25 = df_regional[df_regional['mes_ano'] == 'nov/25']['QTDE'].sum()
            variacao_mom = ((dez_25 - nov_25) / nov_25 * 100) if nov_25 > 0 else 0
            
            # Calcular alcance da meta (%) - agora usando real_jan_26 vs meta_jan_26
            alcance_meta = (((real_jan_26 / meta_jan_26)-1) * 100) if meta_jan_26 > 0 else 0
            
            pivot_data.append({
                'Regional': regional,
                'Total 2024': total_2024,
                **{meses_2025[i]: valores_mensais_2025[i] for i in range(12)},
                'Total 2025': total_2025,
                'Real Jan/26': real_jan_26,
                'Meta Jan/26': meta_jan_26,
                'Alcance Meta': alcance_meta,
                'Var 2025/2024': variacao_2024_2025,
                'Var MoM': variacao_mom
            })
        
        return pivot_data
    
    # AGORA CHAMAR A FUNÇÃO PARA CRIAR A TABELA PIVOT
    pivot_data = create_pivot_table(df_tabela, meses_2025)
    
    # Ordenar pivot_data pelo Total 2025 (do maior para o menor)
    df_temp_ordenacao = pd.DataFrame(pivot_data)
    df_temp_ordenacao = df_temp_ordenacao.sort_values('Total 2025', ascending=False)
    pivot_data_ordenada = df_temp_ordenacao.to_dict('records')
    
    # Criar linha de TOTAL (soma de todas as regionais)
    df_total = df_tabela.copy()
    
    # Calcular totais gerais
    total_2024_geral = df_total[df_total['ano'] == '24']['QTDE'].sum()
    total_2025_geral = df_total[df_total['ano'] == '25']['QTDE'].sum()
    
    # Calcular valores mensais gerais para 2025
    valores_mensais_2025_geral = []
    for mes in meses_2025:
        valor = df_total[df_total['mes_ano'] == mes]['QTDE'].sum()
        valores_mensais_2025_geral.append(valor)
    
    # Calcular REAL geral jan/26
    real_jan_26_geral = df_total[df_total['mes_ano'] == 'jan/26']['QTDE'].sum()
    
    # Calcular meta geral jan/26
    meta_jan_26_geral = df_total[df_total['mes_ano'] == 'jan/26']['DESAFIO_QTD'].sum()
    
    # Calcular variações gerais
    variacao_2024_2025_geral = ((total_2025_geral - total_2024_geral) / total_2024_geral * 100) if total_2024_geral > 0 else 0
    
    # Calcular variação MoM geral
    dez_25_geral = df_total[df_total['mes_ano'] == 'dez/25']['QTDE'].sum()
    nov_25_geral = df_total[df_total['mes_ano'] == 'nov/25']['QTDE'].sum()
    variacao_mom_geral = ((dez_25_geral - nov_25_geral) / nov_25_geral * 100) if nov_25_geral > 0 else 0
    
    # Calcular alcance da meta geral
    alcance_meta_geral = (((real_jan_26_geral / meta_jan_26_geral)-1) * 100) if meta_jan_26_geral > 0 else 0
    
    # Adicionar linha de TOTAL no início
    linha_total = {
        'Regional': 'TOTAL',
        'Total 2024': total_2024_geral,
        **{meses_2025[i]: valores_mensais_2025_geral[i] for i in range(12)},
        'Total 2025': total_2025_geral,
        'Real Jan/26': real_jan_26_geral,
        'Meta Jan/26': meta_jan_26_geral,
        'Alcance Meta': alcance_meta_geral,
        'Var 2025/2024': variacao_2024_2025_geral,
        'Var MoM': variacao_mom_geral
    }
    
    # Criar DataFrame final com as regionais ordenadas por Total 2025 (decrescente)
    df_final = pd.DataFrame([linha_total] + pivot_data_ordenada)
    
    # Ordenar colunas
    colunas_ordenadas = ['Regional', 'Total 2024'] + meses_2025 + ['Total 2025', 'Real Jan/26', 'Meta Jan/26', 'Alcance Meta', 'Var 2025/2024', 'Var MoM']
    df_final = df_final[colunas_ordenadas]
    
    # Formatar para exibição
    def formatar_numero(valor):
        if isinstance(valor, (int, float)):
            if valor == int(valor):
                return f'{int(valor):,}'.replace(',', '.')
            else:
                return f'{valor:,.1f}'.replace(',', '.')
        return valor
    
    def formatar_percentual(valor):
        if isinstance(valor, (int, float)):
            return f'{valor:+.1f}%'.replace('.', ',')
        return valor
    
    df_exibicao = df_final.copy()
    for col in df_exibicao.columns:
        if col not in ['Regional', 'Var 2025/2024', 'Var MoM', 'Alcance Meta']:
            df_exibicao[col] = df_exibicao[col].apply(formatar_numero)
        else:
            df_exibicao[col] = df_exibicao[col].apply(formatar_percentual)
    
    # Função para criar tabela HTML estilizada
    def criar_tabela_html(df):
        html = """
        <style>
            .tabela-container-melhorada {
                width: 100%;
                max-height: 650px;
                overflow-y: auto;
                overflow-x: auto;
                border: 2px solid #790E09;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(121, 14, 9, 0.15);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                margin: 20px 0;
                background: white;
            }
            
            .tabela-melhorada {
                width: 100%;
                border-collapse: collapse;
                border-spacing: 0;
                font-size: 13px;
                line-height: 1.5;
            }
            
            .tabela-melhorada thead {
                position: sticky;
                top: 0;
                z-index: 100;
            }
            
            .tabela-melhorada th {
                background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                color: white !important;
                font-weight: 600;
                padding: 14px 10px;
                text-align: center;
                border-bottom: 3px solid #5A0A06;
                border-right: 1px solid rgba(255, 255, 255, 0.15);
                white-space: nowrap;
                font-size: 12px;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                position: relative;
                transition: all 0.2s ease;
            }
            
            .tabela-melhorada th:hover {
                background: linear-gradient(135deg, #8A1F1A 0%, #6B0F0B 100%) !important;
            }
            
            .tabela-melhorada th:first-child {
                border-left: none;
                border-top-left-radius: 8px;
            }
            
            .tabela-melhorada th:last-child {
                border-right: none;
                border-top-right-radius: 8px;
            }
            
            .tabela-melhorada th.col-total-anual {
                background: linear-gradient(135deg, #A23B36 0%, #790E09 100%) !important;
            }
            
            .tabela-melhorada th.col-real-jan26 {
                background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
            }
            
            .tabela-melhorada th.col-meta {
                background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
            }
            
            .tabela-melhorada th.col-alcance,
            .tabela-melhorada th.col-variacao {
                background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
            }
            
            .tabela-melhorada td {
                padding: 12px 10px;
                text-align: center;
                border-bottom: 1px solid #E8E8E8;
                border-right: 1px solid #F0F0F0;
                font-weight: 400;
                transition: all 0.2s ease;
            }
            
            .tabela-melhorada tr:not(.linha-total-melhorada) td:first-child {
                border-left: none;
                text-align: left;
                font-weight: 600;
                color: #333;
                background: linear-gradient(90deg, #fef5f4 0%, white 100%) !important;
                padding-left: 15px;
            }
            
            .tabela-melhorada td:last-child {
                border-right: none;
            }
            
            .linha-total-melhorada {
                background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                color: white !important;
                position: sticky;
                bottom: 0;
                z-index: 50;
                border-top: 2px solid #790E09;
            }
            
            .linha-total-melhorada td {
                background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                color: white !important;
                border-bottom: none;
                font-weight: 700;
                font-size: 14px;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            .linha-total-melhorada td.col-total-anual,
            .linha-total-melhorada td.col-mes,
            .linha-total-melhorada td.col-real-jan26,
            .linha-total-melhorada td.col-meta,
            .linha-total-melhorada td.col-alcance,
            .linha-total-melhorada td.col-variacao {
                background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                color: white !important;
                border-left: none !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding-left: 10px !important;
            }
            
            .linha-total-melhorada td.col-alcance::before,
            .linha-total-melhorada td.col-variacao::before,
            .linha-total-melhorada td.percentual-positivo::before,
            .linha-total-melhorada td.percentual-negativo::before,
            .linha-total-melhorada td.percentual-neutro::before {
                content: "" !important;
            }
            
            .linha-total-melhorada td:first-child {
                font-weight: 800;
                background: linear-gradient(135deg, #3D0704 0%, #5A0A06 100%) !important;
            }
            
            .linha-regional-melhorada:nth-child(even) {
                background-color: #FFF9F8 !important;
            }
            
            .linha-regional-melhorada:nth-child(odd) {
                background-color: white !important;
            }
            
            .linha-regional-melhorada:hover {
                background-color: #FFEBEE !important;
                box-shadow: inset 0 0 0 1px #FFCDD2;
                transform: translateY(-1px);
            }
            
            .linha-regional-melhorada td.col-total-anual {
                background: linear-gradient(135deg, #FDE8E6 0%, #FCE4E2 100%) !important;
                color: #790E09 !important;
                font-weight: 600;
                border-left: 2px solid #A23B36;
                border-right: 2px solid #A23B36;
            }
            
            .linha-regional-melhorada td.col-mes {
                background-color: #F9F0EF !important;
                color: #333 !important;
                border-left: 1px solid #E8D6D5;
                border-right: 1px solid #E8D6D5;
            }
            
            .linha-regional-melhorada td.col-real-jan26 {
                background: linear-gradient(135deg, #F1F3F5 0%, #E9ECEF 100%) !important;
                color: #495057 !important;
                font-weight: 600;
                border-left: 2px solid #ADB5BD;
                border-right: 2px solid #ADB5BD;
            }
            
            .linha-regional-melhorada td.col-meta {
                background: linear-gradient(135deg, #FFEBEE 0%, #FFE5E8 100%) !important;
                color: #B71C1C !important;
                font-weight: 600;
                border-left: 2px solid #F44336;
                border-right: 2px solid #F44336;
            }
            
            .linha-regional-melhorada td.col-alcance,
            .linha-regional-melhorada td.col-variacao {
                background-color: #F8F9FA !important;
            }
            
            .linha-regional-melhorada td.col-alcance.percentual-positivo,
            .linha-regional-melhorada td.col-variacao.percentual-positivo {
                color: #1B5E20 !important;
                background: linear-gradient(135deg, #E8F5E9 0%, #E6F4E7 100%) !important;
                font-weight: 700;
                position: relative;
                padding-left: 28px !important;
                border-left: 3px solid #4CAF50 !important;
                border-right: 1px solid #C8E6C9 !important;
            }
            
            .linha-regional-melhorada td.col-alcance.percentual-positivo::before,
            .linha-regional-melhorada td.col-variacao.percentual-positivo::before {
                content: "▲";
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 11px;
                font-weight: 900;
                color: #2E7D32;
            }
            
            .linha-regional-melhorada td.col-alcance.percentual-negativo,
            .linha-regional-melhorada td.col-variacao.percentual-negativo {
                color: #C62828 !important;
                background: linear-gradient(135deg, #FFEBEE 0%, #FFE5E8 100%) !important;
                font-weight: 700;
                position: relative;
                padding-left: 28px !important;
                border-left: 3px solid #F44336 !important;
                border-right: 1px solid #FFCDD2 !important;
            }
            
            .linha-regional-melhorada td.col-alcance.percentual-negativo::before,
            .linha-regional-melhorada td.col-variacao.percentual-negativo::before {
                content: "▼";
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 11px;
                font-weight: 900;
                color: #C62828;
            }
            
            .linha-regional-melhorada td.col-alcance.percentual-neutro,
            .linha-regional-melhorada td.col-variacao.percentual-neutro {
                color: #666666 !important;
                background: #F8F9FA !important;
                font-weight: 500;
            }
            
            .linha-regional-melhorada td:hover {
                transform: scale(1.02);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                z-index: 10;
                position: relative;
            }
            
            .linha-regional-melhorada td.performance-excelente {
                animation: pulse-green 2s infinite;
            }
            
            .linha-regional-melhorada td.performance-critica {
                animation: pulse-red 2s infinite;
            }
            
            @keyframes pulse-green {
                0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
                100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
            }
            
            @keyframes pulse-red {
                0% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }
                100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
            }
            
            .tabela-container-melhorada::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            .tabela-container-melhorada::-webkit-scrollbar-track {
                background: #F5F5F5;
                border-radius: 10px;
            }
            
            .tabela-container-melhorada::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #A23B36 0%, #790E09 100%);
                border-radius: 10px;
                border: 2px solid #F5F5F5;
            }
            
            .tabela-container-melhorada::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            }
            
            .tabela-container-melhorada::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 20px;
                background: linear-gradient(to bottom, transparent, rgba(121, 14, 9, 0.05));
                pointer-events: none;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        </style>
        
        <div class="tabela-container-melhorada">
        <table class="tabela-melhorada">
        <thead>
            <tr>
        """
        
        for i, col in enumerate(df.columns):
            classe = ""
            if col == 'Regional':
                classe = ""
            elif col in ['Total 2024', 'Total 2025']:
                classe = "col-total-anual"
            elif col in meses_2025:
                classe = "col-mes"
            elif col == 'Real Jan/26':
                classe = "col-real-jan26"
            elif 'Meta' in col and 'Alcance' not in col:
                classe = "col-meta"
            elif 'Alcance' in col:
                classe = "col-alcance"
            elif 'Var' in col:
                classe = "col-variacao"
            
            html += f'<th class="{classe}">{col}</th>'
        
        html += "</tr></thead><tbody>"
        
        for idx, row in df.iterrows():
            is_total = row['Regional'] == 'TOTAL'
            classe_linha = "linha-total-melhorada" if is_total else "linha-regional-melhorada"
            html += f'<tr class="{classe_linha}">'
            
            for col in df.columns:
                valor = row[col]
                classe_celula = ""
                
                if is_total:
                    if col == 'Regional':
                        classe_celula = ""
                    elif col in ['Total 2024', 'Total 2025']:
                        classe_celula = "col-total-anual"
                    elif col in meses_2025:
                        classe_celula = "col-mes"
                    elif col == 'Real Jan/26':
                        classe_celula = "col-real-jan26"
                    elif 'Meta' in col and 'Alcance' not in col:
                        classe_celula = "col-meta"
                    elif 'Alcance' in col:
                        classe_celula = "col-alcance"
                    elif 'Var' in col:
                        classe_celula = "col-variacao"
                else:
                    if col == 'Regional':
                        classe_celula = ""
                    elif col in ['Total 2024', 'Total 2025']:
                        classe_celula = "col-total-anual"
                    elif col in meses_2025:
                        classe_celula = "col-mes"
                    elif col == 'Real Jan/26':
                        classe_celula = "col-real-jan26"
                    elif 'Meta' in col and 'Alcance' not in col:
                        classe_celula = "col-meta"
                    elif 'Alcance' in col or 'Var' in col:
                        try:
                            valor_limpo = str(valor).replace('%', '').replace('+', '').replace(',', '.')
                            num_valor = float(valor_limpo)
                            
                            if num_valor > 0:
                                if 'Alcance' in col:
                                    classe_celula = "col-alcance percentual-positivo"
                                else:
                                    classe_celula = "col-variacao percentual-positivo"
                                
                                if num_valor > 50:
                                    classe_celula += " performance-excelente"
                            elif num_valor < 0:
                                if 'Alcance' in col:
                                    classe_celula = "col-alcance percentual-negativo"
                                else:
                                    classe_celula = "col-variacao percentual-negativo"
                                
                                if num_valor < -30:
                                    classe_celula += " performance-critica"
                            else:
                                if 'Alcance' in col:
                                    classe_celula = "col-alcance percentual-neutro"
                                else:
                                    classe_celula = "col-variacao percentual-neutro"
                        except:
                            if 'Alcance' in col:
                                classe_celula = "col-alcance"
                            else:
                                classe_celula = "col-variacao"
                
                html += f'<td class="{classe_celula}">{valor}</td>'
            
            html += "</tr>"
        
        html += "</tbody></table></div>"
        return html
    
    # Exibir tabela
    st.markdown(criar_tabela_html(df_exibicao), unsafe_allow_html=True)
    
    # Botões de exportação
    col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
    
    with col_exp1:
        def exportar_excel_tabela(df_numerico):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_numerico.to_excel(writer, index=False, sheet_name='Tabela_Dinamica')
                
                workbook = writer.book
                worksheet = writer.sheets['Tabela_Dinamica']
                
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#FF2800',
                    'font_color': 'white',
                    'align': 'center',
                    'border': 1,
                    'font_size': 10
                })
                
                number_format = workbook.add_format({
                    'num_format': '#,##0',
                    'align': 'center'
                })
                
                percent_format = workbook.add_format({
                    'num_format': '0.0%',
                    'align': 'center'
                })
                
                for col_num, col_name in enumerate(df_numerico.columns):
                    worksheet.write(0, col_num, col_name, header_format)
                    
                    if col_name in ['Var 2025/2024', 'Var MoM', 'Alcance Meta']:
                        cell_format = percent_format
                    else:
                        cell_format = number_format
                    
                    for row_num in range(1, len(df_numerico) + 1):
                        value = df_numerico.iloc[row_num-1, col_num]
                        if pd.isna(value):
                            worksheet.write(row_num, col_num, '')
                        elif col_name == 'Regional':
                            worksheet.write(row_num, col_num, value)
                        else:
                            worksheet.write(row_num, col_num, value, cell_format)
                
                for i, col in enumerate(df_numerico.columns):
                    column_width = max(df_numerico[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, min(column_width, 20))
            
            return output.getvalue()
    
        excel_data = exportar_excel_tabela(df_final)
        st.download_button(
            label="📥 Exportar Excel",
            data=excel_data,
            file_name="tabela_dinamica.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )
    
    with col_exp2:
        @st.cache_data
        def convert_to_csv(df):
            return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
    
        csv_data = convert_to_csv(df_final)
        st.download_button(
            label="📄 Exportar CSV",
            data=csv_data,
            file_name="tabela_dinamica.csv",
            mime="text/csv",
            width='stretch'
        )
    
    with col_exp3:
        st.caption(f"""
        **Resumo:** {len(pivot_data)} Regionais | 
        **Total 2024:** {formatar_numero(total_2024_geral)} | 
        **Total 2025:** {formatar_numero(total_2025_geral)} | 
        **Crescimento:** {formatar_percentual(variacao_2024_2025_geral)} | 
        **Alcance Meta:** {formatar_percentual(alcance_meta_geral)}
        """)
    
    # Análise detalhada
    with st.expander("🔍 Ver dados para análise detalhada", expanded=False):
        df_analise = pd.DataFrame([linha_total] + pivot_data)
        df_analise = df_analise[colunas_ordenadas]
        
        st.write("**Principais Insights:**")
        
        col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)
        
        with col_insight1:
            df_crescimento = pd.DataFrame(pivot_data)
            if not df_crescimento.empty and len(df_crescimento) > 0:
                maior_cresc_idx = df_crescimento['Var 2025/2024'].idxmax()
                maior_cresc = df_crescimento.loc[maior_cresc_idx]
                st.metric("Maior Crescimento", 
                         maior_cresc['Regional'], 
                         f"{maior_cresc['Var 2025/2024']:+.1f}%")
        
        with col_insight2:
            if not df_crescimento.empty and len(df_crescimento) > 0:
                maior_volume_idx = df_crescimento['Total 2025'].idxmax()
                maior_volume = df_crescimento.loc[maior_volume_idx]
                st.metric("Maior Volume 2025", 
                         maior_volume['Regional'], 
                         f"{formatar_numero(maior_volume['Total 2025'])}")
        
        with col_insight3:
            if not df_crescimento.empty and len(df_crescimento) > 0:
                media_alcance = df_crescimento['Alcance Meta'].mean()
                st.metric("Média Alcance Meta", 
                         f"{media_alcance:.1f}%", 
                         None)
        
        with col_insight4:
            if not df_crescimento.empty and len(df_crescimento) > 0:
                media_cresc = df_crescimento['Var 2025/2024'].mean()
                st.metric("Crescimento Médio", 
                         f"{media_cresc:+.1f}%", 
                         None)
        
        # Gráfico comparativo
        st.write("**Comparativo entre Regionais (Top 10 por Volume 2025):**")
        
        if not df_crescimento.empty and len(df_crescimento) > 0:
            df_top10 = df_crescimento.nlargest(10, 'Total 2025')
            
            fig_comparativo = px.bar(
                df_top10,
                y='Regional',
                x='Total 2025',
                orientation='h',
                title='Top 10 Regionais por Volume 2025',
                color='Total 2025',
                color_continuous_scale='Reds',
                text='Total 2025'
            )
            
            fig_comparativo.update_traces(
                texttemplate='%{x:,.0f}',
                textposition='outside'
            )
            
            fig_comparativo.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Volume 2025",
                yaxis_title="",
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_comparativo, width='stretch')

# =========================
# ABA 2: DESATIVADOS
# =========================
with tab2:
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📉</span>
            DESATIVADOS
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE DESATIVAÇÕES E CHURN
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Container informativo
    st.info("""
    **🚨 ÁREA EM DESENVOLVIMENTO**  
    Esta seção está sendo construída para análise de desativações e churn.  
    Em breve você terá acesso a:
    - Volume de desativações por canal
    - Taxa de churn e retenção
    - Análise de motivos de cancelamento
    - Métricas de recuperação (win-back)
    """)
    
    # Placeholder para conteúdo futuro
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                border-radius: 12px; border: 2px dashed #E9ECEF; margin: 30px 0;">
        <div style="font-size: 64px; color: #790E09; margin-bottom: 20px;">📉</div>
        <h3 style="color: #333333; margin-bottom: 10px;">
            Dashboard de Desativações
        </h3>
        <p style="color: #666666; max-width: 600px; margin: 0 auto 20px;">
            Esta seção está em construção. Aqui você poderá analisar desativações, 
            calcular taxas de churn e monitorar estratégias de retenção.
        </p>
        <div style="display: inline-flex; gap: 10px; margin-top: 20px;">
            <span style="background: #790E09; color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                Total Desativados
            </span>
            <span style="background: #5A0A06; color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                Taxa de Churn
            </span>
            <span style="background: #333333; color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                Receita Perdida
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos de exemplo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card-title">📊 Evolução de Desativações (Exemplo)</div>', unsafe_allow_html=True)
        
        dados_exemplo = pd.DataFrame({
            'Mês': ['Jan/24', 'Fev/24', 'Mar/24', 'Abr/24', 'Mai/24', 'Jun/24', 'Jul/24', 'Ago/24', 'Set/24', 'Out/24', 'Nov/24', 'Dez/24'],
            'Desativações': [1250, 1180, 1320, 1245, 1190, 1150, 1280, 1340, 1270, 1220, 1180, 1247],
            'Meta Máxima': [1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dados_exemplo['Mês'],
            y=dados_exemplo['Desativações'],
            mode='lines+markers',
            name='Desativações',
            line=dict(color='#FF2800', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=dados_exemplo['Mês'],
            y=dados_exemplo['Meta Máxima'],
            mode='lines',
            name='Meta',
            line=dict(color='#5A6268', width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="card-title">📈 Distribuição por Canal (Exemplo)</div>', unsafe_allow_html=True)
        
        dados_canais = pd.DataFrame({
            'Canal': ['Televendas Ativo', 'Televendas Receptivo', 'S2S+DAC', 'Inside Sales', 'E-commerce', 'Outros'],
            'Desativações': [420, 380, 210, 185, 32, 20],
            'Percentual': [33.7, 30.5, 16.8, 14.8, 2.6, 1.6]
        })
        
        fig = px.bar(
            dados_canais, 
            x='Desativações', 
            y='Canal',
            orientation='h',
            text='Desativações',
            color='Desativações',
            color_continuous_scale='Reds'
        )
        
        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            marker=dict(line=dict(width=0))
        )
        
        fig.update_layout(
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            xaxis_title="",
            yaxis_title="",
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de exemplo
    st.markdown('<div class="card-title">📋 Resumo por Regional (Exemplo)</div>', unsafe_allow_html=True)
    
    tabela_exemplo = pd.DataFrame({
        'Regional': ['SP Capital', 'RJ Capital', 'MG Interior', 'SP Interior', 'RS Capital', 'PR Capital'],
        'Desativados': [280, 195, 165, 142, 98, 87],
        'Variação MoM': [-12.5, -8.7, -15.2, -10.3, -5.6, -7.9],
        'Taxa Churn': [3.2, 2.8, 2.5, 2.1, 1.8, 1.6],
        'Receita Perdida (K)': [98.5, 68.2, 57.8, 49.5, 34.2, 30.5]
    })
    
    st.dataframe(
        tabela_exemplo.style.format({
            'Desativados': '{:,.0f}',
            'Variação MoM': '{:+.1f}%',
            'Taxa Churn': '{:.1f}%',
            'Receita Perdida (K)': 'R$ {:,.1f}K'
        }),
        width='stretch'
    )
    
    # Nota de desenvolvimento
    st.markdown("""
    <div style="background: #F8F9FA; padding: 15px; border-radius: 8px; border-left: 4px solid #790E09; margin-top: 20px;">
        <div style="display: flex; align-items: flex-start; gap: 10px;">
            <span style="color: #790E09; font-size: 20px;">🔨</span>
            <div>
                <strong style="color: #333333;">Próximas etapas de desenvolvimento:</strong>
                <ul style="color: #666666; margin-top: 5px; padding-left: 20px;">
                    <li>Integração com base de dados de desativações</li>
                    <li>Cálculo automático de taxa de churn</li>
                    <li>Análise de motivos de cancelamento</li>
                    <li>Dashboard de recuperação (win-back)</li>
                    <li>Alertas de churn elevado</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ABA 3: PEDIDOS
# =========================
with tab3:
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📋</span>
            PEDIDOS
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE PEDIDOS E CONVERSÃO
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Funcionalidades planejadas:**
        - Volume de pedidos por canal
        - Taxa de conversão
        - Status dos pedidos
        - Tempo médio de processamento
        """)
    
    with col2:
        st.info("""
        **Métricas principais:**
        - Pedidos recebidos
        - Pedidos processados
        - Pedidos pendentes
        - Taxa de cancelamento
        """)
    
    # Exemplo de visualização
    st.subheader("📊 Exemplo de Visualização")
    
    dados_exemplo = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Pedidos Recebidos': [150, 180, 220, 190, 240, 210],
        'Pedidos Processados': [140, 170, 200, 180, 220, 200]
    })
    
    fig_exemplo = px.bar(dados_exemplo, x='Mês', y=['Pedidos Recebidos', 'Pedidos Processados'],
                        title="Volume de Pedidos (Exemplo)",
                        barmode='group',
                        color_discrete_sequence=['#FF2800', '#555555'])
    
    st.plotly_chart(fig_exemplo, width='stretch')

# =========================
# ABA 4: LIGAÇÕES
# =========================
with tab4:
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📞</span>
            LIGAÇÕES
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE LIGAÇÕES E CONTATOS
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================
    # CARREGAR DADOS DE LIGAÇÕES
    # =========================
    @st.cache_data
    def load_ligacoes_data_lig():
        """Carrega dados de ligações com tratamento especial"""
        try:
            ligacoes_path = "televendas_ligacoes.xlsx"
            df_ligacoes_lig = pd.read_excel(ligacoes_path)
            
            # Filtrar apenas TIPO_DADOS = REAL
            df_ligacoes_lig = df_ligacoes_lig[df_ligacoes_lig['TIPO_DADOS'] == 'REAL']
            
            # Criar coluna TIPO_CHAMADA baseada na coluna TELEFONE
            def classificar_tipo_chamada(telefone):
                if pd.isna(telefone):
                    return "DEMAIS"
                
                telefone_str = str(telefone)
                
                # Verificar se contém os números especificados
                if '0960' in telefone_str or '8449' in telefone_str:
                    return "Click to Call"
                else:
                    return "DEMAIS"
            
            df_ligacoes_lig['TIPO_CHAMADA'] = df_ligacoes_lig['TELEFONE'].apply(classificar_tipo_chamada)
            
            # Converter PERIODO para datetime
            df_ligacoes_lig['DATA_DT_LIG'] = pd.to_datetime(df_ligacoes_lig['PERIODO'], errors='coerce')
            
            # Criar coluna mes_ano no formato mm/aa (ex: jan/25)
            def formatar_mes_ano_lig(dt):
                try:
                    # Mapeamento de meses
                    meses_pt = {
                        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
                        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
                    }
                    mes = meses_pt.get(dt.month, 'jan')
                    ano = dt.strftime('%y')
                    return f"{mes}/{ano}"
                except:
                    return "n/a"
            
            df_ligacoes_lig['mes_ano_lig'] = df_ligacoes_lig['DATA_DT_LIG'].apply(formatar_mes_ano_lig)
            
            # Criar coluna ano para agrupamento
            df_ligacoes_lig['ano_lig'] = df_ligacoes_lig['DATA_DT_LIG'].dt.strftime('%y')
            
            # Tratar valores nulos
            df_ligacoes_lig['QTDE_LIG'] = pd.to_numeric(df_ligacoes_lig['QTDE'], errors='coerce').fillna(0)
            
            return df_ligacoes_lig
        except Exception as e:
            st.error(f"Erro ao carregar dados de ligações: {str(e)}")
            return pd.DataFrame()
    
    # Carregar dados
    df_lig_original = load_ligacoes_data_lig()
    
    if df_lig_original.empty:
        st.warning("Não foi possível carregar os dados de ligações. Verifique o arquivo.")
        st.stop()
    
    # =========================
    # FILTROS PARA TABELA LIGAÇÕES
    # =========================
    
    # Container para filtros
    with st.container():
        col_filtro_t1_lig, col_filtro_t2_lig, col_filtro_t3_lig, col_filtro_t4_lig = st.columns(4)
        
        with col_filtro_t1_lig:
            canal_tabela_lig = st.multiselect(
                "Filtrar por Canal:",
                options=["Todos"] + sorted(df_lig_original['CANAL_PLAN'].unique()),
                default=["Todos"],
                key="filtro_canal_tabela_lig"
            )
        
        with col_filtro_t2_lig:
            regional_tabela_lig = st.multiselect(
                "Filtrar por Regional:",
                options=["Todos"] + sorted(df_lig_original['REGIONAL'].unique()),
                default=["Todos"],
                key="filtro_regional_tabela_lig"
            )
        
        with col_filtro_t3_lig:
            indicador_tabela_lig = st.multiselect(
                "Filtrar por Indicador:",
                options=["Todos"] + sorted(df_lig_original['INDICADOR'].unique()),
                default=["Todos"],
                key="filtro_indicador_tabela_lig"
            )
        
        with col_filtro_t4_lig:
            tipo_chamada_opcoes = sorted(df_lig_original['TIPO_CHAMADA'].unique())
            tipo_chamada_tabela_lig = st.multiselect(
                "Filtrar por Tipo de Chamada:",
                options=["Todos"] + tipo_chamada_opcoes,
                default=["Todos"],
                key="filtro_tipo_chamada_tabela_lig"
            )
    
    # Aplicar filtros à tabela
    df_lig_tabela = df_lig_original.copy()
    
    if "Todos" not in canal_tabela_lig:
        df_lig_tabela = df_lig_tabela[df_lig_tabela['CANAL_PLAN'].isin(canal_tabela_lig)]
    
    if "Todos" not in regional_tabela_lig:
        df_lig_tabela = df_lig_tabela[df_lig_tabela['REGIONAL'].isin(regional_tabela_lig)]
    
    if "Todos" not in indicador_tabela_lig:
        df_lig_tabela = df_lig_tabela[df_lig_tabela['INDICADOR'].isin(indicador_tabela_lig)]
    
    if "Todos" not in tipo_chamada_tabela_lig:
        df_lig_tabela = df_lig_tabela[df_lig_tabela['TIPO_CHAMADA'].isin(tipo_chamada_tabela_lig)]
    
    # =========================
    # IDENTIFICAR MÊS ATUAL E CRIAR FILTRO
    # =========================
    # Identificar mês atual do sistema
    from datetime import datetime
    mes_atual_num = datetime.now().month
    ano_atual_2dig = datetime.now().strftime('%y')
    
    # Mapeamento de meses
    meses_pt_map = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }
    mes_atual_str = meses_pt_map.get(mes_atual_num, 'jan')
    mes_ano_atual = f"{mes_atual_str}/{ano_atual_2dig}"
    
    # Container para seleção do mês específico
    col_filtro_mes1, col_filtro_mes2, col_filtro_mes3 = st.columns([2, 2, 4])
    
    with col_filtro_mes1:
        # Obter lista de meses disponíveis nos dados
        meses_disponiveis = sorted(df_lig_tabela['mes_ano_lig'].unique())
        
        # Garantir que o mês atual esteja na lista (se não estiver, adicionar)
        if mes_ano_atual not in meses_disponiveis:
            meses_disponiveis.append(mes_ano_atual)
        
        # Seletor de mês
        mes_selecionado = st.selectbox(
            "📅 Selecione o mês para análise:",
            options=meses_disponiveis,
            index=meses_disponiveis.index(mes_ano_atual) if mes_ano_atual in meses_disponiveis else 0,
            help="As métricas abaixo serão calculadas apenas para o mês selecionado",
            key="filtro_mes_especifico_ligacoes"
        )
    
    with col_filtro_mes2:
        # Calcular o mês anterior para referência
        try:
            mes_num_anterior = mes_atual_num - 1 if mes_atual_num > 1 else 12
            ano_anterior = ano_atual_2dig if mes_atual_num > 1 else str(int(ano_atual_2dig) - 1).zfill(2)
            mes_anterior_str = meses_pt_map.get(mes_num_anterior, 'dez')
            mes_ano_anterior = f"{mes_anterior_str}/{ano_anterior}"
        except:
            mes_ano_anterior = "n/a"
        
        # Substituir o st.info() pelo mesmo estilo do exemplo
        st.markdown(f"""
            <div style="background: linear-gradient(90deg, #F8F0F0, #FFFFFF); 
                        padding: 12px 16px; border-radius: 8px; border-left: 4px solid #790E09;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 14px; color: #333333; font-weight: 600;">
                        Mês selecionado:
                    </span>
                    <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                background: #F8F0F0; padding: 4px 12px; border-radius: 20px;">
                        {mes_selecionado}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # =========================
    # FILTRAR DADOS PARA O MÊS SELECIONADO
    # =========================
    # Filtrar dados apenas para o mês selecionado
    df_lig_mes_selecionado = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == mes_selecionado].copy()
    
    # Calcular dados do mês anterior para comparação (se disponível)
    df_lig_mes_anterior = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == mes_ano_anterior].copy()
    
    # =========================
    # CALCULAR KPIs DO MÊS SELECIONADO
    # =========================
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        total_ligacoes_mes = df_lig_mes_selecionado['QTDE_LIG'].sum()
        
        # Calcular variação vs mês anterior
        total_ligacoes_mes_anterior = df_lig_mes_anterior['QTDE_LIG'].sum() if not df_lig_mes_anterior.empty else 0
        
        if total_ligacoes_mes_anterior > 0:
            variacao_mes = ((total_ligacoes_mes - total_ligacoes_mes_anterior) / total_ligacoes_mes_anterior * 100)
            delta_text = f"{variacao_mes:+.1f}% vs {mes_ano_anterior}"
        else:
            delta_text = "Sem dados mês anterior"
        
        st.metric(
            label=f"Total Ligações ({mes_selecionado})",
            value=f"{total_ligacoes_mes:,.0f}".replace(",", "."),
            delta=delta_text,
            help=f"Total de ligações apenas para {mes_selecionado}"
        )
    
    with col_kpi2:
        click_to_call_mes = df_lig_mes_selecionado[df_lig_mes_selecionado['TIPO_CHAMADA'] == 'Click to Call']['QTDE_LIG'].sum()
        percent_click_mes = (click_to_call_mes / total_ligacoes_mes * 100) if total_ligacoes_mes > 0 else 0
        
        # Calcular variação vs mês anterior
        click_to_call_mes_anterior = df_lig_mes_anterior[df_lig_mes_anterior['TIPO_CHAMADA'] == 'Click to Call']['QTDE_LIG'].sum() if not df_lig_mes_anterior.empty else 0
        
        if click_to_call_mes_anterior > 0:
            variacao_click = ((click_to_call_mes - click_to_call_mes_anterior) / click_to_call_mes_anterior * 100)
            delta_text_click = f"{variacao_click:+.1f}% vs {mes_ano_anterior}"
        else:
            delta_text_click = f"{percent_click_mes:.1f}% do total"
        
        st.metric(
            label=f"Click to Call ({mes_selecionado})",
            value=f"{click_to_call_mes:,.0f}".replace(",", "."),
            delta=delta_text_click
        )
    
    with col_kpi3:
        demais_mes = df_lig_mes_selecionado[df_lig_mes_selecionado['TIPO_CHAMADA'] == 'DEMAIS']['QTDE_LIG'].sum()
        percent_demais_mes = (demais_mes / total_ligacoes_mes * 100) if total_ligacoes_mes > 0 else 0
        
        # Calcular variação vs mês anterior
        demais_mes_anterior = df_lig_mes_anterior[df_lig_mes_anterior['TIPO_CHAMADA'] == 'DEMAIS']['QTDE_LIG'].sum() if not df_lig_mes_anterior.empty else 0
        
        if demais_mes_anterior > 0:
            variacao_demais = ((demais_mes - demais_mes_anterior) / demais_mes_anterior * 100)
            delta_text_demais = f"{variacao_demais:+.1f}% vs {mes_ano_anterior}"
        else:
            delta_text_demais = f"{percent_demais_mes:.1f}% do total"
        
        st.metric(
            label=f"Demais Chamadas ({mes_selecionado})",
            value=f"{demais_mes:,.0f}".replace(",", "."),
            delta=delta_text_demais
        )
    
    with col_kpi4:
        regionais_ativas_mes = df_lig_mes_selecionado['REGIONAL'].nunique()
        regionais_ativas_mes_anterior = df_lig_mes_anterior['REGIONAL'].nunique() if not df_lig_mes_anterior.empty else 0
        
        if regionais_ativas_mes_anterior > 0:
            variacao_reg = regionais_ativas_mes - regionais_ativas_mes_anterior
            delta_text_reg = f"{variacao_reg:+d} vs {mes_ano_anterior}"
        else:
            delta_text_reg = f"{regionais_ativas_mes} regionais ativas"
        
        st.metric(
            label=f"Regionais Ativas ({mes_selecionado})",
            value=regionais_ativas_mes,
            delta=delta_text_reg,
            help=f"Número de regionais com atividade em {mes_selecionado}"
        )
    
    # =========================
    # RESUMO DA DISTRIBUIÇÃO (MÊS SELECIONADO)
    # =========================
    st.markdown("---")
  
    # Criar DataFrame para distribuição do mês selecionado
    df_distribuicao_mes = df_lig_mes_selecionado.groupby('TIPO_CHAMADA')['QTDE_LIG'].sum().reset_index()
    df_distribuicao_mes['Percentual'] = (df_distribuicao_mes['QTDE_LIG'] / df_distribuicao_mes['QTDE_LIG'].sum() * 100).round(1) if df_distribuicao_mes['QTDE_LIG'].sum() > 0 else 0
    
    col_dist1, col_dist2, col_dist3 = st.columns([2, 1, 1])
    
    with col_dist1:
        # Gráfico de pizza do mês selecionado
        if not df_distribuicao_mes.empty:
            fig_pizza_mes = px.pie(
                df_distribuicao_mes,
                values='QTDE_LIG',
                names='TIPO_CHAMADA',
                title=f'Total de Chamadas - {mes_selecionado}',
                color='TIPO_CHAMADA',
                color_discrete_map={
                    'Click to Call': '#FF2800',
                    'DEMAIS': '#790E09'
                },
                hole=0.4
            )
            fig_pizza_mes.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>Percentual: %{percent}"
            )
            fig_pizza_mes.update_layout(
                height=300,
                showlegend=True,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_pizza_mes, use_container_width=True)
    
    with col_dist2:
        st.markdown("**📈 Resumo Quantitativo:**")
        for _, row in df_distribuicao_mes.iterrows():
            st.markdown(f"""
                <div style="background: {'#FFEBEE' if row['TIPO_CHAMADA'] == 'Click to Call' else '#F8F9FA'}; 
                            padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {'#FF2800' if row['TIPO_CHAMADA'] == 'Click to Call' else '#790E09'};">
                    <div style="font-size: 13px; font-weight: 600; color: #333333;">{row['TIPO_CHAMADA']}</div>
                    <div style="font-size: 16px; font-weight: 700; color: {'#FF2800' if row['TIPO_CHAMADA'] == 'Click to Call' else '#790E09'};">
                        {row['QTDE_LIG']:,.0f}
                    </div>
                    <div style="font-size: 12px; color: #666666;">{row['Percentual']}% do total</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col_dist3:
        st.markdown("**ℹ️ Informações:**")
        st.info(f"""
        **Período Analisado:**
        - **Mês:** {mes_selecionado}
        - **Mês anterior (referência):** {mes_ano_anterior}
        
        **Classificação:**
        - **Click to Call**: Ligações contendo '0960' ou '8449' no telefone
        - **DEMAIS**: Todas as outras ligações
        """)
        
         
    # =========================
    # DEFINIR ORDEM DOS MESES
    # =========================
    meses_ordem_lig = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    meses_2025_lig = [f'{mes}/25' for mes in meses_ordem_lig]
    
    # =========================
    # FUNÇÃO PARA CRIAR TABELA PIVOT DINÂMICA
    # =========================
    def create_pivot_table_lig(df_tabela_lig, meses_2025_lig):
        """
        Função para criar tabela pivot dinâmica para ligações
        ATENÇÃO: SEM CACHE para atualizar com filtros
        """
        pivot_data_lig = []
        regionais_lig = sorted(df_tabela_lig['REGIONAL'].unique())
        
        for regional_lig in regionais_lig:
            df_regional_lig = df_tabela_lig[df_tabela_lig['REGIONAL'] == regional_lig]
            
            # Calcular totais por ano
            total_2024_lig = df_regional_lig[df_regional_lig['ano_lig'] == '24']['QTDE_LIG'].sum()
            total_2025_lig = df_regional_lig[df_regional_lig['ano_lig'] == '25']['QTDE_LIG'].sum()
            
            # Calcular valores mensais para 2025
            valores_mensais_2025_lig = []
            for mes_lig in meses_2025_lig:
                valor_lig = df_regional_lig[df_regional_lig['mes_ano_lig'] == mes_lig]['QTDE_LIG'].sum()
                valores_mensais_2025_lig.append(valor_lig)
            
            # Calcular valor REAL de jan/26 (se existir)
            real_jan_26_lig = df_regional_lig[df_regional_lig['mes_ano_lig'] == 'jan/26']['QTDE_LIG'].sum()
            
            # Calcular variações
            variacao_2024_2025_lig = ((total_2025_lig - total_2024_lig) / total_2024_lig * 100) if total_2024_lig > 0 else 0
            
            # Calcular variação MoM (dez/25 vs nov/25)
            dez_25_lig = df_regional_lig[df_regional_lig['mes_ano_lig'] == 'dez/25']['QTDE_LIG'].sum()
            nov_25_lig = df_regional_lig[df_regional_lig['mes_ano_lig'] == 'nov/25']['QTDE_LIG'].sum()
            variacao_mom_lig = ((dez_25_lig - nov_25_lig) / nov_25_lig * 100) if nov_25_lig > 0 else 0
            
            pivot_data_lig.append({
                'Regional': regional_lig,
                'Total 2024': total_2024_lig,
                **{meses_2025_lig[i]: valores_mensais_2025_lig[i] for i in range(12)},
                'Total 2025': total_2025_lig,
                'Real Jan/26': real_jan_26_lig,
                'Var 2025/2024': variacao_2024_2025_lig,
                'Var MoM': variacao_mom_lig
            })
        
        return pivot_data_lig
    
    # =========================
    # CRIAR TABELA PIVOT DINÂMICA
    # =========================
    st.markdown("---")
    st.markdown("""
        <div class="section-title" style="margin-bottom: 15px;">
            <span style="background: linear-gradient(105deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📊</span>
            LIGAÇÕES POR REGIONAL
            
        </div>
    """, unsafe_allow_html=True)
    
    # Criar pivot com dados filtrados
    pivot_data_lig = create_pivot_table_lig(df_lig_tabela, meses_2025_lig)
    
    if not pivot_data_lig:
        st.warning("Nenhum dado encontrado com os filtros selecionados para a tabela.")
    else:
        # Ordenar pivot_data pelo Total 2025 (do maior para o menor)
        df_temp_ordenacao_lig = pd.DataFrame(pivot_data_lig)
        df_temp_ordenacao_lig = df_temp_ordenacao_lig.sort_values('Total 2025', ascending=False)
        pivot_data_ordenada_lig = df_temp_ordenacao_lig.to_dict('records')
        
        # =========================
        # CRIAR LINHA DE TOTAL
        # =========================
        # Calcular totais gerais
        total_2024_geral_lig = df_lig_tabela[df_lig_tabela['ano_lig'] == '24']['QTDE_LIG'].sum()
        total_2025_geral_lig = df_lig_tabela[df_lig_tabela['ano_lig'] == '25']['QTDE_LIG'].sum()
        
        # Calcular valores mensais gerais para 2025
        valores_mensais_2025_geral_lig = []
        for mes_lig in meses_2025_lig:
            valor_lig = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == mes_lig]['QTDE_LIG'].sum()
            valores_mensais_2025_geral_lig.append(valor_lig)
        
        # Calcular REAL geral jan/26
        real_jan_26_geral_lig = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == 'jan/26']['QTDE_LIG'].sum()
        
        # Calcular variações gerais
        variacao_2024_2025_geral_lig = ((total_2025_geral_lig - total_2024_geral_lig) / total_2024_geral_lig * 100) if total_2024_geral_lig > 0 else 0
        
        # Calcular variação MoM geral
        dez_25_geral_lig = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == 'dez/25']['QTDE_LIG'].sum()
        nov_25_geral_lig = df_lig_tabela[df_lig_tabela['mes_ano_lig'] == 'nov/25']['QTDE_LIG'].sum()
        variacao_mom_geral_lig = ((dez_25_geral_lig - nov_25_geral_lig) / nov_25_geral_lig * 100) if nov_25_geral_lig > 0 else 0
        
        # Adicionar linha de TOTAL no início
        linha_total_lig = {
            'Regional': 'TOTAL',
            'Total 2024': total_2024_geral_lig,
            **{meses_2025_lig[i]: valores_mensais_2025_geral_lig[i] for i in range(12)},
            'Total 2025': total_2025_geral_lig,
            'Real Jan/26': real_jan_26_geral_lig,
            'Var 2025/2024': variacao_2024_2025_geral_lig,
            'Var MoM': variacao_mom_geral_lig
        }
        
        # Criar DataFrame final com as regionais ordenadas por Total 2025 (decrescente)
        df_final_lig = pd.DataFrame([linha_total_lig] + pivot_data_ordenada_lig)
        
        # Ordenar colunas
        colunas_ordenadas_lig = ['Regional', 'Total 2024'] + meses_2025_lig + ['Total 2025', 'Real Jan/26', 'Var 2025/2024', 'Var MoM']
        df_final_lig = df_final_lig[colunas_ordenadas_lig]
        
        # =========================
        # FORMATAÇÃO DA TABELA
        # =========================
        def formatar_numero_lig(valor):
            if isinstance(valor, (int, float)):
                if valor == int(valor):
                    return f'{int(valor):,}'.replace(',', '.')
                else:
                    return f'{valor:,.1f}'.replace(',', '.')
            return valor
        
        def formatar_percentual_lig(valor):
            if isinstance(valor, (int, float)):
                return f'{valor:+.1f}%'.replace('.', ',')
            return valor
        
        df_exibicao_lig = df_final_lig.copy()
        for col in df_exibicao_lig.columns:
            if col not in ['Regional', 'Var 2025/2024', 'Var MoM']:
                df_exibicao_lig[col] = df_exibicao_lig[col].apply(formatar_numero_lig)
            else:
                df_exibicao_lig[col] = df_exibicao_lig[col].apply(formatar_percentual_lig)
        
        # =========================
        # FUNÇÃO PARA CRIAR TABELA HTML ESTILIZADA - LIGAÇÕES
        # =========================
        def criar_tabela_html_lig(_df):
            html_lig = """
            <style>
                .tabela-container-lig {
                    width: 100%;
                    max-height: 650px;
                    overflow-y: auto;
                    overflow-x: auto;
                    border: 2px solid #790E09;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(121, 14, 9, 0.15);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    margin: 20px 0;
                    background: white;
                }
                
                .tabela-lig {
                    width: 100%;
                    border-collapse: collapse;
                    border-spacing: 0;
                    font-size: 13px;
                    line-height: 1.5;
                }
                
                .tabela-lig thead {
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                
                .tabela-lig th {
                    background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                    color: white !important;
                    font-weight: 600;
                    padding: 14px 10px;
                    text-align: center;
                    border-bottom: 3px solid #5A0A06;
                    border-right: 1px solid rgba(255, 255, 255, 0.15);
                    white-space: nowrap;
                    font-size: 12px;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                    position: relative;
                    transition: all 0.2s ease;
                }
                
                .tabela-lig th:hover {
                    background: linear-gradient(135deg, #8A1F1A 0%, #6B0F0B 100%) !important;
                }
                
                .tabela-lig th:first-child {
                    border-left: none;
                    border-top-left-radius: 8px;
                }
                
                .tabela-lig th:last-child {
                    border-right: none;
                    border-top-right-radius: 8px;
                }
                
                .tabela-lig th.col-total-anual-lig {
                    background: linear-gradient(135deg, #A23B36 0%, #790E09 100%) !important;
                }
                
                .tabela-lig th.col-mes-lig {
                    background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                }
                
                .tabela-lig th.col-real-jan26-lig {
                    background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                }
                
                .tabela-lig th.col-variacao-lig {
                    background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                }
                
                .tabela-lig td {
                    padding: 12px 10px;
                    text-align: center;
                    border-bottom: 1px solid #E8E8E8;
                    border-right: 1px solid #F0F0F0;
                    font-weight: 400;
                    transition: all 0.2s ease;
                }
                
                .tabela-lig tr:not(.linha-total-lig) td:first-child {
                    border-left: none;
                    text-align: left;
                    font-weight: 600;
                    color: #333;
                    background: linear-gradient(90deg, #fef5f4 0%, white 100%) !important;
                    padding-left: 15px;
                }
                
                .tabela-lig td:last-child {
                    border-right: none;
                }
                
                .linha-total-lig {
                    background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                    color: white !important;
                    position: sticky;
                    bottom: 0;
                    z-index: 50;
                    border-top: 2px solid #790E09;
                }
                
                .linha-total-lig td {
                    background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                    color: white !important;
                    border-bottom: none;
                    font-weight: 700;
                    font-size: 14px;
                    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                }
                
                .linha-total-lig td.col-total-anual-lig,
                .linha-total-lig td.col-mes-lig,
                .linha-total-lig td.col-real-jan26-lig,
                .linha-total-lig td.col-variacao-lig {
                    background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                    color: white !important;
                    border-left: none !important;
                    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                    padding-left: 10px !important;
                }
                
                .linha-total-lig td.col-variacao-lig::before,
                .linha-total-lig td.percentual-positivo-lig::before,
                .linha-total-lig td.percentual-negativo-lig::before,
                .linha-total-lig td.percentual-neutro-lig::before {
                    content: "" !important;
                }
                
                .linha-total-lig td:first-child {
                    font-weight: 800;
                    background: linear-gradient(135deg, #3D0704 0%, #5A0A06 100%) !important;
                }
                
                .linha-regional-lig:nth-child(even) {
                    background-color: #FFF9F8 !important;
                }
                
                .linha-regional-lig:nth-child(odd) {
                    background-color: white !important;
                }
                
                .linha-regional-lig:hover {
                    background-color: #FFEBEE !important;
                    box-shadow: inset 0 0 0 1px #FFCDD2;
                    transform: translateY(-1px);
                }
                
                .linha-regional-lig td.col-total-anual-lig {
                    background: linear-gradient(135deg, #FDE8E6 0%, #FCE4E2 100%) !important;
                    color: #790E09 !important;
                    font-weight: 600;
                    border-left: 2px solid #A23B36;
                    border-right: 2px solid #A23B36;
                }
                
                .linha-regional-lig td.col-mes-lig {
                    background-color: #F9F0EF !important;
                    color: #333 !important;
                    border-left: 1px solid #E8D6D5;
                    border-right: 1px solid #E8D6D5;
                }
                
                .linha-regional-lig td.col-real-jan26-lig {
                    background: linear-gradient(135deg, #F1F3F5 0%, #E9ECEF 100%) !important;
                    color: #495057 !important;
                    font-weight: 600;
                    border-left: 2px solid #ADB5BD;
                    border-right: 2px solid #ADB5BD;
                }
                
                .linha-regional-lig td.col-variacao-lig {
                    background-color: #F8F9FA !important;
                }
                
                .linha-regional-lig td.col-variacao-lig.percentual-positivo-lig {
                    color: #1B5E20 !important;
                    background: linear-gradient(135deg, #E8F5E9 0%, #E6F4E7 100%) !important;
                    font-weight: 700;
                    position: relative;
                    padding-left: 28px !important;
                    border-left: 3px solid #4CAF50 !important;
                    border-right: 1px solid #C8E6C9 !important;
                }
                
                .linha-regional-lig td.col-variacao-lig.percentual-positivo-lig::before {
                    content: "▲";
                    position: absolute;
                    left: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 11px;
                    font-weight: 900;
                    color: #2E7D32;
                }
                
                .linha-regional-lig td.col-variacao-lig.percentual-negativo-lig {
                    color: #C62828 !important;
                    background: linear-gradient(135deg, #FFEBEE 0%, #FFE5E8 100%) !important;
                    font-weight: 700;
                    position: relative;
                    padding-left: 28px !important;
                    border-left: 3px solid #F44336 !important;
                    border-right: 1px solid #FFCDD2 !important;
                }
                
                .linha-regional-lig td.col-variacao-lig.percentual-negativo-lig::before {
                    content: "▼";
                    position: absolute;
                    left: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 11px;
                    font-weight: 900;
                    color: #C62828;
                }
                
                .linha-regional-lig td.col-variacao-lig.percentual-neutro-lig {
                    color: #666666 !important;
                    background: #F8F9FA !important;
                    font-weight: 500;
                }
                
                .linha-regional-lig td:hover {
                    transform: scale(1.02);
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    z-index: 10;
                    position: relative;
                }
                
                .linha-regional-lig td.performance-excelente-lig {
                    animation: pulse-green-lig 2s infinite;
                }
                
                .linha-regional-lig td.performance-critica-lig {
                    animation: pulse-red-lig 2s infinite;
                }
                
                @keyframes pulse-green-lig {
                    0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
                    70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
                    100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
                }
                
                @keyframes pulse-red-lig {
                    0% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4); }
                    70% { box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }
                    100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
                }
                
                .tabela-container-lig::-webkit-scrollbar {
                    width: 10px;
                    height: 10px;
                }
                
                .tabela-container-lig::-webkit-scrollbar-track {
                    background: #F5F5F5;
                    border-radius: 10px;
                }
                
                .tabela-container-lig::-webkit-scrollbar-thumb {
                    background: linear-gradient(135deg, #A23B36 0%, #790E09 100%);
                    border-radius: 10px;
                    border: 2px solid #F5F5F5;
                }
                
                .tabela-container-lig::-webkit-scrollbar-thumb:hover {
                    background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
                }
                
                .tabela-container-lig::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    height: 20px;
                    background: linear-gradient(to bottom, transparent, rgba(121, 14, 9, 0.05));
                    pointer-events: none;
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                }
            </style>
            
            <div class="tabela-container-lig">
            <table class="tabela-lig">
            <thead>
                <tr>
            """
            
            for i, col in enumerate(_df.columns):
                classe_lig = ""
                if col == 'Regional':
                    classe_lig = ""
                elif col in ['Total 2024', 'Total 2025']:
                    classe_lig = "col-total-anual-lig"
                elif col in meses_2025_lig:
                    classe_lig = "col-mes-lig"
                elif col == 'Real Jan/26':
                    classe_lig = "col-real-jan26-lig"
                elif 'Var' in col:
                    classe_lig = "col-variacao-lig"
                
                html_lig += f'<th class="{classe_lig}">{col}</th>'
            
            html_lig += "</tr></thead><tbody>"
            
            for idx, row in _df.iterrows():
                is_total_lig = row['Regional'] == 'TOTAL'
                classe_linha_lig = "linha-total-lig" if is_total_lig else "linha-regional-lig"
                html_lig += f'<tr class="{classe_linha_lig}">'
                
                for col in _df.columns:
                    valor_lig = row[col]
                    classe_celula_lig = ""
                    
                    if is_total_lig:
                        if col == 'Regional':
                            classe_celula_lig = ""
                        elif col in ['Total 2024', 'Total 2025']:
                            classe_celula_lig = "col-total-anual-lig"
                        elif col in meses_2025_lig:
                            classe_celula_lig = "col-mes-lig"
                        elif col == 'Real Jan/26':
                            classe_celula_lig = "col-real-jan26-lig"
                        elif 'Var' in col:
                            classe_celula_lig = "col-variacao-lig"
                    else:
                        if col == 'Regional':
                            classe_celula_lig = ""
                        elif col in ['Total 2024', 'Total 2025']:
                            classe_celula_lig = "col-total-anual-lig"
                        elif col in meses_2025_lig:
                            classe_celula_lig = "col-mes-lig"
                        elif col == 'Real Jan/26':
                            classe_celula_lig = "col-real-jan26-lig"
                        elif 'Var' in col:
                            try:
                                valor_limpo_lig = str(valor_lig).replace('%', '').replace('+', '').replace(',', '.')
                                num_valor_lig = float(valor_limpo_lig)
                                
                                if num_valor_lig > 0:
                                    classe_celula_lig = "col-variacao-lig percentual-positivo-lig"
                                    
                                    if num_valor_lig > 50:
                                        classe_celula_lig += " performance-excelente-lig"
                                elif num_valor_lig < 0:
                                    classe_celula_lig = "col-variacao-lig percentual-negativo-lig"
                                    
                                    if num_valor_lig < -30:
                                        classe_celula_lig += " performance-critica-lig"
                                else:
                                    classe_celula_lig = "col-variacao-lig percentual-neutro-lig"
                            except:
                                classe_celula_lig = "col-variacao-lig"
                    
                    html_lig += f'<td class="{classe_celula_lig}">{valor_lig}</td>'
                
                html_lig += "</tr>"
            
            html_lig += "</tbody></table></div>"
            return html_lig
        
        # Exibir tabela
        st.markdown(criar_tabela_html_lig(df_exibicao_lig), unsafe_allow_html=True)
        
        # =========================
        # BOTÕES DE EXPORTAÇÃO - LIGAÇÕES
        # =========================
        col_exp1_lig, col_exp2_lig, col_exp3_lig = st.columns([1, 1, 2])
        
        with col_exp1_lig:
            def exportar_excel_tabela_lig(_df_numerico_lig):
                output_lig = BytesIO()
                with pd.ExcelWriter(output_lig, engine='xlsxwriter') as writer_lig:
                    _df_numerico_lig.to_excel(writer_lig, index=False, sheet_name='Tabela_Ligacoes')
                    
                    workbook_lig = writer_lig.book
                    worksheet_lig = writer_lig.sheets['Tabela_Ligacoes']
                    
                    header_format_lig = workbook_lig.add_format({
                        'bold': True,
                        'bg_color': '#FF2800',
                        'font_color': 'white',
                        'align': 'center',
                        'border': 1,
                        'font_size': 10
                    })
                    
                    number_format_lig = workbook_lig.add_format({
                        'num_format': '#,##0',
                        'align': 'center'
                    })
                    
                    percent_format_lig = workbook_lig.add_format({
                        'num_format': '0.0%',
                        'align': 'center'
                    })
                    
                    for col_num_lig, col_name_lig in enumerate(_df_numerico_lig.columns):
                        worksheet_lig.write(0, col_num_lig, col_name_lig, header_format_lig)
                        
                        if col_name_lig in ['Var 2025/2024', 'Var MoM']:
                            cell_format_lig = percent_format_lig
                        else:
                            cell_format_lig = number_format_lig
                        
                        for row_num_lig in range(1, len(_df_numerico_lig) + 1):
                            value_lig = _df_numerico_lig.iloc[row_num_lig-1, col_num_lig]
                            if pd.isna(value_lig):
                                worksheet_lig.write(row_num_lig, col_num_lig, '')
                            elif col_name_lig == 'Regional':
                                worksheet_lig.write(row_num_lig, col_num_lig, value_lig)
                            else:
                                worksheet_lig.write(row_num_lig, col_num_lig, value_lig, cell_format_lig)
                    
                    for i_lig, col_lig in enumerate(_df_numerico_lig.columns):
                        column_width_lig = max(_df_numerico_lig[col_lig].astype(str).map(len).max(), len(col_lig)) + 2
                        worksheet_lig.set_column(i_lig, i_lig, min(column_width_lig, 20))
                
                return output_lig.getvalue()
            
            # Converter df_final_lig para formato numérico para exportação
            df_numerico_lig = df_final_lig.copy()
            excel_data_lig = exportar_excel_tabela_lig(df_numerico_lig)
            st.download_button(
                label="📥 Exportar Excel",
                data=excel_data_lig,
                file_name="tabela_ligacoes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="export_excel_ligacoes"
            )
        
        with col_exp2_lig:
            @st.cache_data
            def convert_to_csv_lig(_df_lig):
                return _df_lig.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
            
            csv_data_lig = convert_to_csv_lig(df_numerico_lig)
            st.download_button(
                label="📄 Exportar CSV",
                data=csv_data_lig,
                file_name="tabela_ligacoes.csv",
                mime="text/csv",
                use_container_width=True,
                key="export_csv_ligacoes"
            )
        
        with col_exp3_lig:
            st.caption(f"""
            **Resumo da Tabela:** {len(pivot_data_lig)} Regionais | 
            **Total 2024:** {formatar_numero_lig(total_2024_geral_lig)} | 
            **Total 2025:** {formatar_numero_lig(total_2025_geral_lig)} | 
            **Crescimento:** {formatar_percentual_lig(variacao_2024_2025_geral_lig)} |
            **Último Mês (dez/25):** {formatar_numero_lig(dez_25_geral_lig)}
            """)

# =========================
# RODAPÉ COM LOGO
# =========================
st.markdown("---")

def create_logo_html():
    return """
    <div class="footer-logo">
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
            <div style="text-align: center;">
                <div style="color: #FFFFFF; font-size: 24px; font-weight: bold; font-family: 'Arial Black', sans-serif;">
                    CLARO
                </div>
                <div style="color: #FFFFFF; font-size: 18px; font-weight: bold; margin-top: -5px;">
                    EMPRESAS
                </div>
            </div>
        </div>
        <div class="logo-text">
            Dashboard Canais Estratégicos - PME | © 2024 Claro S.A. - Todos os direitos reservados
        </div>
    </div>
    """

st.markdown(create_logo_html(), unsafe_allow_html=True)
