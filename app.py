import streamlit as st
import joblib

st.title("Prédiction des ventes")

@st.cache_resource
def charger_modele():
    return joblib.load("model_v1.pkl")

model = charger_modele()

# ======================
# STREAMLIT UI (8 variables d'origine)
# ======================
store_nbr = st.number_input("Store", 1, 50)
family = st.number_input("Family (encodé)", 0, 100)
city = st.number_input("City (encodé)", 0, 100)
state = st.number_input("State (encodé)", 0, 100)
onpromotion = st.number_input("Promotion", 0, 1)

year = st.number_input("Year", 2013, 2030)
month = st.number_input("Month", 1, 12)
day = st.number_input("Day", 1, 31)

# ======================
# AJOUT DES 3 VARIABLES MANQUANTES (Exemple à adapter)
# ======================
store_type = st.number_input("Store Type (encodé)", 0, 10)  # Variable manquante 1
cluster = st.number_input("Store Cluster", 1, 25)           # Variable manquante 2
dayofweek = st.number_input("Day of Week (0-6)", 0, 6)      # Variable manquante 3

if st.button("Predict"):
    # REGROUPEMENT DES 11 VARIABLES
    # Attention : l'ordre des variables doit être STRICTEMENT le même que lors de l'entraînement
    X_input = [[
        store_nbr, family, city, state, onpromotion, 
        year, month, day, 
        store_type, cluster, dayofweek  # Les 3 ajouts
    ]]
    
    pred = model.predict(X_input)
    st.success(f"Ventes prévues : {pred[0]:.2f}")
