import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import BootstrapVueIcons from 'bootstrap-vue/dist/bootstrap-vue-icons.esm';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import JsonViewer from 'vue-json-viewer';
import {Network} from 'vue-vis-network';
import VueSocketIO from 'vue-socket.io';
import SocketIO from 'socket.io-client';
// import store from './store';
import './index.css';

Vue.component('network', Network);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(JsonViewer);

console.log('Launching with env', import.meta.env);
const socketConnection = SocketIO(import.meta.env.VITE_SOCKET_ADDRESS);
// const socketConnection = SocketIO('http://10.200.130.43:8002');
Vue.use(new VueSocketIO({
  debug: true,
  connection: socketConnection,
  // vuex: {
  //   store,
  //   actionPrefix: 'SOCKET_',
  //   mutationPrefix: 'SOCKET_',
  // },
  options: {
    path: '/my-app/'
  },
}));

Vue.config.productionTip = false;

new Vue({
  router,
  // store,
  render: h => h(App),
}).$mount('#app');
