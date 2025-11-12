(function () {
	const shell = document.querySelector('.auth-shell');
	const media = document.querySelector('.auth-side-media');
	const formSide = document.querySelector('.auth-side-form');
	const card = document.querySelector('.auth-card');

	if (!shell || !media) {
		return;
	}
	const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
	if (reduceMotion.matches) {
		return;
	}

	let t = 0;

	function animate() {
		t += 0.005;

		const glowX = 20 + Math.sin(t) * 18;
		const glowY = 25 + Math.cos(t * 1.1) * 12;
		const angle = 110 + Math.sin(t * 0.7) * 6;

		shell.style.setProperty('--auth-glow-x', `${glowX}%`);
		shell.style.setProperty('--auth-glow-y', `${glowY}%`);
		shell.style.setProperty('--auth-bg-angle', `${angle}deg`);

		const hue = 205 + Math.sin(t * 0.8) * 10;
		const panelAngle = 130 + Math.cos(t * 0.5) * 10;
		const mediaX = 35 + Math.sin(t * 0.6) * 25;
		const mediaY = 25 + Math.cos(t * 0.4) * 20;

		media.style.setProperty('--auth-panel-hue', hue.toFixed(2));
		media.style.setProperty('--auth-panel-angle', `${panelAngle}deg`);
		media.style.setProperty('--auth-media-glow-x', `${mediaX}%`);
		media.style.setProperty('--auth-media-glow-y', `${mediaY}%`);

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

		if (card) {
			const cardGlowX = 72 + Math.sin(t * 1.3) * 18;
			const cardGlowY = 28 + Math.cos(t * 1.1) * 12;
			card.style.setProperty('--auth-card-glow-x', `${cardGlowX}%`);
			card.style.setProperty('--auth-card-glow-y', `${cardGlowY}%`);
		}

		requestAnimationFrame(animate);
	}

	requestAnimationFrame(animate);
})();
