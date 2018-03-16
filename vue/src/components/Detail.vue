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
            <div class="leftside">
                <gmap-map :center="center"  :zoom="14" map-type-id="terrain"  style="width: 100%; height: 100%">
                    <gmap-polyline class="polyline"
                        :path="coords" 
                        :editable="routedetail"
                        :dragable ="false"
                        :options="{strokeColor: '#CF2E5E'}" 
                        @click="polylinepointclick($event)"                       
                        ref="polygon">
                    </gmap-polyline>
                    <info-window :opened="infoWinOpen['open']" :position="infoWinOpen['position']" @closeclick="infoWinOpen['open']=false" class="infowindow"><img :src="infoWinOpen.content.speedim" class="popupspeedim"><span :class="{groen: infoWinOpen.class.groen, rood: infoWinOpen.class.rood}" class="strong">{{ infoWinOpen.content.speed }} </span><span class="strong">km/u</span></info-window>
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
                            <div><i class="material-icons rood infoicons">access_time</i><p class="inlineinfo">{{ start }} - {{ end }}</p></div>
                            <div><i class="material-icons rood infoicons">account_circle</i><p class="inlineinfo">{{ user }}</p></div>
                        </div>
                        <div class="col s12 m6 l6">
                            <div><i class="material-icons rood infoicons">timer</i><p class="inlineinfo">{{ duur }}</p></div>
                            <div><i class="material-icons rood infoicons">directions_car</i><p class="inlineinfo">{{ highestspeed }} km/u</p></div>
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
                    <p class="subtitle">Overtredingen</p>
                    <div class="row">
                        <div v-show="violationslist.length ">                        
                            <ul class="collapsible">
                                <li v-for="overtreding in uniqueviolations">
                                   <a v-on:click="showviolationdetail" class="violationclick" :speed="overtreding.werkelijkesnelheid" :max="overtreding.maximumsnelheid" :lat="overtreding.lat" :lng="overtreding.lon">
                                        <div class="collapsible-header">
                                            <img class ="maxspeedsign" :src="overtreding.url">
                                            <span class="overtredingstijd">{{ overtreding.tijd }}</span>
                                            <div class="paxspeedtext">{{overtreding.address}}</div>                                    
                                            <span class="new badge red">{{ overtreding.werkelijkesnelheid }} km/u</span>
                                        </div>   
                                    </a> 
                                </li>
                            </ul>
                        </div>
                        <div v-show="!violationslist.length">
                            <p>U hebt geenovertredingen begaan op deze rit</p>
                        </div>
                    </div>
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
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyBRG_RCT37qOM0FoRvX-CZWEH0pu6DzWpk',
    libraries:'geometry',
    language: 'nl'
  }
})
Vue.component('infoWindow', VueGoogleMaps.InfoWindow)
export default {
  name: 'Detail',
  data () {
    return {
      loaded: false,
      routedetail: false,
      firebaseref: db.ref(this.$parent.currentUser.uid),
      icons: {
          "start": '/static/img/icons/start.png',
          "stop": '/static/img/icons/end.png'
      },
      center: {
          "lat": 10,
          "lng": 10
      },
      user: this.$parent.currentUser.displayName,
      logs: {},
      startlocation: {
          "lat": 10,
          "lng": 10
      },
      endlocation: {
          "lat": 10,
          "lng": 10
      },
      start: null,
      infoWinOpen: {
          "open": false,
          "position": {
              "lat": 50.8928966,
              "lng": 3.9989016
          },
          "content": {
              "speedim": null,
              "speed" : null,

          },
          "class": {
              "groen": true,
              "rood": false
          }
      },
      duur: null,
      end: null,
      highestspeed: 0,
      violationslist: [],
      score: 0,
      datum: this.$route.params.datum,
      tijd: this.$route.params.tijd,
      errormessage: null,
      coords: []
    }
  },
  created(){
    if (this.checkparam(this.datum, this.tijd)){
        this.violations(this.datum, this.tijd);
    }else{
        this.$router.push('/Ritten')
    }  
  },
  computed: {
    //overtredingsduplicaten verwijderen en hoogste snelheid loggen
    uniqueviolations: function() {
    let filter = [];
    let list = [];
        for(var i =0; i < this.violationslist.length; i++) {
            if(filter.indexOf(this.violationslist[i].address) === -1) {
                filter.push(this.violationslist[i].address)
                list.push(this.violationslist[i])
            }else{
                let index = filter.indexOf(this.violationslist[i].address)
                if(list[index].tesnel < this.violationslist[i].tesnel){
                    list.splice(index,1)
                    list.push(this.violationslist[i])
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
        let m = matchesd[2];
        let y = matchesd[1] - 1;
        let d = matchesd[3];
        let h = matchesh[1];
        let min = matchesh[2];
        let s = matchesh[3];
        let composedDate = new Date(y, m, d, h, min, s);
        //tijd
        return composedDate.getDate() == d &&
               composedDate.getMonth() == m &&
               composedDate.getFullYear() == y &&
               composedDate.getHours() == h &&
               composedDate.getMinutes() == min &&
               composedDate.getSeconds() == s;


      },
      violations: function(datum, tijd){
          if(datum && tijd){
            let all = this.firebaseref
            let ritdate = new Date(datum)
            let jaar = ritdate.getFullYear();
            let maand = ritdate.getMonth()+1;
            let dag = ritdate.getDate();
            let self = this;
            let keys = [];
            let data = {};
            all.child(jaar).child(maand).child(dag).child(tijd).once('value', (snapshot) => {
                snapshot.forEach(function(childSnapshot) { 
                    let key = childSnapshot.key;  
                    let childData = childSnapshot.val();
                    let childData2 = Object.values(childData)[0];
                    (childData2['snelheid'] > self.highestspeed) ? (self.highestspeed = Number(childData2['snelheid']).toFixed(2)) : false;
                    //elke log wegschrijven in eigen object voor verdere functies 
                    let datacontent = {
                        'lat': childData2['lat'],
                        'lon': childData2['lon'],
                        'maxsnelheid': childData2['maxsnelheid'],
                        'werkelijkesnelheid': childData2['snelheid'],
                        'signaal': childData2['signaal'],
                        'tijd' : key
                    }
                    data[key] = datacontent
                    //array vullen voor een lijst van alle tijdspunten voor zo het center te bepalen
                    keys.push(key);
                    //lat en long wegschrijven naar de coords array voor de route op de map weer te geven
                    let coords = {
                        'lat': Number(childData2['lat']),
                        'lng': Number(childData2['lon']),
                        'info': datacontent
                    }
                    self.coords.push(coords)
                    if(childData2['snelheid'] > childData2['maxsnelheid']){
                        let tesnel = Number(childData2['snelheid']) - Number(childData2['maxsnelheid']);
                        //violation logs
                        let violationdata = {
                            'werkelijkesnelheid': Number(childData2['snelheid']).toFixed(2),
                            'maximumsnelheid': childData2['maxsnelheid'],
                            'url': '../static/img/maxspeed/' + childData2['maxsnelheid'] + '.png',
                            'lat': childData2['lat'],
                            'lon': childData2['lon'],
                            'tijd': key,
                            'tesnel':  tesnel.toFixed(2),
                            'address': 'geen adres'
                        };
                        //assign van alle overtredingen
                        self.violationslist.push(violationdata)                  
                        //ophalen van locatie van overtredingen
                        self.getstreetname(Number(childData2['lat']), Number(childData2['lon']), self.violationslist.length)
                    }                   

                });
                if(Object.keys(data).length === 0){
                    self.logs = null;
                }else{
                    self.logs = data;
                    //start en stop tijd
                    self.start = Object.keys(data)[0]
                    self.end = Object.keys(data)[Object.keys(data).length - 1]
                    //start en stop locatie
                    Vue.set(self.startlocation, "lat", Number(data[self.start]["lat"]))
                    Vue.set(self.startlocation, "lng", Number(data[self.start]["lon"]))
                    Vue.set(self.endlocation, "lat", Number(data[self.end]["lat"]))
                    Vue.set(self.endlocation, "lng", Number(data[self.end]["lon"]))
                    //verschil in tijdseenheden voor duurpebaling 
                    let start = new Date("01/01/2010 " + self.start);
                    let end = new Date("01/01/2010 " + self.end);
                    let difference = end - start;
                    let diff_result = new Date(difference);
                    diff_result.setHours(diff_result.getHours()-1);
                    self.duur =  moment(diff_result).locale('nl').format('LTS')
                    this.getcenter(data, keys);
                    this.getscore()

                }
                this.loaded = true
            })
          }else{
            this.$router.push('/Ritten')                  
          }
      },
      getstreetname: function(lat, lon, lengte){  
            axios.get(`https://maps.googleapis.com/maps/api/geocode/json?`, {
                params: {
                    key: this.$parent.mapsapikey,
                    latlng: lat + ',' + lon
                }       
            })
            .then((val) => {
                if(val.data.status === "OK"){
                    this.violationslist[lengte-1]['address'] = val.data.results[0]['formatted_address']
                }else{
                    this.errormessage = val.data.status;
                    console.log('kan het adres niet ophalen')
                    this.violationslist[lengte-1]['address'] = 'kon locatie niet ophalen'
                }
            }).catch(e => {
                this.errormessage = e.message
            })         
      },
      getcenter: function(data, keys){
        let centernumber = 0
        if(Object.keys(data).length == 1){
            centernumber = 0
        }else if(Object.keys(data).length % 2 == 0){
            centernumber = (Object.keys(data).length / 2)-1
        }else if(Object.keys(data).length % 2 != 0){
            centernumber = Math.round((Object.keys(data).length / 2)-1)
        }
        let key = keys[centernumber]
        let centerobjectkey = data[key]
        let lat = parseFloat(centerobjectkey['lat'])
        let lng = parseFloat(centerobjectkey['lon'])
        this.center['lat'] = lat
        this.center['lng'] = lng
      },
      polylinepointclick: function(event){
          if(event.vertex){
            let info = this.coords[event.vertex].info
            this.infoWinOpen.position.lat = event.latLng.lat()
            this.infoWinOpen.position.lng = event.latLng.lng()
            this.infoWinOpen.content.speed = Number(info.werkelijkesnelheid).toFixed(2)
            this.infoWinOpen.content.speedim = './static/img/maxspeed/' + info.maxsnelheid + '.png'
            if(Number(info.maxsnelheid) >= info.werkelijkesnelheid){
                this.infoWinOpen.class.groen = true
                this.infoWinOpen.class.rood = false
             }else{
                this.infoWinOpen.class.groen = false
                this.infoWinOpen.class.rood = true
             }
            this.infoWinOpen.open = true
          }else{
              this.infoWinOpen.open = false
              console.log("tussenliggend punt")
          }
      },
      showviolationdetail: function(event){
        let lat = Number(event.currentTarget.attributes['lat'].value)
        let lng = Number(event.currentTarget.attributes['lng'].value)
        let max = event.currentTarget.attributes['max'].value
        let werkelijkesnelheid = event.currentTarget.attributes['speed'].value
        this.infoWinOpen.position.lat = lat
        this.infoWinOpen.position.lng = lng
        this.infoWinOpen.content.speed = Number(werkelijkesnelheid).toFixed(2)
        this.infoWinOpen.content.speedim = './static/img/maxspeed/' + max + '.png'
        if(Number(max) >= werkelijkesnelheid){
            this.infoWinOpen.class.groen = true
            this.infoWinOpen.class.rood = false
        }else{
            this.infoWinOpen.class.groen = false
            this.infoWinOpen.class.rood = true
        }
        this.infoWinOpen.open = true
      },
      getscore: function(){
        if(this.violationslist.length > 0){
            let coefficient = 1;
            let scoreopaantal = 100 - ((this.violationslist.length / this.coords.length)*100)
            let totaaltesnel = 0
            this.violationslist.forEach((e)=>{
                totaaltesnel += Number(e.tesnel)
            })
            let gemiddeldtesnel = totaaltesnel / this.violationslist.length
            if(gemiddeldtesnel < 10 && gemiddeldtesnel > 5){
                coefficient = 0.98
            }else if(gemiddeldtesnel >= 10 && gemiddeldtesnel < 20){
                coefficient = 0.9
            }else if(gemiddeldtesnel > 20){
                coefficient = 0.8
            }
            this.score = Number(scoreopaantal * coefficient).toFixed(2)
        }else{
            this.score = 100
        }
      }
  },
  filters: {
      datumnederlands: function(datum){
            if(datum){              
                return moment(datum).locale('nl').format('LL')
            }else{
                return false
            }
        }
  }
}
</script>