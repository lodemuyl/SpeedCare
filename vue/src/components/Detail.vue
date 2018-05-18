<template>
  <div class="detail">
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
        <h2 class="pagetitle center">{{ datum | datumnederlands }}</h2>
        <div class="pannel">
            <div class="leftside" id="leftside">
                <gmap-map  :zoom="ritmetadata.zoom" map-type-id="terrain" :center="ritmetadata.center"  mapTypeId: google.maps.MapTypeId.ROADMAP style="width: 100%; height: 100%">
                    <gmap-polyline class="polyline"
                        :path="coordinates"
                        :editable="routedetail"
                        :dragable ="false"
                        :options="{strokeColor: '#CF2E5E'}" 
                        @click="polylinepointclick($event)"                       
                        ref="polygon">
                    </gmap-polyline>
                    <info-window :opened="infoWinOpen['open']" :position="infoWinOpen['position']" @closeclick="infoWinOpen['open']=false" class="infowindow">
                        <img :src="infoWinOpen.content.speedim" class="popupspeedim">
                        <span :class="{groen: infoWinOpen.class.groen, rood: infoWinOpen.class.rood}" class="strong">{{ infoWinOpen.content.speed }} </span>
                        <span class="strong">km/u</span>
                        <div class="infowindowextratextdiv" v-show="infoWinOpen.content.uur">
                            <p class="infowindowextratext grijs">Om <span class="rood">{{ infoWinOpen.content.uur }}</span> hebt u een overtreding begaan in de <span class="rood">{{ infoWinOpen.content.plaats }}.</span></p>
                        </div>
                    </info-window>
                    <gmap-marker :position="startlocation" :icon="icons.start"></gmap-marker>
                    <gmap-marker :position="endlocation" :icon="icons.stop"></gmap-marker>

                </gmap-map>
            </div>
            <div class="rightside">
                <div class="container">
                    <p class="subtitle">Info</p>
                    <div class="row">
                        <div class="col s12 m6 l6">
                            <div><i class="material-icons rood infoicons">date_range</i><p class="inlineinfo">{{ datum | datumnederlands }}</p></div>
                            <div><i class="material-icons rood infoicons">access_time</i><p class="inlineinfo">{{ ritmetadata.start }} - {{ ritmetadata.einde }}</p></div>
                            <div><i class="material-icons rood infoicons">account_circle</i><p class="inlineinfo">{{ user }}</p></div>
                        </div>
                        <div class="col s12 m6 l6">
                            <div><i class="material-icons rood infoicons">timer</i><p class="inlineinfo">{{ ritmetadata.duur }}</p></div>
                            <div><i class="material-icons rood infoicons">directions_car</i><p class="inlineinfo">{{ ritmetadata.hoogstesnelheid }} km/u</p></div>
                            <div><i class="material-icons rood infoicons">assessment</i><p class="inlineinfo">{{ score }} / 100</p></div>
                        </div>
                    </div>
                    <p class="subtitle">Bekijk gedetailleerde route</p>
                    <div class="row">
                        <div class="col s12 m12 l12">
                            <div class="switch">
                                <label>
                                <span class="wit">Af</span>
                                <input type="checkbox" v-model="routedetail">
                                <span class="lever"></span>
                                <span class="wit">Aan</span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <p class="overtredingenclick subtitle" v-on:click="violationspage"><span>Overtredingen</span> <span v-show="amountviolations.length != 0">({{ amountviolations }} <span class="totaalovertredingentext">in totaal</span>)</span> </p>
                    <div class="row">
                        <div v-show="violations.length">                        
                            <ul class="collapsible">
                                <li v-for="violation in uniqueviolations">
                                   <a class="violationclick" v-scroll-to="'#leftside'" v-on:click="showviolationdetail" :time="violation.tijd" :street="violation.straat" :number="violation.nummer" :city="violation.gemeente" :max="violation.maximumsnelheid" :speed="violation.werkelijkesnelheid" :lat="violation.lat" :lng="violation.lng"> 
                                        <div class="collapsible-header">
                                            <img class ="maxspeedsign" :src="violation.url">
                                            <span class="overtredingstijd">{{ violation.tijd }}</span>
                                            <div class="paxspeedtext">{{ violation.straat }} {{ violation.nummer }}  {{ violation.gemeente }}</div>                                    
                                            <span class="new badge red">{{ violation.werkelijkesnelheid }} km/u</span>
                                        </div>   
                                    </a> 
                                </li>
                            </ul>
                        </div>
                        <div v-show="!violations.length">
                            <p>U hebt geen overtredingen begaan op deze rit</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="topside">
            <div class="container">
                <div class="row">               
                    <p class="subtitle">Overtredingen uitgedrukt in percentage.</p>
                    <chartjs-doughnut  :datalabel="'rapport'" :option="options" :labels="labels" :data="data" :scalesdisplay="scale" :backgroundcolor="backgroundcolor" :bordercolor="'rgba(72,72,72,0.8)'" :hoverbackgroundcolor="backgroundcolor" :hoverbordercolor="'rgba(72,72,72,0.8)'"></chartjs-doughnut>
                </div>
            </div>
        </div>
        <div v-show="errormessage" class="container">
            <div class="col s12 m12 l12">
                <div class="card-panel roodbackground ">
                    <span class="grijs">{{errormessage}}</span>
                </div>
            </div> 
        </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */  
