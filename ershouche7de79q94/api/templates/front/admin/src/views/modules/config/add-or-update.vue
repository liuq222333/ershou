








<template>
	<div class="addEdit-block">
		<el-form
			class="add-update-preview"
			ref="ruleForm"
			:model="ruleForm"
			:rules="rules"
			label-width="180px"
		>
			<template >
				<el-form-item class="input" v-if="type!='info'"  label="名称" prop="name" >
					<el-input v-model="ruleForm.name" placeholder="名称" clearable readonly></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="名称" prop="name" >
					<el-input v-model="ruleForm.name" placeholder="名称" readonly></el-input>
				</el-form-item>
				<el-form-item class="upload" v-if="type!='info' && !ro.value" label="图片" prop="value" >
					<file-upload
						tip="点击上传值"
						action="file/upload"
						:limit="3"
						:disabled="ro.value"
						:multiple="true"
						:fileUrls="ruleForm.value?ruleForm.value:''"
						@change="valueUploadChange"
					></file-upload>
				</el-form-item>
				<el-form-item class="upload" v-else-if="ruleForm.value" label="值" prop="value" >
					<img v-if="ruleForm.value.substring(0,4)=='http'&&ruleForm.value.split(',w').length>1" class="upload-img" style="margin-right:20px;" v-bind:key="index" :src="ruleForm.value" width="100" height="100" @click="imgPreView(ruleForm.tupian)">
					<img v-else-if="ruleForm.value.substring(0,4)=='http'" class="upload-img" style="margin-right:20px;" v-bind:key="index" :src="ruleForm.value.split(',')[0]" width="100" height="100" @click="imgPreView(ruleForm.tupian.split(',')[0])">
					<img v-else class="upload-img" style="margin-right:20px;" v-bind:key="index" v-for="(item,index) in ruleForm.value.split(',')" :src="$base.url+item" width="100" height="100" @click="imgPreView($base.url+item)">
				</el-form-item>
			</template>
			<el-form-item class="textarea" v-if="type!='info'&&ruleForm.type==1" label="链接" prop="url" >
				<el-input
					style="min-width: 200px; max-width: 600px;"
					type="textarea"
					:rows="8"
					placeholder="url"
					v-model="ruleForm.url" >
				</el-input>
			</el-form-item>
			<el-form-item v-else-if="ruleForm.url" label="url" prop="url"  class="textBox">
				<span class="text">{{ruleForm.url}}</span>
			</el-form-item>
			<el-form-item class="btn">
				<el-button class="btn3"  v-if="type!='info'" type="success" @click="onSubmit">
					<span class="icon iconfont icon-queren15"></span>
					提交
				</el-button>
				<el-button class="btn4" v-if="type!='info'" type="success" @click="back()">
					<span class="icon iconfont icon-guanbi2"></span>
					取消
				</el-button>
				<el-button class="btn5" v-if="type=='info'" type="success" @click="back()">
					<span class="icon iconfont icon-fanhui13"></span>
					返回
				</el-button>
			</el-form-item>
		</el-form>
    

	</div>
