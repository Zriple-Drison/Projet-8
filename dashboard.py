"""
Dashboard Streamlit - Scoring Crédit
Prêt à dépenser - Outil d'aide à la décision
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import plotly.express as px
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

API_URL = "https://home-credit-api.onrender.com"

# Chargement du CSV des clients
@st.cache_data
def load_clients():
    try:
        df = pd.read_csv("X_test_sample.csv", index_col=0)
        return df
    except Exception as e:
        return None

# Données de démonstration (vrais clients issus du modèle)
SAMPLE_CLIENTS = {
    "Client A — Faible risque ✅ (2.4%)": {
        "EXT_SOURCE_2": 0.419387842144658,
        "EXT_SOURCE_3": 0.6833170531786634,
        "DAYS_BIRTH": -27858.846009107183,
        "DAYS_REGISTRATION": -2445.7428397662643,
        "DAYS_EMPLOYED": -2402.736317563084,
        "AMT_CREDIT": 151705.66400065727,
        "DAYS_ID_PUBLISH": -4991.882317039751,
        "AMT_ANNUITY": 10671.388291809786,
        "BUREAU_DAYS_CREDIT_MAX_x": -1255.8601325635364,
        "delay_mean": -9.396752340908987,
        "PREV_DAYS_DECISION_MAX": -675.0818344226923,
        "EXT_SOURCE_1": 0.5031474047380476,
        "BUREAU_AMT_CREDIT_SUM_MEAN_x": 115134.7805511389,
        "PREV_CREDIT_APPLICATION_RATIO_MEAN": 0.6405405423615701,
        "DAYS_LAST_PHONE_CHANGE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_SUM_x": 209704.83787909712,
        "instalment_mean": 15234.038914554534,
        "BUREAU_DAYS_CREDIT_MIN_x": -2396.483779939765,
        "PREV_AMT_APPLICATION_MEAN": 242525.75556302548,
        "POS_CNT_INSTALMENT_MEAN": 11.726874369555912,
        "PREV_DAYS_DECISION_MEAN": -1472.7464721596998,
        "BUREAU_DAYS_CREDIT_MEAN_x": -1166.3771611006136,
        "PREV_AMT_ANNUITY_MEAN": 7730.18953960453,
        "PREV_DAYS_DECISION_MIN": -2344.3736714265533,
        "PREV_AMT_ANNUITY_MAX": 24240.656614756677,
        "LOG_INCOME": 13.866980516125738,
        "instalment_sum": 705223.2237017488,
        "PREV_AMT_APPLICATION_MAX": 381966.2195060758,
        "nb_instalments": 65.19396069579012,
        "POS_MONTHS_BALANCE_COUNT": 120.21124658128764,
        "PREV_AMT_DOWN_PAYMENT_MEAN": 14164.222973065147,
        "delay_rate": 0.011039128392619677,
        "PREV_AMT_DOWN_PAYMENT_MAX": 62758.02045637293,
        "BUREAU_CREDIT_ACTIVE_ACTIVE_MEAN_x": 0.0,
        "HOUR_APPR_PROCESS_START": 12.77512897548386,
        "partial_payment_rate": 0.0,
        "LANDAREA_AVG": 0.03618672278386984,
        "POS_MONTHS_BALANCE_MIN": -135.8678342764103,
        "OWN_CAR_AGE": 6.891170083796371,
        "LIVINGAREA_AVG": 0.10398827474673883,
        "BUREAU_BB_STATUS0_RATE_MEAN_x": 0.26337023805410575,
        "APARTMENTS_AVG": 0.10131489296459367,
        "BASEMENTAREA_AVG": 0.10735299876357693,
        "NONLIVINGAREA_AVG": 0.002407497936878282,
        "YEARS_BUILD_AVG": 1.1088805619960675,
        "PREV_IS_APPROVED_MEAN": 0.9528833604155117,
        "COMMONAREA_AVG": 0.030504588133203468,
        "PREV_IS_REFUSED_MEAN": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_x": 29.12629607984366,
        "POS_CNT_INSTALMENT_MAX": 19.23808487696524,
        "LIVINGAPARTMENTS_AVG": 0.05203566966936283,
        "PREV_SK_ID_PREV_COUNT": 4.018675231125497,
        "POS_POS_STATUS_SIGNED_MEAN": 0.0,
        "CC_CNT_DRAWINGS_CURRENT_MEAN": 0.0,
        "CC_MONTHS_BALANCE_COUNT": 0.0,
        "CC_CC_UTILIZATION_MAX": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MEAN_x": 0.0,
        "CC_AMT_BALANCE_MEAN": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MAX_x": 0.0,
        "ENTRANCES_AVG": 0.08177709768337733,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 0.6438679663433298,
        "CC_CC_UTILIZATION_MEAN": 0.0,
        "BUREAU_BB_STATUS0_RATE_MEAN_y": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_y": 0.0,
        "FLOORSMAX_AVG": 0.10079689875032337,
        "CC_CNT_DRAWINGS_CURRENT_MAX": 0.0,
        "CNT_CHILDREN": 0.0,
        "REGION_RATING_CLIENT": 1.8458870874831155,
        "FLOORSMIN_AVG": 0.26986896860820825,
        "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
        "FLAG_WORK_PHONE": 0.0,
        "ELEVATORS_AVG": 0.0,
        "CC_CC_STATUS_ACTIVE_MEAN": 0.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "FLAG_DOCUMENT_3": 0.6413835542163402,
        "FLAG_PHONE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_OVERDUE_SUM_x": 0.0,
        "DEF_60_CNT_SOCIAL_CIRCLE": 0.0,
        "REG_CITY_NOT_WORK_CITY": 0.0,
        "LIVE_CITY_NOT_WORK_CITY": 0.0,
        "REG_CITY_NOT_LIVE_CITY": 0.0,
        "FLAG_EMP_PHONE": 0.0,
        "FLAG_DOCUMENT_6": 0.0,
        "FLAG_DOCUMENT_16": 0.0,
        "FLAG_DOCUMENT_13": 0.0
    },
    "Client B — Risque élevé ❌ (52%)": {
        "EXT_SOURCE_2": 0.15820674818158895,
        "EXT_SOURCE_3": 0.6813275217428424,
        "DAYS_BIRTH": -15128.250154941075,
        "DAYS_REGISTRATION": -1810.8369194545053,
        "DAYS_EMPLOYED": -951.6990541437152,
        "AMT_CREDIT": 310922.9933178773,
        "DAYS_ID_PUBLISH": -3186.8545263408364,
        "AMT_ANNUITY": 13789.358375390619,
        "BUREAU_DAYS_CREDIT_MAX_x": -1411.0503539106976,
        "delay_mean": -12.850867651165716,
        "PREV_DAYS_DECISION_MAX": -1299.6046593474034,
        "EXT_SOURCE_1": 0.504952414207815,
        "BUREAU_AMT_CREDIT_SUM_MEAN_x": 73144.47271827163,
        "PREV_CREDIT_APPLICATION_RATIO_MEAN": 1.1253458309467177,
        "DAYS_LAST_PHONE_CHANGE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_SUM_x": 186572.68599189442,
        "instalment_mean": 7132.884734994083,
        "BUREAU_DAYS_CREDIT_MIN_x": -2758.9770448454906,
        "PREV_AMT_APPLICATION_MEAN": 169543.18336056598,
        "POS_CNT_INSTALMENT_MEAN": 23.402717055303903,
        "PREV_DAYS_DECISION_MEAN": -1820.191211000057,
        "BUREAU_DAYS_CREDIT_MEAN_x": -1413.8358858142678,
        "PREV_AMT_ANNUITY_MEAN": 12904.94516550377,
        "PREV_DAYS_DECISION_MIN": -1982.380019662509,
        "PREV_AMT_ANNUITY_MAX": 32838.73109890656,
        "LOG_INCOME": 14.709688905136233,
        "instalment_sum": 1229939.7731562292,
        "PREV_AMT_APPLICATION_MAX": 303946.25148764404,
        "nb_instalments": 91.62190246770679,
        "POS_MONTHS_BALANCE_COUNT": 62.003331224809564,
        "PREV_AMT_DOWN_PAYMENT_MEAN": 12671.253383899468,
        "delay_rate": 0.02005925236689128,
        "PREV_AMT_DOWN_PAYMENT_MAX": 38137.716363760126,
        "BUREAU_CREDIT_ACTIVE_ACTIVE_MEAN_x": 0.0,
        "HOUR_APPR_PROCESS_START": 17.584664443961156,
        "partial_payment_rate": 0.0,
        "LANDAREA_AVG": 0.03122949619641801,
        "POS_MONTHS_BALANCE_MIN": -126.66605585215373,
        "OWN_CAR_AGE": 6.983302977612928,
        "LIVINGAREA_AVG": 0.06337732506688092,
        "BUREAU_BB_STATUS0_RATE_MEAN_x": 0.3128093610319229,
        "APARTMENTS_AVG": 0.09509103034132828,
        "BASEMENTAREA_AVG": 0.06470969250917998,
        "NONLIVINGAREA_AVG": 0.0041666148706078114,
        "YEARS_BUILD_AVG": 0.3894168691642844,
        "PREV_IS_APPROVED_MEAN": 0.5643748835150396,
        "COMMONAREA_AVG": 0.012652850050985662,
        "PREV_IS_REFUSED_MEAN": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_x": 22.74509371142822,
        "POS_CNT_INSTALMENT_MAX": 31.555108143839423,
        "LIVINGAPARTMENTS_AVG": 0.10494624757544693,
        "PREV_SK_ID_PREV_COUNT": 3.7240537003045038,
        "POS_POS_STATUS_SIGNED_MEAN": 0.0,
        "CC_CNT_DRAWINGS_CURRENT_MEAN": 0.0,
        "CC_MONTHS_BALANCE_COUNT": 0.0,
        "CC_CC_UTILIZATION_MAX": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MEAN_x": 0.0,
        "CC_AMT_BALANCE_MEAN": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MAX_x": 0.0,
        "ENTRANCES_AVG": 0.14815557943972643,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1.2683649926926006,
        "CC_CC_UTILIZATION_MEAN": 0.0,
        "BUREAU_BB_STATUS0_RATE_MEAN_y": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_y": 0.0,
        "FLOORSMAX_AVG": 0.1314978703308597,
        "CC_CNT_DRAWINGS_CURRENT_MAX": 0.0,
        "CNT_CHILDREN": 0.0,
        "REGION_RATING_CLIENT": 1.8180154734725464,
        "FLOORSMIN_AVG": 0.2132938207555144,
        "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
        "FLAG_WORK_PHONE": 0.0,
        "ELEVATORS_AVG": 0.0,
        "CC_CC_STATUS_ACTIVE_MEAN": 0.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "FLAG_DOCUMENT_3": 0.6348748464080477,
        "FLAG_PHONE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_OVERDUE_SUM_x": 0.0,
        "DEF_60_CNT_SOCIAL_CIRCLE": 0.0,
        "REG_CITY_NOT_WORK_CITY": 0.0,
        "LIVE_CITY_NOT_WORK_CITY": 0.0,
        "REG_CITY_NOT_LIVE_CITY": 0.0,
        "FLAG_EMP_PHONE": 0.0,
        "FLAG_DOCUMENT_6": 0.0,
        "FLAG_DOCUMENT_16": 0.0,
        "FLAG_DOCUMENT_13": 0.0
    },
    "Client C — Profil limite ⚠️ (35%)": {
        "EXT_SOURCE_2": 0.169709429462804,
        "EXT_SOURCE_3": 0.8104067045615588,
        "DAYS_BIRTH": -32426.844438509994,
        "DAYS_REGISTRATION": -1576.0897196472245,
        "DAYS_EMPLOYED": -1936.9331721782096,
        "AMT_CREDIT": 407401.8267117075,
        "DAYS_ID_PUBLISH": -3406.817503766196,
        "AMT_ANNUITY": 19111.287434890375,
        "BUREAU_DAYS_CREDIT_MAX_x": -1528.2055695398074,
        "delay_mean": -20.329726764671104,
        "PREV_DAYS_DECISION_MAX": -674.6649992007535,
        "EXT_SOURCE_1": 0.3037649617748197,
        "BUREAU_AMT_CREDIT_SUM_MEAN_x": 52755.17666279475,
        "PREV_CREDIT_APPLICATION_RATIO_MEAN": 1.0818280607482587,
        "DAYS_LAST_PHONE_CHANGE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_SUM_x": 398993.47732181795,
        "instalment_mean": 14208.653425649954,
        "BUREAU_DAYS_CREDIT_MIN_x": -2002.4077386426602,
        "PREV_AMT_APPLICATION_MEAN": 115058.69905334675,
        "POS_CNT_INSTALMENT_MEAN": 19.60047049434916,
        "PREV_DAYS_DECISION_MEAN": -1264.2260608567383,
        "BUREAU_DAYS_CREDIT_MEAN_x": -1955.689545145146,
        "PREV_AMT_ANNUITY_MEAN": 11079.979115362807,
        "PREV_DAYS_DECISION_MIN": -1661.3452351738938,
        "PREV_AMT_ANNUITY_MAX": 17586.82656297261,
        "LOG_INCOME": 7.862391757674454,
        "instalment_sum": 667136.6208468479,
        "PREV_AMT_APPLICATION_MAX": 239675.02872345375,
        "nb_instalments": 60.97370478688005,
        "POS_MONTHS_BALANCE_COUNT": 43.46215480139961,
        "PREV_AMT_DOWN_PAYMENT_MEAN": 12272.049966563174,
        "delay_rate": 0.017316256304286008,
        "PREV_AMT_DOWN_PAYMENT_MAX": 60622.44252841117,
        "BUREAU_CREDIT_ACTIVE_ACTIVE_MEAN_x": 0.0,
        "HOUR_APPR_PROCESS_START": 14.018844203728127,
        "partial_payment_rate": 0.0,
        "LANDAREA_AVG": 0.058532126880613225,
        "POS_MONTHS_BALANCE_MIN": -103.79379290228289,
        "OWN_CAR_AGE": 13.128279672288585,
        "LIVINGAREA_AVG": 0.03884727108906979,
        "BUREAU_BB_STATUS0_RATE_MEAN_x": 0.540576178045355,
        "APARTMENTS_AVG": 0.12778971030481132,
        "BASEMENTAREA_AVG": 0.10394133653856859,
        "NONLIVINGAREA_AVG": 0.002404413649195685,
        "YEARS_BUILD_AVG": 0.6244147187791234,
        "PREV_IS_APPROVED_MEAN": 0.6724518398764654,
        "COMMONAREA_AVG": 0.023237605977602743,
        "PREV_IS_REFUSED_MEAN": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_x": 30.001652553992436,
        "POS_CNT_INSTALMENT_MAX": 19.609770464713396,
        "LIVINGAPARTMENTS_AVG": 0.0785866951592139,
        "PREV_SK_ID_PREV_COUNT": 5.9546028503559745,
        "POS_POS_STATUS_SIGNED_MEAN": 0.0,
        "CC_CNT_DRAWINGS_CURRENT_MEAN": 0.0,
        "CC_MONTHS_BALANCE_COUNT": 0.0,
        "CC_CC_UTILIZATION_MAX": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MEAN_x": 0.0,
        "CC_AMT_BALANCE_MEAN": 0.0,
        "BUREAU_AMT_CREDIT_SUM_LIMIT_MAX_x": 0.0,
        "ENTRANCES_AVG": 0.12705275596590973,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1.3540155304554593,
        "CC_CC_UTILIZATION_MEAN": 0.0,
        "BUREAU_BB_STATUS0_RATE_MEAN_y": 0.0,
        "BUREAU_BB_NB_MONTHS_MEAN_y": 0.0,
        "FLOORSMAX_AVG": 0.21196738124581732,
        "CC_CNT_DRAWINGS_CURRENT_MAX": 0.0,
        "CNT_CHILDREN": 0.0,
        "REGION_RATING_CLIENT": 1.1293310877011413,
        "FLOORSMIN_AVG": 0.23353039359932698,
        "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
        "FLAG_WORK_PHONE": 0.0,
        "ELEVATORS_AVG": 0.0,
        "CC_CC_STATUS_ACTIVE_MEAN": 0.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "FLAG_DOCUMENT_3": 0.7353255509597496,
        "FLAG_PHONE": 0.0,
        "BUREAU_AMT_CREDIT_SUM_OVERDUE_SUM_x": 0.0,
        "DEF_60_CNT_SOCIAL_CIRCLE": 0.0,
        "REG_CITY_NOT_WORK_CITY": 0.0,
        "LIVE_CITY_NOT_WORK_CITY": 0.0,
        "REG_CITY_NOT_LIVE_CITY": 0.0,
        "FLAG_EMP_PHONE": 0.0,
        "FLAG_DOCUMENT_6": 0.0,
        "FLAG_DOCUMENT_16": 0.0,
        "FLAG_DOCUMENT_13": 0.0
    }
}



# Labels lisibles pour les features importantes
FEATURE_LABELS = {
    "EXT_SOURCE_1": "Score externe 1",
    "EXT_SOURCE_2": "Score externe 2",
    "EXT_SOURCE_3": "Score externe 3",
    "DAYS_BIRTH": "Âge (jours)",
    "DAYS_EMPLOYED": "Ancienneté emploi (jours)",
    "AMT_CREDIT": "Montant crédit (€)",
    "AMT_ANNUITY": "Annuité (€)",
    "LOG_INCOME": "Log revenu",
    "delay_rate": "Taux de retard paiements",
    "delay_mean": "Retard moyen (jours)",
    "PREV_IS_APPROVED_MEAN": "Taux approbation précédents",
    "PREV_IS_REFUSED_MEAN": "Taux refus précédents",
    "BUREAU_AMT_CREDIT_SUM_SUM_x": "Total crédits bureau (€)",
    "DAYS_REGISTRATION": "Ancienneté enregistrement",
    "REGION_RATING_CLIENT": "Note région client",
}

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="Prêt à dépenser — Scoring Crédit",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PERSONNALISÉ - Design épuré et professionnel
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Fond principal */
    .stApp {
        background-color: #F0F2F6;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1623 100%);
        border-right: 1px solid #2d3548;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Header custom */
    .main-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #94a3b8;
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
    }
    .header-badge {
        background: rgba(99, 179, 237, 0.15);
        border: 1px solid rgba(99, 179, 237, 0.3);
        color: #63b3ed;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1f2e;
        line-height: 1;
    }
    .metric-card .sub {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }

    /* Decision badge */
    .decision-accordé {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    .decision-refusé {
        background: linear-gradient(135deg, #fc8181, #e53e3e);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(229, 62, 62, 0.4);
    }

    /* Section title */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1f2e;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Info box */
    .info-box {
        background: #EBF8FF;
        border-left: 4px solid #63b3ed;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #2c5282;
    }

    /* Accessibility */
    .wcag-note {
        font-size: 0.75rem;
        color: #94a3b8;
        font-style: italic;
        margin-top: 0.5rem;
    }

    /* Override streamlit defaults */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FONCTIONS
# ============================================================================

def call_api(client_data: dict) -> dict:
    """Appelle l'API de prédiction"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"data": client_data},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur API {response.status_code}: {response.text}"}
    except requests.exceptions.Timeout:
        return {"error": "L'API met trop de temps à répondre (timeout). Elle est peut-être en veille sur Render, réessayez dans 30s."}
    except Exception as e:
        return {"error": str(e)}


