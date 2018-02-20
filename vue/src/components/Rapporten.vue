<template>
  <div class="rapporten">
    <h2 class="pagetitle center">{{ msg }}</h2>
      <div class="container">
      <div class="row">
        <div class="col s12 md12 l12">
          <ul id="" class="tabs tabs tabs-fixed-width">
            <li class="tab col s3"><a id="firstclick" class="active" href="#jaar">Jaar</a></li>
            <li class="tab col s3"><a href="#snelheid">Snelheidsovertredingen</a></li>
          </ul>
        </div>
        <div id="jaar" class="col s12 md12 l12 sw">
              <div class="card">
                <div class="card-content white-text">
                  <span class="card-title halfstrong">Jaar</span>
                  <ul class="collapsible ">
                    <li v-for="item in jaren" v-bind:class="{active: item == jaar}" v-bind:value="item">
                      <div class="collapsible-header halfstrong">{{ item }}</div>
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
require('chart.js');
require('hchs-vue-charts');
Vue.use(VueCharts);
export default {
  name: 'Rapporten',
  data () {
    return {
      msg: 'Rapporten',
      jaren: [2018,2019,2020],
      jaar: moment().format('YYYY'),
      options:{
        responsive: true
      },
      mybackgroundcolor:'#84AE99',
      mybordercolor: '#84AE99',
      mylabel : 'Rijscore',
      mylabels : ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
      mydata : [100, 40, 60, 20, 11, 44, 49, 77, 67, 10, 70, 44],
      
    }
  },
  created(){

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
  }
}
</script>