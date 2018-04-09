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
      <full-calendar :config="config" :editable="true" firstDay=1  @changeMonth="changeMonth" @eventClick="eventClick" :events="fcEvents" class="rittencalender"></full-calendar>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import 'moment/locale/nl';
import moment from 'moment'
import 'vue-fullcalendar/src/dataMap/langSets'
import fullCalendar from 'vue-fullcalendar'
import { alldata } from '../assets/js/firebase'
import { actief } from '../assets/js/firebase'
import { db } from '../assets/js/firebase'
Vue.component('full-calendar', fullCalendar)
export default {
  name: 'Ritten',
  data () {
    return {
      msg: 'Ritten',
      loaded: true,
      config:{
        locale: "nl"
      },
      fcEvents : [
      ]
    }
  },
  created (){

  },
  methods: {
    ritten: function(jaar, maand){
      this.fcEvents = []
      let self = this
      let all = db.ref(this.$parent.currentUser.uid)  
      all.child(jaar).child(maand).once('value', (snapshot) => {
         for (var key in snapshot.val()) {
           for(var subkey in snapshot.val()[key]){
            let ritdate = jaar + '-' + maand + '-' + key
            let ritobject = {
              title : subkey,
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
        let path = '/Ritten/' + event.start + '/' + event.title
        this.$router.push(path)
    },
    changeMonth: function(start, end, current){
      this.loaded = false
      let jaar = new Date(current).getFullYear();
      let maand = new Date(current).getMonth() + 1;
      console.log('s' + jaar)
      console.log('s' + maand)
      this.ritten(jaar, maand);

    }
  },
  components: {
    'full-calendar': require('vue-fullcalendar')
  }
}
</script>