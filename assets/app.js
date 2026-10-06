(() => {
  let prompt;
  const install = document.querySelector('#installGuide'), status = document.querySelector('#installStatus');
  const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  function installed() { if (install) install.hidden = true; if (status) status.textContent = 'The guide is open in its own app window. You’re ready to go.'; }
  if (standalone()) installed();
  addEventListener('beforeinstallprompt', event => {
    if (!install || standalone()) return;
    event.preventDefault(); prompt = event; install.hidden = false;
    if (status) status.textContent = 'This browser can install the guide. Tap the button below.';
  });
  install?.addEventListener('click', async () => {
    if (!prompt) return;
    const current = prompt; prompt = undefined; install.hidden = true; await current.prompt();
    const choice = await current.userChoice;
    if (status) status.textContent = choice.outcome === 'accepted' ? 'Follow your browser’s confirmation, then open the Utah Guide icon.' : 'You can install later using your browser’s menu.';
  });
  addEventListener('appinstalled', installed);
  const notice = document.createElement('div'); notice.className = 'connection-notice'; notice.setAttribute('role', 'status'); notice.hidden = true;
  document.querySelector('.site-header')?.after(notice);
  function connection() { notice.hidden = navigator.onLine; notice.textContent = 'You’re offline. Browsing saved guide information; details may have changed. Tickets and sending forms need a connection.'; }
  addEventListener('online', connection); addEventListener('offline', connection); connection();
  if (!('serviceWorker' in navigator) || !isSecureContext) return;
  const update = document.createElement('div'); update.className = 'app-update'; update.setAttribute('role', 'status'); update.hidden = true; document.body.append(update);
  function showUpdate(registration) {
    if (!registration.waiting || !navigator.serviceWorker.controller) return;
    update.hidden = false;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'button primary'; button.textContent = 'Refresh the guide';
    button.addEventListener('click', () => registration.waiting.postMessage({ type: 'ACTIVATE_UPDATE' }));
    update.replaceChildren(document.createTextNode('A guide update is ready. Save any unfinished form before refreshing. '), button);
  }
  let refreshing = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => { if (!refreshing && !update.hidden) { refreshing = true; location.reload(); } });
  navigator.serviceWorker.register('/sw.js').then(registration => {
    showUpdate(registration);
    registration.addEventListener('updatefound', () => { registration.installing?.addEventListener('statechange', () => showUpdate(registration)); });
  }).catch(() => { if (status) status.textContent = 'You can use the guide online. Offline setup was unavailable; try reloading with a connection.'; });
})();
