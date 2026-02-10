import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from datetime import datetime, date
from io import BytesIO
import locale
import re
from textwrap import dedent

# Harmonizar tema plotly com títulos menores
base_template = go.layout.Template(
    layout=go.Layout(
        template="plotly_white",
        title=go.layout.Title(font=dict(size=16, color="#333333", family="Segoe UI"))
    )
)
px.defaults.template = base_template
px.defaults.color_discrete_sequence = ["#FF2800", "#790E09", "#5A6268", "#2E7D32", "#FF9800", "#2196F3"]

# Configurar locale para português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    pass

# =========================
# NOVA FUNÇÃO DE FORMATAÇÃO BRASILEIRA
# =========================
def formatar_numero_brasileiro(valor, casas_decimais=0):
    """
    Formata número no padrão brasileiro:
    - Ponto como separador de milhar
    - Vírgula como separador decimal
    """
    if pd.isna(valor) or valor is None:
        return "0"
    
    try:
        # Converter para float
        valor_float = float(valor)
        
        # Arredondar para o número de casas decimais
        valor_arredondado = round(valor_float, casas_decimais)
        
        # Formatar inteiro (sem casas decimais)
        if casas_decimais == 0:
            parte_inteira = int(valor_arredondado)
            # Usar abs() para tratar números negativos
            valor_formatado = f"{abs(parte_inteira):,}"
            valor_formatado = valor_formatado.replace(",", ".")
            # Adicionar sinal negativo se necessário
            if parte_inteira < 0:
                valor_formatado = f"-{valor_formatado}"
            return valor_formatado
        
        # Formatar com casas decimais
        # Separar parte inteira e decimal
        sinal = '-' if valor_arredondado < 0 else ''
        valor_abs = abs(valor_arredondado)
        
        parte_inteira = int(valor_abs)
        parte_decimal = valor_abs - parte_inteira
        
        # Formatar parte inteira com separador de milhar
        parte_inteira_fmt = f"{parte_inteira:,}".replace(",", ".")
        
        # Formatar parte decimal
        if casas_decimais > 0:
            # Usar formatação com número fixo de casas decimais
            format_str = f"{{:.{casas_decimais}f}}"
            parte_decimal_str = format_str.format(parte_decimal)
            # Remover o "0." do início
            parte_decimal_fmt = parte_decimal_str[2:] if parte_decimal_str.startswith('0.') else parte_decimal_str
        else:
            parte_decimal_fmt = ""
        
        if parte_decimal_fmt:
            return f"{sinal}{parte_inteira_fmt},{parte_decimal_fmt}"
        else:
            return f"{sinal}{parte_inteira_fmt}"
            
    except Exception as e:
        print(f"Erro ao formatar {valor}: {e}")
        return str(valor)

# =========================
# CONFIGURAÇÕES DE ESTILO GLOBAL
# =========================
st.set_page_config(page_title="Dashboard - Canais Estratégicos", layout="wide")

