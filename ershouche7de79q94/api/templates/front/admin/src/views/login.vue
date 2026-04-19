<template>
	<div class="admin-login">
		<div class="admin-login__ambient admin-login__ambient--left"></div>
		<div class="admin-login__ambient admin-login__ambient--right"></div>

		<section class="admin-login__shell">
			<aside class="admin-login__brand">
				<span class="admin-login__eyebrow">USED CAR INTELLIGENCE</span>
				<h1 class="admin-login__brand-title">二手车数据平台</h1>
				<p class="admin-login__brand-note">管理端入口</p>
				<div class="admin-login__brand-meta">
					<span>价格预测</span>
					<span>车源运营</span>
					<span>数据洞察</span>
				</div>
			</aside>

			<el-form :model="rulesForm" class="admin-login__panel" @submit.native.prevent="login">
				<div class="admin-login__panel-head">
					<span class="admin-login__tag">Admin Access</span>
					<h2>登录管理端</h2>
					<p>输入账号后进入工作台</p>
				</div>

				<div class="admin-login__fields">
					<el-input
						v-if="loginType == 1"
						v-model.trim="rulesForm.username"
						placeholder="请输入账号"
						autocomplete="username"
						@keyup.enter.native="login"
					></el-input>

					<el-input
						v-if="loginType == 1"
						v-model="rulesForm.password"
						type="password"
						:show-password="true"
						placeholder="请输入密码"
						autocomplete="current-password"
						@keyup.enter.native="login"
					></el-input>

					<el-select
						v-if="displayRoles.length > 1 && loginType <= 2"
						v-model="rulesForm.role"
						placeholder="请选择角色"
					>
						<el-option
							v-for="item in displayRoles"
							:key="item.roleName"
							:label="item.roleName"
							:value="item.roleName"
						></el-option>
					</el-select>
				</div>

				<div class="admin-login__actions">
					<el-button
						v-if="loginType == 1 || loginType == 3 || loginType == 4"
						type="primary"
						class="admin-login__submit"
						:loading="isSubmitting"
						:disabled="submitDisabled"
						@click="login"
					>
						进入系统
					</el-button>
					<p class="admin-login__hint">请使用已分配账号登录</p>
				</div>
			</el-form>
		</section>
	</div>
</template>

<script>
	import menu from "@/utils/menu";

	export default {
		data() {
			return {
				loginType: 1,
				rulesForm: {
					username: "",
					password: "",
					role: "",
				},
				isSubmitting: false,
				menus: [],
				roles: [],
				tableName: "",
			};
		},
		computed: {
			displayRoles() {
				return (this.roles || []).filter((item) => this.loginType == 1 || (this.loginType == 2 && item.role != 'users'));
			},
			submitDisabled() {
				if (this.isSubmitting) {
					return true;
				}
				if (this.loginType != 1) {
					return false;
				}
				if (!this.rulesForm.username || !this.rulesForm.password) {
					return true;
				}
				if (this.roles.length > 1 && !this.rulesForm.role) {
					return true;
				}
				return false;
			}
		},
		mounted() {
			let menus = menu.list() || [];
			this.menus = menus;
			this.roles = this.menus.filter((item) => item.hasBackLogin == '是');

			if (this.roles.length === 1) {
				this.rulesForm.role = this.roles[0].roleName;
			}
		},
		methods: {
			login() {
				if (this.isSubmitting) {
					return;
				}
				if (this.loginType == 1) {
					if (!this.roles.length) {
						this.$message.error("未找到可登录角色");
						return;
					}
					if (!this.rulesForm.username) {
						this.$message.error("请输入用户名");
						return;
					}
					if (!this.rulesForm.password) {
						this.$message.error("请输入密码");
						return;
					}
					if (this.roles.length > 1) {
						if (!this.rulesForm.role) {
							this.$message.error("请选择角色");
							return;
						}

						for (let i = 0; i < this.roles.length; i++) {
							if (this.roles[i].roleName == this.rulesForm.role) {
								this.tableName = this.roles[i].tableName;
							}
						}
					} else {
						this.tableName = this.roles[0].tableName;
						this.rulesForm.role = this.roles[0].roleName;
					}
				}

				this.loginPost();
			},
			loginPost() {
				this.isSubmitting = true;
				this.$http({
					url: `${this.tableName}/login?username=${this.rulesForm.username}&password=${this.rulesForm.password}`,
					method: "post"
				}).then(({ data }) => {
					if (!(data && data.code === 0)) {
						throw new Error((data && data.msg) || "登录失败");
					}
					this.$storage.set("Token", data.token);
					this.$storage.set("role", this.rulesForm.role);
					this.$storage.set("sessionTable", this.tableName);
					this.$storage.set("adminName", this.rulesForm.username);
					return this.$nextTick().then(() => {
						return this.$http({
							url: this.tableName + '/session',
							method: "get"
						}).then(({ data }) => {
							if (!(data && data.code === 0)) {
								throw new Error((data && data.msg) || "会话信息加载失败");
							}
							if (this.tableName == 'yonghu') {
								this.$storage.set('headportrait', data.data.touxiang);
							}
							if (this.tableName == 'users') {
								this.$storage.set('headportrait', data.data.image);
							}
							this.$storage.set('userForm', JSON.stringify(data.data));
							this.$storage.set('userid', data.data.id);
							if (this.boardAuth('hasBoard', '查看', this.rulesForm.role)) {
								this.$router.replace({ path: "/board" });
							} else {
								this.$router.replace({ path: "/" });
							}
						});
					});
				}).catch((error) => {
					this.clearLoginStorage();
					this.$message.error(this.getLoginErrorMessage(error));
				}).finally(() => {
					this.isSubmitting = false;
				});
			},
			clearLoginStorage() {
				["Token", "role", "sessionTable", "adminName", "headportrait", "userForm", "userid"].forEach((key) => {
					this.$storage.remove(key);
				});
			},
			getLoginErrorMessage(error) {
				if (error && error.message && error.message !== "Network Error") {
					return error.message;
				}
				return "登录请求失败，请确认后端服务已启动";
			}
		}
	}
