import '@babel/polyfill';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vuetify';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse';
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format';

Vue.config.productionTip = false;

Vue.use(VueFilterDateParse);
Vue.use(VueFilterDateFormat);

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
