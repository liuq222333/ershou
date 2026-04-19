<template>
	<div class="main-content center-page">
		<div class="center-page-head">
			<div class="center-page-title-block">
				<h2 class="center-page-title">个人中心</h2>
				<p class="center-page-subtitle">维护基础资料与账户安全设置，修改密码已合并到本页面</p>
			</div>
			<div class="center-page-metrics">
				<span class="metric-badge">当前角色 {{ sessionTable === 'users' ? '管理员' : '用户' }}</span>
				<span class="metric-badge">账号 {{ this.$storage.get('adminName') || '-' }}</span>
			</div>
		</div>

		<div class="center-layout">
			<section class="center-panel">
				<div class="panel-header">
					<h3 class="panel-title">基础资料</h3>
					<p class="panel-subtitle">支持编辑头像、姓名与联系方式信息</p>
				</div>

				<el-form
					ref="profileForm"
					:model="ruleForm"
					class="profile-form"
					label-position="top"
				>
					<div class="profile-grid" v-if="flag === 'yonghu'">
						<el-form-item class="profile-field" label="账号" prop="zhanghao">
							<el-input v-model="ruleForm.zhanghao" placeholder="账号" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field" label="姓名" prop="xingming">
							<el-input v-model="ruleForm.xingming" placeholder="姓名" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field" label="性别" prop="xingbie">
							<el-select filterable v-model="ruleForm.xingbie" placeholder="请选择性别">
								<el-option
									v-for="(item, index) in yonghuxingbieOptions"
									:key="index"
									:label="item"
									:value="item"
								></el-option>
							</el-select>
						</el-form-item>
						<el-form-item class="profile-field" label="年龄" prop="nianling">
							<el-input v-model="ruleForm.nianling" placeholder="年龄" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field" label="身份证" prop="shenfenzheng">
							<el-input v-model="ruleForm.shenfenzheng" placeholder="身份证" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field" label="手机号" prop="mobile">
							<el-input v-model="ruleForm.mobile" placeholder="手机号" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field profile-upload" label="头像" prop="touxiang">
							<file-upload
								tip="点击上传头像"
								action="file/upload"
								:limit="1"
								:multiple="false"
								:fileUrls="ruleForm.touxiang ? ruleForm.touxiang : ''"
								@change="yonghutouxiangUploadChange"
							></file-upload>
						</el-form-item>
					</div>

					<div class="profile-grid" v-else>
						<el-form-item class="profile-field" label="用户名" prop="username">
							<el-input v-model="ruleForm.username" placeholder="用户名" clearable></el-input>
						</el-form-item>
						<el-form-item class="profile-field profile-upload" label="头像" prop="image">
							<file-upload
								tip="点击上传头像"
								action="file/upload"
								:limit="1"
								:multiple="false"
								:fileUrls="ruleForm.image ? ruleForm.image : ''"
								@change="usersimageUploadChange"
							></file-upload>
						</el-form-item>
					</div>

					<div class="panel-actions">
						<el-button type="primary" @click="onUpdateHandler">保存资料</el-button>
					</div>
				</el-form>
			</section>

			<section class="center-panel security-panel">
				<div class="panel-header">
					<h3 class="panel-title">账户安全</h3>
					<p class="panel-subtitle">修改登录密码，建议定期更新并使用高强度组合</p>
				</div>

				<el-form
					ref="passwordForm"
					:model="passwordForm"
					:rules="passwordRules"
					class="password-form"
					label-position="top"
				>
					<el-form-item class="password-field" label="原密码" prop="password">
						<el-input type="password" show-password v-model="passwordForm.password" autocomplete="new-password"></el-input>
					</el-form-item>
					<el-form-item class="password-field" label="新密码" prop="newpassword">
						<el-input type="password" show-password v-model="passwordForm.newpassword" autocomplete="new-password"></el-input>
					</el-form-item>
					<el-form-item class="password-field" label="确认密码" prop="repassword">
						<el-input type="password" show-password v-model="passwordForm.repassword" autocomplete="new-password"></el-input>
					</el-form-item>

					<div class="panel-actions">
						<el-button type="primary" @click="onPasswordUpdateHandler">更新密码</el-button>
					</div>
				</el-form>
			</section>
		</div>
	</div>
</template>

<script>
import {
	isMobile,
	checkIdCard,
} from '@/utils/validate'

