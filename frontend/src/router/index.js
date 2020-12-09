import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/afspraak-maken",
    name: "Afspraak Maken",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakMaken.vue"),
    props: true
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakMaken.vue")
>>>>>>> 6d2b6ad... frontend merged
  },
  {
    path: "/afspraak-bevestigen",
    name: "AfspraakBevestigen",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakBevestigen.vue"),
    props: true
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakBevestigen.vue")
>>>>>>> 6d2b6ad... frontend merged
  },
  {
    path: "/afspraak-geboekt",
    name: "AfspraakGeboekt",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
<<<<<<< HEAD
      import(/* webpackChunkName: "about" */ "../views/AfspraakGeboekt.vue"),
    props: true
=======
      import(/* webpackChunkName: "about" */ "../views/AfspraakGeboekt.vue")
>>>>>>> 6d2b6ad... frontend merged
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
