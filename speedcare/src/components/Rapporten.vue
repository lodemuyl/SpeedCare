<template>
  <div class="rapporten">
    <h2 class="pagetitle center">{{ msg }}</h2>
      <div class="container">
      <div class="row">
        <div class="col s12 md12 l12">
          <ul id="" class="tabs tabs tabs-fixed-width">
            <li class="tab col s3"><a id="firstclick" class="active" href="#jaar">Jaar</a></li>
            <li class="tab col s3"><a href="#snelheid">Snelheidsovertredingen</a></li>
          </ul>
        </div>
        <div id="jaar" class="col s12 md12 l12 sw">
              <div class="card blue-grey darken-1">
                <div class="card-content white-text">
                  <span class="card-title">Jaar</span>
                  <p>I am a very simple card. I am good at containing small bits of information.
                  I am convenient because I require little markup to use effectively.</p>
                </div>
              </div>
        </div>
        <div id="snelheid" class="col s12 md12 l12 sw">
              <div class="card blue-grey darken-1">
                <div class="card-content white-text">
                  <span class="card-title">Snelheidsovertredingen</span>
                  <p>I am a very simple card. I am good at containing small bits of information.
                  I am convenient because I require little markup to use effectively.</p>
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

export default {
  name: 'Rapporten',
  data () {
    return {
      msg: 'Rapporten'
    }
  },
  created(){

  },
  mounted(){
    var elem
    var elem1
    var instance
    this.$nextTick(function(){
      let options = {
      }
      elem = document.querySelector('.tabs'); 
      elem1 = document.querySelector('#firstclick'); 
      instance = M.Tabs.init(elem,options);    
      instance.updateTabIndicator();
      console.log(elem1)
      elem1.click();      
    })
  }
}
</script>