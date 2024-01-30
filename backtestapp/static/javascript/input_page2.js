
document.addEventListener('DOMContentLoaded', function () {
    let form = document.getElementById('backtesting-form');

    form.addEventListener('submit', function (event) {
        let fechaDesde = new Date(document.getElementById('id_fechaDesde').value + 'T00:00:00').getTime();
        let fechaHasta = new Date(document.getElementById('id_fechaHasta').value + 'T00:00:00').getTime();
        let valorTK = parseFloat(document.getElementById('id_valorTK').value);
        let stopLoss = parseFloat(document.getElementById('id_stopLoss').value);
        let minDate = new Date('2023-01-03' + 'T00:00:00').getTime();
        let maxDate = new Date('2023-12-14' + 'T00:00:00').getTime();
        let processingMessage = document.getElementById('processing-message');

        dataValidate(fechaDesde, fechaHasta, valorTK,stopLoss, minDate, maxDate, processingMessage);

    });

});

function showError(message) {
    let errorMessage = document.getElementById('error-message');
    errorMessage.innerHTML = message;
    errorMessage.style.display = 'block';
}

function dataValidate(fechaDesde, fechaHasta, valorTK,stopLoss, minDate, maxDate, processingMessage) {
    if (fechaDesde === fechaHasta) {
        event.preventDefault();
        showError('Las fechas no pueden ser iguales. Por favor, cambie las fechas.');
    } else if (fechaDesde> fechaHasta) {
        event.preventDefault();
        showError('La fecha de inicio no puede ser mayor que la fecha de fin. Por favor, selecciona fechas válidas.');
    
    } else if (fechaDesde < minDate || fechaHasta > maxDate) {
        event.preventDefault();
        showError('No hay datos disponibles para las fechas ingresadas. Por favor, cambie las fechas.');
    } else if (valorTK <= 0 || valorTK === 0) {
        event.preventDefault();
        showError('El valor de valorTK debe ser mayor a cero. Por favor, ingresa un valor válido.');
    } else if (stopLoss <= 0) {
        event.preventDefault();
        showError('El valor de Stop Loss debe ser mayor a cero. Por favor, ingresa un valor válido.');
    } else {
        processingMessage.style.display = 'flex';
    }
}









