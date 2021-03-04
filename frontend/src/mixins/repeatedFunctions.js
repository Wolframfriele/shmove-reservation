// define a mixin object
export default {
  methods: {
    dateToString(datum) {
      const days = [
        "zondag",
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag"
      ];
      const months = [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december"
      ];
      
      const dateString = datum.split(" ")[0]
      
      const year_int = parseInt(dateString.split("-")[0])
      const month_int = parseInt(dateString.split("-")[1])
      const day_int = parseInt(dateString.split("-")[2])

      let reserverings_tijd = new Date(year_int, month_int, day_int)

      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const date = reserverings_tijd.getDate();
      const monthIndex = reserverings_tijd.getMonth();
      const month = months[monthIndex];

      if (datum.split(" ").length == 2) {
        const timeString = datum.split(" ")[1]

        const hour_int = parseInt(timeString.split(':')[0])
        const minutes_int = parseInt(timeString.split(':')[1])

        reserverings_tijd = new Date(year_int, month_int, day_int, hour_int, minutes_int)
        const hours = reserverings_tijd.getHours();
        const minutes = String(reserverings_tijd.getMinutes()).padStart(2, '0');

        return `${day} ${date} ${month} om ${hours}:${minutes}`; 
      } else {
        return `${day} ${date} ${month}`; 
      }      
    },
    parseDate(inputString) {
      // parse date time to dd/mm/yyy, h:m:s
      const dateString = inputString.split(' ')[0]
      const timeString = inputString.split(' ')[1]

      const year_int = parseInt(dateString.split('-')[0])
      const month_int = parseInt(dateString.split('-')[1])
      const day_int = parseInt(dateString.split('-')[2])

      const hour_int = parseInt(timeString.split(':')[0])
      const minutes_int = parseInt(timeString.split(':')[1])

      const dateObject = new Date(year_int, month_int, day_int, hour_int, minutes_int)
      
      const year = dateObject.getFullYear();
      const day = String(dateObject.getDate()).padStart(2, '0');
      const month = String(dateObject.getMonth()).padStart(2, '0');
      const hours = String(dateObject.getHours()).padStart(2, '0');
      const minutes = String(dateObject.getMinutes()).padStart(2, '0');
      const seconds = String(dateObject.getSeconds()).padStart(2, '0');

      return `${day}/${month}/${year}, ${hours}:${minutes}:${seconds}`;
    },
    logVariable(variable) {
      console.log(variable);
    },
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    getEventColor(event) {
      return event.color;
    }
  }
};
