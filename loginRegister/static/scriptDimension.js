document.addEventListener('DOMContentLoaded', function () {
    const transcription = document.querySelector('.transcription');

    // Ajustar tamaño de fuente dinámicamente
    function adjustFontSize() {
        const transcriptionHeight = transcription.scrollHeight;
        const windowHeight = window.innerHeight;
        const fontSize = parseFloat(window.getComputedStyle(transcription).fontSize);

        // Calcular el nuevo tamaño de fuente basado en la relación entre el contenido y la ventana
        const newFontSize = (windowHeight / transcriptionHeight) * fontSize;

        // Aplicar el nuevo tamaño de fuente
        transcription.style.fontSize = newFontSize + 'px';

        // Ajustar la altura del contenido dinámicamente
        transcription.style.height = windowHeight + 'px';
    }

    // Agregar un manejador de eventos para ajustes dinámicos
    window.addEventListener('resize', adjustFontSize);
});

