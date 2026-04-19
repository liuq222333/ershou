<template>
	<div class="front-page front-pay-page">
		<header class="front-page-header">
			<div class="front-page-header__title">
				<span class="front-pill">Secure Payment</span>
				<h1>确认支付方式</h1>
				<p>将支付页也统一到当前前台的绿色轻透风格里，保留原来的支付提交逻辑，只重新组织视觉层级。</p>
			</div>
			<div class="front-page-header__meta">
				<span class="front-pill">订单 {{ obj.orderid || obj.id || '--' }}</span>
				<span class="front-pill">业务 {{ table || '--' }}</span>
			</div>
		</header>

		<section class="front-page-grid front-page-grid--two">
			<div class="front-section">
				<div class="front-section__head">
					<div>
						<h2>订单摘要</h2>
						<p>在提交支付前，再确认一次订单主体、金额与业务来源。</p>
					</div>
				</div>

				<el-alert title="确认支付前请先核对订单信息" type="success" :closable="false"></el-alert>

				<div class="front-pay-summary">
					<div class="front-pay-summary__item">
						<span>支付对象</span>
						<strong>{{ obj.name || obj.title || (obj.brand ? obj.brand + ' ' + (obj.model1 || '') : '待支付项目') || '--' }}</strong>
					</div>
					<div class="front-pay-summary__item">
						<span>支付金额</span>
						<strong>{{ obj.discountprice || obj.price || obj.money || '--' }}</strong>
					</div>
					<div class="front-pay-summary__item">
						<span>订单编号</span>
						<strong>{{ obj.orderid || obj.id || '--' }}</strong>
					</div>
					<div class="front-pay-summary__item">
						<span>支付状态</span>
						<strong>{{ obj.ispay || '待支付' }}</strong>
					</div>
				</div>
			</div>

			<div class="front-section">
				<div class="front-section__head">
					<div>
						<h2>支付渠道</h2>
						<p>保留原有渠道选项，用更紧凑、更清晰的方式呈现。</p>
					</div>
				</div>

				<div class="front-pay-option-grid">
					<div :class="['front-pay-option', { 'is-active': type === '微信支付' }]" @click="type = '微信支付'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="微信支付">微信支付</el-radio>
						</div>
						<img src="@/assets/weixin.png" alt="微信支付">
					</div>
					<div :class="['front-pay-option', { 'is-active': type === '支付宝支付' }]" @click="type = '支付宝支付'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="支付宝支付">支付宝支付</el-radio>
						</div>
						<img src="@/assets/zhifubao.png" alt="支付宝支付">
					</div>
					<div :class="['front-pay-option', { 'is-active': type === '建设银行' }]" @click="type = '建设银行'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="建设银行">建设银行</el-radio>
						</div>
						<img src="@/assets/jianshe.png" alt="建设银行">
					</div>
					<div :class="['front-pay-option', { 'is-active': type === '农业银行' }]" @click="type = '农业银行'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="农业银行">农业银行</el-radio>
						</div>
						<img src="@/assets/nongye.png" alt="农业银行">
					</div>
					<div :class="['front-pay-option', { 'is-active': type === '中国银行' }]" @click="type = '中国银行'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="中国银行">中国银行</el-radio>
						</div>
						<img src="@/assets/zhongguo.png" alt="中国银行">
					</div>
					<div :class="['front-pay-option', { 'is-active': type === '交通银行' }]" @click="type = '交通银行'">
						<div class="front-pay-option__meta">
							<el-radio v-model="type" label="交通银行">交通银行</el-radio>
						</div>
						<img src="@/assets/jiaotong.png" alt="交通银行">
					</div>
				</div>

				<div class="front-detail-actions">
					<el-button type="primary" @click="submitTap">确认支付</el-button>
					<el-button @click="back">返回</el-button>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
	// import { Message } from "element-ui";
	export default {
		data() {
			return {
				name: "",
				account: "",
				type: "",
				table: "",
				obj: ""
			};
		},
		mounted() {
			let table = localStorage.getItem("paytable");
			let obj = JSON.parse(localStorage.getItem("payObject"));
			this.table = table;
			this.obj = obj;
		},
		methods: {
			submitTap() {
				if (!this.type) {
					this.$message.error("请选择支付方式");
					return;
				}
				this.$confirm(`确定支付?`, "提示", {
					confirmButtonText: "确定",
					cancelButtonText: "取消",
					type: "warning"
				}).then(async () => {
					this.obj.ispay = "已支付";
					let hasBackType = false
					let changeType = true
					let errMsg = ''
					this.$http.post(`${this.table}/update`, this.obj).then(async res => {
						if (res.data && res.data.code === 0) {
							this.$message({
								message: "支付成功",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.$router.go(-1);
								}
							});
						} else {
							this.$message.error(res.data.msg);
						}
					});
				});
			},
			back() {
				this.$router.go(-1);
			}
		}
	};
</script>

<style lang="scss" scoped>
.front-pay-summary {
	display: grid;
	gap: 14px;
	margin-top: 18px;
}

.front-pay-summary__item {
	display: flex;
	justify-content: space-between;
	gap: 16px;
	padding: 16px 18px;
	border-radius: 16px;
	background: rgba(47, 123, 87, 0.06);
	border: 1px solid rgba(47, 123, 87, 0.08);
}

.front-pay-summary__item span {
	color: var(--front-text-soft);
	font-size: 13px;
}

.front-pay-summary__item strong {
	font-size: 15px;
	font-weight: 700;
	color: var(--front-text);
}

.front-pay-option-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 14px;
}

.front-pay-option {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding: 18px;
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.7);
	border: 1px solid rgba(47, 123, 87, 0.1);
	cursor: pointer;
	transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

.front-pay-option:hover,
.front-pay-option.is-active {
	transform: translateY(-2px);
	border-color: rgba(47, 123, 87, 0.24);
	box-shadow: 0 18px 36px rgba(29, 42, 34, 0.08);
}

.front-pay-option__meta {
	display: flex;
	align-items: center;
	gap: 12px;
	font-size: 14px;
	font-weight: 600;
}

.front-pay-option img {
	width: 118px;
	height: 42px;
	object-fit: contain;
}

.front-pay-option {
	::v-deep .el-radio__label {
		font-weight: 600;
		color: var(--front-text);
	}
}

@media (max-width: 900px) {
	.front-pay-option-grid {
		grid-template-columns: 1fr;
	}
}
</style>
