import streamlit as st
import joblib

# Configuration de la page (Doit être la première commande Streamlit)
st.set_page_config(
    page_title="Prédiction des ventes",
    page_icon="📈",
    layout="centered" # "centered" ou "wide" selon votre préférence
)

st.title("📈 Prédiction des Ventes")
st.markdown("Saisissez les caractéristiques ci-dessous pour estimer le volume des ventes.")
st.write("---")

@st.cache_resource
def charger_modele():
    return joblib.load("model_v1.pkl")

model = charger_modele()

# ======================
# STREAMLIT UI (Design amélioré)
# ======================

# Organisation de la saisie à l'aide d'onglets pour alléger l'interface
tab1, tab2 = st.tabs(["🏬 Informations Magasin & Produit", "📅 Calendrier & Promotions"])

with tab1:
    st.subheader("Détails du Magasin et de l'Article")
    
    col1, col2 = st.columns(2)
    with col1:
        store_nbr = st.number_input("Identifiant Magasin (Store)", min_value=1, max_value=50, value=1)
        store_type = st.number_input("Type de Magasin (Store Type encodé)", min_value=0, max_value=10, value=0)
        cluster = st.number_input("Cluster du Magasin", min_value=1, max_value=25, value=1)
    
    with col2:
        family = st.number_input("Famille de produit (Family encodé)", min_value=0, max_value=100, value=0)
        city = st.number_input("Ville (City encodé)", min_value=0, max_value=100, value=0)
        state = st.number_input("État (State encodé)", min_value=0, max_value=100, value=0)

with tab2:
    st.subheader("Période et Promotion")
    
    col3, col4 = st.columns(2)
    with col3:
        # Utilisation de Sliders ou Selectbox pour une saisie plus ergonomique
        year = st.slider("Année (Year)", min_value=2013, max_value=2030, value=2026)
        month = st.slider("Mois (Month)", min_value=1, max_value=12, value=5)
        day = st.slider("Jour (Day)", min_value=1, max_value=31, value=15)
    
    with col4:
        dayofweek = st.selectbox(
            "Jour de la semaine", 
            options=[0, 1, 2, 3, 4, 5, 6], 
            format_func=lambda x: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][x]
        )
        
        # Un bouton radio horizontal pour l'état de la promotion
        onpromotion = st.radio("L'article est-il en promotion ?", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui", horizontal=True)

st.write("---")

# Zone de prédiction isolée dans un conteneur
design_container = st.container()

with design_container:
    # Bouton centré et mis en valeur (utilisation de type="primary")
    if st.button("🚀 Calculer les prévisions", type="primary", use_container_width=True):
        
        # REGROUPEMENT DES 11 VARIABLES (L'ordre strict est préservé)
        X_input = [[
            store_nbr, family, city, state, onpromotion, 
            year, month, day, 
            store_type, cluster, dayofweek
        ]]
        
        with st.spinner('Calcul des prévisions en cours...'):
            pred = model.predict(X_input)
            
        # Affichage du résultat sous forme de métrique attrayante
        st.markdown("### 📊 Résultat de l'estimation")
        st.metric(label="Volume de ventes prévu", value=f"{pred[0]:,.2f} unités")
