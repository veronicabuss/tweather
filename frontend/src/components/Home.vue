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
            <b-title style="font-size:18pt">Weather in {{cityName}}, {{state_name}}: </b-title>
            <!-- Headers for the plots -->
            <b-row style="margin-top: 10px">
              <b-col>
                <h5 style="text-align:center">Average Temp: <strong>{{avg_temp}}°F</strong></h5>
              </b-col>
              <b-col>
                <h5 style="text-align:center">Max wind speed: {{max_wind}} mph</h5>
              </b-col>
              <b-col>
                <h5 style="text-align:center">Average Humidity: {{avg_humidity}}</h5>
              </b-col>
            </b-row>

            <!-- Weather Plots -->
            <b-row>
              <b-col style="margin: 0 -10px;">
                <b-img v-bind:src="'data:image/png;base64,'+ plot2" alt="Temperature/Precipitation Plot" @mouseover="plotTriggered(0, true)" @mouseleave="plotTriggered(0, false)"
                :style="[this.mouseOverTriggered ? plotTriggeredClass.plot1 : restingClass]"></b-img>
              </b-col>
              <b-col style="margin: 0 -10px">
                 <b-img v-bind:src="'data:image/png;base64,'+ plot1" alt="Wind Speed/Direction Plot" @mouseover="plotTriggered(1, true)" @mouseleave="plotTriggered(1, false)"
                :style="[this.mouseOverTriggered ? plotTriggeredClass.plot2 : restingClass]"></b-img>
              </b-col>
              <b-col style="margin: 0 -10px">
                <b-img v-bind:src="'data:image/png;base64,'+ plot4" alt="Visibility/Humidity Plot" @mouseover="plotTriggered(2, true)" @mouseleave="plotTriggered(2, false)"
                :style="[this.mouseOverTriggered ? plotTriggeredClass.plot3 : restingClass]"></b-img>
              </b-col>
            </b-row>

            <!-- Footers for the plots -->
            <b-row>
              <b-col>
                <h5 style="text-align:center">Min Temp: {{min_temp}}°F - Max Temp: {{max_temp}}°F</h5>
              </b-col>
              <b-col>
                <h5 style="text-align:center">Total Precipitation: {{total_precip}} in <br> Rain: {{total_rain}} in, Snow: {{total_snow}} in</h5>
              </b-col>
              <b-col>
                <h5 style="text-align:center">Average cloud cover percent: {{avg_cloud_cover}}%</h5>
              </b-col>
            </b-row>

          </b-card>
        </b-collapse>

        <!-- Select Keywords card -->
        <b-card>
          <!-- Date Header Row -->
          <b-row class="header-row">
            <b-col class="header" id="date-header-1">
              <h3>{{ this.daysInRange[0][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-2">
              <h3>{{ this.daysInRange[1][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-3">
              <h3>{{ this.daysInRange[2][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-4">
              <h3>{{ this.daysInRange[3][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-5">
              <h3>{{ this.daysInRange[4][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-6">
              <h3>{{ this.daysInRange[5][0]}}</h3>
            </b-col>
            <b-col class="header" id="date-header-7">
              <h3>{{ this.daysInRange[6][0]}}</h3>
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
                <b-form-checkbox-group v-model="keywords.day1.cold" id="day1-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <!-- Warm Keywords Dropdown Button -->
              <b-button variant="outline-warning" v-b-toggle.day1-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day1-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day1.warm" id="day1-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <!-- Storm Keywords Dropdown Button -->
              <b-button variant="outline-secondary" v-b-toggle.day1-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day1-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day1.storm" id="day1-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <!-- Precipitation Keywords Dropdown Button -->
              <b-button variant="outline-primary" v-b-toggle.day1-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day1-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day1.precip" id="day1-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day1', daysInRange[0][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 2 Keywords -->
            <b-col class="keywords-col" id="keywords-day-2">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day2-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day2-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day2.cold" id="day2-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day2-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day2-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day2.warm" id="day2-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day2-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day2-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day2.storm" id="day2-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day2-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day2-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day2.precip" id="day2-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day2', daysInRange[1][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 3 Keywords -->
            <b-col class="keywords-col" id="keywords-day-3">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day3-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day3-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day3.cold" id="day3-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day3-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day3-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day3.warm" id="day3-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day3-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day3-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day3.storm" id="day3-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day3-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day3-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day3.precip" id="day3-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day3', daysInRange[2][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 4 Keywords -->
            <b-col class="keywords-col" id="keywords-day-4">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day4-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day4-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day4.cold" id="day4-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day4-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day4-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day4.warm" id="day4-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day4-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day4-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day4.storm" id="day4-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day4-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day4-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day4.precip" id="day4-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day4', daysInRange[3][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 5 Keywords -->
            <b-col class="keywords-col" id="keywords-day-5">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day5-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day5-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day5.cold" id="day5-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day5-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day5-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day5.warm" id="day5-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day5-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day5-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day5.storm" id="day5-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day5-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day5-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day5.precip" id="day5-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day5', daysInRange[4][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 6 Keywords -->
            <b-col class="keywords-col" id="keywords-day-6">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day6-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day6-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day6.cold" id="day6-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day6-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day6-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day6.warm" id="day6-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day6-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day6-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day6.storm" id="day6-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day6-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day6-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day6.precip" id="day6-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day6', daysInRange[5][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
            <!-- Day 7 Keywords -->
            <b-col class="keywords-col" id="keywords-day-7">
              <p>Enter Keywords:</p>
              <b-button variant="outline-info" v-b-toggle.day7-cold-collapse class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day7-cold-collapse">
                <b-form-checkbox-group v-model="keywords.day7.cold" id="day7-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-warning" v-b-toggle.day7-warm-collapse class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day7-warm-collapse">
                <b-form-checkbox-group v-model="keywords.day7.warm" id="day7-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-secondary" v-b-toggle.day7-storm-collapse class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day7-storm-collapse">
                <b-form-checkbox-group v-model="keywords.day7.storm" id="day7-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
              </b-collapse>
              <br>
              <b-button variant="outline-primary" v-b-toggle.day7-precip-collapse class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
              <b-collapse id="day7-precip-collapse">
                <b-form-checkbox-group v-model="keywords.day7.precip" id="day7-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
              </b-collapse>
              <b-button variant="info" @click="saveKeywords('day7', daysInRange[6][1])" style="margin: 10px 0; width: 80%">Save</b-button>
            </b-col>
          </b-row>
        </b-card>

      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  created () {
    // Initialize the keywords object
    this.keywords = {}
    for (var i = 0; i < 7; i++) {
      var keyName = 'day' + (i + 1).toString()
      this.keywords[keyName] = {
        cold: [],
        warm: [],
        storm: [],
        precip: []
      }
    }

    // Get the date range from a week ago until yesterday - format: [[start_date], [end_date]] i.e: ["YYYY-MM-DD", "YYYY-MM-DD"]
    var todaysDate = new Date()
    todaysDate = todaysDate.toISOString().split('T')[0]
    var oneWeekAgo = new Date()
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 6)
    oneWeekAgo = oneWeekAgo.toISOString().split('T')[0]
    const datesRange = [oneWeekAgo.toString(), todaysDate.toString()]
    this.dateRange = datesRange

    // Get the strings for each date
    var allDays = []
    for (i = 6; i >= 0; i--) {
      var aDate = new Date()
      aDate.setDate(aDate.getDate() - i)
      allDays.push([aDate.toString().split(' 202')[0], aDate.toISOString().split('T')[0]])
    }
    this.daysInRange = allDays
  },
  data () {
    return {
      // plots:
      plot1: '',
      plot2: '',
      plot3: '',
      plot4: '',
      // Weather Variables to give NOAA
      state_name: null,
      max_wind: 0, // null,
      avg_temp: 55, // null,
      max_temp: 65, // null,
      min_temp: 45, // null,
      total_rain: 2.0, // null,
      total_snow: 0, // null,
      // Twitter Variables to give API
      keywords: {},
      // Other Variables
      total_precip: null,
      dateRange: null,
      daysInRange: [],
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
        { text: 'Kalamazoo', value: 'Kalamazoo,42.268382,-85.589971,9.0,https://rb.gy/foemki' },
        { text: 'Chicago', value: 'Chicago,41.876584,-87.639529,10.0,https://rb.gy/qwsmxo' },
        { text: 'Miami', value: 'Miami,25.783447,-80.214909,5.0,https://rb.gy/j3u5bo' },
        { text: 'New York City', value: 'New York City,40.633541,-73.915357,15.76,https://rb.gy/n5g7tf' },
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
      imageProps: { blank: true, height: 75, width: 400, class: 'm1' },
      restingClass: { 'width': '100%' },
      plotTriggeredClass: {
        plot1: {},
        plot2: {},
        plot3: {}
      },
      mouseOverTriggered: false
    }
  },
  methods: {
    useDate () {
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
        this.max_wind = response['data']['week']['maxwind_mph']
        this.avg_temp = response['data']['week']['avgtemp_f'].toFixed(1)
        this.max_temp = response['data']['week']['maxtemp_f']
        this.min_temp = response['data']['week']['mintemp_f']
        // this.total_precip = response['data']['week']['totalprecip_in'].toFixed(1)
        this.total_precip = response['data']['week']['avg_precip'].toFixed(2)
        this.total_snow = response['data']['week']['snow_in'].toFixed(2)
        this.total_rain = (this.total_precip - this.total_snow).toFixed(2)
        this.avg_wind = response['data']['week']['avg_wind_speed']
        this.avg_humidity = response['data']['week']['avghumidity'].toFixed(2)
        this.avg_cloud_cover = response['data']['week']['avg_cloud_cover_percent'].toFixed(2)
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
    saveKeywords (dayNum, dayStg) {
      var dayKeywords = this.keywords[dayNum].cold
      dayKeywords = dayKeywords.concat(this.keywords[dayNum].warm)
      dayKeywords = dayKeywords.concat(this.keywords[dayNum].storm)
      dayKeywords = dayKeywords.concat(this.keywords[dayNum].precip)
      console.log(dayKeywords)

      const path = 'http://localhost:5000/api/twitter_request'
      const json = JSON.stringify({keywords: dayKeywords, latitude: this.latitude, longitude: this.longitude, radius: this.radius, date: dayStg})
      axios.post(path, json, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response)
      }).catch(function (error) {
        console.log(error)
      })
    },
    plotTriggered (plotNum, onOff) {
      // Turns plot zoom trigger off if the mouse leaves a plot and on if it enters
      if (onOff) {
        this.mouseOverTriggered = true
      } else {
        this.mouseOverTriggered = false
      }

      // Sets the plot size class based on what plot was hovered over
      if (plotNum === 0) {
        this.plotTriggeredClass.plot1 = {'width': '150%', 'transition': 'transform .2s'}
        this.plotTriggeredClass.plot2 = {'width': '50%', 'float': 'right'}
        this.plotTriggeredClass.plot3 = {'width': '50%', 'float': 'right'}
      } else if (plotNum === 1) {
        this.plotTriggeredClass.plot1 = {'width': '50%', 'float': 'left'}
        this.plotTriggeredClass.plot2 = {'width': '150%', 'float': 'left', 'position': 'relative', 'right': '20%', 'transition': 'transform .2s'}
        this.plotTriggeredClass.plot3 = {'width': '50%', 'float': 'right'}
      } else {
        this.plotTriggeredClass.plot1 = {'width': '50%', 'float': 'left'}
        this.plotTriggeredClass.plot2 = {'width': '50%', 'float': 'left'}
        this.plotTriggeredClass.plot3 = {'width': '150%', 'float': 'left', 'position': 'relative', 'right': '40%', 'transition': 'transform .2s'}
      }
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
