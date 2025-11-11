// ui_helpers.js
// Funciones sencillas de UI: modo oscuro, cambiar tamaño de texto y accesibilidad.
(function(){
    function toggleDark(){
        document.body.classList.toggle('dark');
    }

    function changeTextSize(delta){
        const el = document.documentElement;
        const style = window.getComputedStyle(el).getPropertyValue('font-size');
        const current = parseFloat(style) || 16;
        el.style.fontSize = (current + delta) + 'px';
    }

    // Exponer funciones globalmente para uso directo en plantillas
    window.toggleDark = toggleDark;
    window.increaseText = function(){ changeTextSize(2); };
    window.decreaseText = function(){ changeTextSize(-2); };
})();
