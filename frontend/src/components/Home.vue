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
          <label class="mr-sm-2" for="city-selection">Choose a City:</label>
          <b-form-select
            id="city-selection"
            class="mb-2 mr-sm-2 mb-sm-0"
            :options="[{ text: 'Choose...', value: null }, 'Chicago', 'New York', 'Seattle']"
            :value="null"
          ></b-form-select>

          <!-- Submit Button -->
          <b-button variant="primary" style="margin-left: 10px">Let's Go</b-button>
        </b-form>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
export default {
  data () {
    return {
      randomNumber: 0
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
