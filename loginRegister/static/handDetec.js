function toggleCamera() {
    console.log("Toggle Camera function called");
    if (video_feed.style.display === 'none') {
        console.log("Setting display to block");
        video_feed.style.display = 'block';
        interpretation_result.textContent = "";
    } else {
        console.log("Setting display to none");
        video_feed.style.display = 'none';
    }
}

// Crea una conexión Socket.IO
console.log('Socket.IO connection established.');
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Manejar la actualización del resultado de la interpretación
socket.on('interpretation_result', function (interpretation) {
    var interpretation_result = document.getElementById('interpretation_result');
    interpretation_result.textContent = interpretation;
});

document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var interpretationContainer = document.getElementById('interpretation_container');
    var clearButton = document.getElementById('clearButton');

    // Inicializar lastInterpretation con el valor almacenado localmente o por defecto null
    var lastInterpretation = localStorage.getItem('lastInterpretation') || null;

    socket.on('interpretation_result', function (interpretation) {
        console.log('Interpretation received:', interpretation);

        // Verificar si la interpretación es diferente de la anterior
        if (interpretation !== lastInterpretation || lastInterpretation === null) {
            // Crear un nuevo span para la nueva interpretación
            var newSpan = document.createElement('span');
            
            // Agregar espacio entre interpretaciones
            newSpan.style.marginRight = '10px';

            // Agregar la nueva interpretación al contenido del nuevo span
            newSpan.textContent = interpretation;

            // Agregar el nuevo span al contenedor principal
            interpretationContainer.appendChild(newSpan);

            // Actualizar la última interpretación conocida
            lastInterpretation = interpretation;

            // Almacenar la última interpretación en el almacenamiento local del navegador
            localStorage.setItem('lastInterpretation', interpretation);
        }
    });

    // Agregar un event listener al botón para limpiar interpretaciones
    clearButton.addEventListener('click', function () {
        // Limpiar el contenido del contenedor de interpretaciones
        interpretationContainer.innerHTML = '';

        // Restablecer la última interpretación conocida
        lastInterpretation = null;

        // Limpiar la última interpretación almacenada localmente
        localStorage.removeItem('lastInterpretation');
    });
});


// Ocultar el div al cargar la página
document.addEventListener('DOMContentLoaded', function () {
    var interpretationResultDiv = document.getElementById('interpretation_result');
    interpretationResultDiv.style.display = 'none';
});

