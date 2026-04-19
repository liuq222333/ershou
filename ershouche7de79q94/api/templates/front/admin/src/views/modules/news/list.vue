  
<template>
	<div class="main-content news-list-page">
		<div class="news-page-head">
			<div class="news-page-title-block">
				<h2 class="news-page-title">公告管理</h2>
				<p class="news-page-subtitle">统一维护公告内容、封面图片与发布信息</p>
			</div>
			<div class="news-page-metrics">
				<span class="metric-badge">总记录 {{ totalPage }}</span>
				<span class="metric-badge">已选择 {{ dataListSelections.length }}</span>
			</div>
		</div>
		<!-- 列表页 -->
		<template v-if="showFlag ">
			<el-form class="center-form-pv" :style='{"borderRadius":"0","width":"100%","margin":"0"}' :inline="true" :model="searchForm">
				<el-row :style='{"padding":"0","boxShadow":"nnoe","borderColor":"#00000050","margin":"0","borderRadius":"0px","flexWrap":"wrap","borderWidth":"0","background":"none","display":"flex","width":"100%","position":"relative","borderStyle":"solid"}' >
					<div class="query-field" :style='{"margin":"0 1% 20px 0","display":"flex"}'>
						<label :style='{"margin":"0 10px 0 0","whiteSpace":"nowrap","color":"#333333","display":"inline-block","lineHeight":"41px","fontSize":"16px","fontWeight":"500","height":"41px"}' class="item-label">标题</label>
						<el-input v-model="searchForm.title" placeholder="标题" @keydown.enter.native="search()" clearable></el-input>
					</div>
					<el-button class="search" type="success" @click="search()">
						<span class="icon iconfont icon-fangdajing01" :style='{"margin":"0 0px","fontSize":"16px","color":"#fff","display":"none","height":"40px"}'></span>
						查询
					</el-button>
				</el-row>

				<el-row class="actions" :style='{"padding":"0","boxShadow":"none","margin":"0px 0 0px -4px","borderRadius":"8px","flexWrap":"wrap","background":"none","display":"flex","width":"calc(100% + 8px)","justifyContent":"0"}'>
					<el-button class="add" v-if="isAuth('news','新增')" type="success" @click="addOrUpdateHandler()">
						<span class="icon iconfont icon-tianjia17" :style='{"margin":"0 0px","fontSize":"16px","color":"#883434","display":"none","height":"auto"}'></span>
						添加
					</el-button>
					<el-button class="del" v-if="isAuth('news','删除')" :disabled="dataListSelections.length?false:true" type="danger" @click="deleteHandler()">
						<span class="icon iconfont icon-shanchu6" :style='{"margin":"0 0px","fontSize":"16px","color":"#883434","display":"none","height":"auto"}'></span>
						删除
					</el-button>


				</el-row>
			</el-form>
			<div class="table-shell" :style='{"width":"100%","padding":"0","margin":"20px 0 0 0","borderRadius":"8px","background":"#fff","borderWidth":"0"}'>
				<el-table class="tables"
					:stripe='false'
					:style='{"padding":"0","borderColor":"#e7e8fc","borderRadius":"0","color":"#212D3F","borderWidth":"0px 0 0 0px","background":"none","width":"100%","borderStyle":"solid"}' 
					:border='false'
					v-if="isAuth('news','查看')"
					:data="dataList"
					v-loading="dataListLoading"
					@selection-change="selectionChangeHandler">
					<el-table-column :resizable='true' type="selection" align="center" width="50"></el-table-column>
					<el-table-column :resizable='true' :sortable='true' label="序号" type="index" width="50" />
					<el-table-column :resizable='true' :sortable='true'
												prop="title"
						label="标题">
						<template slot-scope="scope">
							{{scope.row.title}}
						</template>
					</el-table-column>
					<el-table-column  :resizable='true' prop="picture" width="200" label="图片">
						<template slot-scope="scope">
							<div v-if="scope.row.picture">
								<img class="news-thumb" v-if="scope.row.picture.substring(0,4)=='http'&&scope.row.picture.split(',w').length>1" :src="scope.row.picture" @click="imgPreView(scope.row.picture)">
								<img class="news-thumb" v-else-if="scope.row.picture.substring(0,4)=='http'" :src="scope.row.picture.split(',')[0]" @click="imgPreView(scope.row.picture.split(',')[0])">
								<img class="news-thumb" v-else :src="$base.url+scope.row.picture.split(',')[0]" @click="imgPreView($base.url+scope.row.picture.split(',')[0])">
							</div>
							<div v-else>无图片</div>
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="name"
						label="发布人">
						<template slot-scope="scope">
							{{scope.row.name}}
						</template>
					</el-table-column>
					<el-table-column width="300" label="操作">
						<template slot-scope="scope">
							<el-button class="view" v-if=" isAuth('news','查看')" type="success" @click="addOrUpdateHandler(scope.row.id,'info')">
								<span class="icon iconfont icon-chakan2" :style='{"margin":"0 0px","fontSize":"14px","color":"#333","display":"none","height":"40px"}'></span>
								详情
							</el-button>
							<el-button class="edit" v-if=" isAuth('news','修改') " type="success" @click="addOrUpdateHandler(scope.row.id)">
								<span class="icon iconfont icon-xiugai13" :style='{"margin":"0 0px","fontSize":"14px","color":"rgba(255, 140, 0, 1)","display":"none","height":"40px"}'></span>
								修改
							</el-button>




							<el-button class="del" v-if="isAuth('news','删除')" type="primary" @click="deleteHandler(scope.row.id)">
								<span class="icon iconfont icon-shanchu6" :style='{"margin":"0 0px","fontSize":"14px","color":"rgba(220, 38, 38, 1)","display":"none","height":"40px"}'></span>
								删除
							</el-button>
						</template>
					</el-table-column>
				</el-table>
			</div>
			<el-pagination
				class="list-pagination"
				@size-change="sizeChangeHandle"
				@current-change="currentChangeHandle"
				:current-page="pageIndex"
				background
				:page-sizes="[10, 50, 100, 200]"
				:page-size="pageSize"
				:layout="layouts.join()"
				:total="totalPage"
				prev-text="< "
				next-text="> "
				:hide-on-single-page="false"
				:style='{"padding":"0","margin":"20px 0 0","whiteSpace":"nowrap","color":"#333","display":"flex","width":"100%","fontWeight":"500","justifyContent":"flex-end"}'
			></el-pagination>
		</template>
		<!-- 添加/修改页面  将父组件的search方法传递给子组件-->
		<add-or-update v-if="addOrUpdateFlag" :parent="this" ref="addOrUpdate"></add-or-update>





		<el-dialog class="preview-dialog" title="预览图" :visible.sync="previewVisible" width="50%">
			<img class="preview-image" :src="previewImg" alt="">
		</el-dialog>
	</div>
