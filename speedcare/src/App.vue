<template>
  <div id="app">
    <div id="load" v-if="!loaded">
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
    <div v-else>
      <nav class="blauwbackground">
        <div class="nav-wrapper">
          <router-link to="/" class="brand-logo center"><img class="navlogo" src="./assets/images/logo1.png" alt="SpeedCare"></router-link>
          <a href="#" data-target="mobile-demo" class="sidenav-trigger right"><i class="material-icons">menu</i></a>
          <ul id="nav-mobile" class="right hide-on-med-and-down">
            <li><a href="sass.html">Sass</a></li>
            <li><a href="badges.html">Components</a></li>
            <li><a href="collapsible.html">JavaScript</a></li>
          </ul>
          <ul id="mobile-demo" class="sidenav">
            <li><a href="sass.html">Sass</a></li>
            <li><a href="badges.html">Components</a></li>
            <li><a href="collapsible.html">JavaScript</a></li>
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
                <h5 class="grijs">SpeedCare</h5>
                <p class="beige">You can use rows and columns here to organize your footer content.</p>
              </div>
              <div class="col l4 offset-l2 s12">
                <h5 class="grijs">Social Media</h5>
                <ul>
                  <li><a class="grey-text text-lighten-3" href="#!">Facebook</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Twitter</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Instagram</a></li>
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
export default {
  name: 'app',
  data () {
    return {
      loaded: false
    }
  },
  mounted () {   
    this.loaded = true
  }
}
</script>