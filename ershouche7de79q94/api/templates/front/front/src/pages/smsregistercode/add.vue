<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">SMS Form</span>
				<h1>{{ ruleForm.id ? '编辑验证码' : '新增验证码' }}</h1>
				<p>短信验证码编辑页也采用统一表单布局，输入区更清爽，视觉上和其他页面完全对齐。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>验证码信息</h2>
					<p>维护手机号、角色与验证码字段。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="手机" prop="mobile"><el-input v-model="ruleForm.mobile" placeholder="手机" clearable :readonly="ro.mobile"></el-input></el-form-item>
					<el-form-item label="角色" prop="role"><el-input v-model="ruleForm.role" placeholder="角色" clearable :readonly="ro.role"></el-input></el-form-item>
					<el-form-item label="验证码" prop="code"><el-input v-model="ruleForm.code" placeholder="验证码" clearable :readonly="ro.code"></el-input></el-form-item>
				</div>

				<div class="front-detail-actions">
					<el-button type="primary" @click="onSubmit(null)">提交信息</el-button>
					<el-button @click="back">取消</el-button>
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
					mobile : false,
					role : false,
					code : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					mobile: '',
					role: '',
					code: '',
				},

				rules: {
					mobile: [
						{ required: true, message: '手机不能为空', trigger: 'blur' },
					],
					role: [
						{ required: true, message: '角色不能为空', trigger: 'blur' },
					],
					code: [
						{ required: true, message: '验证码不能为空', trigger: 'blur' },
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
						if(o=='mobile'){
							this.ruleForm.mobile = obj[o];
							this.ro.mobile = true;
							continue;
						}
						if(o=='role'){
							this.ruleForm.role = obj[o];
							this.ro.role = true;
							continue;
						}
						if(o=='code'){
							this.ruleForm.code = obj[o];
							this.ro.code = true;
							continue;
						}
					}
				}else if(type=='edit'){
					this.info()
				}

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
				await this.$http.get(`smsregistercode/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`smsregistercode/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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

<style lang="scss" scoped>
</style>
