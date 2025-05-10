import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle as pk

# Load the model
model = pk.load(open('model.pkl', 'rb'))

# Load the dataset
cars_data = pd.read_csv('Cardetails.csv')

# Function to extract the car brand
def get_brand_name(car_name):
    return car_name.split(' ')[0].strip()

cars_data['name'] = cars_data['name'].apply(get_brand_name)

# Function to run the model and display prediction
def run_model():
    try:
        # Model ve sütun isimlerini yükle
        model_columns = pk.load(open('model_columns.pkl', 'rb'))

        # Get values from the widgets
        name = brand_var.get()
        year = int(year_var.get())
        km_driven = int(km_var.get())
        fuel = fuel_var.get()
        seller_type = seller_var.get()
        transmission = transmission_var.get()
        owner = owner_var.get()
        mileage = float(mileage_var.get())
        engine = int(engine_var.get())
        max_power = float(power_var.get())
        seats = int(seats_var.get())

        # Create a DataFrame to match the input format
        input_data = pd.DataFrame([[name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]], 
                                  columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats'])

        # One-hot encoding uygula
        input_data = pd.get_dummies(input_data)

        # Eksik olan sütunları bul
        missing_cols = [col for col in model_columns if col not in input_data.columns]
        # Eksik sütunları içeren bir DataFrame oluştur
        missing_df = pd.DataFrame(0, index=input_data.index, columns=missing_cols)
        # input_data ile missing_df'yi birleştir
        input_data = pd.concat([input_data, missing_df], axis=1)
        # Sütun sırasını ayarla ve kopyasını al
        input_data = input_data[model_columns].copy()

        # Get the price prediction
        car_price = model.predict(input_data)

        # Display the result
        result_label.config(text=f"Predicted Car Price: {car_price[0]:.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Car Price Prediction")

# Define variables for the widgets
brand_var = tk.StringVar(value=cars_data['name'].unique()[0])
year_var = tk.IntVar(value=2020)
km_var = tk.IntVar(value=50000)
fuel_var = tk.StringVar(value=cars_data['fuel'].unique()[0])
seller_var = tk.StringVar(value=cars_data['seller_type'].unique()[0])
transmission_var = tk.StringVar(value=cars_data['transmission'].unique()[0])
owner_var = tk.StringVar(value=cars_data['owner'].unique()[0])
mileage_var = tk.DoubleVar(value=15.0)
engine_var = tk.IntVar(value=1500)
power_var = tk.DoubleVar(value=100.0)
seats_var = tk.IntVar(value=5)

# Create and place widgets for each input
ttk.Label(root, text="Select Car Brand").grid(row=0, column=0, padx=10, pady=5)
ttk.OptionMenu(root, brand_var, *cars_data['name'].unique()).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Car Manufactured Year").grid(row=1, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=1994, to=2024, textvariable=year_var).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="No of kms Driven").grid(row=2, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=11, to=200000, textvariable=km_var).grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Fuel type").grid(row=3, column=0, padx=10, pady=5)
ttk.OptionMenu(root, fuel_var, *cars_data['fuel'].unique()).grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Seller type").grid(row=4, column=0, padx=10, pady=5)
ttk.OptionMenu(root, seller_var, *cars_data['seller_type'].unique()).grid(row=4, column=1, padx=10, pady=5)

ttk.Label(root, text="Transmission type").grid(row=5, column=0, padx=10, pady=5)
ttk.OptionMenu(root, transmission_var, *cars_data['transmission'].unique()).grid(row=5, column=1, padx=10, pady=5)

ttk.Label(root, text="Owner").grid(row=6, column=0, padx=10, pady=5)
ttk.OptionMenu(root, owner_var, *cars_data['owner'].unique()).grid(row=6, column=1, padx=10, pady=5)

ttk.Label(root, text="Car Mileage").grid(row=7, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=10, to=40, textvariable=mileage_var).grid(row=7, column=1, padx=10, pady=5)

ttk.Label(root, text="Engine CC").grid(row=8, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=700, to=5000, textvariable=engine_var).grid(row=8, column=1, padx=10, pady=5)

ttk.Label(root, text="Max Power").grid(row=9, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=0, to=200, textvariable=power_var).grid(row=9, column=1, padx=10, pady=5)

ttk.Label(root, text="No of Seats").grid(row=10, column=0, padx=10, pady=5)
ttk.Spinbox(root, from_=2, to=10, textvariable=seats_var).grid(row=10, column=1, padx=10, pady=5)

# Button to predict the price
ttk.Button(root, text="Predict", command=run_model).grid(row=11, column=0, columnspan=2, padx=10, pady=20)

# Label to show the result
result_label = ttk.Label(root, text="")
result_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Start the tkinter main loop
root.mainloop()
