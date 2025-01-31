
from fastapi import FastAPI, Response, Request
from app.pdf_generator import generate_pdf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://tudominio.com"] en vez de "*" por seguridad
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.post("/generate-report")
async def generate_report(data: dict):
    """
    Genera un reporte en PDF basado en los datos recibidos.
    """
    # Generar el PDF usando el módulo pdf_generator
    pdf_binary = generate_pdf(data)

    # Retornar el PDF como respuesta
    headers = {'Content-Disposition': 'inline; filename="Reporte.pdf"'}
    return Response(content=pdf_binary, media_type="application/pdf", headers=headers)

@app.post("/receive-data")
async def receive_data(request: Request):
    """
    Recibe datos en formato JSON y decide si debe generar un reporte o devolver una respuesta natural.
    """
    # Leer el JSON enviado por el cliente
    data = await request.json()

    # Verificar si la clave "tipo" está en el JSON
    tipo = data.get("tipo", "").lower()

    if tipo == "reporte":
        # Si el tipo es "reporte", llamar a generate_report con data como parámetro directamente
        # return await generate_report(data)
        return data
    elif tipo == "natural":
        # Si el tipo es "natural", devolver una respuesta en JSON con el texto adecuado
        respuesta = data.get("respuesta", "¡Hola! ¿En qué puedo ayudarte hoy?")
        return {"output": {"tipo": "natural", "respuesta": respuesta}}
    else:
        # Si el tipo no es válido, devolver un mensaje de error
        return {"error": "Tipo de solicitud no reconocido. Usa 'reporte' o 'natural'."}