</template>

<script>
	import * as echarts from 'echarts'
	import chinaJson from "@/components/echarts/china.json";
	import axios from 'axios';
	import AddOrUpdate from "./add-or-update";
	import {
		Loading
	} from 'element-ui';
	export default {
		data() {
			return {
				indexQueryCondition: '',
				searchForm: {
					key: ""
				},
				form:{},
				dataList: [],
				pageIndex: 1,
				pageSize: 10,
				totalPage: 0,
				dataListLoading: false,
				dataListSelections: [],
				showFlag: true,
				addOrUpdateFlag:false,
				layouts: ["total","prev","pager","next","sizes","jumper"],
				previewImg: '',
				previewVisible: false,
			};
		},
		created() {
			if(this.statType) {
				return false
			}
			this.init();
			this.getDataList();
		},
		mounted() {
		},
		watch: {
		},
		filters: {
			htmlfilter: function (val) {
				return val.replace(/<[^>]*>/g).replace(/undefined/g,'');
			}
		},
		computed: {
			tablename(){
				return this.$storage.get('sessionTable')
			},
			role(){
				return this.$storage.get('role')
			},
		},
		components: {
			AddOrUpdate,
		},
		methods: {
			queryChange(arr){
				for(let x in arr) {
					if(arr[x] == this.role) {
						return true
					}
				}
				return false
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
				
			},
			init () {
			},
			search() {
				this.pageIndex = 1;
				this.getDataList();
			},

			// 获取数据列表
			getDataList() {
				this.dataListLoading = true;
				let params = {
					page: this.pageIndex,
					limit: this.pageSize,
					sort: 'id',
					order: 'desc',
				}
				if(this.searchForm.title!='' && this.searchForm.title!=undefined){
					params['title'] = '%' + this.searchForm.title + '%'
				}
				let user = JSON.parse(this.$storage.getObj('userForm'))
				this.$http({
					url: "news/page",
					method: "get",
					params: params
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.dataList = data.data.list;
						this.totalPage = data.data.total;
					} else {
						this.dataList = [];
						this.totalPage = 0;
					}
					this.dataListLoading = false;
				});
			},
			// 每页数
			sizeChangeHandle(val) {
				this.pageSize = val;
				this.pageIndex = 1;
				this.getDataList();
			},
			// 当前页
			currentChangeHandle(val) {
				this.pageIndex = val;
				this.getDataList();
			},
			// 多选
			selectionChangeHandler(val) {
				this.dataListSelections = val;
			},
			// 添加/修改
			addOrUpdateHandler(id,type) {
				this.showFlag = false;
				this.addOrUpdateFlag = true;
				this.crossAddOrUpdateFlag = false;
				if(type!='info'&&type!='msg'){
					type = 'else';
				}
				this.$nextTick(() => {
					this.$refs.addOrUpdate.init(id,type );
				});
			},
			// 删除
			async deleteHandler(id ) {
				var ids = id? [Number(id)]: this.dataListSelections.map(item => {
					return Number(item.id);
				});
				await this.$confirm(`确定进行[${id ? "删除" : "批量删除"}]操作?`, "提示", {
					confirmButtonText: "确定",
					cancelButtonText: "取消",
					type: "warning"
				}).then(async () => {
					await this.$http({
						url: "news/delete",
						method: "post",
						data: ids
					}).then(async ({ data }) => {
						if (data && data.code === 0) {
							this.$message({
								message: "操作成功",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.search();
								}
							});
			
						} else {
							this.$message.error(data.msg);
						}
					});
				});
			},


		}

	};
