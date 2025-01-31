
# from fpdf import FPDF
# import matplotlib.pyplot as plt
# import tempfile
# import io

# def generate_dynamic_graph(data, graph_type="bar"):
#     """
#     Genera un gráfico dinámico en función de los datos proporcionados.
#     :param data: Lista de diccionarios con los datos.
#     :param graph_type: Tipo de gráfico ('bar', 'pie', 'line').
#     :return: Imagen en bytes del gráfico generado.
#     """
#     labels = [item.get("nombre", "Sin nombre") for item in data]
#     values = [item.get("calificacion", 0) for item in data]

#     plt.figure(figsize=(8, 6))
#     if graph_type == "bar":
#         plt.bar(labels, values, color="skyblue")
#         plt.ylabel("Calificaciones")
#         plt.xlabel("Proyectos")
#     elif graph_type == "pie":
#         plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
#     elif graph_type == "line":
#         plt.plot(labels, values, marker="o", linestyle="-", color="blue")
#         plt.ylabel("Calificaciones")
#         plt.xlabel("Proyectos")
#     else:
#         raise ValueError("Tipo de gráfico no soportado.")

#     plt.title("Gráfico de Calificaciones")
#     plt.tight_layout()

#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format="png")
#     plt.close()
#     img_buffer.seek(0)
#     return img_buffer

# def generate_pdf(data):
#     """
#     Genera un PDF dinámico en función de los datos proporcionados.
#     :param data: Diccionario con información para el reporte.
#     :return: Contenido binario del PDF.
#     """
#     proyectos = data.get("proyectos", [])
#     graph_type = data.get("graph_type", "bar")  # Tipo de gráfico solicitado

#     class PDF(FPDF):
#         def header(self):
#             self.set_font("Arial", size=12)
#             self.cell(0, 10, data.get("resumen", "resumen"), ln=True, align="C")
#             self.ln(10)

#         def footer(self):
#             self.set_y(-15)
#             self.set_font("Arial", size=10)
#             self.cell(0, 10, f"Página {self.page_no()}", align="C")

#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     pdf.multi_cell(0, 10, "Proyectos y Calificaciones Promedio:")

#     for proyecto in proyectos:
#         nombre = proyecto.get("nombre", "Sin nombre")
#         calificacion = proyecto.get("calificacion", "No especificada")
#         pdf.multi_cell(0, 10, f"Proyecto: {nombre}, Calificación: {calificacion}")

#     graph_image = generate_dynamic_graph(proyectos, graph_type=graph_type)
#     with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
#         temp_file.write(graph_image.read())
#         temp_file_name = temp_file.name

#     pdf.ln(10)
#     pdf.image(temp_file_name, x=10, y=pdf.get_y(), w=180)

#     pdf_binary = pdf.output(dest="S").encode("latin1")

#     return pdf_binary

# # Ejemplo de uso:
# data = {
#     "proyectos": [
#         {"nombre": "Proyecto A", "calificacion": 85},
#         {"nombre": "Proyecto B", "calificacion": 90},
#         {"nombre": "Proyecto C", "calificacion": 78},
#     ],
#     "graph_type": "bar"  # Tipo de gráfico: 'bar', 'pie', 'line'
# }

# # Generar el PDF
# pdf_content = generate_pdf(data)

# # Guardar el PDF en un archivo (opcional)
# with open("reporte_simplificado.pdf", "wb") as f:
#     f.write(pdf_content)

from fpdf import FPDF
import matplotlib.pyplot as plt
import io

def generate_pdf(data, include_graph=True):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar el título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Reporte de Datos", ln=True, align='C')
    pdf.ln(10)

    # Agregar el resumen
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, data.get("resumen", "No hay descripción disponible."))
    pdf.ln(10)

    # Agregar los proyectos
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Lista de Proyectos:", ln=True)
    pdf.set_font("Arial", size=12)

    for proyecto in data.get("proyectos", []):
        pdf.cell(0, 10, f"Proyecto: {proyecto['nombre']}, Calificación: {proyecto['calificacion']}", ln=True)
    
    # Verificar si se debe incluir la gráfica
    if include_graph:
        pdf.ln(10)
        pdf.cell(0, 10, "Gráfico de Calificaciones:", ln=True)

        # Crear el gráfico
        nombres = [p["nombre"] for p in data.get("proyectos", [])]
        calificaciones = [float(p["calificacion"]) for p in data.get("proyectos", [])]

        plt.figure(figsize=(6, 4))
        plt.bar(nombres, calificaciones, color='skyblue')
        plt.xlabel("Proyectos")
        plt.ylabel("Calificaciones")
        plt.xticks(rotation=45, ha='right')
        plt.title("Calificación de los Proyectos")

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)

        # Agregar la imagen al PDF
        pdf.image(img_buffer, x=10, y=pdf.get_y(), w=180)
        img_buffer.close()

    return pdf.output(dest='S').encode('latin1')
