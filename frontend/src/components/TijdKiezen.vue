<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
        <v-toolbar
          flat
        >
          <v-btn
            outlined
            class="mr-4"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="prev"
          >
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="next"
          >
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer>
          </v-spacer>
          <v-toolbar-title>
            Kies een afspraak:
          </v-toolbar-title>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="550">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="eventColor"
          :type="type"
          :weekdays="weekdays"
          :first-interval="firstinterval"
          :interval-count="intervalcount"
          :interval-format="intervalFormat"
          :locale='locale'
          @click:event="bevestigAfspraak"
        ></v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>
  
<script>
import axios from 'axios';

export default {
  data: () => ({
    focus: '',
    type: 'week',
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    firstinterval: '9',
    intervalcount: '9',
    locale: 'nl',
    selectedEvent: {},
    eventColor: 'primary',
    events: [],
  }),
  async created() {
    try {
      const res = await axios.get(`https://run.mocky.io/v3/b456ae47-4cfe-438b-8098-cda5ebb8bbf3`)

      this.events = res.data.events;
    } catch(e) {
      console.error(e)
    }
  },
  mounted () {
    this.$refs.calendar.checkChange()
  },
  methods: {
    setToday () {
      this.focus = ''
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    // updateRange ({ start, end }) {
      
    // },
    intervalFormat(interval) {
      return interval.time
    },
    bevestigAfspraak ({ event }) {
      this.selectedEvent = event
      this.$emit('selectie', this.selectedEvent)
      this.$router.push('afspraak-bevestigen')
    },
  },
}
</script>

<style scoped>
  .v-calendar-daily__scroll-area {
    overflow: hidden;
  }

</style>