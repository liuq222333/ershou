<template>
	<div class="admin-navbar-brand" @click="goHome">
		<span class="admin-navbar-brand__mark"></span>
	</div>
</template>

<script>
	export default {
		methods: {
			goHome() {
				this.$router.push('/')
			}
		}
	}
</script>

<style lang="scss" scoped>
	.admin-navbar-brand {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 44px;
		height: 44px;
		cursor: pointer;
		user-select: none;
	}

	.admin-navbar-brand__mark {
		display: inline-flex;
		width: 26px;
		height: 26px;
		border-radius: 9px 14px 9px 14px;
		background: linear-gradient(180deg, #42bf84 0%, #1f8f63 100%);
		transform: rotate(-18deg);
		box-shadow: 0 10px 20px rgba(31, 143, 99, 0.2);
	}
</style>