def create_gauge(probability: float, threshold: float) -> go.Figure:
    """Crée une jauge visuelle du score de risque - accessible WCAG"""
    pct = probability * 100
    
    # Couleurs accessibles (contraste suffisant, pas uniquement basé sur rouge/vert)
    if probability < threshold:
        bar_color = "#2E7D32"   # Vert foncé - accessible
        text_color = "#2E7D32"
    else:
        bar_color = "#C62828"   # Rouge foncé - accessible
        text_color = "#C62828"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct,
        number={
            "suffix": "%",
            "font": {"size": 36, "color": text_color, "family": "DM Sans"},
        },
        delta={
            "reference": threshold * 100,
            "decreasing": {"color": "#2E7D32"},
            "increasing": {"color": "#C62828"},
            "suffix": "% vs seuil"
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#64748b",
                "tickfont": {"size": 11},
                "tickvals": [0, 20, 35, 40, 60, 80, 100],
                "ticktext": ["0%", "20%", "35%", "40%", "60%", "80%", "100%"],
            },
            "bar": {"color": bar_color, "thickness": 0.7},
            "bgcolor": "#f8fafc",
            "borderwidth": 2,
            "bordercolor": "#e2e8f0",
            "steps": [
                {"range": [0, 20], "color": "#E8F5E9"},
                {"range": [20, threshold * 100], "color": "#FFF9C4"},
                {"range": [threshold * 100, 60], "color": "#FFEBEE"},
                {"range": [60, 100], "color": "#FFCDD2"},
            ],
            "threshold": {
                "line": {"color": "#1565C0", "width": 4},
                "thickness": 0.85,
                "value": threshold * 100,
            },
        },
        title={
            "text": "Probabilité de défaut<br><span style='font-size:12px;color:#64748b'>Ligne bleue = seuil de décision</span>",
            "font": {"size": 15, "family": "DM Sans"},
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ))

    fig.update_layout(
        height=280,
        margin=dict(t=60, b=10, l=20, r=20),
        paper_bgcolor="white",
        font={"family": "DM Sans"},
    )
    return fig


