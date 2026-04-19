<template>
	<div class="admin-shell">
		<div class="admin-shell__topbar">
			<div class="admin-shell__brand">
				<index-header></index-header>
			</div>
			<div class="admin-shell__nav">
				<index-aside></index-aside>
			</div>
			<div class="admin-shell__user">
				<index-user-menu></index-user-menu>
			</div>
		</div>

		<el-main class="admin-shell__main">
			<div class="admin-shell__main-inner">
				<tags-view />
				<router-view class="router-view"></router-view>
			</div>
		</el-main>
	</div>
</template>

<script>
	import IndexAside from '@/components/index/IndexAsideStatic'
	import IndexHeader from '@/components/index/IndexHeader'
	import IndexUserMenu from '@/components/index/IndexUserMenu'
	import TagsView from '@/components/index/TagsView'

	export default {
		components: {
			IndexAside,
			IndexHeader,
			IndexUserMenu,
			TagsView
		},
		data() {
			return {
				title: ''
			}
		}
	}
</script>

<style lang="scss" scoped>
	.admin-shell {
		min-height: 100vh;
		padding: 16px 0 0;
	}

	.admin-shell__topbar {
		position: sticky;
		top: 14px;
		z-index: 100;
		display: flex;
		align-items: center;
		gap: 18px;
		width: min(calc(100% - 56px), var(--admin-page-wide));
		min-height: var(--admin-nav-height);
		margin: 0 auto;
		padding: 12px 18px;
		border: 1px solid rgba(255, 255, 255, 0.42);
		border-radius: 22px;
		background: rgba(247, 250, 247, 0.1);
		backdrop-filter: blur(30px) saturate(152%);
		box-shadow: 0 14px 32px rgba(21, 33, 24, 0.05);
	}

	.admin-shell__brand,
	.admin-shell__user {
		display: flex;
		align-items: center;
		flex: 0 0 auto;
	}

	.admin-shell__nav {
		flex: 1 1 auto;
		min-width: 0;
		overflow: hidden;
	}

	.admin-shell__main {
		padding: 20px 0 56px;
	}

	.admin-shell__main-inner {
		width: 100%;
	}

	.router-view {
		min-height: calc(100vh - 170px);
	}

	@media (max-width: 1400px) {
		.admin-shell__topbar {
			width: min(calc(100% - 40px), var(--admin-page-wide));
			padding: 10px 16px;
		}
	}
</style>
