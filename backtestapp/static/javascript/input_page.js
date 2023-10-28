document.addEventListener('DOMContentLoaded', function () {
    let form = document.getElementById('backtesting-form');

    form.addEventListener('submit', function (event) {
        let fechaDesde = new Date(document.getElementById('id_fechaDesde').value);
        let fechaHasta = new Date(document.getElementById('id_fechaHasta').value);
        let valorTK = parseFloat(document.getElementById('id_valorTK').value);
        let minDate = new Date('2023-05-01');
        let maxDate = new Date('2023-09-30');
        let processingMessage = document.getElementById('processing-message');

        dataValidate(fechaDesde, fechaHasta, valorTK, minDate, maxDate, processingMessage);

    });

});

function showError(message) {
    let errorMessage = document.getElementById('error-message');
    errorMessage.innerHTML = message;
    errorMessage.style.display = 'block';
}

function dataValidate(fechaDesde, fechaHasta, valorTK, minDate, maxDate, processingMessage) {
    if (fechaDesde === fechaHasta) {
        event.preventDefault();
        showError('Las fechas no pueden ser iguales. Por favor, cambie las fechas.');
    } else if (fechaDesde > fechaHasta) {
        event.preventDefault();
        showError('La fecha de inicio no puede ser mayor que la fecha de fin. Por favor, selecciona fechas válidas.');
    } else if (fechaDesde < minDate || fechaHasta > maxDate) {
        event.preventDefault();
        showError('No hay datos disponibles para las fechas ingresadas. Por favor, cambie las fechas.');
    } else if (valorTK < 0) {
        event.preventDefault();
        showError('El valor de valorTK no puede ser negativo. Por favor, ingresa un valor válido.');
    } else {
        processingMessage.style.display = 'flex';
    }
}









