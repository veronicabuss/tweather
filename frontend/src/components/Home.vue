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

        <!-- Styling - ignore -->
        <p style="margin-left: 45px">or</p>
        
        <!-- dateRange is the output of the date range selector - I can't figure out how to get rid of the time
        part on the end so just chop it off 
        Output:  [ "2020-10-13T04:00:00.000Z", "2020-10-15T04:00:00.000Z" ] 
        So use:  [ "2020-10-13", "2020-10-15" ]-->
        <p>Selected Range: {{ dateRange }}</p>

      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import DatePicker from 'vue2-datepicker'  
import 'vue2-datepicker/index.css'
export default {
  components: { DatePicker },
  data () {
    return {
      randomNumber: 0,
      dateRange: null
    }
  },
  methods: {
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    getRandom () {
      this.randomNumber = this.getRandomInt(1, 100)
    }
  },
  created () {
    this.getRandom()
  }
}
</script>