export default {
	data() {
		return {
			ruleForm: {},
			user: {},
			flag: '',
			yonghuxingbieOptions: ['男', '女'],
			passwordForm: {
				password: '',
				newpassword: '',
				repassword: '',
			},
			passwordRules: {
				password: [
					{ required: true, message: '原密码不能为空', trigger: 'blur' },
				],
				newpassword: [
					{ required: true, message: '新密码不能为空', trigger: 'blur' },
				],
				repassword: [
					{ required: true, message: '确认密码不能为空', trigger: 'blur' },
				],
			},
		}
	},
	computed: {
		sessionTable() {
			return this.$storage.get('sessionTable')
		},
	},
	mounted() {
		this.flag = this.sessionTable
		this.fetchSession()
	},
	methods: {
		fetchSession() {
			this.$http({
				url: `${this.sessionTable}/session`,
				method: 'get',
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.user = data.data || {}
					this.ruleForm = JSON.parse(JSON.stringify(this.user))
				} else {
					this.$message.error(data.msg)
				}
			})
		},
		normalizeFileValue(value) {
			if (!value) {
				return ''
			}
			return value.replace(new RegExp(this.$base.url, 'g'), '')
		},
		yonghutouxiangUploadChange(fileUrls) {
			this.ruleForm.touxiang = fileUrls
		},
		usersimageUploadChange(fileUrls) {
			this.ruleForm.image = fileUrls
		},
		onUpdateHandler() {
			if (this.flag === 'yonghu' && !this.ruleForm.zhanghao) {
				this.$message.error('账号不能为空')
				return
			}
			if (this.flag === 'yonghu' && !this.ruleForm.touxiang) {
				this.$message.error('头像不能为空')
				return
			}
			if (this.flag === 'yonghu' && this.ruleForm.shenfenzheng && !checkIdCard(this.ruleForm.shenfenzheng)) {
				this.$message.error('身份证应输入身份证格式')
				return
			}
			if (this.flag === 'yonghu' && this.ruleForm.mobile && !isMobile(this.ruleForm.mobile)) {
				this.$message.error('手机号应输入手机格式')
				return
			}
			if (this.flag === 'users' && (!this.ruleForm.username || this.ruleForm.username.trim().length < 1)) {
				this.$message.error('用户名不能为空')
				return
			}

			const payload = JSON.parse(JSON.stringify(this.ruleForm))
			if (this.flag === 'users') {
				payload.image = this.normalizeFileValue(payload.image)
			}
			if (this.flag === 'yonghu') {
				payload.touxiang = this.normalizeFileValue(payload.touxiang)
			}

			this.$http({
				url: `${this.sessionTable}/update`,
				method: 'post',
				data: payload,
			}).then(({ data }) => {
				if (data && data.code === 0) {
					if (this.flag === 'users') {
						this.$storage.set('headportrait', payload.image)
					} else if (this.flag === 'yonghu') {
						this.$storage.set('headportrait', payload.touxiang)
					}
					this.user = Object.assign({}, this.user, payload)
					this.ruleForm = JSON.parse(JSON.stringify(this.user))
					this.$message({
						message: '修改信息成功',
						type: 'success',
						duration: 1500,
					})
				} else {
					this.$message.error(data.msg)
				}
			})
		},
		resetPasswordForm() {
			this.passwordForm = {
				password: '',
				newpassword: '',
				repassword: '',
			}
			this.$nextTick(() => {
				if (this.$refs.passwordForm) {
					this.$refs.passwordForm.clearValidate()
				}
			})
		},
		submitNewPassword(newPassword) {
			const payload = Object.assign({}, this.user, {
				password: newPassword,
				mima: newPassword,
			})
			this.$http({
				url: `${this.sessionTable}/update`,
				method: 'post',
				data: payload,
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.user = payload
					this.resetPasswordForm()
					this.$message({
						message: '修改密码成功，下次登录生效',
						type: 'success',
						duration: 1500,
					})
				} else {
					this.$message.error(data.msg)
				}
			})
		},
		onPasswordUpdateHandler() {
			this.$refs.passwordForm.validate(async (valid) => {
				if (!valid) {
					return
				}

				const oldPassword = this.passwordForm.password
				const newPassword = this.passwordForm.newpassword
				const confirmPassword = this.passwordForm.repassword
				const currentPassword = this.user.mima || this.user.password || ''

				if (!currentPassword) {
					this.$message.error('当前账号未配置密码，无法修改')
					return
				}
				if (newPassword !== confirmPassword) {
					this.$message.error('两次密码输入不一致')
					return
				}
				if (newPassword === oldPassword) {
					this.$message.error('新密码与原密码相同')
					return
				}

				if (this.sessionTable === 'users') {
					if (oldPassword !== currentPassword) {
						this.$message.error('原密码错误')
						return
					}
					this.submitNewPassword(newPassword)
					return
				}

				let md5OldPassword = ''
				await this.$http({
					url: `/encrypt/md5?text=${oldPassword}`,
					method: 'get',
				}).then((res) => {
					if (res.data && res.data.code === 0) {
						md5OldPassword = res.data.data
					}
				})

				if (!md5OldPassword || md5OldPassword !== currentPassword) {
					this.$message.error('原密码错误')
					return
				}
				this.submitNewPassword(newPassword)
			})
		},
	},
}
</script>

