<template>
  <div class="activeer">
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
        <input type="file" class="fileinport" ref="fileinput" accept="image/*" @change="imagechange">
        <h2 class="pagetitle center">{{msg}}</h2>
        <div class="container">    
                <div class="row">
                    <div class="col s12">
                        <div class="row">
                            <div class="col s12 m12 l12 center">
                            <div class="relative">
                                <img class="circle profileim" :src="profilepicurl">
                                <div class="absolute editbutton">
                                <a v-on:click="editprofilepicture" class="btn-floating btn-large waves-effect waves-light relative">
                                    <i class="fa fa-plus"></i>
                                </a>
                                </div>                
                            </div>              
                            </div>
                        </div>
                        <div class="row">
                            <div class="input-field col s12 m12 l6">
                                <input @keyup.enter="activeer" id="pnummer" type="text" class="validate" v-model="productnummer" tabindex=1>
                                <label for="pnummer">Productnummer</label>
                            </div>
                            <div class="input-field col s12 m12 l6">
                                <input @keyup.enter="activeer" id="Gebruikersnaam" type="text" class="validate" v-model="naam" tabindex=2>
                                <label for="Gebruikersnaam">Gebruikersnaam</label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="input-field col s12 m12 l12">
                                <input @keyup.enter="activeer" id="email" type="email" class="validate" v-model="email" tabindex=3>
                                <label for="email">Email</label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="input-field col s12 m12 l12">
                            <input @keyup.enter="activeer" id="password" type="password" class="validate" v-model="wachtwoord" tabindex=5>
                            <label for="password">Standaard Wachtwoord</label>
                            </div>
                        </div>
                        <button tabindex=7 class="btn fullwidth waves-effect waves-light" type="submit" name="action" v-on:click="activeer">Activeer</button>                 
                        <div class="fullwidth center"><router-link tabindex=8 to="Login" class="">Login</router-link></div>
                        <div class="row">
                            <ul class="collapsible">
                                <li>
                                    <div class="collapsible-header">
                                        <span tabindex=9 class="link">Wat is het productnummer?</span>
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
  </div>
</template>

<script>
/* eslint-disable */
import firebase from 'firebase'
import { db } from '../assets/js/firebase'
export default {
  name: 'Activeer',
  data () {
    return {
      msg: "Activeer",
      email: null,
      naam: null,
      loaded: true,
      wachtwoord: null,
      productnummer: null,
      useruid: null,
      profilepicurl: "../../static/img/user.png",
      afbeelding: null,
      errors: []
    }
  },
  firebase: {
      db: db
  },
  mounted(){
    var elem = document.querySelector('.collapsible');
    var instance = M.Collapsible.getInstance(elem);
    var instance = M.Collapsible.init(elem);
  },
  methods: {
    activeer: function(){
        let element = document.querySelector('.page-footer');
        this.loaded = false;
        this.errors = []
        //validatie
        if(!this.productnummer){
           this.errors.push("Gelieve het productnummer in te voeren")
           element.scrollIntoView();
           this.loaded = true;
        }else if(!this.naam){
           this.errors.push("Gelieve jouw gebruikersnaam in te vullen")
           element.scrollIntoView();
           this.loaded = true;
        }else if(!this.email){
           this.errors.push("Gelieve jouw email in te vullen")
           element.scrollIntoView();
           this.loaded = true;
        }else if(!this.wachtwoord){
            this.errors.push("Gelieve jouw wachtwoord in te vullen")
            element.scrollIntoView();
            this.loaded = true;
        }else{
            if(this.email){
                var re = /\S+@\S+\.\S+/;
                if(!re.test(this.email)){
                    this.errors.push("Gelieve een geldig emailadres in te vullen")
                    this.loaded = true;
                    element.scrollIntoView();
                }else{
                    try{
                        firebase.auth().createUserWithEmailAndPassword(this.email, this.wachtwoord)
                        .then(
                            (user) => {
                                this.useruid = user.uid;
                                let temp = {
                                    actief: true,
                                    productnummer: this.productnummer.toUpperCase()
                                }
                                db.ref(user.uid).set(temp)
                                if(this.afbeelding){
                                    let ref = user.uid + "/customurl"        
                                    return firebase.storage().ref('userafbeeldingen/'+user.uid).put(this.afbeelding)
                                }
                                return null
                            }
                        ).then(
                            ()=>{
                                let pk = this.productnummer
                                let uid = this.useruid
                                let temp = {
                                     user: uid
                                }
                                let ref = "Relations/" + pk
                                db.ref(ref).set(temp)
                            }
                        ).then(
                            (filedata) => {
                                if(filedata){
                                    let downloadurl = filedata.metadata.downloadURLs[0];
                                    firebase.auth().currentUser.updateProfile({
                                        photoURL: downloadurl,                         
                                        displayName: this.naam
                                    })
                                }else{                    
                                    firebase.auth().currentUser.updateProfile({                         
                                        displayName: this.naam
                                    })
                                }                
                            }
                        ).then(
                            (data) => {
                                if(this.errors.length =! 0){
                                    M.toast({html: "Je profiel is aangemaakt", displayLength:6000,classes:"groenbackground"})
                                    this.$router.replace('Account') 
                                    location.reload();                   
                                }                
                            }
                        )
                    }catch(e){
                        this.errors.push(e.message)
                        element.scrollIntoView();
                        this.loaded = true;
                    }     
                }
            }
        }

    },
    editprofilepicture: function(){
      this.$refs.fileinput.click();
    },
    imagechange: function(event){
      const files = event.target.files
      let filename = files[0].name
      if(filename.lastIndexOf('.') <= 0){
        return alert('Selecteer een geldige afbeelding.')
      }
      const fileReader = new FileReader()
      fileReader.addEventListener('load', () => {
        this.profilepicurl = fileReader.result
      })
      fileReader.readAsDataURL(files[0])
      this.afbeelding = files[0]   
    }
  }
}
</script>