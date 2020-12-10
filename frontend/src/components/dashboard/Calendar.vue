<template>
    <div>
        <v-row class="fill-height">
            <v-col>
                <v-sheet height="64">
                    <v-toolbar flat>
                        <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
                            Vandaag
                        </v-btn>
                        <v-btn fab text small color="grey darken-2" @click="prev">
                            <v-icon small>
                                mdi-chevron-left
                            </v-icon>
                        </v-btn>
                        <v-btn fab text small color="grey darken-2" @click="next">
                            <v-icon small>
                                mdi-chevron-right
                            </v-icon>
                        </v-btn>
                        <v-toolbar-title v-if="$refs.calendar">
                            {{ $refs.calendar.title }}
                        </v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-menu bottom right>
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                                    <span>{{ typeToLabel[type] }}</span>
                                    <v-icon right>
                                        mdi-menu-down
                                    </v-icon>
                                </v-btn>
                            </template>
                            <v-list>
                                <v-list-item @click="type = 'day'">
                                    <v-list-item-title>Dag</v-list-item-title>
                                </v-list-item>
                                <v-list-item @click="type = 'week'">
                                    <v-list-item-title>Week</v-list-item-title>
                                </v-list-item>
                                <v-list-item @click="type = 'month'">
                                    <v-list-item-title>Maand</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </v-toolbar>
                </v-sheet>
                <v-sheet height="600">
                    <v-calendar
                        ref="calendar"
                        v-model="focus"
                        color="primary"
                        :first-interval="firstinterval"
                        :interval-count="intervalcount"
                        :events="events"
                        locale="nl"
                        :event-color="getEventColor"
                        :type="type"
                        :event-overlap-mode="mode"
                        @click:event="showEvent"
                        @click:more="viewDay"
                        @click:date="viewDay"
                        @change="getAllEvents()"
                    ></v-calendar>
<!--                                          @click:time="createEvent"-->
                </v-sheet>
            </v-col>
        </v-row>
      <v-dialog v-model="showEventModal" width="500" height="250" hide-overlay offset-x>
                        <v-card color="grey lighten-4" min-width="350px" flat>
                            <v-toolbar :color="selectedEvent.color" dark>
                                <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                                <v-spacer></v-spacer>
                            </v-toolbar>
                            <v-card-text>
                                <label for="email">Email: </label>
                                <span id="email" v-html="selectedEvent.email"></span><br />
                                <label for="phone">Telefoon: </label>
                                <span id="phone" v-html="selectedEvent.phone"></span><br />
                                <label for="treatments">Behandelingen: </label>
                                <span id="treatments" v-html="selectedEvent.treatments"></span><br />
                                <label for="stylist">Stylist: </label>
                                <span id="stylist" v-html="selectedEvent.stylist"></span>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn text color="secondary" @click="selectedOpen = false">
                                    Cancel
                                </v-btn>
                            </v-card-actions>
                        </v-card>
        </v-dialog>
        <v-dialog v-model="createEventModal" width="500" height="250" hide-overlay offset-x>
            <v-card>
                <v-toolbar dark color="indigo">
                    <v-card-title>
                        <span class="headline">Maak een afspraak</span>
                    </v-card-title>
                </v-toolbar>
                <v-card-text>
                    <br />
                    <label>Kies behandeling(en)</label>
                    <v-select id="picktreatments" v-model="select" :items="allTreatments" multiple outlined chips dense deletable-chips :menu-props="{ top: false, offsetY: true }" @change="calculateDuration()" tags ref="select"></v-select>
                    <div class="times">
                        <div class="timea">
                            <label for="startTime">Begintijd: </label>
                            <span id="startTime">{{ starttime }}</span>
                        </div>
                        <div class="timeb">
                            <label for="endtime">Eindtijd: </label>
                            <span id="endtime">{{ endtime }}</span>
                        </div>
                    </div>
                    <br />
                    <label>Stylist:</label>
                    <v-select id="pickstylist" placeholder="Geen voorkeur" :items="stylists" outlined dense :menu-props="{ top: false, offsetY: true }"> </v-select>
                    <label>Klant:</label>
                    <v-form>
                        <v-container>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <v-text-field :counter="15" label="Voornaam" required dense></v-text-field>
                                </v-col>

                                <v-col cols="12" md="6">
                                    <v-text-field :counter="15" label="Achternaam" dense></v-text-field>
                                </v-col>

                                <v-col cols="12" md="6">
                                    <v-text-field label="E-mail" dense></v-text-field>
                                </v-col>

                                <v-col cols="12" md="6">
                                    <v-text-field label="Telefoonnummer" dense></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-form>
                </v-card-text>
                <v-btn v-on:click="sendToBackEnd()" color="accent" elevation="2" block>Voeg afspraak toe </v-btn>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios';
