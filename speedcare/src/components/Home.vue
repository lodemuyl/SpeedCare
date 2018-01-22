<template>
  <div class="home">
    <div class="container">
      <img class="logo" src="../assets/images/logo.png" alt="SpeedCare">
    </div>
    <h1>{{ msg }}</h1>    
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js PWA'
    }
  }
}
</script>