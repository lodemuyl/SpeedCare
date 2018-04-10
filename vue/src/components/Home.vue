<template>
  <div class="home">
    <div>
      <agile :arrows="false" :speed="750" :autoplaySpeed="8000" :fade="true":autoplay="true" :pauseOnHover="false">
        <div class="slide slide--1"></div>
        <div class="slide slide--2"></div>
        <div class="slide slide--3"></div>
        <div class="slide slide--4"></div>
      </agile>
    </div>
    <div class="container pannelview">
      <div v-show="loggedin">
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
        <div v-show="loaded" class="row pannelpadding">
          <router-link to="Ritten">        
            <div class="col pannelpadding s12 m12 l6 fullcard">
              <div class="card-panel grijsbackground fullheight">
                <span class="rood initchar ">{{ aantalritten }}</span>
                <span class="white-text bold">{{ naamritten }} deze maand</span>
                <br>
                <span class="white-text">Je hebt deze maand al {{ aantalritten }} {{ naamritten }} gereden.<br> Bekijk het overzicht van al jouw ritten waarna je alle ritten in detail kan bekijken.<br> Overtredingen worden tevens geregistreerd en bijgehouden.</span>
              </div>
            </div>
          </router-link>
          <router-link to="Rapporten">
            <div class="col pannelpadding s12 m12 l6 halfplus">
              <div class="card-panel groenbackground fullheight">
                <span class="rood initchar ">{{ aantalovertredingen }}</span>
                <span class="white-text bold">{{ naamovertredingen }} deze maand</span>
                <br>
                <span class="white-text">Je hebt deze maand al {{ aantalovertredingen }} {{ naamovertredingen }} in totaal gereden.<br> Elke overtreding die je op de weg begaat wordt geregistreerd en zal worden gebruikt voor jouw rijscore te bepalen.</span>
              
               </div>
            </div>
          </router-link>
          <router-link to="Account">
            <div class="col pannelpadding s12 m12 l6 halfminus">
              <div class="card-panel blauwbackground fullheight">
               <span class="rood initcharaccount">Account</span>
                <br>
                <span class="white-text">Bekijk jouw persoonlijke gegevens.</span>              
              </div>
            </div>
          </router-link>
          <router-link to="Over">          
            <div class="col pannelpadding s12 m12 l12 halfcard">
              <div class="card-panel groenbackground fullheight">
               <span class="rood initcharaccount">Speedcare</span>
                <br>
                <span class="white-text">Speedcare is een Bachelorproject in opdracht van de ArteveldeHogeschool. </span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
      <div v-show="!loggedin">
          <div class="columns is-mobile">
            <div class="column is-10 is-offset-1">
              <h1 class="center blauw titlefrontpage">SPEEDCARE</h1>
              <p class="center subtitle">SpeedCare is een systeem die de snelheid en locatie van jouw auto zal vastleggen. <br>Aan de hand van de maximumsnelheden kan je zien waar je te snel gereden hebt.<br>Indien jouw gps dongle nog niet geactiveerd is moet je deze eerst <router-link to="activeer" class="link">activeren</router-link>.<br>Indien je deze wel al hebt geactiveerd kan je gewoon <router-link to="login" class="link">inloggen</router-link>.</p>
            </div>
          </div>
          <div class="columns is-mobile logotext">
            <div class="column is-10 is-offset-1">  
              <div class="frontpageimages">
                <router-link to="/activeren"><img src="../assets/images/key.png"></router-link>
              </div>
              <h1 class="leftcenter notopmargin subtitlefrontpage">ACTIVEREN</h1>
              <p class="regulartext leftcenter">Elke module is voorzien van een unieke code die je moet ingeven bij je activering. Aan de hand van deze code worden jouw gegevens gelogd. Van zodra je account geactiveerd is met jouw unieke code van jouw dongle zal je alle registraties van jouw dongle kunnen bekijken.</p>
            </div>
          </div>
          <div class="columns is-mobile">
            <div class="column is-10 is-offset-1">  
              <div class="frontpageimages">
                <img src="../assets/images/maxsspeed.png">
              </div>
              <h1 class="rightcenter notopmargin subtitlefrontpage">MAXIMUMSNELHEDEN</h1>
              <p class="rightcenter regulartextfontsize">Bij elke locatie wordt nagegaan wat jouw werkelijke snelheid is en wat de maximum toegelaten snelheid is. Op basis hiervan zal een score berekend worden die je er zal op wijzen dat je al dan niet te snel gereden hebt. </p>
            </div>
          </div>
          <div class="columns is-mobile">
            <div class="column is-10 is-offset-1">  
              <div class="frontpageimages">
                <img src="../assets/images/maps.png">
              </div>
              <h1 class="leftcenter notopmargin subtitlefrontpage">LOCATIES</h1>
              <p class="leftcenter regulartextfontsize">De coordinaten van de afgelegde weg wordt geregistreerd zodat ze nadt je bent ingelogd overzichtelijk kan opvragen op een map.</p>
            </div>
          </div>
          <div class="columns is-mobile">
            <div class="column is-10 is-offset-1">  
              <div class="frontpageimages">
                <img src="../assets/images/settings.png">
              </div>
              <h1 class="rightcenter notopmargin subtitlefrontpage">HOE WERKT HET</h1>
              <p class="rightcenter regulartextfontsize">Vanaf het moment de dongle wordt aangezet en deze 4g verbinding heeft zal deze beginnen te loggen. Elke second wordt er een log gepushed met locatie en tijdstip. Aan de hand van deze logs kan je via dit platform een overzichtelijke weergave opvragen van jouw rijgedrag.</p>
            </div>
          </div>
      </div>
    </div>   
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import VueAgile from 'vue-agile'
Vue.use(VueAgile)
import { db } from '../assets/js/firebase'
export default {
  name: 'Home',
  data () {
    return {
      loggedin: this.$parent.currentUser,
      aantalritten: 0,
      aantalovertredingen: 0,
      loaded: false     
    }
  },
  computed: {
    naamritten: function(){
      if(this.aantalritten == 1){
        return "rit"
      }else{
        return "ritten"
      }
    },
    naamovertredingen: function(){
      if(this.aantalovertredingen == 1){
        return "overtreding"
      }else{
        return "overtredingen"
      }
    }
  },
  created () {
    if(this.loggedin){
      let vandaag = new Date();
      let all = db.ref(this.$parent.currentUser.uid)  
      let jaar = vandaag.getFullYear()
      let maand = vandaag.getMonth()+1
      this.ritten(jaar, maand, all);
      this.overtredingen(jaar, maand, all);
    }
  },
  methods: {
    ritten: function(jaar, maand, all){
        all.child('aantalritten').child(jaar).child(maand).once('value').then((val)=>{
          this.aantalritten = val.val()
          })
    },
    overtredingen: function(jaar, maand , all){
       all.child('aantalovertredingen').once('value', (snapshot)=>{
         if(snapshot.exists()){
           this.aantalovertredingen = snapshot.child(jaar).child(maand).val()
         }
       }).then(()=>{
         this.loaded = true
       })
    }
  }
}
</script>