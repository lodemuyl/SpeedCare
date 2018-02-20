<template>
  <div class="notfound">
    <h2 class="pagetitle center">{{ msg }}</h2>
  </div>
</template>

<script>
export default {
  name: 'Notfound',
  data () {
    return {
      msg: 'Not found'
    }
  }
}
</script>