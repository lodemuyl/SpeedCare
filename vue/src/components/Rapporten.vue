<template>
  <div class="rapporten">
    <h2 class="pagetitle center">{{ msg }} {{  year }}</h2>
      <div class=""></div>
        <div class="row">
          <div class="col s12 md12 l12">
            <div>
                <select class="select" v-model="monthnumber" v-on:change="changemonth()">
                  <option v-for="(maand, index) in months"  v-bind:value="index" v-bind:selected="index == (monthnumber+1)" >{{maand.name}}</option>
                </select>
                <label>Selecteer jouw maand.</label>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col s12 md12 l12">
            <ul id="" class="tabs tabs tabs-fixed-width">
              <li class="tab col s3"><a :id="actiefoverzicht" href="#overzicht">Overzicht</a></li>
              <li class="tab col s3"><a :id="actiefsnelheid" href="#snelheid">Snelheidsovertredingen</a></li>
            </ul>
          </div>
          <div id="overzicht" class="col s12 md12 l12 sw">        
            <div class="card">
                  <div v-show="!loadoverzicht">
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
                  <div v-show="loadoverzicht" class="card-content white-text">
                    <span class="card-title halfstrong">Overzicht {{ monthname() }} {{ year }}</span>
                    <p>Hier krijgt u een percentueel overzicht van alle overtredingen.</p>
                    <table>
                      <thead>
                        <tr>
                            <th></th>
                            <th v-for="(percent, key) in percentages">{{key}}</th>                
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td><img :src="'../static/img/maxspeed/10.png'"></td>
                          <td v-for="speed in percentages" v-bind:class="{'rood bold': colorcondition(speed['10'])}" >{{ speed['10'] | percentfilter }}</td>
                        </tr>
                        <tr>
                          <td><img :src="'../static/img/maxspeed/30.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['30'])}" >{{speed['30'] | percentfilter }}</td>
                        </tr>
                        <tr>
                          <td><img :src="'../static/img/maxspeed/50.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['50'])}" >{{speed['50'] | percentfilter }}</td>
                        </tr>
                        <tr>
                          <td><img :src="'../static/img/maxspeed/70.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['70'])}" >{{speed['70'] | percentfilter }}</td>
                        </tr>
                         <tr>
                          <td><img :src="'../static/img/maxspeed/90.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['90'])}" >{{speed['90'] | percentfilter }}</td>
                        </tr> 
                        <tr>
                          <td><img :src="'../static/img/maxspeed/100.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['100'])}" >{{speed['100'] | percentfilter }}</td>
                        </tr>   
                        <tr>
                          <td><img :src="'../static/img/maxspeed/120.png'"></td>
                          <td v-for="speed in percentages"  v-bind:class="{'rood bold': colorcondition(speed['120'])}" >{{speed['120'] | percentfilter }}</td>
                        </tr>                       
                      </tbody>
                    </table>
                  </div>
            </div>
          </div>
          <div id="snelheid" class="col s12 md12 l12 sw">
                <div class="card">
                  <div v-show="!overtredingen">
                    <p class="noviolations"><span class="card-title halfstrong">Er zijn geen overtredingen vastgesteld voor {{ monthname() }}.</span></p>
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
                      <span class="card-title halfstrong overtredingenmaand">Overtredingen {{ monthname() }}</span>
                        <div  v-for="overtreding in overtredingenlistwatch">
                          <p class="dagnaam">{{overtreding.dagnaam}}</p>
                          <div class="ritten" v-for="rit in overtreding.ritten">
                            <p>Rit van {{rit.rit}}</p>
                            <div class="collection overtredingcollection" v-for="tijdstip in rit.logs">
                              <div class="collection-item"><p><img :src="'../static/img/maxspeed/' + tijdstip.info.maximumsnelheid + '.png'"></p><p>{{tijdstip.info.straat}}  {{tijdstip.info.nummer}}  {{tijdstip.info.postcode}} {{tijdstip.info.gemeente}}</p><p> om {{tijdstip.tijd}}</p><p class="right"><span class="rood">{{tijdstip.info.werkelijkesnelheid}}</span> km/h</p></div>
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
const over = {
        "0 tot 5 km/h": {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "5 tot 10 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "10 tot 20 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "+20 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
      }
export default {
  name: 'Rapporten',
  data () {
    return {
      msg: 'Rapporten',
      user: this.$parent.currentUser.providerData[0].displayName,
      firebaseref: db.ref(this.$parent.currentUser.uid), 
      loadoverzicht: false,
      loadedspeed: false,
      actiefoverzicht: this.$parent.actiefoverzicht,
      actiefsnelheid: this.$parent.actiefsnelheid,
      overtredingen: true,
      overtredingenaantal: 0,
      overtredingenlist: [],
      overtredingscategorie: over,
      year: moment(moment(), "YYYY").locale('nl').format('YYYY'),
      monthnumber: 0,
      options:{
        responsive: true
      },
      changed: false,
      months: [
        { name: "Januari", value: 1},
        { name: "Februari", value: 2},
        { name: "Maart", value: 3},
        { name: "April", value: 4},
        { name: "Mei", value: 5},
        { name: "Juni", value: 6},
        { name: "Juli", value: 7},
        { name: "Augustus", value: 8},
        { name: "September", value: 9},
        { name: "Oktober", value: 10},
        { name: "November", value: 11},
        { name: "December", value: 12}
        ]
    }
  },
  created(){
    this.speedviolations();
  },
  mounted(){
    //monthnumber
    this.monthnumber = new Date().getMonth()
    //materialize initialization
    var tabs = document.querySelector('.tabs'); 
    var firstclick = document.querySelector('#firstclick');
    var select = document.querySelector('.select');
    this.$nextTick(function(){ 
      var instances = M.Select.init(select);
      var tab = M.Tabs.init(tabs);    
      tab.updateTabIndicator();
      firstclick.click();            
    })
  },
  computed: {
    percentages: function(){ 
        let aantalovertredingen = this.overtredingenaantal
        let percentage = {}
        Object.keys(this.overtredingscategorie).forEach(key => {        
          percentage[key] = {}
        Object.keys(this.overtredingscategorie[key]).forEach(waarde =>{ 
          let huidigewaarde =  this.overtredingscategorie[key][waarde];
          let nieuwewaarde = (huidigewaarde / aantalovertredingen) * 100
          if (huidigewaarde == 0 && aantalovertredingen == 0){
            nieuwewaarde = 0
          }
          percentage[key][waarde] = Number(nieuwewaarde).toFixed(2);
        })
        });
        return percentage
      
    },
    overtredingenlistwatch: function(){
      console.log("lode")
      if(this.overtredingenlist){
        this.overtredingen = true
      }
      return this.overtredingenlist
    }
  },
  methods: {
    changemonth: function(){
      this.changed = true;    
      this.overtredingenaantal = 0
      this.overtredingenlist = [],
        this.overtredingscategorie = {
        "0 tot 5 km/h": {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "5 tot 10 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "10 tot 20 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        },
        "+20 km/h":  {
          "10": 0,
          "30": 0,
          "50": 0,
          "70": 0,
          "90": 0,
          "100": 0,
          "120": 0,
        }
      } 
      this.$forceUpdate()
      this.speedviolations()
    },
    speedviolations: function(){
      this.loadoverzicht = false;
      this.loadedspeed = false;
      //inladen lijst voor select.
      let all = db.ref(this.$parent.currentUser.uid)
      let jaar = new Date().getFullYear();
      let maand = this.monthnumber + 1
      all.child('overtredingen').child(jaar).child(maand).once('value', (snapshot)=>{
        let list =[]
      //ophalen van gewone rittendata overtredingen
        if(snapshot.val() !== null){   
              snapshot.forEach((dag)=>{
              let dagnummer = dag.key
              let dagobj = {
                "dag": dagnummer,
                "dagnaam": moment(dagnummer, "D").locale('nl').format('dddd LL'),
                "ritten": []
              }
              list.push(dagobj)
              dag.forEach((ritten)=>{
                let ritobj = {}
                let ritkey = ritten.key
                ritobj["rit"] = ritkey
                ritobj["logs"] = []
                dagobj["ritten"].push(ritobj)
                ritten.forEach((info)=>{
                  let infoobj = {}
                  infoobj["tijd"] = info.key
                  infoobj["info"] = []
                  ritobj["logs"].push(infoobj)
                  info.forEach((snapshot)=>{
                   let val = snapshot.val();
                   let maxspeed = val.maximumsnelheid;
                   let werkelijkesnelheid = val.werkelijkesnelheid
                   let tesnel = val.tesnel
                   this.overtredingenaantal += 1;
                   //this.overtredingscategorie[maxspeed] += 1
                   if(tesnel <= 5){
                      this.overtredingscategorie["0 tot 5 km/h"][maxspeed] += 1
                   }else if(tesnel > 5 && tesnel <= 10){
                      this.overtredingscategorie["5 tot 10 km/h"][maxspeed] += 1
                   }else if(tesnel > 10 && tesnel <= 20){
                      this.overtredingscategorie["10 tot 20 km/h"][maxspeed] += 1
                   }else if(tesnel > 20){
                     this.overtredingscategorie["+20 km/h"][maxspeed] += 1
                   };

                   infoobj["info"] = val;
                   infoobj["info"].werkelijkesnelheid =  Number(werkelijkesnelheid).toFixed(2);               
                  })
                })
              })
            })    
            //Vue.set(this.overtredingenlist, list)
          this.overtredingenlist = list                 
        }else{
          this.overtredingen = false; 
        }   
      }).then(()=>{
        this.changed == false
        this.loadoverzicht = true;
        this.loadedspeed = true;
      })     
    },
    colorcondition: function(param){
      if(param > 0.00){
        return true
      }else{
        return false
      }
    },
    monthname: function(){
      let name =  moment(moment().month(this.monthnumber), "YYYY-MM").locale('nl').format('MMMM')
      return name
    }
  },

  filters: {
    percentfilter: function(waarde){
      return waarde + ' %'
    }
  }
}
</script>