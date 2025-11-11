// ui_helpers.js
// Funciones sencillas de UI: modo oscuro, cambiar tamaño de texto y accesibilidad.
(function(){
    // Improved UI helpers: persist dark mode and font size in localStorage
    const LS_DARK = 'prefersDarkMode';
    const LS_FONTSIZE = 'prefFontSize';

    function applyDark(on){
        if(on) document.body.classList.add('dark');
        else document.body.classList.remove('dark');
        // update toggle button pressed state if present
        const btn = document.getElementById('btn-toggle-dark');
        if(btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    }

    function toggleDark(){
        const isDark = document.body.classList.toggle('dark');
        localStorage.setItem(LS_DARK, isDark ? '1' : '0');
        const btn = document.getElementById('btn-toggle-dark');
        if(btn) btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    }

    function changeTextSize(delta){
        const el = document.documentElement;
        const style = window.getComputedStyle(el).getPropertyValue('font-size');
        const current = parseFloat(style) || 16;
        const next = Math.max(12, Math.min(28, current + delta)); // clamp
        el.style.fontSize = next + 'px';
        try{ localStorage.setItem(LS_FONTSIZE, String(next)); }catch(e){}
    }

    // restore preferences on load
    function restorePrefs(){
        try{
            const d = localStorage.getItem(LS_DARK);
            if(d === '1') applyDark(true);
        }catch(e){}
        try{
            const fs = localStorage.getItem(LS_FONTSIZE);
            if(fs){ document.documentElement.style.fontSize = parseFloat(fs) + 'px'; }
        }catch(e){}
    }

    window.toggleDark = toggleDark;
    window.increaseText = function(){ changeTextSize(2); };
    window.decreaseText = function(){ changeTextSize(-2); };

    // Floating accessibility toggle (for mobile): shows/hides the floating controls
    function toggleFloatingAccessibility(){
        const el = document.getElementById('floating-accessibility') || document.querySelector('.floating-accessibility');
        if(!el) return;
        const expanded = el.classList.toggle('expanded');
        const t = document.getElementById('floating-toggle');
        if(t) t.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }
    window.toggleFloatingAccessibility = toggleFloatingAccessibility;

    // expose restore to run on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function(){
        restorePrefs();
        // reflect state to button if present
        const btn = document.getElementById('btn-toggle-dark');
        if(btn){
            btn.setAttribute('aria-pressed', document.body.classList.contains('dark') ? 'true' : 'false');
        }
        // init floating accessibility toggle if present
        const toggle = document.getElementById('floating-toggle');
        const container = document.getElementById('floating-accessibility') || document.querySelector('.floating-accessibility');
        if(toggle && container){
            toggle.addEventListener('click', function(e){
                e.stopPropagation();
                toggleFloatingAccessibility();
            });
            // close when clicking outside
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
