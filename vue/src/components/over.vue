<template>
  <div class="over">
    <h2 class="pagetitle center">{{ msg }}</h2>
    <div class="container">
    <p>Speedcare is een Bachelorproject in opdracht van de ArteveldeHogeschool.
    <br> Het onderwerp van deze opdracht heb ik zelf gekozen en heeft te maken met het welbekende Internet Of Things.
    <br> Dit project bestaat uit een "carlog" systeem die de gewone mens in staat stelt om zijn locaties tijdens het rijden op te slaan, bijkomend kan de app van elke locatie de maximum toegelaten snelheid ophalen.
    <br> Aan de hand van jouw snelheid en de maximum toegelaten snelheid kan er een score bepaald worden, deze score vertegenwoordigd jouw rijgedrag. 
    <br>Deze score kan niet alleen handig zijn voor de gebruiker maar ook voor verzekeringsmaatschappijen die mensen willen gaan verzekeren op basis van hun rijgedrag.</p>  
    </div>
  </div>
</template>

<script>
export default {
  name: 'Over',
  data () {
    return {
      msg: 'Over'
    }
  }
}
</script>