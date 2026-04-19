<template>
	<div class="hero-home">
		<el-carousel
			ref="heroCarousel"
			class="hero-carousel"
			height="100%"
			:interval="5000"
			arrow="never"
			indicator-position="none"
			@change="onSlideChange"
		>
			<el-carousel-item v-for="(slide, idx) in slides" :key="idx">
				<div class="hero-slide" :class="'slide-' + idx">
					<div class="hero-overlay"></div>
					<div class="hero-body">
						<span class="hero-tag">{{ slide.tag }}</span>
						<h1 class="hero-title" v-html="slide.title"></h1>
						<p class="hero-desc">{{ slide.desc }}</p>
						<div class="hero-actions">
							<button
								v-for="(btn, bi) in slide.buttons"
								:key="bi"
								:class="['hero-btn', btn.type]"
								@click="handleNav(btn.route)"
							>{{ btn.label }}</button>
						</div>
					</div>
				</div>
			</el-carousel-item>
		</el-carousel>

		<div class="hero-controls">
			<div class="hero-indicators">
				<span
					v-for="(slide, idx) in slides"
					:key="idx"
					:class="['indicator', { active: currentSlide === idx }]"
					@click="goSlide(idx)"
				></span>
			</div>
			<div class="hero-arrows">
				<button class="arrow-btn" @click="prevSlide">‹</button>
				<button class="arrow-btn" @click="nextSlide">›</button>
			</div>
		</div>

		<div class="hero-stats">
			<div class="stat-card">
				<div class="stat-num">{{ usedcarCount }}</div>
				<div class="stat-label">车源总数</div>
			</div>
			<div class="stat-divider"></div>
			<div class="stat-card">
				<div class="stat-num">{{ yonghuCount }}</div>
				<div class="stat-label">注册用户</div>
			</div>
			<div class="stat-divider"></div>
			<div class="stat-card">
				<div class="stat-num">{{ forecastCount }}</div>
				<div class="stat-label">预测记录</div>
			</div>
		</div>
	</div>
</template>

<script>
import router from "@/router/router-static";

export default {
	data() {
		return {
			currentSlide: 0,
			yonghuCount: 0,
			usedcarCount: 0,
			forecastCount: 0,
			slides: [
				{
					tag: "USED CAR DATA PLATFORM",
					title: "二手车销售数据<br/>采集与趋势分析系统",
					desc: "整合全网车源数据，智能采集、清洗与分析，助您全面掌握二手车市场动态。",
					buttons: [
						{ label: "浏览车源", route: "/usedcar", type: "primary" },
						{ label: "数据大屏", route: "/board", type: "outline" },
					],
				},
				{
					tag: "AI PRICE PREDICTION",
					title: "智能价格预测，<br/>让估价更精准",
					desc: "基于机器学习算法，结合品牌、车龄、里程、城市等多维特征，为您提供科学的价格预测与区间分析。",
					buttons: [
						{ label: "开始预测", route: "/usedcarforecast", type: "primary" },
						{ label: "查看趋势", route: "/board", type: "outline" },
					],
				},
				{
					tag: "REAL-TIME DATA CRAWLING",
					title: "实时数据采集，<br/>掌握市场脉搏",
					desc: "一键爬取汽车之家等主流平台真实车源数据，自动入库清洗，保持数据新鲜度。",
					buttons: [
						{ label: "进入车源管理", route: "/usedcar", type: "primary" },
						{ label: "系统简介", route: "/systemintro", type: "outline" },
					],
				},
			],
		};
	},
	mounted() {
		this.init();
		this.getyonghuCount();
		this.getusedcarCount();
		this.getforecastCount();
	},
	methods: {
		init() {
			if (this.$storage.get("Token")) {
				this.$http({
					url: `${this.$storage.get("sessionTable")}/session`,
					method: "get",
				}).then(({ data }) => {
					if (data && data.code != 0) {
						router.push({ name: "login" });
					}
				});
			} else {
				router.push({ name: "login" });
			}
		},
		handleNav(route) {
			if (route === "/board") {
				window.open(this.$router.resolve({ path: route }).href, "_blank");
			} else {
				this.$router.push(route);
			}
		},
		onSlideChange(idx) {
			this.currentSlide = idx;
		},
		goSlide(idx) {
			this.$refs.heroCarousel.setActiveItem(idx);
		},
		prevSlide() {
			this.$refs.heroCarousel.prev();
		},
		nextSlide() {
			this.$refs.heroCarousel.next();
		},
		getyonghuCount() {
			this.$http({ url: "yonghu/count", method: "get" }).then(({ data }) => {
				if (data && data.code == 0) this.yonghuCount = data.data;
			});
		},
		getusedcarCount() {
			this.$http({ url: "usedcar/count", method: "get" }).then(({ data }) => {
				if (data && data.code == 0) this.usedcarCount = data.data;
			});
		},
		getforecastCount() {
			this.$http({ url: "usedcarforecast/count", method: "get" }).then(({ data }) => {
				if (data && data.code == 0) this.forecastCount = data.data;
			}).catch(() => {});
		},
	},
};
</script>

<style lang="scss" scoped>
.hero-home {
	position: relative;
	width: 100%;
	height: calc(100vh - 140px);
	min-height: 400px;
	overflow: hidden;
	border-radius: 18px;
}

