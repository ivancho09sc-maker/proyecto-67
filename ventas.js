/* Formulario de nueva venta: agregar/quitar líneas y calcular el total en pantalla.
   El servidor vuelve a calcular todo (precio, stock y total): esto es solo ayuda visual. */
(function () {
  var contenedor = document.getElementById('lineas');
  if (!contenedor) return;

  var formato = function (n) {
    return '$' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  };

  function recalcular() {
    var total = 0;
    contenedor.querySelectorAll('.linea-venta').forEach(function (fila) {
      var select = fila.querySelector('select');
      var cantidad = fila.querySelector('input[name="cantidad"]');
      var opcion = select.options[select.selectedIndex];
      var precio = parseFloat(opcion.dataset.precio || '0');
      var stock = parseInt(opcion.dataset.stock || '0', 10);
      var n = parseInt(cantidad.value || '0', 10);

      if (opcion.value) cantidad.max = stock; else cantidad.removeAttribute('max');
      cantidad.setCustomValidity(opcion.value && n > stock ? 'Solo hay ' + stock + ' unidades disponibles.' : '');

      var subtotal = (opcion.value && n > 0) ? precio * n : 0;
      fila.querySelector('.subtotal').textContent = formato(subtotal);
      total += subtotal;
    });
    document.getElementById('total-venta').textContent = formato(total);
  }

  contenedor.addEventListener('input', recalcular);
  contenedor.addEventListener('change', recalcular);

  document.getElementById('agregar-linea').addEventListener('click', function () {
    var nueva = contenedor.querySelector('.linea-venta').cloneNode(true);
    nueva.querySelector('select').selectedIndex = 0;
    nueva.querySelector('input[name="cantidad"]').value = 1;
    contenedor.appendChild(nueva);
    recalcular();
  });

  contenedor.addEventListener('click', function (e) {
    if (!e.target.classList.contains('quitar-linea')) return;
    if (contenedor.querySelectorAll('.linea-venta').length > 1) {
      e.target.closest('.linea-venta').remove();
      recalcular();
    }
  });

  recalcular();
})();
