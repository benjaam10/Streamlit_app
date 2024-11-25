import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Título del dashboard
st.title("Crypto Dashboard - Resumen de Estadísticas")

# URL de la API de CoinMarketCap (API Key y URL pueden necesitar ajustes)
api_key = "759cb517-f5df-4e50-bd15-fa789e6653c1"
url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={api_key}"

# Realizamos la solicitud a la API
response = requests.get(url)
datos = json.loads(response.text)

# Verificamos que la respuesta contiene datos correctos
if "data" in datos:
    plt.style.use('dark_background')
    # Extraemos nombres, valores y símbolos de las criptomonedas
    nombre_cripto = [item["name"] for item in datos["data"]]
    simbolo = [item["symbol"] for item in datos["data"]]

    # Mostrar un selectbox para seleccionar una criptomoneda
    st.subheader("Seleccione una criptomoneda para ver detalles")
    seleccion = st.selectbox("Seleccione una criptomoneda", nombre_cripto)
    # Extraemos datos de una criptomoneda específica
    cripto_data = [item for item in datos["data"] if item["name"] == seleccion][0]

    precio_actual = cripto_data["quote"]["USD"]["price"]
    cambio_24h = cripto_data["quote"]["USD"]["percent_change_24h"]
    
    url_esp = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?CMC_PRO_API_KEY={api_key}&symbol={cripto_data['symbol']}"
    response_esp = requests.get(url_esp)
    datos_esp = json.loads(response_esp.text)
    if "data" in datos_esp:
        cripto_data_esp = datos_esp["data"][simbolo[nombre_cripto.index(seleccion)]]
        imagen = cripto_data_esp["logo"]
        ranking = cripto_data["cmc_rank"]
        volumen24h = cripto_data["quote"]["USD"]["volume_24h"]
        web = cripto_data_esp["urls"]["website"]
        descripcion = cripto_data_esp["description"]
    # Mostrar métricas en la parte superior
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown(f"""<img src="{imagen}" alt="Logo" style="width:100px;height:100px;">""", unsafe_allow_html=True)
    col2.metric("Criptomoneda Seleccionada", seleccion)
    col3.metric("Precio Actual (USD)", f"${precio_actual:,.3f}", f"{cambio_24h:.2f}% en 24h")
    col4.metric("Rango", ranking) #cmc_rank
    col5.metric("Volumen en 24h", f"${volumen24h:,.2f}") # volume_24h
    # Mostrar la descripción de la criptomoneda
    st.write(descripcion)
    st.write("")
    st.write("")

    # Guardar los datos en un DataFrame y exportarlo a CSV
    data_conjunto = pd.DataFrame({
        "Nombre": nombre_cripto,
        "Simbolo": simbolo,
        "Precio (USD)": [item["quote"]["USD"]["price"] for item in datos["data"]],
        "Cambio 24h (%)": [item["quote"]["USD"]["percent_change_24h"] for item in datos["data"]],
        "Rango": [item["cmc_rank"] for item in datos["data"]],
        "Volumen 24h": [item["quote"]["USD"]["volume_24h"] for item in datos["data"]]
    })
    # Centrar el botón de descarga
    col1, col2, col3 = st.columns(3)
    with col2:
        st.download_button(
            label="📥 Descargar datos en CSV de las 100 criptomonedas",
            data=data_conjunto.to_csv(index=False),
            file_name="cripto_data.csv",
            mime="text/csv"
        )
    st.write("")
    st.write("")
    # Datos estadísticos de las 10 criptomonedas que más cuestan: promedio, desviación estándar, moda, máximo y mínimo
    top_10_cripto = data_conjunto.sort_values(by="Precio (USD)", ascending=False).iloc[1:11]
    # Mostrar en una tabla de 2 filas x 5 columnas los datos estadísticos
    st.subheader("Estadísticas de las 10 criptomonedas más valiosas:")
    colu_1, colu_2, colu_3, colu_4, colu_5 = st.columns(5)
    colu_1.metric("Promedio de precios", f"${top_10_cripto['Precio (USD)'].mean():,.2f}")
    colu_2.metric("Desviación estándar", f"${top_10_cripto['Precio (USD)'].std():,.2f}")
    colu_3.metric("Moda de precios", f"${top_10_cripto['Precio (USD)'].mode()[0]:,.2f}")
    colu_4.metric("Precio máximo", f"${top_10_cripto['Precio (USD)'].max():,.2f}")
    colu_5.metric("Precio mínimo", f"${top_10_cripto['Precio (USD)'].min():,.2f}")
    #st.write(top_10_cripto)
    st.write("")
    st.write("")
    st.subheader("Gráficos estadísticos")	

    # Gráfico de barras con los precios de las 10 criptomonedas más valiosas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top_10_cripto["Nombre"], top_10_cripto["Precio (USD)"], color='cyan')
    ax.set_xlabel('Criptomoneda')
    ax.set_ylabel('Precio (USD)')
    ax.set_title('Precios de las 10 criptomonedas más valiosas (Sin BTC)')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # 2 graficos de lineas agrupados en la misma ventana sobre los precios de las 10 criptomonedas más valiosas y cambio 24h de estas mismas criptos
    fig, ax = plt.subplots(1, 2, figsize=(24, 6))
    ax[0].plot(top_10_cripto["Nombre"], top_10_cripto["Precio (USD)"], marker='o', color='b', label="Precio (USD)")
    ax[0].set_ylabel('Precio (USD)')
    ax[0].set_title('Precios de las 10 criptomonedas más valiosas (Sin BTC)')
    ax[0].grid(True)
    ax[0].legend()
    plt.xticks(rotation=45)
    ax[1].plot(top_10_cripto["Nombre"], top_10_cripto["Cambio 24h (%)"], marker='o', color='r', label="Cambio 24h (%)")
    ax[1].set_ylabel('Cambio 24h (%)')
    ax[1].set_title('Cambio 24h de las 10 criptomonedas más valiosas (Sin BTC)')
    ax[1].grid(True)
    ax[1].legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Grafico de torta con el cambio 24h de las 10 criptomonedas más valiosas
    # Verifica si hay algun valor negativo, si lo hay, le añade "(negativo)" al lado del nombre de la criptomoneda
    

    # Suponiendo que top_10_cripto es el DataFrame con los datos de las criptomonedas
    etiquetas = top_10_cripto["Nombre"]

    # Añadir la etiqueta "(negativo)" a las criptomonedas con cambio negativo
    etiquetas[top_10_cripto["Cambio 24h (%)"] < 0] += " (negativo)"

    # Crear el gráfico de torta de color morado sin px
    fig_torta = plt.figure(figsize=(12, 6))
    plt.pie(top_10_cripto["Cambio 24h (%)"].abs(), labels=etiquetas, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title('Cambio 24h de las 10 criptomonedas más valiosas (Sin BTC)')
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(fig_torta)


    # Grafico de dispersion con el precio vs cambio 24h de las 10 criptomonedas más valiosas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(top_10_cripto["Precio (USD)"], top_10_cripto["Cambio 24h (%)"], color='g')
    ax.set_xlabel('Precio (USD)')
    ax.set_ylabel('Cambio 24h (%)')
    ax.set_title('Precio vs Cambio 24h de las 10 criptomonedas más valiosas (Sin BTC)')
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

    # Gráfico de líneas con los precios de las 10 criptomonedas sin usar px
    fig_linea = plt.figure(figsize=(12, 6))
    plt.plot(top_10_cripto["Nombre"], top_10_cripto["Precio (USD)"], marker='o', color='b', label="Precio (USD)")
    plt.xlabel('Criptomoneda')
    plt.ylabel('Precio (USD)')
    plt.title('Precios de las 10 criptomonedas más valiosas (Sin BTC)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig_linea)

else:
    st.error("No se pudieron obtener los datos de la API.")
