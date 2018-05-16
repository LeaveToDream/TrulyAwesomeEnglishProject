<template>
<div id="app" class="container-flex">
  <div class="loading" v-bind:class="{loaded:loaded}">
    <div class="img-looping">
      <i class="fal fa-cog fa-8x fa-spin"></i>
    </div>
  </div>
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
          v-bind:image="getImage(card.type_id)"
          v-bind:date="card.year"
          v-bind:type="getType(card.type_id)"
          v-bind:inserting="inserting"
          v-on:try-card-at="tryCardAt">
    </tl-board-card>

    <tl-board-card v-show="!activeBoard"
          v-for="(card, i) in discarded"
          v-bind:key="i"
          v-bind:id="i"
          v-bind:name="card.name"
          v-bind:desc="card.desc"
          v-bind:image="getImage(card.type_id)"
          v-bind:date="card.year"
          v-bind:type="getType(card.type_id)"
          v-bind:inserting="false">
    </tl-board-card>
  </div>
  <div id="hand" class="row" v-bind:class="{insertingCardHandOverlay:inserting}">
    <div class="inner-hand">
      <tl-hand-card
            v-for="(card, i) in hand"
            v-bind:key="i"
            v-bind:id="i"
            v-bind:name="card.name"
            v-bind:desc="card.desc"
            v-bind:image="getImage(card.type_id)"
            v-bind:type="getType(card.type_id)"
            v-bind:selected="card.selected"
            v-on:change-selected-card="selectCard">
      </tl-hand-card>
      <div class="row" v-if="hand.length==0">
        <div class="hand-home clickable" @click="$router.push('/')">
          <i class="fal fa-home fa-4x"></i>
        </div>
        <div class="hand-home clickable" @click="$router.go($router.currentRoute)">
          <i class="fal fa-undo fa-4x fa-flip-vertical"></i>
        </div>
      </div>
    </div>
    <div class="handBackCard activable"
         @click="unselectCard"
         v-bind:class="{active:inserting}">
      <span class="goBackToHand">
        <i class="fal fa-4x fa-times"></i>
      </span>
    </div>
  </div>
  <div class="cemeteryToggle clickable" @click="toggleCemetery" v-b-tooltip="'Intervertir plateau/défausse'">
    <img v-if="activeBoard" src="https://png.icons8.com/ios/100/000000/cemetery.png">
    <img v-else src="https://png.icons8.com/wired/100/000000/timetable.png">
  </div>
  <div class="home clickable" @click="$router.push('/')">
    <i class="fal fa-home fa-4x"></i>
  </div>
</div>

</template>

<script>
// import ApiLoader from '@/control/apiLoader';
import swal from 'sweetalert';
import axios from 'axios';

export default {
	name: 'Board',
	data () {
		return {
			pseudo: 'John',
			deck: { },
			cards: [ ],
			drawable: [ ],
			hand: [ ],
			board: [ ],
			discarded: [ ],
			loaded: false,
			activeBoard: true,
			selected: undefined
		};
	},
	methods: {
		selectCard (i) {
			if (this.selected) {
				this.unselectCard();
			}
			this.selected = this.hand[i];
			this.selected.i = i;
			this.hand[i].selected = true;
		},
		unselectCard () {
			if (this.hand[this.selected.i]) {
				this.hand[this.selected.i].selected = false;
			}
			this.selected = undefined;
			console.log(this.selected);
		},
		toggleCemetery () {
			this.activeBoard = !this.activeBoard;
		},
		getImage (typeId) {
			let images = [
				'https://cdn.discordapp.com/attachments/414476081274290188/446381870104444930/sword_bw.jpg',
				'https://cdn.discordapp.com/attachments/414476081274290188/446381866044489738/globe_bw.jpg',
				'https://cdn.discordapp.com/attachments/414476081274290188/446381864987394058/crown_bw.jpg'
			];
			return (typeId !== undefined) ? images[typeId] : 'https://via.placeholder.com/200x200';
		},
		getType (typeId) {
			let types = ['battle', 'society', 'royalty'];
			return (typeId !== undefined) ? types[typeId] : types[Math.floor(Math.random() * (3))];
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
				let card = this.drawable.pop();
				card.selected = false;
				this.hand.push(card);
				return true;
			}
		},
		discard (goesToCemetery = false) {
			if (this.selected) {
				const discardedCard = this.hand.splice(this.selected.i, 1)[0];
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
		asyncLoad (url) {
			let script = document.createElement('script');
			script.async = true;
			script.src = url;
			document.head.appendChild(script);
		}
	},
	created () {
		// Load FA5, because thoses guys are awesome
		this.asyncLoad('https://pro.fontawesome.com/releases/v5.0.8/js/all.js');

		// retrieve cards from db
		this.deck.id = (this.$route.query.deck) ? this.$route.query.deck : '5af9967af435bb627c612375';
		// this.deck.id = '5af5e5f4f435bb5d8d2bbdaf'; // Histoire de l'angleterre
		// other.deck.id = "5af8aad2f435bb5d8d2bbe02" ;
		// ApiLoader.get(`deck/${this.deck.id}?shuffle&cards_content`)
		axios.get(`http://omachi.moe:9876/api/deck/${this.deck.id}?shuffle&cards_content`)
			.then(response => {
				this.deck.name = response.data.name;
				this.cards = response.data.cards;

				// fill the draw deck
				this.drawable = this.cards;

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

				this.loaded = true;
			})
			.catch(e => {
				console.error(e);
				// this.errors.push(e);
			});
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
button:focus {
  outline: 0;
}

* {
  transition: 0.5s;
}

body {
  background-color: #292C33;
}

.activable {
  opacity: 0;
  transition: opacity .2s linear;
}

.activable.active {
  opacity: 1;
}

.clickable {
  cursor: pointer;
}

#board, #hand {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100vh;
  width: 100%;
  overflow: auto;
}
#board > *, #hand > * {
  margin: 25px;
}
#board button, #hand button {
  border: 0;
  padding: 0;
  border-radius: 12px;
  background-color: #abb2c2;
}

