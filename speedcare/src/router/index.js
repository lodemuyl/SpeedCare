import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
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
    }
  ]
})
