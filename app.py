import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Model ve kolonları yükle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Tüm araç modellerini Cardetails.csv'den çek
car_data = pd.read_csv('Cardetails.csv')
car_names = sorted(car_data['name'].unique())

# Giriş başlığı
st.title("Araç Fiyat Tahmin Uygulaması (Orijinal Model)")

# Kullanıcıdan veri al
name = st.selectbox("Araç Modeli", car_names)
year = st.number_input("Model Yılı", min_value=1990, max_value=datetime.now().year, value=2015)
km_driven = st.number_input("Km (km_driven)", min_value=0, value=50000)
fuel = st.selectbox("Yakıt Tipi", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
seller_type = st.selectbox("Satıcı Tipi", ["Individual", "Dealer", "Trustmark Dealer"])
transmission = st.selectbox("Vites Tipi", ["Manual", "Automatic"])
owner = st.selectbox("Sahiplik", [
    "First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"
])
mileage = st.number_input("Ortalama Yakıt (kmpl)", min_value=0.0, value=20.0)
engine = st.number_input("Motor Hacmi (cc)", min_value=500.0, value=1200.0)
max_power = st.number_input("Maksimum Güç (bhp)", min_value=20.0, value=80.0)
seats = st.number_input("Koltuk Sayısı", min_value=2, max_value=10, value=5)

# DataFrame oluştur
input_dict = {
    'name': name,
    'year': year,
    'km_driven': km_driven,
    'fuel': fuel,
    'seller_type': seller_type,
    'transmission': transmission,
    'owner': owner,
    'mileage': mileage,
    'engine': engine,
    'max_power': max_power,
    'seats': seats
}
input_df = pd.DataFrame([input_dict])

# Kategorik değişkenleri one-hot encode et
categorical_cols = ['name', 'fuel', 'seller_type', 'transmission', 'owner']
input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

# Modelin beklediği tüm kolonları ekle (eksik olanları 0 ile doldur)
with open('model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)
missing_cols = [col for col in model_columns if col not in input_df.columns]
missing_df = pd.DataFrame(0, index=input_df.index, columns=missing_cols)
input_df = pd.concat([input_df, missing_df], axis=1)
input_df = input_df[model_columns]
input_df = input_df.copy()  # Fragmentation'ı önler

if st.button("Tahmini Fiyatı Göster"):
    prediction = model.predict(input_df)[0]
    st.success(f"Tahmini Araç Fiyatı: {int(prediction):,} TL")