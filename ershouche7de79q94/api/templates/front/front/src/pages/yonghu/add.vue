<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">User Form</span>
				<h1>{{ ruleForm.id ? '编辑用户' : '新增用户' }}</h1>
				<p>用户资料编辑页同步切换到新的前台表单样式，保持和个人中心、用户列表一致的视觉语言。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>用户资料</h2>
					<p>支持维护账号、密码、头像以及实名信息。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="账号" prop="zhanghao"><el-input v-model="ruleForm.zhanghao" placeholder="账号" clearable :readonly="ro.zhanghao"></el-input></el-form-item>
					<el-form-item label="密码" prop="mima"><el-input v-model="ruleForm.mima" placeholder="密码" clearable :readonly="ro.mima"></el-input></el-form-item>
					<el-form-item label="姓名" prop="xingming"><el-input v-model="ruleForm.xingming" placeholder="姓名" clearable :readonly="ro.xingming"></el-input></el-form-item>
					<el-form-item label="性别" prop="xingbie">
						<el-select v-model="ruleForm.xingbie" placeholder="请选择性别" :disabled="ro.xingbie" filterable>
							<el-option v-for="(item,index) in xingbieOptions" :key="index" :label="item" :value="item"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="年龄" prop="nianling"><el-input v-model="ruleForm.nianling" placeholder="年龄" clearable :readonly="ro.nianling"></el-input></el-form-item>
					<el-form-item label="手机号" prop="mobile"><el-input v-model="ruleForm.mobile" placeholder="手机号" clearable :readonly="ro.mobile"></el-input></el-form-item>
				</div>

				<el-form-item label="头像" v-if="type!='cross' || (type=='cross' && !ro.touxiang)" prop="touxiang">
					<file-upload tip="点击上传头像" action="file/upload" :limit="1" :multiple="true" :disabled="ro.touxiang" :fileUrls="ruleForm.touxiang ? ruleForm.touxiang : ''" @change="touxiangUploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="头像" prop="touxiang">
					<img v-if="ruleForm.touxiang && ruleForm.touxiang.substring(0,4)=='http'" class="upload-img" :src="ruleForm.touxiang.split(',')[0]">
					<img v-else-if="ruleForm.touxiang" class="upload-img" :src="baseUrl + ruleForm.touxiang.split(',')[0]">
				</el-form-item>

				<el-form-item label="身份证" prop="shenfenzheng"><el-input v-model="ruleForm.shenfenzheng" placeholder="身份证" clearable :readonly="ro.shenfenzheng"></el-input></el-form-item>

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
					zhanghao : false,
					mima : false,
					xingming : false,
					xingbie : false,
					touxiang : false,
					nianling : false,
					shenfenzheng : false,
					mobile : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					zhanghao: '',
					mima: '',
					xingming: '',
					xingbie: '',
					touxiang: '',
					nianling: '',
					shenfenzheng: '',
					mobile: '',
				},
				xingbieOptions: [],

				rules: {
					zhanghao: [
						{ required: true, message: '账号不能为空', trigger: 'blur' },
					],
					mima: [
						{ required: true, message: '密码不能为空', trigger: 'blur' },
					],
					xingming: [
					],
					xingbie: [
					],
					touxiang: [
						{ required: true, message: '头像不能为空', trigger: 'blur' },
					],
					nianling: [
					],
					shenfenzheng: [
						{ validator: this.$validate.isIdCard, trigger: 'blur' },
					],
					mobile: [
						{ validator: this.$validate.isMobile, trigger: 'blur' },
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
						if(o=='zhanghao'){
							this.ruleForm.zhanghao = obj[o];
							this.ro.zhanghao = true;
							continue;
						}
						if(o=='mima'){
							this.ruleForm.mima = obj[o];
							this.ro.mima = true;
							continue;
						}
						if(o=='xingming'){
							this.ruleForm.xingming = obj[o];
							this.ro.xingming = true;
							continue;
						}
						if(o=='xingbie'){
							this.ruleForm.xingbie = obj[o];
							this.ro.xingbie = true;
							continue;
						}
						if(o=='touxiang'){
							this.ruleForm.touxiang = obj[o]?obj[o].split(",")[0]:'';
							this.ro.touxiang = true;
							continue;
						}
						if(o=='nianling'){
							this.ruleForm.nianling = obj[o];
							this.ro.nianling = true;
							continue;
						}
						if(o=='shenfenzheng'){
							this.ruleForm.shenfenzheng = obj[o];
							this.ro.shenfenzheng = true;
							continue;
						}
						if(o=='mobile'){
							this.ruleForm.mobile = obj[o];
							this.ro.mobile = true;
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
				this.xingbieOptions = "男,女".split(',')

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
				await this.$http.get(`yonghu/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`yonghu/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			touxiangUploadChange(fileUrls) {
				this.ruleForm.touxiang = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
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
