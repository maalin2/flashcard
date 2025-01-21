<template>
	<div>
		<i><li><router-link to="/">home</router-link></li></i>

		<div>
			<button @click="del_deck()">
				delete deck
			</button>
		</div>
		
		<p>list of cards</p>
		
		<div v-if="loading">loading</div>
		<div v-if="error" class="error">error viewing decks</div>

		<div v-if="cards.length === 0">
			no cards. maybe make a new card?
		</div>

		<ul>
			<div v-for="card in cards" :key="card.id">
				<li>
					<p>
						<i>{{card.question}}</i>
						<br>
						<b>{{card.answer}}</b>
					</p>
				</li>
			</div>
		</ul>

		<div>
			make a new card?
			<input v-model="card_question" placeholder="question">
			<input v-model="card_answer" placeholder="answer">
			<button @click="new_card(card_question, card_answer)">create</button>
		</div>

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
				card_question: '',
				card_answer: '',
				id: this.$route.params.id,
				base_url: 'http://127.0.0.1:5000'
			}
		},

		created() {
			this.fetchCards();
		},
		
		methods: {
			async del_deck(){
				const url = `${this.base_url}/deck/${this.id}`
				console.log(url)
				axios.delete(url)
					.then(() => {
						this.$router.replace({
							path: '/',
							query: {deck_deleted: true}
						})
					}).catch((e) => {
						console.error('failed to delete deck', e)
					}
				)
			}, 
			async fetchCards() {
				try {
					const url = `${this.base_url}/deck/${this.id}/cards`
					const response = await axios.get(url)
					this.cards = response.data.cards
					console.log(this.cards)
				} catch (e) {
					this.error = true;
				} finally {
					this.loading = false;
				}
			},

			async new_card(card_question, card_answer){
				try {
					const url = `${this.base.url}/deck/${this.id}/card`
					await axios.post(url, {
						question: card_question,
						answer: card_answer
					})
				} catch (e) {
					this.error = true
				} finally {
					this.fetchCards()
				}
			}
		}, 
		


		name: 'DeckPage',
	}
</script>
