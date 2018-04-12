<template>
  <div class="rapporten">
    <h2 class="pagetitle center">{{ msg }}</h2>
      <div class="">
        <div class="row">
          <div class="col s12 md12 l12">
            <ul id="" class="tabs tabs tabs-fixed-width">
              <li class="tab col s3"><a :id="actiefjaar" href="#jaar">Jaar</a></li>
              <li class="tab col s3"><a :id="actiefsnelheid" href="#snelheid" v-on:click="speedviolations">Snelheidsovertredingen</a></li>
            </ul>
          </div>
          <div id="jaar" class="col s12 md12 l12 sw">        
            <div class="card" v-for="jaar in jaren">
                  <div v-show="!loadedyear">
                      <div id="load">
                            <div class="loadblock">
                                <div class="preloader-wrapper big active">
                                <div class="spinner-layer spinnerwhite">
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
                  <div v-show="loadedyear" class="card-content white-text">
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
                <div class="card">
                  <div v-show="!overtredingen">
                    <p class="noviolations"><span class="card-title halfstrong">Er zijn geen overtredingen vastgesteld voor {{ month }}.</span></p>
                  </div>
                  <div v-show="overtredingen">
                    <div v-show="!loadedspeed" id="load">
                          <div class="loadblock">
                              <div class="preloader-wrapper big active">
                              <div class="spinner-layer spinnerwhite">
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
                    <div v-show="loadedspeed" class="card-content white-text">
                      <span class="card-title halfstrong overtredingenmaand">Overtredingen {{ month }}</span>
                        <div class="dag" v-for="overtreding in overtredingenlist">
                          <p class="dagnaam">{{overtreding.dagnaam}}</p>
                          <div class="ritten" v-for="rit in overtreding.ritten">
                            <p>{{rit.rit}}</p>
                            <div class="overtreding" v-for="tijdstip in rit.logs">
                              <p>overtreding om  {{ tijdstip.tijd }} op de {{tijdstip.info.straat}}</p>                            
                            </div>
                          </div>
                         
                        </div>                  
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
      user: this.$parent.currentUser.providerData[0].displayName,
      firebaseref: db.ref(this.$parent.currentUser.uid), 
      loadedyear: false,
      loadedspeed: false,
      actiefjaar: this.$parent.actiefjaar,
      actiefsnelheid: this.$parent.actiefsnelheid,
      jaren: [2018],
      overtredingen: true,
      overtredingenlist: [],
      maanden:['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
      jaar: moment().format('YYYY'),
      month:  moment(moment(), "YYYY-MM").locale('nl').format('MMMM YYYY'),
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
    //materialize initialization
    var tabs = document.querySelector('.tabs'); 
    var firstclick = document.querySelector('#firstclick'); 
    var collapsible = document.querySelector('.collapsible');
    let optionstab = {
    };
    var optionsselect = {
      classes: "selectperiode"
    };
    var optionscollapsible = {
    };  
    var instance = M.Collapsible.init(collapsible,optionscollapsible);     
    this.$nextTick(function(){ 
      var tab = M.Tabs.init(tabs,optionstab);    
      tab.updateTabIndicator();
      firstclick.click();            
    })
  },
  updated(){

  },
  methods: {
    speedviolations: function(){
      //inladen lijst voor select.
      let all = db.ref(this.$parent.currentUser.uid)
      let jaar = new Date().getFullYear();
      let maand = new Date().getMonth()+1 
      //leegmaken lijst  
      this.overtredingenlist = []
      all.child('overtredingen').child(jaar).child(maand).once('value', (snapshot)=>{
        let list= {}
      //ophalen van gewone rittendata
        if(snapshot.val() !== null){   
              snapshot.forEach((dag)=>{
              let dagnummer = dag.key
              list["dag"] = dagnummer;
              list["dagnaam"] = moment(dagnummer, "D").locale('nl').format('dddd LL')
              list["ritten"] = []
              dag.forEach((ritten)=>{
                let ritobj = {}
                let ritkey = ritten.key
                ritobj["rit"] = ritkey
                ritobj["logs"] = []
                list["ritten"].push(ritobj)
                ritten.forEach((info)=>{
                  let infoobj = {}
                  infoobj["tijd"] = info.key
                  infoobj["info"] = []
                  ritobj["logs"].push(infoobj)
                  info.forEach((snapshot)=>{
                   infoobj["info"] = snapshot.val()
                  })
                })
              })
            })    
          this.overtredingenlist.push(list)                  
        }else{
          this.overtredingen = false; 
        }   
      }).then(()=>{
        this.loadedspeed = true
      })     
    },
    getdates: function(){
      let all = this.firebaseref;
      let dates = {}
      this.loadedyear = true
    }

  }
}
</script>