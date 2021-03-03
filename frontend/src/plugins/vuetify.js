import Vue from "vue";
import Vuetify from "vuetify/lib";

import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#895537", // #E53935
        secondary: colors.orange.base, // #FFCDD2
        accent: colors.orange.base // #3F51B5
      }
    }
  }
});
