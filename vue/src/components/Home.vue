<template>
  <div class="home">

      <agile :arrows="false" :speed="750" :autoplaySpeed="8000" :fade="true":autoplay="true" :pauseOnHover="false">
          <div class="slide slide--1"></div>
          <div class="slide slide--2"></div>
          <div class="slide slide--3"></div>
          <div class="slide slide--4"></div>
      </agile>
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