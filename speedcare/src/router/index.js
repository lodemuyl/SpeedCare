import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Activeer from '@/components/Activeer'
import Rapporten from '@/components/Rapporten'
import Ritten from '@/components/Ritten'
import Notfound from '@/components/404'
import Account from '@/components/Account'
import Disclaimer from '@/components/Disclaimer'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
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
      path: '/Rapporten',
      name: 'Rapporten',
      component: Rapporten
    },
    {
      path: '/Ritten',
      name: 'Ritten',
      component: Ritten
    },
    {
      path: '/Account',
      name: 'Account',
      component: Account
    },
    {
      path: '/*',
      name: 'Notfound',
      component: Notfound
    }
  ]
})
