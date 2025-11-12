// main.js - controla renderizado dinámico, validaciones y cotizador
(function(){
    // Cargaremos los tratamientos desde el backend (DB) vía fetch.
    // El arreglo quedará vacío hasta que se carguen los datos desde /api/tratamientos/.
    let tratamientos = [];
    const TREATMENTS_PER_PAGE = 4;
    let tratamientoPages = [];
    let currentTratamientoPage = 0;

    function updateTratamientosSlider(){
        const track = document.getElementById('tratamientos-list');
        const dots = document.getElementById('tratamientos-dots');
        const prev = document.getElementById('tratamientos-prev');
        const next = document.getElementById('tratamientos-next');
        if(!track || !tratamientoPages.length){
            if(prev) prev.disabled = true;
            if(next) next.disabled = true;
            return;
        }
        track.style.transform = `translateX(-${currentTratamientoPage * 100}%)`;
        if(prev){ prev.disabled = tratamientoPages.length <= 1; }
        if(next){ next.disabled = tratamientoPages.length <= 1; }
        if(dots){
            Array.from(dots.children).forEach((dot, idx) => {
                dot.classList.toggle('active', idx === currentTratamientoPage);
            });
        }
    }

    function bindSliderButtons(){
        const prev = document.getElementById('tratamientos-prev');
        const next = document.getElementById('tratamientos-next');
        if(prev && !prev.dataset.bound){
            prev.addEventListener('click', function(){
                if(currentTratamientoPage > 0){
                    currentTratamientoPage--;
                    updateTratamientosSlider();
                }
            });
            prev.dataset.bound = '1';
        }
        if(next && !next.dataset.bound){
            next.addEventListener('click', function(){
                if(currentTratamientoPage < tratamientoPages.length - 1){
                    currentTratamientoPage++;
                    updateTratamientosSlider();
                }
            });
            next.dataset.bound = '1';
        }
    }

    // Render servicios en la sección principal
    // Renderiza los tratamientos como tarjetas y crea opciones para el cotizador
    function renderTratamientos(){
        const container = document.getElementById('tratamientos-list');
        const select = document.getElementById('tratamiento-select');
        const dots = document.getElementById('tratamientos-dots');
        const counter = document.getElementById('tratamientos-count');
        if(!container || !select){
            return;
        }

        container.innerHTML = '';
        tratamientoPages = [];
        currentTratamientoPage = 0;

        select.innerHTML = '';
        const optDefault = document.createElement('option');
        optDefault.value = '';
        optDefault.textContent = '-- Selecciona un tratamiento --';
        select.appendChild(optDefault);

        tratamientos.forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.nombre} — ${t.precioTexto || (t.precio ? '$' + t.precio : '')}`;
            select.appendChild(opt);
        });

        for(let i = 0; i < tratamientos.length; i += TREATMENTS_PER_PAGE){
            tratamientoPages.push(tratamientos.slice(i, i + TREATMENTS_PER_PAGE));
        }
        if(!tratamientoPages.length){
            tratamientoPages.push([]);
        }

        tratamientoPages.forEach(chunk => {
            const page = document.createElement('div');
            page.className = 'slider-page';
            const row = document.createElement('div');
            row.className = 'row g-3';
            chunk.forEach(t => {
                const col = document.createElement('div');
                col.className = 'col-12 col-md-6 col-xl-3';
                const imgHtml = t.imagen ? `<img src="${t.imagen}" class="card-img-top" alt="${t.nombre}">` : '';
                const features = Array.isArray(t.caracteristicas) ? t.caracteristicas.join(' · ') : (t.caracteristicas || '');
                col.innerHTML = `
                    <div class="card h-100">
                        ${imgHtml}
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${t.nombre}</h5>
                            <p class="card-text">${t.descripcion || ''}</p>
                            <p class="mt-auto"><strong>${t.precioTexto || (t.precio ? '$' + t.precio : '')}</strong></p>
                            <p class="service-features">${features}</p>
                            <div class="mt-2">
                                <button class="btn btn-outline-primary btn-sm btn-cotizar" data-id="${t.id}">Cotizar</button>
                                <button class="btn btn-primary btn-sm ms-2 btn-agendar" type="button">Agendar</button>
                            </div>
                        </div>
                    </div>
                `;
                row.appendChild(col);
            });
            page.appendChild(row);
            container.appendChild(page);
        });

        if(counter){
            counter.textContent = tratamientos.length ? `${tratamientos.length} tratamientos disponibles` : 'Sin tratamientos registrados';
        }

        if(dots){
            dots.innerHTML = '';
        tratamientoPages.forEach((_, idx) => {
                const dot = document.createElement('button');
                dot.type = 'button';
                dot.addEventListener('click', () => {
                    currentTratamientoPage = idx;
                    updateTratamientosSlider();
                });
                dots.appendChild(dot);
            });
        }

        bindSliderButtons();
        updateTratamientosSlider();

        Array.from(document.querySelectorAll('.btn-cotizar')).forEach(btn => {
            btn.addEventListener('click', function(){
                const id = this.dataset.id;
                const sel = document.getElementById('tratamiento-select');
                sel.value = id;
                document.getElementById('cotizacion').scrollIntoView({behavior:'smooth'});
            });
        });

        Array.from(document.querySelectorAll('.btn-agendar')).forEach(btn => {
            btn.addEventListener('click', function(){
                const contacto = document.getElementById('contacto');
                if(contacto){
                    contacto.scrollIntoView({behavior:'smooth'});
                }
            });
        });
    }

    // Cotizador
    // Cotizador: ahora trabaja con un select (un solo tratamiento seleccionado)
    function setupCotizador(){
        const form = document.getElementById('form-cotizacion');
        const output = document.getElementById('cotizacion-output');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            const selectedId = parseInt(document.getElementById('tratamiento-select').value);
            if(!selectedId){
                alert('Seleccione un tratamiento para cotizar.');
                return;
            }
            const tratamiento = tratamientos.find(t=>t.id===selectedId);
            if(!tratamiento){
                alert('Tratamiento no encontrado.');
                return;
            }
            const cantidad = parseInt(document.getElementById('cantidad').value) || 1;
            const descuento = parseInt(document.querySelector('input[name=descuento]:checked').value) || 0;
            // Usar precio base (promedio) para cálculo — es más representativo del valor real
            const precioUnitario = tratamiento.precio;
            const subtotal = precioUnitario * cantidad;
            const ahorro = subtotal * (descuento/100);
            const totalConDesc = subtotal - ahorro;

            // Mostrar detalles en pantalla
            const detalles = `\n                <p><strong>Tratamiento:</strong> ${tratamiento.nombre}</p>\n                <p><strong>Precio unitario (base):</strong> $${precioUnitario.toFixed(2)} MXN</p>\n                <p><strong>Rango estimado:</strong> ${tratamiento.precioTexto}</p>\n                <p><strong>Cantidad/unidades:</strong> ${cantidad}</p>\n                <p><strong>Subtotal:</strong> $${subtotal.toFixed(2)} MXN</p>\n                <p><strong>Descuento aplicado:</strong> ${descuento}% ( - $${ahorro.toFixed(2)} MXN )</p>\n                <h4>El costo total estimado es: $${totalConDesc.toFixed(2)} MXN</h4>\n            `;
            output.innerHTML = detalles;
            // Mensaje adicional en alerta para visibilidad inmediata
            alert('Cotización: $' + totalConDesc.toFixed(2) + ' MXN (ver detalles en la sección de cotización)');
        });
    }

    // Solicitud de cita (vinculada a CitaDental)
    // - Renderiza checkboxes de tratamientos (desde `tratamientos`)
    // - Permite seleccionar hasta 2 tratamientos
    // - Valida que no haya otra cita a la misma hora (comparando año/mes/día/hora)
    // - Guarda la cita en localStorage bajo la clave 'citas' (simulación de backend)
    function setupAppointmentForm(){
        const form = document.getElementById('appointment-form');
        if(!form) return;
        const alertBox = document.getElementById('contact-alert');
        const checkboxesContainer = document.getElementById('tratamientos-checkboxes');
        const emailInput = document.getElementById('correo');
        const dateInput = document.getElementById('fecha-dia');
        const timeInput = document.getElementById('hora-cita');
        const hiddenDatetime = document.getElementById('fecha-cita');
        if(!checkboxesContainer) return;

        // Render checkboxes
        checkboxesContainer.innerHTML = '';
        tratamientos.forEach(t => {
            const id = 'tchk-' + t.id;
            const wrapper = document.createElement('div');
            wrapper.className = 'form-check';
            wrapper.innerHTML = `\n                <input class="form-check-input" type="checkbox" value="${t.id}" id="${id}" name="tratamiento[]">\n                <label class="form-check-label" for="${id}">${t.nombre} <small class="text-muted">(${t.precioTexto})</small></label>\n            `;
            checkboxesContainer.appendChild(wrapper);
        });

        // Enforce max 2 checkboxes selected
        checkboxesContainer.addEventListener('change', function(e){
            const checked = checkboxesContainer.querySelectorAll('input[type=checkbox]:checked');
            if(checked.length > 2){
                // undo last change
                e.target.checked = false;
                alert('Solo puedes seleccionar hasta 2 tratamientos por solicitud.');
            }
        });

        const phoneRegex = /^[0-9]{7,15}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        form.addEventListener('submit', function(e){
            // Perform client-side validation but allow the form to submit traditionally to the server.
            if(alertBox){
                alertBox.style.display = 'none';
            }
            const nombre = document.getElementById('nombre').value.trim();
            const telefono = document.getElementById('telefono').value.trim();
            const correo = emailInput ? emailInput.value.trim() : '';
            const fechaDia = dateInput ? dateInput.value : '';
            const horaVal = timeInput ? timeInput.value : '';
            const fechaVal = (fechaDia && horaVal) ? `${fechaDia}T${horaVal}` : '';
            if(hiddenDatetime){
                hiddenDatetime.value = fechaVal;
            }
            const selected = Array.from(checkboxesContainer.querySelectorAll('input[type=checkbox]:checked')).map(i=>parseInt(i.value));

            if(!nombre){
                e.preventDefault();
                showAlert('Por favor ingrese su nombre.', 'danger');
                return;
            }
            if(!telefono || !phoneRegex.test(telefono)){
                e.preventDefault();
                showAlert('Ingrese un telefono valido (7-15 digitos).', 'danger');
                return;
            }
            if(selected.length === 0){
                e.preventDefault();
                showAlert('Seleccione al menos un tratamiento (max. 2).', 'danger');
                return;
            }
            if(!fechaDia || !horaVal){
                e.preventDefault();
                showAlert('Seleccione fecha y hora para la cita.', 'danger');
                return;
            }
            if(correo && !emailRegex.test(correo)){
                e.preventDefault();
                showAlert('Ingrese un correo valido.', 'danger');
                return;
            }

            // Parse datetime-local to JS Date (assume local timezone)
            const fecha = new Date(fechaVal);
            if(isNaN(fecha.getTime())){
                e.preventDefault();
                showAlert('Fecha invalida.', 'danger');
                return;
            }

            // No localStorage save anymore - submission will be handled server-side.
            // Optionally, we could disable the submit button here to avoid double submits.
            // Allow the form to submit normally to Django view which will perform server-side checks.
        });

        function showAlert(msg, type){
            if(alertBox){
                alertBox.style.display = 'block';
                alertBox.className = 'alert alert-' + type;
                alertBox.textContent = msg;
            }else{
                alert(msg);
            }
        }
    }

    // Galería simple
    function renderGaleria(){
        const grid = document.getElementById('galeria-grid');
        // Use local images from assets/img for the gallery carousel
        // Only use images that start with 'equipo' or 'instalaciones'
        // Usar rutas absolutas al static para evitar problemas de resolución
        const urls = [
            '/static/img/equipo1.png',
            '/static/img/equipo2.png',
            '/static/img/equipo3.png',
            '/static/img/instalaciones1.png',
            '/static/img/instalaciones2.png',
            '/static/img/instalaciones3.png',
            '/static/img/instalaciones4.png'
        ];

        const indicators = document.getElementById('galeria-indicators');
        grid.innerHTML = '';
        indicators.innerHTML = '';

        urls.forEach((u, idx) => {
            const item = document.createElement('div');
            item.className = 'carousel-item' + (idx === 0 ? ' active' : '');
            item.innerHTML = `
                <img src="${u}" class="gallery-img d-block w-100" loading="lazy" alt="Galería ${idx+1}">
            `;
            grid.appendChild(item);

            // indicators (bootstrap 5 expects buttons inside .carousel-indicators)
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.setAttribute('data-bs-target', '#galleryCarousel');
            btn.setAttribute('data-bs-slide-to', String(idx));
            if(idx === 0){
                btn.className = 'active';
                btn.setAttribute('aria-current', 'true');
            }
            btn.setAttribute('aria-label', 'Slide ' + (idx+1));
            indicators.appendChild(btn);
        });

        // Initialize carousel with autoplay and pause on hover
        try{
            const carouselEl = document.getElementById('galleryCarousel');
            if(window.bootstrap && carouselEl){
                // destroy previous instance if exists
                const existingInstance = bootstrap.Carousel.getInstance(carouselEl);
                if(existingInstance){
                    existingInstance.dispose();
                }
                // Create new carousel instance with autoplay
                const bsCarousel = new bootstrap.Carousel(carouselEl, { 
                    interval: 3000, 
                    ride: 'carousel',
                    pause: 'hover', 
                    wrap: true 
                });
            }
        }catch(err){
            console.warn('Carousel init failed', err);
        }
    }

    // Testimonios
    function renderTestimonios(){
        const data = [
            {nombre:'Laura M.', texto:'Excelente servicio, muy profesional.', rating:5, foto:'https://i.pravatar.cc/100?img=12'},
            {nombre:'Carlos G.', texto:'Me atendieron rápido y el tratamiento fue efectivo.', rating:4, foto:'https://i.pravatar.cc/100?img=5'},
            {nombre:'Ana P.', texto:'Ambiente agradable y personal amable.', rating:5, foto:'https://i.pravatar.cc/100?img=20'}
        ];
        const cont = document.getElementById('testimonios-list');
        cont.innerHTML = '';
        data.forEach((t, idx) => {
            const item = document.createElement('div');
            item.className = 'carousel-item' + (idx===0 ? ' active' : '');
            item.innerHTML = `
                <div class="d-flex justify-content-center">
                    <div class="card p-3" style="max-width:720px;">
                        <div class="d-flex align-items-center mb-2">
                            <img src="${t.foto}" class="rounded-circle me-3" width="64" height="64" alt="foto">
                            <div>
                                <strong>${t.nombre}</strong>
                                <div class="testimonial-star">${'★'.repeat(t.rating)}${'☆'.repeat(5-t.rating)}</div>
                            </div>
                        </div>
                        <p class="mb-0">${t.texto}</p>
                    </div>
                </div>
            `;
            cont.appendChild(item);
        });
    }

    // Toggle modo oscuro y login (simulación)
    function setupUI(){
        const btnDark = document.getElementById('btn-toggle-dark');
        const logoImg = document.querySelector('.site-logo');

        const syncThemeState = () => {
            const isDark = document.body.classList.contains('dark');
            btnDark && btnDark.setAttribute('aria-pressed', isDark ? 'true' : 'false');
            const icon = btnDark ? btnDark.querySelector('i') : null;
            if(icon){
                icon.classList.remove('bi-moon-fill', 'bi-sun-fill');
                icon.classList.add(isDark ? 'bi-sun-fill' : 'bi-moon-fill');
            }
            if(logoImg){
                logoImg.src = isDark ? '/static/img/logo-blanco.png' : '/static/img/logo-negro.png';
                logoImg.alt = isDark ? 'Clinica Dental Vitaldent logo blanco' : 'Clinica Dental Vitaldent logo oscuro';
            }
        };

        btnDark && btnDark.addEventListener('click', function(){
            if(typeof window.toggleDark === 'function'){
                window.toggleDark();
            }else{
                const isDark = document.body.classList.toggle('dark');
                try{
                    localStorage.setItem('prefersDarkMode', isDark ? '1' : '0');
                }catch(err){}
            }
            syncThemeState();
        });

        syncThemeState();
    }

    // Scroll spy ligero para resaltar la sección activa en la navegación
    function setupNavScrollHighlight(){
        const navLinks = document.querySelectorAll('.site-nav a');
        if(!navLinks.length) return;

        const linkMap = new Map();
        navLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            const key = href.startsWith('#') && href.length > 1 ? href.substring(1) : 'inicio';
            linkMap.set(key, link);
        });

        const sections = [];
        const hero = document.querySelector('.hero');
        if(hero){ sections.push({key:'inicio', el: hero}); }

        document.querySelectorAll('main section[id]').forEach(section => {
            if(linkMap.has(section.id)){
                sections.push({key: section.id, el: section});
            }
        });

        const footer = document.getElementById('contacto');
        if(footer && linkMap.has('contacto')){
            sections.push({key:'contacto', el: footer});
        }

        if(!sections.length) return;

        let lastActive = null;
        const setActive = (key) => {
            if(key === lastActive) return;
            navLinks.forEach(link => link.classList.remove('active'));
            const targetLink = linkMap.get(key) || linkMap.get('inicio');
            targetLink && targetLink.classList.add('active');
            lastActive = key;
        };

        const updateActive = () => {
            const scrollPos = window.scrollY + 160; // compensa header fijo
            let current = 'inicio';
            sections.forEach(({key, el}) => {
                if(scrollPos >= el.offsetTop - 40){
                    current = key;
                }
            });
            setActive(current);
        };

        updateActive();
        window.addEventListener('scroll', updateActive, {passive:true});
        window.addEventListener('resize', updateActive);
    }

    // Cargar tratamientos desde el backend y luego inicializar la app
    async function loadTratamientosAndInit(){
        try{
            const resp = await fetch('/api/tratamientos/');
            if(resp.ok){
                const data = await resp.json();
                // normalize precios (ya vienen como number desde el servidor)
                tratamientos = Array.isArray(data) ? data : [];
            }else{
                tratamientos = [];
            }
        }catch(err){
            console.warn('No se pudieron cargar los tratamientos:', err);
            tratamientos = [];
        }

        // Inicializar componentes que dependen de tratamientos
        renderTratamientos();
        setupCotizador();
        setupAppointmentForm();

        // Inicializaciones independientes
        renderGaleria();
        renderTestimonios();
        setupUI();
        setupNavScrollHighlight();
    }

    document.addEventListener('DOMContentLoaded', loadTratamientosAndInit);

})();
