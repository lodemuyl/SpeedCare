// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

/* eslint-disable */
import Vue from 'vue'
import App from './App'
import router from './router'
import VueRouter from 'vue-router'
import 'materialize-css/sass/materialize.scss'
import 'materialize-css'
import 'font-awesome/css/font-awesome.css' 
import '@/assets/sass/main.scss'
import './assets/js/firebase'
import firebase from 'firebase'
Vue.config.productionTip = false
Vue.use(VueRouter)
let app;

firebase.auth().onAuthStateChanged(function(user){
  if(!app){
    new Vue({
      el: '#app',
      router,
      template: '<App/>',
      components: { App }
    })
  }
})

