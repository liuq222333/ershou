<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Config Form</span>
				<h1>{{ ruleForm.id ? '编辑配置' : '新增配置' }}</h1>
				<p>配置编辑页采用和前台其他模块一致的轻透表单结构，避免旧模板的重边框感。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>配置内容</h2>
					<p>支持维护名称、值、类型和链接地址。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="名称" prop="name"><el-input v-model="ruleForm.name" placeholder="名称" clearable :readonly="ro.name"></el-input></el-form-item>
					<el-form-item label="类型" prop="type"><el-input v-model.number="ruleForm.type" placeholder="类型" clearable :readonly="ro.type"></el-input></el-form-item>
				</div>

				<el-form-item label="值" v-if="type!='cross' || (type=='cross' && !ro.value)" prop="value">
					<file-upload tip="点击上传值" action="file/upload" :limit="1" :multiple="true" :disabled="ro.value" :fileUrls="ruleForm.value ? ruleForm.value : ''" @change="valueUploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="值" prop="value">
					<img v-if="ruleForm.value && ruleForm.value.substring(0,4)=='http'" class="upload-img" :src="ruleForm.value.split(',')[0]">
					<img v-else-if="ruleForm.value" class="upload-img" :src="baseUrl + ruleForm.value.split(',')[0]">
				</el-form-item>

				<el-form-item label="URL" prop="url">
					<el-input type="textarea" :rows="6" :disabled="ro.url" placeholder="url" v-model="ruleForm.url"></el-input>
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
					name : false,
					value : false,
					url : false,
					type : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					name: '',
					value: '',
					url: '',
					type: '',
				},

				rules: {
					name: [
						{ required: true, message: '名称不能为空', trigger: 'blur' },
					],
					value: [
					],
					url: [
					],
					type: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
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
						if(o=='name'){
							this.ruleForm.name = obj[o];
							this.ro.name = true;
							continue;
						}
						if(o=='value'){
							this.ruleForm.value = obj[o]?obj[o].split(",")[0]:'';
							this.ro.value = true;
							continue;
						}
						if(o=='url'){
							this.ruleForm.url = obj[o];
							this.ro.url = true;
							continue;
						}
						if(o=='type'){
							this.ruleForm.type = obj[o];
							this.ro.type = true;
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
				await this.$http.get(`config/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`config/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			valueUploadChange(fileUrls) {
				this.ruleForm.value = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style lang="scss" scoped>
.upload-img {
	width: 180px;
	height: 120px;
	object-fit: cover;
	border-radius: 18px;
	border: 1px solid rgba(47, 123, 87, 0.12);
	background: #edf3ed;
}
</style>
