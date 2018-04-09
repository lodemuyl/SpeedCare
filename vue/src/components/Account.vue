<template>
  <div class="account">
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
    <h2 class="pagetitle center">{{ naam }}</h2>
    <div class="row">
      <div class="container">
        <div class="col s12">
          <div class="row">
              <div class="col s12 m12 l12 center">
                <div class="relative">
                  <img class="circle profileim" :src="profilepicurl">
                  <div class="absolute editbutton">
                    <a v-on:click="editprofilepicture" class="btn-floating btn-large waves-effect waves-light relative">
                      <i class="fa fa-pencil"></i>
                    </a>
                  </div>                
                </div>              
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12 m6 l6">
                <i class="fa fa-ticket prefix rood"></i>
                <input disabled v-bind:value="productnummer" id="Productnummer" type="text" class="validate">
                <label class="labelacc rood strong" for="Productnummer">Productnummer</label>
              </div>
              <div class="input-field col s12 m6 l6">
              <i class="fa fa-user prefix rood"></i>
                <input disabled v-bind:value="naam" id="Naam" type="text" class="validate">
                <label class="labelacc rood strong" for="Naam">
                Naam
                  <div class="editbuttoninline">
                    <a v-on:click="modal('naam')" class="">
                      <i class="fa fa-pencil"></i>
                    </a>
                  </div>
                </label>                
              </div>
              <div class="input-field col s12 m6 l6">
                <i class="fa fa-envelope prefix rood"></i>              
                <input disabled v-bind:value="email" id="Email" type="text" class="validate">
                <label class="labelacc rood strong" for="Email">Email
                <div class="editbuttoninline">
                    <a v-on:click="modal('email')" class="">
                      <i class="fa fa-pencil"></i>
                    </a>
                  </div>
                </label>
              </div>
              <div class="input-field col s12 m6 l6">
                <i class="fa fa-unlock-alt prefix rood"></i>
                <input disabled value="nicetry" id="Wachtwoord" type="password" class="validate">
                <label class="labelacc rood strong" for="Wachtwoord">Wachtwoord
                 <div class="editbuttoninline">
                    <a v-on:click="modal('ww')" class="">
                      <i class="fa fa-pencil"></i>
                    </a>
                  </div>
                </label>
              </div>
              <div class="input-field col s12 m12 l12">
                <a v-on:click="logout" class="waves-effect waves-light btn fullwidth groenbackground">Logout</a>
              </div>
            </div>
              <!-- Modal Structure -->
              <div id="modalchange" class="modal">
                <div class="modal-content">
                  <h4 class="rood strong">{{ modalname }} wijzigen</h4>
                  <div class="input-field col s12 m12 l12">
                    <i class="fa fa-edit prefix rood"></i>              
                    <input v-model="modalvalue" v-bind:type="typetext" v-bind:placeholder="modalplaceholder" id="Emailmodal" type="text" class="validate">                    
                  </div>
                 <div v-show="showww" class="input-field col s12 m12 l12">
                    <i class="fa fa-edit prefix rood"></i>              
                    <input v-model="ww.new" type="password" placeholder="Nieuw wachtwoord" id="nieuwwachtwoord" class="validate">                    
                </div>                
                <div v-show="showww" class="input-field col s12 m12 l12">
                    <i class="fa fa-edit prefix rood"></i>              
                    <input v-model="ww.confirm" type="password" placeholder="Herhaal nieuw wachtwoord" id="wwherhaal" class="validate">                    
                </div>
              </div>
                <div class="modal-footer">
                  <a v-on:click="modalchange(modalname)" class="modal-action modal-close waves-effect waves-green btn-flat ">Opslaan</a>
                  <a v-on:click="modalchange('annuleer')" class="modal-action modal-close waves-effect waves-green btn-flat ">Annuleren</a>
                </div>
              </div>
                <div class="row">
              <div v-show="errormessage" class="col s12 m12 l12">
                <div class="card-panel roodbackground ">
                  <span class="wit">{{errormessage}}</span>
                </div>
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
import moment from 'moment'
import firebase from 'firebase'
import { db } from '../assets/js/firebase'
var elem 
var instance
export default {
  name: 'Account',
  data () {
    return {
      naam: null,
      typetext: "text",
      loaded: false,
      email: null,
      profilepicurl: '/static/img/user.93a57c9.png',
      newprofilepic :null,
      modalvalue: null,
      productnummer: null,
      userid: this.$parent.currentUser.uid,
      modalplaceholder: null,
      modalname: null,
      showww: false,
      ww: {
        "new": null,
        "confirm": null
      },
      errormessage: null,
    }
  },
  created(){
    if(this.$parent.currentUser){
      this.getinfo();
    }
  },
  mounted: function(){
    let options = {
      opacity: 0.7,
      preventScrolling: false,
      startingTop: '15%',
      endingTop: '40%',
      dismissible: false

    };
    elem = document.querySelector('#modalchange');
    instance = M.Modal.init(elem, options);
  },
  methods: {
    modal: function(param){      
      instance.open();
      this.errormessage = null;
      this.confirmmessage = null;
      if (param === "email"){
        this.modalplaceholder = this.email
        this.modalname = "Email"        
      }else if(param === "naam"){
        this.modalplaceholder = this.naam
        this.modalname = "Naam"
      }else if(param === "ww"){
         this.typetext = "password";
        this.showww = true
        this.modalplaceholder = "oud wachtwoord"
        this.modalname = "Wachtwoord"
      }
    },
    modalchange: function(param){
      if(param){
        if(param === "Naam"){
          this.loaded = false;
          this.changedisplayname(this.modalvalue)
        }else if(param === "Email"){
          this.loaded = false;
          this.changeemail(this.modalvalue)
        }else if(param === "Wachtwoord"){         
          this.loaded = false
          this.changeww(this.modalvalue)
        }else if(param === "annuleer"){
          this.showww = false;
          this.modalvalue = null;
          this.modalplaceholder = null;
          this.modalname = null;
          this.ww.new = null;
          this.ww.confirm = null;
          this.typetext = "text";
        }
      }      
    },
    changedisplayname: function(param){
      if(param){      
        firebase.auth().currentUser.updateProfile({
          displayName: param
        }).then(() => {
          this.naam = firebase.auth().currentUser.displayName;
          this.modalvalue = null;
          this.modalplaceholder = null;
          this.loaded = true;
          M.toast({html: "Jouw naam is gewijzigd.", displayLength:6000,classes:"groenbackground"})
        }, (error) => {
          console.log(error)
          this.errormessage = error.message;
          this.loaded = true
        });
      }else{
        this.errormessage = "Je hebt geen naam ingevoerd"
        this.loaded = true
      }
    },
    changeemail: function(param){     
      if(param){
        firebase.auth().currentUser.updateEmail(param).then(() => {
          this.email = firebase.auth().currentUser.email;
          this.modalvalue = null;
          this.modalplaceholder = null;
          this.loaded = true;
          M.toast({html: "Jouw emailadres is gewijzigd.", displayLength:6000,classes:"groenbackground"})
        }, (error) => {
          console.log(error)
          this.errormessage = error.message
          this.loaded = true
        });
      }else{             
        this.errormessage = "Je hebt geen email ingevoerd"
        this.loaded = true      
      }
    },
    changeww: function(param){
      if(param){
        if(this.ww.new && this.ww.new == this.ww.confirm){
          let newpass = String(this.ww.new)
          let ver = firebase.auth().currentUser.reauthenticateWithCredential(firebase.auth.EmailAuthProvider.credential(firebase.auth().currentUser.email, param)).then(()=>{
            firebase.auth().currentUser.updatePassword(newpass).then((ok) => {
              M.toast({html: "Jouw wachtwoord is gewijzigd.", displayLength:6000,classes:"groenbackground"})
              this.loaded = true
            },(error) =>{
              this.errormessage = "Kon jouw wachtwoord niet wijzigen : " + error
              this.loaded = true
            });
          },
          (error)=>{
            this.errormessage = "Jouw oud wachtwoord is niet correct."
            this.loaded = true
          })         
        }else{
          this.errormessage = "Jouw nieuw wachtwoorden komen niet overeen of zijn leeg."
          this.loaded = true  
        }
        this.ww.new = null
        this.ww.confirm = null
        this.modalvalue = null
        this.typetext = "text";
      }else{
        this.errormessage = "Oud wachtwoord niet ingevoerd."
        this.loaded = true
      }
      this.showww = false
    },
    getinfo: function(){      
      let user = this.$parent.currentUser.providerData[0];
      let uid = this.$parent.currentUser.uid
      this.email = user.email;
      this.naam = user.displayName;
      let ref = uid + "/productnummer"   
      if(user.photoURL){
        this.profilepicurl = user.photoURL;
        this.$parent.profilepicurl = user.photoURL;
      };         
      db.ref(ref).once("value").then((e)=>{
        this.productnummer = e.val()
        this.loaded = true
      })
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
      this.newprofilepic = files[0]
      if(this.newprofilepic){
        let ref = this.userid + "/customurl"        
        firebase.storage().ref('userafbeeldingen/'+this.userid).put(this.newprofilepic)
        .then(function(filedata){
          let downloadurl = filedata.metadata.downloadURLs[0]
          return downloadurl
        })
        .then(function(data){
          firebase.auth().currentUser.updateProfile({
              photoURL: data,
          }).then(function() {            
            M.toast({html: "Jouw afbeelding is gewijzigd.", displayLength:6000,classes:"groenbackground"})
          }, function(error) {
              this.errors.push(error)
          });
        })
      }
    },
    logout: function(){
      let ref = this.userid + "/actief"
      db.ref(ref).set(false)
      firebase.auth().signOut().then(() => {
        this.$router.push('Home')
        M.toast({html: "Je bent uitgelogd", displayLength:6000,classes:"groenbackground"})
      })
      
    }
  }
}
</script>