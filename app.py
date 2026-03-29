import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Observatoire Chlordécone",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS — STYLE CARTOGRAPHIQUE & SCIENTIFIQUE
# Palette : fond ardoise profonde, accents
# ambre chaud + vert tropical + rouge alerte
# Typo : Syne (titres) + IBM Plex Mono (data)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Lato:wght@300;400&display=swap');

:root {
    --bg-deep:       #0e1520;
    --bg-surface:    #14202e;
    --bg-card:       #1a2a3a;
    --bg-card-hover: #1f3347;
    --border:        rgba(100,160,220,0.12);
    --border-light:  rgba(100,160,220,0.22);

    --col-sain:      #27ae60;
    --col-modere:    #e8a020;
    --col-critique:  #c0392b;
    --col-anomalie:  #566573;
    --col-accent:    #3d8fbf;
    --col-amber:     #f0a500;

    --text-primary:  #dde8f0;
    --text-muted:    #6d8fa8;
    --text-dim:      #3d5a72;

    --font-title: 'Syne', sans-serif;
    --font-mono:  'IBM Plex Mono', monospace;
    --font-body:  'Lato', sans-serif;

    --radius-card: 14px;
    --shadow-card: 0 4px 24px rgba(0,0,0,0.4);
}

/* ── Reset & base ── */
html, body, [class*="css"], .main, .block-container {
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}
.block-container { padding: 1.2rem 2rem 2rem !important; max-width: 1600px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border-light) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
section[data-testid="stSidebar"] label { font-family: var(--font-mono) !important; font-size: 0.72rem !important; letter-spacing: 0.06em; color: var(--text-muted) !important; }
.stSlider [data-baseweb="slider"] { accent-color: var(--col-accent); }

/* ── HERO ── */
.hero {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    background: linear-gradient(110deg, #0a1929 0%, #112240 55%, #0e2035 100%);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-card);
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 85% 30%, rgba(61,143,191,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 10% 80%, rgba(39,174,96,0.10) 0%, transparent 50%);
    pointer-events: none;
}
.hero-left { position: relative; z-index: 1; }
.hero-tag {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--col-accent);
    border: 1px solid rgba(61,143,191,0.35);
    border-radius: 4px;
    padding: 0.2rem 0.7rem;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-family: var(--font-title);
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    color: var(--text-primary);
    margin: 0 0 0.55rem;
}
.hero-title span { color: var(--col-accent); }
.hero-subtitle {
    font-family: var(--font-body);
    font-size: 0.9rem;
    font-weight: 300;
    color: var(--text-muted);
    max-width: 560px;
    line-height: 1.6;
}
.hero-right { position: relative; z-index: 1; text-align: right; }
.hero-island-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    color: var(--text-dim);
    text-transform: uppercase;
}
.hero-island-name {
    font-family: var(--font-title);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--col-amber);
    letter-spacing: 0.04em;
}

/* ── Section label ── */
.sec-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.9rem;
}
.sec-label::before {
    content: "";
    display: inline-block;
    width: 20px; height: 1px;
    background: var(--col-accent);
}
.sec-label::after {
    content: "";
    flex: 1; height: 1px;
    background: var(--border);
}

/* ── KPI grid ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
    margin-bottom: 1.4rem;
}
.kpi {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: 2.5px solid var(--kpi-color, var(--col-accent));
    border-radius: var(--radius-card);
    padding: 1.2rem 1.4rem 1rem;
    position: relative;
    transition: border-color 0.2s, background 0.2s;
    box-shadow: var(--shadow-card);
}
.kpi:hover { background: var(--bg-card-hover); }
.kpi-icon {
    position: absolute;
    top: 1rem; right: 1rem;
    font-size: 1.1rem;
    opacity: 0.4;
}
.kpi-label {
    font-family: var(--font-mono);
    font-size: 0.63rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.55rem;
}
.kpi-value {
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.25rem;
}
.kpi-value sup {
    font-size: 0.9rem;
    font-weight: 400;
    color: var(--text-muted);
    margin-left: 2px;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--text-dim);
}
.kpi-bar-bg {
    height: 3px;
    background: rgba(255,255,255,0.05);
    border-radius: 2px;
    margin-top: 0.75rem;
    overflow: hidden;
}
.kpi-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: var(--kpi-color, var(--col-accent));
    transition: width 0.6s ease;
}

/* ── Panels ── */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 1.3rem 1.5rem;
    box-shadow: var(--shadow-card);
    height: 100%;
}
.panel-title {
    font-family: var(--font-title);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}
.panel-desc {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-bottom: 0.9rem;
    line-height: 1.5;
}

