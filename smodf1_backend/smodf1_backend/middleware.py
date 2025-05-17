class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Procesar la solicitud primero
        response = self.get_response(request)
        
        # Añadir cabeceras CORS a todas las respuestas
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        
        # Si es una petición OPTIONS, devolver una respuesta vacía con headers CORS
        if request.method == "OPTIONS":
            response = response.__class__()
            response.status_code = 200
            
            # Asegurar que las cabeceras CORS se establecen correctamente
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"

        return response 