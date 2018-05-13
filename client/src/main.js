// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import App from './App';
import router from './control/routes';
import swal from 'sweetalert';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.component('tl-board-card', {
	props: [
		'id',
		'name',
		'desc',
		'date',
		'image',
		'inserting'
	],
	template: `
    <div>
      <button v-b-tooltip="desc">
        <b-card overlay
                v-bind:title="name"
                img-src="https://via.placeholder.com/200x200"
                v-bind:img-alt="name"
                img-top
                tag="card"
                style="max-width: 20rem;">
          <p class="card-date">
            {{ date }}
          </p>
        </b-card>
      </button>
      <span class="insertingCardArrow" @click="$emit('try-card-at',id)">
        <span v-show="inserting" class="clickable">
          <i class="fal fa-2x fa-long-arrow-alt-down"></i>
        </span>
      </span>
    </div>`
});

Vue.component('tl-hand-card', {
	props: [
		'id',
		'name',
		'desc',
		'date',
		'image'
	],
	template: `
    <div>
      <button v-b-tooltip="desc" @click="$emit('change-selected-card',id)">
        <b-card overlay
                v-bind:title="name"
                img-src="https://via.placeholder.com/200x200"
                v-bind:img-alt="name"
                img-top
                tag="card"
                style="max-width: 20rem;">
        </b-card>
      </button>
    </div>`
});

/* eslint-disable no-new */
new Vue({
	el: '#app',
	router,
	components: {App},
	template: '<App/>'
});
Vue.config.devtools = true;
