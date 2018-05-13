<template>
	<div id="app" class="container-flex">
	<div id="board" class="row" v-bind:class="{cemeteryBoard:!activeBoard}">
		<div v-show="activeBoard">
			<div class="firstCard"></div>
			<span class="insertingCardArrow">
				<span v-show="inserting" class="clickable" @click="tryCardAt(-1)">
					<i class="fal fa-2x fa-long-arrow-alt-down"></i>
				</span>
			</span>
		</div>
		<tl-board-card v-show="activeBoard"
					v-for="(card, i) in board"
					v-bind:key="i"
					v-bind:id="i"
					v-bind:name="card.name"
					v-bind:desc="card.desc"
					v-bind:image="getCardImage(card.img)"
					v-bind:date="card.year"
					v-bind:inserting="inserting"
					v-on:try-card-at="tryCardAt">
		</tl-board-card>

		<tl-board-card v-show="!activeBoard"
					v-for="(card, i) in discarded"
					v-bind:key="i"
					v-bind:id="i"
					v-bind:name="card.name"
					v-bind:desc="card.desc"
					v-bind:image="getCardImage(card.img)"
					v-bind:date="card.year"
					v-bind:inserting="false">
		</tl-board-card>
		<div class="cemeteryToggle clickable" @click="toggleCemetery" v-b-tooltip="'Intervertir plateau/défausse'">
			<img v-if="activeBoard" src="https://png.icons8.com/ios/100/000000/cemetery.png">
			<img v-else src="https://png.icons8.com/wired/100/000000/timetable.png">
		</div>
	</div>
	<div id="hand" class="row" v-bind:class="{insertingCardHandOverlay:inserting}">
		<tl-hand-card v-if="!inserting"
					v-for="(card, i) in hand"
					v-bind:key="i"
					v-bind:id="i"
					v-bind:name="card.name"
					v-bind:desc="card.desc"
					v-bind:image="getCardImage(card.img)"
					v-on:change-selected-card="selectCard">
		</tl-hand-card>

		<tl-hand-card v-if="inserting"
				v-bind:id="0"
				v-bind:name="selected.name"
				v-bind:desc="selected.desc"
        v-bind:image="getCardImage(selected.img)">
		</tl-hand-card>
		<div class="firstCard" @click="unselectCard" v-if="inserting">
			<span class="goBackToHand">
				<i class="fal fa-4x fa-undo"></i>
			</span>
		</div>
	</div>
</div>

</template>

<script>
import ApiLoader from '@/control/apiLoader';