@keyframes rainbow {
  0%{background-image: linear-gradient( 0deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  1%{background-image: linear-gradient( 3deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  2%{background-image: linear-gradient( 7deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  3%{background-image: linear-gradient( 10deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  4%{background-image: linear-gradient( 14deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  5%{background-image: linear-gradient( 18deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  6%{background-image: linear-gradient( 21deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  7%{background-image: linear-gradient( 25deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  8%{background-image: linear-gradient( 28deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  9%{background-image: linear-gradient( 32deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  10%{background-image: linear-gradient( 36deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  11%{background-image: linear-gradient( 39deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  12%{background-image: linear-gradient( 43deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  13%{background-image: linear-gradient( 46deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  14%{background-image: linear-gradient( 50deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  15%{background-image: linear-gradient( 54deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  16%{background-image: linear-gradient( 57deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  17%{background-image: linear-gradient( 61deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  18%{background-image: linear-gradient( 64deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  19%{background-image: linear-gradient( 68deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  20%{background-image: linear-gradient( 72deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  21%{background-image: linear-gradient( 75deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  22%{background-image: linear-gradient( 79deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  23%{background-image: linear-gradient( 82deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  24%{background-image: linear-gradient( 86deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  25%{background-image: linear-gradient( 90deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  26%{background-image: linear-gradient( 93deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  27%{background-image: linear-gradient( 97deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  28%{background-image: linear-gradient( 100deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  29%{background-image: linear-gradient( 104deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  30%{background-image: linear-gradient( 108deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  31%{background-image: linear-gradient( 111deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  32%{background-image: linear-gradient( 115deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  33%{background-image: linear-gradient( 118deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  34%{background-image: linear-gradient( 122deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  35%{background-image: linear-gradient( 126deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  36%{background-image: linear-gradient( 129deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  37%{background-image: linear-gradient( 133deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  38%{background-image: linear-gradient( 136deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  39%{background-image: linear-gradient( 140deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  40%{background-image: linear-gradient( 144deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  41%{background-image: linear-gradient( 147deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  42%{background-image: linear-gradient( 151deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  43%{background-image: linear-gradient( 154deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  44%{background-image: linear-gradient( 158deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  45%{background-image: linear-gradient( 162deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  46%{background-image: linear-gradient( 165deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  47%{background-image: linear-gradient( 169deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  48%{background-image: linear-gradient( 172deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  49%{background-image: linear-gradient( 176deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  50%{background-image: linear-gradient( 180deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  51%{background-image: linear-gradient( 183deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  52%{background-image: linear-gradient( 187deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  53%{background-image: linear-gradient( 190deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  54%{background-image: linear-gradient( 194deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  55%{background-image: linear-gradient( 198deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  56%{background-image: linear-gradient( 201deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  57%{background-image: linear-gradient( 205deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  58%{background-image: linear-gradient( 208deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  59%{background-image: linear-gradient( 212deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  60%{background-image: linear-gradient( 216deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  61%{background-image: linear-gradient( 219deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  62%{background-image: linear-gradient( 223deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  63%{background-image: linear-gradient( 226deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  64%{background-image: linear-gradient( 230deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  65%{background-image: linear-gradient( 234deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  66%{background-image: linear-gradient( 237deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  67%{background-image: linear-gradient( 241deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  68%{background-image: linear-gradient( 244deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  69%{background-image: linear-gradient( 248deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  70%{background-image: linear-gradient( 252deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  71%{background-image: linear-gradient( 255deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  72%{background-image: linear-gradient( 259deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  73%{background-image: linear-gradient( 262deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  74%{background-image: linear-gradient( 266deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  75%{background-image: linear-gradient( 270deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  76%{background-image: linear-gradient( 273deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  77%{background-image: linear-gradient( 277deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  78%{background-image: linear-gradient( 280deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  79%{background-image: linear-gradient( 284deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  80%{background-image: linear-gradient( 288deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  81%{background-image: linear-gradient( 291deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  82%{background-image: linear-gradient( 295deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  83%{background-image: linear-gradient( 298deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  84%{background-image: linear-gradient( 302deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  85%{background-image: linear-gradient( 306deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  86%{background-image: linear-gradient( 309deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  87%{background-image: linear-gradient( 313deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  88%{background-image: linear-gradient( 316deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  89%{background-image: linear-gradient( 320deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  90%{background-image: linear-gradient( 324deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  91%{background-image: linear-gradient( 327deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  92%{background-image: linear-gradient( 331deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  93%{background-image: linear-gradient( 334deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  94%{background-image: linear-gradient( 338deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  95%{background-image: linear-gradient( 342deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  96%{background-image: linear-gradient( 345deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  97%{background-image: linear-gradient( 349deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  98%{background-image: linear-gradient( 352deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  99%{background-image: linear-gradient( 356deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
  100%{background-image: linear-gradient( 360deg, #FF3CAC 0%, #562B7C 52%, #2B86C5 100%);}
}

#board button .card, #hand button .card {
  border: 12px solid white;
  border-radius: 12px;
  border-color: rgba(0, 0, 0, 0);
  background-color: rgba(0, 0, 0, 0);
}
#board button .card .card-img-top, #hand button .card .card-img-top {
  border-radius: 6px;
  width: 176px;
  height: 176px;
}

#board button.active, #hand button.active {
  background-image: linear-gradient(to bottom right, #ff3cac, #562b7c, #2b86c5);
	animation: rainbow 5s ease infinite;
}
/*
███████╗██╗      █████╗ ███████╗██╗  ██╗██╗   ██╗    ██████╗  ██████╗ ██████╗ ██████╗ ███████╗██████╗
██╔════╝██║     ██╔══██╗██╔════╝██║  ██║╚██╗ ██╔╝    ██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
█████╗  ██║     ███████║███████╗███████║ ╚████╔╝     ██████╔╝██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝
██╔══╝  ██║     ██╔══██║╚════██║██╔══██║  ╚██╔╝      ██╔══██╗██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗
██║     ███████╗██║  ██║███████║██║  ██║   ██║       ██████╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

#board button.society, #hand button.society {
  background-image: linear-gradient(to top left, #f9f047, #0fd850);
}
#board button.battle, #hand button.battle {
  background-image: linear-gradient(to bottom left, rgba(148, 9, 9, 0.8), #e81b14);
}
#board button.royalty, #hand button.royalty {
  background-image: linear-gradient(to top right, #005bea, #00c6fb);
}
/*
███████╗███╗   ██╗██████╗
██╔════╝████╗  ██║██╔══██╗
█████╗  ██╔██╗ ██║██║  ██║
██╔══╝  ██║╚██╗██║██║  ██║
███████╗██║ ╚████║██████╔╝
╚══════╝╚═╝  ╚═══╝╚═════╝
*/

#board {
  height: 70%;
}

#hand {
  height: 30%;
  top: 70%;
}
#hand .inner-hand {
  border: 4px dotted white;
  border-bottom: 0;
  display: inline-flex;
  margin: auto;
  margin-bottom: 0;
  padding: 15px;
  bottom: 0;
  overflow-y: hidden;
}
#hand button {
  margin: 0 1.5em;
}

.insertingCardArrow {
  display: block;
  height: 202px;
  width: 20px;
  float: right;
  padding: 100px 0px 100px 2.1em;
  color: white;
}

.firstCard {
  width: 0;
  height: 0;
  display: inline-block;
}

.handBackCard {
  position: absolute;
  right: 0;
	bottom: 0;
}

.goBackToHand {
  color: white;
}

.cemeteryToggle {
  position: absolute;
  bottom: 0;
  right: calc(100% - 14em);
  background-color: lightgray;
  border-radius: 50%;
  padding: 25px;
  margin: 25px;
}

.card-img-overlay {
    padding: 1rem 0.5rem ;
}
.card-date {
	position: absolute;
	bottom: 0;
	width: calc(100% - 0.5rem);
	margin-bottom: 5px;
	font-size: 1.3em;
}
.home {
  color: white;
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 100;
}
.hand-home, .hand-replay {
  color: white;
  font-size: 2em;
  padding : 35px;
}

.loading{
  transition:height .2s 1s, z-index .2s 1s, background 0.5s, opacity .5s;
  display: block;
  position: absolute;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  background-color: #292C33;
  z-index: 101;
}

.img-looping {
  text-align: center;
  position: relative;
  top: 47%;
  color: white;
}

.loading.loaded .img-looping {
  opacity: 0;
}

.loaded {
  z-index : 0;
  background-color: transparent;
  height: 0;
}
</style>