.hero-carousel {
	width: 100%;
	height: 100% !important;
}

.hero-carousel ::v-deep .el-carousel__container {
	height: 100% !important;
}

/* === 三张幻灯片的背景 === */
.hero-slide {
	position: relative;
	width: 100%;
	height: 100%;
	background-size: cover;
	background-position: center;
	display: flex;
	align-items: center;
}

.slide-0 {
	background:
		linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.05) 100%),
		url('https://th.bing.com/th/id/R.f17c8cb3ae37c787d5fe4cd617fb411e?rik=XgQUVORwO1QtsQ&pid=ImgRaw&r=0') center/cover no-repeat;
}

.slide-1 {
	background:
		linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.05) 100%),
		url('https://img-baofun.zhhainiao.com/fs/28ce386ae04b860a50c576f5556505a6.jpg') center/cover no-repeat;
}

.slide-2 {
	background:
		linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.05) 100%),
		url('https://cdn.svipaigc.com/bizi/2025/08/20250807055211-68943f0b6549a-scaled.jpg') center/cover no-repeat;
}

.hero-overlay {
	position: absolute;
	inset: 0;
	background: linear-gradient(
		to right,
		rgba(0, 0, 0, 0.45) 0%,
		rgba(0, 0, 0, 0.15) 55%,
		rgba(0, 0, 0, 0.05) 100%
	);
	z-index: 1;
}

.hero-body {
	position: relative;
	z-index: 2;
	padding: 0 7vw;
	max-width: 720px;
}

.hero-tag {
	display: inline-block;
	color: #e8652a;
	font-size: 12px;
	font-weight: 700;
	letter-spacing: 0.18em;
	margin-bottom: 16px;
	text-transform: uppercase;
}

.hero-title {
	margin: 0 0 18px;
	color: #fff;
	font-size: clamp(28px, 3.8vw, 48px);
	font-weight: 800;
	line-height: 1.2;
	letter-spacing: -0.01em;
	text-shadow: 0 3px 18px rgba(0, 0, 0, 0.5);
}

.hero-desc {
	margin: 0 0 30px;
	color: rgba(255, 255, 255, 0.72);
	font-size: clamp(13px, 1.2vw, 16px);
	line-height: 1.75;
	max-width: 500px;
}

.hero-actions {
	display: flex;
	gap: 14px;
	flex-wrap: wrap;
}

.hero-btn {
	padding: 12px 32px;
	border-radius: 40px;
	font-size: 14px;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.25s ease;
	letter-spacing: 0.02em;

	&.primary {
		border: none;
		background: #fff;
		color: #1a1a1a;
		box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);

		&:hover {
			background: #e8652a;
			color: #fff;
			transform: translateY(-2px);
			box-shadow: 0 6px 22px rgba(232, 101, 42, 0.4);
		}
	}

	&.outline {
		border: 1.5px solid rgba(255, 255, 255, 0.45);
		background: transparent;
		color: #fff;

		&:hover {
			border-color: #fff;
			background: rgba(255, 255, 255, 0.1);
			transform: translateY(-2px);
		}
	}
}

/* 指示器 + 箭头 */
.hero-controls {
	position: absolute;
	bottom: 70px;
	left: 0;
	right: 0;
	z-index: 10;
	padding: 0 7vw;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.hero-indicators {
	display: flex;
	gap: 8px;
}

.indicator {
	width: 30px;
	height: 3px;
	border-radius: 2px;
	background: rgba(255, 255, 255, 0.28);
	cursor: pointer;
	transition: all 0.35s ease;

	&.active {
		width: 44px;
		background: #e8652a;
	}
}

.hero-arrows {
	display: flex;
	gap: 10px;
}

.arrow-btn {
	width: 42px;
	height: 42px;
	border-radius: 50%;
	border: 1.5px solid rgba(255, 255, 255, 0.3);
	background: transparent;
	color: rgba(255, 255, 255, 0.75);
	font-size: 20px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.25s ease;

	&:hover {
		border-color: #fff;
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}
}

/* 底部统计 */
.hero-stats {
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	z-index: 10;
	display: flex;
	justify-content: center;
	align-items: center;
	padding: 14px 0;
	background: linear-gradient(to top, rgba(0, 0, 0, 0.55) 0%, transparent 100%);
}

.stat-card {
	padding: 6px 44px;
	text-align: center;
}

.stat-num {
	color: #fff;
	font-size: 24px;
	font-weight: 700;
	line-height: 1.2;
}

.stat-label {
	color: rgba(255, 255, 255, 0.55);
	font-size: 12px;
	margin-top: 3px;
	font-weight: 500;
}

.stat-divider {
	width: 1px;
	height: 32px;
	background: rgba(255, 255, 255, 0.15);
}

@media (max-width: 768px) {
	.hero-home {
		height: calc(100vh - 120px);
		border-radius: 12px;
	}

	.hero-body {
		padding: 0 5vw;
	}

	.hero-controls {
		bottom: 60px;
		padding: 0 5vw;
	}

	.hero-btn {
		padding: 10px 24px;
		font-size: 13px;
	}

	.stat-card {
		padding: 6px 20px;
	}

	.stat-num {
		font-size: 20px;
	}

	.hero-arrows {
		display: none;
	}
}
</style>