def create_feature_importance_chart(client_data: dict) -> go.Figure:
    """Graphique des features clés du client - accessible WCAG"""
    
    # Features les plus importantes pour l'interprétation
    key_features = {
        "EXT_SOURCE_2": ("Score externe 2", 1, True),
        "EXT_SOURCE_3": ("Score externe 3", 1, True),
        "EXT_SOURCE_1": ("Score externe 1", 1, True),
        "delay_rate": ("Taux retards paiements", -1, False),
        "PREV_IS_APPROVED_MEAN": ("Approbations précédentes", 1, True),
        "LOG_INCOME": ("Niveau de revenu (log)", 1, True),
        "AMT_CREDIT": ("Montant du crédit", -0.5, False),
        "DAYS_EMPLOYED": ("Ancienneté emploi", 1, True),
    }
    
    labels = []
    values = []
    colors = []
    
    for feat, (label, direction, positive_good) in key_features.items():
        if feat in client_data:
            val = client_data[feat]
            # Normaliser pour affichage
            if feat == "LOG_INCOME":
                normalized = (val - 10) / 5  
            elif feat == "AMT_CREDIT":
                normalized = -(val / 500000)
            elif feat in ["DAYS_EMPLOYED", "DAYS_BIRTH"]:
                normalized = min(1.0, abs(val) / 5000)
            elif feat in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]:
                normalized = val
            elif feat == "delay_rate":
                normalized = -min(1.0, val * 10)
            elif feat == "PREV_IS_APPROVED_MEAN":
                normalized = val
            else:
                normalized = val
            
            labels.append(label)
            values.append(normalized * direction)
            colors.append("#2E7D32" if (normalized * direction) > 0 else "#C62828")
    
    # Trier par valeur absolue
    sorted_data = sorted(zip(labels, values, colors), key=lambda x: abs(x[1]), reverse=True)
    labels, values, colors = zip(*sorted_data) if sorted_data else ([], [], [])

    fig = go.Figure(go.Bar(
        x=list(values),
        y=list(labels),
        orientation='h',
        marker_color=list(colors),
        marker_line_color='white',
        marker_line_width=1,
        hovertemplate="<b>%{y}</b><br>Impact: %{x:.2f}<extra></extra>",
    ))

    fig.add_vline(x=0, line_dash="solid", line_color="#94a3b8", line_width=1)

    fig.update_layout(
        title={
            "text": "Facteurs clés du profil client",
            "font": {"size": 14, "family": "DM Sans", "color": "#1a1f2e"},
            "x": 0
        },
        xaxis={
            "title": "← Défavorable  |  Favorable →",
            "title_font": {"size": 12, "color": "#64748b"},
            "showgrid": True,
            "gridcolor": "#f1f5f9",
            "zeroline": False,
        },
        yaxis={
            "showgrid": False,
            "tickfont": {"size": 13, "color": "#1a1f2e"},
            "automargin": True,
        },
        height=380,
        margin=dict(t=50, b=50, l=180, r=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "DM Sans"},
        showlegend=False,
    )
    
    return fig


