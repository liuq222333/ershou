<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Forecast Form</span>
				<h1>{{ ruleForm.id ? '编辑预测条件' : '新增预测条件' }}</h1>
				<p>预测表单采用与前台其他页面一致的轻透布局，减少旧模板里堆叠的输入块。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>预测参数</h2>
					<p>输入车辆品牌、型号、年份、里程和城市，随后进入预测流程。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="品牌" prop="brand"><el-input v-model="ruleForm.brand" placeholder="品牌" clearable :readonly="ro.brand"></el-input></el-form-item>
					<el-form-item label="型号" prop="model1"><el-input v-model="ruleForm.model1" placeholder="型号" clearable :readonly="ro.model1"></el-input></el-form-item>
					<el-form-item label="年份" prop="vehicleage"><el-input v-model="ruleForm.vehicleage" placeholder="年份" clearable :readonly="ro.vehicleage"></el-input></el-form-item>
					<el-form-item label="里程" prop="kilometer"><el-input-number v-model="ruleForm.kilometer" placeholder="行驶里程" :disabled="ro.kilometer"></el-input-number></el-form-item>
					<el-form-item label="城市" prop="city"><el-input v-model="ruleForm.city" placeholder="所在城市" clearable :readonly="ro.city"></el-input></el-form-item>
				</div>
				<div class="front-detail-actions">
					<el-button type="primary" @click="onSubmit(null)">提交信息</el-button>
					<el-button @click="back()">取消</el-button>
				</div>
			</el-form>
		</section>
	</div>
</template>
<script>
	export default {
		data() {
			return {
				id: '',
				baseUrl: '',
				ro:{
					brand : false,
					model1 : false,
					discountprice : false,
					vehicleage : false,
					kilometer : false,
					city : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					brand: '',
					model1: '',
					discountprice: '',
					vehicleage: '',
					kilometer: '',
					city: '',
				},

				rules: {
					brand: [
					],
					model1: [
					],
					discountprice: [
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					vehicleage: [
					],
					kilometer: [
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					city: [
					],
				},
				centerType: false,
			};
		},
		computed: {
			sessionForm() {
				return JSON.parse(localStorage.getItem('sessionForm'))
			},



		},
		components: {
		},
		created() {
			if(this.$route.query.centerType){
				this.centerType = true
			}
			//this.bg();
			let type = this.$route.query.type ? this.$route.query.type : '';
			this.init(type);
			this.baseUrl = this.$config.baseUrl;
		},
		methods: {
			getMakeZero(s) {
				return s < 10 ? '0' + s : s;
			},
			// 下载
			download(file ){
				window.open(`${file}`)
			},
			// 初始化
			init(type) {
				this.type = type;
				if(type=='cross'){
					var obj = JSON.parse(localStorage.getItem('crossObj'));
					for (var o in obj){
						if(o=='brand'){
							this.ruleForm.brand = obj[o];
							this.ro.brand = true;
							continue;
						}
						if(o=='model1'){
							this.ruleForm.model1 = obj[o];
							this.ro.model1 = true;
							continue;
						}
						if(o=='discountprice'){
							this.ruleForm.discountprice = obj[o];
							this.ro.discountprice = true;
							continue;
						}
						if(o=='vehicleage'){
							this.ruleForm.vehicleage = obj[o];
							this.ro.vehicleage = true;
							continue;
						}
						if(o=='kilometer'){
							this.ruleForm.kilometer = obj[o];
							this.ro.kilometer = true;
							continue;
						}
						if(o=='city'){
							this.ruleForm.city = obj[o];
							this.ro.city = true;
							continue;
						}
					}
				}else if(type=='edit'){
					this.info()
				}
				// 获取用户信息
				this.$http.get(this.userTableName + '/session', {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						var json = res.data.data;
					}
				});

				if (localStorage.getItem('raffleType') && localStorage.getItem('raffleType') != null) {
					localStorage.removeItem('raffleType')
					setTimeout(() => {
						this.onSubmit(null)
					}, 300)
				}
			},

			// 多级联动参数
			// 多级联动参数
			async info() {
				await this.$http.get(`usedcarforecast/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						this.ruleForm = res.data.data;
					}
				});
			},
			// 提交
			async onSubmit(subMitType=null) {
				if(!this.ruleForm.id) {
					delete this.ruleForm.userid
				}
				await this.$refs["ruleForm"].validate(async valid => {
					if(valid) {
						if(this.type=='cross'){
							var statusColumnName = localStorage.getItem('statusColumnName');
							var statusColumnValue = localStorage.getItem('statusColumnValue');
							if(statusColumnName && statusColumnName!='') {
								var obj = JSON.parse(localStorage.getItem('crossObj'));
								if(!statusColumnName.startsWith("[")) {
									for (var o in obj){
										if(o==statusColumnName){
											obj[o] = statusColumnValue;
										}
									}
									var table = localStorage.getItem('crossTable');
									await this.$http.post(table+'/update', obj).then(res => {});
								}
							}
						}

						await this.$http.post(`usedcarforecast/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
							if (res.data.code == 0) {
								await this.$message({
									message: '操作成功',
									type: 'success',
									duration: 1500,
									onClose: () => {
										this.$router.go(-1);
										
									}
								});
							} else {
								this.$message({
									message: res.data.msg,
									type: 'error',
									duration: 1500
								});
							}
						});
					}
				});
			},
			// 获取uuid
			getUUID () {
				return new Date().getTime();
			},
			// 返回
			back() {
				this.$router.go(-1);
			},
		}
	};
</script>

