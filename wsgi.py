# Punto de entrada para gunicorn en el servidor (AWS):  gunicorn wsgi:app
import os

from app import app

# En producción la clave secreta DEBE venir del archivo .env: con la clave por defecto cualquiera podría falsificar sesiones.
if not os.getenv("SECRET_KEY"):
    raise RuntimeError("Falta SECRET_KEY en el archivo .env (ver .env.example).")

if __name__ == "__main__":
    app.run()
