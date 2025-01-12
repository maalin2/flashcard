<template>
	<div>
		<ul>
			<li><router-link to="/deck">deck</router-link></li>
			<div v-if="error">
				error!
			</div>
			<div>
				you are viewing {{selected}}
				<select v-model="selected">
					<option disabled value="">please select a deck</option>
					<option v-for="deck in this.decks" :key="deck.id">
						<option>{{deck.name}}</option>
					</option>
				</select>
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
				selected: 'no deck'
			}
		},

		methods: {
			async get_decks() {
				try {
					const res = await axios.get('http://localhost:5000/decks')
					this.decks = res.data.decks
				} catch (e) {
					this.error = true
				}
			}
		},

		mounted() {
			this.get_decks()

		},
		name: 'HomePage',
	}
</script>
