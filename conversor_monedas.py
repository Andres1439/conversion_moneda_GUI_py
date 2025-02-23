import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Configuración
API_KEY = ""
URL = "https://api.exchangeratesapi.io/v1/latest"

# Obtener tasas de cambio
def obtener_tasas():
    try:
        response = requests.get(f"{URL}?access_key={API_KEY}&symbols=USD,AUD,CAD,PLN,MXN&format=1")
        data = response.json()
        if "rates" in data:
            return data["rates"]
        else:
            messagebox.showerror("Error", "No se pudieron obtener las tasas de cambio.")
            return {}
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        return {}


def convertir():
    try:
        monto = float(entry_monto.get())
        moneda_origen = combo_origen.get()
        moneda_destino = combo_destino.get()

        if moneda_origen not in tasas or moneda_destino not in tasas:
            messagebox.showerror("Error", "Selecciona monedas válidas.")
            return

        tasa_conversion = tasas[moneda_destino] / tasas[moneda_origen]
        resultado = monto * tasa_conversion
        label_resultado.config(text=f"{monto} {moneda_origen} = {resultado:.2f} {moneda_destino}")
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {e}")


# Obtener tasas iniciales
tasas = obtener_tasas()
monedas = sorted(tasas.keys()) if tasas else []

# Crear ventana principal
root = tk.Tk()
root.title("Conversor de Monedas 💰")
root.geometry("400x300")

# Widgets
ttk.Label(root, text="Cantidad:").pack(pady=5)
entry_monto = ttk.Entry(root)
entry_monto.pack(pady=5)

ttk.Label(root, text="Convertir de:").pack(pady=5)
combo_origen = ttk.Combobox(root, values=monedas)
combo_origen.pack(pady=5)

ttk.Label(root, text="A:").pack(pady=5)
combo_destino = ttk.Combobox(root, values=monedas)
combo_destino.pack(pady=5)

btn_convertir = ttk.Button(root, text="Convertir", command=convertir)
btn_convertir.pack(pady=10)

label_resultado = ttk.Label(root, text="", font=("Arial", 14))
label_resultado.pack(pady=10)

# Ejecutar aplicación
root.mainloop()
