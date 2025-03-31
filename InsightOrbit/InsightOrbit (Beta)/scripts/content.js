// Sobrescribir las propiedades en la página
(function() {
    Object.defineProperty(document, 'visibilityState', {
        get: () => 'visible',
    });
    Object.defineProperty(document, 'hidden', {
        get: () => false,
    });

    // Opcional: interceptar eventos relacionados
    const events = ['visibilitychange', 'blur', 'focus'];
    events.forEach(event => {
        document.addEventListener(event, e => {
            e.stopImmediatePropagation();
        }, true);
    });
})();

