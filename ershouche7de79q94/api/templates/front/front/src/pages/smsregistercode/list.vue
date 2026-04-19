<template>
	<div class="front-page">
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">SMS Code Center</span>
				<h1>短信验证码</h1>
				<p>短信验证码页改成更轻的表格工作台，和其他前台管理页面保持一致的玻璃感与留白节奏。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 条记录</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-button v-if="btnAuth('smsregistercode','新增')" type="primary" @click="add('/index/smsregistercodeAdd')">新增验证码</el-button>
			</div>
			<div class="front-toolbar__hint">用于查看手机号、角色与验证码记录。</div>
		</section>

		<section class="front-table-shell">
			<el-table :data="dataList" border>
				<el-table-column prop="mobile" label="手机" min-width="160"></el-table-column>
				<el-table-column prop="role" label="角色" min-width="140"></el-table-column>
				<el-table-column prop="code" label="验证码" min-width="140"></el-table-column>
				<el-table-column label="操作" width="120" fixed="right">
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
						name: '短信验证码'
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
				this.$http.get(`smsregistercode/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
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
				this.$router.push({path: '/index/smsregistercodeDetail', query: params});
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
</style>