export default {
  data: () => ({
    focus: '',
    type: 'week',
    typeToLabel: {
      month: 'Maand',
      week: 'Week',
      day: 'Dag'
    }, mode: 'column',
    weekday: [1, 2, 3, 4, 5, 6, 0],
    value: '',
    firstinterval: '8',
    intervalcount: '12',
    events: [],
    select: [{text: 'Knippen & Stylen', value: '30'}],
    allTreatments: [],
    eventColor:  ['primary', 'red'],
    stylists: ['Geen voorkeur', 'Gert', 'Truus', 'Piet', 'Julia'],
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    createEventModal: false,
    showEventModal: false,
    tms: '',
    starttime: '',
    endtime: '',
  }),
  created() {
    this.getData();
  },
  mounted() {
    this.$refs.calendar.checkChange();
  },
  methods: {
    sendToBackEnd(){
    console.log('fun')
    },
    calculateDuration(endtime) {
      this.endtime = endtime;
      let sum = 0;
      for (let i = 0; i < this.select.length; i++) {
        sum += (parseFloat(this.select[i]));
      }
      let [hours, minutes] = this.starttime.split(':');
      hours = parseInt(hours);
      minutes = parseInt(minutes);
      minutes += sum;
      this.endtime = (hours * 60) + minutes;     // Convert hours and minutes to time in minutes
      let rounded = Math.round(this.endtime / 15) * 15;
      let rHr = '' + Math.floor(rounded / 60)
      let rMin = '' + rounded % 60
      this.endtime = rHr.padStart(2, '0') + ':' + rMin.padStart(2, '0')
      setTimeout(() => {
        this.$refs.select.isMenuActive = false
      }, 50)
    },
    createEvent(tms) {
      if (this.createEventModal == false) {
        this.tms = tms
        //Starttime minutes
        let [hours, minutes] = this.tms.time.split(':');
        hours = parseInt(hours);
        minutes = parseInt(minutes);
        this.tms.time = (hours * 60) + minutes;     // Convert hours and minutes to time in minutes
        let rounded = Math.round(this.tms.time / 15) * 15;
        let rHr = '' + Math.floor(rounded / 60)
        let rMin = '' + rounded % 60
        this.starttime = rHr.padStart(2, '0') + ':' + rMin.padStart(2, '0')
        this.endtime = this.starttime;
        //Endtime minutes
        let [endHours, endMinutes] = this.endtime.split(':');
        endHours = parseInt(endHours);
        endMinutes = parseInt(endMinutes);
        endMinutes += 30;
        this.endtime = (endHours * 60) + endMinutes;
        let endRounded = Math.round(this.endtime / 15) * 15;
        let endrHr = '' + Math.floor(endRounded / 60)
        let endrMin = '' + endRounded % 60
        this.endtime = endrHr.padStart(2, '0') + ':' + endrMin.padStart(2, '0')
        this.createEventModal = true
      } else {
        this.createEventModal = false;
      }
    },
    viewDay({date}) {
      this.focus = date
      this.type = 'day'
    },
    setToday() {
      this.focus = ''
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    async getData() {
      let self = this;
      await axios.get('https://my-json-server.typicode.com/liambenschop/school/treatments/', {}
      ).then((response) => {
        response.data.forEach(item => {
          self.allTreatments.push({
            text: item.title,
            value: item.duration
          })
        })
      })
    },
    async updateRange() {
      let events = []
      await axios.get('https://my-json-server.typicode.com/liambenschop/school/events/', {}
      ).then((response) => {
        response.data.forEach(item => {
          events.push({
            name: item.name,
            treatments: item.treatments,
            email: item.email,
            phone: item.phone_number,
            color: this.colors[this.rnd(0, this.colors.length - 1)]
          })
        })
        this.events = events
      })
    },
    async getAllEvents(){
      let self = this;
      await axios.get(`${self.$store.state.HOST}/api/appointments/get_free_places/`,
      {}
      ).then(res => {
        res.data.forEach(times => {
          self.events.push({
            name: times.taked ? "Bezet" : "Vrije Afspraak",
            start: times.start,
            end: times.end,
            color: times.taked ? self.eventColor[1] : self.eventColor[0],
            timed: true
          })
        });
      }).catch(e => {
        console.log(e)
      })
    },
    getEventColor(event) {
      return event.color
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    showEvent({nativeEvent, event}) {
      this.selectedEvent = event
      this.selectedElement = nativeEvent.target
      if (this.selectedEvent.color == 'red') {
        if (this.showEventModal == false) {
          setTimeout(() => {
            this.showEventModal = true
          }, 10)
        } else {
          this.showEventModal = false;
        }
      } else {
        this.createEventModal = true
      }
    }
  },
}
</script>

<style scoped>
#appointmentbtn {
  right: 15px;
  position: absolute;
  bottom: 15px;
}
form .container {
  padding: 0 !important;
}
.times {
  width: 50%;
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}
</style>