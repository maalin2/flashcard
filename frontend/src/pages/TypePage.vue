<template>
	<div>
		<i><li><router-link to="/">home</router-link></li></i>

		<p>type</p>
		
		<div v-if="loading">loading</div>
		<div v-if="error" class="error">error viewing decks</div>

		<div v-if="cards.length === 0">
			no cards. maybe make a new card?
		</div>

		<ul>
			<div v-if="random_id">
				<i>{{this.cards[this.random_id].question}}</i>
			</div>
			<br>
			<div>
				<button @click="get_random_card_id()">
					random card
				</button>
			</div>
		</ul>
	</div>
</template>

<script>
	import axios from 'axios';

	export default {
		data() {
			return {
				cards: [],
				loading: true,
				error: false,
				random_id: null,
				user_answer: '',
				id: this.$route.params.id,
				base_url: 'http://127.0.0.1:5000'
			}
		},

		created() {
			this.fetchCards()
				.then(() => this.get_random_card_id())
		},
		
		methods: {
			async fetchCards() {
				try {
					const url = `${this.base_url}/deck/${this.id}/cards`
					const response = await axios.get(url)
					this.cards = response.data.cards
				} catch (e) {
					this.error = true;
				} finally {
					this.loading = false;
					this.get_random_card_id()
				}
			},

			get_random_card_id() {
				const N = this.cards.length
				const id =  Math.floor(Math.random() * N)
				this.random_id = id
			},
		}, 
		


		name: 'TypePage',
	}
</script>
