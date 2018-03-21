<template>
  <div class="rapporten">
    <h2 class="pagetitle center">{{ msg }}</h2>
      <div class="">
        <div class="row">
          <div class="col s12 md12 l12">
            <ul id="" class="tabs tabs tabs-fixed-width">
              <li class="tab col s3"><a id="firstclick" class="active" href="#jaar">Jaar</a></li>
              <li class="tab col s3"><a href="#snelheid">Snelheidsovertredingen</a></li>
            </ul>
          </div>
          <div id="jaar" class="col s12 md12 l12 sw">
            <div v-show="!loadedyear">
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
            <div v-show="loadedyear" class="card" v-for="jaar in jaren">
                  <div class="card-content white-text">
                    <span class="card-title halfstrong">2018</span>
                    <ul class="collapsible ">
                      <li v-for="maand in maanden" v-bind:value="jaar">
                        <div class="collapsible-header halfstrong">{{ maand }}</div>
                        <div class="collapsible-body">
                          <chartjs-horizontal-bar :option="options" :bordercolor="mybordercolor" :backgroundcolor="mybackgroundcolor" :datalabel="mylabel" :labels="mylabels" :data="mydata"></chartjs-horizontal-bar>
                        </div>
                      </li>
                    </ul>
                  </div>
            </div>
          </div>
          <div id="snelheid" class="col s12 md12 l12 sw">
                <div class="card blue-grey darken-1">
                  <div class="card-content white-text">
                    <span class="card-title">Snelheidsovertredingen</span>
                    <p>I am a very simple card. I am good at containing small bits of information.
                    I am convenient because I require little markup to use effectively.</p>
                  </div>
                </div>
          </div>
        </div>
      </div>
  </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import moment from 'moment'
import { alldata } from '../assets/js/firebase'
import { actief } from '../assets/js/firebase'
import { db } from '../assets/js/firebase'
require('chart.js');
require('hchs-vue-charts');
Vue.use(VueCharts);
export default {
  name: 'Rapporten',
  data () {
    return {
      msg: 'Rapporten',
      firebaseref: db.ref(this.$parent.currentUser.uid), 
      loadedyear: false,
      jaren: [2018],
      maanden:['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
      jaar: moment().format('YYYY'),
      options:{
        responsive: true
      },
      mybackgroundcolor:'#84AE99',
      mybordercolor: '#84AE99',
      mylabel : 'Rijscore',
      mylabels : ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
      mydata : [100, 40, 60, 20, 11, 44, 49, 77, 67, 5, 70, 44],
      
    }
  },
  created(){
    this.getdates();
  },
  mounted(){
    var elem
    var elem1
    var instance
    this.$nextTick(function(){
      let options = {
      }
      elem = document.querySelector('.tabs'); 
      elem1 = document.querySelector('#firstclick'); 
      instance = M.Tabs.init(elem,options);    
      instance.updateTabIndicator();
      elem1.click();      
    })
    var collapsible = document.querySelector('.collapsible');
    var instance = M.Collapsible.getInstance(collapsible);
    var instance = M.Collapsible.init(collapsible);
  },
  methods: {
    main: function(){

    },
    getdates: function(){
      let all = this.firebaseref;
      let dates = {}
      all.once("value").then((snapshot)=>{
        snapshot.forEach((year)=>{
          if(year.key === "actief" || year.key === "productnummer"){
            return false
          } else{
            console.log(year.key)
            year.forEach((month)=>{
              console.log('--'+month.key)
              month.forEach((day)=>{
                console.log('----'+day.key)
                day.forEach((time)=>{
                  console.log('------'+time.key)
                })
              })
            })
          }        
        })
       // this.jaren = years
        this.loadedyear = true
      })
    }

  }
}
</script>