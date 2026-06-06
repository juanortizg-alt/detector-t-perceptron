import streamlit as st
import numpy as np

st.set_page_config(page_title="Clasificador de T", layout="wide")
st.title("🎛️ Detector Analógico de 'T'")
st.write("Ajusta los pesos de cada píxel y el umbral (threshold) para clasificar los patrones.")

# 1. Definición manual de patrones (Matrices binarias 3x3 aplanadas a 9 elementos)
ejemplos = {
    "T Tradicional (Positivo)":  [1, 1, 1,  0, 1, 0,  0, 1, 0],
    "T Con Base (Positivo)":     [1, 1, 1,  0, 1, 0,  1, 1, 1],
    "Línea Horizontal (Negativo)":[1, 1, 1,  0, 0, 0,  0, 0, 0],
    "Línea Vertical (Negativo)":  [0, 1, 0,  0, 1, 0,  0, 1, 0],
    "Cruz / Más (Negativo)":     [0, 1, 0,  1, 1, 1,  0, 1, 0],
    "Cuadrado Vacío (Negativo)": [1, 1, 1,  1, 0, 1,  1, 1, 1]
}

# 2. Controles de Parámetros (Interfaz de Perillas)
st.header("⚙️ Ajuste de Parámetros")
col_weights, col_thresh = st.columns([2, 1])

with col_weights:
    st.subheader("Pesos de la Matriz 3x3")
    # Generar rejilla de sliders para simular los píxeles
    w = []
    c1, c2, c3 = st.columns(3)
    for i in range(9):
        with [c1, c2, c3][i % 3]:
            # Inicializamos en 1.0 la fila superior y la columna central para guiar al usuario
            valor_inicial = 1.0 if (i < 3 or i % 3 == 1) else -1.0
            peso = st.slider(f"W Píxel {i+1}", -2.0, 2.0, valor_inicial, 0.1, key=f"w_{i}")
            w.append(peso)

with col_thresh:
    st.subheader("Umbral de Decisión")
    threshold = st.slider("Threshold", -5.0, 10.0, 3.0, 0.1)

# 3. Evaluación Automática de todos los ejemplos
st.header("📊 Evaluación de Ejemplos")

aciertos = 0
total_ejemplos = len(ejemplos)

for nombre, pixeles in ejemplos.items():
    es_t_real = "Positivo" in nombre
    
    # Cálculo manual del Score (Suma ponderada píxel por píxel)
    score = sum(p * peso for p, peso in zip(pixeles, w))
    
    # Regla de clasificación automática
    prediccion = "Es una T" if score > threshold else "No es una T"
    
    # Validación del acierto
    es_correcto = (prediccion == "Es una T" and es_t_real) or (prediccion == "No es una T" and not es_t_real)
    if es_correcto:
        aciertos += 1
        
    # Mostrar visualmente el estado del patrón
    with st.expander(f"{'✅' if es_correcto else '❌'} {nombre} | Score: {score:.1f}"):
        # Dibujar la matriz visualmente de forma simple
        matriz_visual = np.array(pixeles).reshape(3, 3)
        st.code(str(matriz_visual).replace('[', '').replace(']', ''), language="markdown")
        st.write(f"**Puntaje obtenido:** {score:.1f} | **Threshold:** {threshold}")
        st.write(f"**Decisión de la máquina:** *{prediccion}*")

# 4. Marcador global de desempeño
st.subheader(f"📈 Rendimiento del Sistema: {aciertos} / {total_ejemplos} correctos")
if aciertos == total_ejemplos:
    st.success("¡Perfecto! Encontraste los pesos y el umbral exactos para detectar la 'T' y rechazar las demás formas.")
