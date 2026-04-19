<template>
	<div class="front-page">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Comment Workspace</span>
				<h1>车辆评论</h1>
				<p>把评论管理从旧式表格容器里抽出来，改成和当前管理端一致的轻透工作台样式，操作更集中。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 条评论</span>
				<span class="front-pill">排序 {{ sortType }} / {{ sortOrder }}</span>
			</div>
		</header>

		<section class="front-toolbar">
			<div class="front-toolbar__group">
				<el-button v-if="btnAuth('discussusedcar','新增')" type="primary" @click="add('/index/discussusedcarAdd')">新增评论</el-button>
			</div>
			<div class="front-toolbar__hint">支持查看、回复、置顶和删除评论，保留原有权限判断与接口。</div>
		</section>

		<section class="front-table-shell">
			<el-table :data="dataList" border>
				<el-table-column prop="nickname" label="用户名" min-width="140" show-overflow-tooltip></el-table-column>
				<el-table-column label="评论内容" min-width="240" show-overflow-tooltip>
					<template slot-scope="scope">
						<span>{{ scope.row.content ? scope.row.content.replace(/<[^>]*>/g, '') : '--' }}</span>
					</template>
				</el-table-column>
				<el-table-column label="回复内容" min-width="220" show-overflow-tooltip>
					<template slot-scope="scope">
						<span>{{ scope.row.reply ? scope.row.reply.replace(/<[^>]*>/g, '') : '待回复' }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="istop" label="置顶" width="110">
					<template slot-scope="scope">
						<el-switch
							v-model="scope.row.istop"
							:width="52"
							:active-value="1"
							:inactive-value="0"
							active-color="#2f7b57"
							inactive-color="#c7d3cb"
							@change="(e) => discussistopChange(e, scope.row)"
						></el-switch>
					</template>
				</el-table-column>
				<el-table-column label="操作" min-width="260" fixed="right">
					<template slot-scope="scope">
						<el-button size="mini" type="primary" @click="toDetail(scope.row)">查看</el-button>
						<el-button size="mini" @click="editClick(scope.row)">回复</el-button>
						<el-button size="mini" type="danger" @click="delClick(scope.row)" v-if="btnAuth('usedcar','删除评论')">删除</el-button>
						<el-button size="mini" type="warning" @click="discussClick(scope.row)" v-if="btnAuth('discussusedcar','查看评论')">查看评论</el-button>
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
						name: '二手车'
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
				params.refid = this.$route.query.refid
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`discussusedcar/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
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
				this.$router.push({path: '/index/discussusedcarDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				history.back()
			},

			discussClick (row){
				let params = {
					refid: row.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/discussdiscussusedcar', query: params});
			},
			editClick (row){
				this.$router.push(`/index/discussusedcarAdd?type=edit&&id=${row.id}`);
			},
			async delClick (row){
				await this.$confirm('是否删除此评论？') .then(_ => {
					this.$http.post('discussusedcar/delete', [row.id]).then(async res => {
						if (res.data.code == 0) {
							await this.$http.get('usedcar/info/' + row.refid).then(async rs=>{
								rs.data.data.discussnum--
								await this.$http.post('usedcar/update',rs.data.data).then(rs2=>{})
							})
							this.$message({
								message: "操作成功",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.getList(1, '全部');
								}
							});
						}
					});
				}).catch(_ => {});
			},
			discussistopChange(e,row){
				this.$http.post('discussusedcar/update',row).then(res=>{})
			},
		}
	}
</script>

<style lang="scss" scoped>
</style>
