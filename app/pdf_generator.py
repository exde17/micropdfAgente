from app.graph_generator import generate_graph
from fpdf import FPDF
import tempfile


def generate_pdf(data):
    # Extraer datos dinámicos
    fecha = data.get("fecha", "Fecha no especificada")
    para = data.get("para", "Nombre no especificado")
    de = data.get("de", "Tu Nombre")
    resumen = data.get("resumen", "Resumen no especificado")
    proyectos = data.get("proyectos", [])

    # Clase personalizada para el PDF
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", size=12)
            self.cell(0, 10, "Informe de Calificaciones de Proyectos", ln=True, align="C")
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", size=10)
            self.cell(0, 10, f"Página {self.page_no()}", align="C")

    # Crear el PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar contenido dinámico
    pdf.multi_cell(0, 10, f"""
    Fecha: {fecha}
    Para: {para}
    De: {de}

    Resumen
    {resumen}

    Proyectos y Calificaciones Promedio
    """)

    for proyecto in proyectos:
        nombre = proyecto.get("nombre", "Proyecto sin nombre")
        integrantes = proyecto.get("integrantes", [])
        calificacion = proyecto.get("calificacion", "No especificada")

        pdf.multi_cell(0, 10, f"""
        Proyecto: {nombre}
        Integrantes: {', '.join(integrantes)}
        Calificación Promedio: {calificacion}
        """)

    # Generar gráfica y agregarla al PDF
    graph_image = generate_graph(proyectos)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(graph_image.read())
        temp_file_name = temp_file.name

    pdf.ln(10)
    pdf.image(temp_file_name, x=10, y=pdf.get_y(), w=180)

    # Guardar el PDF como un string en memoria
    pdf_binary = pdf.output(dest='S').encode('latin1')  # Guardar el PDF en memoria

    return pdf_binary