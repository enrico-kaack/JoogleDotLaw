// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ListItem from './components/ListItem'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'
import VueScrollTo from 'vue-scrollto'
import Vuetify from 'vuetify'

axios.defaults.baseURL = 'http://localhost:5000'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead)
Vue.component('ListItem', ListItem)

Vue.use(VueScrollTo)

Vue.use(Vuetify)
import 'vuetify/dist/vuetify.min.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