</script>
<style lang="scss" scoped>
	.news-list-page {
		--hw-red: #cf0a2c;
		--hw-red-strong: #b90525;
		--hw-text: #1f2329;
		--hw-sub: #6b7280;
		--hw-line: #e7e9ef;
		--hw-bg: #f4f6fa;
		padding: 22px !important;
		background:
			radial-gradient(circle at 0% 0%, rgba(207, 10, 44, 0.06) 0%, transparent 34%),
			radial-gradient(circle at 100% 100%, rgba(207, 10, 44, 0.04) 0%, transparent 30%),
			var(--hw-bg) !important;
		font-family: "HarmonyOS Sans SC", "PingFang SC", "Segoe UI", sans-serif;
	}

	.news-page-head {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 16px;
		margin-bottom: 14px;
	}

	.news-page-title {
		margin: 0;
		color: var(--hw-text);
		font-size: 28px;
		line-height: 1.18;
		font-weight: 700;
		letter-spacing: 0.01em;
	}

	.news-page-subtitle {
		margin: 8px 0 0;
		color: var(--hw-sub);
		font-size: 14px;
	}

	.news-page-metrics {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.metric-badge {
		padding: 7px 12px;
		border: 1px solid var(--hw-line);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.88);
		color: #505a6a;
		font-size: 12px;
		font-weight: 600;
	}

	.center-form-pv {
		padding: 16px 18px 10px !important;
		border: 1px solid var(--hw-line) !important;
		border-radius: 16px !important;
		background: rgba(255, 255, 255, 0.95) !important;
		box-shadow: 0 8px 26px rgba(31, 35, 41, 0.06) !important;
	}

	.query-field {
		display: flex !important;
		align-items: center;
		gap: 8px;
		margin: 0 12px 12px 0 !important;
	}

	.query-field .item-label {
		min-width: 40px;
		margin: 0 !important;
		color: #374151 !important;
		font-size: 13px !important;
		font-weight: 600 !important;
		line-height: 40px !important;
		height: 40px !important;
	}

	.center-form-pv .el-input,
	.center-form-pv .el-select {
		width: 240px !important;
	}

	.center-form-pv .el-input ::v-deep .el-input__inner,
	.center-form-pv .el-select ::v-deep .el-input__inner {
		height: 40px !important;
		border: 1px solid #d8dce5 !important;
		border-radius: 10px !important;
		background: #fff !important;
		color: var(--hw-text) !important;
		font-size: 13px !important;
		box-shadow: none !important;
	}

	.center-form-pv .el-input ::v-deep .el-input__inner:focus,
	.center-form-pv .el-select ::v-deep .el-input__inner:focus {
		border-color: var(--hw-red) !important;
		box-shadow: 0 0 0 3px rgba(207, 10, 44, 0.12) !important;
	}

	.center-form-pv .search {
		height: 40px !important;
		padding: 0 18px !important;
		margin: 0 0 12px !important;
		border: 0 !important;
		border-radius: 10px !important;
		background: linear-gradient(135deg, var(--hw-red) 0%, var(--hw-red-strong) 100%) !important;
		color: #fff !important;
		font-size: 13px !important;
		font-weight: 600 !important;
		box-shadow: 0 8px 18px rgba(207, 10, 44, 0.24) !important;
	}

	.center-form-pv .actions {
		margin: 0 !important;
		padding-top: 2px !important;
		width: 100% !important;
		display: flex !important;
		flex-wrap: wrap !important;
	}

	.center-form-pv .actions .add,
	.center-form-pv .actions .del {
		height: 38px !important;
		padding: 0 14px !important;
		margin: 0 8px 8px 0 !important;
		border-radius: 10px !important;
		font-size: 12px !important;
		font-weight: 600 !important;
		box-shadow: none !important;
	}

	.center-form-pv .actions .add {
		border: 0 !important;
		background: var(--hw-red) !important;
		color: #fff !important;
	}

	.center-form-pv .actions .add:hover {
		background: var(--hw-red-strong) !important;
	}

	.center-form-pv .actions .del {
		border: 1px solid rgba(207, 10, 44, 0.28) !important;
		background: #fff !important;
		color: var(--hw-red) !important;
	}

	.center-form-pv .actions .del:hover {
		border-color: var(--hw-red) !important;
		background: rgba(207, 10, 44, 0.06) !important;
	}

	.table-shell {
		margin-top: 14px !important;
		border: 1px solid var(--hw-line) !important;
		border-radius: 16px !important;
		background: #fff !important;
		box-shadow: 0 8px 24px rgba(31, 35, 41, 0.06) !important;
		overflow: hidden;
	}

	.tables {
		border-radius: 16px !important;
	}

	.tables ::v-deep .el-table__header-wrapper thead tr th {
		padding: 12px 0 !important;
		background: #f8f9fc !important;
		border-bottom: 1px solid var(--hw-line) !important;
	}

	.tables ::v-deep .el-table__header-wrapper thead tr th .cell {
		padding-left: 12px !important;
		color: #2f3440 !important;
		font-size: 13px !important;
		font-weight: 700 !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td {
		padding: 9px 0 !important;
		border-bottom: 1px solid #edf0f5 !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .cell {
		padding-left: 12px !important;
		color: #2f3745 !important;
		font-size: 13px !important;
		line-height: 22px !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr:hover td {
		background: rgba(207, 10, 44, 0.045) !important;
	}

	.news-thumb {
		display: block;
		width: 64px;
		height: 64px;
		border-radius: 12px;
		object-fit: cover;
		border: 1px solid #eceff4;
		cursor: pointer;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .view,
	.tables ::v-deep .el-table__body-wrapper tbody tr td .edit,
	.tables ::v-deep .el-table__body-wrapper tbody tr td .del {
		height: 30px !important;
		padding: 0 12px !important;
		margin: 0 6px 6px 0 !important;
		border-radius: 8px !important;
		font-size: 12px !important;
		font-weight: 600 !important;
		box-shadow: none !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .view {
		border: 1px solid #d8deea !important;
		background: #fff !important;
		color: #4b5563 !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .view:hover {
		border-color: #9eabc1 !important;
		background: #f8fafc !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .edit {
		border: 1px solid #c8d7f3 !important;
		background: #edf3ff !important;
		color: #2b5fa5 !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .edit:hover {
		border-color: #9fbce7 !important;
		background: #e3ecfe !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .del {
		border: 1px solid #f3ccd3 !important;
		background: #fff3f5 !important;
		color: #bf1239 !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .del:hover {
		border-color: #e9a8b4 !important;
		background: #ffecef !important;
	}

	.list-pagination {
		margin-top: 20px !important;
	}

	.list-pagination ::v-deep .el-pagination__total {
		color: #667085 !important;
		font-size: 13px !important;
		line-height: 34px !important;
	}

	.list-pagination ::v-deep .btn-prev,
	.list-pagination ::v-deep .btn-next,
	.list-pagination ::v-deep .el-pager li {
		min-width: 34px !important;
		height: 34px !important;
		line-height: 34px !important;
		border-radius: 8px !important;
		border: 1px solid #d9e0ec !important;
		background: #fff !important;
		color: #4a5568 !important;
		margin: 0 4px !important;
	}

	.list-pagination ::v-deep .el-pager li.active {
		border-color: var(--hw-red) !important;
		background: var(--hw-red) !important;
		color: #fff !important;
	}

	.list-pagination ::v-deep .el-pagination__sizes .el-input__inner,
	.list-pagination ::v-deep .el-pagination__jump .el-input__inner {
		height: 34px !important;
		line-height: 34px !important;
		border-radius: 8px !important;
		border: 1px solid #d9e0ec !important;
		box-shadow: none !important;
	}

	.list-pagination ::v-deep .el-pagination__sizes .el-input {
		width: 112px !important;
	}

	.preview-dialog ::v-deep .el-dialog {
		border-radius: 16px !important;
		overflow: hidden;
	}

	.preview-dialog ::v-deep .el-dialog__header {
		padding: 16px 20px !important;
		border-bottom: 1px solid #edf0f5;
		background: #f8fafc;
	}

	.preview-dialog ::v-deep .el-dialog__title {
		color: #1f2937;
		font-size: 15px;
		font-weight: 700;
	}

	.preview-dialog ::v-deep .el-dialog__body {
		padding: 16px 20px 20px !important;
	}

	.preview-image {
		display: block;
		width: 100%;
		max-height: 70vh;
		object-fit: contain;
		border-radius: 12px;
		background: #fff;
	}

	@media (max-width: 1400px) {
		.news-page-head {
			align-items: flex-start;
			flex-direction: column;
		}

		.news-page-metrics {
			justify-content: flex-start;
		}
	}

	@media (max-width: 992px) {
		.news-list-page {
			padding: 16px !important;
		}

		.news-page-title {
			font-size: 24px;
		}

		.center-form-pv .el-input,
		.center-form-pv .el-select {
			width: 100% !important;
		}

		.query-field {
			width: 100%;
		}
	}
</style>
