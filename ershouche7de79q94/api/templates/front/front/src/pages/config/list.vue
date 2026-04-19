<template>
	<div class="front-page">
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Config Center</span>
				<h1>配置管理</h1>
				<p>配置列表也切换到统一的工作台风格，信息更规整，图片值和链接字段更容易扫描。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 项配置</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-button v-if="btnAuth('config','新增')" type="primary" @click="add('/index/configAdd')">新增配置</el-button>
			</div>
			<div class="front-toolbar__hint">统一管理图片值、链接和配置类型。</div>
		</section>

		<section class="front-table-shell">
			<el-table :data="dataList" border>
				<el-table-column prop="name" label="名称" min-width="160"></el-table-column>
				<el-table-column label="值" min-width="180">
					<template slot-scope="scope">
						<div v-if="scope.row.value && (scope.row.value.substring(0,4)=='http' || scope.row.value.indexOf('/') !== -1)" class="front-config-thumb" @click="imgPreView(scope.row.value.substring(0,4)=='http' ? (scope.row.value.split(',w').length>1 ? scope.row.value : scope.row.value.split(',')[0]) : baseUrl + scope.row.value.split(',')[0]">
							<img :src="scope.row.value.substring(0,4)=='http' ? (scope.row.value.split(',w').length>1 ? scope.row.value : scope.row.value.split(',')[0]) : baseUrl + scope.row.value.split(',')[0]" alt="config value">
						</div>
						<span v-else>{{ scope.row.value || '--' }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="url" label="URL" min-width="220" show-overflow-tooltip></el-table-column>
				<el-table-column prop="type" label="类型" width="120"></el-table-column>
				<el-table-column label="操作" min-width="120" fixed="right">
					<template slot-scope="scope">
						<el-button size="mini" type="primary" @click="toDetail(scope.row)">查看</el-button>
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
	</div>
</template>

<script>
	import axios from 'axios';
	export default {
		//数据集合
		data() {
			return {
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '配置管理'
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
				this.$http.get(`config/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
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
			sortClick(type){
				if(this.sortType==type){
					if(this.sortOrder == 'desc'){
						this.sortOrder = 'asc'
					}else{
						this.sortOrder = 'desc'
					}
				}else{
					this.sortType = type
					this.sortOrder = 'desc'
				}
				this.getList(1, '全部')
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
				this.$router.push({path: '/index/configDetail', query: params});
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

		}
	}
</script>

<style lang="scss" scoped>
.front-config-thumb {
	width: 90px;
	height: 90px;
	border-radius: 18px;
	overflow: hidden;
	background: #e6efe6;
	cursor: pointer;
}

.front-config-thumb img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}
</style>
