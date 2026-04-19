<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Comment Form</span>
				<h1>{{ ruleForm.id ? '回复评论' : '新增评论' }}</h1>
				<p>评论编辑页也切换到统一的表单体系里，减少旧模板的粗边框与密集输入块。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>评论信息</h2>
					<p>支持补充用户昵称、评论内容和管理端回复信息。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="头像" v-if="type!='cross' || (type=='cross' && !ro.avatarurl)" prop="avatarurl">
						<file-upload tip="点击上传头像" action="file/upload" :limit="1" :multiple="true" :disabled="ro.avatarurl" :fileUrls="ruleForm.avatarurl ? ruleForm.avatarurl : ''" @change="avatarurlUploadChange"></file-upload>
					</el-form-item>
					<el-form-item v-else label="头像" prop="avatarurl">
						<img v-if="ruleForm.avatarurl && ruleForm.avatarurl.substring(0,4)=='http'" class="upload-img" :src="ruleForm.avatarurl.split(',')[0]">
						<img v-else-if="ruleForm.avatarurl" class="upload-img" :src="baseUrl + ruleForm.avatarurl.split(',')[0]">
					</el-form-item>
					<el-form-item label="用户名" prop="nickname">
						<el-input v-model="ruleForm.nickname" placeholder="用户名" clearable :readonly="ro.nickname"></el-input>
					</el-form-item>
				</div>

				<el-form-item label="评论内容" prop="content">
					<el-input type="textarea" :rows="6" :disabled="ro.content" placeholder="评论内容" v-model="ruleForm.content"></el-input>
				</el-form-item>
				<el-form-item label="回复内容" prop="reply">
					<el-input type="textarea" :rows="6" :disabled="ro.reply" placeholder="回复内容" v-model="ruleForm.reply"></el-input>
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
					refid : false,
					userid : false,
					avatarurl : false,
					nickname : false,
					content : false,
					reply : false,
					thumbsupnum : false,
					crazilynum : false,
					istop : false,
					tuserids : false,
					cuserids : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					refid: '',
					userid: '',
					avatarurl: '',
					nickname: '',
					content: '',
					reply: '',
					thumbsupnum: '',
					crazilynum: '',
					istop: '',
					tuserids: '',
					cuserids: '',
				},

				rules: {
					refid: [
						{ required: true, message: '关联表id不能为空', trigger: 'blur' },
					],
					userid: [
						{ required: true, message: '用户id不能为空', trigger: 'blur' },
					],
					avatarurl: [
					],
					nickname: [
					],
					content: [
						{ required: true, message: '评论内容不能为空', trigger: 'blur' },
					],
					reply: [
					],
					thumbsupnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					crazilynum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					istop: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					tuserids: [
					],
					cuserids: [
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
						if(o=='refid'){
							this.ruleForm.refid = obj[o];
							this.ro.refid = true;
							continue;
						}
						if(o=='userid'){
							this.ruleForm.userid = obj[o];
							this.ro.userid = true;
							continue;
						}
						if(o=='avatarurl'){
							this.ruleForm.avatarurl = obj[o]?obj[o].split(",")[0]:'';
							this.ro.avatarurl = true;
							continue;
						}
						if(o=='nickname'){
							this.ruleForm.nickname = obj[o];
							this.ro.nickname = true;
							continue;
						}
						if(o=='content'){
							this.ruleForm.content = obj[o];
							this.ro.content = true;
							continue;
						}
						if(o=='reply'){
							this.ruleForm.reply = obj[o];
							this.ro.reply = true;
							continue;
						}
						if(o=='thumbsupnum'){
							this.ruleForm.thumbsupnum = obj[o];
							this.ro.thumbsupnum = true;
							continue;
						}
						if(o=='crazilynum'){
							this.ruleForm.crazilynum = obj[o];
							this.ro.crazilynum = true;
							continue;
						}
						if(o=='istop'){
							this.ruleForm.istop = obj[o];
							this.ro.istop = true;
							continue;
						}
						if(o=='tuserids'){
							this.ruleForm.tuserids = obj[o];
							this.ro.tuserids = true;
							continue;
						}
						if(o=='cuserids'){
							this.ruleForm.cuserids = obj[o];
							this.ro.cuserids = true;
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
				await this.$http.get(`discussusedcar/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`discussusedcar/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			avatarurlUploadChange(fileUrls) {
				this.ruleForm.avatarurl = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style lang="scss" scoped>
.upload-img {
	width: 160px;
	height: 120px;
	object-fit: cover;
	border-radius: 16px;
	border: 1px solid rgba(47, 123, 87, 0.12);
	background: #edf3ed;
}
</style>
