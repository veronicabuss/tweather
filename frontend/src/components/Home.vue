// Home.vue

<template>
  <div>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom" style="margin-bottom: 20px">New random number</button>

    <!-- Main Card -->
    <b-card-group deck>
      <b-card
        border-variant="primary"
        header=" "
        header-bg-variant="primary"
        header-text-variant="white"
        align="left"
      >
        <b-card-text>Use the parameters below to see how people in that area are feeling about the weather.</b-card-text>
        <!-- Start of init inputs -->
        <b-form inline>
          <!-- City Selection -->
          <label class="mr-sm-2" for="id-city-selector">Choose a City:</label>
          <b-form-select
            id="id-city-selector"
            class="mb-2 mr-sm-2 mb-sm-0"
            :options="cityOptions"
            v-model="cityData"
            @change="processCity"
          ></b-form-select>

          <!-- Date Range Selector -->
          <label class="mr-sm-2" for="id-date-range-picker"> Select a date range:</label>
          <date-picker v-model="dateRange" range id="id-date-range-picker"></date-picker>

          <!-- Submit Button -->
          <b-button @click="useDate" variant="primary" style="margin-left: 10px">Let's Go</b-button>
          <!-- <b-button @click="useDate" variant="primary" style="margin-left: 10px">Let's Go</b-button> -->
        </b-form>

        <!-- Styling -->
        <p class="or-label">or</p>

        <!-- Link to website where finding a coordinate circle is really easy -->
        <p>Use <a v-bind:href="circleSelectorLink">this link</a> to adjust the preselected city parameters or select a different location.
          Input the city / address, then click <b>"New Circle"</b>. Copy over the Position and Radius in miles.</p>

        <!-- Coordinate Circle Inputs -->
        <b-form class="coordinate-circle-wrapper" inline>
          <label for="id-latitude">Latitude: </label>
          <b-form-input v-model="latitude" id="id-latitude" placeholder="Latitude"></b-form-input>
          <label for="id-longitude">Longitude: </label>
          <b-form-input v-model="longitude" id="id-longitude" placeholder="Longitude"></b-form-input>
          <label for="id-radius">Radius (in miles): </label>
          <b-form-input v-model="radius" id="id-radius" placeholder="Radius (in miles)"></b-form-input>
        </b-form>

        <!-- Weather Data goes in this card -->
        <b-card
          title="Official Weather Data Goes Here"
          tag="article"
          class="weather-card"
        >
          <!-- Average Temp and city name for the header -->
          <h1>&nbsp;&nbsp;75° in {{cityName}}</h1>

          <!-- Weather Filtering Inputs -->
          <b-form class="weather-filtering-wrapper" inline>
            <label for="id-temps-above">Temps Above: </label>
            <b-form-input v-model="tempsAbove" id="id-temps-above" placeholder="Temps Above"></b-form-input>
            <label for="id-temps-below">Temps Below: </label>
            <b-form-input v-model="tempsBelow" id="id-temps-below" placeholder="Temps Below"></b-form-input>
            <label for="id-precip-above">Precip Above: </label>
            <b-form-input v-model="precipAbove" id="id-precip-above" placeholder="Precip Above"></b-form-input>
            <p class="space">&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</p>
            <label for="id-precip-below">Precip Below: </label>
            <b-form-input v-model="precipBelow" id="id-precip-below" placeholder="Precip Below"></b-form-input>
            <label for="id-avg-wind-direction">Avg Wind Direction: </label>
            <b-form-input v-model="avgWindDirection" id="id-avg-wind-direction" placeholder="Avg Wind Direction"></b-form-input>
            <label for="id-avg-wind-speed">Avg Wind Speed (mph): </label>
            <b-form-input v-model="avgWindSpeed" id="id-avg-wind-speed" placeholder="Avg Wind Speed (mph)"></b-form-input>
          </b-form>
        </b-card>

      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'
import axios from 'axios'
export default {
  components: { DatePicker },
  data () {
    return {
      cityName: null,
      dateRange: null,
      randomNumber: 0,
      tempData: null,
      cityData: null,
      latitude: null,
      longitude: null,
      radius: null,
      circleSelectorLink: 'https://www.mapdevelopers.com/draw-circle-tool.php',
      // Value format: City name, Lat, Long, Radius (miles), link to circle (see processCity())
      cityOptions: [
        { text: 'Choose...', value: null },
        { text: 'Chicago', value: 'Chicago,41.876584,-87.639529,10.0,https://rb.gy/qwsmxo' },
        { text: 'Miami', value: 'Miami,25.783447,-80.214909,5.0,https://rb.gy/j3u5bo' },
        { text: 'Seattle', value: 'Seattle,47.606609,-122.332815,8.0,https://rb.gy/ypkbxo' }
      ]

    }
  },
  methods: {
    useDate () {
      const path = 'http://localhost:5000/api/request'
      const json = JSON.stringify({date: this.dateRange, city: this.cityName})
      axios.post(path, json, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
    },
    // On select of a city, updates the manual select buttons with prepopulated data
    processCity () {
      var parsedCityData = this.cityData.split(',')
      if (parsedCityData.length === 5) {
        this.cityName = parsedCityData[0]
        this.latitude = parsedCityData[1]
        this.longitude = parsedCityData[2]
        this.radius = parsedCityData[3]
        this.circleSelectorLink = parsedCityData[4]
      }
    },
    getRandom () {
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/random`
      axios.get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getRandom()
  }
}
</script>

<style>
label{
  margin-right: 5px;
  margin-left: 10px;
}
#id-latitude, #id-longitude, #id-radius{
  margin-right: 10px;
}
.coordinate-circle-wrapper{
  margin-bottom: 10px;
}
.or-label{
  margin: 10px 45px;
}
.space{
  margin-bottom: 25px;
}
.weather-card{
  margin-top: 20px;
}
</style>
