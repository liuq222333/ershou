<template>
	<div id="app" class="front-app-root">
		<router-view></router-view>
	</div>
</template>

<script>
	export default {
		name: 'App'
	}
</script>

<style>
	* {
		box-sizing: border-box;
	}

	html,
	body,
	#app {
		width: 100%;
		min-height: 100%;
		margin: 0;
		padding: 0;
	}

	[v-cloak] {
		display: none;
	}
</style>
