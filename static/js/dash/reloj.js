(function fechaHora() {
    const reloj = document.getElementById("reloj");
    const fechaCompleta = document.getElementById("fechaCompleta"); // Nuevo elemento para la fecha completa

    function actualizarHoraYFecha() {
        const fechaActual = new Date();

        // Hora
        const hora = fechaActual.getHours().toString().padStart(2, '0');
        const minuto = fechaActual.getMinutes().toString().padStart(2, '0');
        const segundo = fechaActual.getSeconds().toString().padStart(2, '0');

        // Fecha
        const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
        const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
        const diaSemana = diasSemana[fechaActual.getDay()];
        const dia = fechaActual.getDate();
        const mes = meses[fechaActual.getMonth()];
        const año = fechaActual.getFullYear();

        // Formato ej.:  "Viernes, 9 de agosto de 2024"
        const fechaCompletaStr = `${diaSemana}, ${dia} de ${mes} de ${año}`;

        reloj.textContent = `${hora}:${minuto}:${segundo}`;
        fechaCompleta.textContent = fechaCompletaStr;
    }

    actualizarHoraYFecha();
    setInterval(actualizarHoraYFecha, 1000);
})();
