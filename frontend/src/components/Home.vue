// Home.vue

<template>
  <div>
    <!-- Main Card -->
    <b-card-group deck>
      <b-card
        border-variant="primary"
        header=" "
        header-bg-variant="primary"
        header-text-variant="white"
        align="left"
      >
        <b-card-text>Use the parameters below to see how people in that area were feeling about the weather this week. {{dateRange}}</b-card-text>
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

          <!-- Submit Button -->
          <b-button @click="useDate" variant="primary" style="margin-left: 10px" v-b-toggle.weather-collapse>Let's Go</b-button>
          <!-- <b-button @click="useDate" variant="primary" style="margin-left: 10px">Let's Go</b-button> -->
        </b-form>

        <b-button variant="outline-primary" v-b-toggle.coordinates-collapse style="margin: 20px">Enter Coordinates Manually</b-button>
        <b-collapse id="coordinates-collapse" class="mt-2">
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
        </b-collapse>

        <!-- Weather Data goes in this card -->
        <b-collapse id="weather-collapse" class="mt-2">
          <b-card
            tag="article"
            class="weather-card"
          >
            <b-title style="font-size:15pt">Weather in {{cityName}} according to {{station_name}}, {{station_dist}} miles away: </b-title>
            <!-- Headers for the plots -->
            <b-row style="margin-top: 10px">
              <b-col>
                <h3 style="text-align:center">{{avg_temp}}°F Average in {{cityName}}</h3>
              </b-col>
              <b-col>
                <h3 style="text-align:center">{{total_precip}} inches Total Precipitation</h3>
              </b-col>
              <b-col>
                <h3 style="text-align:center">{{max_wind}} mph Max Winds</h3>
              </b-col>
            </b-row>

            <!-- Weather Plots - start as blank colors, src will be given.
            NOTE: The blank prop takes precedence over the src prop. If you set both and later,
            set blank to false the image specified in src will then be displayed. -->
            <b-row>
              <b-col>
                <b-img v-bind="imageProps" blank-color="#338833" fluid alt="Weather Plot 1"></b-img>
              </b-col>
              <b-col>
                <b-img v-bind="imageProps" blank-color="rgba(128, 255, 255, 0.5)" fluid alt="Weather Plot 2"></b-img>
              </b-col>
              <b-col>
                <b-img v-bind="imageProps" blank-color="#88f" alt="Weather Plot 3" fluid ></b-img>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <h5 style="text-align:left; margin-left:">{{avg_max_temp}}°F average max, {{avg_min_temp}}°F average min</h5>
              </b-col>
              <b-col>
                <h5 style="text-align:left">{{total_rain}} inches of rain, {{total_snow}} inches of snow</h5>
              </b-col>
              <b-col>
                <h5 style="text-align:left">{{num_thunderous_days}} days of detected thunder</h5>
              </b-col>
            </b-row>

          </b-card>
        </b-collapse>
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
      // Weather Variables from NOAA
      station_name: 'DTW', // null,
      station_dist: 2, // null,
      num_thunderous_days: 0, // null,
      max_wind: 0, // null,
      avg_temp: 55, // null,
      avg_max_temp: 65, // null,
      avg_min_temp: 45, // null,
      total_rain: 2, // null,
      total_snow: 0, // null,
      // Other Variables
      total_precip: null,
      dateRange: null,
      cityName: null,
      tempData: null,
      cityData: null,
      latitude: null,
      longitude: null,
      radius: null,
      circleSelectorLink: 'https://www.mapdevelopers.com/draw-circle-tool.php',
      // Value format: City name, Lat, Long, Radius (miles), link to circle (see processCity())
      cityOptions: [
        { text: 'Choose...', value: null },
        { text: 'Detroit', value: 'Detroit,42.372169,-83.116741,9.4,https://rb.gy/nuulim' },
        { text: 'Chicago', value: 'Chicago,41.876584,-87.639529,10.0,https://rb.gy/qwsmxo' },
        { text: 'Miami', value: 'Miami,25.783447,-80.214909,5.0,https://rb.gy/j3u5bo' },
        { text: 'Seattle', value: 'Seattle,47.606609,-122.332815,8.0,https://rb.gy/ypkbxo' }
      ],
      imageProps: { blank: true, height: 75, width: 400, class: 'm1' }
    }
  },
  methods: {
    useDate () {
      // Other inits
      this.total_precip = this.total_rain + this.total_snow

      // Get the date range from a week ago until yesterday - format: [[start_date], [end_date]] i.e: ["YYYY-MM-DD", "YYYY-MM-DD"]
      var todaysDate = new Date()
      todaysDate.setDate(todaysDate.getDate() - 1)
      todaysDate = todaysDate.toISOString().split('T')[0]
      var oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
      oneWeekAgo = oneWeekAgo.toISOString().split('T')[0]
      const datesRange = [oneWeekAgo.toString(), todaysDate.toString()]
      this.dateRange = datesRange

      // Push the date range to the backend
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
    }
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
