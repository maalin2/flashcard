import { createRouter, createWebHistory } from 'vue-router'

import HomePage from './components/HomePage.vue'
import DeckPage from './pages/DeckPage.vue'
import TypePage from './pages/TypePage.vue'

const routes = [
	{ path: '/', component: HomePage },
	{ path: '/deck/:id', component: DeckPage, props: true },
	{ path: '/deck/:id/type', component: TypePage, props: true},
];


const router = createRouter({
	history: createWebHistory(),
	routes
});

export default router;
