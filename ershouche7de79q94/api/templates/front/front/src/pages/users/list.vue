<template>
	<div class="front-page">
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Admin Directory</span>
				<h1>管理员列表</h1>
				<p>管理员页面也同步成当前这套留白更充足的前台风格，头像、角色和账户层级更清晰。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 位管理员</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-button v-if="btnAuth('users','新增')" type="primary" @click="add('/index/usersAdd')">新增管理员</el-button>
			</div>
			<div class="front-toolbar__hint">管理员账户与头像在这里统一维护。</div>
		</section>

		<section class="front-section">
			<div v-if="dataList.length" class="front-admin-grid">
				<article v-for="(item, index) in dataList" :key="index" class="front-admin-card front-clickable" @click.stop="toDetail(item)">
					<div class="front-admin-card__avatar">
						<img :src="item.image ? (item.image.substring(0,4)=='http' ? item.image.split(',')[0] : baseUrl + item.image.split(',')[0]) : require('@/assets/avator.png')" alt="avatar">
					</div>
					<div>
						<h3>{{ item.username || '管理员' }}</h3>
						<p>{{ item.role || '系统角色' }}</p>
						<div class="front-admin-card__footer">
							<span>账户已创建</span>
							<span>点击查看详情</span>
						</div>
					</div>
				</article>
			</div>
			<div v-else class="front-empty">暂无管理员数据</div>

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
						name: '管理员'
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
				this.$http.get(`users/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
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
				this.$router.push({path: '/index/usersDetail', query: params});
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
.front-admin-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 18px;
}

.front-admin-card {
	display: grid;
	grid-template-columns: 88px 1fr;
	gap: 16px;
	padding: 18px;
	border-radius: 20px;
	background: rgba(255, 255, 255, 0.72);
	border: 1px solid rgba(47, 123, 87, 0.08);
}

.front-admin-card__avatar {
	width: 88px;
	height: 88px;
	border-radius: 24px;
	overflow: hidden;
	background: #e2ece3;
}

.front-admin-card__avatar img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.front-admin-card h3 {
	margin: 4px 0 6px;
	font-size: 22px;
	line-height: 1.1;
}

.front-admin-card p {
	margin: 0;
	color: var(--front-text-soft);
	font-size: 13px;
}

.front-admin-card__footer {
	display: flex;
	justify-content: space-between;
	gap: 12px;
	margin-top: 18px;
	color: var(--front-text-soft);
	font-size: 12px;
}

@media (max-width: 1100px) {
	.front-admin-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 760px) {
	.front-admin-grid {
		grid-template-columns: 1fr;
	}
}
</style>
