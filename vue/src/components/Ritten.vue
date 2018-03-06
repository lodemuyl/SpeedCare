<template>
  <div class="ritten">
    <div v-show="!loaded">
      <div id="load">
            <div class="loadblock">
                <div class="preloader-wrapper big active">
                <div class="spinner-layer spinner-red-only">
                    <div class="circle-clipper left">
                    <div class="circle"></div>
                    </div><div class="gap-patch">
                    <div class="circle"></div>
                    </div><div class="circle-clipper right">
                    <div class="circle"></div>
                    </div>
                </div>
                </div>
            </div>
      </div>
    </div>
    <div v-show="loaded">
      <h2 class="pagetitle center">{{ msg }}</h2>
      <full-calendar @changeMonth="changeMonth" @eventClick="eventClick" :events="fcEvents" :config="config" class="rittencalender"></full-calendar>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import '../assets/js/calenderlanguage.js'
import fullCalendar from 'vue-fullcalendar'
import { alldata } from '../assets/js/firebase'
import { actief } from '../assets/js/firebase'
import { db } from '../assets/js/firebase'
Vue.component('full-calendar', fullCalendar)
var helpers = require('../assets/js/helpers')

export default {
  name: 'Ritten',
  data () {
    return {
      msg: 'Ritten',
      loaded: false,
      logs: {},
      config: {
        locale: 'fr'
      },
      fcEvents : [
      ]
    }
  },
  created (){
    this.ritten();
  },
  methods: {
    ritten: function(){
      let vandaag = new Date();
      let all = db.ref(this.$parent.currentUser.uid)  
      let self = this
      all.child(vandaag.getFullYear()).child(vandaag.getMonth()+1).on('value', (snapshot) => {
        let data = snapshot.val()
        self.logs = data
        for (var key in self.logs) {
          for(var subkey in self.logs[key]){
            let maand = vandaag.getMonth() + 1
            let jaar = vandaag.getFullYear()
            let ritdate = jaar + '-' + maand + '-' + key
            let ritobject = {
              title : subkey.substring(0,5),
              start : ritdate,
              cssClass  : 'autoritevent',
            }
            self.fcEvents.push(ritobject)
          }
        } 
        self.loaded = true
      })
    },
    eventClick: function(event, jsEvent, pos) {
        console.log('eventClick', event, jsEvent, pos)
    },
    changeMonth: function(start, end, current){
      console.log('changeMonth', start, end, current)
    }
  },
  components: {
    'full-calendar': require('vue-fullcalendar')
  }
}
</script>