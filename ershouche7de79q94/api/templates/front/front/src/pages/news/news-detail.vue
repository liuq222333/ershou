<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回公告列表</el-button>
		</div>

		<section class="front-article-detail">
			<span class="front-pill">Notice Detail</span>
			<h1 style="margin: 16px 0 0; font-size: clamp(32px, 4vw, 48px); line-height: 1.05; letter-spacing: -0.05em;">
				{{ detail.title }}
			</h1>
			<div class="front-article-detail__meta">
				<span>发布时间 {{ detail.addtime ? detail.addtime.split(' ')[0] : '' }}</span>
				<span>发布人 {{ detail.name || '系统发布' }}</span>
			</div>
			<div class="front-article-detail__cover" v-if="detail.picture">
				<img :src="baseUrl + detail.picture.split(',')[0]" alt="cover">
			</div>
			<div class="front-article-detail__body ql-snow ql-editor" v-html="detail.content"></div>
		</section>

		<section class="front-detail-section">
			<div class="front-section__head" style="margin-bottom: 0;">
				<div>
					<h2>继续阅读</h2>
					<p>继续查看其他二手车交易公告、服务规则与市场提醒。</p>
				</div>
			</div>
			<div class="front-page-grid front-page-grid--two">
				<div class="front-section front-clickable" @click="prepDetailClick">
					<span class="front-pill">上一篇</span>
					<h3 style="margin: 14px 0 0; font-size: 22px;">{{ currentIndex === 0 || !allList[currentIndex - 1] ? '没有上一篇了' : allList[currentIndex - 1].title }}</h3>
				</div>
				<div class="front-section front-clickable" @click="nextDetailClick">
					<span class="front-pill">下一篇</span>
					<h3 style="margin: 14px 0 0; font-size: 22px;">{{ currentIndex === allList.length - 1 || !allList[currentIndex + 1] ? '已经是最后一篇' : allList[currentIndex + 1].title }}</h3>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				id: 0,
				detail: {},
				baseUrl: '',
				currentIndex: 0,
				allList: [],
				storeupType: false
			}
		},
		created() {
			if (this.$route.query.storeupType && this.$route.query.storeupType !== 0) {
				this.storeupType = true
			}
			this.id = this.$route.query.id
			this.baseUrl = this.$config.baseUrl
			this.getDetail()
			this.getNewsList()
		},
		watch: {
			$route() {
				this.id = this.$route.query.id
				this.getDetail()
			}
		},
		methods: {
			backClick() {
				if (this.storeupType) {
					history.back()
				} else {
					this.$router.push({ path: '/index/news' })
				}
			},
			getNewsList() {
				const params = { page: 1, limit: 100, sort: 'addtime', order: 'desc' }
				this.$http.get('news/list', { params }).then((res) => {
					if (res.data.code === 0) {
						const list = res.data.data.list || []
						this.allList = list
						for (let x = 0; x < list.length; x++) {
							if (list[x].id === this.id || String(list[x].id) === String(this.id)) {
								this.currentIndex = x
								break
							}
						}
					}
				})
			},
			prepDetailClick() {
				if (this.currentIndex === 0) {
					this.$message.error('已经是第一篇了')
					return
				}
				this.currentIndex -= 1
				this.$router.push({ path: '/index/newsDetail', query: { id: this.allList[this.currentIndex].id } })
			},
			nextDetailClick() {
				if (this.currentIndex === this.allList.length - 1) {
					this.$message.error('已经是最后一篇了')
					return
				}
				this.currentIndex += 1
				this.$router.push({ path: '/index/newsDetail', query: { id: this.allList[this.currentIndex].id } })
			},
			getDetail() {
				this.$http.get(`news/detail/${this.id}`, {}).then((res) => {
					if (res.data && res.data.code === 0) {
						this.detail = res.data.data
						window.scrollTo(0, 0)
					}
				})
			}
		}
	}
</script>
