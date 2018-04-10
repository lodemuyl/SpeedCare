<template>
  <div id="app">
      <nav class="blauwbackground">
        <div class="nav-wrapper">
          <router-link to="/home" class="brand-logo center"><img class="navlogo" src="./assets/images/logo1.png" alt="SpeedCare"></router-link>
          <a href="#" data-target="mobile-demo" class="sidenav-trigger right"><i class="material-icons">menu</i></a>
          <ul id="nav-mobile" class="right hide-on-med-and-down">
            <li v-show="!currentUser"><router-link to="/Login"><i class="material-icons left">input</i>Login</router-link></li>
            <li v-show="!currentUser"><router-link to="/Activeer"><i class="material-icons left">loupe</i>Activeren</router-link></li>
            <li v-show="currentUser"><router-link to="/Ritten"><i class="material-icons left">view_list</i>Ritten</router-link></li>
            <li v-show="currentUser"><router-link to="/Rapporten"><i class="material-icons left">show_chart</i>Rapporten</router-link></li>
            <li v-show="currentUser"><router-link to="/Account"><i class="material-icons left">person_pin</i>Account</router-link></li>
            <li v-show="currentUser" v-on:click="logout"><a><i class="material-icons left">power_settings_new</i>Logout</a></li>
          </ul>
          <ul id="mobile-demo" class="sidenav">
            <li v-on:click="close"><div class="user-view">
              <div class="background">
                <img src="./assets/images/sidenav.png">
              </div>
              <router-link to="/Account" v-if="currentUser"><img class="circle" :src="profilepicurl"></router-link>
              <router-link to="/Account" v-if="currentUser"><span class="name">{{ currentUser.displayName }}</span></router-link>
              <router-link to="/Account" v-if="currentUser"><span class="email">{{ currentUser.email }}</span></router-link>
            </div></li>
            <li v-show="!currentUser" v-on:click="close"><router-link to="/Login"><i class="material-icons">input</i>Login</router-link></li>
            <li v-show="!currentUser" v-on:click="close"><router-link to="/Activeer"><i class="material-icons">loupe</i>Activeren</router-link></li>
            <li v-show="currentUser" v-on:click="close"><router-link to="/Ritten"><i class="material-icons">view_list</i>Ritten</router-link></li>
            <li v-show="currentUser" v-on:click="close"><router-link to="/Rapporten"><i class="material-icons">show_chart</i>Rapporten</router-link></li>
            <li v-show="currentUser"><div class="divider"></div></li>
            <li v-show="currentUser"><a class="subheader">Account</a></li>
            <li v-show="currentUser" v-on:click="close"><router-link to="/Account"><i class="material-icons">person_pin</i>Mijn account</router-link></li>
            <li v-show="currentUser" v-on:click="logout"><a><i class="material-icons">power_settings_new</i>Logout</a></li>
          </ul>
        </div>
      </nav>
      <main>      
        <router-view></router-view>
      </main>
      <footer class="page-footer blauwbackground">
          <div class="container">
            <div class="row">
              <div class="col l6 s12">
                <h5 class="groen">SpeedCare</h5>
                <p class="beige">SpeedCare is een bachelorproef geschreven in opdracht van Arteveldehogeschool. </p>
              </div>
              <div class="col l3 s12">
                <h5 class="groen">Algemeen</h5></h5>
                <ul>
                  <li><router-link class="grey-text text-lighten-3" to="Disclaimer">Disclaimer</router-link></li>
                  <li><a class="grey-text text-lighten-3" href="mailto:lodemuyl@student.arteveldehs.be">Contact</a></li>
                  <li><router-link to="Over" class="grey-text text-lighten-3">Over</router-link></li>
                  <li v-show="!currentUser"><router-link to="Admin" class="grey-text text-lighten-3">Admin</router-link></li>
                </ul>
              </div>
              <div class="col l3 s12">
                <h5 class="groen">Social Media</h5>
                <ul>
                  <li><a class="grey-text text-lighten-3" target="_blank" href="https://www.facebook.com/lode.muylaert">Facebook</a></li>
                  <li><a class="grey-text text-lighten-3" target="_blank" href="https://twitter.com/LodeMuylaert?lang=nl">Twitter</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div class="footer-copyright">
            <div class="container">
            © 2018 Copyright - <router-link class="grey-text text-lighten-3" to="Disclaimer"><strong class="rood">www.speedcare.herokuapp.com </strong></router-link>
            <a class="grijs right" target="_blank" href="http://lodemuylaert.be">Auteur</a>
            </div>
        </div>
      </footer>
  </div>
</template>

<script>
/* eslint-disable */
import firebase from 'firebase';
import { db } from './assets/js/firebase'
import moment from 'moment'
var elem;
var instance;

export default {
  name: 'app',
  data () {
    return {
      currentUser: firebase.auth().currentUser,
      uid: null,
      profilepicurl: '../static/img/user.png',
      mapsapikey: 'AIzaSyCjDB7jB1CqPueuUcUPXj1LBxMmob3iF1M',
      actiefjaar: "firstclick",
      actiefsnelheid: null,
    }
  },
  created(){
  },
  mounted: function(){
    this.$nextTick(function(){
      let options = {
        edge: 'right'
      }
      elem = document.querySelector('.sidenav');
      instance = M.Sidenav.init(elem, options);
    })   
  }, 
  methods: {
    close: function(){
      instance.close();
    },
    logout: function(){
      let ref = this.currentUser.uid + "/actief"
      db.ref(ref).set(false)
      firebase.auth().signOut().then(() => {
        this.close()
        M.toast({html: "Je bent uitgelogd", displayLength:6000,classes:"groenbackground"})
        this.$router.replace('/Home')
      })      
    }
  }
}
</script>