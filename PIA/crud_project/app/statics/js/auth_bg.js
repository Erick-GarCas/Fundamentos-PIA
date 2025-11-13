/*
	auth_bg.js

	Manual de usuario (documentación en español):

	Propósito:
	- Este script anima los degradados y brillos (glows) del layout de autenticación
		(páginas de login/signup) usando variables CSS personalizadas (custom properties).
	- Crea animaciones suaves y continuas que actualizan variables como posiciones de glow,
		ángulos y matices (hue) para producir un movimiento orgánico en el fondo y paneles.

	Componentes esperados en el DOM (selectores usados):
	- `.auth-shell`      : contenedor principal que recibe variables globales de background/glow
	- `.auth-side-media` : panel lateral con medios (imagen/video) que usa variables propias
	- `.auth-side-form`  : panel donde está el formulario; variables propias opcionales
	- `.auth-card`       : tarjeta principal (opcional) que recibe un glow puntual

	Consideraciones de accesibilidad:
	- Si el usuario ha indicado `prefers-reduced-motion: reduce`, la animación no se inicia.
		Esto respeta las preferencias del sistema para reducir movimiento.

	Comportamiento general:
	- El script calcula valores periódicos (con funciones trigonométricas) para producir
		movimientos suaves y no repetitivos. Esencialmente actualiza variables CSS mediante
		`element.style.setProperty('--variable', value)` en cada frame de animación.
	- La animación se ejecuta con `requestAnimationFrame` para sincronizar con el repaint del navegador.

	Notas técnicas:
	- No cambia ni manipula el contenido semántico; solo actualiza estilos en línea (custom properties).
	- Las variables CSS utilizadas (_por ejemplo_ `--auth-glow-x`, `--auth-panel-hue`) deben
		estar referenciadas en el CSS para que el efecto sea visible.
	- Mantén los nombres de clases exactamente como están si añades o modificas elementos.
*/

(function () {
		// Obtener referencias a los elementos relevantes del DOM.
		const shell = document.querySelector('.auth-shell');
		const media = document.querySelector('.auth-side-media');
		const formSide = document.querySelector('.auth-side-form');
		const card = document.querySelector('.auth-card');

		// Si no existen los elementos mínimos requeridos, no iniciar la animación.
		if (!shell || !media) {
				return;
		}

		// Respetar la preferencia del usuario para reducir movimiento.
		const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
		if (reduceMotion.matches) {
				// Si el usuario prefiere reducir movimientos, no iniciamos la animación.
				return;
		}

		// Variable de tiempo para generar movimientos continuos.
		let t = 0;

		/*
			Función animate():
			- Ejecutada en bucle mediante requestAnimationFrame.
			- Calcula offsets y ángulos usando funciones trigonométricas (sin/cos).
			- Actualiza variables CSS en `shell`, `media`, `formSide` y `card`.
			- Los valores se ajustan con pequeños factores para que el movimiento sea sutil.
		*/
		function animate() {
				// Incremento muy pequeño para suavizar la animación.
				t += 0.005;

				// Cálculo de posiciones para el glow principal del shell (porcentajes).
				const glowX = 20 + Math.sin(t) * 18; // movimiento horizontal oscilante
				const glowY = 25 + Math.cos(t * 1.1) * 12; // movimiento vertical ligeramente distinto
				const angle = 110 + Math.sin(t * 0.7) * 6; // ángulo del gradiente de fondo

				// Aplicar las variables CSS en el contenedor principal.
				shell.style.setProperty('--auth-glow-x', `${glowX}%`);
				shell.style.setProperty('--auth-glow-y', `${glowY}%`);
				shell.style.setProperty('--auth-bg-angle', `${angle}deg`);

				// Cálculos para el panel lateral (media)
				const hue = 205 + Math.sin(t * 0.8) * 10; // matiz del color (hue)
				const panelAngle = 130 + Math.cos(t * 0.5) * 10; // ángulo del panel
				const mediaX = 35 + Math.sin(t * 0.6) * 25; // glow del media (x)
				const mediaY = 25 + Math.cos(t * 0.4) * 20; // glow del media (y)

				// Aplicar variables en el panel media
				media.style.setProperty('--auth-panel-hue', hue.toFixed(2));
				media.style.setProperty('--auth-panel-angle', `${panelAngle}deg`);
				media.style.setProperty('--auth-media-glow-x', `${mediaX}%`);
				media.style.setProperty('--auth-media-glow-y', `${mediaY}%`);

				// Si existe el panel del formulario, aplicarle variaciones propias
				if (formSide) {
						const formHue = 215 + Math.cos(t * 0.6) * 8;
						const formAngle = 205 + Math.sin(t * 0.5) * 10;
						const formGlowX = 58 + Math.sin(t * 0.9) * 18;
						const formGlowY = 48 + Math.cos(t * 0.7) * 12;
						formSide.style.setProperty('--auth-form-hue', formHue.toFixed(2));
						formSide.style.setProperty('--auth-form-angle', `${formAngle}deg`);
						formSide.style.setProperty('--auth-form-glow-x', `${formGlowX}%`);
						formSide.style.setProperty('--auth-form-glow-y', `${formGlowY}%`);
				}

				// Si existe la tarjeta central (`.auth-card`), aplicarle un glow puntual
				if (card) {
						const cardGlowX = 72 + Math.sin(t * 1.3) * 18;
						const cardGlowY = 28 + Math.cos(t * 1.1) * 12;
						card.style.setProperty('--auth-card-glow-x', `${cardGlowX}%`);
						card.style.setProperty('--auth-card-glow-y', `${cardGlowY}%`);
				}

				// Volver a solicitar el siguiente frame de animación
				requestAnimationFrame(animate);
		}

		// Iniciar la animación (primera solicitud de frame)
		requestAnimationFrame(animate);
})();
