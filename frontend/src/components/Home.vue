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
        <b-card-text>Use the parameters below to see how people in that area were feeling about the weather this week.</b-card-text>
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
          <b-button @click="useDate" variant="primary" style="margin-left: 10px">Let's Go</b-button>
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

        <!-- Spinner for indicating loading -->
        <div style="text-align: center">
          <b-spinner variant="primary" v-if="weatherCardLoading" style="width: 3rem; height: 3rem;"></b-spinner>
        </div>
        <!-- Weather Data card -->
        <b-collapse v-model="weatherCardDoneLoading" >
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
        <b-collapse v-model="weatherCardDoneLoading">
          <b-card>
            <!-- Date Header Row -->
            <b-row class="header-row">
              <b-col class="header" id="date-header-1">
                <h4>{{ this.daysInRange[0][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-2">
                <h4>{{ this.daysInRange[1][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-3">
                <h4>{{ this.daysInRange[2][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-4">
                <h4>{{ this.daysInRange[3][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-5">
                <h4>{{ this.daysInRange[4][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-6">
                <h4>{{ this.daysInRange[5][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-7">
                <h4>{{ this.daysInRange[6][0]}}</h4>
              </b-col>
            </b-row>
            <!-- Keywords Row -->
            <b-row class="keywords-row">
              <!-- Day 1 Keywords -->
              <b-col class="keywords-col" id="keywords-day-1">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day1')">{{collapses.day1.text}}</b-button>
                <p>Enter Keywords:</p>
                <!-- Cold Keywords Dropdown Button -->
                <b-button variant="outline-info" @click="toggleAndUpdate('day1', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day1.cold">
                  <b-form-checkbox-group v-model="keywords.day1.cold" id="day1-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <!-- Warm Keywords Dropdown Button -->
                <b-button variant="outline-warning" @click="toggleAndUpdate('day1', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day1.warm">
                  <b-form-checkbox-group v-model="keywords.day1.warm" id="day1-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <!-- Storm Keywords Dropdown Button -->
                <b-button variant="outline-dark" @click="toggleAndUpdate('day1', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse id="day1-storm-collapse" v-model="collapses.day1.storm">
                  <b-form-checkbox-group v-model="keywords.day1.storm" id="day1-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <!-- Precipitation Keywords Dropdown Button -->
                <b-button variant="outline-primary" @click="toggleAndUpdate('day1', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse id="day1-precip-collapse" v-model="collapses.day1.precip">
                  <b-form-checkbox-group v-model="keywords.day1.precip" id="day1-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>

                <!-- Save and Apply to All buttons -->
                <b-button variant="info" @click="saveKeywords('day1', daysInRange[0][1])" style="margin: 10px 5px; width: 80%">Save</b-button>
                <b-button variant="secondary" @click="applyToAll" style="width: 90%; margin-bottom: 10px">Apply to All</b-button>
              </b-col>
              <!-- Day 2 Keywords -->
              <b-col class="keywords-col" id="keywords-day-2">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day2')">{{collapses.day2.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day2', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day2.cold">
                  <b-form-checkbox-group v-model="keywords.day2.cold" id="day2-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day2', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day2.warm">
                  <b-form-checkbox-group v-model="keywords.day2.warm" id="day2-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day2', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day2.storm">
                  <b-form-checkbox-group v-model="keywords.day2.storm" id="day2-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day2', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day2.precip">
                  <b-form-checkbox-group v-model="keywords.day2.precip" id="day2-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day2', daysInRange[1][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
              <!-- Day 3 Keywords -->
              <b-col class="keywords-col" id="keywords-day-3">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day3')">{{collapses.day3.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day3', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day3.cold">
                  <b-form-checkbox-group v-model="keywords.day3.cold" id="day3-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day3', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day3.warm">
                  <b-form-checkbox-group v-model="keywords.day3.warm" id="day3-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day3', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day3.storm">
                  <b-form-checkbox-group v-model="keywords.day3.storm" id="day3-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day3', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day3.precip">
                  <b-form-checkbox-group v-model="keywords.day3.precip" id="day3-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day3', daysInRange[2][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
              <!-- Day 4 Keywords -->
              <b-col class="keywords-col" id="keywords-day-4">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day4')">{{collapses.day4.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day4', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day4.cold">
                  <b-form-checkbox-group v-model="keywords.day4.cold" id="day4-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day4', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day4.warm">
                  <b-form-checkbox-group v-model="keywords.day4.warm" id="day4-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day4', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day4.storm">
                  <b-form-checkbox-group v-model="keywords.day4.storm" id="day4-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day4', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day4.precip">
                  <b-form-checkbox-group v-model="keywords.day4.precip" id="day4-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day4', daysInRange[3][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
              <!-- Day 5 Keywords -->
              <b-col class="keywords-col" id="keywords-day-5">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day5')">{{collapses.day5.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day5', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day5.cold">
                  <b-form-checkbox-group v-model="keywords.day5.cold" id="day5-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day5', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day5.warm">
                  <b-form-checkbox-group v-model="keywords.day5.warm" id="day5-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day5', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day5.storm">
                  <b-form-checkbox-group v-model="keywords.day5.storm" id="day5-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day5', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day5.precip">
                  <b-form-checkbox-group v-model="keywords.day5.precip" id="day5-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day5', daysInRange[4][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
              <!-- Day 6 Keywords -->
              <b-col class="keywords-col" id="keywords-day-6">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day6')">{{collapses.day6.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day6', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day6.cold">
                  <b-form-checkbox-group v-model="keywords.day6.cold" id="day6-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day6', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day6.warm">
                  <b-form-checkbox-group v-model="keywords.day6.warm" id="day6-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day6', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day6.storm">
                  <b-form-checkbox-group v-model="keywords.day6.storm" id="day6-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day6', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day6.precip">
                  <b-form-checkbox-group v-model="keywords.day6.precip" id="day6-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day6', daysInRange[5][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
              <!-- Day 7 Keywords -->
              <b-col class="keywords-col" id="keywords-day-7">
                <b-button variant="warning" class="expand-collapse-button" @click="expandOrCollapse('day7')">{{collapses.day7.text}}</b-button>
                <p>Enter Keywords:</p>
                <b-button variant="outline-info" @click="toggleAndUpdate('day7', 'cold')" class="button-dropdown">Cold <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day7.cold">
                  <b-form-checkbox-group v-model="keywords.day7.cold" id="day7-cold-checkboxes" :options="coldOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-warning" @click="toggleAndUpdate('day7', 'warm')" class="button-dropdown">Warm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day7.warm">
                  <b-form-checkbox-group v-model="keywords.day7.warm" id="day7-warm-checkboxes" :options="warmOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-dark" @click="toggleAndUpdate('day7', 'storm')" class="button-dropdown">Storm <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day7.storm">
                  <b-form-checkbox-group v-model="keywords.day7.storm" id="day7-storm-checkboxes" :options="stormOptions"></b-form-checkbox-group>
                </b-collapse>
                <br>
                <b-button variant="outline-primary" @click="toggleAndUpdate('day7', 'precip')" class="button-dropdown">Precipitation <b-icon icon="chevron-down" scale="0.8"></b-icon></b-button>
                <b-collapse v-model="collapses.day7.precip">
                  <b-form-checkbox-group v-model="keywords.day7.precip" id="day7-precip-checkboxes" :options="precipOptions"></b-form-checkbox-group>
                </b-collapse>
                <b-button variant="info" @click="saveKeywords('day7', daysInRange[6][1])" style="margin: 10px 0; width: 80%">Save</b-button>
              </b-col>
            </b-row>
            <!-- Save and Clear all buttons -->
            <b-button-group style="width: 100%; margin-top: 10px">
              <b-button variant="outline-success" style="width: 50%" @click="saveAll" >Save All</b-button>
              <b-button variant="outline-danger" style="width: 50%" @click="clearAll" >Clear All</b-button>
            </b-button-group>
          </b-card>
        </b-collapse>

        <!-- Twitter Output card -->
        <b-collapse v-model="weatherCardDoneLoading">
          <b-card>
            <!-- Date Header Row -->
            <b-row class="header-row">
              <b-col class="header" id="date-header-1">
                <h4>{{ this.daysInRange[0][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-2">
                <h4>{{ this.daysInRange[1][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-3">
                <h4>{{ this.daysInRange[2][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-4">
                <h4>{{ this.daysInRange[3][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-5">
                <h4>{{ this.daysInRange[4][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-6">
                <h4>{{ this.daysInRange[5][0]}}</h4>
              </b-col>
              <b-col class="header" id="date-header-7">
                <h4>{{ this.daysInRange[6][0]}}</h4>
              </b-col>
            </b-row>
            <!-- twitterResults Row -->
            <b-row class="twitterResults-row">
              <!-- Day 1 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-1">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day1'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day1'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day1'].max_sentiment[0]}}</strong> - "{{twitterResults['day1'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day1'].min_sentiment[0]}}</strong> - "{{twitterResults['day1'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 2 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-2">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day2'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day2'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day2'].max_sentiment[0]}}</strong> - "{{twitterResults['day2'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day2'].min_sentiment[0]}}</strong> - "{{twitterResults['day2'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 3 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-3">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day3'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day3'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day3'].max_sentiment[0]}}</strong> - "{{twitterResults['day3'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day3'].min_sentiment[0]}}</strong> - "{{twitterResults['day3'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 4 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-4">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day4'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day4'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day4'].max_sentiment[0]}}</strong> - "{{twitterResults['day4'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day4'].min_sentiment[0]}}</strong> - "{{twitterResults['day4'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 5 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-5">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day5'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day5'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day5'].max_sentiment[0]}}</strong> - "{{twitterResults['day5'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day5'].min_sentiment[0]}}</strong> - "{{twitterResults['day5'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 6 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-6">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day6'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day6'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day6'].max_sentiment[0]}}</strong> - "{{twitterResults['day6'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day6'].min_sentiment[0]}}</strong> - "{{twitterResults['day6'].min_sentiment[1]}}"
              </b-col>
              <!-- Day 7 Twitter Results -->
              <b-col class="twitterResults-col" id="twitterResults-day-7">
                <div><div class="text-primary" style="float: left"><strong>Avg Sentiment:</strong></div> {{twitterResults['day7'].avg_sentiment}}</div>
                <div><strong># of Tweets:</strong> {{twitterResults['day7'].num_tweets}}</div><br>
                <div class="text-success"><strong>Max Sentiment:</strong></div><strong>{{twitterResults['day7'].max_sentiment[0]}}</strong> - "{{twitterResults['day7'].max_sentiment[1]}}"<br><br>
                <div class="text-danger"><strong>Min Sentiment:</strong></div><strong>{{twitterResults['day7'].min_sentiment[0]}}</strong> - "{{twitterResults['day7'].min_sentiment[1]}}"
              </b-col>
            </b-row>
          </b-card>
        </b-collapse>

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

    // Initialize the collapses
    this.collapses = {}
    for (i = 0; i < 7; i++) {
      keyName = 'day' + (i + 1).toString()
      this.collapses[keyName] = {
        cold: false,
        warm: false,
        storm: false,
        precip: false,
        text: 'Expand All'
      }
    }

    // Get the date range from a week ago until yesterday - format: [[start_date], [end_date]] i.e: ["YYYY-MM-DD", "YYYY-MM-DD"]
    var todaysDate = new Date()
    todaysDate.setDate(todaysDate.getDate() - 1) // Iso String makes you subtract one for today's date
    todaysDate = todaysDate.toISOString().split('T')[0]
    var oneWeekAgo = new Date()
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
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

    // Initialize the twitter twitterResults object
    this.twitterResults = {}
    for (i = 0; i < 7; i++) {
      var dayNum = 'day' + (i + 1).toString()
      this.twitterResults[dayNum] = {
        avg_sentiment: 0,
        max_sentiment: [0, ''],
        min_sentiment: [0, ''],
        num_tweets: 0
      }
    }
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
      avg_humidity: 0,
      avg_cloud_cover: 0,
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
      collapses: {},
      twitterResults: {},
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
      mouseOverTriggered: false,
      weatherCardLoading: false,
      weatherCardDoneLoading: false
    }
  },
  methods: {
    useDate () {
      // Push the date range to the backend
      this.weatherCardLoading = true
      // Re-renders the page with new updates
      this.$forceUpdate()
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
        this.total_precip = response['data']['week']['total_precip'].toFixed(1)
        // this.total_precip = response['data']['week']['total_precip'].toFixed(2)
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
        // Disable spinner and enable cards
        this.weatherCardLoading = false
        this.weatherCardDoneLoading = true
      }).catch(function (error) {
        // Disable spinner
        this.weatherCardLoading = false
        console.log(error)
      })
    },
    // On select of a city, updates the manual select buttons with prepopulated data
    processCity () {
      this.weatherCardDoneLoading = false
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
    async saveKeywords (dayNum, dayStg) {
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
      }).then((response) => {
        if (response) {
          this.twitterResults[dayNum].avg_sentiment = response['data'][dayStg]['average_sentiment'].toFixed(2)
          this.twitterResults[dayNum].max_sentiment = response['data'][dayStg]['max_sentiment']
          this.twitterResults[dayNum].min_sentiment = response['data'][dayStg]['min_sentiment']
          this.twitterResults[dayNum].num_tweets = response['data'][dayStg]['number_of_tweets']
          // Add decimal places
          this.twitterResults[dayNum].max_sentiment[0] = this.twitterResults[dayNum].max_sentiment[0].toFixed(3)
          this.twitterResults[dayNum].min_sentiment[0] = this.twitterResults[dayNum].min_sentiment[0].toFixed(3)
          console.log(this.twitterResults[dayNum])
          // Re-renders the page with new updates
          this.$forceUpdate()
        }
      }).catch((error) => {
        var msg = 'Either something went wrong or there are no tweets for ' + dayStg + ' :(. Try fewer or different keywords'
        this.makeToast(msg, 'danger', 'Failed to Pull Relevant Tweets')
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
    },
    expandOrCollapse (dayNum) {
      console.log(this.collapses)
      if (this.collapses[dayNum].text === 'Expand All') {
        this.collapses[dayNum].text = 'Collapse All'
        this.collapses[dayNum].cold = true
        this.collapses[dayNum].warm = true
        this.collapses[dayNum].precip = true
        this.collapses[dayNum].storm = true
      } else {
        this.collapses[dayNum].text = 'Expand All'
        this.collapses[dayNum].cold = false
        this.collapses[dayNum].warm = false
        this.collapses[dayNum].precip = false
        this.collapses[dayNum].storm = false
      }
      // Re-renders the page with new updates
      this.$forceUpdate()
    },
    toggleAndUpdate (dayNum, el) {
      // Toggles the desired collapse
      this.collapses[dayNum][el] = !this.collapses[dayNum][el]
      // Re-renders the page with new updates
      this.$forceUpdate()
    },
    applyToAll () {
      // Applies the day1 selected keywords to all of the checkboxes
      for (var i = 1; i < 7; i++) {
        var dayNum = 'day' + (i + 1).toString()
        Object.assign(this.keywords[dayNum], this.keywords['day1'])
      }
      // Re-renders the page with new updates
      this.$forceUpdate()
      // Success message
      this.makeToast('Applied keywords to all the days')
    },
    // Saves all the keywords in the range
    async saveAll () {
      for (var i = 0; i < this.daysInRange.length; i++) {
        var dayNum = 'day' + (i + 1).toString()
        await this.saveKeywords(dayNum, this.daysInRange[i][1])
      }
    },
    // Clears all the keywords
    clearAll () {
      for (var i = 0; i < 7; i++) {
        var dayNum = 'day' + (i + 1).toString()
        this.keywords[dayNum] = {
          cold: [],
          warm: [],
          storm: [],
          precip: []
        }
      }
      for (i = 0; i < 7; i++) {
        dayNum = 'day' + (i + 1).toString()
        this.twitterResults[dayNum] = {
          avg_sentiment: 0,
          max_sentiment: [0, ''],
          min_sentiment: [0, ''],
          num_tweets: 0
        }
      }
      // Re-renders the page with new updates
      this.$forceUpdate()
      // Success message
      this.makeToast('Cleared the keywords', 'warning')
    },
    // Little dismissisable notification message
    makeToast (message, variant = 'success', title = 'Success') {
      this.$bvToast.toast(message, {
        title: title,
        toaster: 'b-toaster-top-left',
        variant: variant,
        solid: true
      })
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
* {
  font-family: 'Montserrat', sans-serif;
}

.expand-collapse-button{
  text-align: center;
  margin: 10px;
}
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
.keywords-col, .twitterResults-col{
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
