<script>
function cargarPuntos() {
    var formElement = document.getElementById('puntaje-form');
    var formData = new FormData(formElement);

    fetch('/guardar-puntaje/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Manipular la respuesta del backend y actualizar la interfaz de usuario según sea necesario
        alert('Puntos cargados: ' + data.puntos);  // Ejemplo de cómo mostrar una alerta con los puntos
    })
    .catch(error => {
        // Manejar el error en caso de que falle la solicitud AJAX
        console.error('Error al cargar los puntos:', error);
    });
}
</script>