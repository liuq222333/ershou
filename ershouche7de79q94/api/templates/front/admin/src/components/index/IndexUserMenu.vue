<template>
	<el-dropdown class="admin-user-menu" @command="handleCommand" trigger="click">
		<div class="admin-user-menu__trigger">
			<el-image
				v-if="avatar"
				:src="avatar ? this.$base.url + avatar : require('@/assets/img/avator.png')"
				fit="cover"
			></el-image>
			<span v-else class="admin-user-menu__avatar-fallback">A</span>
			<span class="admin-user-menu__name">{{ this.$storage.get('adminName') || '管理用户' }}</span>
			<span class="icon iconfont icon-xiala admin-user-menu__arrow"></span>
		</div>
		<el-dropdown-menu class="top-el-dropdown-menu" slot="dropdown">
			<el-dropdown-item :command="'home'">首页</el-dropdown-item>
			<el-dropdown-item :command="'center'">个人中心</el-dropdown-item>
			<el-dropdown-item v-if="isAuth('hasBoard','查看')" :command="'board'">数据看板</el-dropdown-item>
			<el-dropdown-item v-if="this.$storage.get('sessionTable') == 'users'" :command="'analyze'">数据分析</el-dropdown-item>
			<el-dropdown-item v-if="this.$storage.get('sessionTable') != 'users'" :command="'front'">退出到前台</el-dropdown-item>
			<el-dropdown-item divided :command="'logout'">退出登录</el-dropdown-item>
		</el-dropdown-menu>
	</el-dropdown>
</template>

<script>
	import { Loading } from 'element-ui'

	export default {
		computed: {
			avatar() {
				return this.$storage.get('headportrait') ? this.$storage.get('headportrait') : ''
			}
		},
		methods: {
			handleCommand(name) {
				if (name === 'logout') {
					this.onLogout()
				} else if (name === 'front') {
					this.onIndexTap()
				} else if (name === 'board') {
					this.toBoard()
				} else if (name === 'analyze') {
					this.analyzeClick()
				} else if (name === 'home') {
					this.goHome()
				} else {
					this.$router.push('/' + name)
				}
			},
			goHome() {
				this.$router.push('/')
			},
			async onLogout() {
				await this.$http.post(`${this.$storage.get('sessionTable')}/logout`).then(() => {
					let storage = this.$storage
					let router = this.$router
					storage.clear()
					this.$store.dispatch('tagsView/delAllViews')
					router.replace({
						name: 'login'
					})
				})
			},
			onIndexTap() {
				localStorage.setItem('frontToken', localStorage.getItem('Token'))
				localStorage.setItem('frontRole', localStorage.getItem('role'))
				localStorage.setItem('frontSessionTable', localStorage.getItem('sessionTable'))
				localStorage.setItem('frontHeadportrait', localStorage.getItem('headportrait'))
				localStorage.setItem('UserTableName', localStorage.getItem('sessionTable'))
				localStorage.setItem('frontUserid', localStorage.getItem('userid'))
				localStorage.setItem('username', localStorage.getItem('adminName'))
				window.location.href = `${this.$base.indexUrl}`
			},
			toBoard() {
				let routeData = this.$router.resolve({ path: '/board' })
				window.open(routeData.href, '_blank')
			},
			analyzeClick() {
				this.$confirm('是否进行大数据分析?', '数据分析提示', {
					confirmButtonText: '是',
					cancelButtonText: '否',
					type: 'warning'
				}).then(() => {
					let loading = Loading.service({
						fullscreen: false,
						text: '数据分析中，请稍等...'
					})
					this.$http({
						url: '/spark/analyze',
						method: 'get'
					}).then(({ data }) => {
						loading.close()
						if (data.code == 0) {
							this.$message({
								message: '数据分析完成',
								type: 'success',
								duration: 1500
							})
						}
					}, () => {
						loading.close()
					})
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.admin-user-menu {
		position: relative;
		z-index: 3;
		display: inline-flex;
		align-items: center;
		flex: 0 0 auto;
	}

	.admin-user-menu__trigger {
		display: inline-flex;
		align-items: center;
		gap: 12px;
		min-height: 48px;
		padding: 0 16px 0 12px;
		border: 1px solid rgba(255, 255, 255, 0.34);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.14);
		backdrop-filter: blur(24px) saturate(145%);
		color: var(--admin-text);
		transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
	}

	.admin-user-menu__trigger:hover {
		background: rgba(255, 255, 255, 0.24);
		transform: translateY(-1px);
		box-shadow: 0 10px 24px rgba(21, 33, 24, 0.04);
	}

	.admin-user-menu__trigger .el-image,
	.admin-user-menu__avatar-fallback {
		width: 28px;
		height: 28px;
		border-radius: 999px;
		overflow: hidden;
	}

	.admin-user-menu__avatar-fallback {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		background: rgba(31, 143, 99, 0.14);
		color: var(--admin-accent);
		font-size: 13px;
		font-weight: 700;
	}

	.admin-user-menu__name {
		font-size: 14px;
		font-weight: 600;
		white-space: nowrap;
	}

	.admin-user-menu__arrow {
		font-size: 12px;
		opacity: 0.48;
	}
</style>
