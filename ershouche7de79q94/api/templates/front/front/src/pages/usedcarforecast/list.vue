<template>
	<div class="front-page">
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Forecast Workspace</span>
				<h1>二手车预测列表</h1>
				<p>将预测列表切换成更轻的工作台语言，让新增、预测图表与结果查看都统一到管理端同一套风格里。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 条预测记录</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-button v-if="btnAuth('usedcarforecast','新增')" type="primary" @click="add('/index/usedcarforecastAdd')">新增预测</el-button>
				<el-button v-if="btnAuth('usedcarforecast','预测')" @click="forecastImgClick()">预测图表</el-button>
			</div>
			<div class="front-toolbar__hint">表格样式已向管理端预测模块对齐，优先突出关键字段与操作入口。</div>
		</section>

		<section class="front-table-shell">
			<el-table class="front-table" :border="false" :data="dataList">
				<el-table-column prop="brand" label="品牌"></el-table-column>
				<el-table-column prop="model1" label="型号"></el-table-column>
				<el-table-column prop="discountprice" label="现价"></el-table-column>
				<el-table-column prop="forecastprice" label="预测价"></el-table-column>
				<el-table-column prop="vehicleage" label="年份"></el-table-column>
				<el-table-column prop="kilometer" label="行驶里程"></el-table-column>
				<el-table-column prop="city" label="所在城市"></el-table-column>
				<el-table-column width="220" label="操作">
					<template slot-scope="scope">
						<el-button type="primary" size="mini" @click.native="toDetail(scope.row)">查看</el-button>
						<el-button class="table-btn5" size="mini" @click.native="chapterClick(scope.row)" v-if="btnAuth('usedcarforecast','章节管理')">章节管理</el-button>
					</template>
				</el-table-column>
			</el-table>

			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				:page-sizes="pageSizes"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
			></el-pagination>
		</section>

		<el-dialog title="预览图" :visible.sync="previewVisible" width="50%">
			<img :src="previewImg" alt="" style="width: 100%;">
		</el-dialog>
		<el-dialog title="可视化图表" :visible.sync="forecastVisible" width="60%">
			<div style="display: flex; flex-wrap: wrap; gap: 12px;">
				<el-image v-for="item in forecastImgList" :key="item" :src="baseUrl + item" lazy style="border-radius: 16px; overflow: hidden;"></el-image>
			</div>
		</el-dialog>
	</div>
</template>
<script>
	import axios from 'axios';
	import {
		Loading
	} from 'element-ui';
	export default {
		//数据集合
		data() {
			return {
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '二手车预测'
					}
				],
				formSearch: {
				},
				fenlei: [],
				dataList: [],
				total: 1,
				pageSize: 12,
				pageSizes: [],
				totalPage: 1,
				curFenlei: '全部',
				isPlain: false,
				indexQueryCondition: '',
				timeRange: [],
				centerType:false,
				previewImg: '',
				previewVisible: false,
				sortType: 'id',
				sortOrder: 'desc',
				forecastVisible: false,
				forecastImgList: [],
			}
		},
		async created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0){
				this.centerType = true
			}
			this.baseUrl = this.$config.baseUrl;
			if(this.centerType) {
			}
			await this.getFenlei();
			this.getList(1, '全部');
		},
		watch:{
			$route(newValue){
				this.getList(1, newValue.query.homeFenlei);
			}
		},
		computed: {
			role(){
				return localStorage.getItem('frontRole');
			},
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			queryChange(arr){
				for(let x in arr) {
					if(arr[x] == this.role) {
						return true
					}
				}
				return false
			},
			add(path) {
				let query = {}
				if(this.centerType){
					query.centerType = 1
				}
				this.$router.push({path: path,query:query});
			},
			async getFenlei() {
			},
			getList(page, fenlei, ref = '') {
				let params = {
					page,
					limit: this.pageSize,
				};
				let searchWhere = {};
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`usedcarforecast/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.dataList = res.data.data.list;
						this.total = Number(res.data.data.total);
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getList(page);
			},
			prevClick(page) {
				this.getList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getList(1);
			},
			nextClick(page) {
				this.getList(page);
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			toDetail(item) {
				let params = {
					id: item.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/usedcarforecastDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				this.$router.push({path: '/index/center'});
			},
			forecastImgClick(){
				this.forecastImgList = []
				let loading = null
				loading = Loading.service({
					target: this.$refs['roleMenuBox'],
					fullscreen: false,
					text: '图表生成中...'
				})
				this.$http.get('usedcarforecast/forecastimgs').then(res=>{
					if (loading) loading.close()
					if(res.data&&res.data.code==0){
						if(res.data.data) {
							let arr = []
							arr = JSON.parse(JSON.stringify(res.data.data))
							this.$message({
								message: "操作成功！",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.forecastImgList = arr
									this.forecastVisible = true
									this.$forceUpdate()
								}
							});
						}else {
							this.$message({
								message: "请先完成预测！",
								type: "error",
								duration: 1500
							});
						}
					}else {
						this.$message({
							message: "请先完成预测！",
							type: "error",
							duration: 1500
						});
					}
				},err=>{
					if (loading) loading.close()
					this.$message({
						message: "请先完成预测！",
						type: "error",
						duration: 1500
					});
				})
			},

			chapterClick (row){
				let params = {
					refid: row.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chapterusedcarforecast', query: params});
			},
		}
	}
</script>

