<template>
  <div class="disclaimer">
    <h2 class="pagetitle center">{{ msg }}</h2>
    <div class="container">
    <p>Last updated: January 22, 2018</p>
    <p>The information contained on www.speedcare.herokuapp.com website (the
    "Service") is for general information and educational purposes only.</p>
    <p>SpeedCare assumes no responsibility for errors or omissions in the contents on
    the Service.</p>
    <p>In no event shall SpeedCare be liable for any special, direct, indirect,
    consequential, or incidental damages or any damages whatsoever, whether in an
    action of contract, negligence or other tort, arising out of or in connection
    with the use of the Service or the contents of the Service. SpeedCare reserves
    the right to make additions, deletions, or modification to the contents on the
    Service at any time without prior notice.</p>
    <p>SpeedCare does not warrant that the website is free of viruses or other
    harmful components.</p>
    <p>Disclaimer for SpeedCare based on the [disclaimer example from
    TermsFeed](https://termsfeed.com/blog/sample-disclaimer-template/).</p>
  
    <p>www.speedcare.herokuapp.com website may contain links to external websites
    that are not provided or maintained by or in any way affiliated with SpeedCare</p>
    <p>Please note that the SpeedCare does not guarantee the accuracy, relevance,
    timeliness, or completeness of any information on these external websites.</p>    
    </div>
  </div>
</template>

<script>
export default {
  name: 'Disclaimer',
  data () {
    return {
      msg: 'Disclaimer'
    }
  }
}
</script>