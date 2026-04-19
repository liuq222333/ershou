<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">System Content</span>
				<h1>{{ ruleForm.id ? '编辑系统简介' : '新增系统简介' }}</h1>
				<p>把系统简介的图文编辑页也统一到当前前台工作区风格，减少旧式表单边框感。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>图文内容</h2>
					<p>支持配置标题、副标题、三张图片和正文内容。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="标题" prop="title"><el-input v-model="ruleForm.title" placeholder="标题" clearable :readonly="ro.title"></el-input></el-form-item>
					<el-form-item label="副标题" prop="subtitle"><el-input v-model="ruleForm.subtitle" placeholder="副标题" clearable :readonly="ro.subtitle"></el-input></el-form-item>
				</div>

				<el-form-item label="图片1" v-if="type!='cross' || (type=='cross' && !ro.picture1)" prop="picture1">
					<file-upload tip="点击上传图片1" action="file/upload" :limit="1" :multiple="true" :disabled="ro.picture1" :fileUrls="ruleForm.picture1 ? ruleForm.picture1 : ''" @change="picture1UploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="图片1" prop="picture1">
					<img v-if="ruleForm.picture1 && ruleForm.picture1.substring(0,4)=='http'" class="upload-img" :src="ruleForm.picture1.split(',')[0]">
					<img v-else-if="ruleForm.picture1" class="upload-img" :src="baseUrl + ruleForm.picture1.split(',')[0]">
				</el-form-item>

				<el-form-item label="图片2" v-if="type!='cross' || (type=='cross' && !ro.picture2)" prop="picture2">
					<file-upload tip="点击上传图片2" action="file/upload" :limit="1" :multiple="true" :disabled="ro.picture2" :fileUrls="ruleForm.picture2 ? ruleForm.picture2 : ''" @change="picture2UploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="图片2" prop="picture2">
					<img v-if="ruleForm.picture2 && ruleForm.picture2.substring(0,4)=='http'" class="upload-img" :src="ruleForm.picture2.split(',')[0]">
					<img v-else-if="ruleForm.picture2" class="upload-img" :src="baseUrl + ruleForm.picture2.split(',')[0]">
				</el-form-item>

				<el-form-item label="图片3" v-if="type!='cross' || (type=='cross' && !ro.picture3)" prop="picture3">
					<file-upload tip="点击上传图片3" action="file/upload" :limit="1" :multiple="true" :disabled="ro.picture3" :fileUrls="ruleForm.picture3 ? ruleForm.picture3 : ''" @change="picture3UploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="图片3" prop="picture3">
					<img v-if="ruleForm.picture3 && ruleForm.picture3.substring(0,4)=='http'" class="upload-img" :src="ruleForm.picture3.split(',')[0]">
					<img v-else-if="ruleForm.picture3" class="upload-img" :src="baseUrl + ruleForm.picture3.split(',')[0]">
				</el-form-item>

				<el-form-item label="内容" prop="content">
					<editor v-model="ruleForm.content" class="editor" myQuillEditor="content" action="file/upload"></editor>
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
					title : false,
					subtitle : false,
					content : false,
					picture1 : false,
					picture2 : false,
					picture3 : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					title: '',
					subtitle: '',
					content: '',
					picture1: '',
					picture2: '',
					picture3: '',
				},

				rules: {
					title: [
						{ required: true, message: '标题不能为空', trigger: 'blur' },
					],
					subtitle: [
					],
					content: [
						{ required: true, message: '内容不能为空', trigger: 'blur' },
					],
					picture1: [
					],
					picture2: [
					],
					picture3: [
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
						if(o=='title'){
							this.ruleForm.title = obj[o];
							this.ro.title = true;
							continue;
						}
						if(o=='subtitle'){
							this.ruleForm.subtitle = obj[o];
							this.ro.subtitle = true;
							continue;
						}
						if(o=='content'){
							this.ruleForm.content = obj[o];
							this.ro.content = true;
							continue;
						}
						if(o=='picture1'){
							this.ruleForm.picture1 = obj[o]?obj[o].split(",")[0]:'';
							this.ro.picture1 = true;
							continue;
						}
						if(o=='picture2'){
							this.ruleForm.picture2 = obj[o]?obj[o].split(",")[0]:'';
							this.ro.picture2 = true;
							continue;
						}
						if(o=='picture3'){
							this.ruleForm.picture3 = obj[o]?obj[o].split(",")[0]:'';
							this.ro.picture3 = true;
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
				await this.$http.get(`systemintro/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`systemintro/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			picture1UploadChange(fileUrls) {
				this.ruleForm.picture1 = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
			picture2UploadChange(fileUrls) {
				this.ruleForm.picture2 = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
			picture3UploadChange(fileUrls) {
				this.ruleForm.picture3 = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style lang="scss" scoped>
.upload-img {
	width: 220px;
	height: 140px;
	object-fit: cover;
	border-radius: 18px;
	border: 1px solid rgba(47, 123, 87, 0.12);
	background: #edf3ed;
}

.front-form-shell {
	::v-deep .editor {
		border-radius: 18px;
		overflow: hidden;
		border: 1px solid rgba(47, 123, 87, 0.1);
	}

	::v-deep .ql-container {
		min-height: 220px;
		font-family: inherit;
	}

	::v-deep .ql-editor {
		min-height: 220px;
	}
}
</style>
