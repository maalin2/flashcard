<template>
	<div>
		<i><li><router-link to="/">home</router-link></li></i>
		<p>list of decks</p>
		
		<div v-if="loading">loading</div>
		<div v-if="error" class="error">error viewing decks</div>

		<ul v-if="decks.length">
			<li v-for="deck in decks" :key="deck.id">
				<router-link :to="'/deck' + deck.id">{{deck.name}}</router-link>

			</li>
		</ul>

		<div v-else>no decks</div>
	</div>
</template>

<script>
	import axios from 'axios';

	export default {
		data() {
			return {
				decks: [],
				loading: true,
				error: false,
			}
		},

		created() {
			this.fetchDecks();
		},
		
		methods: {
			async fetchDecks() {
				try {
					const response = await axios.get('http://127.0.0.1:5000/decks');
					this.decks = response.data.decks;
				} catch (e) {
					this.error = true;
				} finally {
					this.loading = false;
				}
				
			},
		}, 
		


		name: 'DeckPage',
	}
</script>
