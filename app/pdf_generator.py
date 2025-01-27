# from app.graph_generator import generate_graph
# from fpdf import FPDF
# import tempfile


# def generate_pdf(data):
#     # Extraer datos dinámicos
#     fecha = data.get("fecha", "Fecha no especificada")
#     para = data.get("para", "Nombre no especificado")
#     de = data.get("de", "Tu Nombre")
#     resumen = data.get("resumen", "Resumen no especificado")
#     proyectos = data.get("proyectos", [])

#     # Clase personalizada para el PDF
#     class PDF(FPDF):
#         def header(self):
#             self.set_font("Arial", size=12)
#             self.cell(0, 10, "Informe de Calificaciones de Proyectos", ln=True, align="C")
#             self.ln(10)

#         def footer(self):
#             self.set_y(-15)
#             self.set_font("Arial", size=10)
#             self.cell(0, 10, f"Página {self.page_no()}", align="C")

#     # Crear el PDF
#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # Agregar contenido dinámico
#     pdf.multi_cell(0, 10, f"""
#     Fecha: {fecha}
#     Para: {para}
#     De: {de}

#     Resumen
#     {resumen}

#     Proyectos y Calificaciones Promedio
#     """)

#     for proyecto in proyectos:
#         nombre = proyecto.get("nombre", "Proyecto sin nombre")
#         integrantes = proyecto.get("integrantes", [])
#         calificacion = proyecto.get("calificacion", "No especificada")

#         pdf.multi_cell(0, 10, f"""
#         Proyecto: {nombre}
#         Integrantes: {', '.join(integrantes)}
#         Calificación Promedio: {calificacion}
#         """)

#     # Generar gráfica y agregarla al PDF
#     graph_image = generate_graph(proyectos)
#     with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
#         temp_file.write(graph_image.read())
#         temp_file_name = temp_file.name

#     pdf.ln(10)
#     pdf.image(temp_file_name, x=10, y=pdf.get_y(), w=180)

#     # Guardar el PDF como un string en memoria
#     pdf_binary = pdf.output(dest='S').encode('latin1')  # Guardar el PDF en memoria

#     return pdf_binary

from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import io

def generate_dynamic_graph(data, graph_type="bar"):
    """
    Genera un gráfico dinámico en función de los datos proporcionados.
    :param data: Lista de diccionarios con los datos.
    :param graph_type: Tipo de gráfico ('bar', 'pie', 'line').
    :return: Imagen en bytes del gráfico generado.
    """
    labels = [item.get("nombre", "Sin nombre") for item in data]
    values = [item.get("calificacion", 0) for item in data]

    plt.figure(figsize=(8, 6))
    if graph_type == "bar":
        plt.bar(labels, values, color="skyblue")
        plt.ylabel("Calificaciones")
        plt.xlabel("Proyectos")
    elif graph_type == "pie":
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    elif graph_type == "line":
        plt.plot(labels, values, marker="o", linestyle="-", color="blue")
        plt.ylabel("Calificaciones")
        plt.xlabel("Proyectos")
    else:
        raise ValueError("Tipo de gráfico no soportado.")

    plt.title("Gráfico de Calificaciones")
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)
    return img_buffer

def generate_pdf(data):
    """
    Genera un PDF dinámico en función de los datos proporcionados.
    :param data: Diccionario con información para el reporte.
    :return: Contenido binario del PDF.
    """
    proyectos = data.get("proyectos", [])
    graph_type = data.get("graph_type", "bar")  # Tipo de gráfico solicitado

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", size=12)
            self.cell(0, 10, data.get("resumen", "resumen"), ln=True, align="C")
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", size=10)
            self.cell(0, 10, f"Página {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, "Proyectos y Calificaciones Promedio:")

    for proyecto in proyectos:
        nombre = proyecto.get("nombre", "Sin nombre")
        calificacion = proyecto.get("calificacion", "No especificada")
        pdf.multi_cell(0, 10, f"Proyecto: {nombre}, Calificación: {calificacion}")

    graph_image = generate_dynamic_graph(proyectos, graph_type=graph_type)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(graph_image.read())
        temp_file_name = temp_file.name

    pdf.ln(10)
    pdf.image(temp_file_name, x=10, y=pdf.get_y(), w=180)

    pdf_binary = pdf.output(dest="S").encode("latin1")

    return pdf_binary

# Ejemplo de uso:
data = {
    "proyectos": [
        {"nombre": "Proyecto A", "calificacion": 85},
        {"nombre": "Proyecto B", "calificacion": 90},
        {"nombre": "Proyecto C", "calificacion": 78},
    ],
    "graph_type": "bar"  # Tipo de gráfico: 'bar', 'pie', 'line'
}

# Generar el PDF
pdf_content = generate_pdf(data)

# Guardar el PDF en un archivo (opcional)
with open("reporte_simplificado.pdf", "wb") as f:
    f.write(pdf_content)
