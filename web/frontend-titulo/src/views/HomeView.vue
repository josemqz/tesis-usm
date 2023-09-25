<template> 
	<main>
		<!-- Disminuir enfoque en el texto -->
		<!-- font-size puede definirse a partir de vw :O -->
		<h1>Ocupación de campus San Joaquín</h1>

		<p>Hacer clic en cada área para ver detalles.</p>

		<SvgCampus v-if="this.loaded" />
	</main>
</template>

<script>
// import TheWelcome from '../components/TheWelcome.vue'

// import { onMounted, computed } from "vue";
import SvgCampus from '../components/SvgCampus.vue';

import { useOccupancyStore } from "../stores/occupancy";

export default {
	components: {
		SvgCampus
	},
	data(){
		return {
			occupancyStore: useOccupancyStore(),
		}
	},
	computed: {
		loaded(){
			console.log("get store.loaded:", this.loaded)
			return this.occupancyStore.getLoaded;
		},
	},

	// cada 5 segundos ?
	mounted() {
		console.log("onMounted start")
		this.occupancyStore.fetchSalas();
		this.occupancyStore.fetchOcupaciones();
		this.occupancyStore.setTasasOcupacion();
		console.log("onMounted end")
	}
}
</script>

<style scoped>
main{
	text-align: center;
	display: flex;
	flex-direction:column;
	/* grid-template-rows: 1fr 1fr 4fr; */
	align-items: center;
	/* grid-auto-flow: row; */
}
@media (min-width: 1024px) {
	main{
		/* min-height: 80vh; */
		/* display: flex; */
		grid-gap: 1vh;
	}
}
</style>