<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Admin Form</span>
				<h1>{{ ruleForm.id ? '编辑管理员' : '新增管理员' }}</h1>
				<p>管理员账户编辑页也切换到统一表单体系，保留原有新增和更新逻辑。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>管理员信息</h2>
					<p>支持维护用户名、密码、角色和头像。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="用户名" prop="username"><el-input v-model="ruleForm.username" placeholder="用户名" clearable :readonly="ro.username"></el-input></el-form-item>
					<el-form-item label="密码" prop="password"><el-input v-model="ruleForm.password" placeholder="密码" clearable :readonly="ro.password"></el-input></el-form-item>
					<el-form-item label="角色" prop="role"><el-input v-model="ruleForm.role" placeholder="角色" clearable :readonly="ro.role"></el-input></el-form-item>
				</div>

				<el-form-item label="头像" v-if="type!='cross' || (type=='cross' && !ro.image)" prop="image">
					<file-upload tip="点击上传头像" action="file/upload" :limit="1" :multiple="true" :disabled="ro.image" :fileUrls="ruleForm.image ? ruleForm.image : ''" @change="imageUploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="头像" prop="image">
					<img v-if="ruleForm.image && ruleForm.image.substring(0,4)=='http'" class="upload-img" :src="ruleForm.image.split(',')[0]">
					<img v-else-if="ruleForm.image" class="upload-img" :src="baseUrl + ruleForm.image.split(',')[0]">
				</el-form-item>

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
					username : false,
					password : false,
					role : false,
					image : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					username: '',
					password: '',
					role: '',
					image: '',
				},

				rules: {
					username: [
						{ required: true, message: '用户名不能为空', trigger: 'blur' },
					],
					password: [
						{ required: true, message: '密码不能为空', trigger: 'blur' },
					],
					role: [
					],
					image: [
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
						if(o=='username'){
							this.ruleForm.username = obj[o];
							this.ro.username = true;
							continue;
						}
						if(o=='password'){
							this.ruleForm.password = obj[o];
							this.ro.password = true;
							continue;
						}
						if(o=='role'){
							this.ruleForm.role = obj[o];
							this.ro.role = true;
							continue;
						}
						if(o=='image'){
							this.ruleForm.image = obj[o]?obj[o].split(",")[0]:'';
							this.ro.image = true;
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
				await this.$http.get(`users/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`users/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			imageUploadChange(fileUrls) {
				this.ruleForm.image = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style lang="scss" scoped>
.upload-img {
	width: 160px;
	height: 160px;
	object-fit: cover;
	border-radius: 22px;
	border: 1px solid rgba(47, 123, 87, 0.12);
	background: #edf3ed;
}
</style>
