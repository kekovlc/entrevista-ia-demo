
import streamlit as st
import openai
import os

# Configura tu API Key de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# --------------------------
# Preguntas y criterios de evaluación
# --------------------------
preguntas = [
    {
        "pregunta": "Si tienes 4 mesas en tu rango: una acaba de sentarse y necesita el QR, otra ha terminado los primeros y necesita que tomes el pedido de los segundos, otra está levantando la mano y la última te ha pedido la cuenta. ¿Cómo gestionarías la situación?",
        "criterio": "Evaluar la rapidez del candidato y su capacidad para organizar tareas y mantener la eficiencia en momentos de alta demanda."
    },
    {
        "pregunta": "Después de un turno largo, notas que hay vasos y platos vacíos en algunas mesas y que el área de servicio está desordenada. Se acerca el compañero del segundo turno que va a darte el relevo. ¿Cómo os organizáis?",
        "criterio": "Evaluar si el candidato comprende que es su responsabilidad dejar el área de trabajo limpia y organizada antes de ceder el puesto al compañero del segundo turno."
    },
    {
        "pregunta": "Durante un turno de mucho trabajo, un compañero se encuentra sobrecargado y un cliente está visiblemente molesto por una espera. ¿Cómo manejas esta situación para ayudar a tu compañero y al cliente?",
        "criterio": "Evaluar si el candidato tiene iniciativa para apoyar a un compañero sobrecargado y prioriza la satisfacción del cliente, mostrando una actitud colaborativa en momentos de alta presión."
    }
]

# --------------------------
# Función para evaluación con IA
# --------------------------
def evaluar_respuesta_ia(respuesta, criterio):
    prompt = f"""
    Eres un evaluador profesional de entrevistas para personal de sala en un restaurante.
    A continuación se presenta una respuesta del candidato junto con el criterio de evaluación.

    Criterio: {criterio}

    Respuesta del candidato: "{respuesta}"

    Evalúa esta respuesta del 0 al 10 y justifica brevemente tu decisión. Devuelve el resultado en el siguiente formato:
    Puntuación: X/10
    Comentario: ...
    """
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error en evaluación IA: {e}"

# --------------------------
# Streamlit UI
# --------------------------
st.title("🤖 Entrevista Automatizada - Demo con IA")

st.write("Responde a las preguntas como si fueras el candidato. La IA evaluará tus respuestas en base a los criterios definidos.")

respuestas = []
evaluaciones = []
puntuaciones = []

for i, item in enumerate(preguntas):
    st.subheader(f"Pregunta {i+1}")
    st.write(item["pregunta"])
    st.write(f"_Criterio de evaluación: {item['criterio']}_")
    respuesta = st.text_area(f"Tu respuesta a la pregunta {i+1}", key=f"respuesta_{i}")
    if respuesta:
        evaluacion = evaluar_respuesta_ia(respuesta, item["criterio"])
        st.markdown("**Evaluación IA:**")
        st.write(evaluacion)
        respuestas.append(respuesta)
        evaluaciones.append(evaluacion)
        try:
            puntuacion = int(evaluacion.split("Puntuación:")[1].split("/10")[0].strip())
        except:
            puntuacion = 0
        puntuaciones.append(puntuacion)

# Mostrar resultados finales
if len(puntuaciones) == len(preguntas):
    st.markdown("---")
    st.header("📊 Resultado final")
    total = sum(puntuaciones)
    media = total / len(puntuaciones)
    st.write(f"**Puntuación total:** {total}/30")
    st.write(f"**Puntuación media por respuesta:** {round(media, 2)}/10")

    if media >= 8:
        st.success("✅ Excelente candidato. Muestra organización, proactividad y atención al cliente.")
    elif media >= 5:
        st.info("🟡 Candidato con potencial. Requiere algo más de estructura y precisión.")
    else:
        st.warning("🔴 Bajo desempeño. Se recomienda seguir evaluando otras opciones.")
