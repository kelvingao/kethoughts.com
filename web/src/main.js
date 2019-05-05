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
import Post from '@/components/pages/post'
import Manage from '@/components/manage/index'
import Analytics from '@/components/manage/analytics'
import Users from '@/components/manage/users/index'
import Posts from '@/components/manage/posts/index'
import CreatePost from '@/components/manage/posts/createPost'
import EditPost from '@/components/manage/posts/editPost'


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
    { path: '/posts', component: Home },
    { path: '/login', component: Login },
    { path: '/posts/:slug', component: Post  },
    { path: '/manage', component: Manage, beforeEnter: ifAuthenticated, children: [
      { path: 'analytics', component: Analytics, meta: { title: 'analytics' } },
      { path: 'users', component: Users, meta: { title: 'users' } },
      { path: 'posts', component: Posts, meta: { title: 'posts' }, children: [
        { path: 'create', component: CreatePost, meta: { title: 'create' }},
        { path: 'edit/:id', component: EditPost, meta: { title: 'edit' }} ]
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
