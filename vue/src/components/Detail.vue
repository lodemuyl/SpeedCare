<template>
  <div class="detail">
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
        <h2 class="pagetitle center">{{ msg }}</h2>
        <div class="pannel">
            <div class="leftside">
            </div>
            <div class="rightside">
                <div class="container">
                    <p class="subtitle">Info</p>
                    <div class="row">
                        <div class="col s12 m6 l6">
                            <div><i class="material-icons rood infoicons">date_range</i><p class="inlineinfo">Datum</p></div>
                            <div><i class="material-icons rood infoicons">access_time</i><p class="inlineinfo">7 uur tot 8 uur</p></div>
                            <div><i class="material-icons rood infoicons">account_circle</i><p class="inlineinfo">lode muylaert</p></div>
                        </div>
                        <div class="col s12 m6 l6">
                            <div><i class="material-icons rood infoicons">timer</i><p class="inlineinfo">duuur vd rit</p></div>
                            <div><i class="material-icons rood infoicons">directions_car</i><p class="inlineinfo">maxspeed</p></div>
                        </div>
                    </div>
                    <p class="subtitle">Overtredingen</p>
                    <div class="row">
                        <div v-show="violationslist">                        
                            <ul class="collapsible">
                                <li v-for="overtreding in violationslist">
                                    <div class="collapsible-header">
                                    <img class ="maxspeedsign" :src="overtreding.url">
                                    {{ overtreding.lat }}
                                    <span class="new badge red">{{ overtreding.werkelijkesnelheid }} km/u</span></div>                                    
                                </li>
                            </ul>
                        </div>
                        <div v-show="!violationslist">
                            <p>U hebt geenovertredingen begaan op deze rit</p>
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
import { alldata } from '../assets/js/firebase'
import { actief } from '../assets/js/firebase'
import { db } from '../assets/js/firebase' 
export default {
  name: 'Detail',
  data () {
    return {
      msg: 'Overzicht Detail',
      loaded: false,
      logs: {},
      violationslist: {},
      datum: this.$route.params.datum,
      tijd: this.$route.params.tijd
    }
  },
  created(){
    if (this.checkparam(this.datum, this.tijd)){
        //this.getdata(this.datum, this.tijd)
        this.violations(this.datum, this.tijd);
    }else{
        this.$router.push('/Ritten')
    }  
  },
  methods: {
      checkparam: function(datum, tijd){
        //datum
        let matchesd = /^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$/.exec(datum);
        let matchesh = /^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$/.exec(tijd);
        if (matchesd == null) return false;
        if (matchesh == null) return false;
        let m = matchesd[2];
        let y = matchesd[1] - 1;
        let d = matchesd[3];
        let h = matchesh[1];
        let min = matchesh[2];
        let s = matchesh[3];
        let composedDate = new Date(y, m, d, h, min, s);
        //tijd
        return composedDate.getDate() == d &&
               composedDate.getMonth() == m &&
               composedDate.getFullYear() == y &&
               composedDate.getHours() == h &&
               composedDate.getMinutes() == min &&
               composedDate.getSeconds() == s;


      },
      getdata: function(datum, tijd){
        if(datum && tijd){
            let all = db.ref(this.$parent.currentUser.uid)  
            let ritdate = new Date(datum)
            let jaar = ritdate.getFullYear();
            let maand = ritdate.getMonth()+1;
            let dag = ritdate.getDate();
            let self = this
            all.child(jaar).child(maand).child(dag).child(tijd).once('value', (snapshot) => {
                let data = snapshot.val()
                self.logs = data
                if(!data){
                    this.$router.push('/Ritten')
                }
                this.loaded = true
            })
        }
      },
      violations: function(datum, tijd){
          if(datum && tijd){
            let all = db.ref(this.$parent.currentUser.uid)  
            let ritdate = new Date(datum)
            let jaar = ritdate.getFullYear();
            let maand = ritdate.getMonth()+1;
            let dag = ritdate.getDate();
            let self = this
            let violation = {};
            all.child(jaar).child(maand).child(dag).child(tijd).once('value', (snapshot) => {
                snapshot.forEach(function(childSnapshot) { 
                    let key = childSnapshot.key;  
                    let childData = childSnapshot.val();
                    let childData2 = Object.values(childData)[0];
                    if(childData2['snelheid'] > childData2['maxsnelheid']){
                        violation[key] = {
                            'werkelijkesnelheid': childData2['snelheid'],
                            'maximumsnelheid': childData2['maxsnelheid'],
                            'url': '../static/img/maxspeed/' + childData2['maxsnelheid'] + '.png',
                            'lat': childData2['lat'],
                            'lon': childData2['lon'],
                            'tesnel': childData2['snelheid'] - Number(childData2['maxsnelheid'])
                        }                        
                    }
                });
                if(Object.keys(violation).length === 0){
                    self.violationslist = null;
                }else{
                    self.violationslist = violation;
                }
                this.loaded = true
            })
          }else{
            this.$router.push('/Ritten')                  
          }
      }
  }
}
</script>