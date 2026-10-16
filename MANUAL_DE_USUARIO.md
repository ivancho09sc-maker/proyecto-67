---
title: "Manual de usuario — Elixir Urbano"
subtitle: "Sistema de información para la gestión de inventario de la droguería"
lang: es
---

# 1. Introducción

**Elixir Urbano** es una aplicación web que permite a la droguería registrar y controlar sus medicamentos: cuántas unidades hay, a qué precio se venden y cuándo es necesario reponerlos. Reemplaza el control manual y reduce errores y pérdidas de productos.

Este manual explica, paso a paso, cómo usar la aplicación.

# 2. Requisitos

- Un computador, tablet o celular con conexión a internet.
- Un navegador actualizado (Chrome, Edge o Firefox).
- La dirección web (URL) de la aplicación, que entrega el administrador del sistema.

# 3. Tipos de acceso

| Tipo | Qué puede hacer |
|---|---|
| Visitante (sin sesión) | Ver el inicio, el catálogo y el listado de productos (solo lectura). |
| Usuario registrado (con sesión) | Todo lo anterior, más crear, editar y eliminar productos; administrar clientes; registrar y anular ventas; y descargar reportes. |

# 4. Crear una cuenta

1. En la página de inicio pulse **Registrarse**.
2. Escriba su **nombre completo** y su **correo electrónico**.
3. Escriba una **contraseña de mínimo 8 caracteres** y repítala en *Confirmar contraseña*.
4. Pulse **Registrarse**. Si todo está correcto verá el mensaje *"Cuenta creada correctamente"*.

Mensajes posibles: *"Ese correo ya está registrado"* (use otro correo o inicie sesión) y *"Las contraseñas no coinciden"* (vuelva a escribirlas).

# 5. Iniciar y cerrar sesión

1. Pulse **Iniciar sesión**.
2. Escriba su correo y su contraseña, y pulse **Ingresar**.
3. Si los datos son correctos entrará a la pantalla de **Inventario de Productos**.
4. Para salir pulse el botón **Cerrar sesión** (arriba a la derecha). Haga esto siempre que use un equipo compartido. La sesión también se cierra sola después de 8 horas.

# 6. Pantallas de consulta

- **Inicio:** resumen del proyecto con indicadores (productos, clientes, ventas activas, ingresos, productos con stock bajo y usuarios) y la lista de **medicamentos de mayor rotación**.
- **Catálogo:** productos disponibles con imagen y precio.
- **Vista pública:** productos con su descripción.
- **Inventario (Productos):** tabla con ID, nombre, precio, stock, estado y descripción, además de la vista en tarjetas.

# 7. Gestión del inventario

> Debe haber iniciado sesión para ver estas opciones.

## 7.1 Crear un producto

1. En **Inventario**, vaya a la sección **Crear Producto**.
2. Complete los campos:
   - **Nombre:** mínimo 2 caracteres.
   - **Precio:** número mayor a 0.
   - **Stock:** unidades disponibles (entero, 0 o más).
   - **Stock mínimo:** cantidad a partir de la cual se debe reponer (entero, 0 o más).
   - **URL imagen** (opcional): dirección que empiece por `http://` o `https://`.
   - **Descripción** (opcional).
3. Pulse **Guardar producto**. Aparecerá *"Producto creado correctamente"*.

## 7.2 Editar un producto

1. En la tabla, pulse **Editar** en la fila del producto.
2. Modifique los datos necesarios (por ejemplo, el stock después de recibir mercancía).
3. Pulse **Actualizar**. Para salir sin guardar pulse **Cancelar**.

## 7.3 Eliminar un producto

1. Pulse **Eliminar** en la fila del producto.
2. Confirme en el mensaje *"¿Seguro que deseas eliminar este producto?"*.
3. El producto se borra de forma definitiva.

## 7.4 Alertas de stock bajo

Cuando el **stock** de un producto es **igual o menor** que su **stock mínimo**:

