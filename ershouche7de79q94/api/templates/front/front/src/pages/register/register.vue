<template>
	<div class="front-auth-shell">
		<section class="front-auth-shell__intro">
			<div>
				<span class="front-pill" style="background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.18); color: #fff;">Create Account</span>
				<h1>注册后即可开始使用用户端完整能力。</h1>
				<p>注册界面同步切换到新的产品视觉系统，保留短信验证与头像上传功能，但让表单更清楚、更舒展。</p>
			</div>
			<div class="front-auth-shell__metrics">
				<div class="front-auth-shell__metric"><strong>01</strong><span>用户注册</span></div>
				<div class="front-auth-shell__metric"><strong>02</strong><span>短信验证</span></div>
				<div class="front-auth-shell__metric"><strong>03</strong><span>资料完善</span></div>
			</div>
		</section>

		<section class="front-auth-shell__panel">
			<span class="front-pill">Register</span>
			<h2>创建用户账号</h2>
			<p>完成基础信息后即可进入系统浏览车源、查看公告并使用预测功能。</p>

			<el-form v-if="pageFlag == 'register'" ref="registerForm" :model="registerForm" :rules="rules" style="margin-top: 24px;">
				<el-form-item v-if="tableName == 'yonghu'" prop="zhanghao">
					<el-input v-model="registerForm.zhanghao" :readonly="ro.zhanghao" placeholder="请输入账号"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="mima">
					<el-input v-model="registerForm.mima" type="password" placeholder="请输入密码"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="mima2">
					<el-input v-model="registerForm.mima2" type="password" placeholder="请再次输入密码"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="xingming">
					<el-input v-model="registerForm.xingming" :readonly="ro.xingming" placeholder="请输入姓名"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="xingbie">
					<el-select v-model="registerForm.xingbie" placeholder="请选择性别" :disabled="ro.xingbie" style="width: 100%;">
						<el-option v-for="(item, index) in yonghuxingbieOptions" :key="index" :label="item" :value="item"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="nianling">
					<el-input v-model="registerForm.nianling" :readonly="ro.nianling" placeholder="请输入年龄"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="shenfenzheng">
					<el-input v-model="registerForm.shenfenzheng" :readonly="ro.shenfenzheng" placeholder="请输入身份证"></el-input>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="touxiang">
					<file-upload tip="点击上传头像" action="file/upload" :limit="1" :multiple="true" :fileUrls="registerForm.touxiang ? registerForm.touxiang : ''" @change="yonghutouxiangUploadChange"></file-upload>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'" prop="mobile">
					<div style="display: flex; gap: 12px; align-items: center;">
						<el-input v-model="registerForm.mobile" placeholder="请输入手机号"></el-input>
						<el-button v-if="isEndFlag" type="primary" @click="sendsmscode">发送验证码</el-button>
						<el-button v-else disabled>{{ count }}秒后重发</el-button>
					</div>
				</el-form-item>
				<el-form-item v-if="tableName == 'yonghu'">
					<el-input v-model="smscode" placeholder="请输入验证码"></el-input>
				</el-form-item>

				<div class="front-detail-actions">
					<el-button type="primary" @click="submitForm('registerForm')">注册</el-button>
					<router-link to="/login"><el-button>已有账号，去登录</el-button></router-link>
				</div>
			</el-form>
		</section>
	</div>
</template>
<script>
	import 'animate.css';

export default {
    //数据集合
    data() {
		return {
            pageFlag : '',
			tableName: '',
			registerForm: {},
			forgetForm: {},
			rules: {},
			ro: {},
			requiredRules: {},
            yonghuxingbieOptions: [],
            smscode:'',
			//倒计时60s
			count: 60,
			//倒计时定时器
			inter: null,
			//倒计结束标识
			isEndFlag: true,
			indexBgUrl: '',
		}
    },
	mounted() {
		if(this.$route.query.pageFlag=='register'){
			this.tableName = this.$route.query.role;
			if(this.tableName=='yonghu'){
				this.registerForm = {
					zhanghao: '',
					mima: '',
					mima2: '',
					xingming: '',
					xingbie: '',
					touxiang: '',
					nianling: '',
					shenfenzheng: '',
					mobile: '',
				}
				this.ro = {
					zhanghao: false,
					mima: false,
					xingming: false,
					xingbie: false,
					touxiang: false,
					nianling: false,
					shenfenzheng: false,
					mobile: false,
				}
			}
			if ('yonghu' == this.tableName) {
				this.rules.zhanghao = [{ required: true, message: '请输入账号', trigger: 'blur' }];
				this.requiredRules.zhanghao = [{ required: true, message: '请输入账号', trigger: 'blur' }]
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }];
				this.requiredRules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
				this.yonghuxingbieOptions = "男,女".split(',');
				this.rules.touxiang = [{ required: true, message: '请上传头像', trigger: 'blur' }];
				this.requiredRules.touxiang = [{ required: true, message: '请上传头像', trigger: 'blur' }]
				this.rules.shenfenzheng = [{ required: true, validator: this.$validate.isIdCard, trigger: 'blur' }];
				this.rules.mobile = [{ required: true, validator: this.$validate.isMobile, trigger: 'blur' }];
			}
		}
	},
    created() {
		this.$http.get('config/info?name=fRegisterBackgroudImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		this.pageFlag = this.$route.query.pageFlag;
    },
    //方法集合
    methods: {
		changeRules(name){
			if(this.requiredRules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
        // 下二随
		yonghutouxiangUploadChange(fileUrls) {
			this.registerForm.touxiang = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
		},

		// 多级联动参数

		sendsmscode() {
			if(!this.registerForm.mobile){
				this.$message.error(`手机号码不能为空`);
				return
			}
			let mobileF = this.$validate.isMobile2(this.registerForm.mobile);
			if(this.registerForm.mobile&&(!this.$validate.isMobile2(this.registerForm.mobile))){
				this.$message.error(`请输入正确的手机格式`);
				return
			}
			this.isEndFlag = false;
			var _this = this;
			this.inter = window.setInterval(function() {
				_this.count = _this.count - 1;
				if (_this.count <= 0) {
					window.clearInterval(_this.inter);
					_this.isEndFlag = true;
					_this.count=60;
				}
			}, 1000);
			this.$http({
				url: `${this.tableName}/sendsms?mobile=`+this.registerForm.mobile,
				method: "get",
				params: {}
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.$message.success(`发送成功`);
				} else {
					this.$message.error(data.msg)
				}
			});
		},

		submitForm(formName) {
			this.$refs[formName].validate((valid) => {
				if (valid) {
					var url=this.tableName+"/register";
					if(`yonghu` == this.tableName ){
						url=this.tableName+"/register?smscode="+this.smscode;
						if(this.registerForm.mobile&&(!this.$validate.isMobile2(this.registerForm.mobile))){
							this.$message.error(`请输入正确的手机格式`);
							return
						}
					}
					if((!this.smscode) && `yonghu` == this.tableName){
						this.$message.error(`验证码不能为空`);
						return
					}
					if(`yonghu` == this.tableName && this.registerForm.mima!=this.registerForm.mima2) {
						this.$message.error(`两次密码输入不一致`);
						return
					}
					this.$http.post(url, this.registerForm).then(res => {
						if (res.data.code === 0) {
							this.$message({
								message: '注册成功',
								type: 'success',
								duration: 1500,
								onClose: () => {
									this.$router.push('/login');
								}
							});
						} else {
							this.$message.error(res.data.msg);
						}
					});
				} else {
					return false;
				}
			});
		},
		resetForm(formName) {
			this.$refs[formName].resetFields();
		},
    }
}
</script>

