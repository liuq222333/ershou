<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回列表</el-button>
		</div>

		<section class="front-detail-hero front-detail-hero--user">
			<div class="front-detail-hero__gallery front-user-detail-media">
				<div class="front-user-detail-avatar">
					<img :src="detail.touxiang ? (detail.touxiang.substring(0,4) == 'http' ? detail.touxiang.split(',')[0] : baseUrl + detail.touxiang.split(',')[0]) : require('@/assets/avator.png')" alt="avatar">
				</div>
				<div class="front-user-detail-caption">
					<strong>{{ detail.xingming || detail.zhanghao || '用户资料' }}</strong>
					<span>{{ detail.mobile || '暂无手机号' }}</span>
				</div>
			</div>

			<aside class="front-detail-hero__summary">
				<span class="front-pill">User Profile</span>
				<h1>{{ detail.xingming || detail.zhanghao || '用户详情' }}</h1>
				<p>用户详情页按当前管理端的工作区风格重排，把身份信息、联系方式和操作按钮收拢成更清楚的结构。</p>
				<div class="front-detail-facts">
					<div class="front-detail-fact"><small>账号</small><strong>{{ detail.zhanghao || '--' }}</strong></div>
					<div class="front-detail-fact"><small>性别</small><strong>{{ detail.xingbie || '--' }}</strong></div>
					<div class="front-detail-fact"><small>年龄</small><strong>{{ detail.nianling || '--' }}</strong></div>
					<div class="front-detail-fact"><small>手机号</small><strong>{{ detail.mobile || '--' }}</strong></div>
					<div class="front-detail-fact"><small>身份证</small><strong>{{ detail.shenfenzheng || '--' }}</strong></div>
					<div class="front-detail-fact"><small>资料状态</small><strong>{{ detail.id ? '已建档' : '待完善' }}</strong></div>
				</div>
				<div class="front-detail-actions">
					<el-button v-if="btnAuth('yonghu','修改')" type="primary" @click="editClick">修改</el-button>
					<el-button v-if="btnAuth('yonghu','删除')" type="danger" @click="delClick">删除</el-button>
					<el-button v-if="btnAuth('yonghu','章节管理')" @click="allchapterClick()">章节管理</el-button>
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
				tablename: 'yonghu',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '用户'
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
					this.$router.push({path: '/index/yonghu', query: params});
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
				this.$router.push(`/index/yonghuAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此用户？') .then(_ => {
					this.$http.post('yonghu/delete', [this.detail.id]).then(async res => {
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
			allchapterClick (){
				let params = {
					refid: this.detail.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chapteryonghu', query: params});
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
.front-detail-hero--user {
	grid-template-columns: 360px 1fr;
}

.front-user-detail-media {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	gap: 18px;
}

.front-user-detail-avatar {
	border-radius: 24px;
	overflow: hidden;
	background: #dbe6dc;
	aspect-ratio: 1 / 1;
}

.front-user-detail-avatar img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.front-user-detail-caption {
	display: flex;
	flex-direction: column;
	gap: 6px;
	padding: 18px;
	border-radius: 18px;
	background: rgba(47, 123, 87, 0.06);
}

.front-user-detail-caption strong {
	font-size: 22px;
}

.front-user-detail-caption span {
	color: var(--front-text-soft);
	font-size: 13px;
}

@media (max-width: 1200px) {
	.front-detail-hero--user {
		grid-template-columns: 1fr;
	}
}
</style>
