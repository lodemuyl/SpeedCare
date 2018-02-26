/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Activeer from '@/components/Activeer'
import Rapporten from '@/components/Rapporten'
import Ritten from '@/components/Ritten'
import Over from '@/components/Over'
import Notfound from '@/components/404'
import Account from '@/components/Account'
import Disclaimer from '@/components/Disclaimer'
import firebase from 'firebase'

Vue.use(Router)

let router = new Router({
  routes: [
    // {
    //   path: '*',
    //   redirect: '/Home'
    // },
    {
      path: '/',
      redirect: '/Home'
    },
    {
      path: '/Disclaimer',
      name: 'Disclaimer',
      component: Disclaimer
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Activeer',
      name: 'Activeer',
      component: Activeer
    },
    {
      path: '/Over',
      name: 'Over',
      component: Over
    },
    {
      path: '/Rapporten',
      name: 'Rapporten',
      component: Rapporten,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/Ritten',
      name: 'Ritten',
      component: Ritten,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/Account',
      name: 'Account',
      component: Account,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home,
    },
    {
       path: '/*',
       name: 'Notfound',
       component: Notfound
     }
  ]
})
router.beforeEach((to, from, next) => {
  let currentUser = firebase.auth().currentUser;
  let requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  if(requiresAuth && !currentUser) next('Login')
  // bugfix anders zal hij in een ininity loop geraken
  //else if (!requiresAuth && !currentUser && to.name == "Home") next()
  else if (!requiresAuth && currentUser && to.name == "Home") next()
  else if (!requiresAuth && currentUser) next('Home')
  else next()
})
export default router