- Aparece un aviso naranja en la parte superior con la lista de productos por reponer.
- El producto muestra la etiqueta roja **Stock bajo** en la tabla.

# 8. Clientes

> Debe haber iniciado sesión. Se accede desde el menú **Clientes**.

1. En **Crear Cliente** escriba el **nombre** y el **documento** (5 a 20 caracteres, sin repetir con otro cliente). El **teléfono** y el **correo** son opcionales.
2. Pulse **Guardar cliente**.
3. Para corregir datos pulse **Editar**; para borrar un cliente pulse **Eliminar** y confirme. Las ventas que ya hizo se conservan, pero quedan como "Sin cliente".

# 9. Ventas

> Debe haber iniciado sesión. Se accede desde el menú **Ventas**.

## 9.1 Registrar una venta

1. Pulse **+ Nueva venta**.
2. Elija el **cliente** (opcional).
3. En la primera línea elija el **producto** y escriba la **cantidad**. Pulse **+ Agregar otro producto** para añadir más líneas, o **✕** para quitar una.
4. El sistema muestra el subtotal de cada línea y el **total**. No permite pedir más unidades que las disponibles.
5. Pulse **Registrar venta**. El **stock de cada producto se descuenta automáticamente**.

## 9.2 Ver el detalle de una venta

En **Ventas** pulse **Ver detalle** para ver los productos, cantidades, precios y el total. El precio queda guardado tal como era el día de la venta, aunque después se cambie en el inventario.

## 9.3 Anular una venta

1. Abra el detalle de la venta y pulse **Anular venta**.
2. Confirme el mensaje. La venta queda marcada como **Anulada** y las unidades **vuelven al inventario**.
3. Una venta anulada no se puede reactivar y no suma en los totales.

# 10. Reportes

Los reportes se descargan con sesión iniciada:

| Dónde | Botón | Archivo | Contenido |
|---|---|---|---|
| Inventario | Reporte Excel | `reporte_inventario.xlsx` | Productos, precio, stock, valor en inventario, totales y productos con stock bajo resaltados. |
| Inventario | Reporte PDF | `reporte_inventario.pdf` | Lo mismo, listo para imprimir. |
| Ventas | Reporte Excel | `reporte_ventas.xlsx` | Hoja de ventas (con total de ventas activas) y hoja de los 10 medicamentos más vendidos. |
| Ventas | Reporte PDF | `reporte_ventas.pdf` | Historial de ventas y Top 10 de rotación. |

# 11. Mensajes frecuentes y soluciones

| Mensaje o situación | Qué hacer |
|---|---|
| *Usuario o contraseña incorrectos* | Revise mayúsculas y que el correo sea el mismo con el que se registró. |
| *Debes iniciar sesión para acceder a esta sección* | Inicie sesión e intente de nuevo. |
| *El precio debe ser mayor a 0* | Escriba un precio positivo, sin letras. |
| *El stock y el stock mínimo no pueden ser negativos* | Use números enteros desde 0. |
| *La URL de la imagen debe empezar por http:// o https://* | Copie la dirección completa de la imagen o deje el campo vacío. |
| *Stock insuficiente de ...* | Reduzca la cantidad de esa línea o reponga el producto en el inventario. |
| *Ya existe un cliente con ese documento* | Busque al cliente en el listado y edítelo en lugar de crear uno nuevo. |
| *La solicitud no es válida o el formulario expiró* | Recargue la página (tecla F5) e intente de nuevo. |
| No aparecen los botones de crear, editar, ventas o reportes | Su sesión no está iniciada o expiró. Inicie sesión. |
| La página no carga | Verifique su conexión a internet y la dirección web; si persiste, avise al administrador. |

# 12. Recomendaciones

- Actualice el stock cada vez que **reciba** mercancía (las ventas lo descuentan solas).
- Revise el aviso de stock bajo al comenzar el día.
- Defina un stock mínimo realista para los medicamentos de alta rotación.
- Cierre la sesión al terminar.
- No comparta su contraseña.
