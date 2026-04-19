<template>
	<div :style='{"width":"100%","padding":"30px 30px 30px 30px","background":"#FDF7ED"}'>
		<el-form
			v-if="showType==1"
			:style='{"padding":"40px 130px 30px 30px","boxShadow":"0px 3px 6px 1px rgba(0,0,0,0.10)","margin":"0","borderRadius":"10px","flexWrap":"wrap","background":"#FEFEF6","display":"flex","width":"100%"}'
			class="add-update-preview"
			ref="ruleForm"
			:rules="rules"
			:model="ruleForm"
			label-width="180px"
		>
			<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' label="原密码" prop="password">
				<el-input type="password" v-model="ruleForm.password" ></el-input>
			</el-form-item>
			<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' label="新密码" prop="newpassword">
				<el-input type="password" v-model="ruleForm.newpassword" ></el-input>
			</el-form-item>
			<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' label="确认密码" prop="repassword">
				<el-input type="password" v-model="ruleForm.repassword" ></el-input>
			</el-form-item>
			<el-form-item :style='{"padding":"0","margin":"10px 0 10px 180px","flexWrap":"wrap","background":"none","display":"flex","width":"auto","justifyContent":"center"}'>
				<el-button class="btn3" :style='{"border":"1px solid #f3a213","cursor":"pointer","padding":"0 24px","boxShadow":"inset 0px 3px 6px 1px #FFFFFF","margin":"10px 10px 0 0","color":"#fff","minWidth":"130px","outline":"none","borderRadius":"0","background":"#f3a213","width":"auto","fontSize":"16px","fontWeight":"bold","height":"47px"}' type="primary" @click="onUpdateHandler">
					<span class="icon iconfont icon-queren15" :style='{"margin":"0 2px","fontSize":"16px","color":"#fff","display":"none","height":"40px"}'></span>
					提交
				</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>
