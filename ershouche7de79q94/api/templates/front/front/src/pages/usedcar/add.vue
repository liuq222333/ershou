<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Used Car Form</span>
				<h1>{{ ruleForm.id ? '编辑车源' : '新增车源' }}</h1>
				<p>表单页同步切换到新的前台视觉系统，保留原有字段、上传和提交逻辑。</p>
			</div>
		</header>

		<section class="front-form-shell">
			<div class="front-form-shell__head">
				<div>
					<h2>车辆基础信息</h2>
					<p>填写品牌、型号、价格、年份、里程和城市信息。</p>
				</div>
			</div>

			<el-form class="add-update-form" ref="ruleForm" :model="ruleForm" :rules="rules" label-width="92px">
				<div class="front-form-grid">
					<el-form-item label="品牌" prop="brand"><el-input v-model="ruleForm.brand" placeholder="品牌" clearable :readonly="ro.brand"></el-input></el-form-item>
					<el-form-item label="型号" prop="model1"><el-input v-model="ruleForm.model1" placeholder="型号" clearable :readonly="ro.model1"></el-input></el-form-item>
					<el-form-item label="现价" prop="discountprice"><el-input-number v-model="ruleForm.discountprice" placeholder="现价" :disabled="ro.discountprice"></el-input-number></el-form-item>
					<el-form-item label="已减" prop="originalprice"><el-input-number v-model="ruleForm.originalprice" placeholder="已减" :disabled="ro.originalprice"></el-input-number></el-form-item>
					<el-form-item label="年份" prop="vehicleage"><el-input v-model="ruleForm.vehicleage" placeholder="年份" clearable :readonly="ro.vehicleage"></el-input></el-form-item>
					<el-form-item label="里程" prop="kilometer"><el-input-number v-model="ruleForm.kilometer" placeholder="行驶里程" :disabled="ro.kilometer"></el-input-number></el-form-item>
					<el-form-item label="城市" prop="city"><el-input v-model="ruleForm.city" placeholder="所在城市" clearable :readonly="ro.city"></el-input></el-form-item>
				</div>
				<el-form-item label="图片" v-if="type != 'cross' || (type == 'cross' && !ro.imgurl)" prop="imgurl">
					<file-upload tip="点击上传图片" action="file/upload" :limit="3" :multiple="true" :disabled="ro.imgurl" :fileUrls="ruleForm.imgurl ? ruleForm.imgurl : ''" @change="imgurlUploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-else label="图片" prop="imgurl">
					<img v-if="ruleForm.imgurl.substring(0,4) == 'http'" class="upload-img" v-bind:key="index" :src="ruleForm.imgurl.split(',')[0]">
					<img v-else class="upload-img" v-bind:key="index" v-for="(item,index) in ruleForm.imgurl.split(',')" :src="baseUrl + item">
				</el-form-item>
				<el-form-item label="链接" prop="xqurl">
					<el-input type="textarea" :rows="6" :disabled="ro.xqurl" placeholder="链接" v-model="ruleForm.xqurl"></el-input>
				</el-form-item>
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
					originalprice : false,
					vehicleage : false,
					kilometer : false,
					imgurl : false,
					xqurl : false,
					city : false,
					thumbsupnum : false,
					crazilynum : false,
					clicktime : false,
					clicknum : false,
					discussnum : false,
					storeupnum : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					brand: '',
					model1: '',
					discountprice: '',
					originalprice: '',
					vehicleage: '',
					kilometer: '',
					imgurl: '',
					xqurl: '',
					city: '',
					thumbsupnum: '',
					crazilynum: '',
					clicktime: '',
					clicknum: '',
					discussnum: '',
					storeupnum: '',
				},

				rules: {
					brand: [
					],
					model1: [
					],
					discountprice: [
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					originalprice: [
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					vehicleage: [
					],
					kilometer: [
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					imgurl: [
					],
					xqurl: [
						{ validator: this.$validate.isURL, trigger: 'blur' },
					],
					city: [
					],
					thumbsupnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					crazilynum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					clicktime: [
					],
					clicknum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					discussnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					storeupnum: [
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
						if(o=='originalprice'){
							this.ruleForm.originalprice = obj[o];
							this.ro.originalprice = true;
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
						if(o=='imgurl'){
							this.ruleForm.imgurl = obj[o]?obj[o].split(",")[0]:'';
							this.ro.imgurl = true;
							continue;
						}
						if(o=='xqurl'){
							this.ruleForm.xqurl = obj[o];
							this.ro.xqurl = true;
							continue;
						}
						if(o=='city'){
							this.ruleForm.city = obj[o];
							this.ro.city = true;
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
						if(o=='clicktime'){
							this.ruleForm.clicktime = obj[o];
							this.ro.clicktime = true;
							continue;
						}
						if(o=='clicknum'){
							this.ruleForm.clicknum = obj[o];
							this.ro.clicknum = true;
							continue;
						}
						if(o=='discussnum'){
							this.ruleForm.discussnum = obj[o];
							this.ro.discussnum = true;
							continue;
						}
						if(o=='storeupnum'){
							this.ruleForm.storeupnum = obj[o];
							this.ro.storeupnum = true;
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
				await this.$http.get(`usedcar/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
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

						await this.$http.post(`usedcar/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
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
			imgurlUploadChange(fileUrls) {
				this.ruleForm.imgurl = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

