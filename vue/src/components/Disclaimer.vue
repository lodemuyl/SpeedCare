<template>
  <div class="disclaimer">
    <h2 class="pagetitle center">{{ msg }}</h2>
    <p>
Last updated: January 22, 2018

The information contained on www.speedcare.herokuapp.com website (the
"Service") is for general information purposes only.

SpeedCare assumes no responsibility for errors or omissions in the contents on
the Service.

In no event shall SpeedCare be liable for any special, direct, indirect,
consequential, or incidental damages or any damages whatsoever, whether in an
action of contract, negligence or other tort, arising out of or in connection
with the use of the Service or the contents of the Service. SpeedCare reserves
the right to make additions, deletions, or modification to the contents on the
Service at any time without prior notice.

SpeedCare does not warrant that the website is free of viruses or other
harmful components.

Disclaimer for SpeedCare based on the [disclaimer example from
TermsFeed](https://termsfeed.com/blog/sample-disclaimer-template/).

External links disclaimer  
-------------------------

www.speedcare.herokuapp.com website may contain links to external websites
that are not provided or maintained by or in any way affiliated with SpeedCare

Please note that the SpeedCare does not guarantee the accuracy, relevance,
timeliness, or completeness of any information on these external websites.


    </p>
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