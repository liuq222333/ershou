<template>
	<div class="front-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Account Workspace</span>
				<h1>个人中心</h1>
				<p>将资料维护、密码修改和常用入口整合到一个更清晰的账户工作区里，保持和管理端一致的留白与秩序感。</p>
			</div>
		</header>

		<section class="front-account-shell">
			<aside>
				<div class="front-account-card">
					<img class="front-account-avatar" :src="avatarUrl" alt="avatar">
					<div class="front-account-name">{{ sessionForm.xingming || sessionForm.zhanghao || '用户' }}</div>
					<div class="front-account-subtitle">
						账号 {{ sessionForm.zhanghao || '--' }} · 手机 {{ sessionForm.mobile || '--' }}
					</div>

					<div class="front-account-list">
						<div class="front-account-list__item">
							<span>性别</span>
							<strong>{{ sessionForm.xingbie || '--' }}</strong>
						</div>
						<div class="front-account-list__item">
							<span>年龄</span>
							<strong>{{ sessionForm.nianling || '--' }}</strong>
						</div>
						<div class="front-account-list__item">
							<span>身份证</span>
							<strong>{{ sessionForm.shenfenzheng || '--' }}</strong>
						</div>
					</div>
				</div>

				<div class="front-account-card">
					<div class="front-section__head" style="margin-bottom: 0;">
						<div>
							<h2 style="font-size: 22px;">快捷入口</h2>
							<p style="margin-top: 8px;">将收藏、点赞和评论统一收进账户侧栏。</p>
						</div>
					</div>
					<div class="front-account-list">
						<div class="front-account-list__item front-clickable" @click="openStoreup(1)">
							<span>我的收藏</span>
							<strong>进入</strong>
						</div>
						<div class="front-account-list__item front-clickable" @click="openStoreup(21)">
							<span>我的点赞</span>
							<strong>进入</strong>
						</div>
						<div class="front-account-list__item front-clickable" @click="openStoreup(81)">
							<span>我的评论</span>
							<strong>进入</strong>
						</div>
					</div>
				</div>
			</aside>

			<div>
				<section class="front-form-shell">
					<div class="front-form-shell__head">
						<div>
							<h2>资料维护</h2>
							<p>保留原有字段与接口，只重构页面结构与层级。</p>
						</div>
					</div>

					<el-form ref="sessionForm" :model="sessionForm" :rules="rules" label-width="92px">
						<div class="front-form-grid">
							<el-form-item label="账号" prop="zhanghao">
								<el-input v-model="sessionForm.zhanghao" disabled></el-input>
							</el-form-item>
							<el-form-item label="姓名" prop="xingming">
								<el-input v-model="sessionForm.xingming" placeholder="请输入姓名"></el-input>
							</el-form-item>
							<el-form-item label="性别" prop="xingbie">
								<el-select v-model="sessionForm.xingbie" placeholder="请选择性别">
									<el-option v-for="item in genderOptions" :key="item" :label="item" :value="item"></el-option>
								</el-select>
							</el-form-item>
							<el-form-item label="年龄" prop="nianling">
								<el-input v-model="sessionForm.nianling" placeholder="请输入年龄"></el-input>
							</el-form-item>
							<el-form-item label="身份证" prop="shenfenzheng">
								<el-input v-model="sessionForm.shenfenzheng" placeholder="请输入身份证"></el-input>
							</el-form-item>
							<el-form-item label="手机号" prop="mobile">
								<el-input v-model="sessionForm.mobile" placeholder="请输入手机号"></el-input>
							</el-form-item>
						</div>

						<el-form-item label="头像" prop="touxiang">
							<file-upload
								tip="点击上传头像"
								action="file/upload"
								:limit="1"
								:multiple="true"
								:fileUrls="sessionForm.touxiang ? sessionForm.touxiang : ''"
								@change="handleAvatarChange"
							></file-upload>
						</el-form-item>

						<div class="front-detail-actions">
							<el-button type="primary" @click="onSubmit('sessionForm')">保存资料</el-button>
							<el-button @click="logout">退出登录</el-button>
						</div>
					</el-form>
				</section>

				<section class="front-form-shell" style="margin-top: 22px;">
					<div class="front-form-shell__head">
						<div>
							<h2>安全设置</h2>
							<p>将修改密码合并进个人中心，不再作为割裂的单独页面风格。</p>
						</div>
					</div>

					<el-form ref="passwordForm" :model="passwordForm" :rules="passwordRules" label-width="92px">
						<div class="front-form-grid">
							<el-form-item label="原密码" prop="password">
								<el-input type="password" v-model="passwordForm.password" placeholder="请输入原密码"></el-input>
							</el-form-item>
							<el-form-item label="新密码" prop="newpassword">
								<el-input type="password" v-model="passwordForm.newpassword" placeholder="请输入新密码"></el-input>
							</el-form-item>
							<el-form-item label="确认密码" prop="repassword">
								<el-input type="password" v-model="passwordForm.repassword" placeholder="请再次输入新密码"></el-input>
							</el-form-item>
						</div>

						<div class="front-detail-actions">
							<el-button type="primary" @click="updatePassword">更新密码</el-button>
						</div>
					</el-form>
				</section>
			</div>
		</section>
	</div>
