document.addEventListener('DOMContentLoaded', function () {
    var botonesEditar = document.querySelectorAll('.editar');
    var botonesEliminar = document.querySelectorAll('.eliminar');
    var transcriptionDiv = document.getElementById('transcription');

    function actualizarTranscripcion(contenedorTexto) {
        var textoContenido = contenedorTexto.textContent.trim();

        if (textoContenido !== '') {
            var nuevoTexto = document.createTextNode(textoContenido);
            transcriptionDiv.innerHTML = '';
            transcriptionDiv.appendChild(nuevoTexto);
        }
    }

    function manejarEliminarClick(botonEliminar) {
        var contenedorPadre = botonEliminar.closest('.content');
        var contenedorTexto = contenedorPadre.querySelector('.texto');
        var inputTexto = contenedorTexto.querySelector('input');

        if (inputTexto) {
            // Si hay un input de texto, actualizar la transcripción
            actualizarTranscripcion(inputTexto);
            // Guardar en localStorage
            localStorage.setItem('textoGuardado', inputTexto.value);
        } else {
            // Si no hay un input de texto, se está en modo de texto normal
            actualizarTranscripcion(contenedorTexto);
        }
    }

    function manejarEditarClick(botonEditar) {
        var contenedorPadre = botonEditar.closest('.content');
        var contenedorTexto = contenedorPadre.querySelector('.texto');

        var inputTexto = document.createElement('input');
        inputTexto.type = 'text';

        // Recuperar el texto guardado del localStorage
        inputTexto.value = localStorage.getItem('textoGuardado') || contenedorTexto.textContent.trim();

        contenedorTexto.innerHTML = '';
        contenedorTexto.appendChild(inputTexto);

        inputTexto.focus();

        inputTexto.addEventListener('blur', function () {
            contenedorTexto.textContent = inputTexto.value;
            actualizarTranscripcion(contenedorTexto);
            // Guardar en localStorage
            localStorage.setItem('textoGuardado', inputTexto.value);
        });
    }

    function cargarTextoGuardado() {
        var textoGuardado = localStorage.getItem('textoGuardado');
        var contenedorTexto = document.querySelector('.texto');

        if (textoGuardado && contenedorTexto) {
            contenedorTexto.textContent = textoGuardado;
            actualizarTranscripcion(contenedorTexto);
            // Si hay texto guardado, vaciar transcriptionDiv
            transcriptionDiv.innerHTML = '';
        } else {
            // Si no hay texto guardado, vaciar transcriptionDiv
            transcriptionDiv.innerHTML = '';
        }
    }

    // Llamar a la función para cargar el texto guardado al cargar la página
    cargarTextoGuardado();

    botonesEliminar.forEach(function (botonEliminar) {
        botonEliminar.addEventListener('click', function () {
            manejarEliminarClick(botonEliminar);
        });
    });

    botonesEditar.forEach(function (botonEditar) {
        botonEditar.addEventListener('click', function () {
            manejarEditarClick(botonEditar);
        });
    });
});