<script>
export default {
	data() {
		return {
			dialogVisible: false,
			ruleForm: {},
			payForm: {},
			user: {},
			rules: {
				password: [
					{
						required: true,
						message: "密码不能为空",
						trigger: "blur"
					}
				],
				newpassword: [
					{
						required: true,
						message: "新密码不能为空",
						trigger: "blur"
					}
				],
				repassword: [
					{
						required: true,
						message: "确认密码不能为空",
						trigger: "blur"
					}
				]
			},
			rules2: {
				password: [
					{
						required: true,
						message: "支付密码不能为空",
						trigger: "blur"
					}
				],
				newpassword: [
					{
						required: true,
						message: "新支付密码不能为空",
						trigger: "blur"
					}
				],
				repassword: [
					{
						required: true,
						message: "确认支付密码不能为空",
						trigger: "blur"
					}
				]
			},
			showType: '1'
		};
	},
	mounted() {
		this.$http({
			url: `${this.$storage.get("sessionTable")}/session`,
			method: "get"
		}).then(({ data }) => {
			if (data && data.code === 0) {
				this.user = data.data;
			} else {
				this.$message.error(data.msg);
			}
		});
	},
	methods: {
		onLogout() {
			this.$storage.remove("Token");
			this.$router.replace({ name: "login" });
		},
		// 修改密码
		async onUpdateHandler() {
			this.$refs["ruleForm"].validate(async valid => {
				if (valid) {
					var password = "";
					if (this.user.mima) {
						password = this.user.mima;
					} else if (this.user.password) {
						password = this.user.password;
					}
					if(this.$storage.get("sessionTable")=='users'){
						if (this.ruleForm.password != password) {
							this.$message.error("原密码错误");
							return;
						}
						if (this.ruleForm.newpassword != this.ruleForm.repassword) {
							this.$message.error("两次密码输入不一致");
							return;
						}
						this.user.password = this.ruleForm.newpassword;
						this.user.mima = this.ruleForm.newpassword;
						this.$http({
							url: `${this.$storage.get("sessionTable")}/update`,
							method: "post",
							data: this.user
						}).then(({ data }) => {
							if (data && data.code === 0) {
								this.$message({
									message: "修改密码成功,下次登录系统生效",
									type: "success",
									duration: 1500,
									onClose: () => {
									}
								});
							} else {
								this.$message.error(data.msg);
							}
						});
						return false
					}
					var nowpassword = ''
					await this.$http({
						url: '/encrypt/md5?text=' + this.ruleForm.password,
						method: 'get'
					}).then(res=>{
						if(res.data&&res.data.code==0){
							nowpassword = res.data.data
						}
					})
					if(nowpassword!=password){
						this.$message.error("原密码错误");
						return;
					}
					if (this.ruleForm.newpassword != this.ruleForm.repassword) {
						this.$message.error("两次密码输入不一致");
						return;
					}
					if (this.ruleForm.newpassword == this.ruleForm.password) {
						this.$message.error("新密码与原密码相同");
						return;
					}
					this.user.password = this.ruleForm.newpassword;
					this.user.mima = this.ruleForm.newpassword;
					this.$http({
						url: `${this.$storage.get("sessionTable")}/update`,
						method: "post",
						data: this.user
					}).then(({ data }) => {
						if (data && data.code === 0) {
							this.$message({
								message: "修改密码成功,下次登录系统生效",
								type: "success",
								duration: 1500,
								onClose: () => {
								}
							});
						} else {
							this.$message.error(data.msg);
						}
					});
				}
			});
		}
	}
};
</script>
<style lang="scss" scoped>
	.el-date-editor.el-input {
		width: auto;
	}
	
	.add-update-preview .el-form-item ::v-deep .el-form-item__label {
	  	  padding: 0 10px;
	  	  color: #333333;
	  	  white-space: nowrap;
	  	  background: none;
	  	  font-weight: 600;
	  	  width: 180px;
	  	  font-size: 16px;
	  	  line-height: 64px;
	  	  text-align: right;
	  	  height: 64px;
	  	}
	.add-update-preview .el-form-item ::v-deep .el-form-item__content {
		margin-left: auto !important;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	
	.add-update-preview .el-input ::v-deep .el-input__inner {
	  	  border:  1px solid #DADFE6;
	  	  border-radius: 4px;
	  	  padding: 0 12px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  outline: none;
	  	  color: #333;
	  	  background: #FFFFFF;
	  	  flex: 1;
	  	  width: 100%;
	  	  font-size: 16px;
	  	  height: 48px;
	  	}
	
	.add-update-preview .el-select ::v-deep .el-input__inner {
	  	  border:  1px solid #DADFE6;
	  	  border-radius: 4px;
	  	  padding: 0 12px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  outline: none;
	  	  color: #333;
	  	  background: #FFFFFF;
	  	  flex: 1;
	  	  width: 100%;
	  	  font-size: 16px;
	  	  height: 48px;
	  	}
	
	.add-update-preview .el-date-editor ::v-deep .el-input__inner {
	  	  border:  1px solid #DADFE6;
	  	  border-radius: 4px;
	  	  padding: 0 30px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  outline: none;
	  	  color: #333;
	  	  background: #FFFFFF;
	  	  flex: 1;
	  	  width: 100%;
	  	  font-size: 16px;
	  	  height: 48px;
	  	}
	
	.add-update-preview ::v-deep .el-upload--picture-card {
		background: transparent;
		border: 0;
		border-radius: 0;
		width: auto;
		height: auto;
		line-height: initial;
		vertical-align: middle;
	}
	
	.add-update-preview ::v-deep .el-upload-list .el-upload-list__item {
	  	  border: 1px solid #DADFE6;
	  	  cursor: pointer;
	  	  border-radius: 4px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  color: #999;
	  	  background: #fff;
	  	  font-weight: 600;
	  	  width: 80px;
	  	  font-size: 30px;
	  	  line-height: 80px;
	  	  text-align: center;
	  	  height: 80px;
	  	}
	
	.add-update-preview ::v-deep .el-upload .el-icon-plus {
	  	  border: 1px solid #DADFE6;
	  	  cursor: pointer;
	  	  border-radius: 4px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  color: #999;
	  	  background: #fff;
	  	  font-weight: 600;
	  	  width: 80px;
	  	  font-size: 30px;
	  	  line-height: 80px;
	  	  text-align: center;
	  	  height: 80px;
	  	}
	
	.add-update-preview .el-textarea ::v-deep .el-textarea__inner {
	  	  border-radius: 4px;
	  	  padding: 12px;
	  	  box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
	  	  outline: none;
	  	  color: #666;
	  	  background: #fff;
	  	  width: 100%;
	  	  font-size: 16px;
	  	  border-color: #e8e9eb;
	  	  border-width: 1px;
	  	  border-style: solid;
	  	  height: auto;
	  	}
	
	.add-update-preview .btn3 {
				border: 1px solid #f3a213;
				cursor: pointer;
				padding: 0 24px;
				margin: 10px 10px 0 0;
				color: #fff;
				font-weight: bold;
				font-size: 16px;
				border-radius: 0;
				box-shadow: inset 0px 3px 6px 1px #FFFFFF;
				outline: none;
				background: #f3a213;
				width: auto;
				min-width: 130px;
				height: 47px;
			}
	
	.add-update-preview .btn3:hover {
				opacity: 0.8;
			}
</style>

