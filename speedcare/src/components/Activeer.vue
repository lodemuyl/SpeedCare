<template>
  <div class="activeer">
  <h2 class="pagetitle center">{{msg}}</h2>
    <div class="container">    
        <div class="row">
            <div class="col s12">
                <div class="row">
                    <div class="input-field col s12">
                    <input id="pnummer" type="text" class="validate" v-model="productnummer">
                    <label for="pnummer">Productnummer</label>
                    </div>
                </div>
                <div class="row">
                    <div class="input-field col s12">
                    <input id="email" type="email" class="validate" v-model="email">
                    <label for="email">Email</label>
                    </div>
                </div>
                <div class="row">
                    <div class="input-field col s12">
                    <input id="password" type="password" class="validate" v-model="wachtwoord">
                    <label for="password">Standaard Wachtwoord</label>
                    </div>
                </div>
                <button class="btn fullwidth waves-effect waves-light" type="submit" name="action" v-on:click="activeer">Activeer</button>                 
                <div class="fullwidth center"><router-link to="Login" class="">Login</router-link></div>
                <div class="row">
                    <ul class="collapsible">
                        <li>
                            <div class="collapsible-header">
                                <span class="link">Wat is het productnummer?</span>
                            </div>
                            <div class="collapsible-body autooverflow">
                                <div class="col s12 m4 l4  center-align">
                                    <img class="pn" src="../assets/images/pn.jpg" alt="Productnummer">
                                </div>
                                <div class="col s12 m8 l8 pntext vlign-wrapper">                                  
                                    <h5>Productnummer</h5>
                                    <p>Het productnummer is een uniek nummer die op elke gpsmodule wordt geplaatst bij het distributeren van het product.</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div> 
                <div v-if="errors.length !== 0" class="row">                
                    <div class="input-field col s12 card-panel teal roodbackground wit">
                        <p v-for="errors in errors">{{ errors }}</p>
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
  name: 'Activeer',
  data () {
    return {
      msg: "Activeer",
      email: null,
      wachtwoord: null,
      productnummer: null,
      errors: []
    }
  },
  mounted(){
    var elem = document.querySelector('.collapsible');
    var instance = M.Collapsible.getInstance(elem);
    var instance = M.Collapsible.init(elem);
  },
  methods: {
    activeer: function(){
        this.errors = []
        firebase.auth().createUserWithEmailAndPassword(this.email, this.wachtwoord).then(
            (user) => {
                console.log('aangemaakt')
                this.$router.replace('Account')  
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