import axios from "axios";

export default {
  namespaced: true,
  state: {
    appointmentDataArr: [], // array contains appointments data
  },

  getters: {
    setAppointments: (state) => (data) => {
      if (state.appointmentDataArr.length > 0) {
        state.appointmentDataArr = [];
      } 
      data.forEach((item) => {
        state.appointmentDataArr.push(item);
      });
    },
    getAppointments: (state) => {
      return state.appointmentDataArr;
    },
  },

  mutations: {
    getAxiosCall(state, payload) {
      /*
                http get request
                params:
                    payload: [object]: [data sended with the request]
            */
      axios
        .get(`${payload.host}/api/${payload.url}/`, {
          params: payload.params,
          // headers: {
          //     "X-CSRFToken": payload.csrftoken,
          //     Authorization: `token ${payload.auth}`,
          // },
        })
        .then((response) => {
          let res = response.data;
          payload.callback(res);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    postAxiosCall(state, payload) {
      /*
           http post request
           params:
               payload: [object]: [data sended with the request]
       */
      axios
        .post(`${payload.host}/api/${payload.url}/`, {
          body: payload.params,
          // headers: {
          //     "X-CSRFToken": payload.csrftoken,
          //     Authorization: `token ${payload.auth}`,
          // },
        })
        .then((response) => {
          let res = response.data;
          payload.callback(res);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  actions: {
    // allWorks({ commit, rootState }, payload) {
    //   commit("getAxiosCall", {
    //     url: payload.url,
    //     params: payload.params,
    //     callback: payload.callback,
    //     host: rootState.HOST,
    //   });
    // },
  },
};