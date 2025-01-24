import matplotlib.pyplot as plt
import io

def generate_graph(proyectos):
    # Extraer datos para la gráfica
    nombres_proyectos = [p.get("nombre", "N/A") for p in proyectos]
    calificaciones = [p.get("calificacion", 0) for p in proyectos]

    # Crear gráfica
    plt.bar(nombres_proyectos, calificaciones, color='blue')
    plt.xlabel("Proyectos")
    plt.ylabel("Calificaciones Promedio")
    plt.title("Calificaciones de Proyectos")

    # Guardar la gráfica en memoria como imagen
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf
