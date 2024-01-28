// Función para cambiar al modo oscuro
function toggleDarkMode() {
    var body = document.body;
    body.classList.toggle('dark-mode');
    var isDarkMode = body.classList.contains('dark-mode');

    // Almacenar la preferencia en localStorage
    localStorage.setItem('darkMode', isDarkMode);
}

// Aplicar el modo oscuro al cargar la página o si está activo según localStorage
window.addEventListener('load', function () {
    var isDarkMode = localStorage.getItem('darkMode') === 'true';
    var body = document.body;

    // Aplicar el modo oscuro si la preferencia está activada
    if (isDarkMode) {
        body.classList.add('dark-mode');
    }
});
