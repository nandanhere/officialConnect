importScripts("https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js");
firebase.initializeApp({
    apiKey: "AIzaSyAKT1K87BKF-N_EfqRT9QtnasHQk-p9CVI",
    authDomain: "officialconnect-58897.firebaseapp.com",
    databaseURL: "https://officialconnect-58897-default-rtdb.firebaseio.com",
    projectId: "officialconnect-58897",
    storageBucket: "officialconnect-58897.appspot.com",
    messagingSenderId: "325443015605",
    appId: "1:325443015605:web:565e445cd3b50016813ffc",
    measurementId: "G-S60LB92CG8"
});
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const promiseChain = clients
        .matchAll({
            type: "window",
            includeUncontrolled: true
        })
        .then(windowClients => {
            for (let i = 0; i < windowClients.length; i++) {
                const windowClient = windowClients[i];
                windowClient.postMessage(payload);
            }
        })
        .then(() => {
            return registration.showNotification("New Message");
        });
    return promiseChain;
});
self.addEventListener('notificationclick', function (event) {
    console.log('notification received: ', event)
});