/* ── Legend pills ── */
.legend-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.75rem;
}
.pill {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
}
.pill-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── Download button ── */
.stDownloadButton button {
    font-family: var(--font-mono) !important;
    font-size: 0.74rem !important;
    background: transparent !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    letter-spacing: 0.05em;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton button:hover {
    background: var(--col-accent) !important;
    border-color: var(--col-accent) !important;
    color: white !important;
}

/* ── Divider ── */
.div-line { height: 1px; background: var(--border); margin: 1.6rem 0; }

/* ── Status badge ── */
.status-row {
    display: flex;
    gap: 1.2rem;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-dim);
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--col-sain);
    display: inline-block;
    margin-right: 4px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Hide Streamlit UI ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Metric overrides ── */
[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('chlordecone_clustered.csv')

    noms_clusters = {
        0: "Zone Saine",
        1: "Zone Modérée",
        2: "Zone Critique",
        3: "Anomalie"
    }
    df['Profil'] = df['cluster'].map(noms_clusters)

    # ── Détection automatique de l'île ──────────────────────────────
    # On essaie d'abord des colonnes latitude/longitude standards
    lat_col = next((c for c in df.columns if c.lower() in ['lat','latitude','lat_wgs84','y_wgs84']), None)
    lon_col = next((c for c in df.columns if c.lower() in ['lon','longitude','lng','lon_wgs84','x_wgs84']), None)

    if lat_col and lon_col:
        df['LAT'] = pd.to_numeric(df[lat_col], errors='coerce')
        df['LON'] = pd.to_numeric(df[lon_col], errors='coerce')
    else:
        # Les colonnes X/Y sont probablement en Lambert / projection locale.
        # On détecte l'île selon la plage de valeurs de X pour choisir
        # les bons paramètres de reprojection approximative.
        x_mean = df['X'].mean()
        y_mean = df['Y'].mean()

        # Si X > 500000 → coordonnées métriques (Lambert ou UTM)
        if x_mean > 500:
            # Guadeloupe UTM 20N  ≈  X:[620000-720000]  Y:[1730000-1810000]
            # Martinique UTM 20N  ≈  X:[695000-730000]  Y:[1590000-1640000]
            if y_mean > 1700000:
                # Guadeloupe
                # Centre approx (16.25°N, -61.55°E)
                lat0, lon0 = 16.25, -61.55
                x0, y0 = 663000, 1797000
            else:
                # Martinique
                # Centre approx (14.67°N, -61.02°E)
                lat0, lon0 = 14.67, -61.02
                x0, y0 = 712000, 1622000

            # Conversion linéaire approximative (1 degré lat ≈ 111320 m)
            df['LAT'] = lat0 + (df['Y'] - y0) / 111320
            df['LON'] = lon0 + (df['X'] - x0) / (111320 * np.cos(np.radians(lat0)))
        else:
            # Déjà en degrés décimaux
            df['LAT'] = df['Y']
            df['LON'] = df['X']

    return df

df = load_data()

# Couleurs
COLORS = {
    "Zone Saine":    "#27ae60",
    "Zone Modérée":  "#e8a020",
    "Zone Critique": "#c0392b",
    "Anomalie":      "#566573"
}

PLOTLY_DARK = dict(
    plot_bgcolor  = "rgba(26,42,58,0)",
    paper_bgcolor = "rgba(26,42,58,0)",
    font          = dict(color="#dde8f0", family="IBM Plex Mono, monospace", size=11),
)
_GRID = dict(gridcolor="rgba(100,160,220,0.08)", zerolinecolor="rgba(100,160,220,0.1)")

def apply_grid(fig):
    """Apply dark grid to all axes of a figure."""
    fig.update_xaxes(**_GRID)
    fig.update_yaxes(**_GRID)
    return fig

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="
        font-family:'Syne',sans-serif;
        font-size:1.05rem;font-weight:700;
        color:#dde8f0;
        border-bottom:1px solid rgba(100,160,220,0.15);
        padding-bottom:0.9rem;margin-bottom:1.2rem;">
        ⚙ Paramètres
    </div>""", unsafe_allow_html=True)

    min_y = int(df['ANNEE'].min())
    max_y = int(df['ANNEE'].max())
    selected_years = st.slider("Période", min_y, max_y, (min_y, max_y))

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    liste_communes = sorted(df['COMMU_LAB'].unique())
    selected_communes = st.multiselect("Communes", liste_communes, default=liste_communes)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    profils_dispo = list(df['Profil'].unique())
    selected_profils = st.multiselect("Profil de territoire", profils_dispo, default=profils_dispo)

    # Fond de carte
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    map_style = st.selectbox("Style de carte", [
        "carto-darkmatter",
        "open-street-map",
        "carto-positron",
        "stamen-terrain"
    ])

    st.markdown("""
    <div style="margin-top:1.5rem;padding:0.8rem;
        background:rgba(61,143,191,0.08);border:1px solid rgba(61,143,191,0.2);
        border-radius:8px;font-family:'IBM Plex Mono',monospace;font-size:0.64rem;
        color:#6d8fa8;line-height:1.7;">
        Données : BDAT / INRAE<br>
        Contamination sols agricoles<br>
        Antilles françaises
    </div>""", unsafe_allow_html=True)

# ==========================================
# FILTRAGE
# ==========================================
df_f = df[
    (df['ANNEE'] >= selected_years[0]) &
    (df['ANNEE'] <= selected_years[1]) &
    (df['COMMU_LAB'].isin(selected_communes)) &
    (df['Profil'].isin(selected_profils))
].copy()

# ==========================================
# HERO
# ==========================================
# Détection île dominante
lat_mean = df_f['LAT'].mean() if not df_f.empty else 14.67
if lat_mean > 15.5:
    ile_name = "Guadeloupe"
elif lat_mean > 14.2:
    ile_name = "Martinique"
else:
    ile_name = "Antilles françaises"

n_total   = len(df_f)
taux_moy  = df_f['Taux_Chlordecone'].mean()  if not df_f.empty else 0
taux_max  = df_f['Taux_Chlordecone'].max()   if not df_f.empty else 0
n_crit    = len(df_f[df_f['Profil'] == "Zone Critique"])
pct_crit  = (n_crit / n_total * 100) if n_total > 0 else 0

st.markdown(f"""
<div class="hero">
  <div class="hero-left">
    <div class="hero-tag">// Outil d'aide à la décision publique</div>
    <div class="hero-title">Observatoire <span>Chlordécone</span></div>
    <div class="hero-subtitle">
      Analyse spatiale de la contamination des sols agricoles — cartographie géographique
      en temps réel sur fond de carte satellitaire.
    </div>
  </div>
  <div class="hero-right">
    <div class="hero-island-label">Territoire analysé</div>
    <div class="hero-island-name">🌴 {ile_name}</div>
    <div style="margin-top:0.6rem;" class="status-row">
      <span><span class="status-dot"></span>Données actives</span>
      <span>{selected_years[0]} – {selected_years[1]}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPIs
# ==========================================
st.markdown('<div class="sec-label">Indicateurs de surveillance</div>', unsafe_allow_html=True)

# Calcul bar fill %
max_possible = 1000  # µg/kg plafond visuel
bar_taux = min(taux_moy / max_possible * 100, 100)
bar_max  = min(taux_max / max_possible * 100, 100)

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi" style="--kpi-color:#3d8fbf;">
    <span class="kpi-icon">📍</span>
    <div class="kpi-label">Parcelles analysées</div>
    <div class="kpi-value">{n_total:,}</div>
    <div class="kpi-sub">unités de mesure actives</div>
    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{min(n_total/max(len(df),1)*100,100):.0f}%"></div></div>
  </div>
  <div class="kpi" style="--kpi-color:#e8a020;">
    <span class="kpi-icon">⚗️</span>
    <div class="kpi-label">Taux moyen chlordécone</div>
    <div class="kpi-value">{taux_moy:.2f}<sup>µg/kg</sup></div>
    <div class="kpi-sub">concentration moyenne des sols</div>
    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{bar_taux:.1f}%;background:#e8a020;"></div></div>
  </div>
  <div class="kpi" style="--kpi-color:#c0392b;">
    <span class="kpi-icon">🚨</span>
    <div class="kpi-label">Zones critiques</div>
    <div class="kpi-value">{pct_crit:.1f}<sup>%</sup></div>
    <div class="kpi-sub">{n_crit:,} parcelles en alerte haute</div>
    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{pct_crit:.1f}%;background:#c0392b;"></div></div>
  </div>
  <div class="kpi" style="--kpi-color:#9b59b6;">
    <span class="kpi-icon">📈</span>
    <div class="kpi-label">Pic de contamination</div>
    <div class="kpi-value">{taux_max:.0f}<sup>µg/kg</sup></div>
    <div class="kpi-sub">valeur maximale relevée</div>
    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{bar_max:.1f}%;background:#9b59b6;"></div></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

# ==========================================
# CARTE GÉOGRAPHIQUE RÉELLE + ÉVOLUTION
# ==========================================
st.markdown('<div class="sec-label">Cartographie géographique des risques</div>', unsafe_allow_html=True)

col_map, col_right = st.columns([1.7, 1], gap="large")

with col_map:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🗺 Carte de contamination — vue satellite</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Chaque point représente une parcelle analysée. Les couleurs indiquent le niveau de risque. Zoom et survol disponibles.</div>', unsafe_allow_html=True)

    # Légende pills
    st.markdown("""
    <div class="legend-pills">
      <div class="pill"><div class="pill-dot" style="background:#27ae60"></div>Zone Saine</div>
      <div class="pill"><div class="pill-dot" style="background:#e8a020"></div>Zone Modérée</div>
      <div class="pill"><div class="pill-dot" style="background:#c0392b"></div>Zone Critique</div>
      <div class="pill"><div class="pill-dot" style="background:#566573"></div>Anomalie</div>
    </div>
    """, unsafe_allow_html=True)

    if not df_f.empty and df_f['LAT'].notna().any():
        # Centre de la carte
        center_lat = df_f['LAT'].median()
        center_lon = df_f['LON'].median()

        # Calcul zoom adaptatif
        lat_range = df_f['LAT'].max() - df_f['LAT'].min()
        lon_range = df_f['LON'].max() - df_f['LON'].min()
        spread = max(lat_range, lon_range)
        if spread < 0.1:   zoom = 12
        elif spread < 0.5: zoom = 10
        elif spread < 1.5: zoom = 9
        else:              zoom = 8

        fig_map = px.scatter_mapbox(
            df_f,
            lat='LAT', lon='LON',
            color='Profil',
            color_discrete_map=COLORS,
            hover_name='COMMU_LAB',
            hover_data={
                'LAT': False, 'LON': False,
                'ANNEE': True,
                'Taux_Chlordecone': ':.2f',
                'histoBanane_Histo_ban': True,
                'Profil': False
            },
            labels={
                'ANNEE': 'Année',
                'Taux_Chlordecone': 'Taux (µg/kg)',
                'histoBanane_Histo_ban': 'Indice bananier'
            },
            opacity=0.75,
            size_max=10,
            zoom=zoom,
            center={"lat": center_lat, "lon": center_lon},
            mapbox_style=map_style,
            height=520
        )
        fig_map.update_traces(marker=dict(size=8))
        fig_map.update_layout(
            paper_bgcolor="rgba(26,42,58,0.0)",
            margin=dict(r=0, t=0, l=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.07,
                xanchor="center", x=0.5,
                title_text='',
                font=dict(size=10, family="IBM Plex Mono"),
                bgcolor="rgba(14,21,32,0.7)",
                bordercolor="rgba(100,160,220,0.2)",
                borderwidth=1
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Aucune coordonnée GPS disponible pour la sélection actuelle.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # ── Évolution temporelle ─────────────────────────
    st.markdown('<div class="panel" style="margin-bottom:0.9rem;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📈 Évolution temporelle</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Taux moyen de chlordécone par année (µg/kg)</div>', unsafe_allow_html=True)

    if not df_f.empty:
        ev = df_f.groupby('ANNEE')['Taux_Chlordecone'].agg(['mean','max','min']).reset_index()
        fig_ev = go.Figure()
        # Zone min-max
        fig_ev.add_trace(go.Scatter(
            x=list(ev['ANNEE']) + list(ev['ANNEE'][::-1]),
            y=list(ev['max']) + list(ev['min'][::-1]),
            fill='toself',
            fillcolor='rgba(61,143,191,0.1)',
            line=dict(color='rgba(0,0,0,0)'),
            hoverinfo='skip', showlegend=False, name='Étendue'
        ))
        # Courbe moyenne
        fig_ev.add_trace(go.Scatter(
            x=ev['ANNEE'], y=ev['mean'],
            mode='lines+markers',
            line=dict(color='#3d8fbf', width=2.5),
            marker=dict(size=7, color='#3d8fbf',
                        line=dict(color='#dde8f0', width=1.5)),
            fill='tozeroy', fillcolor='rgba(61,143,191,0.06)',
            name='Taux moyen',
            hovertemplate='<b>%{x}</b><br>%{y:.2f} µg/kg<extra></extra>'
        ))
        fig_ev.update_layout(
            **PLOTLY_DARK,
            height=215,
            margin=dict(t=5, b=30, l=10, r=10),
            showlegend=False,
        )
        fig_ev.update_xaxes(title='', tickfont=dict(size=10), **_GRID)
        fig_ev.update_yaxes(title='µg/kg', tickfont=dict(size=10), **_GRID)
        apply_grid(fig_ev)
        st.plotly_chart(fig_ev, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Répartition par profil (donut) ──────────────
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🥧 Répartition des profils</div>', unsafe_allow_html=True)

    if not df_f.empty:
        dist = df_f['Profil'].value_counts().reset_index()
        dist.columns = ['Profil', 'N']
        fig_pie = go.Figure(go.Pie(
            labels=dist['Profil'], values=dist['N'],
            marker_colors=[COLORS.get(p, '#aaa') for p in dist['Profil']],
            hole=0.58,
            textfont=dict(size=10, family="IBM Plex Mono"),
            hovertemplate='<b>%{label}</b><br>%{value:,} parcelles<br>%{percent}<extra></extra>',
            insidetextorientation='radial'
        ))
        fig_pie.update_layout(
            **PLOTLY_DARK,
            height=210,
            margin=dict(t=5, b=5, l=10, r=10),
            showlegend=False,
            annotations=[dict(
                text=f"<b>{n_total:,}</b><br><span style='font-size:9px'>parcelles</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color='#dde8f0', family='IBM Plex Mono')
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

# ==========================================
# ANALYSES AGRONOMIQUES
# ==========================================
st.markdown('<div class="sec-label">Analyses agronomiques</div>', unsafe_allow_html=True)
col_sol, col_ban = st.columns(2, gap="large")

with col_sol:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🪨 Chlordécone par type de sol</div>', unsafe_allow_html=True)
    if not df_f.empty and 'type_sol' in df_f.columns:
        sol = (df_f.groupby('type_sol')['Taux_Chlordecone']
               .mean().reset_index()
               .sort_values('Taux_Chlordecone', ascending=True))
        fig_sol = go.Figure(go.Bar(
            x=sol['Taux_Chlordecone'], y=sol['type_sol'],
            orientation='h',
            marker=dict(
                color=sol['Taux_Chlordecone'],
                colorscale=[[0,'#1a4d2e'],[0.45,'#e8a020'],[1,'#c0392b']],
                showscale=False,
                line=dict(width=0)
            ),
            hovertemplate='<b>%{y}</b><br>%{x:.2f} µg/kg<extra></extra>'
        ))
        fig_sol.update_layout(
            **PLOTLY_DARK,
            height=260,
            margin=dict(t=5, b=5, l=5, r=20),
        )
        fig_sol.update_xaxes(title='Taux moyen (µg/kg)', tickfont=dict(size=10), **_GRID)
        fig_sol.update_yaxes(title='', tickfont=dict(size=10), **_GRID)
        apply_grid(fig_sol)
        st.plotly_chart(fig_sol, use_container_width=True)
    else:
        st.info("Données de type de sol non disponibles.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_ban:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🍌 Pression historique bananière</div>', unsafe_allow_html=True)
    if not df_f.empty:
        fig_ban = go.Figure()
        for profil, col_hex in COLORS.items():
            sub = df_f[df_f['Profil'] == profil]
            if not sub.empty:
                r = int(col_hex[1:3], 16)
                g = int(col_hex[3:5], 16)
                b = int(col_hex[5:7], 16)
                fig_ban.add_trace(go.Violin(
                    y=sub['histoBanane_Histo_ban'],
                    name=profil,
                    line_color=col_hex,
                    fillcolor=f'rgba({r},{g},{b},0.18)',
                    box_visible=True,
                    meanline_visible=True,
                    points=False,
                    hoverinfo='y+name'
                ))
        fig_ban.update_layout(
            **PLOTLY_DARK,
            height=260,
            margin=dict(t=5, b=5, l=5, r=5),
            showlegend=False,
            violingap=0.25,
        )
        fig_ban.update_xaxes(showticklabels=False, **_GRID)
        fig_ban.update_yaxes(title='Indice historique banane', tickfont=dict(size=10), **_GRID)
        apply_grid(fig_ban)
        st.plotly_chart(fig_ban, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# EXPORT
# ==========================================
st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

if not df_f.empty and df_f['LAT'].notna().any():
    html_str = fig_map.to_html(full_html=True, include_plotlyjs='cdn')
    col_dl, col_meta = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "↓ Télécharger la carte (HTML)",
            data=html_str,
            file_name="carte_chlordecone_geo.html",
            mime="text/html"
        )
    with col_meta:
        st.markdown(
            f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:0.68rem;color:#3d5a72;">'
            f'{n_total:,} parcelles · {ile_name} · {selected_years[0]}–{selected_years[1]}'
            f'</span>',
            unsafe_allow_html=True
        )