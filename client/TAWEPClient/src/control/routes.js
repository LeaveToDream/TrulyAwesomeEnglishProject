import Vue from 'vue';
import Router from 'vue-router';

import Board from '@/components/Board';
import HelloWorld from '@/components/HelloWorld';

Vue.use(Router);

export default new Router({
	routes: [
		{
			path: '/hello-world',
			name: 'HelloWorld',
			component: HelloWorld
		},
		{
			path: '/board',
			name: 'Board',
			component: Board
		}
	]
});
