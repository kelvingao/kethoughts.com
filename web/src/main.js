import Vue from "vue";
import App from "./App.vue";

import store from './store'


/*--------------------------------------------------------------
Buefy & font-awesome
--------------------------------------------------------------*/
import Buefy from 'buefy'
import '@fortawesome/fontawesome-free/css/solid.css'
import '@fortawesome/fontawesome-free/css/fontawesome.css'

Vue.use(Buefy, {
  defaultIconPack: 'fas',
});


/*--------------------------------------------------------------
Custom components
--------------------------------------------------------------*/
import Login from '@/components/pages/login'


/*--------------------------------------------------------------
Vue Router
--------------------------------------------------------------*/
import VueRouter from 'vue-router'
Vue.use(VueRouter);

const router = new VueRouter({
  linkActiveClass: 'is-active',
  mode: 'history',
  routes: [
    { path: '/login', component: Login },
  ]
});


Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
