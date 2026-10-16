# Elixir Urbano — Sistema de inventario para droguería

Aplicación web en **Python + Flask + SQLAlchemy** con base de datos (SQLite en local, MySQL en AWS RDS).

## Funcionalidades
- Registro e inicio de sesión (contraseñas cifradas, sesiones, base de datos)
- CRUD completo de **productos** y de **clientes**
- Módulo de **ventas**: descuenta stock, permite anular (devuelve el stock) y guarda el historial
- Control de **stock**, **alertas de stock mínimo** y **medicamentos de mayor rotación**
- Protección **CSRF** en todos los formularios y cookies de sesión seguras
- Validación de datos en frontend (HTML5 + JavaScript) y backend (Flask)
- **Reportes de inventario y de ventas en Excel y PDF**
- Pruebas automáticas (`tests/`) y ruta `/health` para verificar la conexión a la base de datos
- Despliegue en AWS (EC2 + RDS)

## Estructura
```
elixir_urbano/
├── app.py                 # aplicación Flask (rutas, modelos, validaciones, reportes)
├── wsgi.py                # entrada para gunicorn
├── requirements.txt
├── schema_mysql.sql       # script SQL de la base de datos
├── .env.example           # plantilla de variables de entorno
├── templates/             # páginas HTML (Jinja2); base.html es la plantilla común
├── tests/                 # pruebas automáticas
├── static/                # style.css, styleregistrer.css, validaciones.js, ventas.js
├── deploy/                # archivos de servidor (systemd, nginx)
├── docs/                  # manual de usuario
└── DEPLOY_AWS.md          # guía de despliegue paso a paso
```

## Ejecutar en el computador
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000/ . Se crea `elixir_urbano.db` (SQLite) automáticamente.

> Si ya tenías un `elixir_urbano.db` de una versión anterior, bórralo: hay tablas y columnas nuevas (stock, clientes, ventas).

## Pruebas automáticas
```bash
python -m unittest discover -s tests -v
```
Usan una base de datos temporal y verifican login, validaciones, CRUD, CSRF, ventas (descuento y devolución de stock) y reportes.

## Usar MySQL
Define las variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (archivo `.env`, ver `.env.example`).
Si `DB_HOST` no existe, la app usa SQLite.

## Repositorio Git
```bash
git init
git add .
git commit -m "Versión inicial del proyecto Elixir Urbano"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/elixir_urbano.git
git push -u origin main
```
Recomendación: que **cada integrante haga sus propios commits** con mensajes claros
(`git commit -m "Agrega reporte en PDF"`), para evidenciar el trabajo del equipo con `git log --oneline`.

## Despliegue
Ver [DEPLOY_AWS.md](DEPLOY_AWS.md).

## Manual de usuario
Ver [docs/MANUAL_DE_USUARIO.md](docs/MANUAL_DE_USUARIO.md) (también en Word: `MANUAL_DE_USUARIO.docx`).
