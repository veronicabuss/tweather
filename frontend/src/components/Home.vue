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
        style="margin-left: -10px; margin-right: -10px"
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
        <b-collapse id="weather-collapse" >
          <b-card
            tag="article"
            class="weather-card"
          >
            <b-title style="font-size:15pt">Weather in {{cityName}}, {{state_name}}: </b-title>
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
              <b-col style="margin: 0 -10px">
                <b-img v-bind:src="'data:image/png;base64,'+ plot2" fluid alt="Temperature/Precipitation Plot" style="margin: 0"></b-img>
              </b-col>
              <b-col style="margin: 0 -10px">
                <b-img v-bind:src="'data:image/png;base64,'+ plot1" fluid alt="Wind Speed/Direction Plot" style="margin: 0"></b-img>
                <!-- <img v-bind:src="'data:image/png;base64,'+ plot1" > -->
              </b-col>
              <b-col style="margin: 0 -10px">
                <b-img v-bind:src="'data:image/png;base64,'+ plot4" fluid alt="Visibility/Humidity Plot" style="margin: 0"></b-img>
                <!-- <img v-bind:src="'data:image/png;base64,'+ plot4" width="500"> -->
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <h5 style="text-align:left">{{avg_max_temp}}°F average max, {{avg_min_temp}}°F average min</h5>
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

      <!-- Select Keywords card -->
      <b-card>
        <!-- Date Header Row -->
        <b-row class="header-row">
          <b-col class="header" id="date-header-1">
            <h3>11/22</h3>
          </b-col>
          <b-col class="header" id="date-header-2">
            <h3>11/23</h3>
          </b-col>
          <b-col class="header" id="date-header-3">
            <h3>11/24</h3>
          </b-col>
          <b-col class="header" id="date-header-4">
            <h3>11/25</h3>
          </b-col>
          <b-col class="header" id="date-header-5">
            <h3>11/26</h3>
          </b-col>
          <b-col class="header" id="date-header-6">
            <h3>11/27</h3>
          </b-col>
          <b-col class="header" id="date-header-7">
            <h3>11/28</h3>
          </b-col>
        </b-row>
         <!-- Keywords Row -->
        <b-row class="keywords-row">
          <!-- Day 1 Keywords -->
          <b-col class="keywords-col" id="keywords-day-1">
            <p>Enter Keywords:</p>
            <!-- Cold Keywords Dropdown Button -->
            <b-button variant="outline-info" v-b-toggle.day1-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day1-cold-collapse">
              <b-form-checkbox-group v-model="day1_keywords.cold" id="day1-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <!-- Warm Keywords Dropdown Button -->
            <b-button variant="outline-warning" v-b-toggle.day1-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day1-warm-collapse">
              <b-form-checkbox-group v-model="day1_keywords.warm" id="day1-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <!-- Storm Keywords Dropdown Button -->
            <b-button variant="outline-secondary" v-b-toggle.day1-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day1-storm-collapse">
              <b-form-checkbox-group v-model="day1_keywords.storm" id="day1-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <!-- Precipitation Keywords Dropdown Button -->
            <b-button variant="outline-primary" v-b-toggle.day1-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day1-precip-collapse">
              <b-form-checkbox-group v-model="day1_keywords.precip" id="day1-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
            <b-button variant="info" @click="saveDay1Keywords()" style="margin-top: 10px; width: 80%">Save</b-button>
          </b-col>
          <!-- Day 2 Keywords -->
          <b-col class="keywords-col" id="keywords-day-2">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day2-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day2-cold-collapse">
              <b-form-checkbox-group v-model="day2_keywords.cold" id="day2-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day2-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day2-warm-collapse">
              <b-form-checkbox-group v-model="day2_keywords.warm" id="day2-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day2-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day2-storm-collapse">
              <b-form-checkbox-group v-model="day2_keywords.storm" id="day2-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day2-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day2-precip-collapse">
              <b-form-checkbox-group v-model="day2_keywords.precip" id="day2-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
          <!-- Day 3 Keywords -->
          <b-col class="keywords-col" id="keywords-day-3">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day3-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day3-cold-collapse">
              <b-form-checkbox-group v-model="day3_keywords.cold" id="day3-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day3-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day3-warm-collapse">
              <b-form-checkbox-group v-model="day3_keywords.warm" id="day3-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day3-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day3-storm-collapse">
              <b-form-checkbox-group v-model="day3_keywords.storm" id="day3-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day3-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day3-precip-collapse">
              <b-form-checkbox-group v-model="day3_keywords.precip" id="day3-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
          <!-- Day 4 Keywords -->
          <b-col class="keywords-col" id="keywords-day-4">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day4-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day4-cold-collapse">
              <b-form-checkbox-group v-model="day4_keywords.cold" id="day4-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day4-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day4-warm-collapse">
              <b-form-checkbox-group v-model="day4_keywords.warm" id="day4-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day4-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day4-storm-collapse">
              <b-form-checkbox-group v-model="day4_keywords.storm" id="day4-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day4-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day4-precip-collapse">
              <b-form-checkbox-group v-model="day4_keywords.precip" id="day4-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
          <!-- Day 5 Keywords -->
          <b-col class="keywords-col" id="keywords-day-5">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day5-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day5-cold-collapse">
              <b-form-checkbox-group v-model="day5_keywords.cold" id="day5-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day5-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day5-warm-collapse">
              <b-form-checkbox-group v-model="day5_keywords.warm" id="day5-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day5-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day5-storm-collapse">
              <b-form-checkbox-group v-model="day5_keywords.storm" id="day5-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day5-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day5-precip-collapse">
              <b-form-checkbox-group v-model="day5_keywords.precip" id="day5-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
          <!-- Day 6 Keywords -->
          <b-col class="keywords-col" id="keywords-day-6">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day6-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day6-cold-collapse">
              <b-form-checkbox-group v-model="day6_keywords.cold" id="day6-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day6-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day6-warm-collapse">
              <b-form-checkbox-group v-model="day6_keywords.warm" id="day6-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day6-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day6-storm-collapse">
              <b-form-checkbox-group v-model="day6_keywords.storm" id="day6-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day6-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day6-precip-collapse">
              <b-form-checkbox-group v-model="day6_keywords.precip" id="day6-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
          <!-- Day 7 Keywords -->
          <b-col class="keywords-col" id="keywords-day-7">
            <p>Enter Keywords:</p>
            <b-button variant="outline-info" v-b-toggle.day7-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day7-cold-collapse">
              <b-form-checkbox-group v-model="day7_keywords.cold" id="day7-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-warning" v-b-toggle.day7-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day7-warm-collapse">
              <b-form-checkbox-group v-model="day7_keywords.warm" id="day7-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-secondary" v-b-toggle.day7-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day7-storm-collapse">
              <b-form-checkbox-group v-model="day7_keywords.storm" id="day7-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
            </b-collapse>
            <br>
            <b-button variant="outline-primary" v-b-toggle.day7-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
            <b-collapse id="day7-precip-collapse">
              <b-form-checkbox-group v-model="day7_keywords.precip" id="day7-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
            </b-collapse>
          </b-col>
        </b-row>

      </b-card>
            </b-card>
    </b-card-group>

      <img v-bind:src="'data:image/png;base64,'+ plot1" width="500">
      <img v-bind:src="'data:image/png;base64,'+ plot2" width="500">
      <img v-bind:src="'data:image/png;base64,'+ plot3" width="500">
      <img v-bind:src="'data:image/png;base64,'+ plot4" width="500">

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
      // plots:
      plot1: '',
      plot2: '',
      plot3: '',
      plot4: '',
      // Weather Variables to give NOAA
      state_name: null,
      num_thunderous_days: 0, // null,
      max_wind: 0, // null,
      avg_temp: 55, // null,
      avg_max_temp: 65, // null,
      avg_min_temp: 45, // null,
      total_rain: 2, // null,
      total_snow: 0, // null,
      // Twitter Variables to give API
      day1_keywords: {
        cold: [],
        warm: [],
        storm: [],
        precip: []
      },
      day2_keywords: {},
      day3_keywords: {},
      day4_keywords: {},
      day5_keywords: {},
      day6_keywords: {},
      day7_keywords: {},
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
      coldOptions: [
        'Cold', 'Icy', 'Snowy', 'Frigid', 'Frost', 'Slippery', 'Blizzard', 'Freezing'
      ],
      warmOptions: [
        'Warm', 'Nice out', 'Sunny', 'Sunshine', 'Hot day', 'Humid', 'Heat wave', 'Dry heat'
      ],
      stormOptions: [
        'Wind', 'Windy', 'Brisk', 'Gusty', 'Hurricane', 'Storm', 'Nor\'easter', 'Thunder', 'Lightning'
      ],
      precipOptions: [
        'Rain', 'Snow', 'Cloudy', 'Sleet', 'Hail', 'Fog', 'Rainy', 'Dreary', 'Gloomy', 'Overcast', 'Flood'
      ],
      imageProps: { blank: true, height: 75, width: 400, class: 'm1' }
    }
  },
  methods: {
    useDate () {
      // Get the date range from a week ago until yesterday - format: [[start_date], [end_date]] i.e: ["YYYY-MM-DD", "YYYY-MM-DD"]
      var todaysDate = new Date()
      todaysDate = todaysDate.toISOString().split('T')[0]
      var oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 6)
      oneWeekAgo = oneWeekAgo.toISOString().split('T')[0]
      const datesRange = [oneWeekAgo.toString(), todaysDate.toString()]
      this.dateRange = datesRange

      // Push the date range to the backend
      const path = 'http://localhost:5000/api/request'
      const json = JSON.stringify({latitude: this.latitude, longitude: this.longitude, date: this.dateRange})
      axios.post(path, json, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then((response) => {
        console.log(response)
        this.cityName = response['data']['city']
        this.state_name = response['data']['state']
        this.max_wind = response['data']['maxwind_mph']
        this.avg_temp = response['data']['avgtemp_f']
        this.avg_max_temp = response['data']['maxtemp_f']
        this.avg_min_temp = response['data']['mintemp_f']
        this.total_precip = response['data']['totalprecip_in']
        this.total_snow = response['data']['snow_in']
        // this.total_rain = this.total_precip = this.total_snow
        // this.avg_wind = response['data']['avg_wind_speed']
        // this.avg_humidity = response['data']['avghumidity']
        // this.avg_cloud_cover = response['data']['avg_cloud_cover_percent']
        // IMAGES
        this.plot1 = response['data']['plots'][0]
        this.plot2 = response['data']['plots'][1]
        this.plot3 = response['data']['plots'][2]
        this.plot4 = response['data']['plots'][3]
      }).catch(function (error) {
        console.log(error)
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
    // Function that attaches to the save button
    saveDay1Keywords () {
      var keywords = this.day1_keywords.cold
      keywords = keywords.concat(this.day1_keywords.warm)
      keywords = keywords.concat(this.day1_keywords.storm)
      keywords = keywords.concat(this.day1_keywords.precip)

      const path = 'http://localhost:5000/api/twitter_request'
      var oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
      oneWeekAgo = oneWeekAgo.toISOString().split('T')[0]

      const json = JSON.stringify({keywords: keywords, latitude: this.latitude, longitude: this.longitude, radius: this.radius, date: oneWeekAgo})
      axios.post(path, json, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response)
      }).catch(function (error) {
        console.log(error)
      })
    }
  }
}
</script>

<style>
.button-dropdown{
  padding: 3px 10px;
  margin-bottom: 3px;
}
.header{
  border: 3px solid skyblue;
  text-align: center;
  vertical-align: middle;
  margin: 1px 1px 0px 1px;
  padding-top: 5px;
}
.keywords-col{
  border: 3px solid skyblue;
  margin: 0px 1px 1px 1px;
}
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
.space{
  margin-bottom: 25px;
}
.weather-card{
  margin-top: 20px;
}
</style>
