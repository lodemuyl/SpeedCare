/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Activeer from '@/components/Activeer'
import Rapporten from '@/components/Rapporten'
import Ritten from '@/components/Ritten'
import Over from '@/components/Over'
import Detail from '@/components/Detail'
import Detaillist from '@/components/Detaillist'
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
      path: '/Ritten/:datum',
      name: 'Detaillist',
      component: Detaillist,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/Ritten/:datum/:tijd',
      name: 'Detail',
      component: Detail,
      meta: {
        requiresAuth: true
      }
    },
     {
      path: '/Over',
      name: 'Over',
      component: Over,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/Disclaimer',
      name: 'Disclaimer',
      component: Disclaimer,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/*',
      name: 'Notfound',
      component: Notfound,
      meta: {
        requiresAuth: false
      }
    },
  ],
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})
router.beforeEach((to, from, next) => {
  //ingelogd of niet
  let currentUser = firebase.auth().currentUser;
  //kijken naar de route waar naartoe en zien of deze auth bevat ja of neen
  let requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  //als je niet ingelogd bent en de route is requireauth dan ...
  if(requiresAuth && !currentUser) next('Login')
  else if (currentUser && to.name == 'Over') next()
  else if (!requiresAuth && currentUser && to.name == 'Disclaimer') next()
  // als auth niet moet en wel ingelogd en route naar is home 
  else if (!requiresAuth && currentUser && to.name == 'Home') next()
  // als auth niet moet en wel ingelogd 
  else if (!requiresAuth && currentUser) next('Home')
  else next()
})
export default router