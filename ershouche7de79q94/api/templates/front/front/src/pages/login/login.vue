<template>
	<div class="front-auth-shell">
		<section class="front-auth-shell__intro">
			<div>
				<span class="front-pill" style="background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.18); color: #fff;">Used Car Platform</span>
				<h1>登录后继续查看车源、预测与公告。</h1>
				<p>用户端界面已经切换成更统一的绿色产品风格，登录入口也同步重构为更清晰、更有留白的双栏结构。</p>
			</div>
			<div class="front-auth-shell__metrics">
				<div class="front-auth-shell__metric"><strong>01</strong><span>车源浏览</span></div>
				<div class="front-auth-shell__metric"><strong>02</strong><span>价格预测</span></div>
				<div class="front-auth-shell__metric"><strong>03</strong><span>公告阅读</span></div>
			</div>
		</section>

		<section class="front-auth-shell__panel">
			<span class="front-pill">Sign In</span>
			<h2>欢迎回来</h2>
			<p>支持账号密码登录，也可以切换到手机验证码登录。</p>

			<div class="front-auth-shell__switch">
				<el-button :type="loginType == 1 ? 'primary' : 'default'" @click="loginType = 1">账号登录</el-button>
				<el-button :type="loginType == 4 ? 'primary' : 'default'" @click="loginType = 4; loginForm.tableName = ''; role = ''">手机登录</el-button>
			</div>

			<el-form ref="loginForm" :model="loginForm" :rules="rules" style="margin-top: 24px;">
				<template v-if="loginType == 1">
					<el-form-item prop="username">
						<el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
					</el-form-item>
					<el-form-item prop="password">
						<el-input :type="showPassword ? 'text' : 'password'" v-model="loginForm.password" placeholder="请输入密码">
							<template slot="suffix">
								<i class="el-input__icon el-icon-view front-clickable" @click="showPassword = !showPassword"></i>
							</template>
						</el-input>
					</el-form-item>
				</template>

				<template v-else>
					<el-form-item>
						<el-input v-model="phone" placeholder="请输入手机号"></el-input>
					</el-form-item>
					<el-form-item>
						<div style="display: flex; gap: 12px; align-items: center;">
							<el-input v-model="phonecode" placeholder="请输入手机验证码"></el-input>
							<el-button v-if="isEndFlag" @click="phoneClick">发送验证码</el-button>
							<el-button v-else disabled>{{ emailText }}</el-button>
						</div>
					</el-form-item>
				</template>

				<el-form-item v-if="roles.length > 1 && loginType == 1">
					<el-radio-group v-model="loginForm.tableName">
						<el-radio v-for="(item, index) in roles" :key="index" :label="item.tableName" @change.native="getCurrentRow(item)">{{ item.roleName }}</el-radio>
					</el-radio-group>
				</el-form-item>

				<el-form-item v-if="phoneroles.length > 1 && loginType == 4">
					<el-radio-group v-model="loginForm.tableName">
						<el-radio v-for="(item, index) in phoneroles" :key="index" :label="item.tableName" @change.native="getCurrentRow(item)">{{ item.roleName }}</el-radio>
					</el-radio-group>
				</el-form-item>

				<div class="front-detail-actions" style="margin-top: 8px;">
					<el-button type="primary" @click="submitForm('loginForm')">登录</el-button>
					<el-button @click="$router.push('/index/home')">返回首页</el-button>
				</div>
			</el-form>

			<div class="front-auth-shell__footer">
				<div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-top: 10px;">
					<router-link v-for="(item, index) in roles2" :key="index" :to="{ path: '/register', query: { role: item.tableName, pageFlag: 'register' } }">注册{{ item.roleName.replace('注册', '') }}</router-link>
					<span v-if="loginType == 4" class="front-clickable" @click="passwordLoginChange">切换回账号登录</span>
				</div>
			</div>
		</section>
	</div>
</template>
<script>
	import 'animate.css';