</template>

<script>
	import config from '@/config/config'
	import Vue from 'vue'

	export default {
		data() {
			return {
				baseUrl: config.baseUrl,
				sessionForm: {
					zhanghao: '',
					mima: '',
					xingming: '',
					xingbie: '',
					touxiang: '',
					nianling: '',
					shenfenzheng: '',
					mobile: ''
				},
				passwordForm: {
					password: '',
					newpassword: '',
					repassword: ''
				},
				genderOptions: ['男', '女'],
				userTableName: localStorage.getItem('UserTableName') || 'yonghu',
				rules: {
					mobile: [{ required: false, validator: (rule, value, callback) => this.$validate.isMobile(rule, value, callback), trigger: 'blur' }],
					shenfenzheng: [{ required: false, validator: (rule, value, callback) => this.$validate.isIdCard(rule, value, callback), trigger: 'blur' }]
				},
				passwordRules: {
					password: [{ required: true, message: '原密码不能为空', trigger: 'blur' }],
					newpassword: [{ required: true, message: '新密码不能为空', trigger: 'blur' }],
					repassword: [{ required: true, message: '确认密码不能为空', trigger: 'blur' }]
				}
			}
		},
		computed: {
			avatarUrl() {
				if (!this.sessionForm.touxiang) {
					return require('@/assets/avator.png')
				}
				return this.sessionForm.touxiang.indexOf('http') === 0 ? this.sessionForm.touxiang : this.baseUrl + this.sessionForm.touxiang
			}
		},
		created() {
			this.loadSession()
		},
		methods: {
			loadSession() {
				this.$http.get(`${this.userTableName}/session`, { emulateJSON: true }).then((res) => {
					if (res.data.code === 0) {
						this.sessionForm = Object.assign({}, this.sessionForm, res.data.data)
					}
				})
			},
			setSession() {
				localStorage.setItem('sessionForm', JSON.stringify(this.sessionForm))
				if (this.sessionForm.touxiang) {
					localStorage.setItem('frontHeadportrait', this.sessionForm.touxiang)
				}
			},
			handleAvatarChange(fileUrls) {
				this.sessionForm.touxiang = fileUrls.replace(new RegExp(this.$config.baseUrl, 'g'), '')
			},
			onSubmit(formName) {
				if (this.sessionForm.touxiang != null) {
					this.sessionForm.touxiang = this.sessionForm.touxiang.replace(new RegExp(this.$config.baseUrl, 'g'), '')
				}
				this.$refs[formName].validate((valid) => {
					if (!valid) {
						return false
					}
					this.$http.post(this.userTableName + '/update', this.sessionForm).then((res) => {
						if (res.data.code === 0) {
							this.setSession()
							this.$message({
								message: '更新成功',
								type: 'success',
								duration: 1500
							})
						}
					})
				})
			},
			openStoreup(type) {
				localStorage.setItem('storeupType', type)
				this.$router.push('/index/storeup')
			},
			async updatePassword() {
				this.$refs.passwordForm.validate(async (valid) => {
					if (!valid) {
						return false
					}
					let password = this.sessionForm.mima || this.sessionForm.password || ''
					let nowpassword = ''
					await this.$http.get('encrypt/md5?text=' + this.passwordForm.password).then((res) => {
						if (res.data && res.data.code === 0) {
							nowpassword = res.data.data
						}
					})
					if (nowpassword !== password) {
						this.$message.error('原密码错误')
						return
					}
					if (this.passwordForm.newpassword !== this.passwordForm.repassword) {
						this.$message.error('两次密码输入不一致')
						return
					}
					if (this.passwordForm.newpassword === this.passwordForm.password) {
						this.$message.error('新密码与原密码相同')
						return
					}
					this.sessionForm.password = this.passwordForm.newpassword
					this.sessionForm.mima = this.passwordForm.newpassword
					this.$http.post(`${this.userTableName}/update`, this.sessionForm).then(({ data }) => {
						if (data && data.code === 0) {
							this.setSession()
							this.passwordForm = {
								password: '',
								newpassword: '',
								repassword: ''
							}
							this.$message({
								message: '修改密码成功，下次登录生效',
								type: 'success',
								duration: 1500
							})
						} else {
							this.$message.error(data.msg)
						}
					})
				})
			},
			logout() {
				localStorage.clear()
				Vue.http.headers.common.Token = ''
				this.$router.push('/index/home')
				this.$message({
					message: '登出成功',
					type: 'success',
					duration: 1500
				})
			}
		}
	}
</script>
