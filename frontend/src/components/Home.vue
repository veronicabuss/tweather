// Home.vue

<template>
  <div>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom" style="margin-bottom: 20px">New random number</button>

    <!-- Card that holds the inputs -->
    <b-card-group deck>
      <b-card
        border-variant="primary"
        header=" "
        header-bg-variant="primary"
        header-text-variant="white"
        align="left"
      >
        <b-card-text>Use the parameters below to see how people in that area are feeling about the weather.</b-card-text>
        <!-- Start of input form -->
        <b-form inline>
          <!-- City Selection -->
          <label class="mr-sm-2" for="id-city-selector">Choose a City:</label>
          <b-form-select
            id="id-city-selector"
            class="mb-2 mr-sm-2 mb-sm-0"
            :options="[{ text: 'Choose...', value: null }, 'Chicago', 'New York', 'Seattle']"
            :value="null"
          ></b-form-select>

          <!-- Date Range Selector -->
          <label class="mr-sm-2" for="id-date-range-picker"> Select a date range:</label>
          <date-picker v-model="dateRange" range id="id-date-range-picker"></date-picker>

          <!-- Submit Button -->
          <b-button variant="primary" style="margin-left: 10px">Let's Go</b-button>
        </b-form>

        <!-- dateRange is the output of the date range selector - I can't figure out how to get rid of the time
        part on the end so just chop it off
        Output:  [ "2020-10-13T04:00:00.000Z", "2020-10-15T04:00:00.000Z" ]
        So use:  [ "2020-10-13", "2020-10-15" ]-->
        <p>Selected Range: {{ dateRange }}</p>

        <!-- Styling - ignore -->
        <p class="or-label">or</p>

        <!-- Link to website where finding a coordinate circle is really easy -->
        <p>Use <a href="https://www.mapdevelopers.com/draw-circle-tool.php">this link</a> for an interactive coordinate circle finder map.
          Input the city / address, then click <b>"New Circle"</b>. Copy over the Position and Radius in miles.</p>

        <!-- Coordinate Circle Inputs -->
        <b-form class="coordinate-circle-wrapper">
          <!-- TODO: Fix styling so labels are inline  -->
          <label for="id-latitude">Latitude: </label>
          <b-form-input v-model="text" id="id-latitude" placeholder="Latitude"></b-form-input>
          <label for="id-longitude">Longitude: </label>
          <b-form-input v-model="text" id="id-longitude" placeholder="Longitude"></b-form-input>
          <label for="id-radius">Radius (in miles): </label>
          <b-form-input v-model="text" id="id-radius" placeholder="Radius (in miles)"></b-form-input>
        </b-form>

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
      dateRange: null,
      randomNumber: 0
    }
  },
  methods: {
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
#id-latitude, #id-longitude, #id-radius{
  margin-bottom: 10px;
}
.coordinate-circle-wrapper{
  width: 300px
}
.or-label{
  margin: 10px 45px;
}
</style>