# Adicionar CSS personalizado (mantido igual)
st.markdown("""
    <style>
        * {font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;}
        html, body, .block-container {
            background: radial-gradient(circle at 20% 20%, rgba(255,40,0,0.05), transparent 35%),
                        radial-gradient(circle at 80% 10%, rgba(121,14,9,0.06), transparent 30%),
                        radial-gradient(circle at 50% 70%, rgba(90,10,6,0.05), transparent 40%),
                        #ffffff;
        }
        .block-container {padding-top: 15px;}
        .css-18e3th9 {padding-top: 10px;}
        
        .main-title {
            font-size: 52px;
            font-weight: 900;
            background: linear-gradient(135deg, #FF2800 0%, #790E09 50%, #5A0A06 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 10px 0 20px 0;
            letter-spacing: -1.5px;
            position: relative;
            padding: 30px 0 40px 0;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            text-shadow: 0 4px 12px rgba(121, 14, 9, 0.15);
            line-height: 1.1;
        }
        
        .main-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 180px;
            height: 6px;
            background: linear-gradient(90deg, #FF2800, #790E09, #5A0A06);
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(255, 40, 0, 0.3);
        }
        
        .main-title::after {
            content: 'DASHBOARD ANALÍTICO | PERFORMANCE DE CANAIS';
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: 700;
            color: #666666;
            letter-spacing: 3px;
            text-transform: uppercase;
            background: none;
            -webkit-text-fill-color: #666666;
            opacity: 0.9;
            padding: 8px 30px;
            background: linear-gradient(90deg, rgba(255, 40, 0, 0.05), rgba(121, 14, 9, 0.05));
            border-radius: 25px;
            border: 1px solid rgba(121, 14, 9, 0.1);
        }
        
        .section-title {
            font-size: 32px;
            font-weight: 800;
            color: #333333;
            margin: 40px 0 25px 0;
            padding: 18px 0 18px 30px;
            position: relative;
            background: linear-gradient(90deg, rgba(255, 40, 0, 0.12) 0%, transparent 100%);
            border-left: 5px solid #FF2800;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 6px 20px rgba(255, 40, 0, 0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .section-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(180deg, #FF2800 0%, #790E09 100%);
            border-radius: 5px;
        }
        
        .section-icon {
            font-size: 28px;
            background: linear-gradient(135deg, #FF2800, #790E09);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subsection-title {
            font-size: 24px;
            font-weight: 700;
            color: #333333;
            margin: 35px 0 20px 0;
            padding: 15px 0 15px 25px;
            position: relative;
            border-left: 4px solid #FF2800;
            background: linear-gradient(90deg, rgba(255, 40, 0, 0.08) 0%, transparent 100%);
            border-radius: 0 10px 10px 0;
        }
        
        .card-title {
            font-size: 20px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 20px;
            text-align: center;
            padding: 16px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border-radius: 16px;
            border: 2px solid #E9ECEF;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card-dinamico {
            background: linear-gradient(145deg, #FFFFFF, #F8F9FA);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 
                0 8px 25px rgba(121, 14, 9, 0.12),
                0 3px 10px rgba(0, 0, 0, 0.06),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            margin: 10px 0;
            border: 2px solid #F0F0F0;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .kpi-card-dinamico:hover {
            transform: translateY(-6px);
            box-shadow: 
                0 15px 35px rgba(121, 14, 9, 0.18),
                0 5px 15px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.95);
            border-color: #FF2800;
        }
        
        .kpi-card-dinamico::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #FF2800, #790E09, #5A0A06);
            border-radius: 16px 16px 0 0;
        }
        
        .kpi-title-dinamico {
            font-size: 18px !important;
            background: linear-gradient(135deg, #FF2800 0%, #790E09 50%, #5A0A06 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px !important;
            text-align: center;
            font-weight: 900;
            position: relative;
            padding-bottom: 10px;
            letter-spacing: 0.5px;
        }
        
        .kpi-title-dinamico::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background: linear-gradient(90deg, #FF2800, #790E09);
            border-radius: 3px;
        }
        
        .kpi-block-dinamico {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            border-radius: 12px;
            padding: 15px 10px;
            text-align: center;
            border: 2px solid #E9ECEF;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-block-dinamico:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(121, 14, 9, 0.15);
            border-color: #FF2800;
        }
        
        .kpi-block-dinamico::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #5A0A06, #790E09, #FF2800);
            opacity: 0.8;
        }
        
        .kpi-value-dinamico {
            font-size: 28px !important;
            color: #333333;
            font-weight: 900;
            margin: 10px 0 !important;
            line-height: 1.2;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #333333, #555555);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Reforço de hierarquia visual para legendas em gráficos */
        .js-plotly-plot .plotly .legend text {font-weight: 700 !important;}
        .js-plotly-plot .plotly .main-svg .gtitle {font-size: 16px !important; font-weight: 800 !important;}
        
        .kpi-variacao-item {
            font-size: 10px !important;
            font-weight: 800;
            padding: 4px 8px !important;
            border-radius: 12px;
            display: inline-block;
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1.5px solid rgba(0, 0, 0, 0.05);
            min-height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            letter-spacing: 0.3px;
            text-align: center;
        }
        
        .variacao-positiva {
            color: #1B5E20 !important;
            background: linear-gradient(135deg, rgba(232, 245, 233, 1), rgba(200, 230, 201, 1)) !important;
            border: 1.5px solid #4CAF50 !important;
        }
        
        .variacao-negativa {
            color: #C62828 !important;
            background: linear-gradient(135deg, rgba(255, 235, 238, 1), rgba(255, 205, 210, 1)) !important;
            border: 1.5px solid #F44336 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: #F8F9FA;
            padding: 8px;
            border-radius: 16px;
            margin-bottom: 30px;
            border: 2px solid #E9ECEF;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA) !important;
            border-radius: 12px;
            padding: 15px 28px;
            font-weight: 700;
            color: #666666 !important;
            border: 2px solid #E9ECEF !important;
            transition: all 0.3s ease;
            font-size: 16px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #FF2800 0%, #790E09 100%) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 6px 20px rgba(255, 40, 0, 0.3);
            font-weight: 800;
            transform: scale(1.05);
        }
        
        /* Controles de filtro (select / multiselect) */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            min-height: 46px;
            border: 2px solid #A23B36 !important;
            border-radius: 12px !important;
            padding: 8px 12px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #FF5434 0%, #7A120C 100%) !important;
            box-shadow: 0 6px 16px rgba(121, 14, 9, 0.25) !important;
            transition: all 0.2s ease;
            display: flex !important;
            align-items: center !important;
            overflow: visible !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div > div {
            overflow: visible !important;
            min-height: 22px !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] span,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] span {
            line-height: 1.25 !important;
            max-height: none !important;
            white-space: normal !important;
            text-overflow: clip !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:hover,
        [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"]:focus-within > div {
            border-color: #FF9D8A !important;
            box-shadow: 0 8px 20px rgba(255, 84, 52, 0.35) !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div *,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            fill: #FFFFFF !important;
            font-weight: 700 !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] input::placeholder,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] input::placeholder {
            color: #FFD5CB !important;
            -webkit-text-fill-color: #FFD5CB !important;
            opacity: 1 !important;
        }

        /* Menu dropdown dos filtros */
        div[data-baseweb="popover"] ul[role="listbox"] {
            background: #FFFFFF !important;
            border: 1.5px solid #A23B36 !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
            padding: 4px !important;
        }

        div[data-baseweb="popover"] li[role="option"] {
            color: #333333 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            background: #FFFFFF !important;
        }

        div[data-baseweb="popover"] li[role="option"]:hover {
            background: rgba(255, 84, 52, 0.10) !important;
            color: #7A120C !important;
        }

        div[data-baseweb="popover"] li[role="option"][aria-selected="true"] {
            background: rgba(121, 14, 9, 0.14) !important;
            color: #5A0A06 !important;
            font-weight: 800 !important;
        }

        /* Chips selecionados do multiselect */
        [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
            background: linear-gradient(135deg, #FF5434, #7A120C) !important;
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
            padding: 2px 8px !important;
        }

        [data-testid="stMultiSelect"] span[data-baseweb="tag"] *,
        [data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 800 !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #FF2800 0%, #790E09 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(255, 40, 0, 0.25);
            border: 2px solid rgba(255, 255, 255, 0.15);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
            color: white;
            box-shadow: 0 8px 25px rgba(121, 14, 9, 0.4);
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            padding: 24px;
            border-radius: 16px;
            border: 2px solid #E9ECEF;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        }
        
        [data-testid="stMetricValue"] {
            font-weight: 900;
            color: #333333;
            font-size: 32px !important;
            background: linear-gradient(135deg, #333333, #555555);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .filter-container {
            background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
            border: 2px solid #E9ECEF;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        }
        
        .filter-title {
            font-size: 16px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #E9ECEF;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .filter-label-standard {
            font-size: 12px;
            font-weight: 800;
            color: #6B1A14;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            margin: 0 0 8px 0;
            line-height: 1.1;
        }

        [data-testid="stWidgetLabel"] p {
            font-size: 12px !important;
            font-weight: 800 !important;
            color: #6B1A14 !important;
            letter-spacing: 0.4px !important;
            text-transform: uppercase;
            margin: 0 !important;
            line-height: 1.15 !important;
        }

        [data-testid="stWidgetLabel"] {
            margin-bottom: 8px !important;
            padding-bottom: 0 !important;
        }

        [data-testid="stSelectbox"],
        [data-testid="stMultiSelect"] {
            margin: 0 0 10px 0 !important;
        }

        [data-testid="stSelectbox"] > div,
        [data-testid="stMultiSelect"] > div {
            margin-top: 0 !important;
        }
        
        .info-box {
            background: linear-gradient(135deg, rgba(255, 40, 0, 0.05), rgba(121, 14, 9, 0.05));
            border-radius: 12px;
            padding: 20px;
            border: 2px solid rgba(255, 40, 0, 0.1);
            margin: 20px 0;
        }
        
        .info-box-title {
            font-size: 14px;
            font-weight: 700;
            color: #FF2800;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .footer-logo {
            background: linear-gradient(135deg, #000000 0%, #1A1A1A 100%);
            padding: 30px;
            text-align: center;
            margin: 60px -20px -20px -20px;
            border-top: 4px solid #FF2800;
            position: relative;
        }
        
        .footer-logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 3px;
            background: linear-gradient(90deg, transparent, #FF2800, #790E09, transparent);
        }
        
        .logo-text {
            color: #FFFFFF;
            font-size: 14px;
            margin-top: 15px;
            font-family: 'Segoe UI', sans-serif;
            opacity: 0.9;
            letter-spacing: 1px;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 36px;
                padding: 20px 0 30px 0;
            }
            
            .main-title::after {
                font-size: 12px;
                padding: 6px 20px;
                letter-spacing: 2px;
            }
            
            .section-title {
                font-size: 24px;
                padding: 15px 0 15px 20px;
            }
            
            .kpi-value-dinamico {
                font-size: 24px !important;
            }
            
            .kpi-variacao-item {
                font-size: 9px !important;
                padding: 3px 6px !important;
            }
        }
        
        /* Tamanho padronizado dos títulos dos gráficos */
        .js-plotly-plot .plotly .main-svg .gtitle {
              font-size: 16px !important;
        }

        /* =========================
           VISUAL SYSTEM OVERRIDES
           ========================= */
        :root {
            --ds-primary: #790E09;
            --ds-primary-soft: #A23B36;
            --ds-bg: #F7F8FA;
            --ds-surface: #FFFFFF;
            --ds-surface-soft: #FAFBFC;
            --ds-text: #1F2937;
            --ds-text-muted: #4B5563;
            --ds-border: #E5E7EB;
            --ds-border-strong: #D1D5DB;
            --ds-positive: #1B5E20;
            --ds-negative: #C62828;
        }

        html, body, .block-container {
            background: var(--ds-bg) !important;
        }

        .block-container {
            max-width: 1550px;
        }

        .main-title {
            font-size: 44px;
            text-shadow: none;
            margin-bottom: 14px;
        }

        .main-title::after {
            letter-spacing: 1.6px;
            font-size: 12px;
            border: 1px solid var(--ds-border);
            background: #FFFFFF;
        }

        .section-title {
            font-size: 28px;
            color: var(--ds-text);
            background: var(--ds-surface);
            border: 1px solid var(--ds-border);
            border-left: 5px solid var(--ds-primary);
            border-radius: 12px;
            box-shadow: none;
            margin: 28px 0 18px 0;
            padding: 14px 18px;
            gap: 10px;
        }

        .section-title::before {
            display: none;
        }

        .subsection-title,
        .card-title {
            background: var(--ds-surface);
            border: 1px solid var(--ds-border);
            box-shadow: none;
        }

        .kpi-card-dinamico,
        .kpi-block-dinamico,
        [data-testid="stMetric"] {
            background: var(--ds-surface) !important;
            border: 1px solid var(--ds-border) !important;
            box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06) !important;
        }

        .kpi-card-dinamico::before,
        .kpi-block-dinamico::before {
            height: 3px;
            background: var(--ds-primary);
            opacity: 1;
        }

        .kpi-card-dinamico:hover,
        .kpi-block-dinamico:hover {
            transform: none;
            border-color: var(--ds-border-strong) !important;
            box-shadow: 0 4px 12px rgba(16, 24, 40, 0.10) !important;
        }

        .kpi-title-dinamico {
            background: none !important;
            color: var(--ds-primary) !important;
            -webkit-text-fill-color: var(--ds-primary) !important;
            font-size: 16px !important;
            letter-spacing: 0.2px;
            margin-bottom: 10px !important;
        }

        .kpi-title-dinamico::after {
            height: 2px;
            width: 42px;
            background: var(--ds-primary);
        }

        .kpi-value-dinamico {
            font-size: 24px !important;
            color: var(--ds-text) !important;
            background: none !important;
            -webkit-text-fill-color: var(--ds-text) !important;
            text-shadow: none;
        }

        .kpi-variacao-item {
            box-shadow: none;
            border-radius: 10px;
        }

        .variacao-positiva {
            color: var(--ds-positive) !important;
            background: #EAF6EC !important;
            border-color: #4CAF50 !important;
        }

        .variacao-negativa {
            color: var(--ds-negative) !important;
            background: #FDECEC !important;
            border-color: #F44336 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: var(--ds-surface);
            border: 1px solid var(--ds-border);
            box-shadow: none;
            padding: 5px;
            margin-bottom: 20px;
        }

        .stTabs [data-baseweb="tab"] {
            background: var(--ds-surface-soft) !important;
            color: var(--ds-text-muted) !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            border-radius: 10px;
            padding: 10px 18px;
            font-size: 14px;
        }

        .stTabs [aria-selected="true"] {
            background: var(--ds-primary) !important;
            color: #FFFFFF !important;
            border-color: var(--ds-primary) !important;
            box-shadow: none !important;
            transform: none;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            min-height: 46px;
            padding: 7px 12px !important;
            border: 1.5px solid var(--ds-border-strong) !important;
            border-radius: 10px !important;
            background: #FFFFFF !important;
            box-shadow: none !important;
            align-items: center !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:hover,
        [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"]:focus-within > div {
            border-color: var(--ds-primary-soft) !important;
            box-shadow: 0 0 0 3px rgba(121, 14, 9, 0.10) !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div *,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div * {
            color: var(--ds-text) !important;
            -webkit-text-fill-color: var(--ds-text) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] span,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] span {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.25 !important;
            max-height: none !important;
        }

        [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
            background: var(--ds-primary) !important;
            border: none !important;
            box-shadow: none !important;
        }

        [data-testid="stMultiSelect"] span[data-baseweb="tag"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stWidgetLabel"] p {
            color: var(--ds-text-muted) !important;
            letter-spacing: 0.3px !important;
        }

        .filter-title {
            color: var(--ds-text);
            border-bottom: 1px solid var(--ds-border);
            margin-bottom: 10px;
            padding-bottom: 8px;
        }

        .info-box {
            background: var(--ds-surface) !important;
            border: 1px solid var(--ds-border) !important;
            box-shadow: none !important;
        }

        .info-box-title {
            color: var(--ds-primary);
            letter-spacing: 0.7px;
        }

        .stButton > button {
            background: var(--ds-primary);
            border: 1px solid var(--ds-primary);
            box-shadow: none;
        }

        .stButton > button:hover {
            background: #5A0A06;
            border-color: #5A0A06;
            box-shadow: none;
            transform: none;
        }

        [data-testid="stDownloadButton"] > button {
            width: 100% !important;
            min-height: 40px !important;
            border-radius: 10px !important;
            border: 1.5px solid var(--ds-primary-soft) !important;
            background: #FFFFFF !important;
            color: var(--ds-primary) !important;
            box-shadow: none !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stDownloadButton"] > button:hover {
            border-color: var(--ds-primary) !important;
            background: #FAF3F2 !important;
            color: #5A0A06 !important;
            box-shadow: 0 2px 8px rgba(121, 14, 9, 0.12) !important;
        }

        [data-testid="stDownloadButton"] > button:focus {
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(121, 14, 9, 0.14) !important;
        }

        [data-testid="stDownloadButton"] > button p {
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 0.1px !important;
            color: inherit !important;
        }

        [data-testid="stCaptionContainer"] {
            margin-top: 4px !important;
            padding: 10px 12px !important;
            border: 1px solid var(--ds-border) !important;
            border-left: 3px solid var(--ds-primary-soft) !important;
            border-radius: 10px !important;
            background: #FFFFFF !important;
        }

        [data-testid="stCaptionContainer"] p {
            color: var(--ds-text-muted) !important;
            font-size: 12px !important;
            line-height: 1.4 !important;
            margin: 0 !important;
        }

        [data-testid="stCaptionContainer"] strong {
            color: var(--ds-text) !important;
        }

        /* Filtros com fundo vermelho: garantir texto branco */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #FF5434 0%, #7A120C 100%) !important;
            border-color: #A23B36 !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div *,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div *,
        [data-testid="stSelectbox"] div[data-baseweb="select"] span,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] span,
        [data-testid="stSelectbox"] div[data-baseweb="select"] input,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] input {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] input::placeholder,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] input::placeholder {
            color: #FFD5CB !important;
            -webkit-text-fill-color: #FFD5CB !important;
            opacity: 1 !important;
        }

        @media (max-width: 768px) {
            .section-title {
                font-size: 22px;
                padding: 12px 14px;
                margin: 20px 0 12px 0;
            }

            .kpi-card-dinamico {
                min-height: 150px;
            }
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

def mes_ano_para_data(mes_ano_str: str) -> datetime:
    """Converte string 'mes/ano' para objeto datetime"""
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

def get_mes_atual_formatado() -> str:
    """Retorna o mês atual no formato 'mmm/aa'"""
    hoje = date.today()
    meses_abreviados = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }
    mes_abrev = meses_abreviados.get(hoje.month, 'jan')
    ano_abrev = str(hoje.year)[-2:]
    return f"{mes_abrev}/{ano_abrev}"

def get_mes_anterior(mes_atual: str) -> str:
    """Retorna o mês anterior baseado no mês atual no formato 'mmm/aa'"""
    try:
        meses_pt = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        meses_reverso = {v: k for k, v in meses_pt.items()}
        
        mes_str, ano_str = mes_atual.lower().split('/')
        mes_num = meses_pt.get(mes_str, 1)
        ano_num = int(f"20{ano_str}")
        
        # Calcular mês anterior
        if mes_num == 1:  # Janeiro
            mes_anterior_num = 12
            ano_anterior_num = ano_num - 1
        else:
            mes_anterior_num = mes_num - 1
            ano_anterior_num = ano_num
        
        mes_anterior_str = meses_reverso.get(mes_anterior_num, 'jan')
        ano_anterior_str = str(ano_anterior_num)[-2:]
        
        return f"{mes_anterior_str}/{ano_anterior_str}"
    except:
        return mes_atual

def render_filter_label(texto: str):
    """Renderiza rótulo padrão para filtros com label colapsado."""
    st.markdown(f'<div class="filter-label-standard">{texto}</div>', unsafe_allow_html=True)

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
    df_linhas['Valor_Formatado'] = df_linhas['Valor'].apply(lambda x: formatar_numero_brasileiro(x, 0))
    
    return df_linhas

@st.cache_data
def create_bar_chart_data(df_mes_selecionado):
    """Cria dados para gráfico de barras horizontais"""
    bar_data = df_mes_selecionado.groupby(['CANAL_PLAN', 'COD_PLATAFORMA'], observed=True)['QTDE'].sum().reset_index()
    canal_totals = bar_data.groupby('CANAL_PLAN', observed=True)['QTDE'].sum().sort_values(ascending=False)
    canal_order = canal_totals.index
    
    bar_data['CANAL_PLAN'] = pd.Categorical(bar_data['CANAL_PLAN'], categories=canal_order, ordered=True)
    bar_data = bar_data.sort_values('CANAL_PLAN', ascending=False)
    bar_data['QTDE_Formatado'] = bar_data['QTDE'].apply(lambda x: formatar_numero_brasileiro(x, 0))
    
    return bar_data, canal_totals

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
file_path = "base_final_trt_new3.xlsx"
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
    <div style="margin: 15px 0 35px 0; text-align: center; position: relative;">
        <div style="height: 2px; background: linear-gradient(90deg, 
                    rgba(255, 40, 0, 0) 0%, 
                    rgba(255, 40, 0, 0.3) 20%, 
                    rgba(255, 40, 0, 0.8) 50%, 
                    rgba(255, 40, 0, 0.3) 80%, 
                    rgba(255, 40, 0, 0) 100%);"></div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    background: white; padding: 0 20px;">
            <span style="color: #FF2800; font-size: 14px; font-weight: 700; letter-spacing: 3px;">● ● ●</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["📱 Ativados", "📉 Desativados", "📋 Pedidos", "📞 Ligações"])

# Persistir aba selecionada entre reruns para evitar voltar para Ativados ao filtrar
components.html(
    """
    <script>
    (function() {
      const KEY = "dashboard_tab_ativa";
      const doc = window.parent.document;

      function getTabs() {
        const tabList = doc.querySelector('div[data-baseweb="tab-list"]');
        if (!tabList) return [];
        return Array.from(tabList.querySelectorAll('button[role="tab"]'));
      }

      function bindTabClicks() {
        const tabs = getTabs();
        tabs.forEach((tab) => {
          if (tab.dataset.tabBound === "1") return;
          tab.dataset.tabBound = "1";
          tab.addEventListener("click", () => {
            try {
              window.sessionStorage.setItem(KEY, tab.innerText.trim());
            } catch (e) {}
          });
        });
      }

      function restoreSavedTab() {
        let saved = null;
        try {
          saved = window.sessionStorage.getItem(KEY);
        } catch (e) {}
        if (!saved) return;

        const tabs = getTabs();
        const target = tabs.find((t) => t.innerText.trim() === saved);
        if (target && target.getAttribute("aria-selected") !== "true") {
          target.click();
        }
      }

      let attempts = 0;
      const timer = setInterval(() => {
        bindTabClicks();
        restoreSavedTab();
        attempts += 1;
        if (attempts > 30) clearInterval(timer);
      }, 120);
    })();
    </script>
    """,
    height=0,
)

# =========================
# ABA 1: ATIVADOS
# =========================
with tab1:
    # Container para o filtro de mês compartilhado
    with st.container():
        st.markdown('<div class="filter-title">📅 SELECIONE O MÊS PARA ANÁLISE</div>', unsafe_allow_html=True)
        
        # Obter meses disponíveis e ordenar cronologicamente
        meses_disponiveis_cards = df_filtered['dat_tratada'].unique()
        
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
        
        # Obter mês atual formatado
        mes_atual_formatado = get_mes_atual_formatado()
        
        # Encontrar índice do mês atual ou usar o último disponível
        if mes_atual_formatado in meses_ordenados:
            idx_padrao = meses_ordenados.index(mes_atual_formatado)
        else:
            idx_padrao = len(meses_ordenados) - 1 if len(meses_ordenados) > 0 else 0
        
        # Selectbox para seleção do mês
        col_filtro1, col_filtro2 = st.columns([1, 3])
        
        with col_filtro1:
            mes_selecionado_cards = st.selectbox(
                "Selecione o mês para análise",
                options=meses_ordenados,
                index=idx_padrao,
                key="mes_compartilhado",
                label_visibility="collapsed"
            )
        
        # Calcular mês anterior corretamente
        mes_anterior_cards = get_mes_anterior(mes_selecionado_cards)
        
        # Container informativo
        with col_filtro2:
            st.markdown(f"""
                <div class="info-box" style="margin: 0; padding: 12px 15px;">
                    <div style="display: flex; align-items: center; gap: 15px; flex-wrap: nowrap; height: 100%;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Atual:</span>
                            <span style="font-size: 14px; color: #FF2800; font-weight: 800; 
                                    background: rgba(255, 40, 0, 0.1); padding: 6px 15px; border-radius: 20px;">
                                {mes_selecionado_cards}
                            </span>
                        </div>
                        <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Anterior:</span>
                            <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                    background: rgba(121, 14, 9, 0.1); padding: 6px 15px; border-radius: 20px;">
                                {mes_anterior_cards}
                            </span>
                        </div>
                        <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Comparativo:</span>
                            <span style="font-size: 13px; color: #666666; font-weight: 600;">
                                MoM (Mês sobre Mês)
                            </span>
                        </div>
                    </div>
                </div>
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
        'E-Commerce',
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
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> PERFORMANCE POR CANAL</div>', unsafe_allow_html=True)
    
    for i in range(0, num_canais, 3):
        cols = st.columns(3, gap="medium")
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
                    classe_mom = "variacao-positiva"
                else:
                    classe_mom = "variacao-negativa"
                
                if desvio_meta is not None:
                    if desvio_meta >= 0:
                        classe_meta = "variacao-positiva"
                    else:
                        classe_meta = "variacao-negativa"
                    
                    meta_html = f'<div class="kpi-variacao-item {classe_meta}" style="font-size: 10px !important;">{desvio_meta:+.0f}% Meta</div>'
                else:
                    meta_html = '<div class="kpi-variacao-item" style="background: #F5F5F5 !important; color: #666666 !important; border: 1.5px solid #E0E0E0 !important; font-size: 10px !important;">Meta N/A</div>'
                
                bloco_html += (
                    f'<div class="kpi-block-dinamico">'
                    f'<div style="font-size: 13px; color: #333333; font-weight: 700; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">{plataforma}</div>'
                    f'<div class="kpi-value-dinamico">{atual_formatado}</div>'
                    f'<div style="font-size: 12.5px; color: #666666; margin: 5px 0; line-height: 1.4; font-weight: 500;">'
                    f'<span style="font-weight: 600;">Anterior:</span> {anterior_formatado} | '
                    f'<span style="font-weight: 600;">Meta:</span> {meta_formatado}'
                    f'</div>'
                    f'<div style="display: flex; justify-content: space-between; gap: 8px; margin-top: 10px;">'
                    f'<div class="kpi-variacao-item {classe_mom}" style="flex: 1; font-size: 10px !important;">{variacao_mom:+.0f}% MoM</div>'
                    f'{meta_html}'
                    f'</div>'
                    f'</div>'
                )
            
            with cols[j]:
                with st.container():
                    st.markdown(
                        f'<div class="kpi-card-dinamico animate-fade-in-up">'
                        f'<div class="kpi-title-dinamico">{canal}</div>'
                        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">{bloco_html}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
    
    # Rodapé da seção
    st.markdown(f"""
        <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #F8F9FA, #FFFFFF); 
                    border-radius: 16px; border: 2px solid #E9ECEF; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
            <div style="font-size: 13px; color: #666666; margin-bottom: 10px; text-align: center;">
                <span style="color: #FF2800; font-weight: 700;">📌</span> 
                <strong>Métricas calculadas:</strong> 
                <span style="color: #333333; font-weight: 600;">MoM</span> (Mês sobre mês vs {mes_anterior_cards}) e 
                <span style="color: #333333; font-weight: 600;">% Meta</span> (Desvio percentual em relação à meta)
            </div>
            <div style="display: flex; justify-content: center; gap: 25px; margin-top: 15px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: linear-gradient(135deg, #4CAF50, #2E7D32); border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);"></div>
                    <span style="font-size: 13px; color: #333333; font-weight: 700;">Positivo ▲</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: linear-gradient(135deg, #F44336, #C62828); border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);"></div>
                    <span style="font-size: 13px; color: #333333; font-weight: 700;">Negativo ▼</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: linear-gradient(135deg, #9E9E9E, #757575); border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);"></div>
                    <span style="font-size: 13px; color: #333333; font-weight: 700;">Meta não disponível</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================
    # GRÁFICO DE LINHAS TEMPORAL
    # =========================
    with st.container():
        st.markdown('<div class="section-title"><span class="section-icon">📈</span> EVOLUÇÃO MENSAL - COMPARATIVO ANUAL</div>', unsafe_allow_html=True)
        
        with st.container():
            col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
            
            with col_filtro1:
                render_filter_label("CANAL")
                canal_selecionado = st.selectbox(
                    "Selecione o Canal",
                    options=["Todos"] + sorted(df_filtered['CANAL_PLAN'].unique()),
                    key="filtro_canal_linhas",
                    label_visibility="collapsed"
                )
            
            with col_filtro2:
                render_filter_label("REGIONAL")
                regional_selecionada = st.selectbox(
                    "Selecione a Regional",
                    options=["Todos"] + sorted(df_filtered['REGIONAL'].unique()),
                    key="filtro_regional_linhas",
                    label_visibility="collapsed"
                )
            
            with col_filtro3:
                render_filter_label("INDICADOR")
                indicador_selecionado = st.selectbox(
                    "Selecione o Indicador",
                    options=["Todos"] + sorted(df_filtered['DSC_INDICADOR'].unique()),
                    key="filtro_indicador_linhas",
                    label_visibility="collapsed"
                )
            
            with col_filtro4:
                render_filter_label("PLATAFORMA")
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
            title=f'<b>EVOLUÇÃO MENSAL</b><br><span style="font-size: 14px; color: #666666;">{titulo_filtros}</span>',
            labels={'Valor': 'Volume', 'Mês': ''},
            markers=True,
            line_shape='spline',
            color_discrete_map=cores_personalizadas,
            text='Valor_Formatado'
        )
        
        fig_linhas.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=14, color='#333333'),
            margin=dict(l=60, r=60, t=100, b=80),
            xaxis=dict(
                title='',
                tickmode='array',
                tickvals=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
                tickfont=dict(size=13, color='#666666', weight=600),
                showgrid=True,
                gridcolor='rgba(233, 236, 239, 0.5)',
                gridwidth=1,
                linecolor='#E9ECEF',
                linewidth=2,
                mirror=True,
                tickangle=0,
                showline=True,
                zeroline=False
            ),
            yaxis=dict(
                title='<b>VOLUME</b>',
                title_font=dict(size=15, weight=700, color='#333333'),
                tickfont=dict(size=13, color='#666666', weight=600),
                showgrid=True,
                gridcolor='rgba(233, 236, 239, 0.5)',
                gridwidth=1,
                linecolor='#E9ECEF',
                linewidth=2,
                mirror=True,
                showline=True,
                zeroline=False
            ),
            legend=dict(
                title=dict(text='<b>ANO</b>', font=dict(size=14, weight=700, color='#333333')),
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#E9ECEF',
                borderwidth=2,
                font=dict(size=13, color='#333333', weight=600),
                itemwidth=50,
                traceorder='normal'
            ),
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=16, color='#333333', weight=800),
                y=0.95
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='white',
                font_size=14,
                font_family='Segoe UI',
                bordercolor='#E9ECEF',
                font_color='#333333',
                font_weight=600
            ),
            height=500,
            showlegend=True
        )
        
        for i, trace in enumerate(fig_linhas.data):
            ano = trace.name
            trace.update(
                mode='lines+markers+text',
                marker=dict(size=12, line=dict(width=2, color='white'), symbol='circle', opacity=0.9),
                line=dict(width=4, smoothing=1.3),
                textposition='top center',
                textfont=dict(size=12, color=cores_personalizadas[ano], weight=700),
                hovertemplate=(
                    f"<b>%{{x}}/{ano}</b><br>" +
                    "<b>Valor:</b> %{y:,.0f}<br>" +
                    "<extra></extra>"
                )
            )
            
            if ano == '2026':
                trace.update(
                    line=dict(width=4, dash='dash', color=cores_personalizadas[ano]),
                    marker=dict(size=12, line=dict(width=2, color='white'), symbol='diamond', opacity=0.9)
                )
        
        # Container de informações
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                        padding: 15px 20px; 
                        border-radius: 12px; 
                        border: 2px solid #E9ECEF;
                        margin: 15px 0 5px 0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                    <div style="font-size: 14px; color: #333333; font-weight: 700;">
                        <span>📊 Dados Filtrados:</span>
                        <span style="color: #FF2800; margin-left: 8px;">{len(df_grafico):,}</span>
                    </div>
                    <div style="font-size: 13px; color: #666666; display: flex; gap: 20px; flex-wrap: wrap;">
                        <span style="display: inline-flex; align-items: center; gap: 8px;">
                            <div style="width: 12px; height: 12px; background: #FF2800; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                            <span style="font-weight: 600;">2024 (Real)</span>
                        </span>
                        <span style="display: inline-flex; align-items: center; gap: 8px;">
                            <div style="width: 12px; height: 12px; background: #790E09; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                            <span style="font-weight: 600;">2025 (Real)</span>
                        </span>
                        <span style="display: inline-flex; align-items: center; gap: 8px;">
                            <div style="width: 12px; height: 12px; background: #5A6268; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                            <span style="font-weight: 600;">2026 (Meta)</span>
                            <span style="color: #5A6268; margin-left: 4px;">— —</span>
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Exibir gráfico
        st.plotly_chart(fig_linhas, width='stretch', config={'displayModeBar': True, 'displaylogo': False})
    
    # =========================
    # GRÁFICO DE BARRAS HORIZONTAIS
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> DISTRIBUIÇÃO POR CANAL E PLATAFORMA</div>', unsafe_allow_html=True)
    
    # Usar o mesmo mês selecionado nos cards KPI
    mes_selecionado = mes_selecionado_cards
    
    st.markdown(f"""
        <div class="info-box">
            <div class="info-box-title">Período de Análise</div>
            <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 14px; color: #333333; font-weight: 600;">Mês Selecionado:</span>
                    <span style="font-size: 16px; color: #FF2800; font-weight: 800; 
                            background: rgba(255, 40, 0, 0.1); padding: 8px 20px; border-radius: 25px;">
                        {mes_selecionado}
                    </span>
                </div>
                <div style="font-size: 14px; color: #666666; font-weight: 600;">
                    Gráfico sincronizado com a seleção dos cards KPI
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filtrar dados
    df_mes_selecionado = df_filtered[df_filtered['dat_tratada'] == mes_selecionado]
    
    if not df_mes_selecionado.empty:
        # Criar dados para gráfico
        bar_data, canal_totals = create_bar_chart_data(df_mes_selecionado)
        
        # Definir paleta de cores vermelho e cinza conforme solicitado
        color_map = {
            'CONTA': '#790E09',  # Vermelho especificado
            'FIXA': '#495057'    # Cinza especificado
        }
        
        # Se houver outras plataformas, atribua cores diferentes
        plataformas_unicas = bar_data['COD_PLATAFORMA'].unique()
        cores_adicionais = ['#C62828', '#78909C', '#B71C1C', '#546E7A']
        
        # Atribuir cores sequencialmente para outras plataformas
        for i, plataforma in enumerate(plataformas_unicas):
            if plataforma not in color_map:
                color_map[plataforma] = cores_adicionais[i % len(cores_adicionais)]
        
        # Ordenar dados para garantir ordem correta das cores
        bar_data_sorted = bar_data.sort_values('COD_PLATAFORMA')
        
        # Criar gráfico
        fig_bar = px.bar(
            bar_data_sorted, 
            y='CANAL_PLAN',
            x='QTDE',
            color='COD_PLATAFORMA',
            text='QTDE_Formatado',
            barmode='stack',
            color_discrete_map=color_map,
            title=f'<b>DISTRIBUIÇÃO POR CANAL</b><br><span style="font-size: 14px; color: #666666;">Análise de {mes_selecionado}</span>',
            labels={'QTDE': 'Volume', 'CANAL_PLAN': 'Canal'},
            orientation='h',
            height=550,
        )
        
        fig_bar.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=14, color='#333333'),
            margin=dict(l=20, r=150, t=100, b=80),
            yaxis=dict(
                title='<b>CANAL</b>',
                title_font=dict(size=16, weight=800, color='#333333'),
                tickfont=dict(size=14, color='#666666', weight=600),
                showgrid=False,
                linecolor='#E9ECEF',
                linewidth=2,
                ticksuffix="  ",
                categoryorder='total ascending'
            ),
            xaxis=dict(
                title='<b>VOLUME TOTAL</b>',
                title_font=dict(size=16, weight=800, color='#333333'),
                tickfont=dict(size=13, color='#666666', weight=600),
                gridcolor='rgba(233, 236, 239, 0.7)',
                showgrid=True,
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor='#E9ECEF',
                linewidth=2
            ),
            legend=dict(
                title=dict(text='<b>PLATAFORMA</b>', font=dict(size=14, weight=800, color='#333333')),
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#E9ECEF',
                borderwidth=2,
                font=dict(size=13, color='#333333', weight=600),
                itemwidth=40,
                traceorder='normal',
                itemsizing='constant'
            ),
            title=dict(
                x=0.02,
                xanchor='left',
                yanchor='top',
                font=dict(size=16, color='#333333', weight=800),
                y=0.95
            ),
            hovermode='y unified',
            hoverlabel=dict(
                bgcolor='white',
                font_size=14,
                font_family='Segoe UI',
                bordercolor='#E9ECEF',
                font_color='#333333',
                font_weight=600
            ),
            bargap=0.3,
            bargroupgap=0.1,
            showlegend=True,
            transition=dict(duration=300)
        )
        
        fig_bar.update_traces(
            texttemplate='<b>%{text}</b>',
            textposition='inside',
            textfont=dict(size=12, color='white', weight=700),
            marker=dict(line=dict(width=1.5, color='white'), opacity=0.95),
            hovertemplate=(
                "<b>Canal: %{y}</b><br>" +
                "<b>Plataforma: %{fullData.name}</b><br>" +
                "<b>Volume: %{x:,.0f}</b><br>" +
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
                text=f'<b>{total_canal:,.0f}</b><br><span style="font-size: 12px; color: #666666;">({percentual:.1f}%)</span>',
                showarrow=False,
                xshift=60,
                font=dict(size=13, color='#333333', weight=700),
                align='left',
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#E9ECEF',
                borderwidth=2,
                borderpad=6,
                width=80
            )
            
            fig_bar.add_shape(
                type="line",
                x0=total_canal,
                y0=i,
                x1=total_canal + 50,
                y1=i,
                line=dict(color="#CCCCCC", width=1, dash="dash"),
                layer="below"
            )
        
        # Adicionar total geral
        fig_bar.add_annotation(
            xref="paper",
            yref="paper",
            x=1.15,
            y=1.05,
            text=f"<b>TOTAL GERAL</b><br><span style='font-size: 24px; color: #790E09; font-weight: 900;'>{total_geral:,.0f}</span>",
            showarrow=False,
            font=dict(size=14, color='#333333', weight=700),
            align="center",
            bgcolor='#F8F9FA',
            bordercolor='#E9ECEF',
            borderwidth=2,
            borderpad=10
        )
        
        # Exibir gráfico
        st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': True, 'displaylogo': False})
        
        # Insights e KPIs
        with st.container():
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                            padding: 25px; border-radius: 16px; border: 2px solid #E9ECEF; 
                            margin-top: 30px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                        <span style="color: #790E09; font-size: 24px;">💡</span>
                        <span style="font-size: 16px; color: #333333; font-weight: 800;">
                            INSIGHTS E ANÁLISES
                        </span>
                    </div>
            """, unsafe_allow_html=True)
            
            total_por_plataforma = bar_data.groupby('COD_PLATAFORMA', observed=True)['QTDE'].sum()
            top_canal = canal_totals.index[0] if len(canal_totals) > 0 else "N/A"
            top_valor = canal_totals.iloc[0] if len(canal_totals) > 0 else 0
            
            if len(total_por_plataforma) > 0:
                top_plataforma = total_por_plataforma.idxmax()
                top_plataforma_valor = total_por_plataforma.max()
                top_plataforma_percent = (top_plataforma_valor / total_geral * 100) if total_geral > 0 else 0
            
            col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
            
            with col_kpi1:
                st.metric(
                    label="Total Geral",
                    value=f"{total_geral:,.0f}".replace(',', '.'),
                    help="Soma total de todos os canais",
                    delta=None
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
                if len(total_por_plataforma) > 0:
                    st.metric(
                        label="Plataforma Principal",
                        value=top_plataforma,
                        delta=f"{top_plataforma_percent:.1f}%",
                        delta_color="normal"
                    )
            
            with col_kpi4:
                st.metric(
                    label="Canais Analisados",
                    value=len(canal_totals),
                    delta="Segmentos",
                    delta_color="off"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFEBEE, #FFCDD2); 
                        padding: 40px; border-radius: 16px; border: 2px solid #F44336;
                        text-align: center; margin: 20px 0;">
                <div style="color: #C62828; font-size: 64px; margin-bottom: 20px;">
                    ⚠️
                </div>
                <h3 style="color: #333333; margin-bottom: 15px; font-weight: 800;">
                    Dados Insuficientes para Análise
                </h3>
                <p style="color: #666666; margin-bottom: 25px; font-size: 16px; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Não há dados disponíveis para <strong style="color: #790E09;">{mes_selecionado}</strong> com os filtros atuais.
                </p>
        """, unsafe_allow_html=True)
        
        if len(meses_disponiveis_cards) > 0:
            st.info(f"**Meses disponíveis para análise:** {', '.join(sorted(meses_disponiveis_cards))}")

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
    
    # FUNÇÃO PARA CRIAR TABELA PIVOT ATUALIZADA
    @st.cache_data
    def create_pivot_table_updated(df_tabela, mes_atual):
        """
        Função para criar tabela pivot dinâmica atualizada (Ativados)
        """
        pivot_data = []
        regionais = sorted(df_tabela['REGIONAL'].unique())

        # Determinar meses de 2026 até o mês anterior ao foco (evitar duplicar Real/Meta do mês foco)
        mes_atual_num = meses_ordem.index(mes_atual.split('/')[0]) + 1
        meses_2026 = [f'{meses_ordem[i]}/26' for i in range(mes_atual_num) if f'{meses_ordem[i]}/26' != mes_atual]

        for regional in regionais:
            df_regional = df_tabela[df_tabela['REGIONAL'] == regional]

            # Total 2024 (para cálculo, não exibido)
            total_2024 = df_regional[df_regional['ano'] == '24']['QTDE'].sum()
            # Total 2025
            total_2025 = df_regional[df_regional['ano'] == '25']['QTDE'].sum()

            # Mensal 2025
            valores_mensais_2025 = []
            for mes in [f'{m}/25' for m in meses_ordem]:
                valor = df_regional[df_regional['mes_ano'] == mes]['QTDE'].sum()
                valores_mensais_2025.append(valor)

            # Mensal 2026 até mês anterior ao foco
            valores_mensais_2026 = []
            for mes in meses_2026:
                valor = df_regional[df_regional['mes_ano'] == mes]['QTDE'].sum()
                valores_mensais_2026.append(valor)

            mes_anterior = get_mes_anterior(mes_atual)
            mes_atual_valor = df_regional[df_regional['mes_ano'] == mes_atual]['QTDE'].sum()
            mes_anterior_valor = df_regional[df_regional['mes_ano'] == mes_anterior]['QTDE'].sum()
            variacao_mom = ((mes_atual_valor - mes_anterior_valor) / mes_anterior_valor * 100) if mes_anterior_valor > 0 else 0

            meta_mes_atual = df_regional[df_regional['mes_ano'] == mes_atual]['DESAFIO_QTD'].sum()
            alcance_meta = (((mes_atual_valor / meta_mes_atual) - 1) * 100) if meta_mes_atual > 0 else 0

            var_2025_2024 = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0

            row_data = {
                'Regional': regional,
                'Total 2024': total_2024,
                **{f'{meses_ordem[i]}/25': valores_mensais_2025[i] for i in range(12)},
                'Total 2025': total_2025,
                **{meses_2026[i]: valores_mensais_2026[i] for i in range(len(meses_2026))},
                f'Real {mes_atual}': mes_atual_valor,
                f'Meta {mes_atual}': meta_mes_atual,
                'Alcance Meta': alcance_meta,
                'Var MoM': variacao_mom,
                'Var 2025/2024': var_2025_2024
            }

            pivot_data.append(row_data)

        return pivot_data, meses_2026
    
    # Obter mês atual para a tabela
    mes_atual_tabela = mes_selecionado_cards
    
    # AGORA CHAMAR A FUNÇÃO PARA CRIAR A TABELA PIVOT ATUALIZADA
    pivot_data, meses_2026_tabela = create_pivot_table_updated(df_tabela, mes_atual_tabela)
    
    # Ordenar pivot_data pelo Total 2025 (do maior para o menor)
    if pivot_data:
        df_temp_ordenacao = pd.DataFrame(pivot_data)
        df_temp_ordenacao = df_temp_ordenacao.sort_values('Total 2025', ascending=False)
        pivot_data_ordenada = df_temp_ordenacao.to_dict('records')
    else:
        pivot_data_ordenada = []
    
    # Criar linha de TOTAL (soma de todas as regionais)
    df_total = df_tabela.copy()
    
    # Calcular totais gerais
    total_2024_geral = df_total[df_total['ano'] == '24']['QTDE'].sum()
    total_2025_geral = df_total[df_total['ano'] == '25']['QTDE'].sum()
    
    # Calcular valores mensais gerais para 2025
    valores_mensais_2025_geral = []
    for mes in [f'{m}/25' for m in meses_ordem]:
        valor = df_total[df_total['mes_ano'] == mes]['QTDE'].sum()
        valores_mensais_2025_geral.append(valor)
    
    # Calcular valores mensais gerais para 2026 (até o mês atual)
    valores_mensais_2026_geral = []
    for mes in meses_2026_tabela:
        valor = df_total[df_total['mes_ano'] == mes]['QTDE'].sum()
        valores_mensais_2026_geral.append(valor)
    
    # Calcular REAL geral do mês atual
    real_mes_atual_geral = df_total[df_total['mes_ano'] == mes_atual_tabela]['QTDE'].sum()
    
    # Calcular meta geral do mês atual
    meta_mes_atual_geral = df_total[df_total['mes_ano'] == mes_atual_tabela]['DESAFIO_QTD'].sum()
    
    # Calcular variações gerais
    variacao_2024_2025_geral = ((total_2025_geral - total_2024_geral) / total_2024_geral * 100) if total_2024_geral > 0 else 0
    
    # Calcular variação MoM geral
    mes_anterior_geral = get_mes_anterior(mes_atual_tabela)
    mes_atual_valor_geral = df_total[df_total['mes_ano'] == mes_atual_tabela]['QTDE'].sum()
    mes_anterior_valor_geral = df_total[df_total['mes_ano'] == mes_anterior_geral]['QTDE'].sum()
    variacao_mom_geral = ((mes_atual_valor_geral - mes_anterior_valor_geral) / mes_anterior_valor_geral * 100) if mes_anterior_valor_geral > 0 else 0
    
    # Calcular alcance da meta geral
    alcance_meta_geral = (((real_mes_atual_geral / meta_mes_atual_geral)-1) * 100) if meta_mes_atual_geral > 0 else 0
    
    # Adicionar linha de TOTAL no início
    linha_total = {
        'Regional': 'TOTAL',
        'Total 2024': total_2024_geral,
        'Total 2025': total_2025_geral,
        **{f'{meses_ordem[i]}/25': valores_mensais_2025_geral[i] for i in range(12)},
        **{meses_2026_tabela[i]: valores_mensais_2026_geral[i] for i in range(len(meses_2026_tabela))},
        f'Real {mes_atual_tabela}': real_mes_atual_geral,
        f'Meta {mes_atual_tabela}': meta_mes_atual_geral,
        'Alcance Meta': alcance_meta_geral,
        'Var 2025/2024': variacao_2024_2025_geral,
        'Var MoM': variacao_mom_geral
    }
    
    # Criar DataFrame final com as regionais ordenadas por Total 2025 (decrescente)
    if pivot_data_ordenada:
        df_final = pd.DataFrame([linha_total] + pivot_data_ordenada)
    else:
        df_final = pd.DataFrame([linha_total])
    
    # Ordenar colunas
    colunas_base = ['Regional', 'Total 2024']
    colunas_meses_2025 = [f'{meses_ordem[i]}/25' for i in range(12)]
    colunas_meses_2026 = meses_2026_tabela
    colunas_finais = [f'Real {mes_atual_tabela}', f'Meta {mes_atual_tabela}', 'Alcance Meta', 'Var 2025/2024', 'Var MoM']

    colunas_ordenadas = colunas_base + colunas_meses_2025 + ['Total 2025'] + colunas_meses_2026 + colunas_finais
    
    # Manter apenas colunas presentes no DataFrame
    colunas_ordenadas = [col for col in colunas_ordenadas if col in df_final.columns]
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
                padding: 9px 8px; /* reduced height */
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
            
            .tabela-melhorada th.col-real-mes {
                background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
            }
            
            .tabela-melhorada th.col-meta {
                background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
            }
            
            .tabela-melhorada th.col-alcance,
            .tabela-melhorada th.col-variacao {
                background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
            }
            
            .tabela-melhorada td {
                padding: 8px 8px; /* reduced height */
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
            .linha-total-melhorada td.col-real-mes,
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
            
            .linha-regional-melhorada td.col-real-mes {
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

            /* Unified table visual override */
            .tabela-melhorada th {
                padding: 9px 7px !important;
                font-size: 10.5px !important;
                box-shadow: none !important;
            }

            .tabela-melhorada td {
                padding: 7px 7px !important;
                font-size: 10.5px !important;
                line-height: 1.25 !important;
                box-shadow: none !important;
            }

            .tabela-melhorada td:not(:first-child) {
                text-align: right !important;
                font-variant-numeric: tabular-nums;
            }

            .linha-regional-melhorada:hover {
                background-color: #FFF2EF !important;
                box-shadow: inset 0 0 0 1px #FFD9CF !important;
            }

            .linha-regional-melhorada td.performance-excelente,
            .linha-regional-melhorada td.performance-critica {
                animation: none !important;
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
            elif '/25' in col or '/26' in col:
                classe = "col-mes"
            elif 'Real' in col:
                classe = "col-real-mes"
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
                    elif '/25' in col or '/26' in col:
                        classe_celula = "col-mes"
                    elif 'Real' in col:
                        classe_celula = "col-real-mes"
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
                    elif '/25' in col or '/26' in col:
                        classe_celula = "col-mes"
                    elif 'Real' in col:
                        classe_celula = "col-real-mes"
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
    if not df_exibicao.empty:
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
            **Total 2025:** {formatar_numero(total_2025_geral)} | 
            **Crescimento vs 2024:** {formatar_percentual(variacao_2024_2025_geral)} | 
            **Alcance Meta ({mes_atual_tabela}):** {formatar_percentual(alcance_meta_geral)}
            """)
        
        # Análise detalhada
        with st.expander("🔍 Ver dados para análise detalhada", expanded=False):
            df_analise = pd.DataFrame([linha_total] + pivot_data_ordenada)
            df_analise = df_analise[colunas_ordenadas]
            
            st.write("**Principais Insights:**")
            
            col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)
            
            with col_insight1:
                df_crescimento = pd.DataFrame(pivot_data_ordenada)
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
    else:
        st.warning("Não há dados disponíveis para exibir a tabela dinâmica com os filtros atuais.")

# =========================
# ABA 2: DESATIVADOS - VERSÃO COMPLETA E CORRIGIDA
# =========================
with tab2:
    # =========================
    # CARREGAR DADOS DE DESATIVADOS
    # =========================
    @st.cache_data
    def load_desativados_data():
        """Carrega dados de desativados com tratamento especial"""
        try:
            file_path = "base_final_churn.xlsx"
            df_desativados = pd.read_excel(file_path)
            
            # Validar colunas necessárias (data pode vir como DAT_MOVIMENTO ou MES_MOVIMENTO)
            required_columns = ['COD_PLATAFORMA', 'DSC_REGIONAL_CMV', 'QTDE_AJUSTADA',
                               'FLG_SILENTE', 'DSC_CANAL_AJUSTADO', 'FLAG_INADIMPLENTE']
            missing_columns = [col for col in required_columns if col not in df_desativados.columns]
            
            if missing_columns:
                st.error(f"Colunas faltando no dataset de desativados: {missing_columns}")
                return pd.DataFrame()

            col_data = 'DAT_MOVIMENTO' if 'DAT_MOVIMENTO' in df_desativados.columns else (
                'MES_MOVIMENTO' if 'MES_MOVIMENTO' in df_desativados.columns else None
            )
            if col_data is None:
                st.error("Coluna de data ausente no dataset de desativados: esperado DAT_MOVIMENTO ou MES_MOVIMENTO")
                return pd.DataFrame()
            
            # Tratar coluna de regional (apenas 3 primeiros caracteres)
            df_desativados['REGIONAL'] = (
                df_desativados['DSC_REGIONAL_CMV'].astype(str).str.strip().str[:3].str.upper()
            )
            
            # Tratar coluna de data diária e fechar por mês
            df_desativados['DAT_MOVIMENTO2'] = pd.to_datetime(
                df_desativados[col_data], errors='coerce', dayfirst=True
            )
            df_desativados = df_desativados[df_desativados['DAT_MOVIMENTO2'].notna()].copy()
            
            # Criar coluna mes_ano no formato mm/aa (ex: jan/25)
            def formatar_mes_ano(dt):
                meses_pt = {
                    1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
                    7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
                }
                mes = meses_pt.get(dt.month, 'jan')
                ano = dt.strftime('%y')
                return f"{mes}/{ano}"
            
            df_desativados['mes_ano'] = df_desativados['DAT_MOVIMENTO2'].apply(formatar_mes_ano)
            
            # Renomear colunas para padronização
            df_desativados = df_desativados.rename(columns={
                'QTDE_AJUSTADA': 'QTDE',
                'DSC_CANAL_AJUSTADO': 'CANAL_PLAN',
                'FLAG_INADIMPLENTE': 'INADIMPLENTE'
            })
            
            # Garantir tipos numéricos e padronizar campos categóricos
            df_desativados['QTDE'] = pd.to_numeric(df_desativados['QTDE'], errors='coerce').fillna(0)
            df_desativados['FLG_SILENTE'] = pd.to_numeric(df_desativados['FLG_SILENTE'], errors='coerce').fillna(0)
            df_desativados['COD_PLATAFORMA'] = df_desativados['COD_PLATAFORMA'].astype(str).str.strip().str.upper()
            df_desativados['CANAL_PLAN'] = df_desativados['CANAL_PLAN'].astype(str).str.strip()
            
            # Criar coluna para quantidade silente (FLG_SILENTE = 1)
            df_desativados['QTDE_SILENTE'] = np.where(
                df_desativados['FLG_SILENTE'] == 1, df_desativados['QTDE'], 0
            )
            
            # Tratar inadimplente (aceita 1/0 e textos Sim/Não)
            inad_raw = df_desativados['INADIMPLENTE'].astype(str).str.strip().str.upper()
            inad_num = pd.to_numeric(df_desativados['INADIMPLENTE'], errors='coerce')
            mask_inad_sim = (inad_num == 1) | inad_raw.isin(['1', 'SIM', 'S', 'TRUE', 'VERDADEIRO'])
            df_desativados['INADIMPLENTE'] = np.where(mask_inad_sim, 'Sim', 'Não')
            
            return df_desativados
            
        except Exception as e:
            st.error(f"Erro ao carregar dados de desativados: {str(e)}")
            return pd.DataFrame()
    
    # Carregar dados
    df_desativados = load_desativados_data()
    
    if df_desativados.empty:
        st.warning("Não foi possível carregar os dados de desativados.")
        st.stop()
    
    # =========================
    # CABEÇALHO DA ABA
    # =========================
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📉</span>
            DESATIVADOS
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE DESATIVAÇÕES E CHURN
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================
    # FILTROS GERAIS (SIDEBAR)
    # =========================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📉 FILTROS DESATIVADOS")
    
    # Obter valores únicos
    regionais_disponiveis = sorted(df_desativados['REGIONAL'].dropna().unique().tolist())
    canais_disponiveis = sorted(df_desativados['CANAL_PLAN'].dropna().unique().tolist())
    meses_disponiveis = sorted(
        df_desativados['mes_ano'].dropna().unique().tolist(),
        key=mes_ano_para_data
    )
    inadimplentes_opcoes = sorted(df_desativados['INADIMPLENTE'].dropna().unique().tolist())
    
    # Aplicar filtros
    with st.sidebar:
        # Filtro de regional
        regionais_selecionadas = st.multiselect(
            "**Regional (Desativados):**",
            options=regionais_disponiveis,
            default=regionais_disponiveis,
            help="Selecione uma ou mais regionais",
            key="filtro_regional_desativados"
        )
        
        # Filtro de canal
        canais_selecionados = st.multiselect(
            "**Canal (Desativados):**",
            options=canais_disponiveis,
            default=canais_disponiveis,
            help="Selecione um ou mais canais",
            key="filtro_canal_desativados"
        )
        
        # Filtro de período
        periodos_selecionados = st.multiselect(
            "**Período (Desativados):**",
            options=meses_disponiveis,
            default=meses_disponiveis,
            help="Selecione um ou mais períodos",
            key="filtro_periodo_desativados"
        )
        
        # Filtro de inadimplência
        inadimplentes_selecionados = st.multiselect(
            "**Situação Inadimplência:**",
            options=inadimplentes_opcoes,
            default=inadimplentes_opcoes,
            help="Selecione situação de inadimplência",
            key="filtro_inadimplente_desativados"
        )
        
        st.markdown("---")
        
        # Resumo dos filtros
        total_registros = len(df_desativados)
        st.info(f"**Total de registros:** {total_registros:,}")
    
    # Aplicar filtros ao DataFrame
    df_filtrado = df_desativados[
        df_desativados['REGIONAL'].isin(regionais_selecionadas) &
        df_desativados['CANAL_PLAN'].isin(canais_selecionados) &
        df_desativados['mes_ano'].isin(periodos_selecionados) &
        df_desativados['INADIMPLENTE'].isin(inadimplentes_selecionados)
    ].copy()
    
    # =========================
    # CONTAINER PARA FILTRO DE MÊS COMPARTILHADO
    # =========================
    with st.container():
        st.markdown('<div class="filter-title">📅 SELECIONE O MÊS PARA ANÁLISE DE DESATIVADOS</div>', unsafe_allow_html=True)
        
        # Ordenar meses cronologicamente
        meses_disponiveis_cards = sorted(df_filtrado['mes_ano'].unique(), 
                                         key=lambda x: (int(x.split('/')[1]), 
                                                        ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 
                                                         'jul', 'ago', 'set', 'out', 'nov', 'dez'].index(x.split('/')[0])))
        
        # Selecionar mês mais recente como padrão
        if meses_disponiveis_cards:
            mes_padrao = meses_disponiveis_cards[-1]
            idx_padrao = meses_disponiveis_cards.index(mes_padrao)
        else:
            meses_disponiveis_cards = ['jan/24']
            idx_padrao = 0
        
        # Selectbox para seleção do mês
        col_filtro1, col_filtro2 = st.columns([1, 3])
        
        with col_filtro1:
            mes_selecionado = st.selectbox(
                "Selecione o mês para análise",
                options=meses_disponiveis_cards,
                index=idx_padrao,
                key="mes_compartilhado_desativados",
                label_visibility="collapsed"
            )
        
        # Encontrar mês anterior
        if len(meses_disponiveis_cards) > 1:
            try:
                idx_mes_atual = meses_disponiveis_cards.index(mes_selecionado)
                mes_anterior = meses_disponiveis_cards[idx_mes_atual - 1] if idx_mes_atual > 0 else mes_selecionado
            except:
                mes_anterior = meses_disponiveis_cards[0]
        else:
            mes_anterior = mes_selecionado
        
        # Container informativo
        with col_filtro2:
            st.markdown(f"""
                <div class="info-box" style="margin: 0; padding: 12px 15px;">
                    <div style="display: flex; align-items: center; gap: 15px; flex-wrap: nowrap; height: 100%;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Atual:</span>
                            <span style="font-size: 14px; color: #FF2800; font-weight: 800; 
                                    background: rgba(255, 40, 0, 0.1); padding: 6px 15px; border-radius: 20px;">
                                {mes_selecionado}
                            </span>
                        </div>
                        <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Anterior:</span>
                            <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                    background: rgba(121, 14, 9, 0.1); padding: 6px 15px; border-radius: 20px;">
                                {mes_anterior}
                            </span>
                        </div>
                        <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 13px; color: #333333; font-weight: 600;">Comparativo:</span>
                            <span style="font-size: 13px; color: #666666; font-weight: 600;">
                                MoM (Mês sobre Mês)
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # =========================
    # FUNÇÃO PARA CALCULAR MÉTRICAS POR CANAL
    # =========================
    def calcular_metricas_canal_desativados(canal, mes_atual, mes_anterior):
        """Calcula métricas de desativados para um canal específico"""
        # Dados do mês atual
        df_mes_atual = df_filtrado.query(
            "CANAL_PLAN == @canal and mes_ano == @mes_atual"
        )
        
        # Dados do mês anterior
        df_mes_anterior = df_filtrado.query(
            "CANAL_PLAN == @canal and mes_ano == @mes_anterior"
        )
        
        # Calcular totais
        total_atual = df_mes_atual['QTDE'].sum()
        total_anterior = df_mes_anterior['QTDE'].sum()
        
        # Calcular silentes
        silentes_atual = df_mes_atual['QTDE_SILENTE'].sum()
        
        # Calcular variações
        variacao_mom = ((total_atual - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
        
        # Calcular percentual de silentes
        percent_silentes = (silentes_atual / total_atual * 100) if total_atual > 0 else 0
        
        return {
            'total_atual': total_atual,
            'total_anterior': total_anterior,
            'silentes_atual': silentes_atual,
            'variacao_mom': variacao_mom,
            'percent_silentes': percent_silentes
        }
    
    # =========================
    # CARDS KPI POR CANAL
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> PERFORMANCE POR CANAL - DESATIVADOS</div>', unsafe_allow_html=True)
    
    # Ordenar canais
    canais_ordenados = sorted(df_filtrado['CANAL_PLAN'].unique())
    num_canais = len(canais_ordenados)
    
    # Renderizar cards KPI
    for i in range(0, num_canais, 3):
        cols = st.columns(3, gap="medium")
        canais_linha = canais_ordenados[i:i+3]
        
        for j, canal in enumerate(canais_linha):
            metricas = calcular_metricas_canal_desativados(canal, mes_selecionado, mes_anterior)
            
            total_atual = metricas['total_atual']
            total_anterior = metricas['total_anterior']
            silentes_atual = metricas['silentes_atual']
            variacao_mom = metricas['variacao_mom']
            percent_silentes = metricas['percent_silentes']
            
            # Formatar valores
            total_atual_fmt = f"{total_atual:,.0f}".replace(",", ".")
            total_anterior_fmt = f"{total_anterior:,.0f}".replace(",", ".")
            silentes_fmt = f"{silentes_atual:,.0f}".replace(",", ".")
            
            # Determinar classes de variação
            classe_mom = "variacao-positiva" if variacao_mom < 0 else "variacao-negativa"
            classe_silentes = "variacao-negativa" if percent_silentes > 20 else "variacao-positiva"
            
            with cols[j]:
                st.markdown(
                    f"""
                    <div class="kpi-card-dinamico animate-fade-in-up">
                        <div class="kpi-title-dinamico">{canal}</div>
                        <div style="text-align: center; padding: 15px 0;">
                            <div class="kpi-value-dinamico">{total_atual_fmt}</div>
                            <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                                <span style="font-weight: 600;">Anterior ({mes_anterior}):</span> {total_anterior_fmt}<br>
                                <span style="font-weight: 600;">Silentes:</span> {silentes_fmt}
                            </div>
                            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                                <div class="kpi-variacao-item {classe_mom}" style="font-size: 10px !important;">
                                    {variacao_mom:+.0f}% MoM
                                </div>
                                <div class="kpi-variacao-item {classe_silentes}" style="font-size: 10px !important;">
                                    {percent_silentes:.0f}% Silentes
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # =========================
    # GRÁFICO DE DONUT - INADIMPLENTES vs NÃO INADIMPLENTES
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📈</span> DISTRIBUIÇÃO POR INADIMPLÊNCIA</div>', unsafe_allow_html=True)
    
    # Filtros para o gráfico de donut
    with st.container():
        col_filtro_donut1, col_filtro_donut2 = st.columns(2)
        
        with col_filtro_donut1:
            render_filter_label("CANAL")
            canal_donut = st.selectbox(
                "Selecione o Canal",
                options=["Todos"] + sorted(df_filtrado['CANAL_PLAN'].unique()),
                key="filtro_canal_donut",
                label_visibility="collapsed"
            )
        
        with col_filtro_donut2:
            render_filter_label("REGIONAL")
            regional_donut = st.selectbox(
                "Selecione a Regional",
                options=["Todos"] + sorted(df_filtrado['REGIONAL'].unique()),
                key="filtro_regional_donut",
                label_visibility="collapsed"
            )
    
    # Aplicar filtros para o donut
    df_donut = df_filtrado.copy()
    
    if canal_donut != "Todos":
        df_donut = df_donut[df_donut['CANAL_PLAN'] == canal_donut]
    
    if regional_donut != "Todos":
        df_donut = df_donut[df_donut['REGIONAL'] == regional_donut]
    
    # Calcular totais por inadimplência
    if not df_donut.empty:
        total_por_inadimplencia = df_donut.groupby('INADIMPLENTE')['QTDE'].sum().reset_index()
        total_geral_donut = total_por_inadimplencia['QTDE'].sum()
        
        # Calcular percentuais
        total_por_inadimplencia['Percentual'] = (total_por_inadimplencia['QTDE'] / total_geral_donut * 100).round(1)
        
        # Criar gráfico de donut
        fig_donut = px.pie(
            total_por_inadimplencia,
            values='QTDE',
            names='INADIMPLENTE',
            title=f'<b>DISTRIBUIÇÃO POR INADIMPLÊNCIA</b>',
            hole=0.6,
            color='INADIMPLENTE',
            color_discrete_map={
                'Sim': '#FF2800',
                'Não': '#790E09'
            }
        )
        
        # Atualizar layout
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>Percentual: %{percent}",
            marker=dict(line=dict(color='white', width=2))
        )
        
        fig_donut.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=14, color='#333333'),
            margin=dict(l=20, r=20, t=80, b=20),
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=16, color='#333333', weight=800),
                y=0.95
            ),
            showlegend=True,
            legend=dict(
                title=dict(text='<b>INADIMPLÊNCIA</b>', font=dict(size=14, weight=700, color='#333333')),
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            )
        )
        
        # Adicionar texto no centro
        fig_donut.add_annotation(
            text=f"<b>TOTAL</b><br>{total_geral_donut:,.0f}",
            x=0.5, y=0.5,
            font=dict(size=20, color='#333333', weight=800),
            showarrow=False
        )
        
        # Exibir gráfico
        st.plotly_chart(fig_donut, width='stretch', config={'displayModeBar': True, 'displaylogo': False})
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
    
    # =========================
    # GRÁFICO DE LINHAS TEMPORAL
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📈</span> EVOLUÇÃO MENSAL - DESATIVADOS</div>', unsafe_allow_html=True)
    
    # Filtros para o gráfico de linhas
    with st.container():
        col_filtro_linha1, col_filtro_linha2 = st.columns(2)
        
        with col_filtro_linha1:
            render_filter_label("CANAL")
            canal_linha = st.selectbox(
                "Selecione o Canal",
                options=["Todos"] + sorted(df_filtrado['CANAL_PLAN'].unique()),
                key="filtro_canal_linha",
                label_visibility="collapsed"
            )
        
        with col_filtro_linha2:
            render_filter_label("REGIONAL")
            regional_linha = st.selectbox(
                "Selecione a Regional",
                options=["Todos"] + sorted(df_filtrado['REGIONAL'].unique()),
                key="filtro_regional_linha",
                label_visibility="collapsed"
            )
    
    # Aplicar filtros para o gráfico de linhas
    df_linhas = df_filtrado.copy()
    
    if canal_linha != "Todos":
        df_linhas = df_linhas[df_linhas['CANAL_PLAN'] == canal_linha]
    
    if regional_linha != "Todos":
        df_linhas = df_linhas[df_linhas['REGIONAL'] == regional_linha]
    
    # Preparar dados para o gráfico de linhas
    if not df_linhas.empty:
        # Extrair ano e mês
        df_linhas['ANO'] = df_linhas['DAT_MOVIMENTO2'].dt.year
        df_linhas['MES_NUM'] = df_linhas['DAT_MOVIMENTO2'].dt.month
        
        # Mapear meses
        meses_abreviados = {
            1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
            7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
        }
        
        # Criar DataFrame para o gráfico
        dados_grafico = []
        anos_disponiveis = sorted(df_linhas['ANO'].unique())
        
        for ano in anos_disponiveis:
            df_ano = df_linhas[df_linhas['ANO'] == ano]
            for mes_num in range(1, 13):
                df_mes = df_ano[df_ano['MES_NUM'] == mes_num]
                total = df_mes['QTDE'].sum()
                
                dados_grafico.append({
                    'Ano': str(ano),
                    'Mês': meses_abreviados.get(mes_num, str(mes_num)),
                    'Mês_Num': mes_num,
                    'Valor': total,
                    'Tipo': 'Real'
                })
        
        df_linhas_grafico = pd.DataFrame(dados_grafico)
        df_linhas_grafico['Mês_Ord'] = df_linhas_grafico['Mês_Num']
        df_linhas_grafico = df_linhas_grafico.sort_values(['Ano', 'Mês_Ord'])
        df_linhas_grafico['Valor_Formatado'] = df_linhas_grafico['Valor'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
        
        # Criar título dinâmico
        filtros_ativos = []
        if canal_linha != "Todos":
            filtros_ativos.append(f"Canal: {canal_linha}")
        if regional_linha != "Todos":
            filtros_ativos.append(f"Regional: {regional_linha}")
        
        titulo_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Todos os Filtros"
        
        # Criar gráfico
        cores_personalizadas = {
            '2024': '#FF2800',
            '2025': '#790E09',
            '2026': '#5A6268'
        }
        
        # Filtrar apenas anos com dados
        anos_com_dados = sorted(df_linhas_grafico['Ano'].unique())
        color_map = {ano: cores_personalizadas.get(int(ano), '#666666') for ano in anos_com_dados}
        
        fig_linhas = px.line(
            df_linhas_grafico,
            x='Mês',
            y='Valor',
            color='Ano',
            title=f'<b>EVOLUÇÃO MENSAL DE DESATIVADOS</b><br><span style="font-size: 14px; color: #666666;">{titulo_filtros}</span>',
            labels={'Valor': 'Volume', 'Mês': ''},
            markers=True,
            line_shape='spline',
            color_discrete_map=color_map,
            text='Valor_Formatado'
        )
        
        fig_linhas.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=14, color='#333333'),
            margin=dict(l=60, r=60, t=100, b=80),
            xaxis=dict(
                title='',
                tickmode='array',
                tickvals=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
                tickfont=dict(size=13, color='#666666', weight=600),
                showgrid=True,
                gridcolor='rgba(233, 236, 239, 0.5)',
                gridwidth=1,
                linecolor='#E9ECEF',
                linewidth=2,
                mirror=True,
                tickangle=0,
                showline=True,
                zeroline=False
            ),
            yaxis=dict(
                title='<b>VOLUME DE DESATIVADOS</b>',
                title_font=dict(size=15, weight=700, color='#333333'),
                tickfont=dict(size=13, color='#666666', weight=600),
                showgrid=True,
                gridcolor='rgba(233, 236, 239, 0.5)',
                gridwidth=1,
                linecolor='#E9ECEF',
                linewidth=2,
                mirror=True,
                showline=True,
                zeroline=False
            ),
            legend=dict(
                title=dict(text='<b>ANO</b>', font=dict(size=14, weight=700, color='#333333')),
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#E9ECEF',
                borderwidth=2,
                font=dict(size=13, color='#333333', weight=600),
                itemwidth=50,
                traceorder='normal'
            ),
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=16, color='#333333', weight=800),
                y=0.95
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='white',
                font_size=14,
                font_family='Segoe UI',
                bordercolor='#E9ECEF',
                font_color='#333333',
                font_weight=600
            ),
            height=500,
            showlegend=True
        )
        
        for i, trace in enumerate(fig_linhas.data):
            ano = trace.name
            trace.update(
                mode='lines+markers+text',
                marker=dict(size=12, line=dict(width=2, color='white'), symbol='circle', opacity=0.9),
                line=dict(width=4, smoothing=1.3),
                textposition='top center',
                textfont=dict(size=12, color=color_map.get(ano, '#666666'), weight=700),
                hovertemplate=(
                    f"<b>%{{x}}/{ano}</b><br>" +
                    "<b>Valor:</b> %{y:,.0f}<br>" +
                    "<extra></extra>"
                )
            )
        
        # Container de informações
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                        padding: 15px 20px; 
                        border-radius: 12px; 
                        border: 2px solid #E9ECEF;
                        margin: 15px 0 5px 0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                    <div style="font-size: 14px; color: #333333; font-weight: 700;">
                        <span>📊 Dados Filtrados:</span>
                        <span style="color: #FF2800; margin-left: 8px;">{len(df_linhas):,}</span>
                    </div>
                    <div style="font-size: 13px; color: #666666; display: flex; gap: 20px; flex-wrap: wrap;">
        """, unsafe_allow_html=True)
        
        # Adicionar legendas de cores
        for ano, cor in color_map.items():
            st.markdown(f"""
                <span style="display: inline-flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; background: {cor}; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                    <span style="font-weight: 600;">{ano} (Real)</span>
                </span>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Exibir gráfico
        st.plotly_chart(fig_linhas, width='stretch', config={'displayModeBar': True, 'displaylogo': False})
    
    # =========================
    # GRÁFICO DE BARRAS HORIZONTAIS
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> DESATIVADOS vs SILENTES POR CANAL</div>', unsafe_allow_html=True)
    
    # Filtrar dados para o mês selecionado
    df_mes_selecionado = df_filtrado[df_filtrado['mes_ano'] == mes_selecionado]
    
    if not df_mes_selecionado.empty:
        # Agrupar por canal
        dados_barras = df_mes_selecionado.groupby('CANAL_PLAN').agg({
            'QTDE': 'sum',
            'QTDE_SILENTE': 'sum'
        }).reset_index()
        
        # Calcular percentual de silentes
        dados_barras['Percentual_Silentes'] = (dados_barras['QTDE_SILENTE'] / dados_barras['QTDE'] * 100).round(1)
        
        # Ordenar por total de desativados (maior para menor)
        dados_barras = dados_barras.sort_values('QTDE', ascending=False).reset_index(drop=True)
        
        # Rótulos de dados
        labels_total = dados_barras['QTDE'].apply(lambda x: formatar_numero_brasileiro(x, 0))
        labels_silente = dados_barras.apply(
            lambda row: f"{formatar_numero_brasileiro(row['QTDE_SILENTE'], 0)} ({row['Percentual_Silentes']:.1f}%)",
            axis=1
        )
        
        # Criar gráfico de barras verticais agrupadas (não empilhadas)
        fig_barras = go.Figure()
        
        fig_barras.add_trace(go.Bar(
            x=dados_barras['CANAL_PLAN'],
            y=dados_barras['QTDE'],
            name='Total Desativados',
            marker=dict(color='#790E09'),
            text=labels_total,
            textposition='outside',
            cliponaxis=False,
            hovertemplate='<b>Canal:</b> %{x}<br><b>Total Desativados:</b> %{y:,.0f}<extra></extra>'
        ))
        
        fig_barras.add_trace(go.Bar(
            x=dados_barras['CANAL_PLAN'],
            y=dados_barras['QTDE_SILENTE'],
            name='Silentes',
            marker=dict(color='#FF2800'),
            text=labels_silente,
            textposition='outside',
            cliponaxis=False,
            customdata=dados_barras['Percentual_Silentes'],
            hovertemplate='<b>Canal:</b> %{x}<br><b>Silentes:</b> %{y:,.0f}<br><b>% Silentes:</b> %{customdata:.1f}%<extra></extra>'
        ))
        
        y_max = max(
            float(dados_barras['QTDE'].max()) if not dados_barras.empty else 0.0,
            float(dados_barras['QTDE_SILENTE'].max()) if not dados_barras.empty else 0.0
        )
        y_top = y_max * 1.30 if y_max > 0 else 1
        
        # Atualizar layout
        fig_barras.update_layout(
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=14, color='#333333'),
            margin=dict(l=20, r=20, t=80, b=90),
            height=520,
            xaxis=dict(
                title='<b>CANAL</b>',
                title_font=dict(size=16, weight=800, color='#333333'),
                tickfont=dict(size=12, color='#666666', weight=600),
                showgrid=False,
                linecolor='#E9ECEF',
                linewidth=2,
                tickangle=-15,
                categoryorder='array',
                categoryarray=dados_barras['CANAL_PLAN'].tolist()
            ),
            yaxis=dict(
                title='<b>QUANTIDADE</b>',
                title_font=dict(size=16, weight=800, color='#333333'),
                tickfont=dict(size=13, color='#666666', weight=600),
                gridcolor='rgba(233, 236, 239, 0.7)',
                showgrid=True,
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor='#E9ECEF',
                linewidth=2,
                range=[0, y_top]
            ),
            legend=dict(
                title=dict(text='<b>TIPO</b>', font=dict(size=14, weight=800, color='#333333')),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0.0,
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#E9ECEF',
                borderwidth=1,
                font=dict(size=12, color='#333333', weight=600),
                traceorder='normal'
            ),
            title=dict(
                text=f'<b>DESATIVADOS vs SILENTES - {mes_selecionado}</b>',
                x=0.02,
                xanchor='left',
                yanchor='top',
                font=dict(size=16, color='#333333', weight=800),
                y=0.95
            ),
            hovermode='x unified',
            bargap=0.32,
            bargroupgap=0.12
        )
        
        fig_barras.update_traces(
            marker_line_color='white',
            marker_line_width=1.2
        )
        
        # Exibir gráfico
        st.plotly_chart(fig_barras, width='stretch', config={'displayModeBar': True, 'displaylogo': False})
        
        # KPIs de resumo
        total_desativados = dados_barras['QTDE'].sum()
        total_silentes = dados_barras['QTDE_SILENTE'].sum()
        percentual_silentes = (total_silentes / total_desativados * 100) if total_desativados > 0 else 0
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        with col_kpi1:
            st.metric(
                label="Total Desativados",
                value=f"{total_desativados:,.0f}".replace(",", "."),
                delta=None
            )
        
        with col_kpi2:
            st.metric(
                label="Total Silentes",
                value=f"{total_silentes:,.0f}".replace(",", "."),
                delta=f"{percentual_silentes:.1f}%"
            )
        
        with col_kpi3:
            canal_maior_silentes = dados_barras.loc[dados_barras['QTDE_SILENTE'].idxmax(), 'CANAL_PLAN'] if not dados_barras.empty else "N/A"
            st.metric(
                label="Canal com Mais Silentes",
                value=canal_maior_silentes,
                delta=None
            )
    
    # =========================
    # TABELA DINÂMICA POR REGIONAL
    # =========================
    st.markdown('<div class="section-title"><span class="section-icon">📋</span> DESATIVADOS POR REGIONAL</div>', unsafe_allow_html=True)

    # Filtros específicos da tabela dinâmica (Canal, Silente e Inadimplente)
    col_filtro_tab_des1, col_filtro_tab_des2, col_filtro_tab_des3 = st.columns([2, 1.2, 1.2])
    with col_filtro_tab_des1:
        canais_tabela_desativados = st.multiselect(
            "Filtrar Canal (Tabela):",
            options=["Todos"] + sorted(df_filtrado['CANAL_PLAN'].dropna().unique().tolist()),
            default=["Todos"],
            key="filtro_canal_tabela_desativados"
        )
    with col_filtro_tab_des2:
        silente_opcoes = sorted({
            str(int(v))
            for v in pd.to_numeric(df_filtrado['FLG_SILENTE'], errors='coerce').dropna().unique().tolist()
        })
        silentes_tabela_desativados = st.multiselect(
            "Filtrar Silente:",
            options=["Todos"] + silente_opcoes,
            default=["Todos"],
            key="filtro_silente_tabela_desativados"
        )
    with col_filtro_tab_des3:
        inad_opcoes = sorted(df_filtrado['INADIMPLENTE'].dropna().astype(str).unique().tolist())
        inadimplentes_tabela_desativados = st.multiselect(
            "Filtrar Inadimplente:",
            options=["Todos"] + inad_opcoes,
            default=["Todos"],
            key="filtro_inadimplente_tabela_desativados"
        )

    # Base filtrada só para a tabela
    df_filtrado_tabela_des = df_filtrado.copy()
    if "Todos" not in canais_tabela_desativados:
        df_filtrado_tabela_des = df_filtrado_tabela_des[
            df_filtrado_tabela_des['CANAL_PLAN'].isin(canais_tabela_desativados)
        ].copy()
    if "Todos" not in silentes_tabela_desativados:
        silentes_sel = {int(v) for v in silentes_tabela_desativados if str(v).isdigit()}
        if silentes_sel:
            df_filtrado_tabela_des = df_filtrado_tabela_des[
                pd.to_numeric(df_filtrado_tabela_des['FLG_SILENTE'], errors='coerce').fillna(-1).astype(int).isin(silentes_sel)
            ].copy()
    if "Todos" not in inadimplentes_tabela_desativados:
        df_filtrado_tabela_des = df_filtrado_tabela_des[
            df_filtrado_tabela_des['INADIMPLENTE'].astype(str).isin(inadimplentes_tabela_desativados)
        ].copy()
    
    # Preparar dados para tabela
    def criar_tabela_regional(df):
        """Cria tabela pivot por regional"""
        # Definir ordem dos meses
        meses_ordem = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        meses_2025 = [f'{mes}/25' for mes in meses_ordem]
        
        # Extrair ano da coluna mes_ano
        df = df.copy()
        df.loc[:, 'ano'] = df['mes_ano'].str.split('/').str[1]
        df.loc[:, 'mes_ano_formatado'] = df['mes_ano']
        
        # Agrupar por regional e mês
        pivot_data = []
        regionais = sorted(df['REGIONAL'].unique())
        
        for regional in regionais:
            df_regional = df[df['REGIONAL'] == regional]
            
            # Calcular totais por ano
            total_2024 = df_regional[df_regional['ano'] == '24']['QTDE'].sum()
            total_2025 = df_regional[df_regional['ano'] == '25']['QTDE'].sum()
            
            # Calcular silentes por ano
            silentes_2024 = df_regional[df_regional['ano'] == '24']['QTDE_SILENTE'].sum()
            silentes_2025 = df_regional[df_regional['ano'] == '25']['QTDE_SILENTE'].sum()
            
            # Calcular valores mensais para 2025
            valores_mensais_2025 = []
            silentes_mensais_2025 = []
            for mes in meses_2025:
                valor = df_regional[df_regional['mes_ano_formatado'] == mes]['QTDE'].sum()
                silente = df_regional[df_regional['mes_ano_formatado'] == mes]['QTDE_SILENTE'].sum()
                valores_mensais_2025.append(valor)
                silentes_mensais_2025.append(silente)
            
            # Calcular valor REAL de jan/26 (se existir)
            real_jan_26 = df_regional[df_regional['mes_ano_formatado'] == 'jan/26']['QTDE'].sum()
            silentes_jan_26 = df_regional[df_regional['mes_ano_formatado'] == 'jan/26']['QTDE_SILENTE'].sum()
            
            # Calcular variações
            variacao_2024_2025 = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
            
            # Calcular variação MoM (dez/25 vs nov/25)
            dez_25 = df_regional[df_regional['mes_ano_formatado'] == 'dez/25']['QTDE'].sum()
            nov_25 = df_regional[df_regional['mes_ano_formatado'] == 'nov/25']['QTDE'].sum()
            variacao_mom = ((dez_25 - nov_25) / nov_25 * 100) if nov_25 > 0 else 0
            
            # Calcular percentual de silentes
            percent_silentes_2025 = (silentes_2025 / total_2025 * 100) if total_2025 > 0 else 0
            
            pivot_data.append({
                'Regional': regional,
                'Total 2024': total_2024,
                'Silentes 2024': silentes_2024,
                **{meses_2025[i]: valores_mensais_2025[i] for i in range(12)},
                'Total 2025': total_2025,
                'Silentes 2025': silentes_2025,
                '% Silentes': percent_silentes_2025,
                'Real Jan/26': real_jan_26,
                'Silentes Jan/26': silentes_jan_26,
                'Var 2025/2024': variacao_2024_2025,
                'Var MoM': variacao_mom
            })
        
        return pivot_data, meses_2025
    
    # Garantir colunas auxiliares para agregações gerais
    if 'ano' not in df_filtrado_tabela_des.columns or 'mes_ano_formatado' not in df_filtrado_tabela_des.columns:
        df_filtrado_tabela_des = df_filtrado_tabela_des.copy()
        df_filtrado_tabela_des['ano'] = df_filtrado_tabela_des['mes_ano'].str.split('/').str[1]
        df_filtrado_tabela_des['mes_ano_formatado'] = df_filtrado_tabela_des['mes_ano']

    # Criar tabela pivot
    pivot_data, meses_2025 = criar_tabela_regional(df_filtrado_tabela_des)
    
    if pivot_data:
        # Ordenar por Total 2025
        df_temp = pd.DataFrame(pivot_data)
        df_temp = df_temp.sort_values('Total 2025', ascending=False)
        pivot_data_ordenada = df_temp.to_dict('records')
        
        # Calcular totais gerais
        total_2024_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['ano'] == '24']['QTDE'].sum()
        total_2025_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['ano'] == '25']['QTDE'].sum()
        silentes_2024_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['ano'] == '24']['QTDE_SILENTE'].sum()
        silentes_2025_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['ano'] == '25']['QTDE_SILENTE'].sum()
        
        # Calcular valores mensais gerais
        valores_mensais_2025_geral = []
        silentes_mensais_2025_geral = []
        for mes in meses_2025:
            valor = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == mes]['QTDE'].sum()
            silente = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == mes]['QTDE_SILENTE'].sum()
            valores_mensais_2025_geral.append(valor)
            silentes_mensais_2025_geral.append(silente)
        
        # Calcular REAL geral jan/26
        real_jan_26_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == 'jan/26']['QTDE'].sum()
        silentes_jan_26_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == 'jan/26']['QTDE_SILENTE'].sum()
        
        # Calcular variações gerais
        variacao_2024_2025_geral = ((total_2025_geral - total_2024_geral) / total_2024_geral * 100) if total_2024_geral > 0 else 0
        
        # Calcular variação MoM geral
        dez_25_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == 'dez/25']['QTDE'].sum()
        nov_25_geral = df_filtrado_tabela_des[df_filtrado_tabela_des['mes_ano_formatado'] == 'nov/25']['QTDE'].sum()
        variacao_mom_geral = ((dez_25_geral - nov_25_geral) / nov_25_geral * 100) if nov_25_geral > 0 else 0
        
        # Calcular percentual de silentes
        percent_silentes_geral = (silentes_2025_geral / total_2025_geral * 100) if total_2025_geral > 0 else 0
        
        # Adicionar linha de TOTAL
        linha_total = {
            'Regional': 'TOTAL',
            'Total 2024': total_2024_geral,
            'Silentes 2024': silentes_2024_geral,
            **{meses_2025[i]: valores_mensais_2025_geral[i] for i in range(12)},
            'Total 2025': total_2025_geral,
            'Silentes 2025': silentes_2025_geral,
            '% Silentes': percent_silentes_geral,
            'Real Jan/26': real_jan_26_geral,
            'Silentes Jan/26': silentes_jan_26_geral,
            'Var 2025/2024': variacao_2024_2025_geral,
            'Var MoM': variacao_mom_geral
        }
        
        # Criar DataFrame final
        df_final = pd.DataFrame([linha_total] + pivot_data_ordenada)
        
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
            if col not in ['Regional', 'Var 2025/2024', 'Var MoM', '% Silentes']:
                df_exibicao[col] = df_exibicao[col].apply(formatar_numero)
            else:
                df_exibicao[col] = df_exibicao[col].apply(formatar_percentual)
        
        # Criar tabela HTML estilizada
        def criar_tabela_html_desativados(df):
            html = """
            <style>
                .tabela-container-desativados {
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
                
                .tabela-desativados {
                    width: 100%;
                    border-collapse: collapse;
                    border-spacing: 0;
                    font-size: 13px;
                    line-height: 1.5;
                }
                
                .tabela-desativados thead {
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                
            .tabela-desativados th {
                    background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                    color: white !important;
                    font-weight: 600;
                    padding: 9px 8px; /* reduced height */
                    text-align: center;
                    border-bottom: 3px solid #5A0A06;
                    border-right: 1px solid rgba(255, 255, 255, 0.15);
                    white-space: nowrap;
                    font-size: 12px;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                    position: relative;
                }
                
                .tabela-desativados th:first-child {
                    border-left: none;
                    border-top-left-radius: 8px;
                }
                
                .tabela-desativados th:last-child {
                    border-right: none;
                    border-top-right-radius: 8px;
                }
                
                .tabela-desativados td {
                    padding: 8px 8px; /* reduced height */
                    text-align: center;
                    border-bottom: 1px solid #E8E8E8;
                    border-right: 1px solid #F0F0F0;
                    font-weight: 400;
                }
                
                .tabela-desativados tr:not(.linha-total-desativados) td:first-child {
                    border-left: none;
                    text-align: left;
                    font-weight: 600;
                    color: #333;
                    background: linear-gradient(90deg, #fef5f4 0%, white 100%) !important;
                    padding-left: 15px;
                }
                
                .tabela-desativados td:last-child {
                    border-right: none;
                }
                
                .linha-total-desativados {
                    background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                    color: white !important;
                    position: sticky;
                    bottom: 0;
                    z-index: 50;
                    border-top: 2px solid #790E09;
                }
                
                .linha-total-desativados td {
                    background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                    color: white !important;
                    border-bottom: none;
                    font-weight: 700;
                    font-size: 14px;
                    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                }
                
                .linha-total-desativados td:first-child {
                    font-weight: 800;
                }
                
                .linha-regional-desativados:nth-child(even) {
                    background-color: #FFF9F8 !important;
                }
                
                .linha-regional-desativados:nth-child(odd) {
                    background-color: white !important;
                }
                
                .linha-regional-desativados:hover {
                    background-color: #FFEBEE !important;
                }
                
                .tabela-container-desativados::-webkit-scrollbar {
                    width: 10px;
                    height: 10px;
                }
                
                .tabela-container-desativados::-webkit-scrollbar-track {
                    background: #F5F5F5;
                    border-radius: 10px;
                }
                
                .tabela-container-desativados::-webkit-scrollbar-thumb {
                    background: linear-gradient(135deg, #A23B36 0%, #790E09 100%);
                    border-radius: 10px;
                    border: 2px solid #F5F5F5;
                }

                /* Unified table visual override */
                .tabela-desativados th {
                    padding: 9px 7px !important;
                    font-size: 10.5px !important;
                    box-shadow: none !important;
                }

                .tabela-desativados td {
                    padding: 7px 7px !important;
                    font-size: 10.5px !important;
                    line-height: 1.25 !important;
                    box-shadow: none !important;
                }

                .tabela-desativados td:not(:first-child) {
                    text-align: right !important;
                    font-variant-numeric: tabular-nums;
                }

                .linha-regional-desativados:hover {
                    background-color: #FFF2EF !important;
                    box-shadow: inset 0 0 0 1px #FFD9CF !important;
                }
            </style>
            
            <div class="tabela-container-desativados">
            <table class="tabela-desativados">
            <thead>
                <tr>
            """
            
            for col in df.columns:
                html += f'<th>{col}</th>'
            
            html += "</tr></thead><tbody>"
            
            for idx, row in df.iterrows():
                is_total = row['Regional'] == 'TOTAL'
                classe_linha = "linha-total-desativados" if is_total else "linha-regional-desativados"
                html += f'<tr class="{classe_linha}">'
                
                for col in df.columns:
                    valor = row[col]
                    html += f'<td>{valor}</td>'
                
                html += "</tr>"
            
            html += "</tbody></table></div>"
            return html
        
        # Exibir tabela
        st.markdown(criar_tabela_html_desativados(df_exibicao), unsafe_allow_html=True)
        
        # Botões de exportação
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            @st.cache_data
            def exportar_excel_tabela(df_numerico):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_numerico.to_excel(writer, index=False, sheet_name='Tabela_Desativados')
                return output.getvalue()
            
            excel_data = exportar_excel_tabela(df_final)
            st.download_button(
                label="📥 Exportar Excel",
                data=excel_data,
                file_name="tabela_desativados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col_exp2:
            @st.cache_data
            def exportar_csv_tabela(df_numerico):
                return df_numerico.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
            
            csv_data = exportar_csv_tabela(df_final)
            st.download_button(
                label="📄 Exportar CSV",
                data=csv_data,
                file_name="tabela_desativados.csv",
                mime="text/csv",
                use_container_width=True
            )

# =========================
# ABA 3: PEDIDOS
# =========================
with tab3:
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📋</span>
            PEDIDOS E-Commerce
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE PEDIDOS E CONVERSÃO - E-Commerce
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================
    # FILTRAR DADOS PARA PEDIDOS E-Commerce (usando base original, sem filtros globais)
    # Regras:
    # - DSC_INDICADOR = PEDIDOS
    # - CANAL_PLAN = E-Commerce
    # - Realizado = soma de QTDE
    # - Meta = soma de DESAFIO_QTD
    # - Período baseado em DAT_MOVIMENTO2
    # =========================
    df_pedidos = load_data(file_path).copy()

    # Normalizar regional para evitar tabela vazia por coluna inconsistente
    if 'REGIONAL' not in df_pedidos.columns and 'DSC_REGIONAL_CMV' in df_pedidos.columns:
        df_pedidos['REGIONAL'] = df_pedidos['DSC_REGIONAL_CMV'].astype(str).str.strip().str[:3].str.upper()
    elif 'REGIONAL' in df_pedidos.columns:
        df_pedidos['REGIONAL'] = df_pedidos['REGIONAL'].astype(str).str.strip().str[:3].str.upper()

    # Identificar coluna de canal (fallback para bases antigas)
    coluna_canal = 'CANAL_PLAN' if 'CANAL_PLAN' in df_pedidos.columns else ('DSC_CANAL' if 'DSC_CANAL' in df_pedidos.columns else None)

    if 'DSC_INDICADOR' not in df_pedidos.columns or coluna_canal is None:
        st.error("❌ Base de pedidos sem colunas obrigatórias (DSC_INDICADOR/CANAL_PLAN).")
        df_pedidos = pd.DataFrame()
    else:
        indicador_norm = df_pedidos['DSC_INDICADOR'].astype(str).str.strip().str.upper()
        canal_norm = df_pedidos[coluna_canal].astype(str).str.strip().str.upper()

        mask_indicador = indicador_norm == 'PEDIDOS'
        mask_canal = canal_norm == 'E-COMMERCE'

        df_pedidos = df_pedidos.loc[mask_indicador & mask_canal].copy()

    if not df_pedidos.empty:
        # Garantir base temporal em DAT_MOVIMENTO2
        if 'DAT_MOVIMENTO2' in df_pedidos.columns:
            df_pedidos['DAT_MOVIMENTO2'] = pd.to_datetime(df_pedidos['DAT_MOVIMENTO2'], errors='coerce')
        elif 'PERIODO' in df_pedidos.columns:
            df_pedidos['DAT_MOVIMENTO2'] = pd.to_datetime(df_pedidos['PERIODO'], errors='coerce')
        else:
            df_pedidos['DAT_MOVIMENTO2'] = pd.NaT

        # Criar dat_tratada a partir de DAT_MOVIMENTO2 para padronizar os pivots
        meses_pt = {
            1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
            7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
        }

        def _fmt_mes_ano_pedidos(dt):
            if pd.isna(dt):
                return None
            return f"{meses_pt.get(dt.month, 'jan')}/{dt.strftime('%y')}"

        df_pedidos['dat_tratada'] = df_pedidos['DAT_MOVIMENTO2'].apply(_fmt_mes_ano_pedidos)
        df_pedidos = df_pedidos[df_pedidos['dat_tratada'].notna()].copy()

        # Garantir colunas numéricas
        if 'QTDE' not in df_pedidos.columns and 'QTDE_AJUSTADA' in df_pedidos.columns:
            df_pedidos['QTDE'] = pd.to_numeric(df_pedidos['QTDE_AJUSTADA'], errors='coerce')
        else:
            df_pedidos['QTDE'] = pd.to_numeric(df_pedidos.get('QTDE', 0), errors='coerce')

        df_pedidos['DESAFIO_QTD'] = pd.to_numeric(df_pedidos.get('DESAFIO_QTD', 0), errors='coerce')
        df_pedidos['QTDE'] = df_pedidos['QTDE'].fillna(0)
        df_pedidos['DESAFIO_QTD'] = df_pedidos['DESAFIO_QTD'].fillna(0)
    
    if df_pedidos.empty:
        st.warning("⚠️ Não há dados de pedidos disponíveis para E-Commerce com os filtros atuais.")
        st.info("Verifique se os filtros gerais incluem 'PEDIDOS' no indicador e 'E-Commerce' no canal.")
    else:
        # =========================
        # CONTAINER PARA FILTRO DE MÊS COMPARTILHADO
        # =========================
        with st.container():
            st.markdown('<div class="filter-title">📅 SELECIONE O MÊS PARA ANÁLISE DE PEDIDOS</div>', unsafe_allow_html=True)
            
            # Obter meses disponíveis e ordenar cronologicamente
            meses_disponiveis_pedidos = df_pedidos['dat_tratada'].dropna().unique()
            
            # Função para converter string 'mes/ano' para objeto datetime
            def mes_ano_para_data_pedidos(mes_ano_str):
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
            meses_com_datas_pedidos = []
            for mes in meses_disponiveis_pedidos:
                try:
                    data = mes_ano_para_data_pedidos(mes)
                    meses_com_datas_pedidos.append((mes, data))
                except:
                    meses_com_datas_pedidos.append((mes, datetime(1900, 1, 1)))
            
            # Ordenar por data
            meses_com_datas_pedidos.sort(key=lambda x: x[1])
            meses_ordenados_pedidos = [mes for mes, _ in meses_com_datas_pedidos]
            
            # Encontrar índice do mês atual (dez/25)
            if 'dez/25' in meses_ordenados_pedidos:
                idx_padrao_pedidos = meses_ordenados_pedidos.index('dez/25')
            else:
                idx_padrao_pedidos = len(meses_ordenados_pedidos) - 1
            
            # Selectbox para seleção do mês
            col_filtro_pedidos1, col_filtro_pedidos2 = st.columns([1, 3])
            
            with col_filtro_pedidos1:
                mes_selecionado_pedidos = st.selectbox(
                    "Selecione o mês para análise",
                    options=meses_ordenados_pedidos,
                    index=idx_padrao_pedidos,
                    key="mes_compartilhado_pedidos",
                    label_visibility="collapsed"
                )
            
            # Encontrar o mês anterior cronologicamente
            if len(meses_ordenados_pedidos) > 1:
                try:
                    idx_mes_atual_pedidos = meses_ordenados_pedidos.index(mes_selecionado_pedidos)
                    mes_anterior_pedidos = meses_ordenados_pedidos[idx_mes_atual_pedidos - 1] if idx_mes_atual_pedidos > 0 else mes_selecionado_pedidos
                except:
                    mes_anterior_pedidos = meses_ordenados_pedidos[0] if len(meses_ordenados_pedidos) > 0 else mes_selecionado_pedidos
            else:
                mes_anterior_pedidos = mes_selecionado_pedidos
            
            # Container informativo
            with col_filtro_pedidos2:
                st.markdown(f"""
                    <div class="info-box" style="margin: 0; padding: 12px 15px;">
                        <div style="display: flex; align-items: center; gap: 15px; flex-wrap: nowrap; height: 100%;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Atual:</span>
                                <span style="font-size: 14px; color: #FF2800; font-weight: 800; 
                                        background: rgba(255, 40, 0, 0.1); padding: 6px 15px; border-radius: 20px;">
                                    {mes_selecionado_pedidos}
                                </span>
                            </div>
                            <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 13px; color: #333333; font-weight: 600;">Mês Anterior:</span>
                                <span style="font-size: 14px; color: #790E09; font-weight: 700; 
                                        background: rgba(121, 14, 9, 0.1); padding: 6px 15px; border-radius: 20px;">
                                    {mes_anterior_pedidos}
                                </span>
                            </div>
                            <div style="width: 1px; height: 30px; background: #E9ECEF;"></div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 13px; color: #333333; font-weight: 600;">Comparativo:</span>
                                <span style="font-size: 13px; color: #666666; font-weight: 600;">
                                    MoM (Mês sobre Mês)
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # =========================
        # FUNÇÃO PARA CALCULAR MÉTRICAS DE PEDIDOS
        # =========================
        def calcular_metricas_pedidos(plataforma, mes_atual, mes_anterior):
            """Calcula métricas de pedidos para uma plataforma específica"""
            # Realizado no mês atual (QTDE)
            realizado_atual = df_pedidos.query(
                "COD_PLATAFORMA == @plataforma and dat_tratada == @mes_atual"
            )['QTDE'].sum()
            
            # Realizado no mês anterior (QTDE)
            realizado_anterior = df_pedidos.query(
                "COD_PLATAFORMA == @plataforma and dat_tratada == @mes_anterior"
            )['QTDE'].sum()
            
            # Meta no mês atual (DESAFIO_QTD)
            meta_atual = df_pedidos.query(
                "COD_PLATAFORMA == @plataforma and dat_tratada == @mes_atual"
            )['DESAFIO_QTD'].sum()
            
            # Calcular variações
            variacao_mom = ((realizado_atual - realizado_anterior) / realizado_anterior * 100) if realizado_anterior > 0 else 0
            
            if meta_atual > 0:
                desvio_meta = ((realizado_atual / meta_atual) - 1) * 100
            else:
                desvio_meta = None
            
            return {
                'realizado': realizado_atual,
                'anterior': realizado_anterior,
                'meta': meta_atual,
                'variacao_mom': variacao_mom,
                'desvio_meta': desvio_meta
            }
        
        # =========================
        # CARDS KPI PARA CONTA E FIXA
        # =========================
        st.markdown('<div class="section-title"><span class="section-icon">📊</span> PERFORMANCE DE PEDIDOS POR MÊS</div>', unsafe_allow_html=True)
        
        # Calcular métricas para CONTA e FIXA
        metricas_conta = calcular_metricas_pedidos('CONTA', mes_selecionado_pedidos, mes_anterior_pedidos)
        metricas_fixa = calcular_metricas_pedidos('FIXA', mes_selecionado_pedidos, mes_anterior_pedidos)
        
        # Formatar valores
        realizado_conta_fmt = f"{metricas_conta['realizado']:,.0f}".replace(",", ".")
        anterior_conta_fmt = f"{metricas_conta['anterior']:,.0f}".replace(",", ".")
        meta_conta_fmt = f"{metricas_conta['meta']:,.0f}".replace(",", ".")
        
        realizado_fixa_fmt = f"{metricas_fixa['realizado']:,.0f}".replace(",", ".")
        anterior_fixa_fmt = f"{metricas_fixa['anterior']:,.0f}".replace(",", ".")
        meta_fixa_fmt = f"{metricas_fixa['meta']:,.0f}".replace(",", ".")
        
        # Determinar classes de variação
        classe_mom_conta = "variacao-positiva" if metricas_conta['variacao_mom'] >= 0 else "variacao-negativa"
        classe_mom_fixa = "variacao-positiva" if metricas_fixa['variacao_mom'] >= 0 else "variacao-negativa"
        
        # HTML para meta
        if metricas_conta['desvio_meta'] is not None:
            classe_meta_conta = "variacao-positiva" if metricas_conta['desvio_meta'] >= 0 else "variacao-negativa"
            meta_html_conta = f'<div class="kpi-variacao-item {classe_meta_conta}" style="font-size: 10px !important;">{metricas_conta["desvio_meta"]:+.0f}% Meta</div>'
        else:
            meta_html_conta = '<div class="kpi-variacao-item" style="background: #F5F5F5 !important; color: #666666 !important; border: 1.5px solid #E0E0E0 !important; font-size: 10px !important;">Meta N/A</div>'
        
        if metricas_fixa['desvio_meta'] is not None:
            classe_meta_fixa = "variacao-positiva" if metricas_fixa['desvio_meta'] >= 0 else "variacao-negativa"
            meta_html_fixa = f'<div class="kpi-variacao-item {classe_meta_fixa}" style="font-size: 10px !important;">{metricas_fixa["desvio_meta"]:+.0f}% Meta</div>'
        else:
            meta_html_fixa = '<div class="kpi-variacao-item" style="background: #F5F5F5 !important; color: #666666 !important; border: 1.5px solid #E0E0E0 !important; font-size: 10px !important;">Meta N/A</div>'
        
        # Layout: coluna esquerda com cards empilhados, coluna direita com donut
        col_cards, col_donut = st.columns([1, 1])
        
        with col_cards:
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up" style="margin-bottom:14px;">
                    <div class="kpi-title-dinamico">PEDIDOS CONTA</div>
                    <div style="text-align: center; padding: 12px 0;">
                        <div class="kpi-value-dinamico">{realizado_conta_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior_pedidos}):</span> {anterior_conta_fmt}<br>
                            <span style="font-weight: 600;">Meta ({mes_selecionado_pedidos}):</span> {meta_conta_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 12px;">
                            <div class="kpi-variacao-item {classe_mom_conta}" style="font-size: 10px !important;">
                                {metricas_conta['variacao_mom']:+.0f}% MoM
                            </div>
                            {meta_html_conta}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up">
                    <div class="kpi-title-dinamico">PEDIDOS FIXA</div>
                    <div style="text-align: center; padding: 12px 0;">
                        <div class="kpi-value-dinamico">{realizado_fixa_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior_pedidos}):</span> {anterior_fixa_fmt}<br>
                            <span style="font-weight: 600;">Meta ({mes_selecionado_pedidos}):</span> {meta_fixa_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 12px;">
                            <div class="kpi-variacao-item {classe_mom_fixa}" style="font-size: 10px !important;">
                                {metricas_fixa['variacao_mom']:+.0f}% MoM
                            </div>
                            {meta_html_fixa}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_donut:
            total_conta = metricas_conta['realizado']
            total_fixa = metricas_fixa['realizado']
            total_geral_pedidos = total_conta + total_fixa

            df_donut = pd.DataFrame({
                'Plataforma': ['CONTA', 'FIXA'],
                'Quantidade': [total_conta, total_fixa]
            })

            df_donut['Percentual'] = (df_donut['Quantidade'] / df_donut['Quantidade'].sum() * 100).round(1)

            fig_donut = px.pie(
                df_donut,
                values='Quantidade',
                names='Plataforma',
                title='',
                hole=0.6,
                color='Plataforma',
                color_discrete_map={
                    'CONTA': '#FF2800',
                    'FIXA': '#790E09'
                }
            )

            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>Percentual: %{percent}",
                marker=dict(line=dict(color='white', width=2))
            )

            fig_donut.update_layout(
                height=420,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Segoe UI', size=14, color='#333333'),
                margin=dict(l=10, r=10, t=60, b=10),
                title=dict(
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=16, color='#333333', weight=800),
                    y=0.98
                ),
                showlegend=True,
                legend=dict(
                    title=dict(text='<b>PLATAFORMA</b>', font=dict(size=13, weight=700, color='#333333')),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )

            fig_donut.add_annotation(
                text=f"<b>TOTAL</b><br>{total_geral_pedidos:,.0f}",
                x=0.5, y=0.5,
                font=dict(size=18, color='#333333', weight=800),
                showarrow=False
            )

            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
        
        # =========================
        # TABELA DINÂMICA POR REGIONAL
        # =========================
        st.markdown('<div class="section-title"><span class="section-icon">📋</span> PEDIDOS POR REGIONAL - E-Commerce</div>', unsafe_allow_html=True)
        
        # Adicionar filtros específicos para a tabela
        col_filtro_t1_pedidos, col_filtro_t2_pedidos = st.columns(2)
        
        with col_filtro_t1_pedidos:
            plataforma_tabela_pedidos = st.multiselect(
                "Filtrar por Plataforma:",
                options=["Todos"] + sorted(df_pedidos['COD_PLATAFORMA'].dropna().unique().tolist()),
                default=["Todos"],
                key="filtro_plataforma_tabela_pedidos"
            )
        
        with col_filtro_t2_pedidos:
            # Filtro opcional para indicador (embora só tenha PEDIDOS)
            indicador_tabela_pedidos = st.multiselect(
                "Filtrar por Indicador:",
                options=["Todos"] + sorted(df_pedidos['DSC_INDICADOR'].dropna().unique().tolist()),
                default=["Todos"],
                key="filtro_indicador_tabela_pedidos"
            )
        
        # Aplicar filtros à tabela
        df_tabela_pedidos = df_pedidos.copy()
        
        if "Todos" not in plataforma_tabela_pedidos:
            df_tabela_pedidos = df_tabela_pedidos[df_tabela_pedidos['COD_PLATAFORMA'].isin(plataforma_tabela_pedidos)]
        
        if "Todos" not in indicador_tabela_pedidos:
            df_tabela_pedidos = df_tabela_pedidos[df_tabela_pedidos['DSC_INDICADOR'].isin(indicador_tabela_pedidos)]
        
        # Extrair ano e mês diretamente de DAT_MOVIMENTO2 (regra oficial)
        df_tabela_pedidos['DAT_MOVIMENTO2'] = pd.to_datetime(df_tabela_pedidos['DAT_MOVIMENTO2'], errors='coerce')
        df_tabela_pedidos['ano'] = df_tabela_pedidos['DAT_MOVIMENTO2'].dt.strftime('%y')
        df_tabela_pedidos['mes_ano'] = df_tabela_pedidos['dat_tratada']
        
        # Definir a ordem dos meses
        meses_ordem_pedidos = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        meses_2025_pedidos = [f'{mes}/25' for mes in meses_ordem_pedidos]
        
        # FUNÇÃO PARA CRIAR TABELA PIVOT DE PEDIDOS (NOVA)
        @st.cache_data
        def create_pivot_table_pedidos_new(df_tabela_pedidos, mes_foco):
            meses_ordem = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            meses_2025 = [f'{m}/25' for m in meses_ordem]
            meses_2026 = []
            try:
                mes_str, ano_curto = mes_foco.split('/')
                if ano_curto == '26':
                    idx = meses_ordem.index(mes_str)
                    meses_2026 = [f'{meses_ordem[i]}/26' for i in range(idx + 1)]
            except:
                pass

            pivot = []
            for regional in sorted(df_tabela_pedidos['REGIONAL'].unique()):
                dfr = df_tabela_pedidos[df_tabela_pedidos['REGIONAL'] == regional]
                total_2024 = dfr[dfr['ano'] == '24']['QTDE'].sum()
                total_2025 = dfr[dfr['ano'] == '25']['QTDE'].sum()
                vals_2025 = [dfr[dfr['mes_ano'] == mes]['QTDE'].sum() for mes in meses_2025]
                vals_2026 = [dfr[dfr['mes_ano'] == mes]['QTDE'].sum() for mes in meses_2026]
                real_foco = dfr[dfr['mes_ano'] == mes_foco]['QTDE'].sum()
                meta_foco = dfr[dfr['mes_ano'] == mes_foco]['DESAFIO_QTD'].sum()
                alcance = (((real_foco / meta_foco) - 1) * 100) if meta_foco > 0 else 0
                mes_ant = get_mes_anterior(mes_foco)
                real_ant = dfr[dfr['mes_ano'] == mes_ant]['QTDE'].sum()
                var_mom = ((real_foco - real_ant) / real_ant * 100) if real_ant > 0 else 0
                var_2425 = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0

                linha = {
                    'Regional': regional,
                    'Total 2024': total_2024,
                    **{meses_2025[i]: vals_2025[i] for i in range(12)},
                    'Total 2025': total_2025,
                }
                for i, mes in enumerate(meses_2026):
                    linha[mes] = vals_2026[i]
                linha.update({
                    f'Real {mes_foco}': real_foco,
                    f'Meta {mes_foco}': meta_foco,
                    'Alcance Meta': alcance,
                    'Var 2025/2024': var_2425,
                    'Var MoM': var_mom
                })
                pivot.append(linha)
            return pivot

        # FUNÇÃO PARA CRIAR TABELA PIVOT DE PEDIDOS
        @st.cache_data
        def create_pivot_table_pedidos(df_tabela_pedidos, meses_2025_pedidos):
            """
            Função para criar tabela pivot dinâmica para pedidos
            """
            pivot_data_pedidos = []
            regionais_pedidos = sorted(df_tabela_pedidos['REGIONAL'].unique())
            
            for regional in regionais_pedidos:
                df_regional_pedidos = df_tabela_pedidos[df_tabela_pedidos['REGIONAL'] == regional]
                
                # Calcular totais por ano (QTDE - realizado)
                total_2024_pedidos = df_regional_pedidos[df_regional_pedidos['ano'] == '24']['QTDE'].sum()
                total_2025_pedidos = df_regional_pedidos[df_regional_pedidos['ano'] == '25']['QTDE'].sum()
                
                # Calcular valores mensais para 2025 (QTDE - realizado)
                valores_mensais_2025_pedidos = []
                for mes in meses_2025_pedidos:
                    valor = df_regional_pedidos[df_regional_pedidos['mes_ano'] == mes]['QTDE'].sum()
                    valores_mensais_2025_pedidos.append(valor)
                
                # Calcular valor REAL de jan/26 (QTDE) - NOVA COLUNA
                real_jan_26_pedidos = df_regional_pedidos[df_regional_pedidos['mes_ano'] == 'jan/26']['QTDE'].sum()
                
                # Calcular valor de jan/26 (meta) - DESAFIO_QTD
                meta_jan_26_pedidos = df_regional_pedidos[df_regional_pedidos['mes_ano'] == 'jan/26']['DESAFIO_QTD'].sum()
                
                # Calcular variações
                variacao_2024_2025_pedidos = ((total_2025_pedidos - total_2024_pedidos) / total_2024_pedidos * 100) if total_2024_pedidos > 0 else 0
                
                # Calcular variação MoM (dez/25 vs nov/25)
                dez_25_pedidos = df_regional_pedidos[df_regional_pedidos['mes_ano'] == 'dez/25']['QTDE'].sum()
                nov_25_pedidos = df_regional_pedidos[df_regional_pedidos['mes_ano'] == 'nov/25']['QTDE'].sum()
                variacao_mom_pedidos = ((dez_25_pedidos - nov_25_pedidos) / nov_25_pedidos * 100) if nov_25_pedidos > 0 else 0
                
                # Calcular alcance da meta (%) - usando real_jan_26 vs meta_jan_26
                alcance_meta_pedidos = (((real_jan_26_pedidos / meta_jan_26_pedidos)-1) * 100) if meta_jan_26_pedidos > 0 else 0
                
                pivot_data_pedidos.append({
                    'Regional': regional,
                    'Total 2024': total_2024_pedidos,
                    **{meses_2025_pedidos[i]: valores_mensais_2025_pedidos[i] for i in range(12)},
                    'Total 2025': total_2025_pedidos,
                    'Real Jan/26': real_jan_26_pedidos,
                    'Meta Jan/26': meta_jan_26_pedidos,
                    'Alcance Meta': alcance_meta_pedidos,
                    'Var 2025/2024': variacao_2024_2025_pedidos,
                    'Var MoM': variacao_mom_pedidos
                })
            
            return pivot_data_pedidos
        
        # Criar tabela pivot
        pivot_data_pedidos = create_pivot_table_pedidos_new(df_tabela_pedidos, mes_selecionado_pedidos)
        
        if not pivot_data_pedidos:
            st.warning("Nenhum dado encontrado com os filtros selecionados para a tabela.")
        else:
            # Ordenar pivot_data pelo Total 2025 (do maior para o menor)
            df_temp_ordenacao_pedidos = pd.DataFrame(pivot_data_pedidos)
            df_temp_ordenacao_pedidos = df_temp_ordenacao_pedidos.sort_values('Total 2025', ascending=False)
            pivot_data_ordenada_pedidos = df_temp_ordenacao_pedidos.to_dict('records')
            
            # Criar linha de TOTAL (soma de todas as regionais)
            df_total_pedidos = df_tabela_pedidos.copy()
            
            # Calcular totais gerais
            total_2024_geral_pedidos = df_total_pedidos[df_total_pedidos['ano'] == '24']['QTDE'].sum()
            total_2025_geral_pedidos = df_total_pedidos[df_total_pedidos['ano'] == '25']['QTDE'].sum()
            
            # Calcular valores mensais gerais para 2025
            valores_mensais_2025_geral_pedidos = []
            for mes in meses_2025_pedidos:
                valor = df_total_pedidos[df_total_pedidos['mes_ano'] == mes]['QTDE'].sum()
                valores_mensais_2025_geral_pedidos.append(valor)
            
            # Calcular REAL/META geral do mês foco selecionado
            real_foco_geral_pedidos = df_total_pedidos[df_total_pedidos['mes_ano'] == mes_selecionado_pedidos]['QTDE'].sum()
            meta_foco_geral_pedidos = df_total_pedidos[df_total_pedidos['mes_ano'] == mes_selecionado_pedidos]['DESAFIO_QTD'].sum()
            
            # Calcular variações gerais
            variacao_2024_2025_geral_pedidos = ((total_2025_geral_pedidos - total_2024_geral_pedidos) / total_2024_geral_pedidos * 100) if total_2024_geral_pedidos > 0 else 0
            
            # Calcular variação MoM geral com base no mês foco
            mes_anterior_foco_pedidos = get_mes_anterior(mes_selecionado_pedidos)
            valor_mes_anterior_foco_pedidos = df_total_pedidos[df_total_pedidos['mes_ano'] == mes_anterior_foco_pedidos]['QTDE'].sum()
            variacao_mom_geral_pedidos = ((real_foco_geral_pedidos - valor_mes_anterior_foco_pedidos) / valor_mes_anterior_foco_pedidos * 100) if valor_mes_anterior_foco_pedidos > 0 else 0
            
            # Calcular alcance da meta geral
            alcance_meta_geral_pedidos = (((real_foco_geral_pedidos / meta_foco_geral_pedidos)-1) * 100) if meta_foco_geral_pedidos > 0 else 0
            
            # Adicionar linha de TOTAL no início
            linha_total_pedidos = {
                'Regional': 'TOTAL',
                'Total 2024': total_2024_geral_pedidos,
                **{meses_2025_pedidos[i]: valores_mensais_2025_geral_pedidos[i] for i in range(12)},
                'Total 2025': total_2025_geral_pedidos,
                f'Real {mes_selecionado_pedidos}': real_foco_geral_pedidos,
                f'Meta {mes_selecionado_pedidos}': meta_foco_geral_pedidos,
                'Alcance Meta': alcance_meta_geral_pedidos,
                'Var 2025/2024': variacao_2024_2025_geral_pedidos,
                'Var MoM': variacao_mom_geral_pedidos
            }
            
            # Criar DataFrame final com as regionais ordenadas por Total 2025 (decrescente)
            df_final_pedidos = pd.DataFrame([linha_total_pedidos] + pivot_data_ordenada_pedidos)
            
            # Ordenar colunas dinamicamente em ordem cronológica (evita ordem alfabética)
            ordem_mes = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}

            def _ord_col_mes(coluna: str):
                try:
                    mes_txt, ano_txt = str(coluna).split('/')
                    return (int(f"20{ano_txt}"), ordem_mes.get(mes_txt, 99))
                except Exception:
                    return (9999, 99)

            colunas_mes_2025 = sorted(
                [c for c in df_final_pedidos.columns if re.match(r'^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)/25$', str(c))],
                key=_ord_col_mes
            )
            colunas_mes_2026 = sorted(
                [c for c in df_final_pedidos.columns if re.match(r'^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)/26$', str(c))],
                key=_ord_col_mes
            )

            # Mantém apenas meses de 2026 até o mês foco selecionado
            try:
                mes_foco_num = ordem_mes[mes_selecionado_pedidos.split('/')[0]]
                colunas_mes_2026 = [c for c in colunas_mes_2026 if ordem_mes.get(str(c).split('/')[0], 99) <= mes_foco_num]
            except Exception:
                pass
            colunas_ordenadas_pedidos = ['Regional', 'Total 2024'] + colunas_mes_2025 + ['Total 2025'] + colunas_mes_2026 + [f'Real {mes_selecionado_pedidos}', f'Meta {mes_selecionado_pedidos}', 'Alcance Meta', 'Var 2025/2024', 'Var MoM']
            # Remover duplicidade mantendo ordem
            colunas_ordenadas_pedidos = list(dict.fromkeys(colunas_ordenadas_pedidos))
            colunas_ordenadas_pedidos = [c for c in colunas_ordenadas_pedidos if c in df_final_pedidos.columns]
            df_final_pedidos = df_final_pedidos[colunas_ordenadas_pedidos]
            
            # Formatar para exibição
            def formatar_numero_pedidos(valor):
                if pd.isna(valor):
                    return "0"
                if isinstance(valor, (int, float)):
                    try:
                        if float(valor).is_integer():
                            return f'{int(valor):,}'.replace(',', '.')
                        else:
                            return f'{float(valor):,.1f}'.replace(',', '.')
                    except Exception:
                        return str(valor)
                return str(valor)
            
            def formatar_percentual_pedidos(valor):
                if isinstance(valor, (int, float)):
                    return f'{valor:+.1f}%'.replace('.', ',')
                return valor
            
            df_exibicao_pedidos = df_final_pedidos.copy().fillna(0)
            for col in df_exibicao_pedidos.columns:
                if col in ['Regional', 'Var 2025/2024', 'Var MoM', 'Alcance Meta']:
                    df_exibicao_pedidos[col] = df_exibicao_pedidos[col].apply(formatar_percentual_pedidos)
                else:
                    df_exibicao_pedidos[col] = df_exibicao_pedidos[col].apply(lambda v: formatar_numero_pedidos(v if not isinstance(v, pd.Series) else v.iloc[0]))
            
            # Função para criar tabela HTML estilizada (similar à aba de ativados)
            def criar_tabela_html_pedidos(df):
                html = dedent("""
                <style>
                    .tabela-container-pedidos {
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
                    
                    .tabela-pedidos {
                        width: 100%;
                        border-collapse: collapse;
                        border-spacing: 0;
                        font-size: 13px;
                        line-height: 1.5;
                    }
                    
                    .tabela-pedidos thead {
                        position: sticky;
                        top: 0;
                        z-index: 100;
                    }
                    
            .tabela-pedidos th {
                background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                color: white !important;
                font-weight: 600;
                padding: 9px 8px; /* reduced height */
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
                    
                    .tabela-pedidos th:hover {
                        background: linear-gradient(135deg, #8A1F1A 0%, #6B0F0B 100%) !important;
                    }
                    
                    .tabela-pedidos th:first-child {
                        border-left: none;
                        border-top-left-radius: 8px;
                    }
                    
                    .tabela-pedidos th:last-child {
                        border-right: none;
                        border-top-right-radius: 8px;
                    }
                    
                    .tabela-pedidos th.col-total-anual-pedidos {
                        background: linear-gradient(135deg, #A23B36 0%, #790E09 100%) !important;
                    }
                    
                    .tabela-pedidos th.col-mes-pedidos {
                        background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                    }
                    
                    .tabela-pedidos th.col-real-jan26-pedidos {
                        background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
                    }
                    
                    .tabela-pedidos th.col-meta-pedidos {
                        background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
                    }
                    
                    .tabela-pedidos th.col-alcance-pedidos,
                    .tabela-pedidos th.col-variacao-pedidos {
                        background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                    }
                    
            .tabela-pedidos td {
                padding: 8px 8px; /* reduced height */
                text-align: center;
                border-bottom: 1px solid #E8E8E8;
                border-right: 1px solid #F0F0F0;
                font-weight: 400;
                transition: all 0.2s ease;
            }
                    
                    .tabela-pedidos tr:not(.linha-total-pedidos) td:first-child {
                        border-left: none;
                        text-align: left;
                        font-weight: 600;
                        color: #333;
                        background: linear-gradient(90deg, #fef5f4 0%, white 100%) !important;
                        padding-left: 15px;
                    }
                    
                    .tabela-pedidos td:last-child {
                        border-right: none;
                    }
                    
                    .linha-total-pedidos {
                        background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                        color: white !important;
                        position: sticky;
                        bottom: 0;
                        z-index: 50;
                        border-top: 2px solid #790E09;
                    }
                    
                    .linha-total-pedidos td {
                        background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                        color: white !important;
                        border-bottom: none;
                        font-weight: 700;
                        font-size: 14px;
                        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                    }
                    
                    .linha-total-pedidos td.col-total-anual-pedidos,
                    .linha-total-pedidos td.col-mes-pedidos,
                    .linha-total-pedidos td.col-real-jan26-pedidos,
                    .linha-total-pedidos td.col-meta-pedidos,
                    .linha-total-pedidos td.col-alcance-pedidos,
                    .linha-total-pedidos td.col-variacao-pedidos {
                        background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                        color: white !important;
                        border-left: none !important;
                        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                        padding-left: 10px !important;
                    }
                    
                    .linha-total-pedidos td.col-alcance-pedidos::before,
                    .linha-total-pedidos td.col-variacao-pedidos::before,
                    .linha-total-pedidos td.percentual-positivo-pedidos::before,
                    .linha-total-pedidos td.percentual-negativo-pedidos::before,
                    .linha-total-pedidos td.percentual-neutro-pedidos::before {
                        content: "" !important;
                    }
                    
                    .linha-total-pedidos td:first-child {
                        font-weight: 800;
                        background: linear-gradient(135deg, #3D0704 0%, #5A0A06 100%) !important;
                    }
                    
                    .linha-regional-pedidos:nth-child(even) {
                        background-color: #FFF9F8 !important;
                    }
                    
                    .linha-regional-pedidos:nth-child(odd) {
                        background-color: white !important;
                    }
                    
                    .linha-regional-pedidos:hover {
                        background-color: #FFEBEE !important;
                        box-shadow: inset 0 0 0 1px #FFCDD2;
                        transform: translateY(-1px);
                    }
                    
                    .linha-regional-pedidos td.col-total-anual-pedidos {
                        background: linear-gradient(135deg, #FDE8E6 0%, #FCE4E2 100%) !important;
                        color: #790E09 !important;
                        font-weight: 600;
                        border-left: 2px solid #A23B36;
                        border-right: 2px solid #A23B36;
                    }
                    
                    .linha-regional-pedidos td.col-mes-pedidos {
                        background-color: #F9F0EF !important;
                        color: #333 !important;
                        border-left: 1px solid #E8D6D5;
                        border-right: 1px solid #E8D6D5;
                    }
                    
                    .linha-regional-pedidos td.col-real-jan26-pedidos {
                        background: linear-gradient(135deg, #F1F3F5 0%, #E9ECEF 100%) !important;
                        color: #495057 !important;
                        font-weight: 600;
                        border-left: 2px solid #ADB5BD;
                        border-right: 2px solid #ADB5BD;
                    }
                    
                    .linha-regional-pedidos td.col-meta-pedidos {
                        background: linear-gradient(135deg, #FFEBEE 0%, #FFE5E8 100%) !important;
                        color: #B71C1C !important;
                        font-weight: 600;
                        border-left: 2px solid #F44336;
                        border-right: 2px solid #F44336;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos,
                    .linha-regional-pedidos td.col-variacao-pedidos {
                        background-color: #F8F9FA !important;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos.percentual-positivo-pedidos,
                    .linha-regional-pedidos td.col-variacao-pedidos.percentual-positivo-pedidos {
                        color: #1B5E20 !important;
                        background: linear-gradient(135deg, #E8F5E9 0%, #E6F4E7 100%) !important;
                        font-weight: 700;
                        position: relative;
                        padding-left: 28px !important;
                        border-left: 3px solid #4CAF50 !important;
                        border-right: 1px solid #C8E6C9 !important;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos.percentual-positivo-pedidos::before,
                    .linha-regional-pedidos td.col-variacao-pedidos.percentual-positivo-pedidos::before {
                        content: "▲";
                        position: absolute;
                        left: 10px;
                        top: 50%;
                        transform: translateY(-50%);
                        font-size: 11px;
                        font-weight: 900;
                        color: #2E7D32;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos.percentual-negativo-pedidos,
                    .linha-regional-pedidos td.col-variacao-pedidos.percentual-negativo-pedidos {
                        color: #C62828 !important;
                        background: linear-gradient(135deg, #FFEBEE 0%, #FFE5E8 100%) !important;
                        font-weight: 700;
                        position: relative;
                        padding-left: 28px !important;
                        border-left: 3px solid #F44336 !important;
                        border-right: 1px solid #FFCDD2 !important;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos.percentual-negativo-pedidos::before,
                    .linha-regional-pedidos td.col-variacao-pedidos.percentual-negativo-pedidos::before {
                        content: "▼";
                        position: absolute;
                        left: 10px;
                        top: 50%;
                        transform: translateY(-50%);
                        font-size: 11px;
                        font-weight: 900;
                        color: #C62828;
                    }
                    
                    .linha-regional-pedidos td.col-alcance-pedidos.percentual-neutro-pedidos,
                    .linha-regional-pedidos td.col-variacao-pedidos.percentual-neutro-pedidos {
                        color: #666666 !important;
                        background: #F8F9FA !important;
                        font-weight: 500;
                    }
                    
                    .linha-regional-pedidos td:hover {
                        transform: scale(1.02);
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                        z-index: 10;
                        position: relative;
                    }
                    
                    .linha-regional-pedidos td.performance-excelente-pedidos {
                        animation: pulse-green-pedidos 2s infinite;
                    }
                    
                    .linha-regional-pedidos td.performance-critica-pedidos {
                        animation: pulse-red-pedidos 2s infinite;
                    }
                    
                    @keyframes pulse-green-pedidos {
                        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
                        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
                        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
                    }
                    
                    @keyframes pulse-red-pedidos {
                        0% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4); }
                        70% { box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }
                        100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
                    }
                    
                    .tabela-container-pedidos::-webkit-scrollbar {
                        width: 10px;
                        height: 10px;
                    }
                    
                    .tabela-container-pedidos::-webkit-scrollbar-track {
                        background: #F5F5F5;
                        border-radius: 10px;
                    }
                    
                    .tabela-container-pedidos::-webkit-scrollbar-thumb {
                        background: linear-gradient(135deg, #A23B36 0%, #790E09 100%);
                        border-radius: 10px;
                        border: 2px solid #F5F5F5;
                    }
                    
                    .tabela-container-pedidos::-webkit-scrollbar-thumb:hover {
                        background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%);
                    }
                    
                    .tabela-container-pedidos::after {
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

                    /* Unified table visual override */
                    .tabela-pedidos th {
                        padding: 9px 7px !important;
                        font-size: 10.5px !important;
                        box-shadow: none !important;
                    }

                    .tabela-pedidos td {
                        padding: 7px 7px !important;
                        font-size: 10.5px !important;
                        line-height: 1.25 !important;
                        box-shadow: none !important;
                    }

                    .tabela-pedidos td:not(:first-child) {
                        text-align: right !important;
                        font-variant-numeric: tabular-nums;
                    }

                    .linha-regional-pedidos:hover {
                        background-color: #FFF2EF !important;
                        box-shadow: inset 0 0 0 1px #FFD9CF !important;
                    }

                    .linha-regional-pedidos td.performance-excelente-pedidos,
                    .linha-regional-pedidos td.performance-critica-pedidos {
                        animation: none !important;
                    }
                </style>
                
                <div class="tabela-container-pedidos">
                <table class="tabela-pedidos">
                <thead>
                    <tr>
                """)
                
                for i, col in enumerate(df.columns):
                    classe = ""
                    if col == 'Regional':
                        classe = ""
                    elif col in ['Total 2024', 'Total 2025']:
                        classe = "col-total-anual-pedidos"
                    elif col in meses_2025_pedidos:
                        classe = "col-mes-pedidos"
                    elif col == 'Real Jan/26':
                        classe = "col-real-jan26-pedidos"
                    elif 'Meta' in col and 'Alcance' not in col:
                        classe = "col-meta-pedidos"
                    elif 'Alcance' in col:
                        classe = "col-alcance-pedidos"
                    elif 'Var' in col:
                        classe = "col-variacao-pedidos"
                    
                    html += f'<th class="{classe}">{col}</th>'
                
                html += "</tr></thead><tbody>"
                
                for idx, row in df.iterrows():
                    is_total = row['Regional'] == 'TOTAL'
                    classe_linha = "linha-total-pedidos" if is_total else "linha-regional-pedidos"
                    html += f'<tr class="{classe_linha}">'
                    
                    for col in df.columns:
                        valor = row[col]
                        classe_celula = ""
                        
                        if is_total:
                            if col == 'Regional':
                                classe_celula = ""
                            elif col in ['Total 2024', 'Total 2025']:
                                classe_celula = "col-total-anual-pedidos"
                            elif col in meses_2025_pedidos:
                                classe_celula = "col-mes-pedidos"
                            elif col == 'Real Jan/26':
                                classe_celula = "col-real-jan26-pedidos"
                            elif 'Meta' in col and 'Alcance' not in col:
                                classe_celula = "col-meta-pedidos"
                            elif 'Alcance' in col:
                                classe_celula = "col-alcance-pedidos"
                            elif 'Var' in col:
                                classe_celula = "col-variacao-pedidos"
                        else:
                            if col == 'Regional':
                                classe_celula = ""
                            elif col in ['Total 2024', 'Total 2025']:
                                classe_celula = "col-total-anual-pedidos"
                            elif col in meses_2025_pedidos:
                                classe_celula = "col-mes-pedidos"
                            elif col == 'Real Jan/26':
                                classe_celula = "col-real-jan26-pedidos"
                            elif 'Meta' in col and 'Alcance' not in col:
                                classe_celula = "col-meta-pedidos"
                            elif 'Alcance' in col or 'Var' in col:
                                try:
                                    valor_limpo = str(valor).replace('%', '').replace('+', '').replace(',', '.')
                                    num_valor = float(valor_limpo)
                                    
                                    if num_valor > 0:
                                        if 'Alcance' in col:
                                            classe_celula = "col-alcance-pedidos percentual-positivo-pedidos"
                                        else:
                                            classe_celula = "col-variacao-pedidos percentual-positivo-pedidos"
                                        
                                        if num_valor > 50:
                                            classe_celula += " performance-excelente-pedidos"
                                    elif num_valor < 0:
                                        if 'Alcance' in col:
                                            classe_celula = "col-alcance-pedidos percentual-negativo-pedidos"
                                        else:
                                            classe_celula = "col-variacao-pedidos percentual-negativo-pedidos"
                                        
                                        if num_valor < -30:
                                            classe_celula += " performance-critica-pedidos"
                                    else:
                                        if 'Alcance' in col:
                                            classe_celula = "col-alcance-pedidos percentual-neutro-pedidos"
                                        else:
                                            classe_celula = "col-variacao-pedidos percentual-neutro-pedidos"
                                except:
                                    if 'Alcance' in col:
                                        classe_celula = "col-alcance-pedidos"
                                    else:
                                        classe_celula = "col-variacao-pedidos"
                        
                        html += f'<td class="{classe_celula}">{valor}</td>'
                    
                    html += "</tr>"
                
                html += "</tbody></table></div>"
                return html
            
            # Exibir tabela (renderização HTML direta para evitar parser Markdown exibir código)
            html_tabela_pedidos = criar_tabela_html_pedidos(df_exibicao_pedidos)
            components.html(html_tabela_pedidos, height=700, scrolling=True)
            
            # =========================
            # BOTÕES DE EXPORTAÇÃO
            # =========================
            col_exp1_pedidos, col_exp2_pedidos, col_exp3_pedidos = st.columns([1, 1, 2])
            
            with col_exp1_pedidos:
                def exportar_excel_tabela_pedidos(df_numerico_pedidos):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_numerico_pedidos.to_excel(writer, index=False, sheet_name='Tabela_Pedidos')
                        
                        workbook = writer.book
                        worksheet = writer.sheets['Tabela_Pedidos']
                        
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
                        
                        for col_num, col_name in enumerate(df_numerico_pedidos.columns):
                            worksheet.write(0, col_num, col_name, header_format)
                            
                            if col_name in ['Var 2025/2024', 'Var MoM', 'Alcance Meta']:
                                cell_format = percent_format
                            else:
                                cell_format = number_format
                            
                            for row_num in range(1, len(df_numerico_pedidos) + 1):
                                value = df_numerico_pedidos.iloc[row_num-1, col_num]
                                if pd.isna(value):
                                    worksheet.write(row_num, col_num, '')
                                elif col_name == 'Regional':
                                    worksheet.write(row_num, col_num, value)
                                else:
                                    worksheet.write(row_num, col_num, value, cell_format)
                        
                        for i, col in enumerate(df_numerico_pedidos.columns):
                            # Usa índice posicional para evitar ambiguidade quando há colunas com nomes repetidos
                            col_values = df_numerico_pedidos.iloc[:, i]
                            max_data_len = col_values.astype(str).str.len().max()
                            max_data_len = 0 if pd.isna(max_data_len) else int(max_data_len)
                            header_len = len(str(col))
                            column_width = max(max_data_len, header_len) + 2
                            worksheet.set_column(i, i, min(column_width, 20))
                    
                    return output.getvalue()
                
                # Converter df_final_pedidos para formato numérico para exportação
                df_numerico_pedidos = df_final_pedidos.copy()
                excel_data_pedidos = exportar_excel_tabela_pedidos(df_numerico_pedidos)
                st.download_button(
                    label="📥 Exportar Excel",
                    data=excel_data_pedidos,
                    file_name="tabela_pedidos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col_exp2_pedidos:
                @st.cache_data
                def convert_to_csv_pedidos(df):
                    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
                
                csv_data_pedidos = convert_to_csv_pedidos(df_numerico_pedidos)
                st.download_button(
                    label="📄 Exportar CSV",
                    data=csv_data_pedidos,
                    file_name="tabela_pedidos.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_exp3_pedidos:
                st.caption(f"""
                **Resumo da Tabela:** {len(pivot_data_pedidos)} Regionais | 
                **Total 2024:** {formatar_numero_pedidos(total_2024_geral_pedidos)} | 
                **Total 2025:** {formatar_numero_pedidos(total_2025_geral_pedidos)} | 
                **Crescimento:** {formatar_percentual_pedidos(variacao_2024_2025_geral_pedidos)} | 
                **Alcance Meta:** {formatar_percentual_pedidos(alcance_meta_geral_pedidos)}
                """)
            
            # =========================
            # GRÁFICO DE EVOLUÇÃO MENSAL
            # =========================
            st.markdown('<div class="section-title"><span class="section-icon">📈</span> EVOLUÇÃO MENSAL DE PEDIDOS</div>', unsafe_allow_html=True)
            
            # Filtros para o gráfico de evolução
            with st.container():
                col_filtro_evo1, col_filtro_evo2, col_filtro_evo3 = st.columns(3)
                
                with col_filtro_evo1:
                    render_filter_label("PLATAFORMA")
                    plataforma_evo = st.selectbox(
                        "Selecione a Plataforma",
                        options=["Todas"] + sorted(df_pedidos['COD_PLATAFORMA'].unique()),
                        key="filtro_plataforma_evo_pedidos",
                        label_visibility="collapsed"
                    )
                
                with col_filtro_evo2:
                    render_filter_label("REGIONAL")
                    regional_evo = st.selectbox(
                        "Selecione a Regional",
                        options=["Todas"] + sorted(df_pedidos['REGIONAL'].unique()),
                        key="filtro_regional_evo_pedidos",
                        label_visibility="collapsed"
                    )
                
                with col_filtro_evo3:
                    render_filter_label("INDICADOR")
                    indicador_evo = st.selectbox(
                        "Selecione o Indicador",
                        options=["Todos"] + sorted(df_pedidos['DSC_INDICADOR'].unique()),
                        key="filtro_indicador_evo_pedidos",
                        label_visibility="collapsed"
                    )
            
            # Aplicar filtros para o gráfico de evolução
            df_evo = df_pedidos.copy()
            
            if plataforma_evo != "Todas":
                df_evo = df_evo[df_evo['COD_PLATAFORMA'] == plataforma_evo]
            if regional_evo != "Todas":
                df_evo = df_evo[df_evo['REGIONAL'] == regional_evo]
            if indicador_evo != "Todos":
                df_evo = df_evo[df_evo['DSC_INDICADOR'] == indicador_evo]
            
            # Criar dados para o gráfico de linhas (similar à aba de Ativados)
            def create_line_chart_data_pedidos(df_grafico):
                """Cria dados para gráfico de linhas temporal para pedidos"""
                # Garantir que temos as colunas de ano e mês
                if 'DAT_MOVIMENTO2' in df_grafico.columns:
                    df_grafico['DAT_MOVIMENTO2'] = pd.to_datetime(df_grafico['DAT_MOVIMENTO2'], errors='coerce')
                    df_grafico['ANO'] = df_grafico['DAT_MOVIMENTO2'].dt.year
                    df_grafico['DAT_MÊS'] = df_grafico['DAT_MOVIMENTO2'].dt.month
                else:
                    # Se não tiver DAT_MOVIMENTO2, usar dat_tratada
                    meses_pt = {
                        'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
                        'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
                    }
                    
                    def extrair_mes_ano(mes_ano_str):
                        try:
                            mes_str, ano_str = mes_ano_str.lower().split('/')
                            mes_num = meses_pt.get(mes_str, 1)
                            ano_num = int(f"20{ano_str}")
                            return ano_num, mes_num
                        except:
                            return 2024, 1
                    
                    df_grafico[['ANO', 'DAT_MÊS']] = df_grafico['dat_tratada'].apply(
                        lambda x: pd.Series(extrair_mes_ano(x))
                    )
                
                meses_abreviados = {
                    1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
                    7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
                }
                
                dados_grafico = []
                # Considerar 2024, 2025 e 2026
                for ano in [2024, 2025, 2026]:
                    df_ano = df_grafico[df_grafico['ANO'] == ano]
                    for mes_num in range(1, 13):
                        df_mes = df_ano[df_ano['DAT_MÊS'] == mes_num]
                        
                        # Para 2024 e 2025 usar QTDE (realizado), para 2026 usar DESAFIO_QTD (meta)
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
            
            # Criar dados para gráfico
            df_linhas_pedidos = create_line_chart_data_pedidos(df_evo)
            
            # Criar título dinâmico
            filtros_ativos = []
            if plataforma_evo != "Todas":
                filtros_ativos.append(f"Plataforma: {plataforma_evo}")
            if regional_evo != "Todas":
                filtros_ativos.append(f"Regional: {regional_evo}")
            if indicador_evo != "Todos":
                filtros_ativos.append(f"Indicador: {indicador_evo}")
            
            titulo_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Todos os Filtros"
            
            # Criar gráfico
            cores_personalizadas = {
                '2024': '#FF2800',
                '2025': '#790E09',
                '2026': '#5A6268'
            }
            
            fig_linhas_pedidos = px.line(
                df_linhas_pedidos,
                x='Mês',
                y='Valor',
                color='Ano',
                title=f'<b>EVOLUÇÃO MENSAL DE PEDIDOS</b><br><span style="font-size: 14px; color: #666666;">{titulo_filtros}</span>',
                labels={'Valor': 'Volume', 'Mês': ''},
                markers=True,
                line_shape='spline',
                color_discrete_map=cores_personalizadas,
                text='Valor_Formatado'
            )
            
            fig_linhas_pedidos.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Segoe UI', size=14, color='#333333'),
                margin=dict(l=60, r=60, t=100, b=80),
                xaxis=dict(
                    title='',
                    tickmode='array',
                    tickvals=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
                    tickfont=dict(size=13, color='#666666', weight=600),
                    showgrid=True,
                    gridcolor='rgba(233, 236, 239, 0.5)',
                    gridwidth=1,
                    linecolor='#E9ECEF',
                    linewidth=2,
                    mirror=True,
                    tickangle=0,
                    showline=True,
                    zeroline=False
                ),
                yaxis=dict(
                    title='<b>VOLUME DE PEDIDOS</b>',
                    title_font=dict(size=15, weight=700, color='#333333'),
                    tickfont=dict(size=13, color='#666666', weight=600),
                    showgrid=True,
                    gridcolor='rgba(233, 236, 239, 0.5)',
                    gridwidth=1,
                    linecolor='#E9ECEF',
                    linewidth=2,
                    mirror=True,
                    showline=True,
                    zeroline=False
                ),
                legend=dict(
                    title=dict(text='<b>ANO</b>', font=dict(size=14, weight=700, color='#333333')),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#E9ECEF',
                    borderwidth=2,
                    font=dict(size=13, color='#333333', weight=600),
                    itemwidth=50,
                    traceorder='normal'
                ),
                title=dict(
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=16, color='#333333', weight=800),
                    y=0.95
                ),
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor='white',
                    font_size=14,
                    font_family='Segoe UI',
                    bordercolor='#E9ECEF',
                    font_color='#333333',
                    font_weight=600
                ),
                height=500,
                showlegend=True
            )
            
            for i, trace in enumerate(fig_linhas_pedidos.data):
                ano = trace.name
                trace.update(
                    mode='lines+markers+text',
                    marker=dict(size=12, line=dict(width=2, color='white'), symbol='circle', opacity=0.9),
                    line=dict(width=4, smoothing=1.3),
                    textposition='top center',
                    textfont=dict(size=12, color=cores_personalizadas[ano], weight=700),
                    hovertemplate=(
                        f"<b>%{{x}}/{ano}</b><br>" +
                        "<b>Valor:</b> %{y:,.0f}<br>" +
                        "<extra></extra>"
                    )
                )
                
                if ano == '2026':
                    trace.update(
                        line=dict(width=4, dash='dash', color=cores_personalizadas[ano]),
                        marker=dict(size=12, line=dict(width=2, color='white'), symbol='diamond', opacity=0.9)
                    )
            
            # Container de informações
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                            padding: 15px 20px; 
                            border-radius: 12px; 
                            border: 2px solid #E9ECEF;
                            margin: 15px 0 5px 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div style="font-size: 14px; color: #333333; font-weight: 700;">
                            <span>📊 Dados Filtrados:</span>
                            <span style="color: #FF2800; margin-left: 8px;">{len(df_evo):,}</span>
                        </div>
                        <div style="font-size: 13px; color: #666666; display: flex; gap: 20px; flex-wrap: wrap;">
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #FF2800; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2024 (Real)</span>
                            </span>
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #790E09; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2025 (Real)</span>
                            </span>
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #5A6268; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2026 (Meta)</span>
                                <span style="color: #5A6268; margin-left: 4px;">— —</span>
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Exibir gráfico
            st.plotly_chart(fig_linhas_pedidos, width='stretch', config={'displayModeBar': True, 'displaylogo': False})

# =========================
# ABA 4: LIGAÇÕES - VERSÃO CORRIGIDA
# =========================
with tab4:
    st.markdown("""
        <div class="section-title">
            <span style="background: linear-gradient(135deg, #790E09, #5A0A06); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📞</span>
            LIGAÇÕES
            <div style="font-size: 14px; color: #666666; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">
                ANÁLISE DE LIGAÇÕES E CONTATOS - TELEVENDAS RECEPTIVO
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================
    # CARREGAR DADOS DE LIGAÇÕES (BASE REAL) - CORRIGIDO
    # =========================
    @st.cache_data(ttl=3600)
    def load_ligacoes_base():
        """Carrega dados REAIS de ligações (arquivo televendas_ligacoes2.xlsx)"""
        try:
            ligacoes_path = "televendas_ligacoes2.xlsx"
            
            # Carregar dados
            df_ligacoes = pd.read_excel(ligacoes_path)
            
            # Verificar se as colunas necessárias existem
            colunas_necessarias = ['PERIODO', 'CABEADO', 'TELEFONE', 'DSC_REGIONAL_CMV', 'QTD']
            colunas_faltantes = [col for col in colunas_necessarias if col not in df_ligacoes.columns]
            
            if colunas_faltantes:
                st.error(f"❌ **Colunas faltantes no arquivo de ligações:** {colunas_faltantes}")
                st.write("**Colunas disponíveis:**", list(df_ligacoes.columns))
                return pd.DataFrame()
            
            # 1. Tratar PERIODO - converter para datetime
            df_ligacoes['DAT_MOVIMENTO2'] = pd.to_datetime(df_ligacoes['PERIODO'], errors='coerce')
            
            # 2. Criar coluna TIPO_CHAMADA baseada na regra da coluna TELEFONE
            def classificar_tipo_chamada(telefone):
                if pd.isna(telefone):
                    return "DEMAIS"
                
                telefone_str = str(telefone)
                
                # Verificar se contém os números especificados
                if '0960' in telefone_str or '8449' in telefone_str:
                    return "Click to Call"
                else:
                    return "DEMAIS"
            
            df_ligacoes['TIPO_CHAMADA'] = df_ligacoes['TELEFONE'].apply(classificar_tipo_chamada)
            
            # 3. Tratar DSC_REGIONAL_CMV - CORREÇÃO: usar apenas os 3 primeiros caracteres e garantir que seja string
            df_ligacoes['REGIONAL'] = df_ligacoes['DSC_REGIONAL_CMV'].astype(str).str.strip().str[:3].str.upper()
            
            # 4. Renomear QTD para QTDE
            df_ligacoes['QTDE'] = pd.to_numeric(df_ligacoes['QTD'], errors='coerce').fillna(0)
            
            # 5. Criar coluna COD_PLATAFORMA baseada em CABEADO
            def mapear_cabeado(valor):
                valor_str = str(valor).upper().strip()
                if valor_str in ['SIM', 'S', 'TRUE', '1', 'FIXA']:
                    return 'FIXA'
                elif valor_str in ['NÃO', 'NAO', 'N', 'FALSE', '0', 'CONTA']:
                    return 'CONTA'
                else:
                    return 'OUTROS'
            
            df_ligacoes['COD_PLATAFORMA'] = df_ligacoes['CABEADO'].apply(mapear_cabeado)
            
            # 6. Criar coluna CANAL_PLAN
            df_ligacoes['CANAL_PLAN'] = 'Televendas Receptivo'
            
            # 7. Criar coluna DSC_INDICADOR
            df_ligacoes['DSC_INDICADOR'] = 'LIGACOES'
            
            # 8. Criar coluna mes_ano no formato 'mmm/aa'
            def formatar_mes_ano(dt):
                try:
                    meses_pt = {
                        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
                        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
                    }
                    mes = meses_pt.get(dt.month, 'jan')
                    ano = dt.strftime('%y')
                    return f"{mes}/{ano}"
                except:
                    return "n/a"
            
            df_ligacoes['mes_ano'] = df_ligacoes['DAT_MOVIMENTO2'].apply(formatar_mes_ano)
            
            # 9. Criar coluna dat_tratada (igual a mes_ano)
            df_ligacoes['dat_tratada'] = df_ligacoes['mes_ano']
            
            # 10. Criar coluna DESAFIO_QTD vazia (será preenchida com metas depois)
            df_ligacoes['DESAFIO_QTD'] = 0
            
            # Manter apenas colunas necessárias para otimização
            colunas_manter = [
                'DAT_MOVIMENTO2', 'mes_ano', 'dat_tratada', 'REGIONAL',
                'CANAL_PLAN', 'COD_PLATAFORMA', 'DSC_INDICADOR', 
                'QTDE', 'DESAFIO_QTD', 'CABEADO', 'TIPO_CHAMADA', 'TELEFONE'
            ]
            
            # Filtrar apenas colunas que existem
            colunas_finais = [col for col in colunas_manter if col in df_ligacoes.columns]
            df_ligacoes = df_ligacoes[colunas_finais]
            
            return df_ligacoes
            
        except Exception as e:
            st.error(f"❌ **Erro ao carregar dados de ligações:** {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    # =========================
    # CARREGAR METAS DE LIGAÇÕES (base_final_trt_new3.xlsx) - CORRIGIDO
    # =========================
    @st.cache_data(ttl=3600)
    def load_metas_ligacoes():
        """Carrega METAS de ligações do arquivo base_final_trt_new3.xlsx"""
        try:
            metas_path = "base_final_trt_new3.xlsx"
            
            # Carregar dados
            df_metas = pd.read_excel(metas_path)
            
            # Verificar se as colunas necessárias existem
            colunas_necessarias = ['DESAFIO_QTD', 'DSC_INDICADOR', 'COD_PLATAFORMA', 'DAT_MOVIMENTO2', 'REGIONAL', 'CANAL_PLAN', 'dat_tratada']
            colunas_faltantes = [col for col in colunas_necessarias if col not in df_metas.columns]
            
            if colunas_faltantes:
                st.error(f"❌ **Colunas faltantes no arquivo de metas:** {colunas_faltantes}")
                st.write("**Colunas disponíveis:**", list(df_metas.columns))
                return pd.DataFrame()
            
            # Garantir que DESAFIO_QTD seja numérico
            df_metas['DESAFIO_QTD'] = pd.to_numeric(df_metas['DESAFIO_QTD'], errors='coerce').fillna(0)
            
            # Tratar regional igual ao feito nos dados reais
            df_metas['REGIONAL'] = df_metas['REGIONAL'].astype(str).str.strip().str[:3].str.upper()
            
            # Criar coluna mes_ano a partir de dat_tratada
            df_metas['mes_ano'] = df_metas['dat_tratada']
            
            # Converter DAT_MOVIMENTO2 para datetime se não for
            if not pd.api.types.is_datetime64_any_dtype(df_metas['DAT_MOVIMENTO2']):
                df_metas['DAT_MOVIMENTO2'] = pd.to_datetime(df_metas['DAT_MOVIMENTO2'], errors='coerce')
            
            # Filtrar apenas ligações (DSC_INDICADOR == 'LIGACOES') e CANAL_PLAN == 'Televendas Receptivo'
            df_metas = df_metas[
                (df_metas['DSC_INDICADOR'] == 'LIGACOES') & 
                (df_metas['CANAL_PLAN'] == 'Televendas Receptivo')
            ].copy()
            
            # Verificar se temos dados
            if df_metas.empty:
                st.warning("⚠️ Nenhuma meta de ligações encontrada no arquivo")
                return pd.DataFrame()
            
            return df_metas
            
        except Exception as e:
            st.error(f"❌ Erro ao carregar METAS de ligações: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    # =========================
    # FUNÇÃO PARA CALCULAR META CORRETA (SOMASES)
    # =========================
    def calcular_meta_correta(df_metas, mes_ano, regional=None, plataforma=None):
        """
        Calcula a meta correta conforme especificação:
        somases(DESAFIO_QTD; 
                DSC_INDICADOR = "LIGACOES"; 
                COD_PLATAFORMA = "CONTA" OU "FIXA";
                DAT_MOVIMENTO2 = data_selecionada)
        
        Parâmetros:
        - df_metas: DataFrame com as metas
        - mes_ano: Mês no formato 'mmm/aa' (ex: 'jan/26')
        - regional: Filtro de regional (opcional)
        - plataforma: 'FIXA' ou 'CONTA' (opcional)
        """
        try:
            if df_metas.empty:
                return 0
            
            # Filtrar por mês
            df_filtrado = df_metas[df_metas['mes_ano'] == mes_ano].copy()
            
            if df_filtrado.empty:
                return 0
            
            # Filtrar por regional se especificado
            if regional and regional != "Todas":
                df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional]
            
            # Filtrar por plataforma se especificado
            if plataforma:
                df_filtrado = df_filtrado[df_filtrado['COD_PLATAFORMA'] == plataforma]
            else:
                # Filtrar apenas FIXA e CONTA (excluir outros)
                df_filtrado = df_filtrado[df_filtrado['COD_PLATAFORMA'].isin(['FIXA', 'CONTA'])]
            
            # Calcular soma da meta
            meta_total = df_filtrado['DESAFIO_QTD'].sum()
            
            return meta_total
            
        except Exception as e:
            st.error(f"❌ Erro ao calcular meta: {str(e)}")
            return 0
    
    # =========================
    # CARREGAR DADOS
    # =========================
    with st.spinner('📥 Carregando dados REAIS de ligações...'):
        df_lig = load_ligacoes_base()
    
    if df_lig.empty:
        st.error("""
        ❌ **Não foi possível carregar os dados de ligações.**
        
        **Verifique:**
        1. Arquivo no caminho especificado
        2. Formato do arquivo
        3. Permissões de acesso
        """)
        st.stop()
    
    with st.spinner('🎯 Carregando METAS de ligações...'):
        df_metas_lig = load_metas_ligacoes()
    
    # Nota: Não vamos mais combinar os dados com as metas no início
    # Em vez disso, vamos calcular as metas dinamicamente quando necessário
    
    # =========================
    # FUNÇÕES AUXILIARES PARA LIGAÇÕES - CORRIGIDAS
    # =========================
    def calcular_total_ligacoes(df, mes, regional_filtro=None):
        """Calcula total de ligações para um mês específico"""
        df_filtrado = df[df['mes_ano'] == mes].copy()
        
        if regional_filtro and regional_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional_filtro]
        
        return df_filtrado['QTDE'].sum()
    
    def calcular_ligacoes_fixa(df, mes, regional_filtro=None):
        """Calcula ligações FIXA para um mês específico (CABEADO == 'SIM')"""
        df_filtrado = df[
            (df['mes_ano'] == mes) & 
            (df['CABEADO'].astype(str).str.upper() == 'SIM')
        ].copy()
        
        if regional_filtro and regional_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional_filtro]
        
        return df_filtrado['QTDE'].sum()
    
    def calcular_ligacoes_conta(df, mes, regional_filtro=None):
        """Calcula ligações CONTA para um mês específico (TIPO_CHAMADA == 'DEMAIS')"""
        df_filtrado = df[
            (df['mes_ano'] == mes) & 
            (df['TIPO_CHAMADA'] == 'DEMAIS')
        ].copy()
        
        if regional_filtro and regional_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional_filtro]
        
        return df_filtrado['QTDE'].sum()
    
    def calcular_ligacoes_clicktocall(df, mes, regional_filtro=None):
        """Calcula ligações Click to Call para um mês específico"""
        df_filtrado = df[
            (df['mes_ano'] == mes) & 
            (df['TIPO_CHAMADA'] == 'Click to Call')
        ].copy()
        
        if regional_filtro and regional_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional_filtro]
        
        return df_filtrado['QTDE'].sum()
    
    # FUNÇÕES DE META CORRIGIDAS
    def calcular_meta_fixa(df_metas, mes, regional_filtro=None):
        """Calcula meta FIXA para um mês específico usando a função corrigida"""
        return calcular_meta_correta(df_metas, mes, regional_filtro, 'FIXA')
    
    def calcular_meta_conta(df_metas, mes, regional_filtro=None):
        """Calcula meta CONTA para um mês específico usando a função corrigida"""
        return calcular_meta_correta(df_metas, mes, regional_filtro, 'CONTA')
    
    # =========================
    # SELEÇÃO DO MÊS
    # =========================
    st.markdown("---")
    
    # Obter meses disponíveis
    if 'mes_ano' in df_lig.columns:
        meses_disponiveis = sorted(df_lig['mes_ano'].dropna().unique().tolist())
    else:
        meses_disponiveis = []
    
    # Determinar mês atual
    meses_pt_map = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }
    
    mes_atual = datetime.now().month
    ano_atual = datetime.now().strftime('%y')
    mes_ano_atual = f"{meses_pt_map.get(mes_atual, 'jan')}/{ano_atual}"
    
    # Garantir que o mês atual esteja na lista
    if mes_ano_atual not in meses_disponiveis and meses_disponiveis:
        meses_disponiveis.append(mes_ano_atual)
    
    # Ordenar meses
    def ordenar_meses(mes_str):
        try:
            mes, ano = mes_str.split('/')
            mes_num = {v: k for k, v in meses_pt_map.items()}[mes]
            return (int(ano), mes_num)
        except:
            return (99, 99)
    
    if meses_disponiveis:
        meses_disponiveis = sorted(meses_disponiveis, key=ordenar_meses)
        
        # Encontrar índice do mês atual ou usar o último
        if mes_ano_atual in meses_disponiveis:
            index_default = meses_disponiveis.index(mes_ano_atual)
        else:
            index_default = len(meses_disponiveis) - 1 if len(meses_disponiveis) > 0 else 0
        
        # Filtro de regional
        regionais_disponiveis = ["Todas"] + sorted(df_lig['REGIONAL'].dropna().unique().tolist())
        
        col_sel1, col_sel2 = st.columns(2)
        
        with col_sel1:
            mes_selecionado = st.selectbox(
                "**📅 Selecione o mês:**",
                options=meses_disponiveis,
                index=index_default,
                key="mes_ligacoes"
            )
        
        with col_sel2:
            regional_selecionada = st.selectbox(
                "**📍 Selecione a Regional:**",
                options=regionais_disponiveis,
                index=0,
                key="regional_ligacoes"
            )
        
        # Encontrar mês anterior
        if len(meses_disponiveis) > 1:
            try:
                idx_mes_atual = meses_disponiveis.index(mes_selecionado)
                mes_anterior = meses_disponiveis[idx_mes_atual - 1] if idx_mes_atual > 0 else mes_selecionado
            except:
                mes_anterior = meses_disponiveis[0]
        else:
            mes_anterior = mes_selecionado
        
        st.info(f"**📊 Período de Análise:** Mês Atual: **{mes_selecionado}** | Mês Anterior: **{mes_anterior}**")
    else:
        st.warning("⚠️ Nenhum mês disponível nos dados")
        mes_selecionado = None
        mes_anterior = None
        regional_selecionada = "Todas"
    
    # =========================
    # CARDS KPI - 4 INDICADORES (COM FORMATAÇÃO CORRIGIDA)
    # =========================
    if mes_selecionado:
        st.markdown("---")
        st.markdown("### 📊 **INDICADORES DE LIGAÇÕES**")
        
        # Calcular valores do mês atual
        total_atual = calcular_total_ligacoes(df_lig, mes_selecionado, regional_selecionada)
        fixa_atual = calcular_ligacoes_fixa(df_lig, mes_selecionado, regional_selecionada)
        conta_atual = calcular_ligacoes_conta(df_lig, mes_selecionado, regional_selecionada)
        clicktocall_atual = calcular_ligacoes_clicktocall(df_lig, mes_selecionado, regional_selecionada)
        
        # Calcular valores do mês anterior
        total_anterior = calcular_total_ligacoes(df_lig, mes_anterior, regional_selecionada)
        fixa_anterior = calcular_ligacoes_fixa(df_lig, mes_anterior, regional_selecionada)
        conta_anterior = calcular_ligacoes_conta(df_lig, mes_anterior, regional_selecionada)
        clicktocall_anterior = calcular_ligacoes_clicktocall(df_lig, mes_anterior, regional_selecionada)
        
        # Calcular metas CORRETAS usando a função corrigida
        meta_fixa = calcular_meta_fixa(df_metas_lig, mes_selecionado, regional_selecionada)
        meta_conta = calcular_meta_conta(df_metas_lig, mes_selecionado, regional_selecionada)
        
        # Calcular variações MoM
        variacao_total = ((total_atual - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
        variacao_fixa = ((fixa_atual - fixa_anterior) / fixa_anterior * 100) if fixa_anterior > 0 else 0
        variacao_conta = ((conta_atual - conta_anterior) / conta_anterior * 100) if conta_anterior > 0 else 0
        variacao_clicktocall = ((clicktocall_atual - clicktocall_anterior) / clicktocall_anterior * 100) if clicktocall_anterior > 0 else 0
        
        # Calcular alcance da meta
        alcance_meta_fixa = ((fixa_atual / meta_fixa) * 100) if meta_fixa > 0 else 0
        alcance_meta_conta = ((conta_atual / meta_conta) * 100) if meta_conta > 0 else 0
        
        # Determinar classes de variação
        classe_total = "variacao-positiva" if variacao_total >= 0 else "variacao-negativa"
        classe_fixa = "variacao-positiva" if variacao_fixa >= 0 else "variacao-negativa"
        classe_conta = "variacao-positiva" if variacao_conta >= 0 else "variacao-negativa"
        classe_clicktocall = "variacao-positiva" if variacao_clicktocall >= 0 else "variacao-negativa"
        
        # Formatar valores com a função brasileira
        total_atual_fmt = formatar_numero_brasileiro(total_atual, 0)
        total_anterior_fmt = formatar_numero_brasileiro(total_anterior, 0)
        fixa_atual_fmt = formatar_numero_brasileiro(fixa_atual, 0)
        fixa_anterior_fmt = formatar_numero_brasileiro(fixa_anterior, 0)
        conta_atual_fmt = formatar_numero_brasileiro(conta_atual, 0)
        conta_anterior_fmt = formatar_numero_brasileiro(conta_anterior, 0)
        clicktocall_atual_fmt = formatar_numero_brasileiro(clicktocall_atual, 0)
        clicktocall_anterior_fmt = formatar_numero_brasileiro(clicktocall_anterior, 0)
        meta_fixa_fmt = formatar_numero_brasileiro(meta_fixa, 0)  # Meta sem casas decimais
        meta_conta_fmt = formatar_numero_brasileiro(meta_conta, 0)  # Meta sem casas decimais
        
        # HTML para meta
        if meta_fixa > 0:
            classe_meta_fixa = "variacao-positiva" if alcance_meta_fixa >= 100 else "variacao-negativa"
            meta_fixa_html = f'<div class="kpi-variacao-item {classe_meta_fixa}" style="font-size: 10px !important;">{alcance_meta_fixa:.0f}% Meta</div>'
        else:
            meta_fixa_html = '<div class="kpi-variacao-item" style="background: #F5F5F5 !important; color: #666666 !important; border: 1.5px solid #E0E0E0 !important; font-size: 10px !important;">Meta N/A</div>'
        
        if meta_conta > 0:
            classe_meta_conta = "variacao-positiva" if alcance_meta_conta >= 100 else "variacao-negativa"
            meta_conta_html = f'<div class="kpi-variacao-item {classe_meta_conta}" style="font-size: 10px !important;">{alcance_meta_conta:.0f}% Meta</div>'
        else:
            meta_conta_html = '<div class="kpi-variacao-item" style="background: #F5F5F5 !important; color: #666666 !important; border: 1.5px solid #E0E0E0 !important; font-size: 10px !important;">Meta N/A</div>'
        
        # Layout dos cards KPI - 4 colunas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up">
                    <div class="kpi-title-dinamico">TOTAL LIGAÇÕES</div>
                    <div style="text-align: center; padding: 15px 0;">
                        <div class="kpi-value-dinamico">{total_atual_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior}):</span> {total_anterior_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                            <div class="kpi-variacao-item {classe_total}" style="font-size: 10px !important;">
                                {variacao_total:+.0f}% MoM
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up">
                    <div class="kpi-title-dinamico">LIGAÇÕES FIXA</div>
                    <div style="text-align: center; padding: 15px 0;">
                        <div class="kpi-value-dinamico">{fixa_atual_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior}):</span> {fixa_anterior_fmt}<br>
                            <span style="font-weight: 600;">Meta:</span> {meta_fixa_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                            <div class="kpi-variacao-item {classe_fixa}" style="font-size: 10px !important;">
                                {variacao_fixa:+.0f}% MoM
                            </div>
                            {meta_fixa_html}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up">
                    <div class="kpi-title-dinamico">LIGAÇÕES CONTA</div>
                    <div style="text-align: center; padding: 15px 0;">
                        <div class="kpi-value-dinamico">{conta_atual_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior}):</span> {conta_anterior_fmt}<br>
                            <span style="font-weight: 600;">Meta:</span> {meta_conta_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                            <div class="kpi-variacao-item {classe_conta}" style="font-size: 10px !important;">
                                {variacao_conta:+.0f}% MoM
                            </div>
                            {meta_conta_html}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div class="kpi-card-dinamico animate-fade-in-up">
                    <div class="kpi-title-dinamico">CLICK TO CALL</div>
                    <div style="text-align: center; padding: 15px 0;">
                        <div class="kpi-value-dinamico">{clicktocall_atual_fmt}</div>
                        <div style="font-size: 12.5px; color: #666666; margin: 10px 0; line-height: 1.4; font-weight: 500;">
                            <span style="font-weight: 600;">Anterior ({mes_anterior}):</span> {clicktocall_anterior_fmt}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                            <div class="kpi-variacao-item {classe_clicktocall}" style="font-size: 10px !important;">
                                {variacao_clicktocall:+.0f}% MoM
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
                # =========================
        # GRÁFICO DE LINHAS TEMPORAL - LIGAÇÕES (VERSÃO CORRIGIDA E OTIMIZADA)
        # =========================
        st.markdown("---")
        st.markdown("### 📈 **EVOLUÇÃO MENSAL DE LIGAÇÕES - VISÃO COMPARATIVA**")

        # Container para filtros
        with st.container():
            col_filtro_lig1, col_filtro_lig2, col_filtro_lig3 = st.columns(3)
            
            with col_filtro_lig1:
                render_filter_label("COD_PLATAFORMA")
                plataforma_linha = st.selectbox(
                    "Selecione a Plataforma",
                    options=["Todas"] + sorted(df_lig['COD_PLATAFORMA'].dropna().unique().tolist()),
                    key="filtro_plataforma_linha_lig",
                    label_visibility="collapsed"
                )
            
            with col_filtro_lig2:
                render_filter_label("TIPO DE CHAMADA")
                tipo_chamada_linha = st.selectbox(
                    "Selecione o Tipo de Chamada",
                    options=["Todos"] + sorted(df_lig['TIPO_CHAMADA'].dropna().unique().tolist()),
                    key="filtro_tipo_chamada_linha_lig",
                    label_visibility="collapsed"
                )
            
            with col_filtro_lig3:
                render_filter_label("REGIONAL")
                regional_linha = st.selectbox(
                    "Selecione a Regional",
                    options=["Todas"] + sorted(df_lig['REGIONAL'].dropna().unique().tolist()),
                    key="filtro_regional_linha_lig",
                    label_visibility="collapsed"
                )

        # =========================
        # FUNÇÃO PARA CRIAR DADOS DO GRÁFICO DE LINHAS (VERSÃO SIMPLIFICADA)
        # =========================
        def aplicar_filtro_plataforma(df_base, plataforma):
            plataforma = (plataforma or "Todas").upper()
            if plataforma == "CONTA":
                return df_base[df_base["TIPO_CHAMADA"] == "DEMAIS"]
            if plataforma == "FIXA":
                return df_base[df_base["CABEADO"].astype(str).str.upper() == "SIM"]
            if plataforma != "TODAS":
                return df_base[df_base["COD_PLATAFORMA"] == plataforma]
            return df_base

        @st.cache_data(ttl=3600)
        def create_line_chart_data_ligacoes_otimizado(
            df_lig_reais,
            df_metas_lig,
            plataforma="Todas",
            tipo_chamada="Todos",
            regional="Todas"
        ):
            df_filtrado = aplicar_filtro_plataforma(df_lig_reais, plataforma)

            if tipo_chamada != "Todos":
                df_filtrado = df_filtrado[df_filtrado["TIPO_CHAMADA"] == tipo_chamada]

            if regional != "Todas":
                df_filtrado = df_filtrado[df_filtrado["REGIONAL"] == regional]

            meses_pt = {
                1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
                7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"
            }

            dados_grafico = []

            for ano in [2024, 2025]:
                df_ano = df_filtrado[df_filtrado["DAT_MOVIMENTO2"].dt.year == ano]
                for mes_num in range(1, 13):
                    df_mes = df_ano[df_ano["DAT_MOVIMENTO2"].dt.month == mes_num]
                    valor = df_mes["QTDE"].sum()
                    dados_grafico.append({
                        "Ano": str(ano),
                        "Mês": meses_pt[mes_num],
                        "Mês_Num": mes_num,
                        "Mês_Ano": f"{meses_pt[mes_num]}/{str(ano)[-2:]}",
                        "Valor": valor,
                        "Tipo": "Realizado",
                        "Cor": "#FF2800" if ano == 2024 else "#790E09"
                    })

            for mes_num in range(1, 13):
                mes_str = meses_pt[mes_num]
                mes_ano_str = f"{mes_str}/26"

                if df_metas_lig.empty:
                    valor_meta = 0
                else:
                    meta_fixa = calcular_meta_correta(
                        df_metas_lig,
                        mes_ano_str,
                        regional if regional != "Todas" else None,
                        "FIXA"
                    )
                    meta_conta = calcular_meta_correta(
                        df_metas_lig,
                        mes_ano_str,
                        regional if regional != "Todas" else None,
                        "CONTA"
                    )
                    if plataforma.upper() == "FIXA":
                        valor_meta = meta_fixa
                    elif plataforma.upper() == "CONTA":
                        valor_meta = meta_conta
                    else:
                        valor_meta = meta_fixa + meta_conta

                dados_grafico.append({
                    "Ano": "2026",
                    "Mês": mes_str,
                    "Mês_Num": mes_num,
                    "Mês_Ano": mes_ano_str,
                    "Valor": valor_meta,
                    "Tipo": "Meta",
                    "Cor": "#5A6268"
                })

            df_grafico = pd.DataFrame(dados_grafico)
            df_grafico = df_grafico.sort_values(["Ano", "Mês_Num"])
            df_grafico["Valor_Formatado"] = df_grafico["Valor"].apply(lambda x: formatar_numero_brasileiro(x, 0))
            return df_grafico

        # =========================
        # CRIAR E EXIBIR GRÁFICO COM TAMANHO OTIMIZADO
        # =========================
        with st.spinner('📊 Gerando gráfico de evolução...'):
            # Criar dados para o gráfico
            df_linhas_lig = create_line_chart_data_ligacoes_otimizado(
                df_lig_reais=df_lig,
                df_metas_lig=df_metas_lig,
                plataforma=plataforma_linha,
                tipo_chamada=tipo_chamada_linha,
                regional=regional_linha
            )

        if not df_linhas_lig.empty:
            # Criar título dinâmico
            filtros_ativos = []
            if plataforma_linha != "Todas":
                filtros_ativos.append(f"Plataforma: {plataforma_linha}")
            if tipo_chamada_linha != "Todos":
                filtros_ativos.append(f"Tipo: {tipo_chamada_linha}")
            if regional_linha != "Todas":
                filtros_ativos.append(f"Regional: {regional_linha}")
            
            titulo_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Todos os Filtros"
            
            # Definir cores
            cores_personalizadas = {
                '2024': '#FF2800',
                '2025': '#790E09',
                '2026': '#5A6268'
            }
            
            # Criar gráfico com tamanho otimizado
            fig_linhas_lig = px.line(
                df_linhas_lig,
                x='Mês',
                y='Valor',
                color='Ano',
                title=f'<b>EVOLUÇÃO MENSAL DE LIGAÇÕES</b><br><span style="font-size: 14px; color: #666666;">{titulo_filtros}</span>',
                labels={'Valor': 'Volume de Ligações', 'Mês': ''},
                markers=True,
                line_shape='spline',
                color_discrete_map=cores_personalizadas,
                text='Valor_Formatado'
            )
            
            # ATUALIZAR LAYOUT COM TAMANHO OTIMIZADO
            fig_linhas_lig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Segoe UI', size=14, color='#333333'),
                margin=dict(l=60, r=60, t=100, b=80),
                xaxis=dict(
                    title='',
                    tickmode='array',
                    tickvals=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
                    tickfont=dict(size=13, color='#666666', weight=600),
                    showgrid=True,
                    gridcolor='rgba(233, 236, 239, 0.5)',
                    gridwidth=1,
                    linecolor='#E9ECEF',
                    linewidth=2,
                    mirror=True,
                    tickangle=0,
                    showline=True,
                    zeroline=False
                ),
                yaxis=dict(
                    title='<b>VOLUME DE LIGAÇÕES</b>',
                    title_font=dict(size=15, weight=700, color='#333333'),
                    tickfont=dict(size=13, color='#666666', weight=600),
                    showgrid=True,
                    gridcolor='rgba(233, 236, 239, 0.5)',
                    gridwidth=1,
                    linecolor='#E9ECEF',
                    linewidth=2,
                    mirror=True,
                    showline=True,
                    zeroline=False,
                    rangemode='tozero'
                ),
                legend=dict(
                    title=dict(text='<b>ANO</b>', font=dict(size=14, weight=700, color='#333333')),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#E9ECEF',
                    borderwidth=2,
                    font=dict(size=13, color='#333333', weight=600),
                    itemwidth=50,
                    traceorder='normal'
                ),
                title=dict(
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=16, color='#333333', weight=800),
                    y=0.95
                ),
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor='white',
                    font_size=14,
                    font_family='Segoe UI',
                    bordercolor='#E9ECEF',
                    font_color='#333333',
                    font_weight=600
                ),
                height=600,  # AUMENTADO PARA MAIOR VISIBILIDADE
                showlegend=True
            )
            
            # Personalizar cada linha
            for i, trace in enumerate(fig_linhas_lig.data):
                ano = trace.name
                
                if ano == '2026':
                    trace.update(
                        mode='lines+markers+text',
                        marker=dict(size=10, line=dict(width=2, color='white'), symbol='diamond', opacity=0.9),
                        line=dict(width=3, dash='dash', smoothing=1.3),
                        textposition='top center',
                        textfont=dict(size=11, color=cores_personalizadas[ano], weight=700),
                        hovertemplate=(
                            f"<b>%{{x}}/{ano}</b><br>" +
                            "<b>Meta:</b> %{y:,.0f}<br>" +
                            "<extra></extra>"
                        )
                    )
                else:
                    trace.update(
                        mode='lines+markers+text',
                        marker=dict(size=10, line=dict(width=2, color='white'), symbol='circle', opacity=0.9),
                        line=dict(width=3, smoothing=1.3),
                        textposition='top center',
                        textfont=dict(size=11, color=cores_personalizadas[ano], weight=700),
                        hovertemplate=(
                            f"<b>%{{x}}/{ano}</b><br>" +
                            "<b>Realizado:</b> %{y:,.0f}<br>" +
                            "<extra></extra>"
                        )
                    )
            
            # Container de informações
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                            padding: 15px 20px; 
                            border-radius: 12px; 
                            border: 2px solid #E9ECEF;
                            margin: 15px 0 20px 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div style="font-size: 14px; color: #333333; font-weight: 700;">
                            <span>📊 Filtros Ativos:</span>
                            <span style="color: #FF2800; margin-left: 8px;">{titulo_filtros}</span>
                        </div>
                        <div style="font-size: 13px; color: #666666; display: flex; gap: 20px; flex-wrap: wrap;">
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #FF2800; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2024 (Realizado)</span>
                            </span>
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #790E09; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2025 (Realizado)</span>
                            </span>
                            <span style="display: inline-flex; align-items: center; gap: 8px;">
                                <div style="width: 12px; height: 12px; background: #5A6268; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                                <span style="font-weight: 600;">2026 (Meta)</span>
                                <span style="color: #5A6268; margin-left: 4px;">— —</span>
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # EXIBIR GRÁFICO COM LARGURA COMPLETA
            st.plotly_chart(fig_linhas_lig, use_container_width=True, config={
                'displayModeBar': True, 
                'displaylogo': False,
                'responsive': True
            })
            
            # =========================
            # RESUMO ESTATÍSTICO
            # =========================
            st.markdown("---")
            
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            
            with col_res1:
                total_2024 = df_linhas_lig[
                    (df_linhas_lig['Ano'] == '2024') & 
                    (df_linhas_lig['Tipo'] == 'Realizado')
                ]['Valor'].sum()
                st.metric(
                    label="Total 2024",
                    value=formatar_numero_brasileiro(total_2024, 0),
                    delta=None
                )
            
            with col_res2:
                total_2025 = df_linhas_lig[
                    (df_linhas_lig['Ano'] == '2025') & 
                    (df_linhas_lig['Tipo'] == 'Realizado')
                ]['Valor'].sum()
                crescimento = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
                st.metric(
                    label="Total 2025",
                    value=formatar_numero_brasileiro(total_2025, 0),
                    delta=f"{crescimento:+.1f}%"
                )
            
            with col_res3:
                meta_2026 = df_linhas_lig[
                    (df_linhas_lig['Ano'] == '2026') & 
                    (df_linhas_lig['Tipo'] == 'Meta')
                ]['Valor'].sum()
                st.metric(
                    label="Meta 2026",
                    value=formatar_numero_brasileiro(meta_2026, 0),
                    delta=None
                )
            
            with col_res4:
                crescimento_projetado = ((meta_2026 - total_2025) / total_2025 * 100) if total_2025 > 0 else 0
                st.metric(
                    label="Crescimento Projetado",
                    value=f"{crescimento_projetado:+.1f}%",
                    delta=None
                )
            
            # =========================
            # DETALHES DOS DADOS
            # =========================
            with st.expander("📋 **Detalhes dos Dados do Gráfico**", expanded=False):
                col_det1, col_det2 = st.columns(2)
                
                with col_det1:
                    st.markdown("**📊 Resumo por Ano:**")
                    
                    resumo_por_ano = df_linhas_lig.groupby(['Ano', 'Tipo']).agg({
                        'Valor': 'sum',
                        'Mês': 'count'
                    }).reset_index()
                    
                    for _, row in resumo_por_ano.iterrows():
                        st.write(f"• **{row['Ano']}** ({row['Tipo']}): {formatar_numero_brasileiro(row['Valor'], 0)} em {row['Mês']} meses")
                
                with col_det2:
                    st.markdown("**📈 Análise de Tendência:**")
                    
                    # Calcular média mensal por ano
                    media_por_ano = df_linhas_lig.groupby('Ano')['Valor'].mean().reset_index()
                    
                    for _, row in media_por_ano.iterrows():
                        st.write(f"• **{row['Ano']}**: Média mensal de {formatar_numero_brasileiro(row['Valor'], 0)}")
            
            # =========================
            # DOWNLOAD DOS DADOS
            # =========================
            st.markdown("---")
            
            col_down1, col_down2 = st.columns(2)
            
            with col_down1:
                @st.cache_data
                def exportar_excel_grafico(df_grafico):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_grafico.to_excel(writer, index=False, sheet_name='Dados_Grafico_Ligacoes')
                    return output.getvalue()
                
                excel_data = exportar_excel_grafico(df_linhas_lig)
                st.download_button(
                    label="📥 Exportar Dados do Gráfico (Excel)",
                    data=excel_data,
                    file_name=f"dados_grafico_ligacoes_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col_down2:
                @st.cache_data
                def exportar_csv_grafico(df_grafico):
                    return df_grafico.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
                
                csv_data = exportar_csv_grafico(df_linhas_lig)
                st.download_button(
                    label="📄 Exportar Dados do Gráfico (CSV)",
                    data=csv_data,
                    file_name=f"dados_grafico_ligacoes_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        else:
            st.warning("""
            ⚠️ **Não foi possível gerar o gráfico de evolução.**
            
            **Possíveis causas:**
            1. Não há dados disponíveis para os filtros selecionados
            2. As datas dos dados não estão no formato esperado
            3. Problema na leitura dos arquivos de metas
            
            **Sugestões:**
            1. Verifique se os filtros estão corretos
            2. Confirme se há dados para os períodos selecionados
            3. Verifique o formato das colunas de data
            """)

        # Adicionar CSS para garantir que o gráfico ocupe toda a largura
        st.markdown("""
        <style>
            /* Garantir que o gráfico ocupe toda a largura */
            [data-testid="stPlotlyChart"] {
                width: 100% !important;
                max-width: 100% !important;
            }
            
            /* Ajustar container do gráfico */
            .js-plotly-plot .plotly {
                width: 100% !important;
            }
            
            /* Ajustar tamanho dos filtros */
            .stSelectbox > div > div {
                width: 100% !important;
            }
        </style>
        """, unsafe_allow_html=True)
                
                    # =========================
        # TABELA DINÂMICA POR REGIONAL - LIGAÇÕES (VERSÃO CORRIGIDA E COMPLETA)
        # =========================
        st.markdown("---")
        st.markdown("### 📋 **TABELA DINÂMICA POR REGIONAL - LIGAÇÕES**")

        # Container principal
        with st.container():
            # Filtros avançados para a tabela
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                plataforma_filtro_tabela = st.multiselect(
                    "**Filtrar por Plataforma:**",
                    options=["Todas"] + sorted(df_lig['COD_PLATAFORMA'].dropna().unique().tolist()),
                    default=["Todas"],
                    key="filtro_plataforma_tabela_lig"
                )
            
            with col_filtro2:
                tipo_chamada_filtro_tabela = st.multiselect(
                    "**Filtrar por Tipo de Chamada:**",
                    options=["Todos"] + sorted(df_lig['TIPO_CHAMADA'].dropna().unique().tolist()),
                    default=["Todos"],
                    key="filtro_tipo_chamada_tabela_lig"
                )
            
            with col_filtro3:
                # Filtro de período (mês) - já temos mes_selecionado do seletor principal
                st.markdown(f"""
                    <div style="padding: 8px 0; font-size: 14px; font-weight: 600; color: #333;">
                        Período Selecionado: 
                        <span style="color: #FF2800; background: rgba(255, 40, 0, 0.1); 
                                padding: 4px 12px; border-radius: 20px; margin-left: 8px;">
                            {mes_selecionado}
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            # =========================
            # FUNÇÃO PRINCIPAL PARA CRIAR TABELA DINÂMICA CORRIGIDA
            # =========================
            @st.cache_data(ttl=3600)
            def criar_tabela_dinamica_ligacoes_completa(
                df_lig_reais, 
                df_metas_lig, 
                mes_foco, 
                regional_filtro="Todas",
                plataforma_filtro=["Todas"],
                tipo_chamada_filtro=["Todos"]
            ):
                """
                Cria tabela dinâmica completa para ligações com:
                - Valores realizados de jan/2025 até o mês atual (ou mês selecionado)
                - Filtros de COD_PLATAFORMA e TIPO_CHAMADA
                - Meta do mês atual
                """
                
                try:
                    # 1. APLICAR FILTROS NOS DADOS REAIS
                    df_filtrado = df_lig_reais.copy()
                    
                    # Filtrar por regional selecionada
                    if regional_filtro != "Todas":
                        df_filtrado = df_filtrado[df_filtrado['REGIONAL'] == regional_filtro]
                    
                    # Filtrar por plataforma com a mesma lógica da KPI (CONTA = DEMAIS, FIXA = CABEADO SIM)
                    df_filtrado = aplicar_filtro_plataforma(
                        df_filtrado,
                        plataforma_filtro[0] if len(plataforma_filtro) == 1 else "Todas"
                    )
                    
                    # Filtrar por tipo de chamada
                    if "Todos" not in tipo_chamada_filtro:
                        df_filtrado = df_filtrado[df_filtrado['TIPO_CHAMADA'].isin(tipo_chamada_filtro)]
                    
                    if df_filtrado.empty:
                        return [], []
                    
                    # 2. IDENTIFICAR O ANO DO MÊS FOCO
                    mes_str, ano_curto = mes_foco.split('/')
                    ano_foco = int('20' + ano_curto)
                    
                    # 3. CRIAR LISTA DE MESES DESDE JAN/2025 ATÉ O MÊS FOCO
                    meses_ordem = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 
                                'jul', 'ago', 'set', 'out', 'nov', 'dez']
                    
                    meses_para_tabela = []
                    
                    # Adicionar todos os meses de 2025
                    for mes in meses_ordem:
                        meses_para_tabela.append(f"{mes}/25")
                    
                    # Adicionar meses de 2026 até o mês foco (se for 2026)
                    if ano_foco == 2026:
                        idx_mes_foco = meses_ordem.index(mes_str)
                        for i in range(idx_mes_foco + 1):
                            meses_para_tabela.append(f"{meses_ordem[i]}/26")
                    
                    # 4. AGRUPAR DADOS POR REGIONAL E MÊS
                    pivot_data = []
                    regionais_unicas = sorted(df_filtrado['REGIONAL'].dropna().unique())
                    
                    for regional in regionais_unicas:
                        df_regional = df_filtrado[df_filtrado['REGIONAL'] == regional].copy()
                        
                        # Calcular valores mensais
                        valores_mensais = {}
                        for mes_ano in meses_para_tabela:
                            valor = df_regional[df_regional['mes_ano'] == mes_ano]['QTDE'].sum()
                            valores_mensais[mes_ano] = valor
                        
                        # Calcular total 2025 (soma de todos os meses de 2025)
                        meses_2025 = [m for m in meses_para_tabela if '/25' in m]
                        total_2025 = sum([valores_mensais.get(m, 0) for m in meses_2025])
                        
                        # Calcular REAL do mês foco
                        real_mes_foco = df_regional[df_regional['mes_ano'] == mes_foco]['QTDE'].sum()
                        
                        # 5. CALCULAR META DO MÊS FOCO (usando regional da linha)
                        if not df_metas_lig.empty:
                            meta_fixa = calcular_meta_correta(df_metas_lig, mes_foco, regional, 'FIXA')
                            meta_conta = calcular_meta_correta(df_metas_lig, mes_foco, regional, 'CONTA')
                            
                            if "Todas" not in plataforma_filtro and "CONTA" in plataforma_filtro and "FIXA" not in plataforma_filtro:
                                meta_mes_foco = meta_conta
                            elif "Todas" not in plataforma_filtro and "FIXA" in plataforma_filtro and "CONTA" not in plataforma_filtro:
                                meta_mes_foco = meta_fixa
                            else:
                                meta_mes_foco = meta_fixa + meta_conta
                        else:
                            meta_mes_foco = 0
                        
                        # 6. CALCULAR MÉTRICAS DE DESEMPENHO
                        alcance_meta = ((real_mes_foco / meta_mes_foco) * 100) if meta_mes_foco > 0 else 0
                        
                        mes_anterior = get_mes_anterior(mes_foco)
                        real_mes_anterior = df_regional[df_regional['mes_ano'] == mes_anterior]['QTDE'].sum()
                        variacao_mom = ((real_mes_foco - real_mes_anterior) / real_mes_anterior * 100) if real_mes_anterior > 0 else 0
                        
                        linha = {
                            'Regional': regional,
                            **valores_mensais,
                            'Total 2025': total_2025,
                            f'Real {mes_foco}': real_mes_foco,
                            f'Meta {mes_foco}': meta_mes_foco,
                            'Alcance Meta %': alcance_meta,
                            'Var MoM %': variacao_mom
                        }
                        
                        pivot_data.append(linha)
                    
                    # 8. ADICIONAR LINHA DE TOTAL
                    if pivot_data:
                        df_totais = pd.DataFrame(pivot_data)
                        linha_total = {'Regional': 'TOTAL'}
                        
                        for col in df_totais.columns:
                            if col == 'Regional':
                                continue
                            if col in ['Total 2025', f'Real {mes_foco}', f'Meta {mes_foco}']:
                                linha_total[col] = df_totais[col].sum()
                            elif 'Alcance Meta %' in col:
                                total_real = linha_total.get(f'Real {mes_foco}', 0)
                                total_meta = linha_total.get(f'Meta {mes_foco}', 0)
                                linha_total[col] = (total_real / total_meta * 100) if total_meta > 0 else 0
                            elif 'Var MoM %' in col:
                                linha_total[col] = 0
                            else:
                                linha_total[col] = df_totais[col].sum()
                        
                        pivot_data.insert(0, linha_total)
                    
                    return pivot_data, meses_para_tabela
                    
                except Exception as e:
                    st.error(f"Erro ao criar tabela dinâmica: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return [], []

            # =========================
            # APLICAR FILTROS E CRIAR TABELA
            # =========================
            # Converter filtros para formato esperado pela função
            plataforma_filtro_lista = plataforma_filtro_tabela
            if "Todas" in plataforma_filtro_lista:
                plataforma_filtro_lista = ["Todas"]

            tipo_chamada_filtro_lista = tipo_chamada_filtro_tabela
            if "Todos" in tipo_chamada_filtro_lista:
                tipo_chamada_filtro_lista = ["Todos"]

            # Criar tabela dinâmica
            with st.spinner('📊 Gerando tabela dinâmica...'):
                pivot_data_completa, meses_tabela = criar_tabela_dinamica_ligacoes_completa(
                    df_lig_reais=df_lig,
                    df_metas_lig=df_metas_lig,
                    mes_foco=mes_selecionado,
                    regional_filtro=regional_selecionada,
                    plataforma_filtro=plataforma_filtro_lista,
                    tipo_chamada_filtro=tipo_chamada_filtro_lista
                )

            # =========================
            # FORMATAR E EXIBIR TABELA
            # =========================
            if pivot_data_completa and meses_tabela:
                # Criar DataFrame
                df_tabela_final = pd.DataFrame(pivot_data_completa)
                # Remover qualquer coluna de 2024
                df_tabela_final = df_tabela_final[[c for c in df_tabela_final.columns if '/24' not in c]]
                
                # Evitar duplicidade do mês foco e remover colunas de 2024
                meses_tabela_exib = [m for m in meses_tabela if m != mes_selecionado and '/24' not in m]
                meses_2025_exib = [m for m in meses_tabela_exib if m.endswith('/25')]
                meses_pos_2025_exib = [m for m in meses_tabela_exib if not m.endswith('/25')]

                # Ordenar colunas: meses 2025 -> Total 2025 -> meses 2026 até mês anterior -> Real/Meta mês foco
                colunas_ordenadas = ['Regional'] + meses_2025_exib + ['Total 2025'] + meses_pos_2025_exib + [
                                                                         f'Real {mes_selecionado}',
                                                                         f'Meta {mes_selecionado}',
                                                                         'Alcance Meta %',
                                                                         'Var MoM %'
                                                                     ]
                
                # Manter apenas colunas que existem
                colunas_ordenadas = [col for col in colunas_ordenadas if col in df_tabela_final.columns]
                df_tabela_final = df_tabela_final[colunas_ordenadas]
                
                # Formatar números
                def formatar_valor_tabela(valor, coluna):
                    if pd.isna(valor):
                        return "0"
                    
                    try:
                        if '%' in coluna:
                            # Para porcentagens
                            return f"{float(valor):+.1f}%"
                        elif coluna in ['Regional']:
                            return str(valor)
                        else:
                            # Para números inteiros
                            return formatar_numero_brasileiro(float(valor), 0)
                    except:
                        return str(valor)
                
                # Criar DataFrame formatado para exibição
                df_exibicao_formatado = df_tabela_final.copy()
                for col in df_exibicao_formatado.columns:
                    df_exibicao_formatado[col] = df_exibicao_formatado[col].apply(
                        lambda x, col=col: formatar_valor_tabela(x, col)
                    )
                
                # =========================
                # FUNÇÃO PARA CRIAR TABELA HTML ESTILIZADA
                # =========================
                def criar_tabela_html_ligacoes(df_formatado, df_numerico, meses_lista, mes_foco):
                    """Cria tabela HTML estilizada para ligações"""
                    
                    html = """
                    <style>
                        .tabela-container-ligacoes {
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
                            position: relative;
                        }
                        
                        .tabela-ligacoes {
                            width: 100%;
                            border-collapse: collapse;
                            border-spacing: 0;
                            font-size: 12px;
                            line-height: 1.4;
                        }
                        
                        .tabela-ligacoes thead {
                            position: sticky;
                            top: 0;
                            z-index: 100;
                        }
                        
                        .tabela-ligacoes th {
                            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                            color: white !important;
                            font-weight: 700;
                            padding: 8px 6px; /* reduced height */
                            text-align: center;
                            border-bottom: 3px solid #5A0A06;
                            border-right: 1px solid rgba(255, 255, 255, 0.15);
                            white-space: nowrap;
                            font-size: 11px;
                            letter-spacing: 0.3px;
                            text-transform: uppercase;
                            position: relative;
                            min-width: 70px;
                        }
                        
                        .tabela-ligacoes th.col-regional {
                            min-width: 100px;
                            text-align: left;
                            padding-left: 15px;
                        }
                        
                        .tabela-ligacoes th.col-total-anual {
                            background: linear-gradient(135deg, #A23B36 0%, #790E09 100%) !important;
                            min-width: 90px;
                        }
                        
                        .tabela-ligacoes th.col-mes-2025 {
                            background: linear-gradient(135deg, #790E09 0%, #5A0A06 100%) !important;
                        }
                        
                        .tabela-ligacoes th.col-mes-2026 {
                            background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                        }
                        
                        .tabela-ligacoes th.col-real-mes {
                            background: linear-gradient(135deg, #D45D44 0%, #A23B36 100%) !important;
                            min-width: 90px;
                        }
                        
                        .tabela-ligacoes th.col-meta-mes {
                            background: linear-gradient(135deg, #A23B36 0%, #790E09 100%) !important;
                            min-width: 90px;
                        }
                        
                        .tabela-ligacoes th.col-alcance {
                            background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                            min-width: 90px;
                        }
                        
                        .tabela-ligacoes th.col-variacao {
                            background: linear-gradient(135deg, #5A6268 0%, #3E444A 100%) !important;
                            min-width: 90px;
                        }
                        
                        .tabela-ligacoes td {
                            padding: 7px 6px; /* reduced height */
                            text-align: center;
                            border-bottom: 1px solid #E8E8E8;
                            border-right: 1px solid #F0F0F0;
                            font-weight: 500;
                            transition: all 0.2s ease;
                            font-size: 11px;
                        }
                        
                        .tabela-ligacoes tr:not(.linha-total-ligacoes) td:first-child {
                            text-align: left;
                            font-weight: 700;
                            color: #333;
                            background: linear-gradient(90deg, #fef5f4 0%, white 100%) !important;
                            padding-left: 15px;
                            position: sticky;
                            left: 0;
                            z-index: 10;
                            border-right: 2px solid #E9ECEF;
                            min-width: 100px;
                        }
                        
                        .linha-total-ligacoes {
                            background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                            color: white !important;
                            position: sticky;
                            bottom: 0;
                            z-index: 50;
                            border-top: 2px solid #790E09;
                        }
                        
                        .linha-total-ligacoes td {
                            background: linear-gradient(135deg, #5A0A06 0%, #3D0704 100%) !important;
                            color: white !important;
                            border-bottom: none;
                            font-weight: 800;
                            font-size: 12px;
                            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                        }
                        
                        .linha-total-ligacoes td:first-child {
                            position: sticky;
                            left: 0;
                            z-index: 60;
                            border-right: 2px solid rgba(255, 255, 255, 0.2);
                        }
                        
                        .linha-regional-ligacoes:nth-child(even) {
                            background-color: #FFF9F8 !important;
                        }
                        
                        .linha-regional-ligacoes:nth-child(odd) {
                            background-color: white !important;
                        }
                        
                        .linha-regional-ligacoes:hover {
                            background-color: #FFEBEE !important;
                            transform: translateY(-1px);
                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                        }
                        
                        .valor-negativo { color: #C62828 !important; font-weight: 700; }
                        .valor-positivo { color: #1B5E20 !important; font-weight: 700; }
                        .valor-destaque {
                            background-color: rgba(121, 14, 9, 0.08) !important;
                            border: 1px solid rgba(121, 14, 9, 0.25) !important;
                            font-weight: 800;
                        }
                        
                        .tabela-container-ligacoes::-webkit-scrollbar {
                            width: 8px;
                            height: 8px;
                        }
                        
                        .tabela-container-ligacoes::-webkit-scrollbar-track {
                            background: #F5F5F5;
                            border-radius: 10px;
                        }
                        
                        .tabela-container-ligacoes::-webkit-scrollbar-thumb {
                            background: linear-gradient(135deg, #A23B36 0%, #790E09 100%);
                            border-radius: 10px;
                        }
                        
                        .indicador-performance {
                            display: inline-block;
                            width: 10px;
                            height: 10px;
                            border-radius: 50%;
                            margin-right: 5px;
                        }
                        
                        /* Keep alcance cells visually aligned with Var MoM: no filled backgrounds */
                        .performance-excelente,
                        .performance-boa,
                        .performance-media,
                        .performance-ruim,
                        .performance-critica {
                            background: transparent !important;
                        }
                        
                        @keyframes highlight {
                            0% { background-color: rgba(255, 235, 59, 0.5); }
                            100% { background-color: transparent; }
                        }
                        
                        .highlight-animation {
                            animation: highlight 2s ease;
                        }

                        /* Unified table visual override */
                        .tabela-ligacoes th {
                            padding: 9px 7px !important;
                            font-size: 10.5px !important;
                            box-shadow: none !important;
                        }

                        .tabela-ligacoes td {
                            padding: 7px 7px !important;
                            font-size: 10.5px !important;
                            line-height: 1.25 !important;
                            box-shadow: none !important;
                        }

                        .tabela-ligacoes td:not(:first-child) {
                            text-align: right !important;
                            font-variant-numeric: tabular-nums;
                        }

                        .linha-regional-ligacoes:hover {
                            background-color: #FFF2EF !important;
                            box-shadow: inset 0 0 0 1px #FFD9CF !important;
                        }
                    </style>
                    
                    <div class="tabela-container-ligacoes">
                    <table class="tabela-ligacoes">
                    <thead>
                        <tr>
                    """
                    
                    # Cabeçalhos
                    for i, col in enumerate(df_formatado.columns):
                        classe = ""
                        
                        if col == 'Regional':
                            classe = "col-regional"
                        elif col == 'Total 2024':
                            classe = "col-total-anual"
                        elif col in meses_lista:
                            if '/25' in col:
                                classe = "col-mes-2025"
                            elif '/26' in col:
                                classe = "col-mes-2026"
                        elif 'Real' in col:
                            classe = "col-real-mes"
                        elif 'Meta' in col and 'Alcance' not in col:
                            classe = "col-meta-mes"
                        elif 'Alcance' in col:
                            classe = "col-alcance"
                        elif 'Var' in col:
                            classe = "col-variacao"
                        elif col == 'Total 2025':
                            classe = "col-total-anual"
                        
                        html += f'<th class="{classe}">{col}</th>'
                    
                    html += "</tr></thead><tbody>"
                    
                    # Linhas
                    for idx, row in df_formatado.iterrows():
                        is_total = row['Regional'] == 'TOTAL'
                        classe_linha = "linha-total-ligacoes" if is_total else "linha-regional-ligacoes"
                        
                        html += f'<tr class="{classe_linha}">'
                        
                        for col_idx, col in enumerate(df_formatado.columns):
                            valor_formatado = row[col]
                            valor_numerico = df_numerico.iloc[idx, col_idx] if idx < len(df_numerico) else 0
                            
                            # Determinar classes CSS
                            classes_celula = []
                            
                            if is_total:
                                if col == 'Regional':
                                    classes_celula.append("col-regional")
                                elif 'Real' in col or 'Meta' in col or 'Total' in col:
                                    classes_celula.append("valor-destaque")
                            else:
                                if col == 'Regional':
                                    classes_celula.append("col-regional")
                                
                                # Aplicar cores baseadas em valores
                                if '%' in col:
                                    try:
                                        valor_num = float(str(valor_numerico).replace('%', '').replace('+', ''))
                                        if valor_num > 0:
                                            classes_celula.append("valor-positivo")
                                        elif valor_num < 0:
                                            classes_celula.append("valor-negativo")
                                        
                                        # Indicador de performance para alcance da meta
                                        if 'Alcance' in col and valor_num > 0:
                                            if valor_num >= 120:
                                                classes_celula.append("performance-excelente")
                                            elif valor_num >= 100:
                                                classes_celula.append("performance-boa")
                                            elif valor_num >= 80:
                                                classes_celula.append("performance-media")
                                            elif valor_num >= 60:
                                                classes_celula.append("performance-ruim")
                                            else:
                                                classes_celula.append("performance-critica")
                                    except:
                                        pass
                            
                            # Se for célula de mês atual, destacar
                            if f'Real {mes_foco}' in col or f'Meta {mes_foco}' in col:
                                classes_celula.append("highlight-animation")
                            
                            classe_str = ' '.join(classes_celula)
                            
                            html += f'<td class="{classe_str}">{valor_formatado}</td>'
                        
                        html += "</tr>"
                    
                    html += "</tbody></table></div>"
                    
                    return html
                
                # Criar e exibir tabela HTML
                tabela_html = criar_tabela_html_ligacoes(
                    df_exibicao_formatado,
                    df_tabela_final,
                    meses_tabela,
                    mes_selecionado
                )
                
                st.markdown(tabela_html, unsafe_allow_html=True)
                
                # =========================
                # RESUMO ESTATÍSTICO
                # =========================
                st.markdown("---")
                st.markdown("### 📈 **RESUMO ESTATÍSTICO**")
                
                col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                
                with col_res1:
                    total_registros = len(pivot_data_completa) - 1  # Excluir linha de TOTAL
                    st.metric(
                        label="Regiões Analisadas",
                        value=total_registros,
                        delta=None
                    )
                
                with col_res2:
                    if len(pivot_data_completa) > 1:
                        # Calcular alcance médio (excluindo TOTAL)
                        df_alcance = pd.DataFrame(pivot_data_completa[1:])  # Excluir linha TOTAL
                        alcance_medio = df_alcance['Alcance Meta %'].mean() if 'Alcance Meta %' in df_alcance.columns else 0
                        st.metric(
                            label="Alcance Médio da Meta",
                            value=f"{alcance_medio:.1f}%",
                            delta=None
                        )
                
                with col_res3:
                    if len(pivot_data_completa) > 1:
                        # Calcular crescimento médio 2025/2024
                        df_var = pd.DataFrame(pivot_data_completa[1:])
                        crescimento_medio = df_var['Var 2025/2024 %'].mean() if 'Var 2025/2024 %' in df_var.columns else 0
                        st.metric(
                            label="Crescimento Médio 2025/2024",
                            value=f"{crescimento_medio:+.1f}%",
                            delta=None
                        )
                
                with col_res4:
                    total_geral = df_tabela_final.iloc[0]['Total 2025'] if len(df_tabela_final) > 0 else 0
                    st.metric(
                        label="Total Ligações 2025",
                        value=formatar_numero_brasileiro(total_geral, 0),
                        delta=None
                    )
                
                # =========================
                # BOTÕES DE EXPORTAÇÃO
                # =========================
                st.markdown("---")
                col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
                
                with col_exp1:
                    def exportar_excel_tabela_ligacoes(df_numerico):
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            df_numerico.to_excel(writer, index=False, sheet_name='Tabela_Ligacoes')
                            
                            workbook = writer.book
                            worksheet = writer.sheets['Tabela_Ligacoes']
                            
                            # Formatação para cabeçalho
                            header_format = workbook.add_format({
                                'bold': True,
                                'bg_color': '#790E09',
                                'font_color': 'white',
                                'align': 'center',
                                'border': 1,
                                'font_size': 10
                            })
                            
                            # Formatação para números
                            number_format = workbook.add_format({
                                'num_format': '#,##0',
                                'align': 'center'
                            })
                            
                            # Formatação para porcentagens
                            percent_format = workbook.add_format({
                                'num_format': '0.0%',
                                'align': 'center'
                            })
                            
                            # Aplicar formatação
                            for col_num, col_name in enumerate(df_numerico.columns):
                                worksheet.write(0, col_num, col_name, header_format)
                                
                                for row_num in range(1, len(df_numerico) + 1):
                                    value = df_numerico.iloc[row_num-1, col_num]
                                    
                                    if pd.isna(value):
                                        worksheet.write(row_num, col_num, '')
                                    elif col_name == 'Regional':
                                        worksheet.write(row_num, col_num, value)
                                    elif '%' in col_name:
                                        # Converter para decimal para formato Excel
                                        try:
                                            value_pct = float(str(value).replace('%', '')) / 100
                                            worksheet.write(row_num, col_num, value_pct, percent_format)
                                        except:
                                            worksheet.write(row_num, col_num, value)
                                    else:
                                        worksheet.write(row_num, col_num, value, number_format)
                            
                            # Ajustar largura das colunas
                            for i, col in enumerate(df_numerico.columns):
                                column_width = max(df_numerico[col].astype(str).map(len).max(), len(col)) + 2
                                worksheet.set_column(i, i, min(column_width, 20))
                        
                        return output.getvalue()
                    
                    excel_data = exportar_excel_tabela_ligacoes(df_tabela_final)
                    st.download_button(
                        label="📥 Exportar Excel",
                        data=excel_data,
                        file_name=f"tabela_ligacoes_{mes_selecionado.replace('/', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with col_exp2:
                    @st.cache_data
                    def exportar_csv_tabela_ligacoes(df_numerico):
                        return df_numerico.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
                    
                    csv_data = exportar_csv_tabela_ligacoes(df_tabela_final)
                    st.download_button(
                        label="📄 Exportar CSV",
                        data=csv_data,
                        file_name=f"tabela_ligacoes_{mes_selecionado.replace('/', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_exp3:
                    # Resumo dos filtros aplicados
                    filtros_ativos = []
                    if regional_selecionada != "Todas":
                        filtros_ativos.append(f"Regional: {regional_selecionada}")
                    if "Todas" not in plataforma_filtro_tabela:
                        filtros_ativos.append(f"Plataforma: {', '.join(plataforma_filtro_tabela)}")
                    if "Todos" not in tipo_chamada_filtro_tabela:
                        filtros_ativos.append(f"Tipo: {', '.join(tipo_chamada_filtro_tabela)}")
                    
                    resumo_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Sem filtros específicos"
                    
                    st.caption(f"""
                    **📋 Resumo da Tabela:** {total_registros} regiões | **Período:** {meses_tabela[0]} a {meses_tabela[-1]} | 
                    **Mês Foco:** {mes_selecionado} | **Filtros:** {resumo_filtros}
                    """)
                
            else:
                st.warning("""
                ⚠️ **Nenhum dado disponível para exibir a tabela dinâmica.**
                
                **Possíveis causas:**
                1. Não há dados para o mês selecionado
                2. Os filtros aplicados não retornam resultados
                3. Problema na leitura dos arquivos de dados
                """)
                
                # Sugestões de solução
                with st.expander("🔍 Verificar disponibilidade de dados"):
                    if 'mes_ano' in df_lig.columns:
                        meses_disponiveis = sorted(df_lig['mes_ano'].dropna().unique())
                        st.write(f"**Meses disponíveis nos dados:** {', '.join(meses_disponiveis)}")
                    
                    if not df_metas_lig.empty:
                        st.write(f"**Metas carregadas:** {len(df_metas_lig)} registros")
                    else:
                        st.write("**⚠️ Metas não carregadas**")
                    
                    st.write(f"**Regional selecionada:** {regional_selecionada}")
                    st.write(f"**Plataforma filtro:** {plataforma_filtro_tabela}")
                    st.write(f"**Tipo chamada filtro:** {tipo_chamada_filtro_tabela}")

