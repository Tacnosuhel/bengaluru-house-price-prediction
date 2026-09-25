import requests
import streamlit as st

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── All 241 locations (hard-coded from columns.json) ──────────
LOCATIONS = [
    '1st block jayanagar', '1st phase jp nagar', '2nd phase judicial layout',
    '2nd stage nagarbhavi', '5th block hbr layout', '5th phase jp nagar',
    '6th phase jp nagar', '7th phase jp nagar', '8th phase jp nagar',
    '9th phase jp nagar', 'aecs layout', 'abbigere', 'akshaya nagar',
    'ambalipura', 'ambedkar nagar', 'amruthahalli', 'anandapura', 'ananth nagar',
    'anekal', 'anjanapura', 'ardendale', 'arekere', 'attibele', 'beml layout',
    'btm 2nd stage', 'btm layout', 'babusapalaya', 'badavala nagar', 'balagere',
    'banashankari', 'banashankari stage ii', 'banashankari stage iii',
    'banashankari stage v', 'banashankari stage vi', 'banaswadi', 'banjara layout',
    'bannerghatta', 'bannerghatta road', 'basavangudi', 'basaveshwara nagar',
    'battarahalli', 'begur', 'begur road', 'bellandur', 'benson town',
    'bharathi nagar', 'bhoganhalli', 'billekahalli', 'binny pete', 'bisuvanahalli',
    'bommanahalli', 'bommasandra', 'bommasandra industrial area', 'bommenahalli',
    'brookefield', 'budigere', 'cv raman nagar', 'chamrajpet', 'chandapura',
    'channasandra', 'chikka tirupathi', 'chikkabanavar', 'chikkalasandra',
    'choodasandra', 'cooke town', 'cox town', 'cunningham road', 'dasanapura',
    'dasarahalli', 'devanahalli', 'devarachikkanahalli', 'dodda nekkundi',
    'doddaballapur', 'doddakallasandra', 'doddathoguru', 'domlur', 'dommasandra',
    'epip zone', 'electronic city', 'electronic city phase ii',
    'electronics city phase 1', 'frazer town', 'gm palaya', 'garudachar palya',
    'giri nagar', 'gollarapalya hosahalli', 'gottigere', 'green glen layout',
    'gubbalala', 'gunjur', 'hal 2nd stage', 'hbr layout', 'hrbr layout',
    'hsr layout', 'haralur road', 'harlur', 'hebbal', 'hebbal kempapura',
    'hegde nagar', 'hennur', 'hennur road', 'hoodi', 'horamavu agara',
    'horamavu banaswadi', 'hormavu', 'hosa road', 'hosakerehalli', 'hoskote',
    'hosur road', 'hulimavu', 'isro layout', 'itpl', 'iblur village', 'indira nagar',
    'jp nagar', 'jakkur', 'jalahalli', 'jalahalli east', 'jigani', 'judicial layout',
    'kr puram', 'kadubeesanahalli', 'kadugodi', 'kaggadasapura', 'kaggalipura',
    'kaikondrahalli', 'kalena agrahara', 'kalyan nagar', 'kambipura', 'kammanahalli',
    'kammasandra', 'kanakapura', 'kanakpura road', 'kannamangala', 'karuna nagar',
    'kasavanhalli', 'kasturi nagar', 'kathriguppe', 'kaval byrasandra',
    'kenchenahalli', 'kengeri', 'kengeri satellite town', 'kereguddadahalli',
    'kodichikkanahalli', 'kodigehaali', 'kodigehalli', 'kodihalli', 'kogilu',
    'konanakunte', 'koramangala', 'kothannur', 'kothanur', 'kudlu', 'kudlu gate',
    'kumaraswami layout', 'kundalahalli', 'lb shastri nagar', 'laggere',
    'lakshminarayana pura', 'lingadheeranahalli', 'magadi road', 'mahadevpura',
    'mahalakshmi layout', 'mallasandra', 'malleshpalya', 'malleshwaram',
    'marathahalli', 'margondanahalli', 'marsur', 'mico layout', 'munnekollal',
    'murugeshpalya', 'mysore road', 'ngr layout', 'nri layout', 'nagarbhavi',
    'nagasandra', 'nagavara', 'nagavarapalya', 'narayanapura', 'neeladri nagar',
    'nehru nagar', 'ombr layout', 'old airport road', 'old madras road',
    'padmanabhanagar', 'pai layout', 'panathur', 'parappana agrahara',
    'pattandur agrahara', 'poorna pragna layout', 'prithvi layout', 'r.t. nagar',
    'rachenahalli', 'raja rajeshwari nagar', 'rajaji nagar', 'rajiv nagar',
    'ramagondanahalli', 'ramamurthy nagar', 'rayasandra', 'sahakara nagar',
    'sanjay nagar', 'sarakki nagar', 'sarjapur', 'sarjapur  road',
    'sarjapura - attibele road', 'sector 2 hsr layout', 'sector 7 hsr layout',
    'seegehalli', 'shampura', 'shivaji nagar', 'singasandra', 'somasundara palya',
    'sompura', 'sonnenahalli', 'subramanyapura', 'sultan palaya', 'tc palaya',
    'talaghattapura', 'thanisandra', 'thigalarapalya', 'thubarahalli',
    'thyagaraja nagar', 'tindlu', 'tumkur road', 'ulsoor', 'uttarahalli', 'varthur',
    'varthur road', 'vasanthapura', 'vidyaranyapura', 'vijayanagar',
    'vishveshwarya layout', 'vishwapriya layout', 'vittasandra', 'whitefield',
    'yelachenahalli', 'yelahanka', 'yelahanka new town', 'yelenahalli', 'yeshwanthpur',
]

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #050A18 0%, #0c1632 60%, #0a0f22 100%);
    min-height: 100vh;
}

