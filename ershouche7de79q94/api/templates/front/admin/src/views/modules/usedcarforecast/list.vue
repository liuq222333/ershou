  
<template>
	<div class="main-content usedcarforecast-list-page">
		<div class="forecast-page-head">
			<div class="forecast-page-title-block">
				<h2 class="forecast-page-title">二手车预测管理</h2>
				<p class="forecast-page-subtitle">统一管理预测样本，支持批量维护与可视化图表生成</p>
			</div>
			<div class="forecast-page-metrics">
				<span class="metric-badge">总记录 {{ totalPage }}</span>
				<span class="metric-badge">已选择 {{ dataListSelections.length }}</span>
				<span class="metric-badge">当前页 {{ pageIndex }}</span>
			</div>
		</div>
		<!-- 列表页 -->
		<template v-if="showFlag ">
			<el-form class="center-form-pv" :style='{"borderRadius":"0","width":"100%","margin":"0"}' :inline="true" :model="searchForm">
				<el-row class="query-row" :style='{"padding":"0","boxShadow":"nnoe","borderColor":"#00000050","margin":"0","borderRadius":"0px","flexWrap":"wrap","borderWidth":"0","background":"none","display":"flex","width":"100%","position":"relative","borderStyle":"solid"}' >
					<div class="query-placeholder">预测样本默认按最新数据排序，可直接执行新增、预测与图表查看操作</div>
				</el-row>

				<el-row class="actions" :style='{"padding":"0","boxShadow":"none","margin":"0px 0 0px -4px","borderRadius":"8px","flexWrap":"wrap","background":"none","display":"flex","width":"calc(100% + 8px)","justifyContent":"0"}'>
					<el-button class="btn18" type="success" @click="refreshClick()">
						刷新
					</el-button>
					<el-button class="add" v-if="isAuth('usedcarforecast','新增')" type="success" @click="addOrUpdateHandler()">
						<span class="icon iconfont icon-tianjia17" :style='{"margin":"0 0px","fontSize":"16px","color":"#883434","display":"none","height":"auto"}'></span>
						添加
					</el-button>
					<el-button class="del" v-if="isAuth('usedcarforecast','删除')" :disabled="dataListSelections.length?false:true" type="danger" @click="deleteHandler()">
						<span class="icon iconfont icon-shanchu6" :style='{"margin":"0 0px","fontSize":"16px","color":"#883434","display":"none","height":"auto"}'></span>
						删除
					</el-button>


					<el-button v-if="isAuth('usedcarforecast','预测')" class="btn18" type="success" @click="forecastImgClick()">
						<span class="icon iconfont icon-shuju17" :style='{"margin":"0 0px","fontSize":"16px","color":"#883434","display":"none","height":"auto"}'></span>
						 预测  图表
					</el-button>
				</el-row>
			</el-form>
			<div class="table-shell" :style='{"width":"100%","padding":"0","margin":"20px 0 0 0","borderRadius":"8px","background":"#fff","borderWidth":"0"}'>
				<el-table class="tables"
					:stripe='false'
					:style='{"padding":"0","borderColor":"#e7e8fc","borderRadius":"0","color":"#212D3F","borderWidth":"0px 0 0 0px","background":"none","width":"100%","borderStyle":"solid"}' 
					:border='false'
					v-if="isAuth('usedcarforecast','查看')"
					:data="dataList"
					v-loading="dataListLoading"
					@selection-change="selectionChangeHandler">
					<el-table-column :resizable='true' type="selection" align="center" width="50"></el-table-column>
					<el-table-column :resizable='true' :sortable='true' label="序号" type="index" width="50" />
					<el-table-column :resizable='true' :sortable='true'
												prop="brand"
						label="品牌">
						<template slot-scope="scope">
							{{scope.row.brand}}
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="model1"
						label="型号">
						<template slot-scope="scope">
							{{scope.row.model1}}
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="discountprice"
						label="预测价">
						<template slot-scope="scope">
							{{scope.row.discountprice}}
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="vehicleage"
						label="年份">
						<template slot-scope="scope">
							{{scope.row.vehicleage}}
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="kilometer"
						label="行驶里程">
						<template slot-scope="scope">
							{{scope.row.kilometer}}
						</template>
					</el-table-column>
					<el-table-column :resizable='true' :sortable='true'
												prop="city"
						label="所在城市">
						<template slot-scope="scope">
							{{scope.row.city}}
						</template>
					</el-table-column>
					<el-table-column width="380" label="操作">
						<template slot-scope="scope">
							<div class="op-wrap">
								<el-button class="view" v-if=" isAuth('usedcarforecast','查看')" type="success" @click="addOrUpdateHandler(scope.row.id,'info')">
									详情
								</el-button>
								<el-button class="edit" v-if=" isAuth('usedcarforecast','修改') " type="success" @click="addOrUpdateHandler(scope.row.id)">
									修改
								</el-button>
								<el-button class="del" v-if="isAuth('usedcarforecast','删除')" type="primary" @click="deleteHandler(scope.row.id)">
									删除
								</el-button>
								<el-button v-if="isAuth('usedcarforecast','预测')" class="btn8" type="success" @click="forecastClick(scope.row)">
									预测
								</el-button>
								<el-button class="ai-btn" type="warning" @click="aiAnalyzeClick(scope.row)">
									AI 分析
								</el-button>
							</div>
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





		<el-dialog class="forecast-dialog" title="可视化图表" :visible.sync="forecastVisible" width="50%">
			<div class="forecast-image-grid">
				<el-image class="forecast-image" v-for="item in forecastImgList" :key="item" :src="$base.url + item" lazy></el-image>
			</div>
		</el-dialog>

		<el-dialog class="ai-dialog" title="AI 智能分析" :visible.sync="aiVisible" width="620px" :before-close="aiDialogClose">
			<div class="ai-analyze-body">
				<div v-if="aiLoading && !aiResult" class="ai-loading">
					<i class="el-icon-loading"></i> AI 正在分析中...
				</div>
				<div class="ai-result-text" v-html="aiResultHtml"></div>
			</div>
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
				forecastVisible: false,
				forecastImgList: [],
				aiVisible: false,
				aiLoading: false,
				aiResult: '',
				aiAbortController: null,
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
			aiResultHtml(){
				if(!this.aiResult) return ''
				return this.aiResult
					.replace(/\[Request interrupted by user\]/g, '')
					.replace(/^#{1,6}\s*/gm, '')
					.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
					.replace(/\n/g, '<br>')
			},
		},
		components: {
			AddOrUpdate,
		},
		methods: {
			refreshClick(){
				this.searchForm = {}
				this.search()
			},
			queryChange(arr){
				for(let x in arr) {
					if(arr[x] == this.role) {
						return true
					}
				}
				return false
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
				let user = JSON.parse(this.$storage.getObj('userForm'))
				this.$http({
					url: "usedcarforecast/page",
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
						url: "usedcarforecast/delete",
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
						id: row.id
					}
					for(let x in arr){
						brr[arr[x]] = row[arr[x]]
					}
					this.$http({
						url: 'usedcarforecast/forecast',
						method: 'post',
						data: brr
					}).then(res=>{
						if(res.data&&res.data.code==0){
							if (loading) loading.close()
							this.$message({
								message: "数据预测完成！",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.getDataList()
								}
							});
						}else {
							if (loading) loading.close()
							this.$message.error(res.data.msg)
						}
					},err=>{
						if (loading) loading.close()
						this.$message.error(err.data.msg)
					})
				})
			},
			async aiAnalyzeClick(row) {
				this.aiResult = ''
				this.aiLoading = true
				this.aiVisible = true

				if (this.aiAbortController) {
					this.aiAbortController.abort()
				}
				this.aiAbortController = new AbortController()

				let params = {}
				let arr = 'brand,model1,vehicleage,kilometer,city'.split(',')
				for (let x of arr) {
					params[x] = row[x] || ''
				}

				try {
					const token = this.$storage.get('Token')
					const resp = await fetch('/ershouche7de79q94/usedcarforecast/ai_analyze', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json; charset=utf-8',
							'Token': token
						},
						body: JSON.stringify(params),
						signal: this.aiAbortController.signal
					})

					if (!resp.ok) {
						this.aiResult = '请求失败，状态码：' + resp.status
						this.aiLoading = false
						return
					}

					const reader = resp.body.getReader()
					const decoder = new TextDecoder()
					let buffer = ''

					while (true) {
						const { done, value } = await reader.read()
						if (done) break

						buffer += decoder.decode(value, { stream: true })
						let lines = buffer.split('\n')
						buffer = lines.pop()

						for (let line of lines) {
							if (!line.startsWith('data: ')) continue
							let dataStr = line.slice(6)
							if (dataStr.trim() === '[DONE]') {
								this.aiLoading = false
								return
							}
							try {
								let obj = JSON.parse(dataStr)
								if (obj.error) {
									this.aiResult += '\n[Error] ' + obj.error
									this.aiLoading = false
									return
								} else if (obj.content) {
									this.aiResult += obj.content
								}
							} catch(e) {}
						}
					}
					this.aiLoading = false
				} catch (err) {
					if (err.name !== 'AbortError') {
						this.aiLoading = false
						if (!this.aiResult) {
							this.aiResult = '分析请求失败，请检查网络或 API Key 配置。'
						}
					}
				}
			},

			aiDialogClose(done) {
				if (this.aiAbortController) {
					this.aiAbortController.abort()
					this.aiAbortController = null
				}
				this.aiLoading = false
				done()
			},

			forecastImgClick(){
				this.forecastImgList = []
				let loading = null
				loading = Loading.service({
					target: this.$refs['roleMenuBox'],
					fullscreen: false,
					text: '图表生成中...'
				})
				this.$http({
					url: 'usedcarforecast/forecastimgs',
					method: 'get',
				}).then(res=>{
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
		}

	};
</script>
<style lang="scss" scoped>
	.usedcarforecast-list-page {
		--hw-red: #cf0a2c;
		--hw-red-strong: #b90525;
		--hw-text: #1f2329;
		--hw-sub: #6b7280;
		--hw-line: #e7e9ef;
		--hw-bg: #f4f6fa;
		padding: 22px !important;
		background:
			radial-gradient(circle at 0% 0%, rgba(207, 10, 44, 0.06) 0%, transparent 35%),
			radial-gradient(circle at 100% 100%, rgba(207, 10, 44, 0.04) 0%, transparent 32%),
			var(--hw-bg) !important;
		font-family: "HarmonyOS Sans SC", "PingFang SC", "Segoe UI", sans-serif;
	}

	.forecast-page-head {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 16px;
		margin-bottom: 14px;
	}

	.forecast-page-title {
		margin: 0;
		color: var(--hw-text);
		font-size: 28px;
		line-height: 1.18;
		font-weight: 700;
		letter-spacing: 0.01em;
	}

	.forecast-page-subtitle {
		margin: 8px 0 0;
		color: var(--hw-sub);
		font-size: 14px;
	}

	.forecast-page-metrics {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		justify-content: flex-end;
	}

	.metric-badge {
		padding: 7px 12px;
		border: 1px solid var(--hw-line);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.9);
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

	.query-row {
		margin: 0 0 8px !important;
	}

	.query-placeholder {
		display: flex;
		align-items: center;
		min-height: 32px;
		padding: 0 2px;
		color: #687280;
		font-size: 13px;
		font-weight: 500;
		letter-spacing: 0.01em;
	}

	.center-form-pv .actions {
		margin: 0 !important;
		padding-top: 2px !important;
		width: 100% !important;
		display: flex !important;
		flex-wrap: wrap !important;
	}

	.center-form-pv .actions .add,
	.center-form-pv .actions .del,
	.center-form-pv .actions .btn18 {
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

	.center-form-pv .actions .btn18 {
		border: 1px solid #d6deeb !important;
		background: #fff !important;
		color: #4a5870 !important;
	}

	.center-form-pv .actions .btn18:hover {
		border-color: #8ea1c1 !important;
		color: #334155 !important;
		background: #f7f9fd !important;
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

	.tables ::v-deep .el-table__body-wrapper tbody tr td .view,
	.tables ::v-deep .el-table__body-wrapper tbody tr td .edit,
	.tables ::v-deep .el-table__body-wrapper tbody tr td .del,
	.tables ::v-deep .el-table__body-wrapper tbody tr td .btn8 {
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

	.tables ::v-deep .el-table__body-wrapper tbody tr td .btn8 {
		border: 0 !important;
		background: linear-gradient(135deg, var(--hw-red) 0%, var(--hw-red-strong) 100%) !important;
		color: #fff !important;
		box-shadow: 0 6px 16px rgba(207, 10, 44, 0.22) !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .btn8:hover {
		filter: brightness(0.96);
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

	.forecast-dialog ::v-deep .el-dialog {
		border-radius: 16px !important;
		overflow: hidden;
	}

	.forecast-dialog ::v-deep .el-dialog__header {
		padding: 16px 20px !important;
		border-bottom: 1px solid #edf0f5;
		background: #f8fafc;
	}

	.forecast-dialog ::v-deep .el-dialog__title {
		color: #1f2937;
		font-size: 15px;
		font-weight: 700;
	}

	.forecast-dialog ::v-deep .el-dialog__body {
		padding: 16px 20px 20px !important;
	}

	.forecast-image-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(220px, 1fr));
		gap: 12px;
	}

	.forecast-image-grid .forecast-image {
		display: block;
		width: 100%;
		border-radius: 12px;
		overflow: hidden;
		border: 1px solid #edf0f5;
		background: #fff;
	}

	.forecast-image-grid .forecast-image ::v-deep .el-image__inner {
		display: block;
		width: 100%;
		height: 198px;
		object-fit: cover;
	}

	@media (max-width: 1400px) {
		.forecast-page-head {
			align-items: flex-start;
			flex-direction: column;
		}

		.forecast-page-metrics {
			justify-content: flex-start;
		}

		.tables ::v-deep .el-table__body-wrapper tbody tr td .cell {
			padding-left: 10px !important;
		}
	}

	.op-wrap {
		display: flex !important;
		flex-wrap: wrap !important;
		align-items: center !important;
		gap: 6px;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .ai-btn {
		height: 30px !important;
		padding: 0 12px !important;
		margin: 0 6px 6px 0 !important;
		border-radius: 8px !important;
		font-size: 12px !important;
		font-weight: 600 !important;
		border: 0 !important;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
		color: #fff !important;
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
	}

	.tables ::v-deep .el-table__body-wrapper tbody tr td .ai-btn:hover {
		filter: brightness(1.08);
	}

	.ai-dialog ::v-deep .el-dialog {
		border-radius: 16px !important;
		overflow: hidden;
	}

	.ai-dialog ::v-deep .el-dialog__header {
		padding: 16px 20px !important;
		border-bottom: 1px solid #edf0f5;
		background: linear-gradient(135deg, #f0f0ff 0%, #f8f6ff 100%);
	}

	.ai-dialog ::v-deep .el-dialog__title {
		color: #4338ca;
		font-size: 15px;
		font-weight: 700;
	}

	.ai-dialog ::v-deep .el-dialog__body {
		padding: 20px !important;
		max-height: 60vh;
		overflow-y: auto;
	}

	.ai-analyze-body {
		font-size: 14px;
		line-height: 1.8;
		color: #374151;
	}

	.ai-loading {
		color: #6366f1;
		font-size: 14px;
		padding: 8px 0;
	}

	.ai-result-text {
		white-space: pre-wrap;
		word-break: break-word;
	}

	.ai-result-text ::v-deep strong {
		color: #1f2937;
		font-weight: 700;
	}

	@media (max-width: 992px) {
		.usedcarforecast-list-page {
			padding: 16px !important;
		}

		.forecast-page-title {
			font-size: 24px;
		}

		.forecast-image-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
