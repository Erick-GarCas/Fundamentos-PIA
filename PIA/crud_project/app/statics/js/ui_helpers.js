/*
  ui_helpers.js

  Manual de usuario (comentarios en español):

  Propósito general:
  - Proveer utilidades de interfaz de usuario ligeras para la parte pública y
    las páginas de autenticación: modo oscuro, ajuste de tamaño de fuente y
    controles de accesibilidad flotantes.

  Comportamiento principal:
  - Persistencia: el tamaño de fuente preferido se guarda en `localStorage` bajo
    la clave `prefFontSize` para restaurarlo en cargas posteriores.
  - Dark mode: el script expone `window.toggleDark()` para alternar el modo oscuro
    (aplica la clase `dark` al `body`). Inicialmente el modo claro se asume por defecto.
  - Accesibilidad flotante: permite mostrar/ocultar controles (p. ej. aumentar texto)
    mediante un widget flotante en pantallas pequeñas.

  Selectores esperados (DOM):
  - `#btn-toggle-dark` : botón que refleja el estado del modo oscuro (aria-pressed).
  - `#floating-accessibility` o `.floating-accessibility`: contenedor del widget flotante.
  - `#floating-toggle` : botón que abre/cierra el widget flotante.

  API pública añadida al `window`:
  - `window.toggleDark()`         : alterna el modo oscuro.
  - `window.increaseText()`       : aumenta el tamaño base de fuente en 2px.
  - `window.decreaseText()`       : disminuye el tamaño base de fuente en 2px.
  - `window.toggleFloatingAccessibility()` : muestra/oculta el widget flotante.

  Consideraciones de accesibilidad:
  - Los botones usan atributos ARIA (`aria-pressed`, `aria-expanded`) para reflejar
    el estado y mejorar la experiencia de lectores de pantalla.
  - Las preferencias de usuario se respetan al restaurar el tamaño de fuente.

  NOTA: Las validaciones de accesibilidad y seguridad deben complementarse en el
  servidor/markup si hace falta; este archivo solo controla comportamientos y
  apariencia del cliente.
*/

(function(){
    // Clave de localStorage para persistir el tamaño de fuente.
    const LS_FONTSIZE = 'prefFontSize';

    // Estado interno del modo oscuro (booleano). No representa por sí solo
    // si el sistema está en dark mode; es el estado controlado por la app.
    let darkState = false;

    /*
      applyDark(on)
      - Activa o desactiva el modo oscuro en el `body`.
      - Actualiza el botón `#btn-toggle-dark` si existe, aplicando clases y
        atributos ARIA para reflejar el estado.
    */
    function applyDark(on){
        darkState = !!on;
        if(on) document.body.classList.add('dark');
        else document.body.classList.remove('dark');
        const btn = document.getElementById('btn-toggle-dark');
        if(btn){
            btn.setAttribute('aria-pressed', on ? 'true' : 'false');
            btn.classList.toggle('is-dark', on);
        }
    }

    // toggleDark(): expone la funcionalidad de alternar el modo oscuro.
    function toggleDark(){
        const isDark = !darkState;
        applyDark(isDark);
    }

    /*
      changeTextSize(delta)
      - Aumenta/disminuye el tamaño base de la fuente del documento.
      - `delta` puede ser positivo o negativo; el valor resultante se restringe
        entre 12px y 28px para mantener legibilidad y evitar roturas de diseño.
      - Persiste la preferencia en localStorage cuando sea posible.
    */
    function changeTextSize(delta){
        const el = document.documentElement;
        const style = window.getComputedStyle(el).getPropertyValue('font-size');
        const current = parseFloat(style) || 16;
        const next = Math.max(12, Math.min(28, current + delta)); // limitar entre 12 y 28px
        el.style.fontSize = next + 'px';
        try{ localStorage.setItem(LS_FONTSIZE, String(next)); }catch(e){}
    }

    // restorePrefs(): aplica las preferencias guardadas al cargar la página.
    function restorePrefs(){
        // Por defecto arrancamos en modo claro; el usuario puede activar el oscuro.
        applyDark(false);
        try{
            const fs = localStorage.getItem(LS_FONTSIZE);
            if(fs){ document.documentElement.style.fontSize = parseFloat(fs) + 'px'; }
        }catch(e){}
    }

    // Exponer funciones útiles en `window` para que puedan ser llamadas desde HTML.
    window.toggleDark = toggleDark;
    window.increaseText = function(){ changeTextSize(2); };
    window.decreaseText = function(){ changeTextSize(-2); };

    /*
      toggleFloatingAccessibility()
      - Abre/cierra el widget flotante de accesibilidad (útil en móvil).
      - Busca `#floating-accessibility` o `.floating-accessibility` y alterna la
        clase `expanded`. También actualiza `aria-expanded` en el toggle.
    */
    function toggleFloatingAccessibility(){
        const el = document.getElementById('floating-accessibility') || document.querySelector('.floating-accessibility');
        if(!el) return;
        const expanded = el.classList.toggle('expanded');
        const t = document.getElementById('floating-toggle');
        if(t) t.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }
    window.toggleFloatingAccessibility = toggleFloatingAccessibility;

    // Inicializaciones que deben correrse cuando el DOM esté listo.
    document.addEventListener('DOMContentLoaded', function(){
        restorePrefs();
        // Reflejar el estado en el botón si existe.
        const btn = document.getElementById('btn-toggle-dark');
        if(btn){
            btn.setAttribute('aria-pressed', document.body.classList.contains('dark') ? 'true' : 'false');
        }
        // Inicializar el toggle flotante si existe el markup correspondiente.
        const toggle = document.getElementById('floating-toggle');
        const container = document.getElementById('floating-accessibility') || document.querySelector('.floating-accessibility');
        if(toggle && container){
            // Evitar que el click burbujee y active otros manejadores.
            toggle.addEventListener('click', function(e){
                e.stopPropagation();
                toggleFloatingAccessibility();
            });
            // Cerrar el widget al hacer click fuera del contenedor.
            document.addEventListener('click', function(ev){
                if(!container.classList.contains('expanded')) return;
                if(!container.contains(ev.target)){
                    container.classList.remove('expanded');
                    toggle.setAttribute('aria-expanded','false');
                }
            }, { passive: true });
        }
    });
})();
