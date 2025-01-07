import { createRouter, createWebHistory } from 'vue-router'

import HomePage from './components/HomePage.vue'
import DeckPage from './pages/DeckPage.vue'

const routes = [
	{ path: '/', component: HomePage },
	{ path: '/deck', component: DeckPage },
];


const router = createRouter({
	history: createWebHistory(),
	routes
});

export default router;
