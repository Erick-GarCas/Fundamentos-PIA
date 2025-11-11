// main.js - controla renderizado dinámico, validaciones y cotizador
(function(){
    // Datos de ejemplo para tratamientos (simulan conexión a BD)
    // Cada tratamiento incluye precioMin, precioMax y precio (valor base = promedio) y precioTexto para mostrar rango.
    const tratamientos = [
        {id:1, nombre:'Limpieza Dental Profesional (Profilaxis)', descripcion:'Eliminación de placa y sarro mediante ultrasonido y pulido para prevenir caries y enfermedades de las encías.', precioMin:600, precioMax:900, precio: (600+900)/2, precioTexto: '$600 - $900 MXN', caracteristicas:['Profilaxis','Ultrasonido'], imagen:'https://images.unsplash.com/photo-1588774069159-1e0b03f1d0f4?q=80&w=800&auto=format&fit=crop'},
        {id:2, nombre:'Blanqueamiento Dental', descripcion:'Aclara el color de los dientes mediante geles con peróxido y luz LED.', precioMin:1800, precioMax:2800, precio: (1800+2800)/2, precioTexto: '$1,800 - $2,800 MXN', caracteristicas:['Estético','1 sesión aprox.'], imagen:'https://images.unsplash.com/photo-1548095115-45697e9cf02b?q=80&w=800&auto=format&fit=crop'},
        {id:3, nombre:'Resinas / Empastes Estéticos', descripcion:'Restauraciones con resina del color del diente para devolver forma y función.', precioMin:900, precioMax:1500, precio: (900+1500)/2, precioTexto: '$900 - $1,500 MXN', caracteristicas:['Estético','Durable'], imagen:'https://images.unsplash.com/photo-1588776814546-89ef3b9f1f16?q=80&w=800&auto=format&fit=crop'},
        {id:4, nombre:'Ortodoncia (Brackets o Alineadores)', descripcion:'Corrección de alineación dental mediante brackets o alineadores transparentes.', precioMin:15000, precioMax:35000, precio: (15000+35000)/2, precioTexto: '$15,000 - $35,000 MXN', caracteristicas:['Largo plazo','Plan personalizado'], imagen:'https://images.unsplash.com/photo-1571799008301-5a4d48a1f8f6?q=80&w=800&auto=format&fit=crop'},
        {id:5, nombre:'Extracción Dental', descripcion:'Procedimiento para remover dientes dañados o muelas del juicio.', precioMin:700, precioMax:1800, precio: (700+1800)/2, precioTexto: '$700 - $1,800 MXN', caracteristicas:['Ambulatorio','Anestesia local'], imagen:'https://images.unsplash.com/photo-1606813902843-2f9f2f19c6c4?q=80&w=800&auto=format&fit=crop'},
    {id:6, nombre:'Endodoncia (Tratamiento de Conducto)', descripcion:'Eliminación del nervio dental afectado para preservar el diente.', precioMin:2000, precioMax:3500, precio: (2000+3500)/2, precioTexto: '$2,000 - $3,500 MXN', caracteristicas:['Técnico','Recuperación'], imagen:'https://images.unsplash.com/photo-1597764691519-9d6a6ccd0b2b?q=80&w=800&auto=format&fit=crop'},
        {id:7, nombre:'Carillas Dentales (Veneers)', descripcion:'Láminas estéticas de porcelana o resina para mejorar la apariencia dental.', precioMin:4000, precioMax:6000, precio: (4000+6000)/2, precioTexto: '$4,000 - $6,000 MXN por pieza', caracteristicas:['Estético','Por pieza'], imagen:'https://images.unsplash.com/photo-1587613865766-4f33f8a97f0f?q=80&w=800&auto=format&fit=crop'},
        {id:8, nombre:'Implantes Dentales', descripcion:'Sustitución de dientes perdidos mediante implante de titanio y corona.', precioMin:10000, precioMax:18000, precio: (10000+18000)/2, precioTexto: '$10,000 - $18,000 MXN', caracteristicas:['Rehabilitación','Duradero'], imagen:'https://images.unsplash.com/photo-1582719478250-6f4b7b6b2d3b?q=80&w=800&auto=format&fit=crop'},
        {id:9, nombre:'Coronas y Puentes', descripcion:'Rehabilitación mediante fundas o puentes fijos de porcelana o zirconia.', precioMin:3000, precioMax:5000, precio: (3000+5000)/2, precioTexto: '$3,000 - $5,000 MXN', caracteristicas:['Rehabilitación','Estético'], imagen:'https://images.unsplash.com/photo-1588776814546-89ef3b9f1f16?q=80&w=800&auto=format&fit=crop'},
        {id:10, nombre:'Odontopediatría', descripcion:'Servicios dentales especializados para niños: limpiezas, selladores y orientación.', precioMin:500, precioMax:1200, precio: (500+1200)/2, precioTexto: '$500 - $1,200 MXN', caracteristicas:['Infantil','Preventivo'], imagen:'https://images.unsplash.com/photo-1543852786-1cf6624b9987?q=80&w=800&auto=format&fit=crop'},
        {id:11, nombre:'Periodoncia', descripcion:'Tratamientos para encías y estructuras de soporte: raspado y alisado radicular.', precioMin:1500, precioMax:2500, precio: (1500+2500)/2, precioTexto: '$1,500 - $2,500 MXN', caracteristicas:['Encías','Especializado'], imagen:'https://images.unsplash.com/photo-1556228720-5f0f1b0b8e6d?q=80&w=800&auto=format&fit=crop'},
        {id:12, nombre:'Diagnóstico Digital y Radiografías', descripcion:'Evaluaciones mediante radiografías panorámicas o periapicales.', precioMin:300, precioMax:600, precio: (300+600)/2, precioTexto: '$300 - $600 MXN', caracteristicas:['Diagnóstico','Imágenes digitales'], imagen:'https://images.unsplash.com/photo-1588774069159-1e0b03f1d0f4?q=80&w=800&auto=format&fit=crop'},
        {id:13, nombre:'Urgencias Dentales', descripcion:'Atención inmediata a fracturas, dolor agudo o infecciones.', precioMin:800, precioMax:1200, precio: (800+1200)/2, precioTexto: '$800 - $1,200 MXN', caracteristicas:['24/7','Urgente'], imagen:'https://images.unsplash.com/photo-1582719478250-6f4b7b6b2d3b?q=80&w=800&auto=format&fit=crop'},
        {id:14, nombre:'Revisiones Generales', descripcion:'Consulta de valoración inicial con diagnóstico y plan de tratamiento.', precioMin:500, precioMax:800, precio: (500+800)/2, precioTexto: '$500 - $800 MXN', caracteristicas:['Valoración','Plan personalizado'], imagen:'https://images.unsplash.com/photo-1567016584419-2b8c14f4d3f5?q=80&w=800&auto=format&fit=crop'
        }
    ];

    // Render servicios en la sección principal
    // Renderiza los tratamientos como tarjetas y crea opciones para el cotizador
    function renderTratamientos(){
        const container = document.getElementById('tratamientos-list');
        const select = document.getElementById('tratamiento-select');
        container.innerHTML = '';
        select.innerHTML = '';
        // opción por defecto
        const optDefault = document.createElement('option');
        optDefault.value = '';
        optDefault.textContent = '-- Selecciona un tratamiento --';
        select.appendChild(optDefault);

        tratamientos.forEach(t => {
            // tarjeta tratamiento
            const col = document.createElement('div'); col.className='col-md-6 col-lg-4 mb-3';
            col.innerHTML = `
                <div class="card h-100">
                    <img src="${t.imagen}" class="card-img-top" alt="${t.nombre}">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${t.nombre}</h5>
                        <p class="card-text">${t.descripcion}</p>
                        <p class="mt-auto"><strong>${t.precioTexto}</strong></p>
                        <p class="service-features">${t.caracteristicas.join(' · ')}</p>
                        <div class="mt-2">
                            <button class="btn btn-outline-primary btn-sm btn-cotizar" data-id="${t.id}">Cotizar</button>
                            <button class="btn btn-primary btn-sm ms-2">Agendar</button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(col);

            // opción para select de cotización
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.nombre} — ${t.precioTexto}`;
            select.appendChild(opt);
        });

        // listeners en botones cotizar (se añaden después del render)
        Array.from(document.querySelectorAll('.btn-cotizar')).forEach(btn => {
            btn.addEventListener('click', function(){
                const id = this.dataset.id;
                const sel = document.getElementById('tratamiento-select');
                sel.value = id;
                // llevar foco a cotizador
                document.getElementById('cotizacion').scrollIntoView({behavior:'smooth'});
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
            // Usar precio mínimo para el cálculo (decisión solicitada):
            const precioUnitario = tratamiento.precioMin;
            const subtotal = precioUnitario;
            const total = subtotal * cantidad;
            const ahorro = total * (descuento/100);
            const totalConDesc = total - ahorro;
            const detalles = `\n                <p>Tratamiento: ${tratamiento.nombre}</p>\n                <p>Precio unitario usado para cálculo: $${precioUnitario.toFixed(2)} MXN (ver rango ${tratamiento.precioTexto})</p>\n                <p>Cantidad/unidades: ${cantidad}</p>\n                <p>Subtotal: $${subtotal.toFixed(2)}</p>\n                <p>Descuento: ${descuento}% (-$${ahorro.toFixed(2)})</p>\n                <h4>El costo total de tu tratamiento es de $${totalConDesc.toFixed(2)} MXN.</h4>\n            `;
            output.innerHTML = detalles;
            alert('El costo total de tu tratamiento es de $' + totalConDesc.toFixed(2) + ' MXN. (Se usó precio mínimo para el cálculo)');
        });
    }

    // Contacto: validación simple y mensaje simulado
    function setupContacto(){
        const form = document.getElementById('contact-form');
        const alertBox = document.getElementById('contact-alert');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            const nombre = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const mensaje = document.getElementById('mensaje').value.trim();
            if(!nombre || !email || !mensaje){
                alertBox.style.display='block';
                alertBox.className='alert alert-danger';
                alertBox.textContent='Por favor complete los campos requeridos.';
                return;
            }
            // validación simple de email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if(!emailRegex.test(email)){
                alertBox.style.display='block';
                alertBox.className='alert alert-danger';
                alertBox.textContent='Ingrese un correo válido.';
                return;
            }
            // simulación de envío
            alertBox.style.display='block';
            alertBox.className='alert alert-success';
            alertBox.textContent='Mensaje enviado con éxito. Nos pondremos en contacto pronto.';
            form.reset();
        });
    }

    // Galería simple
    function renderGaleria(){
        const grid = document.getElementById('galeria-grid');
        // Use local images from assets/img for the gallery carousel
        // Only use images that start with 'equipo' or 'instalaciones'
        const urls = [
            'assets/img/equipo1.png',
            'assets/img/equipo2.png',
            'assets/img/equipo3.png',
            'assets/img/instalaciones1.png',
            'assets/img/instalaciones2.png',
            'assets/img/instalaciones3.png',
            'assets/img/instalaciones4.png'
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
        const btnDark = document.getElementById('btn-darkmode');
        const btnLogin = document.getElementById('btn-login');
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
                logoImg.src = isDark ? 'assets/img/logo-blanco.png' : 'assets/img/logo-negro.png';
                logoImg.alt = isDark ? 'Clínica Dental Vitaldent logo blanco' : 'Clínica Dental Vitaldent logo oscuro';
            }
        };

        btnDark && btnDark.addEventListener('click', function(){
            document.body.classList.toggle('dark');
            syncThemeState();
        });

        syncThemeState();

        btnLogin && btnLogin.addEventListener('click', function(e){
            // Si el elemento es un enlace con href válido, dejar que navegue normalmente.
            const href = btnLogin.getAttribute('href');
            if(href && href.trim() !== '' && href !== '#'){
                return;
            }
            // Si es un botón sin href, navegar programáticamente a la página de login
            window.location.href = '/accounts/login/';
        });
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

    // Inicialización
    document.addEventListener('DOMContentLoaded', function(){
        renderTratamientos();
        setupCotizador();
        setupContacto();
        renderGaleria();
        renderTestimonios();
        setupUI();
        setupNavScrollHighlight();
    });

})();
