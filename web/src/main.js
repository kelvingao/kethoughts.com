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
import Home from '@/components/pages/home'
import Login from '@/components/pages/login'
import Manage from '@/components/manage/index'
import Analytics from '@/components/manage/analytics'
import Users from '@/components/manage/users'


/*--------------------------------------------------------------
Vue Router
--------------------------------------------------------------*/
import VueRouter from 'vue-router'
Vue.use(VueRouter);

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next()
    return
  }
  next('/login')
}

const router = new VueRouter({
  linkActiveClass: 'is-active',
  mode: 'history',
  routes: [
    { path: '/home', component: Home },
    { path: '/login', component: Login },
    { path: '/manage', component: Manage, beforeEnter: ifAuthenticated, children: [
      { path: 'analytics', component: Analytics, meta: { title: 'analytics' } },
      { path: 'users', component: Users, meta: { title: 'users' } },
    ], meta: { title: 'manage' } }
  ]
});


Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
