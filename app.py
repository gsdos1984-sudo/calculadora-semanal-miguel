import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

DIAS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

def calcular_df(pago_hora: float, horas_list: list[float]) -> pd.DataFrame:
    pagos = []
    for h in horas_list:
        h = float(h) if h is not None else 0.0
        if h <= 8:
            pago = h * pago_hora
        else:
            pago = (8 * pago_hora) + ((h - 8) * pago_hora * 1.5)
        pagos.append(pago)
    return pd.DataFrame({"Día": DIAS, "Horas": horas_list, "Pago ($)": pagos})

st.set_page_config(page_title="Calculadora semanal | Miguel", layout="wide")
st.title("🐍 Calculadora semanal de horas y pago")
st.caption("Streamlit + pandas + matplotlib")

with st.sidebar:
    st.header("Parámetros")
    pago_hora = st.number_input("Pago por hora ($)", min_value=0.0, value=20.0, step=0.5)
    st.markdown("**Horas por día**")
    horas_inputs = [st.number_input(d, min_value=0.0, value=0.0, step=0.5, key=f"h_{i}") for i, d in enumerate(DIAS)]
    st.info("Las horas > 8 se pagan a 1.5x por día")

df = calcular_df(pago_hora, horas_inputs)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Resumen semanal")
    st.dataframe(df, use_container_width=True)
with col2:
    st.subheader("Totales")
    st.metric("Total horas", f"{df['Horas'].sum():.2f}")
    st.metric("Pago total ($)", f"${df['Pago ($)'].sum():,.2f}")

st.subheader("Gráficas")
fig1 = plt.figure(figsize=(8, 4))
plt.bar(df["Día"], df["Horas"])
plt.title("Horas por día"); plt.xlabel("Día"); plt.ylabel("Horas"); plt.xticks(rotation=45)
st.pyplot(fig1, use_container_width=True)

fig2 = plt.figure(figsize=(8, 4))
plt.bar(df["Día"], df["Pago ($)"])
plt.title("Pago por día ($)"); plt.xlabel("Día"); plt.ylabel("Pago ($)"); plt.xticks(rotation=45)
st.pyplot(fig2, use_container_width=True)

st.subheader("Descargar resultados")
csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV", data=csv_bytes, file_name="pago_semana.csv", mime="text/csv")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False)
st.download_button("Descargar Excel", data=buffer.getvalue(), file_name="pago_semana.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
