
// let swLocation = "sw.js";

// console.log('Init serviceWorker')
// if (navigator.serviceWorker) {
//   var domain = window.location.hostname;
//   console.log(domain);
//   if (window.location.href.includes(domain)) swLocation = "/static/app/js/sw.js";
//   navigator.serviceWorker.register(swLocation);
// }

const checkPermission = () => {
  if(!('serviceWorker') in navigator){
    throw new Error('ServiceWorker no soportado')
  }

  if(!('Notification') in window){
    throw new Error('Notificaciones no soportadas')
  }
}

const registerSW = async () => {
  const registration = await navigator.serviceWorker.register('/static/app_stv/js/sw.js');
  return registration;
}

const requestNotificationPermission = async () => {
  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    console.warn('El usuario ha denegado el permiso para notificaciones');
  }
}

const main = async () => {
  checkPermission();
  requestNotificationPermission();
  // await requestNotificationPermission();
  // await registerSW();

  const lastNotificationDate = localStorage.getItem('lastNotificationDate');
  const today = new Date().toDateString();

  if (lastNotificationDate !== today) {
    const reg = await registerSW();
    reg.showNotification('Hola!', {
      body: '¡Bienvenido a STV App!'
    });
    localStorage.setItem('lastNotificationDate', today);
  }
}

main();