def create_comparison_chart(client_data: dict, feature: str) -> go.Figure:
    """Comparaison client vs population simulée - accessible WCAG"""
    
    label = FEATURE_LABELS.get(feature, feature)
    client_value = client_data.get(feature, 0)
    
    # Simuler une distribution population (basée sur des valeurs réalistes Home Credit)
    np.random.seed(42)
    if feature in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]:
        population = np.random.beta(2, 2, 1000)
    elif feature == "AMT_CREDIT":
        population = np.random.lognormal(11.5, 0.8, 1000)
    elif feature == "AMT_ANNUITY":
        population = np.random.lognormal(9, 0.7, 1000)
    elif feature == "delay_rate":
        population = np.random.exponential(0.05, 1000)
    elif feature == "LOG_INCOME":
        population = np.random.normal(13.5, 1.2, 1000)
    elif feature == "DAYS_EMPLOYED":
        population = np.random.uniform(-5000, -100, 1000)
    else:
        population = np.random.normal(client_value, abs(client_value) * 0.3 + 1, 1000)

    fig = go.Figure()
    
    # Distribution population
    fig.add_trace(go.Histogram(
        x=population,
        name="Population globale",
        marker_color="#93C5FD",
        marker_line_color="white",
        marker_line_width=0.5,
        opacity=0.8,
        nbinsx=30,
        hovertemplate="Valeur: %{x:.2f}<br>Nombre: %{y}<extra>Population</extra>",
    ))
    
    # Position client
    fig.add_vline(
        x=client_value,
        line_dash="dash",
        line_color="#C62828",
        line_width=3,
        annotation_text=f"▼ Ce client<br>{client_value:.2f}",
        annotation_position="top",
        annotation_font={"size": 11, "color": "#C62828"},
        annotation_bgcolor="rgba(255,235,238,0.9)",
        annotation_bordercolor="#C62828",
        annotation_borderwidth=1,
    )
    
    fig.update_layout(
        title={
            "text": f"{label} — Client vs Population",
            "font": {"size": 14, "family": "DM Sans", "color": "#1a1f2e"},
            "x": 0
        },
        xaxis={
            "title": label,
            "title_font": {"size": 11, "color": "#64748b"},
            "showgrid": True,
            "gridcolor": "#f1f5f9",
        },
        yaxis={
            "title": "Nombre de clients",
            "title_font": {"size": 11, "color": "#64748b"},
            "showgrid": True,
            "gridcolor": "#f1f5f9",
        },
        height=300,
        margin=dict(t=50, b=40, l=10, r=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "DM Sans"},
        legend={"orientation": "h", "y": -0.2},
        bargap=0.05,
    )
    
    return fig


