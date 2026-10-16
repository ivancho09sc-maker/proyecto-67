# Despliegue en AWS: EC2 + RDS (MySQL)

Arquitectura: el navegador llega a **Nginx** (puerto 80) en una instancia **EC2**, Nginx pasa la petición a **gunicorn** (Flask) y la app guarda los datos en **RDS MySQL**.

```
Usuario ──► EC2 (Nginx :80 ─► gunicorn :8000 ─► Flask) ──► RDS MySQL :3306
```

## 1. Crear la base de datos en RDS
1. Consola AWS → **RDS → Create database** → *Standard create* → **MySQL**.
2. Plantilla **Free tier** (si tu cuenta la tiene), instancia `db.t3.micro` o similar.
3. Identificador: `elixir-urbano`. Usuario maestro: `admin`. Define una contraseña y guárdala.
4. En *Additional configuration* → **Initial database name**: `elixir_urbano`.
5. *Public access*: **No**. Crea un Security Group nuevo llamado `sg-rds`.
6. Cuando esté *Available*, copia el **Endpoint** (algo como `elixir-urbano.xxxx.us-east-1.rds.amazonaws.com`).

## 2. Crear el servidor EC2
1. **EC2 → Launch instance** → Ubuntu Server 24.04 LTS → tipo `t2.micro`/`t3.micro`.
2. Crea (o elige) un **key pair** `.pem` y guárdalo bien.
3. Security Group `sg-ec2` con reglas de entrada:
   - SSH (22) → solo **tu IP**
   - HTTP (80) → `0.0.0.0/0`
   - HTTPS (443) → `0.0.0.0/0` (opcional)
4. Vuelve a `sg-rds` y agrega regla de entrada: **MySQL/Aurora (3306)** con origen = `sg-ec2`
   (así solo tu servidor puede hablar con la base de datos).
5. Asigna una **Elastic IP** a la instancia para que la dirección no cambie al reiniciar.

## 3. Preparar el servidor
```bash
ssh -i tu-llave.pem ubuntu@IP_DE_LA_INSTANCIA

sudo apt update && sudo apt install -y python3-venv python3-pip nginx git mysql-client
```

## 4. Traer el proyecto desde Git
```bash
cd ~
git clone https://github.com/TU_USUARIO/elixir_urbano.git
cd elixir_urbano
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Configurar variables de entorno
```bash
cp .env.example .env
nano .env        # completa SECRET_KEY, DB_HOST (endpoint de RDS) y DB_PASSWORD
python3 -c "import secrets; print(secrets.token_hex(32))"   # úsalo como SECRET_KEY
```

Prueba la conexión a RDS antes de seguir:
```bash
mysql -h ENDPOINT_RDS -u admin -p -e "SHOW DATABASES;"
```
Debe aparecer `elixir_urbano`. Si se queda colgado, revisa la regla 3306 de `sg-rds`.

## 6. Crear las tablas
Al arrancar, `app.py` ejecuta `db.create_all()` y crea las tablas solo. Si prefieres hacerlo con el script SQL:
```bash
mysql -h ENDPOINT_RDS -u admin -p < schema_mysql.sql
```

## 7. Servicio con gunicorn (systemd)
```bash
sudo cp deploy/elixir.service /etc/systemd/system/elixir.service
sudo systemctl daemon-reload
sudo systemctl enable --now elixir
sudo systemctl status elixir        # debe decir "active (running)"
```

## 8. Nginx
```bash
sudo cp deploy/nginx_elixir.conf /etc/nginx/sites-available/elixir
sudo ln -s /etc/nginx/sites-available/elixir /etc/nginx/sites-enabled/elixir
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```
Abre `http://IP_ELASTICA/` en el navegador. Ya está en línea.

Verifica también la conexión a la base de datos (sirve para mostrarla en la sustentación):
```bash
curl http://IP_ELASTICA/health      # {"base_de_datos":"ok","estado":"ok"}
```
Si más adelante agregas HTTPS (dominio + certificado), pon `COOKIE_SECURE=1` en `.env` para que la cookie de sesión solo viaje cifrada.

## 9. Actualizar el proyecto después
```bash
cd ~/elixir_urbano && git pull
source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart elixir
```

## Problemas frecuentes
| Síntoma | Causa probable |
|---|---|
| 502 Bad Gateway | gunicorn no está corriendo: `sudo journalctl -u elixir -n 50` |
| `Falta SECRET_KEY` en los logs | completa `SECRET_KEY` en `.env` (es obligatoria en el servidor) |
| `/health` responde 503 | la app no alcanza RDS: revisa `DB_HOST`, usuario/clave y la regla 3306 |
| Timeout al conectar a RDS | falta la regla 3306 en `sg-rds` con origen `sg-ec2`, o RDS está en otra VPC |
| `Access denied for user` | `DB_USER` / `DB_PASSWORD` mal escritos en `.env` |
| `Unknown column 'stock'` | la tabla `producto` es anterior al stock: ejecuta los `ALTER TABLE` de `schema_mysql.sql` |
| `Table 'venta' doesn't exist` | reinicia el servicio (`sudo systemctl restart elixir`): crea las tablas nuevas al arrancar |
| Cambié `.env` y no pasa nada | `sudo systemctl restart elixir` |

## Buenas prácticas
- `.env` nunca se sube a Git (ya está en `.gitignore`).
- No dejes RDS con acceso público.
- Al terminar la evaluación, detén o elimina EC2, RDS y la Elastic IP para no generar cobros.
