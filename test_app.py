"""Pruebas automáticas del sistema (evidencia de la etapa de pruebas).
Ejecutar desde la carpeta del proyecto:   python -m unittest discover -s tests -v
Usan una base de datos SQLite temporal: no tocan tus datos reales.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_db.close()
os.environ["DATABASE_URL"] = "sqlite:///" + _db.name
os.environ.pop("DB_HOST", None)

import app as m  # noqa: E402


def tearDownModule():
    with m.app.app_context():
        m.db.session.remove()
        m.db.engine.dispose()
    try:
        os.unlink(_db.name)
    except OSError:
        pass


class Base(unittest.TestCase):
    def setUp(self):
        self.c = m.app.test_client()

    def post(self, url, data=None, **kw):
        """POST con token CSRF válido (como lo enviaría un formulario real)."""
        with self.c.session_transaction() as s:
            s["_csrf"] = "token-de-prueba"
        datos = dict(data or {})
        datos["_csrf"] = "token-de-prueba"
        return self.c.post(url, data=datos, **kw)

    def registrar_y_entrar(self, correo="ana@mail.com"):
        self.post("/registro.html", {"nombre": "Ana", "email": correo, "password": "clave1234", "confirmar": "clave1234"})
        return self.post("/login.html", {"usuario": correo, "clave": "clave1234"}, follow_redirects=True)


class TestAcceso(Base):
    def test_paginas_publicas(self):
        for url in ["/", "/productos.html", "/proyectofinal.html", "/proyectoelixirurbano.html",
                    "/login.html", "/registro.html"]:
            self.assertEqual(self.c.get(url).status_code, 200, url)

    def test_health_confirma_conexion_a_bd(self):
        r = self.c.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["base_de_datos"], "ok")

    def test_rutas_privadas_exigen_login(self):
        for url in ["/clientes.html", "/ventas.html", "/ventas/nueva", "/reportes/excel", "/reportes/pdf",
                    "/reportes/ventas/excel", "/reportes/ventas/pdf"]:
            self.assertEqual(self.c.get(url).status_code, 302, url)
        self.assertEqual(self.post("/productos/crear", {"nombre": "X", "precio": "1"}).status_code, 302)

    def test_post_sin_csrf_es_rechazado(self):
        self.assertEqual(self.c.post("/login.html", data={"usuario": "a@b.co", "clave": "x"}).status_code, 400)

    def test_registro_valida_y_cifra_contrasena(self):
        r = self.post("/registro.html", {"nombre": "A", "email": "malo", "password": "123", "confirmar": "9"}, follow_redirects=True)
        self.assertIn("al menos 8".encode(), r.data)
        self.registrar_y_entrar("cifrada@mail.com")
        with m.app.app_context():
            u = m.Usuario.query.filter_by(email="cifrada@mail.com").first()
            self.assertNotIn("clave1234", u.password_hash)
            self.assertTrue(u.check_password("clave1234"))

    def test_login_incorrecto(self):
        r = self.post("/login.html", {"usuario": "nadie@mail.com", "clave": "xxxxxxxx"}, follow_redirects=True)
        self.assertIn("incorrectos".encode(), r.data)


class TestCRUD(Base):
    def setUp(self):
        super().setUp()
        self.registrar_y_entrar("crud@mail.com")

    def test_crud_producto_y_validaciones(self):
        r = self.post("/productos/crear", {"nombre": "Prueba", "precio": "-5", "stock": "1", "stock_minimo": "1"}, follow_redirects=True)
        self.assertIn("mayor a 0".encode(), r.data)
        r = self.post("/productos/crear", {"nombre": "Vitamina C", "precio": "12500", "stock": "3", "stock_minimo": "5"}, follow_redirects=True)
        self.assertIn("creado correctamente".encode(), r.data)
        self.assertIn("Alerta de stock bajo".encode(), r.data)
        with m.app.app_context():
            pid = m.Producto.query.filter_by(nombre="Vitamina C").first().id
        r = self.post(f"/productos/editar/{pid}", {"nombre": "Vitamina C 1g", "precio": "13000", "stock": "50", "stock_minimo": "5"}, follow_redirects=True)
        self.assertIn("actualizado".encode(), r.data)
        r = self.post(f"/productos/eliminar/{pid}", follow_redirects=True)
        self.assertIn("eliminado".encode(), r.data)

    def test_crud_cliente_y_documento_unico(self):
        datos = {"nombre": "Luis Pérez", "documento": "55667788", "telefono": "3001112233", "email": "luis@mail.com"}
        self.assertIn("creado correctamente".encode(), self.post("/clientes/crear", datos, follow_redirects=True).data)
        self.assertIn("Ya existe".encode(), self.post("/clientes/crear", datos, follow_redirects=True).data)
        bad = dict(datos, documento="1", nombre="X")
        self.assertIn("documento debe tener".encode(), self.post("/clientes/crear", bad, follow_redirects=True).data)
        with m.app.app_context():
            cid = m.Cliente.query.filter_by(documento="55667788").first().id
        datos["nombre"] = "Luis P. Actualizado"
        self.assertIn("actualizado".encode(), self.post(f"/clientes/editar/{cid}", datos, follow_redirects=True).data)
        self.assertIn("eliminado".encode(), self.post(f"/clientes/eliminar/{cid}", follow_redirects=True).data)


class TestVentas(Base):
    def setUp(self):
        super().setUp()
        self.registrar_y_entrar("ventas@mail.com")
        self.post("/productos/crear", {"nombre": "Producto Venta", "precio": "1000", "stock": "10", "stock_minimo": "2"})
        with m.app.app_context():
            self.pid = m.Producto.query.filter_by(nombre="Producto Venta").order_by(m.Producto.id.desc()).first().id

    def stock(self):
        with m.app.app_context():
            return m.db.session.get(m.Producto, self.pid).stock

    def test_venta_descuenta_stock_y_anular_lo_devuelve(self):
        antes = self.stock()
        r = self.post("/ventas/nueva", {"producto_id": [str(self.pid)], "cantidad": ["4"]}, follow_redirects=True)
        self.assertIn("registrada".encode(), r.data)
        self.assertEqual(self.stock(), antes - 4)
        with m.app.app_context():
            venta = m.Venta.query.order_by(m.Venta.id.desc()).first()
            self.assertEqual(float(venta.total), 4000.0)
            vid = venta.id
        self.assertIn("anulada".encode(), self.post(f"/ventas/anular/{vid}", follow_redirects=True).data)
        self.assertEqual(self.stock(), antes)
        self.assertIn("ya estaba anulada".encode(), self.post(f"/ventas/anular/{vid}", follow_redirects=True).data)
        self.assertEqual(self.stock(), antes)

    def test_venta_con_stock_insuficiente_es_rechazada(self):
        antes = self.stock()
        r = self.post("/ventas/nueva", {"producto_id": [str(self.pid)], "cantidad": [str(antes + 1)]}, follow_redirects=True)
        self.assertIn("Stock insuficiente".encode(), r.data)
        self.assertEqual(self.stock(), antes)

    def test_venta_vacia_o_con_cantidad_invalida(self):
        self.assertIn("al menos un producto".encode(), self.post("/ventas/nueva", {}, follow_redirects=True).data)
        r = self.post("/ventas/nueva", {"producto_id": [str(self.pid)], "cantidad": ["0"]}, follow_redirects=True)
        self.assertIn("al menos 1".encode(), r.data)

    def test_inicio_reportes_y_rotacion_con_ventas(self):
        self.post("/ventas/nueva", {"producto_id": [str(self.pid)], "cantidad": ["2"]})
        self.assertIn("Producto Venta".encode(), self.c.get("/").data)  # aparece en "mayor rotación"
        for url in ["/reportes/ventas/excel", "/reportes/ventas/pdf", "/ventas.html"]:
            self.assertEqual(self.c.get(url).status_code, 200, url)

    def test_historial_se_conserva_si_borran_el_producto(self):
        self.post("/ventas/nueva", {"producto_id": [str(self.pid)], "cantidad": ["1"]})
        self.post(f"/productos/eliminar/{self.pid}")
        with m.app.app_context():
            d = m.DetalleVenta.query.filter_by(nombre_producto="Producto Venta").first()
            self.assertIsNotNone(d)
            self.assertIsNone(d.producto_id)


class TestReportes(Base):
    def setUp(self):
        super().setUp()
        self.registrar_y_entrar("reportes@mail.com")

    def test_reportes_se_descargan(self):
        casos = {
            "/reportes/excel": (b"PK", "spreadsheetml"),
            "/reportes/ventas/excel": (b"PK", "spreadsheetml"),
            "/reportes/pdf": (b"%PDF", "pdf"),
            "/reportes/ventas/pdf": (b"%PDF", "pdf"),
        }
        for url, (firma, tipo) in casos.items():
            r = self.c.get(url)
            self.assertEqual(r.status_code, 200, url)
            self.assertTrue(r.data.startswith(firma), url)
            self.assertIn(tipo, r.mimetype, url)


if __name__ == "__main__":
    unittest.main()
