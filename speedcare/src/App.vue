<template>
  <div id="app">
   <div id="load" v-show="!loaded">
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
    <div v-show="loaded">
      <nav class="blauwbackground">
        <div class="nav-wrapper">
          <router-link to="/" class="brand-logo center"><img class="navlogo" src="./assets/images/logo1.png" alt="SpeedCare"></router-link>
          <a href="#" data-target="mobile-demo" class="sidenav-trigger right"><i class="material-icons">menu</i></a>
          <ul id="nav-mobile" class="right hide-on-med-and-down">
            <li><router-link to="Login">Login</router-link></li>
            <li><router-link to="Activeer">Activeren</router-link></li>
            <li><router-link to="Ritten">Ritten</router-link></li>
            <li><router-link to="Rapporten">Rapporten</router-link></li>
            <li><router-link to="Account">Account</router-link></li>
          </ul>
          <ul id="mobile-demo" class="sidenav">
            <li><div class="user-view">
              <div class="background">
                <img src="./assets/images/materialize.jpg">
              </div>
              <a href="#!user"><img class="circle" src="./assets/images/user.png"></a>
              <a href="#!name"><span class="name">John Doe</span></a>
              <a href="#!email"><span class="email">jdandturk@gmail.com</span></a>
            </div></li>
            <li v-on:click="close"><router-link to="Login"><i class="material-icons">input</i>Login</router-link></li>
            <li v-on:click="close"><router-link to="Activeer"><i class="material-icons">loupe</i>Activeren</router-link></li>
            <li v-on:click="close"><router-link to="Ritten"><i class="material-icons">view_list</i>Ritten</router-link></li>
            <li v-on:click="close"><router-link to="Rapporten"><i class="material-icons">show_chart</i>Rapporten</router-link></li>
            <li><div class="divider"></div></li>
            <li><a class="subheader">Account</a></li>
            <li v-on:click="close"><router-link to="Account"><i class="material-icons">person_pin</i>Mijn account</router-link></li>
            <li v-on:click="close"><router-link to="/"><i class="material-icons">power_settings_new</i>Logout</router-link></li>
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
                  <li><a class="grey-text text-lighten-3" href="#!">Disclaimer</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Contact</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Over</a></li>
                </ul>
              </div>
              <div class="col l3 s12">
                <h5 class="groen">Social Media</h5>
                <ul>
                  <li><a class="grey-text text-lighten-3" href="#!">Facebook</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Twitter</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div class="footer-copyright">
            <div class="container">
            © 2018 Copyright - <router-link class="grey-text text-lighten-3" to="Disclaimer"><strong class="rood">www.speedcare.herokuapp.com </strong></router-link>
            <a class="rood right" target="_blank" href="http://lodemuylaert.be">Auteur</a>
            </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
var elem;
var instance;
export default {
  name: 'app',
  data () {
    return {
      loaded: false
    }
  },
  mounted: function(){
    this.$nextTick(function(){
      this.loaded = true
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
    }
  }
}
</script>