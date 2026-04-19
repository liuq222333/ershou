<template>
	<div class="front-shell">
		<header class="front-navbar">
			<div class="front-navbar__inner">
				<div class="front-navbar__left">
					<div class="front-navbar__brand" @click="goMenu('/index/home')">
						<span class="front-navbar__brand-mark">Used Car Intelligence</span>
						<span class="front-navbar__brand-name">二手车数据平台</span>
					</div>

					<nav class="front-navbar__menu">
						<button
							v-for="item in displayMenuList"
							:key="item.url"
							:class="['front-navbar__link', { 'is-active': activeMenu === item.url }]"
							@click="goMenu(item.url)"
						>
							{{ item.name }}
						</button>
					</nav>
				</div>

				<div class="front-navbar__right">
					<el-dropdown v-if="Token" trigger="click" @command="handleCommand">
						<div class="front-navbar__panel front-navbar__panel--user">
							<img
								class="front-navbar__avatar"
								:src="headportrait ? baseUrl + headportrait : require('@/assets/avator.png')"
								alt="avatar"
							>
							<div class="front-navbar__meta">
								<span class="front-navbar__meta-label">当前用户</span>
								<span class="front-navbar__meta-name">{{ username || '未命名用户' }}</span>
							</div>
							<i class="el-icon-arrow-down front-navbar__caret"></i>
						</div>
						<el-dropdown-menu slot="dropdown">
							<el-dropdown-item command="home">首页</el-dropdown-item>
							<el-dropdown-item command="user" v-if="notAdmin">个人中心</el-dropdown-item>
							<el-dropdown-item command="board" v-if="boardAuth()">数据看板</el-dropdown-item>
							<el-dropdown-item command="register">退出登录</el-dropdown-item>
						</el-dropdown-menu>
					</el-dropdown>

					<div v-else class="front-navbar__panel front-navbar__panel--auth">
						<button class="front-navbar__login" @click="toLogin">登录</button>
						<button class="front-navbar__register" @click="toRegister">注册</button>
					</div>
				</div>
			</div>
		</header>

		<main class="front-router-shell">
			<router-view></router-view>
		</main>

		<footer class="front-footer">
			<div>
				二手车销售数据采集与趋势分析平台 · 统一用户端体验已切换为绿色产品风格，聚焦车源浏览、价格预测与公告信息。
			</div>
		</footer>
	</div>
</template>

<script>
	import Vue from 'vue'

	export default {
		data() {
			return {
				baseUrl: '',
				menuList: [],
				headportrait: localStorage.getItem('frontHeadportrait') ? localStorage.getItem('frontHeadportrait') : '',
				Token: localStorage.getItem('frontToken'),
				username: localStorage.getItem('username') || '',
				notAdmin: localStorage.getItem('frontSessionTable') !== '"users"'
			}
		},
		created() {
			this.baseUrl = this.$config.baseUrl
			this.menuList = this.$config.indexNav || []
			if (localStorage.getItem('frontToken')) {
				this.getSession()
			}
		},
		watch: {
			$route() {
				this.syncLocalUser()
				window.scrollTo({ top: 0, behavior: 'smooth' })
			}
		},
		computed: {
			displayMenuList() {
				return [
					{ name: '首页', url: '/index/home' },
					...(this.menuList || [])
				]
			},
			activeMenu() {
				const path = this.$route.path
				if (path.indexOf('/index/usedcarforecast') === 0) return '/index/usedcarforecast'
				if (path.indexOf('/index/usedcar') === 0) return '/index/usedcar'
				if (path.indexOf('/index/news') === 0) return '/index/news'
				if (path.indexOf('/index/home') === 0) return '/index/home'
				return path
			}
		},
		methods: {
			syncLocalUser() {
				this.Token = localStorage.getItem('frontToken')
				this.username = localStorage.getItem('username') || ''
				this.headportrait = localStorage.getItem('frontHeadportrait') || ''
				this.notAdmin = localStorage.getItem('frontSessionTable') !== '"users"'
			},
			async getSession() {
				const tableName = localStorage.getItem('UserTableName')
				if (!tableName) {
					return
				}
				await this.$http.get(`${tableName}/session`, { emulateJSON: true }).then((res) => {
					if (res.data.code === 0) {
						localStorage.setItem('sessionForm', JSON.stringify(res.data.data))
						localStorage.setItem('frontUserid', res.data.data.id)
						if (res.data.data.vip) {
							localStorage.setItem('vip', res.data.data.vip)
						}
						const avatar = res.data.data.touxiang || res.data.data.headportrait || ''
						if (avatar) {
							this.headportrait = avatar
							localStorage.setItem('frontHeadportrait', avatar)
						}
						this.syncLocalUser()
					}
				})
			},
			toLogin() {
				this.$router.push('/login')
			},
			toRegister() {
				this.$router.push({ path: '/register', query: { role: 'yonghu', pageFlag: 'register' } })
			},
			async logout() {
				await this.$http.post(`${localStorage.getItem('frontSessionTable')}/logout`).then(() => {
					localStorage.clear()
					Vue.http.headers.common.Token = ''
					this.Token = ''
					this.username = ''
					this.headportrait = ''
					this.$router.push('/index/home')
					this.$message({
						message: '登出成功',
						type: 'success',
						duration: 1000
					})
				})
			},
			goBoard() {
				localStorage.setItem('Token', localStorage.getItem('frontToken'))
				localStorage.setItem('role', localStorage.getItem('frontRole'))
				localStorage.setItem('sessionTable', localStorage.getItem('frontSessionTable'))
				localStorage.setItem('headportrait', localStorage.getItem('frontHeadportrait'))
				localStorage.setItem('userid', Number(localStorage.getItem('frontUserid')))
				localStorage.setItem('adminName', localStorage.getItem('username'))
				localStorage.setItem('userForm', JSON.stringify(localStorage.getItem('sessionForm')))
				window.location.href = 'http://localhost:8080/admin/dist/index.html#/board?frontType==1'
			},
			boardAuth() {
				return this.isAuth('hasBoard', '查看') || this.isBackAuth('hasBoard', '查看')
			},
			goMenu(path) {
				this.$router.push(path)
			},
			handleCommand(name) {
				if (name === 'register') {
					this.logout()
				} else if (name === 'user') {
					this.goMenu('/index/center')
				} else if (name === 'board') {
					this.goBoard()
				} else if (name === 'home') {
					this.goMenu('/index/home')
				}
			}
		}
	}
</script>
