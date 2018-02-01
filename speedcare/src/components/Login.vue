<template>
  <div class="login">
  <h2 class="pagetitle center">{{msg}}</h2>
    <div class="container">    
        <div class="row">
            <div class="col s12">
                <div class="row">
                    <div class="input-field col s12">
                    <input id="email" type="email" class="validate" v-model="email">
                    <label for="email">Email</label>
                    </div>
                </div>
                <div class="row">
                    <div class="input-field col s12">
                    <input id="password" type="password" class="validate" v-model="wachtwoord">
                    <label for="password">Wachtwoord</label>
                    </div>
                </div>
                <button class="btn fullwidth waves-effect waves-light" type="submit" name="action" v-on:click="login">Login</button>                 
                <div class="fullwidth center"><router-link to="Activeer" class="">Activeer</router-link></div>
                <div v-if="errors.length !== 0" class="row">                
                  <div class="input-field col s12 card-panel teal roodbackground wit">
                    <p v-for="error in errors">{{ error }}</p>
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
export default {
  name: 'Login',
  data () {
    return {
      msg: 'Login',
      email: null,
      wachtwoord: null,
      errors: []
    }
  },
  methods: {
    login: function(){
        this.errors = []
        firebase.auth().signInWithEmailAndPassword(this.email, this.wachtwoord).then(
            () => {
              this.$router.replace('/')
            },
            (err) => {             
                console.log('niet gelukt message: ' + err.message)
                this.errors.push(err.message)
            }
        )
    }
  }
}
</script>