<style lang="scss" scoped>
	.center-page {
		--hw-red: #cf0a2c;
		--hw-red-strong: #b90525;
		--hw-text: #1f2329;
		--hw-sub: #6b7280;
		--hw-line: #e7e9ef;
		--hw-bg: #f4f6fa;
		padding: 22px !important;
		background:
			radial-gradient(circle at 0% 0%, rgba(207, 10, 44, 0.06) 0%, transparent 34%),
			radial-gradient(circle at 100% 100%, rgba(207, 10, 44, 0.04) 0%, transparent 30%),
			var(--hw-bg) !important;
		font-family: "HarmonyOS Sans SC", "PingFang SC", "Segoe UI", sans-serif;
	}

	.center-page-head {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 16px;
		margin-bottom: 14px;
	}

	.center-page-title {
		margin: 0;
		color: var(--hw-text);
		font-size: 28px;
		line-height: 1.18;
		font-weight: 700;
		letter-spacing: 0.01em;
	}

	.center-page-subtitle {
		margin: 8px 0 0;
		color: var(--hw-sub);
		font-size: 14px;
	}

	.center-page-metrics {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		justify-content: flex-end;
	}

	.metric-badge {
		padding: 7px 12px;
		border: 1px solid var(--hw-line);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.9);
		color: #505a6a;
		font-size: 12px;
		font-weight: 600;
	}

	.center-layout {
		display: grid;
		grid-template-columns: 1.65fr 1fr;
		gap: 16px;
	}

	.center-panel {
		border: 1px solid var(--hw-line);
		border-radius: 16px;
		background: rgba(255, 255, 255, 0.95);
		box-shadow: 0 8px 26px rgba(31, 35, 41, 0.06);
		padding: 18px;
	}

	.panel-header {
		margin-bottom: 14px;
	}

	.panel-title {
		margin: 0;
		font-size: 18px;
		font-weight: 700;
		color: #1f2937;
	}

	.panel-subtitle {
		margin: 6px 0 0;
		font-size: 13px;
		color: #6b7280;
	}

	.profile-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 10px 14px;
	}

	.profile-field,
	.password-field {
		margin-bottom: 8px !important;
	}

	.profile-upload {
		grid-column: 1 / -1;
	}

	.profile-form ::v-deep .el-form-item__label,
	.password-form ::v-deep .el-form-item__label {
		padding: 0 0 6px !important;
		line-height: 1.2 !important;
		font-size: 13px !important;
		font-weight: 600 !important;
		color: #374151 !important;
	}

	.profile-form ::v-deep .el-input__inner,
	.profile-form ::v-deep .el-select .el-input__inner,
	.password-form ::v-deep .el-input__inner {
		height: 40px !important;
		border: 1px solid #d8dce5 !important;
		border-radius: 10px !important;
		background: #fff !important;
		color: #1f2937 !important;
		font-size: 13px !important;
		box-shadow: none !important;
	}

	.profile-form ::v-deep .el-input__inner:focus,
	.profile-form ::v-deep .el-select .el-input__inner:focus,
	.password-form ::v-deep .el-input__inner:focus {
		border-color: var(--hw-red) !important;
		box-shadow: 0 0 0 3px rgba(207, 10, 44, 0.12) !important;
	}

	.profile-form ::v-deep .el-upload-list__item,
	.profile-form ::v-deep .el-upload--picture-card,
	.profile-form ::v-deep .el-upload .el-icon-plus {
		border-radius: 12px !important;
	}

	.security-panel {
		display: flex;
		flex-direction: column;
	}

	.password-form {
		max-width: 100%;
	}

	.panel-actions {
		display: flex;
		justify-content: flex-start;
		padding-top: 8px;
	}

	.panel-actions .el-button {
		height: 40px !important;
		padding: 0 18px !important;
		border: 0 !important;
		border-radius: 10px !important;
		background: linear-gradient(135deg, var(--hw-red) 0%, var(--hw-red-strong) 100%) !important;
		color: #fff !important;
		font-size: 13px !important;
		font-weight: 600 !important;
		box-shadow: 0 8px 18px rgba(207, 10, 44, 0.24) !important;
	}

	.panel-actions .el-button:hover {
		filter: brightness(0.96);
	}

	@media (max-width: 1400px) {
		.center-page-head {
			align-items: flex-start;
			flex-direction: column;
		}

		.center-page-metrics {
			justify-content: flex-start;
		}

		.center-layout {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 992px) {
		.center-page {
			padding: 16px !important;
		}

		.center-page-title {
			font-size: 24px;
		}

		.profile-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
