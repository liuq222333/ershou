<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回列表</el-button>
		</div>

		<section class="front-detail-hero front-detail-hero--single">
			<aside class="front-detail-hero__summary">
				<span class="front-pill">Comment Detail</span>
				<h1>{{ detail.nickname || '评论详情' }}</h1>
				<p>围绕评论内容、回复状态与管理动作重新排版，减少原页面里无意义的空区域与失效图片区。</p>
				<div class="front-detail-facts">
					<div class="front-detail-fact"><small>评论用户</small><strong>{{ detail.nickname || '--' }}</strong></div>
					<div class="front-detail-fact"><small>来源车辆</small><strong>{{ detail.refid || '--' }}</strong></div>
					<div class="front-detail-fact"><small>置顶状态</small><strong>{{ detail.istop == 1 ? '已置顶' : '普通评论' }}</strong></div>
					<div class="front-detail-fact"><small>回复状态</small><strong>{{ detail.reply ? '已回复' : '待回复' }}</strong></div>
				</div>
				<div class="front-detail-actions">
					<el-button v-if="btnAuth('discussusedcar','修改')" type="primary" @click="editClick">修改</el-button>
					<el-button v-if="btnAuth('discussusedcar','删除')" type="danger" @click="delClick">删除</el-button>
					<el-button v-if="btnAuth('discussusedcar','查看评论')" @click="discussClick">查看评论</el-button>
				</div>
			</aside>
		</section>

		<section class="front-detail-section">
			<h2>评论内容</h2>
			<div class="front-detail-section__panel front-comment-panel ql-snow ql-editor" v-html="detail.content || '<p>暂无评论内容</p>'"></div>
		</section>

		<section class="front-detail-section">
			<h2>回复内容</h2>
			<div v-if="detail.reply" class="front-detail-section__panel front-comment-panel ql-snow ql-editor" v-html="detail.reply"></div>
			<div v-else class="front-empty">当前还没有回复内容</div>
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
				tablename: 'discussusedcar',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '二手车'
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
					this.$router.push({path: '/index/discussusedcar', query: params});
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
				this.$router.push(`/index/discussusedcarAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此二手车？') .then(_ => {
					this.$http.post('discussusedcar/delete', [this.detail.id]).then(async res => {
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
			discussClick (){
				let params = {
					refid: this.detail.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/discussdiscussusedcar', query: params});
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
.front-detail-hero--single {
	grid-template-columns: 1fr;
}

.front-comment-panel {
	min-height: 140px;
}

.front-comment-panel {
	::v-deep .ql-editor {
		padding: 0;
		min-height: auto;
	}
}
</style>
