<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Market Bulletin</span>
				<h1>公告动态</h1>
				<p>集中展示车源上新、检测标准、交易流程、金融服务与售后提醒等二手车交易公告。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 条公告</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-input
					v-model="title"
					class="front-toolbar__search"
					placeholder="搜索交易公告标题"
					clearable
					@keyup.enter.native="getNewsList(1)"
				></el-input>
				<el-button type="primary" @click="getNewsList(1)">搜索</el-button>
			</div>
			<div class="front-toolbar__hint">按时间倒序展示最新交易公告与服务提醒。</div>
		</section>

		<section class="front-section">
			<div v-if="newsList.length" class="front-article-list">
				<article
					v-for="item in newsList"
					:key="item.id"
					class="front-article-card front-clickable"
					@click="toNewsDetail(item)"
				>
					<div class="front-article-card__media">
						<img :src="coverUrl(item)" alt="announcement">
					</div>
					<div>
						<div class="front-article-card__meta">Used Car Notice</div>
						<h3>{{ item.title }}</h3>
						<p>{{ item.introduction || '查看公告详情，了解车源、检测、过户与交易服务最新通知。' }}</p>
						<div class="front-article-card__footer">
							<span>{{ item.addtime ? item.addtime.split(' ')[0] : '' }}</span>
							<span>{{ item.name || '系统发布' }}</span>
						</div>
					</div>
				</article>
			</div>
			<div v-else class="front-empty">没有匹配到交易公告</div>

			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				:page-sizes="pageSizes"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
			></el-pagination>
		</section>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				baseUrl: this.$config.baseUrl,
				newsList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				title: ''
			}
		},
		created() {
			this.getNewsList(1)
		},
		methods: {
			coverUrl(item) {
				if (!item || !item.picture) {
					return require('@/assets/chapter.jpg')
				}
				return this.baseUrl + item.picture.split(',')[0]
			},
			getNewsList(page) {
				const params = { page, limit: this.pageSize, sort: 'addtime', order: 'desc' }
				const searchWhere = {}
				if (this.title !== '') {
					searchWhere.title = '%' + this.title + '%'
				}
				this.$http.get('news/list', { params: Object.assign(params, searchWhere) }).then((res) => {
					if (res.data.code === 0) {
						this.newsList = res.data.data.list || []
						this.total = Number(res.data.data.total || 0)
						this.pageSize = Number(res.data.data.pageSize || this.pageSize)
						this.totalPage = Number(res.data.data.totalPage || 0)
						if (this.pageSizes.length === 0) {
							this.pageSizes = [this.pageSize, this.pageSize * 2, this.pageSize * 3, this.pageSize * 5]
						}
					}
				})
			},
			curChange(page) {
				this.getNewsList(page)
			},
			sizeChange(size) {
				this.pageSize = size
				this.getNewsList(1)
			},
			prevClick(page) {
				this.getNewsList(page)
			},
			nextClick(page) {
				this.getNewsList(page)
			},
			toNewsDetail(item) {
				this.$router.push({ path: '/index/newsDetail', query: { id: item.id } })
			}
		}
	}
</script>