/* global swal */
export default {
	name: 'Board',
	data () {
		return {
			pseudo: 'Bob',
			deck: { },
			cards: [ ],
			drawable: [ ],
			hand: [ ],
			board: [ ],
			discarded: [ ],
			activeBoard: true,
			selected: undefined
		};
	},
	methods: {
		selectCard (i) {
			this.selected = this.hand[i];
		},
		unselectCard () {
			this.selected = undefined;
		},
		toggleCemetery () {
			this.activeBoard = !this.activeBoard;
		},
		getCardImage (image) {
			return (image !== undefined) ? image : 'https://via.placeholder.com/200x200';
		},
		addCardInOrederedDeck (deck, card) {
			if (deck.length === 0 || deck[deck.length - 1].year >= card.year) {
				deck.push(card);
			} else {
				// We checked that it's not the last card
				let i = 0;
				for (i; i < deck.length && card.year <= deck[i].year; i++);
				deck.splice(i, 0, card);
			}
		},
		draw () { // :boolean
			if (this.drawable.length <= 0) {
				swal({
					title: 'Sorry',
					text: 'Sadly, there is no more card in the draw deck ><.\n You can try again.',
					icon: 'error'
				});
				return false;
			} else {
				this.hand.push(this.drawable.pop());
				return true;
			}
		},
		discard (goesToCemetery = false) {
			const index = this.hand.indexOf(this.selected);
			if (index > -1) {
				const discardedCard = this.hand.splice(index, 1)[0];
				if (goesToCemetery) {
					console.log(discardedCard);
					this.addCardInOrederedDeck(this.discarded, discardedCard);
				}
			};
		},
		verifyDate (position) {
			if (position === -1) {
				return this.selected.year >= this.board[0].year;
			} else if (position === this.board.length - 1) {
				return this.board[position].year >= this.selected.year;
			} else {
				return this.board[position].year >= this.selected.year && this.selected.year >= this.board[position + 1].year;
			}
		},
		tryCardAt (position) {
			// The player choosed to put $selected between $position and $position+1
			// If this is the right date, we must thus insert
			// console.log(`${this.cards[position].date}, ${this.selected.date}, ${this.cards[position+1].date}`)
			if (this.verifyDate(position)) {
				this.board.splice(position + 1, 0, this.selected);
				this.discard();
				swal({
					title: 'Good job!',
					text: 'You found the right place in time',
					icon: 'success'
				}).then(() => {
					if (this.hand.length === 0) {
						swal({
							title: 'Good job!',
							text: 'You won the game !',
							icon: 'success'
						}).then(() => {
							// TODO ask for leaving the room, or stay ^^
						});
					}
				});
			} else {
				var vueObject = this;
				swal({
					title: 'Too bad!',
					text: `You did not found the right place in time. The event '${vueObject.selected.name}' took place in ${vueObject.selected.year}`,
					icon: 'info'
				});
				if (this.draw()) {
					this.discard(true);
				}
			}
			this.unselectCard();
		},
		asyncLoad(url){
			let script = document.createElement('script');
			script.async = true;
			script.src = url;
			document.head.appendChild(script);
		}
	},
	created () {

		this.asyncLoad('https://pro.fontawesome.com/releases/v5.0.8/js/all.js');


		// retrieve cards from db

		this.deck.id = "5af5e5f4f435bb5d8d2bbdaf" ; // Histoire de l'angleterre

		ApiLoader.get(`deck/${this.deck.id}`)
			.then(response => {
				this.messages = response.data;
			})
			.catch(e => {
				this.errors.push(e);
			});
		// this.cards = api.getCards()

		// fill the draw deck
		this.drawable = this.cards;

		/**
		 * Randomize array element order in-place.
		 * Using Durstenfeld shuffle algorithm.
		 */
		function shuffleArray (array) {
			for (var i = array.length - 1; i > 0; i--) {
				var j = Math.floor(Math.random() * (i + 1));
				var temp = array[i];
				array[i] = array[j];
				array[j] = temp;
			}
		}

		//shuffleArray(this.drawable);

		if (this.drawable.length < 3) {
			swal({ icon: 'error',
				title: 'Sorry',
				text: 'Sadly, there is not enought card in the draw deck for a game ><.\n Try a different deck if this is not yours, or complete it if this is.'
			});
			return;
		}

		// place 3 cards on the board (fuck it if there is less than 3 cards in the deck, it explodes)
		for (let i = 0; i < 3; i++) {
			this.addCardInOrederedDeck(this.board, this.drawable.pop());
		}

		// make every player draw 4 cards
		if (this.drawable.length < 4) {
			swal({ icon: 'error',
				title: 'Sorry',
				text: 'Sadly, there is not enought card in the draw deck for a game.\n Try a different deck if this is not yours, or complete it if this is.'
			});
			return;
		}
		for (let i = 0; i < 4; i++) {
			this.draw();
		}
	},
	computed: {
		inserting: function () {
			return this.selected !== undefined;
		}
	}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#board, #hand {
	position: absolute;
	top: 0;
	height: 100vh;
	overflow: auto;
}
#board > *, #hand > * {
	margin: 25px;
}
#board button, #hand button {
	border: 0;
	padding: 0;
	border-radius: 15px;
}

#board {
	width: 70%;
	left: 0;
}

#hand {
	width: 30%;
	left: 70%;
}

.clickable {
	cursor: pointer;
}

.insertingCardArrow {
	display: block;
	height: 202px;
	width: 20px;
	float: right;
	padding: 100px 0px 100px 2.1em;
}

.firstCard {
	border-radius: 15px;
	border: 4px dotted grey;
	width: 202px;
	height: 202px;
	display: inline-block;
}

.goBackToHand {
	display: inline-block;
	margin: auto;
	text-align: center;
	width: 100%;
	line-height: 220px;
}

.card-img-top {
	width: 200px;
	height: 200px;
}

.cemeteryToggle {
	position: absolute;
	bottom: 0;
	left: 70%;
	background-color: lightgray;
	border-radius: 50%;
	padding: 25px;
}

</style>
