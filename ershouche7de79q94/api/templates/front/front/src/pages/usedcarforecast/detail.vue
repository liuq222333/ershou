<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回预测列表</el-button>
		</div>

		<section class="front-detail-section">
			<div class="front-section__head">
				<div>
					<span class="front-pill">Forecast Detail</span>
					<h2 style="margin-top: 16px;">{{ detail.brand }} {{ detail.model1 }}</h2>
					<p>预测记录采用与管理端接近的阅读布局，优先展示车辆条件与预测入口。</p>
				</div>
				<div class="front-detail-actions" style="margin-top: 0;">
					<el-button v-if="btnAuth('usedcarforecast','预测')" type="primary" @click="forecastClick()">开始预测</el-button>
					<el-button v-if="btnAuth('usedcarforecast','修改')" @click="editClick">修改</el-button>
					<el-button v-if="btnAuth('usedcarforecast','删除')" type="danger" @click="delClick">删除</el-button>
					<el-button v-if="btnAuth('usedcarforecast','章节管理')" @click="allchapterClick()">章节管理</el-button>
				</div>
			</div>

			<div class="front-detail-section__grid">
				<div class="front-detail-section__panel"><small class="front-muted">品牌</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.brand || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">型号</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.model1 || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">现价</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.discountprice || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">预测价</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.forecastprice || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">年份</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.vehicleage || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">里程 / 城市</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.kilometer || '--' }} / {{ detail.city || '--' }}</div></div>
			</div>
		</section>
	</div>
</template>
<script>
	import axios from 'axios'
	import Swiper from "swiper";
	import {
		Loading
	} from 'element-ui';
	export default {
		//数据集合
		data() {
			return {
				tablename: 'usedcarforecast',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '二手车预测'
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
					this.$router.push({path: '/index/usedcarforecast', query: params});
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
				this.$router.push(`/index/usedcarforecastAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此二手车预测？') .then(_ => {
					this.$http.post('usedcarforecast/delete', [this.detail.id]).then(async res => {
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
			forecastClick(row) {
				this.$confirm(`是否进行数据预测?`, "提示", {
					confirmButtonText: "确定",
					cancelButtonText: "取消",
					type: "warning"
				}).then(()=>{
					let loading = null
					loading = Loading.service({
						target: this.$refs['roleMenuBox'],
						fullscreen: false,
						text: '数据预测中...'
					})
					let arr = 'brand,model1,vehicleage,kilometer,city'.split(',')
					let brr = {
						id: this.detail.id
					}
					for(let x in arr){
						brr[arr[x]] = this.detail[arr[x]]
					}
					this.$http.post('usedcarforecast/forecast',brr).then(res=>{
						if(res.data&&res.data.code==0){
							if (loading) loading.close()
							this.$message({
								message: "数据预测完成！",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.init();
								}
							});
						}else {
							if (loading) loading.close()
							this.$message.error(res.msg)
						}
					},err=>{
						if (loading) loading.close()
						this.$message.error(err.msg)
					})
				})
			},
			allchapterClick (){
				let params = {
					refid: this.detail.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chapterusedcarforecast', query: params});
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