import menu from '@/config/menu'
export default {
	//数据集合
	data() {
		return {
            baseUrl: this.$config.baseUrl,
            loginType: 1,
			roleMenus: [],
			loginForm: {
				username: '',
				password: '',
				tableName: '',
			},
			phone: '',
			phonecode: '',
			phoneroles: [
				{
					tableName: 'yonghu',
					roleName: '用户'
				},
			],
			// 倒计时时间
			count: 60,
			// 倒计时定时器
			inter: null,
			// 倒计时是否结束
			isEndFlag: true,
			role: '',
			roles: [],
			roles2: [],
			rules: {
				username: [
					{ required: true, message: '请输入账号', trigger: 'blur' }
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' }
				]
			},
			codes: [{
				num: 1,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 2,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 3,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 4,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}],
			flag: false,
			verifyCheck2: false,
			showPassword: false,
			indexBgUrl: ''
		}
	},
	components: {
	},
	created() {
		this.$http.get('config/info?name=fLoginBackgroundImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		this.roleMenus = menu.list()
		for(let item in this.roleMenus) {
			if(this.roleMenus[item].hasFrontLogin=='是') {
				this.roles.push(this.roleMenus[item]);
			}
			if(this.roleMenus[item].hasFrontRegister=='是') {
				this.roles2.push(this.roleMenus[item]);
			}
		}
		
	},
	mounted() {
	},
	computed: {
		emailText: function() {
			var time = this.count;
			if (null != time && "" != time) {
				time = parseInt(time) + "秒后重发";
			}
			return time;
		}
	},
	//方法集合
	methods: {
		phoneClick() {
			if(!this.phone){
				this.$message.error(`手机号码不能为空`);
				return
			}
			if(this.phone&&(!this.$validate.isMobile2(this.phone))){
				this.$message.error(`请输入正确的手机格式`);
				return
			}
			if (this.phoneroles.length!=1) {
				if (!this.role) {
					this.$message.error("请选择登录用户类型");
					return false;
				}
			} else {
				this.role = this.phoneroles[0].roleName;
				this.loginForm.tableName = this.phoneroles[0].tableName;
			}
			var _this = this;
			this.$http({
				url: `${this.loginForm.tableName}/sendsms/login?mobile=`+this.phone,
				method: "get",
				params: {}
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.isEndFlag = false;
					this.inter = window.setInterval(function() {
						_this.count = _this.count - 1;
						if (_this.count <= 0) {
							window.clearInterval(_this.inter);
							_this.isEndFlag = true;
							_this.count=60;
						}
					}, 1000);
					this.$message.success(`发送成功`);
				} else {
					this.$message.error(data.msg)
				}
			});
		},
		randomString() {
			var len = 4;
			var chars = [
				'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
				'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
				'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
				'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
				'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2',
				'3', '4', '5', '6', '7', '8', '9'
			]
			var colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
			var sizes = ['14', '15', '16', '17', '18']
			
			var output = []
			for (var i = 0; i < len; i++) {
				// 随机验证码
				var key = Math.floor(Math.random() * chars.length)
				this.codes[i].num = chars[key]
				// 随机验证码颜色
				var code = '#'
				for (var j = 0; j < 6; j++) {
					var key = Math.floor(Math.random() * colors.length)
					code += colors[key]
				}
				this.codes[i].color = code
				// 随机验证码方向
				var rotate = Math.floor(Math.random() * 45)
				var plus = Math.floor(Math.random() * 2)
				if (plus == 1) rotate = '-' + rotate
				this.codes[i].rotate = 'rotate(' + rotate + 'deg)'
				// 随机验证码字体大小
				var size = Math.floor(Math.random() * sizes.length)
				this.codes[i].size = sizes[size] + 'px'
			}
		},
		getCurrentRow(row) {
			this.role = row.roleName;
		},
		submitForm(formName) {
			if(this.loginType==1) {
				if (this.roles.length!=1) {
					if (!this.role) {
						this.$message.error("请选择登录用户类型");
						return false;
					}
				} else {
					this.role = this.roles[0].roleName;
					this.loginForm.tableName = this.roles[0].tableName;
				}
				if (!this.loginForm.username) {
					this.$message.error("请输入用户名");
					return;
				}
				if (!this.loginForm.password) {
					this.$message.error("请输入密码");
					return;
				}
			}
			if(this.loginType==3 || this.loginType==4) {
				if (!this.phone) {
					this.$message.error("请输入手机号");
					return;
				}
				if (!this.phonecode) {
					this.$message.error("请输入手机验证码");
					return;
				}
				if (this.phoneroles.length!=1) {
					if (!this.role) {
						this.$message.error("请选择登录用户类型");
						return false;
					}
				} else {
					this.role = this.phoneroles[0].roleName;
					this.loginForm.tableName = this.phoneroles[0].tableName;
				}
			}

			this.loginPost(formName)
		},
		passwordLoginChange() {
			this.loginType = 1
		},
		loginPost(formName) {
				if(this.loginType==4) {
					this.phoneLogin()
					return false
				}
			this.$refs[formName].validate((valid) => {
				if (valid) {
					this.$http.get(`${this.loginForm.tableName}/login`, {params: this.loginForm}).then(res => {
						if (res.data.code === 0) {
							localStorage.setItem('frontToken', res.data.token);
							localStorage.setItem('UserTableName', this.loginForm.tableName);
							localStorage.setItem('username', this.loginForm.username);
							localStorage.setItem('frontSessionTable', this.loginForm.tableName);
							localStorage.setItem('frontRole', this.role);
							localStorage.setItem('keyPath', 0);
							this.$router.push('/');
							this.$message({
								message: '登录成功',
								type: 'success',
								duration: 1500,
							});
						} 
						else {
							this.$message.error(res.data.msg);
						}
					});
				} else {
					return false;
				}
			});
		},
		phoneLogin() {
			this.$http.post(`${this.loginForm.tableName}/sms/login?mobile=` + this.phone + '&smscode=' + this.phonecode,{}).then(res=>{
				if(res.data.code === 0) {
					localStorage.setItem('frontToken', res.data.token);
					localStorage.setItem('UserTableName', this.loginForm.tableName);
					localStorage.setItem('username', res.data.username);
					localStorage.setItem('frontSessionTable', this.loginForm.tableName);
					localStorage.setItem('frontRole', this.role);
					localStorage.setItem('keyPath', 0);
					this.$router.push('/');
					this.$message({
						message: '登录成功',
						type: 'success',
						duration: 1500,
					});
				} 
				else {
					this.$message.error(res.data.msg);
				}
			})
		},
    }
}
</script>

