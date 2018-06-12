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
      <full-calendar lang="en" :config="config" :editable="true" firstDay=1  @changeMonth="changeMonth" @eventClick="eventClick" :events="fcEvents" class="rittencalender"></full-calendar>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue';
import moment from 'moment';
import fullCalendar from 'vue-fullcalendar'
import { alldata } from '../assets/js/firebase';
import { actief } from '../assets/js/firebase';
import { db } from '../assets/js/firebase';
import 'vue-fullcalendar/src/dataMap/langSets';
Vue.component('full-calendar', fullCalendar);
export default {
  name: 'Ritten',
  data () {
    return {
      msg: 'Ritten',
      loaded: true,
      config: {
        lang: 'nl'
      },
      fcEvents : [
      ]
    }
  },
  created(){
    //let jaar = new Date(current).getFullYear();
    //let maand = new Date(current).getMonth() + 1;
    //this.ritten(2018,4)
  },
  methods: {
    ritten: function(jaar, maand){
      this.fcEvents = []
      let self = this
      let all = db.ref(this.$parent.currentUser.uid)  
      all.child(jaar).child(maand).once('value', (snapshot) => {
         for (var key in snapshot.val()) {
           for(var subkey in snapshot.val()[key]){
            let stringdate = String(jaar + '-' + maand + '-' + key)
            //naar ISO-8601 standaard voor safari en andere browsers
            let iso = moment(stringdate,"YYYY-MM-DD")
            let ritobject = {
              title : subkey,
              start : iso,
              cssClass  : 'autoritevent',
            }
            self.fcEvents.push(ritobject)
           }
        } 
        self.loaded = true
        
      })
    },
    eventClick: function(event, jsEvent, pos) {
      //terug omzetten van iso standaard naar gewoon formaat
      let normaal = moment(event.start, "YYY-MM-DD")
      let path = '/Ritten/' + normaal._i + '/' + event.title
      this.$router.push(path)
    },
    changeMonth: function(start, end, current){
      console.log(start);
      console.log(end)
      this.loaded = false
      let jaar = new Date(current).getFullYear();
      let maand = new Date(current).getMonth() + 1;
      this.ritten(jaar, maand);
    }
  },
  components: {
    'full-calendar': require('vue-fullcalendar')
  }
}
</script>