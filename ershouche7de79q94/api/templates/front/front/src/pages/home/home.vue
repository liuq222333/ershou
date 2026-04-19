<template>
	<div class="front-home">
		<section class="front-home-hero">
			<div class="front-home-hero__copy">
				<div>
					<span class="front-pill">Market Insight Platform</span>
					<h1>用更清晰的界面，查看更真实的二手车市场。</h1>
					<p>
						围绕车源浏览、价格预测、公告动态与系统介绍重新编排内容层级，
						让用户在一个更轻透、更有留白的界面里完成筛选、判断与阅读。
					</p>
					<div class="front-home-hero__actions">
						<el-button type="primary" @click="moreBtn('usedcar')">浏览车源</el-button>
						<el-button @click="moreBtn('usedcarforecast')">开始预测</el-button>
						<el-button @click="moreBtn('news')">查看公告</el-button>
					</div>
				</div>

				<div class="front-home-kpis">
					<div class="front-home-kpi">
						<div class="front-home-kpi__label">车源总数</div>
						<div class="front-home-kpi__value">{{ usedcarCount }}</div>
					</div>
					<div class="front-home-kpi">
						<div class="front-home-kpi__label">预测记录</div>
						<div class="front-home-kpi__value">{{ forecastCount }}</div>
					</div>
					<div class="front-home-kpi">
						<div class="front-home-kpi__label">最新公告</div>
						<div class="front-home-kpi__value">{{ newsTotal }}</div>
					</div>
				</div>
			</div>

			<div class="front-carousel-card">
				<el-carousel height="100%" :interval="4200" arrow="never" indicator-position="outside">
					<el-carousel-item v-for="(slide, index) in heroSlides" :key="index">
						<div
							class="front-carousel-card__slide"
							:style="{ backgroundImage: `linear-gradient(180deg, rgba(20,34,26,.1), rgba(20,34,26,.68)), url(${slide.image})` }"
						>
							<div class="front-carousel-card__content">
								<span class="front-pill" style="background: rgba(255,255,255,.16); border-color: rgba(255,255,255,.18); color: #fff;">
									{{ slide.tag }}
								</span>
								<h3>{{ slide.title }}</h3>
								<p>{{ slide.desc }}</p>
							</div>
							<div class="front-carousel-card__footer">
								<el-button type="primary" size="mini" @click="goSlide(slide.route)">进入模块</el-button>
								<span>{{ slide.meta }}</span>
							</div>
						</div>
					</el-carousel-item>
				</el-carousel>
			</div>
		</section>

		<div class="front-home-grid">
			<section class="front-section">
				<div class="front-section__head">
					<div>
						<h2>系统简介</h2>
						<p>将旧模板式正文块重排为轻阅读内容区，先看摘要，再决定是否进入详情。</p>
					</div>
					<el-button @click="toDetail('systemintroDetail', systemIntroductionDetail)">查看详情</el-button>
				</div>

				<div class="front-article-card front-clickable" @click="toDetail('systemintroDetail', systemIntroductionDetail)">
					<div class="front-article-card__media">
						<img :src="systemCover" alt="system intro">
					</div>
					<div>
						<div class="front-article-card__meta">System Introduction</div>
						<h3>{{ systemIntroductionDetail.title || '平台概览' }}</h3>
						<p>{{ systemSummary }}</p>
						<div class="front-article-card__footer">
							<span>{{ systemIntroductionDetail.subtitle || '数据采集 / 智能预测 / 公告资讯' }}</span>
							<span>了解平台能力</span>
						</div>
					</div>
				</div>
			</section>

			<section class="front-section">
				<div class="front-section__head">
					<div>
						<h2>公告动态</h2>
						<p>公告不再堆叠在密集列表里，而是以更轻的资讯流呈现。</p>
					</div>
					<el-button @click="moreBtn('news')">全部公告</el-button>
				</div>

				<div v-if="newsList.length" class="front-article-list">
					<article
						v-for="item in newsList.slice(0, 3)"
						:key="item.id"
						class="front-article-card front-clickable"
						@click="toDetail('newsDetail', item)"
					>
						<div class="front-article-card__media">
							<img :src="newsImage(item)" alt="news">
						</div>
						<div>
							<div class="front-article-card__meta">Announcement</div>
							<h3>{{ item.title }}</h3>
							<p>{{ item.introduction || '查看最新平台公告与业务动态。' }}</p>
							<div class="front-article-card__footer">
								<span>{{ item.addtime ? item.addtime.split(' ')[0] : '' }}</span>
								<span>{{ item.name || '系统发布' }}</span>
							</div>
						</div>
					</article>
				</div>
				<div v-else class="front-empty">暂无公告内容</div>
			</section>
		</div>

		<section class="front-section" style="margin-top: 24px;">
			<div class="front-section__head">
				<div>
					<h2>推荐车源</h2>
					<p>推荐区域改成图像主导的浏览体验，减少旧模板里的重复字段堆叠。</p>
				</div>
				<el-button type="primary" @click="moreBtn('usedcar')">全部车源</el-button>
			</div>

			<div v-if="usedcarRecommend.length" class="front-car-grid">
				<article
					v-for="item in usedcarRecommend.slice(0, 4)"
					:key="item.id"
					class="front-car-card front-clickable"
					@click="toDetail('usedcarDetail', item)"
				>
					<div class="front-car-card__media">
						<img :src="carImage(item.imgurl)" alt="used car">
					</div>
					<div>
						<div class="front-car-card__header">
							<div class="front-car-card__title">
								<h3>{{ item.brand }}</h3>
								<p>{{ item.model1 }}</p>
							</div>
							<div class="front-car-card__price">
								<strong>{{ item.discountprice || '--' }}</strong>
								<span>现价 / 元</span>
							</div>
						</div>
						<div class="front-car-card__facts">
							<div class="front-car-card__fact">
								<div class="front-car-card__fact-label">年份</div>
								<div class="front-car-card__fact-value">{{ item.vehicleage || '--' }}</div>
							</div>
							<div class="front-car-card__fact">
								<div class="front-car-card__fact-label">里程</div>
								<div class="front-car-card__fact-value">{{ item.kilometer || '--' }}</div>
							</div>
							<div class="front-car-card__fact">
								<div class="front-car-card__fact-label">城市</div>
								<div class="front-car-card__fact-value">{{ item.city || '--' }}</div>
							</div>
						</div>
						<div class="front-car-card__footer">
							<div class="front-car-card__metrics">
								<span>浏览 {{ item.clicknum || 0 }}</span>
								<span>收藏 {{ item.storeupnum || 0 }}</span>
								<span>点赞 {{ item.thumbsupnum || 0 }}</span>
							</div>
							<el-button type="text">查看详情</el-button>
						</div>
					</div>
				</article>
			</div>
			<div v-else class="front-empty">暂无推荐车源</div>
		</section>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				baseUrl: '',
				systemIntroductionDetail: {},
				newsList: [],
				usedcarRecommend: [],
				usedcarCount: 0,
				forecastCount: 0,
				newsTotal: 0
			}
		},
		created() {
			this.baseUrl = this.$config.baseUrl
			this.getNewsList()
			this.getSystemIntroduction()
			this.getList()
			this.getCounts()
		},
		computed: {
			systemSummary() {
				const html = this.systemIntroductionDetail.content || ''
				const text = html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()
				if (!text) {
					return '聚焦二手车数据采集、车源浏览、价格预测与系统公告，让用户更快速理解平台价值与使用方式。'
				}
				return text.length > 160 ? `${text.slice(0, 160)}...` : text
			},
			systemCover() {
				const picture = this.systemIntroductionDetail.picture1 || this.systemIntroductionDetail.picture2 || this.systemIntroductionDetail.picture3
				return this.resolveImage(picture)
			},
			heroSlides() {
				const recommendationSlides = (this.usedcarRecommend || []).slice(0, 3).map((item) => ({
					tag: 'Recommended Car',
					title: `${item.brand || '热门车源'} ${item.model1 || ''}`.trim(),
					desc: `年份 ${item.vehicleage || '--'} · 里程 ${item.kilometer || '--'} · 城市 ${item.city || '--'}`,
					image: this.carImage(item.imgurl),
					route: '/index/usedcar',
					meta: `现价 ${item.discountprice || '--'}`
				}))
				if (recommendationSlides.length) {
					return recommendationSlides
				}
				return [
					{
						tag: 'Prediction',
						title: '基于多维特征的价格预测',
						desc: '用更轻盈的浏览体验连接预测入口与结果页面。',
						image: require('@/assets/chapter.jpg'),
						route: '/index/usedcarforecast',
						meta: '进入预测模块'
					},
					{
						tag: 'Announcement',
						title: '在统一风格中查看最新公告',
						desc: '公告、详情和系统说明页统一回到同一视觉体系里。',
						image: require('@/assets/AI.png'),
						route: '/index/news',
						meta: '进入公告模块'
					}
				]
			}
		},
		methods: {
			resolveImage(value, fallback = require('@/assets/chapter.jpg')) {
				if (!value) {
					return fallback
				}
				const rawValue = String(value).trim()
				if (!rawValue) {
					return fallback
				}
				if (rawValue.substr(0, 4) === 'http') {
					return rawValue.split(',w').length > 1 ? rawValue : rawValue.split(',')[0]
				}
				return this.baseUrl + rawValue.split(',')[0]
			},
			carImage(value) {
				return this.resolveImage(value)
			},
			newsImage(item) {
				return this.resolveImage(item && item.picture)
			},
			getSystemIntroduction() {
				this.$http.get('systemintro/detail/1', {}).then((res) => {
					if (res.data.code === 0) {
						this.systemIntroductionDetail = res.data.data
					}
				})
			},
			getNewsList() {
				const data = {
					page: 1,
					limit: 4,
					sort: 'addtime',
					order: 'desc'
				}
				this.$http.get('news/list', { params: data }).then((res) => {
					if (res.data.code === 0) {
						this.newsList = res.data.data.list || []
						this.newsTotal = Number(res.data.data.total || this.newsList.length || 0)
					}
				})
			},
			getList() {
				let autoSortUrl = 'usedcar/autoSort'
				if (localStorage.getItem('frontToken')) {
					autoSortUrl = 'usedcar/autoSort2'
				}
				this.$http.get(autoSortUrl, { params: { page: 1, limit: 8 } }).then((res) => {
					if (res.data.code === 0) {
						this.usedcarRecommend = res.data.data.list || []
					}
				})
			},
			getCounts() {
				this.$http.get('usedcar/count').then((res) => {
					if (res.data.code === 0) {
						this.usedcarCount = res.data.data || 0
					}
				})
				this.$http.get('usedcarforecast/count').then((res) => {
					if (res.data.code === 0) {
						this.forecastCount = res.data.data || 0
					}
				}).catch(() => {})
			},
			moreBtn(path) {
				this.$router.push(`/index/${path}`)
			},
			goSlide(route) {
				this.$router.push(route)
			},
			toDetail(path, item) {
				if (!item || !item.id) {
					return
				}
				this.$router.push({ path: `/index/${path}`, query: { id: item.id } })
			}
		}
	}
</script>
