<template>
  <div class="detaillist">
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
        <div class="container">
            <ul class="collection with-header">
                <li class="collection-item" v-for="(item, propname) in list">
                    <div>
                        {{ propname }}<router-link :to="{ name: 'Detail', params: { datum:datum, tijd:propname }}" class="secondary-content"><i class="material-icons">send</i></router-link>
                    </div>
                </li>
            </ul>
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
  name: 'Detaillist',
  data () {
    return {
      msg: 'Rittenlijst van ' + this.$route.params.datum,
      loaded: false,
      list: {},
      datum: this.$route.params.datum
    }
  },
  created(){
      if (this.checkparam(this.datum)){
        this.getdata(this.datum)
      }else{
        this.$router.push('/Ritten')
      }    
  },
  methods: {
      checkparam: function(datum){
        let matches = /^(\d{4})[-](\d{1,2})[-](\d{1,2})$/.exec(datum);
        if (matches == null) return false;
        let m = matches[2];
        let y = matches[1] - 1;
        let d = matches[3];
        let composedDate = new Date(y, m, d);
        return composedDate.getDate() == d &&
               composedDate.getMonth() == m &&
               composedDate.getFullYear() == y;
      },
      getdata: function(datum){
        if(datum){
        let vandaag = new Date();
        let all = db.ref(this.$parent.currentUser.uid)  
        let day = new Date(this.datum).getDate();
        let self = this
        all.child(vandaag.getFullYear()).child(vandaag.getMonth()+1).child(day).once('value', (snapshot) => {
            let data = snapshot.val()
            self.list = data
            if(!data){
                this.$router.push('/Ritten')
            }
            this.loaded = true
        })
        }
      }
  }
}
</script>