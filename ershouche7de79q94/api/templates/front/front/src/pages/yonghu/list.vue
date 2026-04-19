<template>
	<div class="front-page">
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">User Directory</span>
				<h1>用户列表</h1>
				<p>把用户页从旧的生成器卡片样式重构成更接近管理端的目录视图，保留筛选和新增逻辑。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 位用户</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-input v-model="formSearch.zhanghao" class="front-toolbar__search" placeholder="搜索账号" clearable @keyup.enter.native="getList(1, curFenlei)"></el-input>
				<el-input v-model="formSearch.xingming" class="front-toolbar__search" placeholder="搜索姓名" clearable @keyup.enter.native="getList(1, curFenlei)"></el-input>
				<el-select v-model="formSearch.xingbie" placeholder="性别" clearable>
					<el-option v-for="(item, index) in xingbieOptions" :key="index" :label="item" :value="item"></el-option>
				</el-select>
				<el-button type="primary" @click="getList(1, curFenlei)">搜索</el-button>
				<el-button v-if="btnAuth('yonghu','新增')" @click="add('/index/yonghuAdd')">新增用户</el-button>
			</div>
			<div class="front-toolbar__hint">以更轻的目录卡片浏览用户基本资料与联系方式。</div>
		</section>

		<section class="front-section">
			<div v-if="dataList.length" class="front-user-grid">
				<article v-for="(item, index) in dataList" :key="index" class="front-user-card front-clickable" @click.stop="toDetail(item)">
					<div class="front-user-card__avatar">
						<img :src="item.touxiang ? (item.touxiang.substring(0,4) == 'http' ? item.touxiang.split(',')[0] : baseUrl + item.touxiang.split(',')[0]) : require('@/assets/avator.png')" alt="avatar">
					</div>
					<div class="front-user-card__body">
						<div class="front-user-card__head">
							<div>
								<h3>{{ item.xingming || item.zhanghao || '未命名用户' }}</h3>
								<p>@{{ item.zhanghao || '--' }}</p>
							</div>
							<span class="front-pill front-user-card__tag">{{ item.xingbie || '未设置' }}</span>
						</div>
						<div class="front-user-card__facts">
							<div><small>手机号</small><strong>{{ item.mobile || '--' }}</strong></div>
							<div><small>年龄</small><strong>{{ item.nianling || '--' }}</strong></div>
							<div><small>身份证</small><strong>{{ item.shenfenzheng || '--' }}</strong></div>
						</div>
						<div class="front-user-card__footer">
							<span>{{ item.addtime ? item.addtime.split(' ')[0] : '最近更新' }}</span>
							<span>点击查看详情</span>
						</div>
					</div>
				</article>
			</div>
			<div v-else class="front-empty">暂无匹配用户</div>

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
						name: '用户'
					}
				],
				formSearch: {
					zhanghao: '',
					xingming: '',
					xingbie: '',
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
				xingbieOptions: [],
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
			this.xingbieOptions = '男,女'.split(',');
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
				if (this.formSearch.zhanghao != '') searchWhere.zhanghao = '%' + this.formSearch.zhanghao + '%';
				if (this.formSearch.xingming != '') searchWhere.xingming = '%' + this.formSearch.xingming + '%';
				if (this.formSearch.xingbie != '') searchWhere.xingbie = this.formSearch.xingbie;
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`yonghu/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
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
				this.$router.push({path: '/index/yonghuDetail', query: params});
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

			chapterClick (row){
				let params = {
					refid: row.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chapteryonghu', query: params});
			},
		}
	}
</script>

<style lang="scss" scoped>
.front-user-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 18px;
}

.front-user-card {
	display: grid;
	grid-template-columns: 108px 1fr;
	gap: 18px;
	padding: 20px;
	border-radius: 20px;
	background: rgba(255, 255, 255, 0.72);
	border: 1px solid rgba(47, 123, 87, 0.08);
	transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.front-user-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 18px 40px rgba(29, 42, 34, 0.1);
}

.front-user-card__avatar {
	width: 108px;
	height: 108px;
	border-radius: 26px;
	overflow: hidden;
	background: #e2ece3;
}

.front-user-card__avatar img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.front-user-card__head {
	display: flex;
	justify-content: space-between;
	gap: 12px;
	align-items: flex-start;
}

.front-user-card__head h3 {
	margin: 0;
	font-size: 24px;
	line-height: 1.1;
}

.front-user-card__head p {
	margin: 6px 0 0;
	color: var(--front-text-soft);
	font-size: 13px;
}

.front-user-card__tag {
	padding: 7px 12px;
	font-size: 11px;
}

.front-user-card__facts {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 10px;
	margin-top: 16px;
}

.front-user-card__facts div {
	padding: 12px 14px;
	border-radius: 14px;
	background: rgba(47, 123, 87, 0.06);
}

.front-user-card__facts small {
	display: block;
	color: var(--front-text-soft);
	font-size: 11px;
}

.front-user-card__facts strong {
	display: block;
	margin-top: 6px;
	font-size: 13px;
	word-break: break-all;
}

.front-user-card__footer {
	display: flex;
	justify-content: space-between;
	gap: 12px;
	margin-top: 16px;
	color: var(--front-text-soft);
	font-size: 12px;
}

@media (max-width: 900px) {
	.front-user-grid {
		grid-template-columns: 1fr;
	}

	.front-user-card {
		grid-template-columns: 1fr;
	}
}
</style>
