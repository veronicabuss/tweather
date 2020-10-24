// Home.vue

<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>
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
