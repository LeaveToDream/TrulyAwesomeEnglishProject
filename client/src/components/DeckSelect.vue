<template>
	<div id="back" v-on:click="clicked=true" v-bind:class="{clicked:clicked}">
		<div class="container text-center" style="margin-top:40px;">
			<h1>Hi !</h1>
			<hr class="colorgraph">
			<h2>Welcome to Lime Time Ⓒ, a game where you have to restore the time line of history</h2>
			<h3
				v-bind:class="{active:notclicked}"
				class="activable">
					<em>*click*</em>
			</h3>
			<div
				v-bind:class="{active:clicked}"
				class="activable"
				>
				<ul class="select-deck">
					<li
						v-for="(deck,i) in decks"
						v-bind:key="i">
							<span class="clickable"
							v-on:click="changePage(deck.id)"
							>
								{{deck.name}}
							</span>
						<span class="card-number">{{deck.cards.length}} cards</span>
					</li>
				</ul>
			</div>

		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'HelloWorld',
	data () {
		return {
			clicked: false,
			decks: [],
			msg: 'Welcome to Your Vue.js App'
		};
	},
	created () {
		axios.get(`http://omachi.moe:9876/api/decks/`)
			.then(response => {
				this.decks = response.data;
			}).catch(e => {
				console.error(e);
				// this.errors.push(e);
			});
	},
	methods: {
		changePage (deckId) {
			if (this.clicked) {
				this.$router.push({ path: `/board?deck=${deckId}` });
				setInterval(() => { this.clicked = false; }, 2000);
			}
		}
	},
	computed: {
		notclicked: function () {
			return !this.clicked;
		}
	}

};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
* {
	transition: 0.5s;
}

#back {
	position: absolute;
	top: 0;
	left: 0;
	height: 100vh;
	width : 100vw;
	color: #292C33;
	background-color: white ;
	transition: 0.5s;
}

#back.clicked {
	color: white;
	background-color: #292C33;
}

.clickable {
  cursor: pointer;
}

.activable {
	opacity: 0;
	transition: opacity .2s linear;
}

.activable.active {
	opacity: 1;
}

.select-deck{
	list-style-type: none;
	margin-top: 50px;
	font-size: 2em;
	font-style: italic;
}
.select-deck li{
	margin-top: 10px;
}

.card-number {
	font-size : initial;
	color : grey;
	font-style: normal;
}

.colorgraph {
	height: 7px;
	border-top: 0;
	background: #c4e17f;
	border-radius: 5px;
	background-image: -webkit-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
	background-image: -moz-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
	background-image: -o-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
	background-image: linear-gradient(to right, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
}
</style>