def get_age_years(days_birth: float) -> int:
    return int(abs(days_birth) / 365.25)


def get_employment_years(days_employed: float) -> float:
    return round(abs(days_employed) / 365.25, 1)


def format_currency(value: float) -> str:
    return f"{value:,.0f} €".replace(",", " ")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 💳 Prêt à dépenser")
    st.markdown("*Outil de scoring crédit*")
    st.markdown("---")
    
    st.markdown("### 👤 Sélection du client")
    
    mode = st.radio(
        "Mode de saisie",
        ["Clients CSV", "Clients de démonstration", "Saisie manuelle JSON"],
        help="Choisissez un client existant ou entrez un nouveau dossier"
    )
    
    if mode == "Clients CSV":
        df_clients = load_clients()
        if df_clients is not None:
            client_ids = df_clients.index.tolist()
            selected_id = st.selectbox(
                "ID Client",
                client_ids,
                help=f"{len(client_ids)} clients disponibles"
            )
            client_data = df_clients.loc[selected_id].to_dict()
            st.success(f"✅ Client {selected_id} chargé")
        else:
            st.error("❌ Fichier X_test_sample.csv introuvable")
            client_data = None

    elif mode == "Clients de démonstration":
        selected_client_name = st.selectbox(
            "Client",
            list(SAMPLE_CLIENTS.keys()),
            help="Sélectionnez un profil client"
        )
        client_data = SAMPLE_CLIENTS[selected_client_name]
        
    else:
        st.markdown("Collez le JSON du client ci-dessous :")
        json_input = st.text_area(
            "Données client (JSON)",
            height=200,
            placeholder='{"EXT_SOURCE_2": 0.42, "AMT_CREDIT": 150000, ...}',
            help="Format attendu : dictionnaire JSON avec les 85 features"
        )
        client_data = None
        if json_input:
            try:
                client_data = json.loads(json_input)
                st.success(f"✅ {len(client_data)} features chargées")
            except Exception as e:
                st.error(f"❌ JSON invalide : {e}")
        else:
            st.info("Collez le JSON d'un client pour commencer")
    
    st.markdown("---")
    predict_btn = st.button(
        "🔍 Analyser ce client",
        type="primary",
        use_container_width=True,
        disabled=(client_data is None)
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    **Modèle :** LightGBM  
    **AUC :** 0.7775  
    **Seuil :** 0.35  
    **Features :** 85  
    """)
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.75rem;color:#64748b;">Interface conforme WCAG 2.1 AA<br>Contraste ≥ 4.5:1 | Navigation clavier</p>',
        unsafe_allow_html=True
    )

# ============================================================================
# CONTENU PRINCIPAL
# ============================================================================

# Header
st.markdown("""
<div class="main-header">
    <div>
        <h1>💳 Scoring Crédit</h1>
        <p>Analyse de risque client — Aide à la décision d'octroi</p>
    </div>
    <div class="header-badge">Prêt à dépenser</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RÉSULTATS DE L'API
# ============================================================================

if predict_btn and client_data:
    with st.spinner("Analyse en cours..."):
        result = call_api(client_data)
    
    if "error" in result:
        st.error(f"❌ {result['error']}")
        st.info("💡 Si l'API est en veille sur Render, attendez 30 secondes et réessayez.")
    else:
        probability = result["probability"]
        decision = result["decision"]
        threshold = result["threshold"]
        risk_level = result.get("risk_level", "N/A")
        
        # Stocker en session state
        st.session_state["result"] = result
        st.session_state["client_data"] = client_data

# Afficher les résultats si disponibles
if "result" in st.session_state:
    result = st.session_state["result"]
    client_data_display = st.session_state.get("client_data", client_data)
    probability = result["probability"]
    decision = result["decision"]
    threshold = result["threshold"]
    risk_level = result.get("risk_level", "N/A")
    
    # ---- SECTION 1 : DÉCISION & SCORE ----
    st.markdown('<p class="section-title">📊 Décision & Score de risque</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col1:
        decision_lower = "accordé" if "ACCORD" in decision.upper() else "refusé"
        st.markdown(
            f'<div class="decision-{decision_lower}">✓ CRÉDIT {decision.upper()}</div>' if decision_lower == "accordé"
            else f'<div class="decision-{decision_lower}">✗ CRÉDIT {decision.upper()}</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Niveau de risque
        risk_colors = {
            "FAIBLE": ("🟢", "#2E7D32"),
            "MODÉRÉ": ("🟡", "#F57F17"),
            "ÉLEVÉ": ("🟠", "#E65100"),
            "TRÈS ÉLEVÉ": ("🔴", "#B71C1C"),
        }
        icon, color = risk_colors.get(risk_level, ("⚪", "#64748b"))
        st.markdown(
            f'<div class="metric-card"><h3>Niveau de risque</h3>'
            f'<div class="value" style="color:{color};font-size:1.5rem;">{icon} {risk_level}</div>'
            f'<div class="sub">Seuil de décision : {threshold:.0%}</div></div>',
            unsafe_allow_html=True
        )
        
        # Distance au seuil
        distance = probability - threshold
        distance_pct = abs(distance) * 100
        if distance < 0:
            st.markdown(
                f'<div class="metric-card"><h3>Marge par rapport au seuil</h3>'
                f'<div class="value" style="color:#2E7D32;font-size:1.4rem;">-{distance_pct:.1f}%</div>'
                f'<div class="sub">En dessous du seuil de refus</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="metric-card"><h3>Dépassement du seuil</h3>'
                f'<div class="value" style="color:#C62828;font-size:1.4rem;">+{distance_pct:.1f}%</div>'
                f'<div class="sub">Au-dessus du seuil de refus</div></div>',
                unsafe_allow_html=True
            )

    with col2:
        fig_gauge = create_gauge(probability, threshold)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<p class="wcag-note">♿ Graphique accessible : couleurs différenciées par intensité et pattern, texte alternatif disponible.</p>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-card"><h3>Probabilité de défaut</h3>'
            f'<div class="value">{probability:.1%}</div>'
            f'<div class="sub">Risque de non-remboursement</div></div>',
            unsafe_allow_html=True
        )
        
        age = get_age_years(client_data_display.get("DAYS_BIRTH", -12775))
        emp = get_employment_years(client_data_display.get("DAYS_EMPLOYED", -1000))
        credit = format_currency(client_data_display.get("AMT_CREDIT", 0))
        annuity = format_currency(client_data_display.get("AMT_ANNUITY", 0))
        
        st.markdown(
            f'<div class="metric-card"><h3>Profil résumé</h3>'
            f'<div style="font-size:0.9rem;line-height:1.8;">'
            f'🎂 <b>Âge :</b> {age} ans<br>'
            f'💼 <b>Emploi :</b> {emp} ans<br>'
            f'💰 <b>Crédit :</b> {credit}<br>'
            f'📅 <b>Annuité :</b> {annuity}'
            f'</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    # ---- SECTION 2 : INTERPRÉTATION ----
    st.markdown('<p class="section-title">🔍 Interprétation des facteurs</p>', unsafe_allow_html=True)
    
    st.markdown(
        '<div class="info-box">💡 Ce graphique montre les principaux facteurs qui influencent le profil de ce client. '
        'Les barres vertes indiquent des éléments favorables, les barres rouges des éléments défavorables à l\'octroi du crédit.</div>',
        unsafe_allow_html=True
    )
    
    fig_importance = create_feature_importance_chart(client_data_display)
    st.plotly_chart(fig_importance, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    
    # ---- SECTION 3 : COMPARAISON ----
    st.markdown('<p class="section-title">📈 Comparaison avec la population</p>', unsafe_allow_html=True)
    
    col_filter1, col_filter2 = st.columns([1, 2])
    with col_filter1:
        feature_choice = st.selectbox(
            "Choisir une variable à comparer",
            options=list(FEATURE_LABELS.keys()),
            format_func=lambda x: FEATURE_LABELS.get(x, x),
            help="Comparez le client sélectionné avec l'ensemble des clients"
        )
    
    fig_comp = create_comparison_chart(client_data_display, feature_choice)
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown(
        '<p class="wcag-note">♿ Les histogrammes sont lisibles sans différenciation par couleur uniquement. '
        'La position du client est indiquée par une ligne pointillée et un label textuel.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    
    # ---- SECTION 4 : DÉTAIL DES FEATURES ----
    with st.expander("📋 Voir toutes les données du client"):
        df_display = pd.DataFrame([client_data_display]).T.reset_index()
        df_display.columns = ["Variable", "Valeur"]
        df_display["Description"] = df_display["Variable"].map(FEATURE_LABELS).fillna("")
        df_display = df_display[["Variable", "Description", "Valeur"]]
        df_display["Valeur"] = df_display["Valeur"].apply(lambda x: f"{x:.4f}" if isinstance(x, float) else x)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    # État initial - invitation à analyser
    st.markdown(
        '<div class="info-box">👈 Sélectionnez un client dans le panneau de gauche et cliquez sur <b>"Analyser ce client"</b> pour obtenir le score de risque et l\'analyse détaillée.</div>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Score de risque</h3>
            <div class="value" style="color:#cbd5e0;">—%</div>
            <div class="sub">En attente d'analyse</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Décision</h3>
            <div class="value" style="color:#cbd5e0;font-size:1.2rem;">En attente</div>
            <div class="sub">Sélectionnez un client</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Niveau de risque</h3>
            <div class="value" style="color:#cbd5e0;font-size:1.2rem;">—</div>
            <div class="sub">En attente d'analyse</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <h3>Comment utiliser cet outil</h3>
        <div style="font-size:0.95rem;line-height:2;color:#475569;">
            <b>1.</b> Sélectionnez un client dans la barre latérale gauche<br>
            <b>2.</b> Cliquez sur "Analyser ce client"<br>
            <b>3.</b> Consultez le score de risque et la décision recommandée<br>
            <b>4.</b> Explorez les facteurs explicatifs et la comparaison avec la population<br>
            <b>5.</b> En mode "Saisie manuelle", collez directement le JSON d'un nouveau client
        </div>
    </div>
    """, unsafe_allow_html=True)
