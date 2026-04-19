<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回列表</el-button>
		</div>

		<section class="front-detail-hero front-detail-hero--config">
			<div class="front-detail-hero__gallery front-config-media">
				<div class="front-config-media__frame" v-if="detail.value && (detail.value.substring(0,4)=='http' || detail.value.indexOf('/') !== -1)">
					<img :src="detail.value.substring(0,4)=='http' ? detail.value.split(',')[0] : baseUrl + detail.value.split(',')[0]" alt="config">
				</div>
				<div v-else class="front-config-media__placeholder">{{ detail.value || '暂无值内容' }}</div>
			</div>

			<aside class="front-detail-hero__summary">
				<span class="front-pill">Config Detail</span>
				<h1>{{ detail.name || '配置详情' }}</h1>
				<p>配置详情页保留原有字段与操作能力，但用更清楚的摘要方式展示配置名、链接、类型和值。</p>
				<div class="front-detail-facts">
					<div class="front-detail-fact"><small>名称</small><strong>{{ detail.name || '--' }}</strong></div>
					<div class="front-detail-fact"><small>类型</small><strong>{{ detail.type || '--' }}</strong></div>
					<div class="front-detail-fact"><small>URL</small><strong>{{ detail.url || '--' }}</strong></div>
					<div class="front-detail-fact"><small>值</small><strong>{{ detail.value || '--' }}</strong></div>
				</div>
				<div class="front-detail-actions">
					<el-button v-if="btnAuth('config','修改')" type="primary" @click="editClick">修改</el-button>
					<el-button v-if="btnAuth('config','删除')" type="danger" @click="delClick">删除</el-button>
				</div>
			</aside>
		</section>
	</div>
</template>

<script>
	import axios from 'axios'
	import Swiper from "swiper";
	export default {
		//数据集合
		data() {
			return {
				tablename: 'config',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '配置管理'
					}
				],
				title: '',
				detailBanner: [],
				userid: Number(localStorage.getItem('frontUserid')),
				id: 0,
				detail: {},
				tabsNum: 0,
				activeName: '1',
				buynumber: 1,
				centerType: false,
				storeupType: false,
				swiperBigUrl: null,
			}
		},
		created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0) {
				this.centerType = true
			}
			if(this.$route.query.storeupType&&this.$route.query.storeupType!=0) {
				this.storeupType = true
			}
			
			this.init();
		},
		mounted() {
		},
		computed: {
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			swiperClick3(src) {
				this.swiperBigUrl = src
			},
			init() {
				this.id = this.$route.query.id
				this.baseUrl = this.$config.baseUrl;
				this.$http.get(this.tablename + '/detail/'  + this.id, {}).then(async res => {
					if (res.data.code == 0) {
						this.detail = res.data.data;
						this.$forceUpdate();
						if(localStorage.getItem('frontToken')){
						}

					}
					if (this.detailBanner.length) {
						if (this.detailBanner[0].substr(0,4)=='http') {
							this.swiperBigUrl = this.detailBanner[0]
						} else {
							this.swiperBigUrl = this.baseUrl + this.detailBanner[0]
						}
					}
				});
			},
			curChange(page) {
				this.getDiscussList(page);
			},
			prevClick(page) {
				this.getDiscussList(page);
			},
			nextClick(page) {
				this.getDiscussList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getDiscussList(1);
			},
			// 返回按钮
			backClick(){
				if(this.storeupType){
					history.back()
				}else{
					let params = {}
					if(this.centerType){
						params.centerType = 1
					}
					this.$router.push({path: '/index/config', query: params});
				}
			},
			// 下载
			download(file ){
				if(!file) {
					this.$message({
						type: 'error',
						message: '文件不存在',
						duration: 1500,
					});
					return;
				}
				let arr = file.replace(new RegExp('upload/', "g"), "")
				axios.get(this.baseUrl + 'file/download?fileName=' + arr, {
					headers: {
						token: localStorage.getItem("frontToken")
					},
					responseType: "blob"
				}).then(({
					data
				}) => {
					const binaryData = [];
					binaryData.push(data);
					const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
						type: 'application/pdf;chartset=UTF-8'
					}))
					const a = document.createElement('a')
					a.href = objectUrl
					a.download = arr
					// a.click()
					// 下面这个写法兼容火狐
					a.dispatchEvent(new MouseEvent('click', {
						bubbles: true,
						cancelable: true,
						view: window
					}))
					window.URL.revokeObjectURL(data)
				},err=>{
					axios.get((location.href.split(this.$config.name).length>1 ? location.href.split(this.$config.name)[0] :'') + this.$config.name + 'file/download?fileName=' + arr, {
						headers: {
							token: localStorage.getItem("frontToken")
						},
						responseType: "blob"
					}).then(({
						data
					}) => {
						const binaryData = [];
						binaryData.push(data);
						const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
							type: 'application/pdf;chartset=UTF-8'
						}))
						const a = document.createElement('a')
						a.href = objectUrl
						a.download = arr
						// a.click()
						// 下面这个写法兼容火狐
						a.dispatchEvent(new MouseEvent('click', {
							bubbles: true,
							cancelable: true,
							view: window
						}))
						window.URL.revokeObjectURL(data)
					})
				})
			},


			// 权限判断
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			// 修改
			editClick(){
				this.$router.push(`/index/configAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此配置管理？') .then(_ => {
					this.$http.post('config/delete', [this.detail.id]).then(async res => {
						if (res.data.code == 0) {
							this.$message({
								type: 'success',
								message: '删除成功!',
								duration: 1500,
								onClose: () => {
									history.back()
								}
							});
						}
					});
				}).catch(_ => {});
			},
			// 获取uuid
			getUUID() {
				return new Date().getTime();
			},
		},
		components: {
		}
	}
</script>

<style lang="scss" scoped>
.front-detail-hero--config {
	grid-template-columns: 360px 1fr;
}

.front-config-media {
	display: flex;
	align-items: stretch;
}

.front-config-media__frame,
.front-config-media__placeholder {
	width: 100%;
	border-radius: 24px;
	overflow: hidden;
	background: #dde8de;
	min-height: 320px;
}

.front-config-media__frame img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.front-config-media__placeholder {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 24px;
	color: var(--front-text-soft);
	text-align: center;
	line-height: 1.8;
}

@media (max-width: 1200px) {
	.front-detail-hero--config {
		grid-template-columns: 1fr;
	}
}
</style>