</template>
<script>
	import { 
		isIntNumer,
	} from "@/utils/validate";
	export default {
		data() {
			var validateIntNumber = (rule, value, callback) => {
				if(!value){
					callback();
				} else if (!isIntNumer(value)) {
					callback(new Error("请输入整数"));
				} else {
					callback();
				}
			};
			return {
				id: '',
				type: '',
			
			
				ro:{
					name : false,
					value : false,
					url : false,
					type : false,
				},
			
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
						{ validator: validateIntNumber, trigger: 'blur' },
					],
				},
			};
		},
		props: ["parent"],
		computed: {
			sessionForm() {
				return JSON.parse(this.$storage.getObj('userForm'))
			},
			sessionTable() {
				return this.$storage.get('sessionTable')
			},



		},
		components: {
		},
		created() {
		},
		methods: {
			imgPreView(url){
				this.$parent.imgPreView(url)
			},
			// 下载
			download(file){
				window.open(`${file}`)
			},
			// 初始化
			init(id,type ,configLen) {
				if (id) {
					this.id = id;
					this.type = type;
				}
				else {
					this.ruleForm = {
						type: 1,
						name: 'picture' + (Number(configLen) + 1),
						value: '',
						url: ''
					}
				}
				if(this.type=='info'||this.type=='else'||this.type=='msg'){
					this.info(id);
				}else if(this.type=='logistics'){
					for(let x in this.ro) {
						this.ro[x] = true
					}
					this.logistics=false;
					this.info(id);
				}else if(this.type=='cross'){
					var obj = this.$storage.getObj('crossObj');
					for (var o in obj){
						if(o=='name'){
							this.ruleForm.name = obj[o];
							this.ro.name = true;
							continue;
						}
						if(o=='value'){
							this.ruleForm.value = obj[o];
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
				}

			
			},
			// 多级联动参数

			async info(id) {
				await this.$http({
					url: `config/info/${id}`,
					method: "get"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.ruleForm = data.data;
						//解决前台上传图片后台不显示的问题
						let reg=new RegExp('../../../upload','g')//g代表全部
					} else {
						this.$message.error(data.msg);
					}
				});
			},

			// 提交
			async onSubmit() {
					if(this.ruleForm.type==1&&!this.ruleForm.value) {
						this.$message.error("轮播图图片不能为空");
						return false
					}
					if(this.ruleForm.value!=null) {
						this.ruleForm.value = this.ruleForm.value.replace(new RegExp(this.$base.url,"g"),"");
					}
					var objcross = this.$storage.getObj('crossObj');
					if(!this.ruleForm.id) {
						delete this.ruleForm.userid
					}
					await this.$refs["ruleForm"].validate(async valid => {
						if (valid) {
							if(this.type=='cross'){
								var statusColumnName = this.$storage.get('statusColumnName');
								var statusColumnValue = this.$storage.get('statusColumnValue');
								if(statusColumnName!='') {
									var obj = this.$storage.getObj('crossObj');
									if(statusColumnName && !statusColumnName.startsWith("[")) {
										for (var o in obj){
											if(o==statusColumnName){
												obj[o] = statusColumnValue;
											}
										}
										var table = this.$storage.get('crossTable');
										await this.$http({
											url: `${table}/update`,
											method: "post",
											data: obj
										}).then(({ data }) => {});
									}
								}
							}
							await this.$http({
								url: `config/${!this.ruleForm.id ? "save" : "update"}`,
								method: "post",
								data: this.ruleForm
							}).then(async ({ data }) => {
								if (data && data.code === 0) {
									this.$message({
										message: "操作成功",
										type: "success",
										duration: 1500,
										onClose: () => {
											this.parent.showFlag = true;
											this.parent.addOrUpdateFlag = false;
											this.parent.configCrossAddOrUpdateFlag = false;
											this.parent.search();
										}
									});
								} else {
									this.$message.error(data.msg);
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
				this.parent.showFlag = true;
				this.parent.addOrUpdateFlag = false;
				this.parent.configCrossAddOrUpdateFlag = false;
			},
			valueUploadChange(fileUrls) {
				this.ruleForm.value = fileUrls;
			},
		}
	};
</script>
<style lang="scss" scoped>
	.addEdit-block {
		padding: 30px 30px 30px 30px;
		background: #FDF7ED;
		width: 100%;
	}
	.add-update-preview {
		border-radius: 10px;
		padding: 40px 130px 30px 30px;
		box-shadow: 0px 3px 6px 1px rgba(0,0,0,0.10);
		margin: 0;
		background: #FEFEF6;
		display: flex;
		width: 100%;
		flex-wrap: wrap;
	}
	.amap-wrapper {
		width: 100%;
		height: 500px;
	}
	
	.search-box {
		position: absolute;
	}
	
	.el-date-editor.el-input {
		width: auto;
	}
	.add-update-preview ::v-deep .el-form-item {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(50% - 0px);
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
	.add-update-preview ::v-deep .el-form-item.editorBox {
		margin: 0 0 15px 0 ;
		display: flex;
		width: 100%;
	}
	.add-update-preview .el-form-item.editorBox ::v-deep .el-form-item__label {
		padding: 0 10px;
		color: #333333;
		white-space: nowrap;
		font-weight: 600;
		width: 180px;
		font-size: 16px;
		line-height: 64px;
		text-align: right;
		height: 64px;
	}
	
	.add-update-preview .el-form-item.editorBox ::v-deep .el-form-item__content {
		margin-left: auto !important;
		padding: 0;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview ::v-deep.el-form-item.editorBox .editor {
		border-radius: 4px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		max-width: 100% !important;
		align-content: flex-start;
		flex: 1;
		background: #fff;
		display: flex;
		align-items: flex-start;
		flex-wrap: wrap;
		height: auto;
	}
	.add-update-preview ::v-deep.el-form-item.editorBox .editor .ql-toolbar {
		background: none;
		width: 100%;
	}
	.add-update-preview ::v-deep.el-form-item.editorBox .editor .ql-container {
		background: none;
		width: 100%;
		min-height: 200px;
	}
	.add-update-preview ::v-deep.el-form-item.editorBox .editor .ql-container .ql-blank::before {
		color: #999;
	}
	
	.add-update-preview ::v-deep .el-form-item.textBox {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(100% - 0px);
	}
	.add-update-preview .el-form-item.textBox ::v-deep .el-form-item__label {
		padding: 0 10px;
		color: #333333;
		white-space: nowrap;
		font-weight: 500;
		width: 180px;
		font-size: 16px;
		line-height: 64px;
		text-align: right;
		height: 64px;
	}
	
	.add-update-preview .el-form-item.textBox ::v-deep .el-form-item__content {
		margin-left: auto !important;
		padding: 0;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview ::v-deep.el-form-item.textBox span.text {
		border: 1px solid #DADFE6;
		border-radius: 4px;
		padding: 12px 12px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		outline: none;
		color: #333;
		background: #fff;
		flex: 1;
		width: 100%;
		font-size: 16px;
		line-height: 30px;
		height: auto;
	}
	
	.add-update-preview .el-input {
		flex: 1;
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
	.add-update-preview .el-input ::v-deep .el-input__inner[readonly="readonly"] {
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
	.add-update-preview .el-input-number {
		text-align: left;
		flex: 1;
	}
	.add-update-preview .el-input-number ::v-deep .el-input__inner {
		text-align: left;
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
	.add-update-preview .el-input-number ::v-deep .is-disabled .el-input__inner {
		text-align: left;
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
	.add-update-preview .el-input-number ::v-deep .el-input-number__decrease {
		display: none;
	}
	.add-update-preview .el-input-number ::v-deep .el-input-number__increase {
		display: none;
	}
	.add-update-preview .el-select {
		width: auto;
		min-width: 100%;
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
	.add-update-preview .el-select ::v-deep .is-disabled .el-input__inner {
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
	.add-update-preview .el-date-editor {
		width: auto;
		min-width: 100%;
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
	.add-update-preview .el-date-editor ::v-deep .el-input__inner[readonly="readonly"] {
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
	.add-update-preview .viewBtn {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 20px;
		outline: none;
		color: #FFFFFF;
		background: #f3a213;
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .viewBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .downBtn {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 20px;
		outline: none;
		color: #FFFFFF;
		background: #f3a213;
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .downBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .unBtn {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 20px;
		outline: none;
		color: #333;
		background: #eee;
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .unBtn:hover {
		opacity: 0.8;
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
	
	.add-update-preview ::v-deep .upload .upload-img {
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
	.add-update-preview ::v-deep .el-upload__tip {
		padding: 0 10px;
		color: #666;
		font-size: 15px;
	}
	.add-update-preview ::v-deep .el-form-item.fileupload {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(50% - 0px);
	}
	.add-update-preview .el-form-item.fileupload ::v-deep .el-form-item__label {
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
	
	.add-update-preview .el-form-item.fileupload ::v-deep .el-form-item__content {
		margin-left: auto !important;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview .el-form-item.fileupload ::v-deep .el-upload-dragger {
		border-radius: 4px;
		padding: 0px 22px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		outline: none;
		color: #333;
		background: #fff;
		width: 100%;
		font-size: 24px;
		border-color: #e8e9eb;
		border-width: 1px;
		border-style: solid;
		height: auto;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger ::v-deep .el-icon-upload {
		padding: 0;
		margin: 10px 0 0;
		color: #f3a213;
		font-size: 62px;
		line-height: 1;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger ::v-deep .el-upload__text {
		padding: 0;
		margin: 0 0 20px;
		color: #606266;
		line-height: 1;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger ::v-deep .el-upload__text em {
		color: #409EFF;
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
	.add-update-preview .el-textarea ::v-deep .el-textarea__inner[readonly="readonly"] {
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
	.add-update-preview ::v-deep .el-form-item.btn {
		padding: 0;
		margin: 10px 0 10px 180px;
		background: none;
		display: flex;
		width: auto;
		justify-content: center;
		flex-wrap: wrap;
		.btn1 {
			border: 1px solid #555555;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 0;
			box-shadow: inset 0px 3px 6px 1px #FFFFFF;
			outline: none;
			background: #555;
			width: auto;
			min-width: 130px;
			height: 47px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 16px;
				height: 40px;
			}
		}
		.btn1:hover {
			opacity: 0.8;
		}
		.btn2 {
			border: 1px solid #136df3;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 0;
			box-shadow: inset 0px 3px 6px 1px #FFFFFF;
			outline: none;
			background: #136df3;
			width: auto;
			min-width: 130px;
			height: 47px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 16px;
				height: 40px;
			}
		}
		.btn2:hover {
			opacity: 0.8;
		}
		.btn3 {
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
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 16px;
				height: 40px;
			}
		}
		.btn3:hover {
			opacity: 0.8;
		}
		.btn4 {
			border: 1px solid #989898;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 0;
			box-shadow: inset 0px 3px 6px 1px #FFFFFF;
			outline: none;
			background: #989898;
			width: auto;
			min-width: 130px;
			height: 47px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 16px;
				height: 40px;
			}
		}
		.btn4:hover {
			opacity: 0.8;
		}
		.btn5 {
			border: 1px solid #1392f3;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 0;
			box-shadow: inset 0px 3px 6px 1px #FFFFFF;
			outline: none;
			background: #1392f3;
			width: auto;
			min-width: 130px;
			height: 47px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 16px;
				height: 40px;
			}
		}
		.btn5:hover {
			opacity: 0.8;
		}
	}
	.add-update-preview .el-form-item.btn ::v-deep .el-form-item__label {
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
	
	.add-update-preview .el-form-item.btn ::v-deep .el-form-item__content {
	}
</style>

