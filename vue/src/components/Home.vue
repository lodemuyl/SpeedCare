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
    <div class="container">
      <div v-show="loggedin" class="row">
        <div class="col s12 m12 l4">
          <div class="card horizontal">
            <div class="card-stacked">
              <div class="card-content">
                <h5>Ritten</h5>
              </div>
              <div class="card-action">
                <a href="#">This is a link</a>
              </div>
            </div>
          </div>
        </div>
        <div class="col s12 m12 l4">
          <div class="card horizontal">
            <div class="card-stacked">
              <div class="card-content">
                <h5>Rapporten</h5>
              </div>
              <div class="card-action">
                <a href="#">This is a link</a>
              </div>
            </div>
          </div>
        </div>
        <div class="col s12 m12 l4">
          <div class="card horizontal">
            <div class="card-stacked">
              <div class="card-content">
                <h5>Account</h5>
              </div>
              <div class="card-action">
                <a href="#">This is a link</a>
              </div>
            </div>
          </div>
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
export default {
  name: 'Home',
  data () {
    return {
      loggedin: this.$parent.currentUser
    }
  },
  created () {    
  }
}
</script>