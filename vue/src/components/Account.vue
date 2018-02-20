<template>
  <div class="account">
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
                <label class="labelacc rood strong" for="Naam">Naam</label>
              </div>
              <div class="input-field col s12 m6 l6">
                <i class="fa fa-envelope prefix rood"></i>              
                <input disabled v-bind:value="email" id="Email" type="text" class="validate">
                <label class="labelacc rood strong" for="Email">Email</label>
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
export default {
  name: 'Account',
  data () {
    return {
      naam: null,
      email: null,
      profilepicurl: '/static/img/user.93a57c9.png',
      newprofilepic :null,
      productnummer: null,
      laatstingelogd: null,
      userid: this.$parent.currentUser.uid
    }
  },
  created(){
    M.Toast.dismissAll();
    if(this.$parent.currentUser){
      this.getinfo();
    }
  },
  methods: {
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