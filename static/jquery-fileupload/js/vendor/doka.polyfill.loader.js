(function () {
  'use strict';
  if (!Array.prototype.forEach) return;
  [
    {
      supported: 'Promise' in window,
      fill:
        'https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js'
    },
    {
      supported: 'fetch' in window,
      fill: 'https://cdn.jsdelivr.net/npm/fetch-polyfill@0.8.2/fetch.min.js'
    },
    {
      supported:
        'CustomEvent' in window &&
        'log10' in Math &&
        'sign' in Math &&
        'assign' in Object &&
        'from' in Array &&
        ['find', 'findIndex', 'includes'].reduce(function (previous, prop) {
          return prop in Array.prototype ? previous : false;
        }, true),
      fill: 'js/vendor/doka.polyfill.min.js'
    }
  ].forEach(function (p) {
    if (p.supported) return;
    document.write('<script src="' + p.fill + '"></script>');
  });
})();