/* Header */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 48px; font-weight: 800;
    line-height: 1.1; letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #4F8EF7 50%, #A78BFA 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; text-align: center; margin-bottom: 6px;
}
.hero-sub {
    text-align: center; color: rgba(168,197,255,0.6);
    font-size: 15px; margin-bottom: 8px;
}
.eyebrow { text-align: center; margin-bottom: 14px; }
.eyebrow span {
    display: inline-block; font-size: 11px; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase; color: #34D399;
    background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.25);
    border-radius: 100px; padding: 5px 16px;
}

/* Stats strip */
.info-strip {
    display: flex; gap: 12px; flex-wrap: wrap;
    justify-content: center; margin-bottom: 28px;
}
.info-chip {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 10px 22px; text-align: center;
    color: rgba(168,197,255,0.6); font-size: 13px;
}
.info-chip b { display: block; color: #E8F0FE; font-size: 20px; font-weight: 700; margin-bottom: 2px; }

/* Labels */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    color: rgba(167,139,250,0.9) !important;
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
}

/* Number input wrapper */
div[data-testid="stNumberInput"] > div {
    background: #1a2744 !important;
    border: 1px solid rgba(99,179,237,0.35) !important;
    border-radius: 12px !important;
    overflow: hidden;
}
div[data-testid="stNumberInput"] input {
    background: #1a2744 !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 16px !important; font-weight: 600 !important;
    border: none !important; box-shadow: none !important;
    caret-color: #4F8EF7 !important;
}
div[data-testid="stNumberInput"] input:focus {
    background: #1a2744 !important;
    color: #ffffff !important;
    border: none !important; box-shadow: none !important;
}
div[data-testid="stNumberInput"] > div:focus-within {
    border-color: #4F8EF7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.28) !important;
}
div[data-testid="stNumberInput"] button {
    background: #243058 !important;
    color: #7eb8ff !important;
    border: none !important;
    border-left: 1px solid rgba(99,179,237,0.2) !important;
}
div[data-testid="stNumberInput"] button:hover {
    background: #2e3f6e !important; color: #ffffff !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    background: #1a2744 !important;
    border: 1px solid rgba(99,179,237,0.35) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important; font-weight: 500 !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #4F8EF7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.28) !important;
}
div[data-testid="stSelectbox"] svg { fill: #7eb8ff !important; }
div[data-testid="stSelectbox"] ul {
    background: #1a2744 !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    border-radius: 12px !important;
}
div[data-testid="stSelectbox"] li { color: #c8daff !important; font-size: 14px !important; }
div[data-testid="stSelectbox"] li:hover,
div[data-testid="stSelectbox"] li[aria-selected="true"] {
    background: rgba(79,142,247,0.2) !important; color: #ffffff !important;
}

/* Predict button */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #4F8EF7, #A78BFA) !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important; padding: 14px 24px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 17px !important; font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 8px 32px rgba(79,142,247,0.38) !important;
    margin-top: 6px;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 40px rgba(79,142,247,0.52) !important;
}

/* Result box */
.result-box {
    background: linear-gradient(135deg, rgba(79,142,247,0.10), rgba(167,139,250,0.10));
    border: 1px solid rgba(79,142,247,0.3); border-radius: 20px;
    padding: 28px 32px; position: relative; overflow: hidden; margin-top: 10px;
}
.result-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(79,142,247,0.7), transparent);
}
.result-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #4F8EF7; margin-bottom: 6px;
}
.result-price {
    font-family: 'Syne', sans-serif; font-size: 54px; font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 20%, #4F8EF7 80%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}
.result-unit { font-size: 13px; color: rgba(168,197,255,0.5); margin-top: 4px; margin-bottom: 18px; }
.pills-row { display: flex; flex-wrap: wrap; gap: 8px; }
.pill {
    font-size: 12px; padding: 5px 13px; border-radius: 100px;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    color: rgba(168,197,255,0.7);
}
.pill b { color: #fff; font-weight: 600; }

/* Error / connection */
.err-box {
    background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px; padding: 14px 18px; color: #FCA5A5;
    font-size: 13px; margin-top: 10px; line-height: 1.6;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="eyebrow"><span>✦ AI-Powered Real Estate</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Bangalore House<br>Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Predict property prices across 241+ locations instantly.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
  <div class="info-chip"><b>241+</b>Locations</div>
  <div class="info-chip"><b>ML</b>Powered</div>
  <div class="info-chip"><b>Live</b>Estimates</div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    total_sqft = st.number_input("📐  Total Square Feet", min_value=300.0, value=1000.0)

with col2:
    location = st.selectbox("📍  Location", options=LOCATIONS, index=LOCATIONS.index("1st phase jp nagar"))

col3, col4 = st.columns(2)

with col3:
    bhk = st.number_input("🛏  BHK", min_value=1, max_value=10, value=2)

with col4:
    bath = st.number_input("🚿  Bathrooms", min_value=1, max_value=10, value=2)

# ── Predict button — SAME LOGIC AS ORIGINAL ───────────────────
if st.button("✦  Predict Price"):
    url = "https://bengaluru-house-price-prediction-775j.onrender.com/predict"

    payload = {
        "total_sqft": float(total_sqft),
        "bath":       float(bath),
        "bhk":        float(bhk),
        "location":   location,
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.markdown(f"""
            <div class="result-box">
                <div class="result-label">── Estimated Price</div>
                <div class="result-price">₹ {result} L</div>
                <div class="result-unit">Indian Rupees — Lakhs (INR)</div>
                <div class="pills-row">
                    <div class="pill">📐 <b>{int(total_sqft):,}</b> sq ft</div>
                    <div class="pill">🛏 <b>{int(bhk)}</b> BHK</div>
                    <div class="pill">🚿 <b>{int(bath)}</b> Bath</div>
                    <div class="pill">📍 <b>{location.title()}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="err-box">⚠ Server error: {response.text}</div>', unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.markdown(
            '<div class="err-box">🔌 Backend server nahi chal raha!<br>Pehle <b>uvicorn</b> start karo: <code>uvicorn Backend.app.main:app --reload</code></div>',
            unsafe_allow_html=True,
        )
