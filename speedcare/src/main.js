// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

/* eslint-disable */
import Vue from 'vue'
import App from './App'
import router from './router'
import '@/assets/sass/main.scss'
import './assets/js/materialize'
Vue.config.productionTip = false

//let elem = document.querySelector('.sidenav');
//let instance = M.Sidenav.init(elem, options);

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