</script>

<style lang="scss" scoped>
	.admin-login {
		position: relative;
		min-height: 100vh;
		overflow: hidden;
		padding: 32px;
		background:
			radial-gradient(circle at top left, rgba(31, 143, 99, 0.16), transparent 30%),
			radial-gradient(circle at top right, rgba(31, 143, 99, 0.08), transparent 22%),
			linear-gradient(180deg, #f8fbf8 0%, #f2f5f2 100%);
	}

	.admin-login__ambient {
		position: absolute;
		border-radius: 999px;
		filter: blur(26px);
		pointer-events: none;
	}

	.admin-login__ambient--left {
		top: 8%;
		left: -6%;
		width: 360px;
		height: 360px;
		background: rgba(31, 143, 99, 0.08);
	}

	.admin-login__ambient--right {
		right: -4%;
		bottom: 8%;
		width: 320px;
		height: 320px;
		background: rgba(31, 143, 99, 0.06);
	}

	.admin-login__shell {
		position: relative;
		z-index: 1;
		display: grid;
		grid-template-columns: minmax(320px, 1fr) minmax(460px, 520px);
		gap: 56px;
		align-items: center;
		width: min(calc(100% - 32px), 1320px);
		min-height: calc(100vh - 64px);
		margin: 0 auto;
	}

	.admin-login__brand,
	.admin-login__panel {
		animation: adminLoginRise 0.75s cubic-bezier(0.22, 1, 0.36, 1) both;
	}

	.admin-login__panel {
		animation-delay: 0.08s;
	}

	.admin-login__brand {
		display: flex;
		flex-direction: column;
		gap: 18px;
		max-width: 560px;
	}

	.admin-login__brand-meta {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		margin-top: 6px;
	}

	.admin-login__brand-meta span {
		display: inline-flex;
		align-items: center;
		min-height: 36px;
		padding: 0 14px;
		border: 1px solid rgba(21, 33, 24, 0.08);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.34);
		color: var(--admin-text-soft);
		font-size: 12px;
		font-weight: 600;
		letter-spacing: 0.04em;
	}

	.admin-login__eyebrow,
	.admin-login__tag {
		display: inline-flex;
		align-items: center;
		width: fit-content;
		min-height: 42px;
		padding: 0 18px;
		border: 1px solid rgba(21, 33, 24, 0.08);
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.46);
		backdrop-filter: blur(18px);
		-webkit-backdrop-filter: blur(18px);
		color: var(--admin-text-soft);
		font-size: 12px;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}

	.admin-login__brand-title {
		margin: 0;
		color: var(--admin-text);
		font-size: clamp(52px, 6vw, 88px);
		line-height: 0.96;
		letter-spacing: -0.06em;
	}

	.admin-login__brand-note,
	.admin-login__panel-head p,
	.admin-login__hint {
		margin: 0;
		color: var(--admin-text-soft);
		font-size: 15px;
		line-height: 1.8;
	}

	.admin-login__panel {
		width: 100%;
		padding: 34px 32px 28px;
		border: 1px solid rgba(255, 255, 255, 0.42);
		border-radius: 22px;
		background: rgba(255, 255, 255, 0.72);
		backdrop-filter: blur(30px) saturate(150%);
		-webkit-backdrop-filter: blur(30px) saturate(150%);
		box-shadow: 0 24px 54px rgba(21, 33, 24, 0.08);
		transition: transform 0.24s ease, box-shadow 0.24s ease, background 0.24s ease;
	}

	.admin-login__panel:hover {
		transform: translateY(-2px);
		background: rgba(255, 255, 255, 0.78);
		box-shadow: 0 28px 60px rgba(21, 33, 24, 0.1);
	}

	.admin-login__panel-head {
		display: flex;
		flex-direction: column;
		gap: 12px;
		margin-bottom: 28px;
	}

	.admin-login__panel-head h2 {
		margin: 0;
		color: var(--admin-text);
		font-size: 34px;
		line-height: 1.08;
		letter-spacing: -0.04em;
	}

	.admin-login__fields {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.admin-login__actions {
		display: flex;
		flex-direction: column;
		gap: 14px;
		margin-top: 24px;
	}

	.admin-login__submit {
		width: 100%;
		min-height: 48px;
		font-size: 15px;
	}

	.admin-login__submit.is-disabled,
	.admin-login__submit.is-disabled:hover,
	.admin-login__submit.is-disabled:focus {
		background: linear-gradient(180deg, #8cc9b0 0%, #6fb495 100%) !important;
		box-shadow: none !important;
	}

	.admin-login ::v-deep .el-select {
		width: 100%;
	}

	.admin-login ::v-deep .el-input__inner,
	.admin-login ::v-deep .el-select .el-input__inner {
		height: 52px !important;
		line-height: 52px !important;
		padding: 0 16px !important;
		border: 1px solid transparent !important;
		border-radius: 14px !important;
		background: rgba(255, 255, 255, 0.84) !important;
		box-shadow: inset 0 0 0 1px rgba(21, 33, 24, 0.08);
		color: var(--admin-text) !important;
	}

	.admin-login ::v-deep .el-input__inner:hover,
	.admin-login ::v-deep .el-select:hover .el-input__inner {
		box-shadow: inset 0 0 0 1px rgba(21, 33, 24, 0.12);
	}

	.admin-login ::v-deep .el-input__inner:focus,
	.admin-login ::v-deep .el-select .el-input.is-focus .el-input__inner {
		box-shadow:
			inset 0 0 0 1px rgba(31, 143, 99, 0.22),
			0 0 0 4px rgba(31, 143, 99, 0.08) !important;
	}

	.admin-login ::v-deep .el-input__inner::placeholder,
	.admin-login ::v-deep .el-select .el-input__inner::placeholder {
		color: rgba(102, 112, 103, 0.72);
	}

	.admin-login ::v-deep .el-input__suffix {
		display: flex;
		align-items: center;
		right: 14px;
	}

	.admin-login ::v-deep .el-input__suffix-inner,
	.admin-login ::v-deep .el-input__icon,
	.admin-login ::v-deep .el-select .el-input .el-select__caret {
		color: rgba(21, 33, 24, 0.45);
		line-height: 52px;
	}

	@keyframes adminLoginRise {
		from {
			opacity: 0;
			transform: translateY(18px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@media (max-width: 1100px) {
		.admin-login__shell {
			grid-template-columns: 1fr;
			gap: 28px;
			align-items: start;
		}

		.admin-login__brand {
			max-width: none;
		}

		.admin-login__brand-title {
			font-size: clamp(40px, 9vw, 64px);
		}
	}

	@media (max-width: 640px) {
		.admin-login {
			padding: 18px;
		}

		.admin-login__shell {
			width: 100%;
			min-height: calc(100vh - 36px);
			gap: 22px;
		}

		.admin-login__panel {
			padding: 24px 18px 20px;
		}

		.admin-login__panel-head h2 {
			font-size: 28px;
		}

		.admin-login__brand-meta {
			gap: 8px;
		}
	}
</style>
