<template>
  <div class="login">
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
      <h2 class="pagetitle center">{{msg}}</h2>
      <div class="container">    
          <div class="row">
              <div class="col s12">
                  <div class="row">
                      <div class="input-field col s12">
                      <input @keyup.enter="login" id="email" type="email" class="validate" v-model="email" tabindex=1>
                      <label for="email">Email</label>
                      </div>
                  </div>
                  <div class="row">
                      <div class="input-field col s12">
                      <input @keyup.enter="login" id="password" type="password" class="validate" v-model="wachtwoord" tabindex=2>
                      <label for="password">Wachtwoord</label>
                      </div>
                  </div>
                  <button tabindex=3 class="btn fullwidth waves-effect waves-light" type="submit" name="action" v-on:click="login">Login</button>                 
                  <div class="fullwidth center"><router-link tabindex=4 to="Activeer" class="">Activeer</router-link></div>
                  <div v-if="errors.length !== 0" class="row">                
                    <div class="input-field col s12 card-panel teal roodbackground wit">
                      <p v-for="error in errors">{{ error }}</p>
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
import firebase from 'firebase'
import { db } from '../assets/js/firebase'
export default {
  name: 'Login',
  data () {
    return {
      msg: 'Login',
      loaded: true,
      email: null,
      wachtwoord: null,
      errors: []
    }
  },
  methods: {
    login: function(){
      this.loaded = false;
      this.errors = []
      firebase.auth().signInWithEmailAndPassword(this.email, this.wachtwoord).then(
            (e) => {
              let ref = e.uid + "/actief"
              db.ref(ref).set(true)              
            },
            (err) => {      
                this.loaded = true;       
                console.log('niet gelukt message: ' + err.message)
                this.errors.push(err.message)
            }
        ).then(()=>{
          this.loaded = true;
          this.$router.push('/Account') 
          location.reload()
        })
    }
  }
}
</script>