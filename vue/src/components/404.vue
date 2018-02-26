<template>
  <div class="notfound">
    <h2 class="pagetitle center">{{ msg }}</h2>
    <div>
        <img class="center" src="../assets/images/notfound.png">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notfound',
  data () {
    return {
      msg: 'Pagina niet gevonden'
    }
  }
}
</script>