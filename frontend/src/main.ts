import store from '@/store';
import '@babel/polyfill';
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format';
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse';
import VeeValidate from 'vee-validate';
import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import App from './App.vue';
// Import Component hooks before component definitions
import './component-hooks';
import './registerServiceWorker';
import router from './router';

Vue.config.productionTip = false;

Vue.use(VeeValidate);
Vue.use(Vuetify, {
  iconfont: 'md',
});
Vue.use(VueFilterDateParse);
Vue.use(VueFilterDateFormat);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
