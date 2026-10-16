-- Esquema de referencia. La aplicación también crea estas tablas sola al arrancar (db.create_all()).
CREATE DATABASE IF NOT EXISTS elixir_urbano CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE elixir_urbano;

CREATE TABLE IF NOT EXISTS usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS producto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  stock_minimo INT NOT NULL DEFAULT 5,
  imagen VARCHAR(200),
  descripcion VARCHAR(255),
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  documento VARCHAR(20) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  email VARCHAR(120),
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS venta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cliente_id INT NULL,
  usuario_id INT NULL,
  total DECIMAL(12,2) NOT NULL DEFAULT 0,
  estado VARCHAR(10) NOT NULL DEFAULT 'activa',   -- activa | anulada
  FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE SET NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS detalle_venta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  venta_id INT NOT NULL,
  producto_id INT NULL,
  nombre_producto VARCHAR(120) NOT NULL,          -- copia del nombre al momento de la venta
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,         -- copia del precio al momento de la venta
  subtotal DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (venta_id) REFERENCES venta(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE SET NULL
);

-- Si ya tenías la tabla "producto" de una versión anterior SIN stock, ejecuta:
-- ALTER TABLE producto ADD COLUMN stock INT NOT NULL DEFAULT 0;
-- ALTER TABLE producto ADD COLUMN stock_minimo INT NOT NULL DEFAULT 5;
-- ALTER TABLE producto MODIFY precio DECIMAL(10,2) NOT NULL;
