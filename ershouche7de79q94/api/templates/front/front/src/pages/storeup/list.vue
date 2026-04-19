<template>
	<div class="front-page">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回个人中心</el-button>
		</div>

		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">User Collection</span>
				<h1>{{ pageTitle }}</h1>
				<p>收藏、点赞和评论页统一到同一套留白充足的浏览界面里，不再使用散乱的模板布局。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">共 {{ total }} 条内容</span>
			</div>
		</header>

		<section v-if="storeupType != 81" class="front-toolbar">
			<div class="front-toolbar__group">
				<el-input v-model="formSearch.name" class="front-toolbar__search" placeholder="搜索名称" clearable @keyup.enter.native="getStoreupList(1)"></el-input>
				<el-button type="primary" @click="getStoreupList(1)">查询</el-button>
			</div>
		</section>

		<section v-if="storeupType != 81" class="front-section">
			<div v-if="storeupList.length" class="front-collection-grid">
				<article v-for="(item, index) in storeupList" :key="index" class="front-collection-card front-clickable" @click="toDetail(item)">
					<div class="front-collection-card__media">
						<el-image v-if="item.picture && item.picture.substr(0,4)=='http'" :src="item.picture" fit="cover"></el-image>
						<el-image v-else-if="item.picture && item.picture.substr(0,4)!='http'" :src="baseUrl + item.picture" fit="cover"></el-image>
						<img v-else :src="require('@/assets/chapter.jpg')" alt="cover">
					</div>
					<h3>{{ item.name }}</h3>
					<p>{{ item.remark || '点击进入详情页查看原始内容。' }}</p>
					<div class="front-car-card__footer" style="margin-top: 16px;">
						<span class="front-muted">{{ item.addtime ? item.addtime.split(' ')[0] : '已收录' }}</span>
						<el-button type="danger" size="mini" @click.stop="delClick(item)">删除</el-button>
					</div>
				</article>
			</div>
			<div v-else class="front-empty">当前没有相关内容</div>

			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				:page-sizes="pageSizes"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				@current-change="curChange"
				@prev-click="prevClick"
				@size-change="sizeChange"
				@next-click="nextClick"
			></el-pagination>
		</section>

		<section v-else class="front-table-shell">
			<el-table class="front-table" :border="false" :data="storeupList">
				<el-table-column prop="content" label="评论内容" show-overflow-tooltip>
					<template slot-scope="scope">
						<span class="ql-snow ql-editor" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" v-html="scope.row.content"></span>
					</template>
				</el-table-column>
				<el-table-column prop="reply" label="回复内容" show-overflow-tooltip>
					<template slot-scope="scope">
						<span class="ql-snow ql-editor" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" v-html="scope.row.reply"></span>
					</template>
				</el-table-column>
				<el-table-column width="220" label="操作">
					<template slot-scope="scope">
						<el-button type="primary" size="mini" @click="toDetail(scope.row)">查看</el-button>
						<el-button type="danger" size="mini" @click="delClick(scope.row)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</section>
	</div>
</template>
<script>
	import config from '@/config/config'
	export default {
		data() {
			return {
				layouts: '',
				baseUrl: config.baseUrl,
				formSearch: {
					name: ''
				},
				storeupType: 1,
				storeupList: [],
				total: 1,
				pageSize: 8,
				pageSizes: [],
				totalPage: 1
			}
		},
		computed: {
			pageTitle() {
				if (String(this.storeupType) === '21') { return '我的点赞' }
				if (String(this.storeupType) === '81') { return '我的评论' }
				return '我的收藏'
			}
		},
		created() {
			this.storeupType = localStorage.getItem('storeupType');
			this.getStoreupList(1);
		},
		methods: {
			backClick() {
				this.$router.push('/index/center')
			},
			getStoreupList(page) {
				if(this.storeupType==81) {
					this.$http.get('comment/list', {}).then(res => {
						this.storeupList = res.data.data;
						this.total = (res.data.data || []).length;
					})
					return false
				}
				let params = {page, limit: this.pageSize, type: this.storeupType, userid: Number(localStorage.getItem('frontUserid')),sort:"addtime",order:"desc"};
				let searchWhere = {
				};
				if (this.formSearch.name != '') searchWhere.name = '%' + this.formSearch.name + '%';
				this.$http.get('storeup/list', {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.storeupList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getStoreupList(page);
			},
			prevClick(page) {
				this.getStoreupList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getStoreupList(1);
			},
			nextClick(page) {
				this.getStoreupList(page);
			},
			toDetail(item) {
				let params = {
					id: item.refid,
					storeupType: 1,
				}
				if(this.storeupType == 81) {
					params.discussId = item.id
				}
				this.$router.push({path: `/index/${item.tablename}Detail`, query: params});
			},
			async delClick(row){
				await this.$confirm(`是否删除此记录？`) .then(async _ => {
					if(this.storeupType==81) {
						await this.$http.post(`discuss${row.tablename}/delete`, [row.id]).then(async res => {
							if (res.data.code == 0) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.discussnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
								this.$message({
									type: 'success',
									message: '删除成功!',
									duration: 1500,
									onClose: () => {
										this.getStoreupList(1);
									}
								});
							}
						});
						return false
					}
					this.$http.post('storeup/delete', [row.id]).then(async res => {
						if (res.data.code == 0) {
							if(this.storeupType==1) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.storeupnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
							}
							if(this.storeupType==21) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.thumbsupnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
							}
							this.$message({
								type: 'success',
								message: '删除成功!',
								duration: 1500,
								onClose: () => {
									this.getStoreupList(1);
								}
							});
						}
					});
				}).catch(_ => {});
			},
		}
	}
</script>

