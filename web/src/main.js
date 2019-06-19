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
Slug generator
--------------------------------------------------------------*/
window.Slug = require('slug')
Slug.defaults.mode = 'rfc3986'


/*--------------------------------------------------------------
VueQillEditor
--------------------------------------------------------------*/
import VueQuillEditor, { Quill } from 'vue-quill-editor'

// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

const icons = Quill.import("ui/icons")
icons['more'] = '<i class="fa fa-ellipsis-h" aria-hidden="true"></i>';

Vue.use(VueQuillEditor, /* { default global options } */)


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
    { path: '/', redirect: '/posts' },
    { path: '/posts', component: (resolve) => require(['@/components/pages/home'],resolve) },
    { path: '/login', component: (resolve) => require(['@/components/pages/login'],resolve) },
    { path: '/posts/:slug', component: (resolve) => require(['@/components/pages/post'],resolve)  },
    { path: '/manage', component: (resolve) => require(['@/components/manage/index'],resolve), beforeEnter: ifAuthenticated, children: [
      { path: 'analytics', component: (resolve) => require(['@/components/manage/analytics'],resolve), meta: { title: 'analytics' } },
      { path: 'users', component: (resolve) => require(['@/components/manage/users/index'],resolve), meta: { title: 'users' } },
      { path: 'posts', component: (resolve) => require(['@/components/manage/posts/index'],resolve), meta: { title: 'posts' }, children: [
        { path: 'create', component: (resolve) => require(['@/components/manage/posts/createPost'],resolve), meta: { title: 'create' }},
        { path: 'edit/:id', component: (resolve) => require(['@/components/manage/posts/editPost'],resolve), meta: { title: 'edit' }} ]
      },
    ], meta: { title: 'manage' } }
  ]
});


/*--------------------------------------------------------------
Vue Filters
--------------------------------------------------------------*/
Vue.filter('formatDate', function (timestamp) {
  function addZero(i) { if (i < 10) i = "0" + i; return i; }

  let date = new Date();
  date.setTime(timestamp * 1000);

  let y = date.getFullYear();
  let M = addZero(date.getMonth() + 1);
  let d = addZero(date.getDate());

  let h = addZero(date.getHours());
  let m = addZero(date.getMinutes());
  let s = addZero(date.getSeconds());

  return y + "-" + M + "-" + d + " " + h + ":" + m + ":" + s;
})


Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
