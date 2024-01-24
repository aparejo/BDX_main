
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


function actualizar_categorias() {
    var evento_id = document.getElementById("id_evento").value;
    var url = "/obtener_categorias/" + evento_id + "/";
    
    fetch(url)
      .then(response => response.json())
      .then(data => {
        var selectCategoria = document.getElementById("id_categoria");
        selectCategoria.innerHTML = "";
        
        data.forEach(categoria => {
          var option = document.createElement("option");
          option.value = categoria.id;
          option.text = categoria.nombre;
          selectCategoria.appendChild(option);
        });
        
        actualizar_categorias();
      });
  }