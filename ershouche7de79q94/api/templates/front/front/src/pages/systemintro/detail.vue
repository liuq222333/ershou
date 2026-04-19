<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<section class="front-article-detail">
			<span class="front-pill">System Introduction</span>
			<h1 style="margin: 16px 0 0; font-size: clamp(32px, 4vw, 48px); line-height: 1.05; letter-spacing: -0.05em;">
				{{ detail.title || '平台简介' }}
			</h1>
			<div class="front-article-detail__meta">
				<span>{{ detail.subtitle || '数据采集 / 价格预测 / 公告资讯' }}</span>
			</div>
			<div class="front-page-grid front-page-grid--two" v-if="detailBanner.length" style="margin-bottom: 24px;">
				<div
					v-for="(item, index) in detailBanner"
					:key="index"
					class="front-article-detail__cover"
					style="margin-bottom: 0;"
				>
					<img :src="item" alt="system intro image">
				</div>
			</div>
			<div class="front-article-detail__body ql-snow ql-editor" v-html="detail.content"></div>
		</section>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				tablename: 'systemintro',
				baseUrl: '',
				id: 0,
				detail: {},
				detailBanner: [],
				centerType: false,
				storeupType: false
			}
		},
		created() {
			if (this.$route.query.centerType && this.$route.query.centerType !== 0) {
				this.centerType = true
			}
			if (this.$route.query.storeupType && this.$route.query.storeupType !== 0) {
				this.storeupType = true
			}
			this.init()
		},
		methods: {
			init() {
				this.id = this.$route.query.id
				this.baseUrl = this.$config.baseUrl
				this.$http.get(this.tablename + '/detail/' + this.id, {}).then((res) => {
					if (res.data.code === 0) {
						this.detail = res.data.data
						this.detailBanner = [res.data.data.picture1, res.data.data.picture2, res.data.data.picture3]
							.filter(Boolean)
							.map((item) => (item.substr(0, 4) === 'http' ? item : this.baseUrl + item))
					}
				})
			},
			backClick() {
				history.back()
			}
		}
	}
</script>