import { alldata } from '../assets/js/firebase'
import { actief } from '../assets/js/firebase'
import { db } from '../assets/js/firebase' 
import Vue from 'vue'
import axios from 'axios'
import uniq from 'lodash/uniq'
import moment from 'moment'
import * as VueGoogleMaps from 'vue2-google-maps'
import 'moment/locale/nl';
import VueScrollTo from 'vue-scrollto'
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyBRG_RCT37qOM0FoRvX-CZWEH0pu6DzWpk',
    libraries:'geometry',
    language: 'nl'
  }
})

Vue.use(VueScrollTo, {
     container: "body",
     duration: 500,
     easing: "ease",
     offset: -40,
     cancelable: true,
     onStart: false,
     onDone: false,
     onCancel: false,
     x: false,
     y: true
 })
Vue.component('infoWindow', VueGoogleMaps.InfoWindow)
export default {
  name: 'Detail',
  data () {
    return {
      loaded: false,
      ritmetadata: {
          "start": null,
          "einde": null,
          "duur": null,
          "hoogstesnelheid": null,
          "center": {
            "lat": 10,
            "lng": 10
          },
          "zoom": 11
      },
      amountviolations: 0,
      coordinates: [],
      violations: [],    
      routedetail: false,
      firebaseref: db.ref(this.$parent.currentUser.uid),
      icons: {
          "start": '/static/img/icons/start.png',
          "stop": '/static/img/icons/end.png'
      },
      user: this.$parent.currentUser.displayName,
      startlocation: {
          "lat": 10,
          "lng": 10
      },
      labels: [],
      scale: false,
      data: [],
      backgroundcolor: ['rgba(80,185,72, 0.8)','rgba(183,200,55, 0.8)','rgba(252,196,0, 0.8)','rgba(237,122,27,0.8)','rgba(198,0,15,0.8)'],
      options:{
        responsive: true,
        beginAtZero: false,
        border: false,
        legend: {
            position: 'left',
            display: true,
            labels: {
                fontColor: '#ffffff'
            }
        }
      },
      endlocation: {
          "lat": 10,
          "lng": 10
      },
      infoWinOpen: {
          "open": false,
          "position": {
              "lat": 50.8928966,
              "lng": 3.9989016
          },
          "content": {
              "speedim": null,
              "speed" : null,
              "uur" : null,
              "plaats" : null
          },
          "class": {
              "groen": true,
              "rood": false
          }
      },
      score: 0,
      overtredingscategorie: {
          "zwak": 0,
          "medium": 0,
          "zwaar": 0,
          "zeerzwaar": 0
      },
      overtredingspercentages: {
          "zwak": 0,
          "medium": 0,
          "zwaar": 0,
          "zeerzwaar": 0,
          "overtredingentotaal": 0
      },
      datum: this.$route.params.datum,
      tijd: this.$route.params.tijd,
      errormessage: null,
    }
  },
  created(){
    if (this.checkparam(this.datum, this.tijd)){
        this.main(this.datum, this.tijd);
    }else{
        this.$router.push('/Ritten')
    }  
  },
  computed: {
    //overtredingsduplicaten verwijderen en hoogste snelheid loggen
    uniqueviolations: function() {
        let filter = [];
        let list = [];
        for(var i =0; i < this.violations.length; i++) { 
            if(filter.indexOf(this.violations[i].straat) === -1) { 
                filter.push(this.violations[i].straat) 
                list.push(this.violations[i])  
            }else{         
                let index = filter.indexOf(this.violations[i].straat)
                if(list[index].werkelijkesnelheid < this.violations[i].werkelijkesnelheid){
                    list[index].werkelijkesnelheid = this.violations[i].werkelijkesnelheid
                }
            }
        }
        return list;
    }
  },
  methods: {
      checkparam: function(datum, tijd){
        //datum
        let matchesd = /^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$/.exec(datum);
        let matchesh = /^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$/.exec(tijd);
        if (matchesd == null) return false;
        if (matchesh == null) return false;
        else return true
      },
      main: function(datum, tijd){
        let all = this.firebaseref;
        let iso = moment(datum, "YYYY-MM-DD");
        let jaar = iso.format('YYYY');
        let maand = iso.format('M');
        let dag = iso.format('D');
        if(datum && tijd){
            all.child(jaar).child(maand).child(dag).child(tijd).once('value', (rit)=>{
                //ophalen van gewone rittendata
                if(rit.val() !== null){
                    //toekennen vertrekmoment
                    this.ritmetadata.start = tijd
                    //ophalen alle logs
                    rit.forEach((timestamp)=>{
                        let key = timestamp.key;
                        let log = timestamp.val();
                        let info = Object.values(log)[0];
                        //maximumsnelheid toekennen
                        (info['snelheid'] > this.ritmetadata.hoogstesnelheid) ? (this.ritmetadata.hoogstesnelheid = Number(info['snelheid']).toFixed(2)) : false;
                        //aangepaste objecten toevoegen aan array voor route weer te geven
                        let pointinfo = {
                            'lat': info['lat'],
                            'lon': info['lon'],
                            'maxsnelheid': info['maxsnelheid'],
                            'werkelijkesnelheid': info['snelheid'],
                            'signaal': info['signaal'],
                            'tijd' : key
                            };
                        let objcoordinates ={
                            'lat': Number(info['lat']),
                            'lng': Number(info['lon']),
                            'info': pointinfo
                        };
                        this.coordinates.push(objcoordinates)
                     })
                     //toekennen einde rit + duur
                    let laatste  = this.coordinates[this.coordinates.length - 1]
                    let eerste = this.coordinates[0]                                 
                    this.ritmetadata.einde = laatste.info.tijd;
                    this.ritmetadata.duur = moment.utc(moment(this.ritmetadata.einde,"HH:mm:ss").diff(moment(this.ritmetadata.start,"HH:mm:ss"))).format("HH:mm:ss")
                    //registreren start en eindmarker
                    this.startlocation.lat = eerste.lat;
                    this.startlocation.lng = eerste.lng;
                    this.endlocation.lat = laatste.lat;
                    this.endlocation.lng = laatste.lng;
                    //center van view
                    this.ritmetadata.center.lat = this.centermap().lat;
                    this.ritmetadata.center.lng = this.centermap().lng;
                    this.ritmetadata.zoom = this.centermap().zoom;
                }else{
                     this.$router.push('/Ritten')
                }              

            }).then(()=>{
                //dan ophalen van overtredingen
                all.child('overtredingen').child(jaar).child(maand).child(dag).child(tijd).once('value', (rit)=>{
                if(rit.val() !== null){
                        rit.forEach((overtreding)=>{
                            let key = overtreding.key;
                            let log = overtreding.val();
                            let info = Object.values(log)[0];
                            info.tijd = key;
                            info.url = '../static/img/maxspeed/'+ info.maximumsnelheid +'.png';
                            info.werkelijkesnelheid = Number(info.werkelijkesnelheid).toFixed(2);
                            let tesnel = Number(info.tesnel);
                            this.violations.push(info);
                            if(tesnel <= 5){
                                this.overtredingscategorie.zwak += 1
                            }else if(tesnel > 5 && tesnel <= 10){
                                this.overtredingscategorie.medium += 1
                            }
                            else if(tesnel > 10 && tesnel <= 20){
                                this.overtredingscategorie.zwaar += 1    
                            }else if(tesnel > 20){
                                this.overtredingscategorie.zeerzwaar += 1 
                            }       
                        })
                        //aantalovertredingen
                        this.amountviolations = this.violations.length
                }else{

                }
            }).then(()=>{
                this.ritscore();
                this.loaded = true
            })
            })

        }else{
            this.$router.push('/Ritten')                  
        }
      },
      showviolationdetail: function(event){
            let lat = Number(event.currentTarget.attributes['lat'].value);
            let lng = Number(event.currentTarget.attributes['lng'].value);
            let max = event.currentTarget.attributes['max'].value;
            let werkelijkesnelheid =  event.currentTarget.attributes['speed'].value;
            this.infoWinOpen.position.lat = lat;
            this.infoWinOpen.position.lng = lng;
            this.infoWinOpen.content.speed = Number(werkelijkesnelheid).toFixed(2);
            this.infoWinOpen.content.speedim = './static/img/maxspeed/' + max + '.png';
            let plaats = event.currentTarget.attributes['street'].value + " " + event.currentTarget.attributes['number'].value + " te " + event.currentTarget.attributes['city'].value;
            this.infoWinOpen.content.plaats = plaats;
            this.infoWinOpen.content.uur = event.currentTarget.attributes['time'].value;
            if(Number(max) >= werkelijkesnelheid){
                this.infoWinOpen.class.groen = true;
                this.infoWinOpen.class.rood = false;
            }else{
                this.infoWinOpen.class.groen = false;
                this.infoWinOpen.class.rood = true;
            };         
            this.infoWinOpen.open = true       
      },
      polylinepointclick: function(event){
          if(event.vertex){
            console.log(event.vertex)
            let info = this.coordinates[event.vertex].info
            let maxsnelheid = this.precisionRound(Number(info.maxsnelheid), 2);
            let werkelijkesnelheid = this.precisionRound(Number(info.werkelijkesnelheid), 2);
            this.infoWinOpen.content.uur = null
            this.infoWinOpen.content.plaats = null
            this.infoWinOpen.position.lat = event.latLng.lat()
            this.infoWinOpen.position.lng = event.latLng.lng()
             this.infoWinOpen.content.speed = werkelijkesnelheid
             this.infoWinOpen.content.speedim = './static/img/maxspeed/' + info.maxsnelheid + '.png'
             if(maxsnelheid >= werkelijkesnelheid){
                this.infoWinOpen.class.groen = true
                this.infoWinOpen.class.rood = false
             }else{
                this.infoWinOpen.class.groen = false
                this.infoWinOpen.class.rood = true
             }
            this.infoWinOpen.open = true
        }
      },
      centermap: function(){      
          let start = this.startlocation
          let end = this.endlocation
          return {
              "lat" : start.lat,
              "lng" : start.lng,
              "zoom" : 14
          }
      },
      violationspage: function(){
          this.$parent.actiefoverzicht = null;
          this.$parent.actiefsnelheid = "firstclick",
          this.$router.push('/Rapporten')

      },
      ritscore: function(){
          let aantallogs = Number(this.coordinates.length)
          let aantalovertredingen = ((Number(this.amountviolations) / aantallogs) * 100).toFixed(2)
          let zwak = Number((this.overtredingscategorie.zwak / aantallogs) * 100).toFixed(2)
          let medium = Number((this.overtredingscategorie.medium / aantallogs) * 100).toFixed(2)
          let zwaar = Number((this.overtredingscategorie.zwaar / aantallogs) * 100).toFixed(2)
          let zeerzwaar = Number((this.overtredingscategorie.zeerzwaar / aantallogs) * 100).toFixed(2)
          this.overtredingspercentages.overtredingentotaal =  aantalovertredingen
          this.overtredingspercentages.zwak =  zwak
          this.overtredingspercentages.medium =  medium
          this.overtredingspercentages.zwaar =  zwaar
          this.overtredingspercentages.zeerzwaar =  zeerzwaar  
          let safe = Number(100-aantalovertredingen)
          this.score = safe.toFixed(2)
          this.labels.push("Geen overtredingen");
          this.labels.push("Zwakke overtredingen (- 5 km/h)");
          this.labels.push("Medium overtredingen (5 - 10km/h)")
          this.labels.push("Zware overtredingen (10 - 20 km/h)")
          this.labels.push("Zeer zware overtredingen (20 - km/h)")
          this.data.push(safe )
          this.data.push(zwak )
          this.data.push(medium )
          this.data.push(zwaar )
          this.data.push(zeerzwaar)
      },
      precisionRound: function(number, precision) {
        var factor = Math.pow(10, precision);
        return Math.round(number * factor) / factor;
      }

  },
  filters: {
      datumnederlands: function(datum){
            if(datum){
               let iso = moment(datum, "YYYY-MM-DD")
               let nederlands = iso.locale('nl').format('LL')
               return nederlands
            }else{
                return false
            }
        }
  }
}
</script>