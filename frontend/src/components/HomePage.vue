<template>
	<div>
		<p v-if="deck_deleted">
			deck deleted
		</p>

		<ul>
			<div>
				<p v-if="complete">
					made a new deck {{this.new_deck_name}}
				</p>
			</div>

			<li>
				<div v-if="selected.id != -1">
					<router-link :to="`/deck/${this.selected.id}`">
						view {{this.selected.name}}'s cards
					</router-link>
					<br>
					<br>
					<router-link :to="`/deck/${this.selected.id}/type`">
						type test {{this.selected.name}}'s cards
					</router-link>
					<br>
					<br>
				</div>
				<div v-else>
					Select a deck
				</div>
			</li>

			<div v-if="error">
				error!
			</div>


			<div>
				you are viewing {{selected.name}}
				<select v-model="selected">
					<option disabled value="">please select a deck</option>
					<option v-for="deck in this.decks" :key="deck.id" :value="deck">
						{{deck.name}}
					</option>
				</select>
			</div>

			<div>
				<p>make a new deck called {{new_deck_name}}</p>
				<input v-model="new_deck_name">
				<button @click="new_deck(new_deck_name)">submit</button>
			</div>

		</ul>
	</div>
</template>

<script>
	import axios from 'axios';
	export default {
		data() {
			return {
				error: false,
				decks: [],
				selected: {
					id: -1,
					name: 'no deck'
				},
				new_deck_name: '',
				complete: false,
				deck_deleted: false

			}
		},
		created() {
			if (this.$route.query.deck_deleted) {
				this.deck_deleted = true
				setTimeout(() => {this.deck_deleted = false}, 3000);

				this.$router.replace({
					path: '/'
				})
			}
		},

		methods: {
			async get_decks() {
				try {
					const res = await axios.get('http://localhost:5000/decks')
					this.decks = res.data.decks
				} catch (e) {
					this.error = true
				} finally {
					this.error = false
				}

			},

			async new_deck(new_deck_name) {
				try {
					await axios.post('http://localhost:5000/deck', {
						name: new_deck_name
					})

				} catch (e) {
					this.error = true
				} finally {
					this.complete = true
					this.get_decks()
					setTimeout(() => {this.complete = false; this.new_deck_name = ''}, 3000);
				}
				
			}
		},

		mounted() {
			this.get_decks()

		},
		name: 'HomePage'
	}
</script>
