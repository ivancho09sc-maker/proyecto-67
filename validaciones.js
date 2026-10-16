/* Validación de datos en el FRONTEND (ítem 3).
   Complementa los atributos HTML5 (required, min, minlength, type) y se repite
   en el BACKEND (app.py), porque el navegador nunca debe ser la única barrera. */
(function () {
  // Campos de texto que no pueden ser solo espacios
  document.querySelectorAll('input[data-no-blank]').forEach(function (campo) {
    campo.addEventListener('input', function () {
      campo.setCustomValidity(campo.value.trim().length < 2 ? 'Escribe al menos 2 caracteres.' : '');
    });
  });

  // Confirmación de contraseña en el registro
  var clave = document.getElementById('password');
  var confirmar = document.getElementById('confirmar');
  if (clave && confirmar) {
    var revisar = function () {
      confirmar.setCustomValidity(confirmar.value !== clave.value ? 'Las contraseñas no coinciden.' : '');
    };
    clave.addEventListener('input', revisar);
    confirmar.addEventListener('input', revisar);
  }

  // El stock mínimo no debe ser negativo ni decimal
  document.querySelectorAll('input[data-entero]').forEach(function (campo) {
    campo.addEventListener('input', function () {
      var v = campo.value;
      campo.setCustomValidity(v !== '' && (!/^\d+$/.test(v)) ? 'Debe ser un número entero mayor o igual a 0.' : '');
    });
  });

  // Confirmación antes de acciones destructivas (eliminar, anular)
  document.querySelectorAll('form[data-confirm]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!window.confirm(f.dataset.confirm)) e.preventDefault();
    });
  });
})();
