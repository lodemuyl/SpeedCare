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
                <label class="labelacc rood strong" for="Email">
                Email
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
                <label class="labelacc rood strong" for="Wachtwoord">Wachtwoord</label>
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
                    <input v-model="modalvalue" v-bind:placeholder="modalplaceholder" id="Emailmodal" type="text" class="validate">                    
                  </div>
                </div>
                <div class="modal-footer">
                  <a v-on:click="modalchange(modalname)" class="modal-action modal-close waves-effect waves-green btn-flat ">Opslaan</a>
                  <a v-on:click="modalchange()" class="modal-action modal-close waves-effect waves-green btn-flat ">Annuleren</a>
                </div>
              </div>
                <div class="row">
              <div v-show="errormessage" class="col s12 m12 l12">
                <div class="card-panel roodbackground ">
                  <span class="grijs">{{errormessage}}</span>
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
      loaded: false,
      email: null,
      profilepicurl: '/static/img/user.93a57c9.png',
      newprofilepic :null,
      modalvalue: null,
      productnummer: null,
      laatstingelogd: null,
      userid: this.$parent.currentUser.uid,
      modalplaceholder: null,
      modalname: null,
      errormessage: null,
    }
  },
  created(){
    M.Toast.dismissAll();
    if(this.$parent.currentUser){
      this.getinfo();
    }
  },
  mounted: function(){
    let options = {
      opacity: 0.7,
      preventScrolling: false,
      startingTop: '15%',
      endingTop: '40%' 
    };
    elem = document.querySelector('#modalchange');
    instance = M.Modal.init(elem, options);
  },
  methods: {
    modal: function(param){      
    instance.open();
    this.errormessage = null
      if (param === "email"){
        this.modalplaceholder = this.email
        this.modalname = "Email"        
      }else if(param === "naam"){
        this.modalplaceholder = this.naam
        this.modalname = "Naam"
      }
    },
    modalchange: function(param){
      if(!this.modalvalue){
        this.errormessage = "Je moet een waarde invoeren"
        this.modalvalue = null;
        this.modalplaceholder = null;
        this.modalname = null;
      }else if(this.modalvalue){
        if(param === "Naam"){
          this.loaded = false;
          this.changedisplayname(this.modalvalue)
        }else if(param === "Email"){
          this.loaded = false;
          this.changeemail(this.modalvalue)
        }else{
          this.modalvalue = null;
          this.modalplaceholder = null;
          this.modalname = null;
        }
      }      
    },
    changedisplayname: function(param){
      firebase.auth().currentUser.updateProfile({
        displayName: param
      }).then(() => {
        this.naam = firebase.auth().currentUser.displayName;
        this.modalvalue = null;
        this.modalplaceholder = null;
        this.loaded = true;
      }, (error) => {
        console.log(error)
        this.errormessage = error.message;
        this.loaded = true
      });
    },
    changeemail: function(param){          
        firebase.auth().currentUser.updateEmail(param).then(() => {
          this.email = firebase.auth().currentUser.email;
          this.modalvalue = null;
          this.modalplaceholder = null;
          this.loaded = true;
        }, (error) => {
          console.log(error)
          this.errormessage = error.message
          this.loaded = true
        });
    },
    getinfo: function(){      
      let user = this.$parent.currentUser.providerData[0];
      let lastsignin = this.$parent.currentUser.metadata.lastSignInTime;
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
      this.laatstingelogd = this.gmtconvert(lastsignin);
      M.toast({html: this.laatstingelogd, displayLength:6000,classes:"groenbackground"})
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
            console.log('opgeslaan')
          }, function(error) {
              this.errors.push(error)
          });
        })
      }
    },
    gmtconvert: function(currtime){
      let newtime1 = moment(String(currtime)).format('MM/DD/YYYY');
      let newtime2 = moment(String(currtime)).format('HH:mm')
      return "Laatst ingelogd op " + newtime1 + " om " + newtime2;
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