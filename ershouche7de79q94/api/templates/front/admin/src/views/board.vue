<template>
	<div class="apple-board" ref="roleMenuBox">
		<div class="ambient-layer"></div>
		<header class="board-header">
			<div class="header-left">
				<div class="product-title">{{this.$project.projectName}}</div>
				<div class="product-sub">Used Car Intelligence Dashboard</div>
			</div>
			<div class="header-right">
				<span class="status-chip"><i class="live-dot"></i>Live</span>
				<span class="date-chip">{{ dates }}</span>
				<button class="back-btn" type="button" @click="backClick">{{frontType==1?'返回首页':'返回管理'}}</button>
			</div>
		</header>

		<main class="board-body">
			<section class="left-column">
				<article class="glass hero-panel" id="usedcarTable">
					<div class="panel-head">
						<span class="panel-index">A1</span>
						<div>
							<h2>车辆展示</h2>
							<p>Vehicle Showcase</p>
						</div>
						<span class="counter" v-if="usedcarList.length">{{currentCarIndex + 1}} / {{usedcarList.length}}</span>
					</div>

					<div class="hero-main" @mouseenter="pauseCarousel" @mouseleave="resumeCarousel" v-if="currentCar">
						<div class="hmi-stage">
							<div class="hmi-meta hmi-meta-price">
								<span>现价</span>
								<strong>¥ {{currentCar.discountprice || '—'}}</strong>
							</div>
							<div class="hmi-meta hmi-meta-year">
								<span>年份</span>
								<strong>{{currentCar.vehicleage || '—'}}</strong>
							</div>
							<div class="hmi-meta hmi-meta-km">
								<span>里程</span>
								<strong>{{currentCar.kilometer || '—'}} km</strong>
							</div>
							<div class="hmi-meta hmi-meta-city">
								<span>城市</span>
								<strong>{{currentCar.city || '—'}}</strong>
							</div>

							<div class="hmi-center">
								<transition name="car-fade" mode="out-in">
									<img :key="currentCarIndex" :src="getCarImg(currentCar)" class="hero-image hmi-image" />
								</transition>
							</div>

							<div class="hero-brand">{{currentCar.brand}} · {{currentCar.model1}}</div>
						</div>
					</div>
					<div class="hero-empty" v-else>暂无车辆数据</div>

					<div class="hero-controls">
						<button type="button" class="nav-btn" @click="prevCar">‹</button>
						<div class="dot-wrap">
							<button
								v-for="(item, idx) in usedcarList.slice(0, 10)"
								:key="idx"
								type="button"
								class="dot"
								:class="{active: idx === currentCarIndex % 10}"
								@click="goToCar(idx)">
							</button>
						</div>
						<button type="button" class="nav-btn" @click="nextCar">›</button>
					</div>
				</article>

				<article class="glass kpi-panel">
					<div class="kpi-item">
						<div class="kpi-left">
							<span class="kpi-icon"><i class="el-icon-user-solid"></i></span>
							<div class="kpi-copy">
								<em>用户总数</em>
								<span>USERS</span>
							</div>
						</div>
						<strong>{{yonghuCount}}</strong>
					</div>
					<div class="kpi-item">
						<div class="kpi-left">
							<span class="kpi-icon"><i class="el-icon-truck"></i></span>
							<div class="kpi-copy">
								<em>二手车总数</em>
								<span>VEHICLES</span>
							</div>
						</div>
						<strong>{{usedcarCount}}</strong>
					</div>
				</article>

				<article class="glass forecast-panel">
					<div class="panel-head compact">
						<span class="panel-index">A2</span>
						<div>
							<h2>价格预测</h2>
							<p>Forecast Input</p>
						</div>
					</div>
					<div class="forecast-grid">
						<label class="input-wrap">
							<span>品牌</span>
							<input v-model="forecastForm.brand" placeholder="例如：大众" />
						</label>
						<label class="input-wrap">
							<span>型号</span>
							<input v-model="forecastForm.model1" placeholder="例如：朗逸" />
						</label>
						<label class="input-wrap">
							<span>年份</span>
							<input v-model="forecastForm.vehicleage" placeholder="例如：2021" />
						</label>
						<label class="input-wrap">
							<span>里程</span>
							<input v-model="forecastForm.kilometer" placeholder="例如：3.2" />
						</label>
						<label class="input-wrap full">
							<span>城市</span>
							<input v-model="forecastForm.city" placeholder="例如：上海" />
						</label>
						<div class="result-card">
							<span>预测价</span>
							<strong>{{form.discountprice || '—'}}</strong>
						</div>
						<button class="predict-btn" type="button" @click="forecastClick">开始预测</button>
					</div>
				</article>
			</section>

			<section class="right-column">
				<article class="glass chart-carousel" @mouseenter="pauseChartCarousel" @mouseleave="resumeChartCarousel">
					<div class="panel-head compact">
						<span class="panel-index">B</span>
						<div>
							<h2>{{currentChart.name}}</h2>
							<p>Data Insights</p>
						</div>
						<span class="counter">{{activeChartIndex + 1}} / {{chartPanels.length}}</span>
					</div>

					<div class="chart-stage-wrap">
						<div
							class="chart-stage"
							v-for="(chart, ci) in chartPanels"
							:key="chart.id"
							:class="{active: ci === activeChartIndex}">
							<div :id="chart.id" class="chart-canvas"></div>
						</div>
					</div>

					<div class="chart-controls">
						<button type="button" class="nav-btn" @click="prevChart">‹</button>
						<div class="dot-wrap">
							<button
								v-for="(chart, idx) in chartPanels"
								:key="chart.id + '-dot'"
								type="button"
								class="dot"
								:class="{active: idx === activeChartIndex}"
								@click="goToChart(idx)">
							</button>
						</div>
						<button type="button" class="nav-btn" @click="nextChart">›</button>
					</div>
				</article>

				<article class="glass table-panel table-panel-side">
					<div class="panel-head compact">
						<span class="panel-index">A3</span>
						<div>
							<h2>二手车预测列表</h2>
							<p>Prediction Records</p>
						</div>
					</div>
					<div class="table-wrap" id="usedcarforecastTable">
						<el-table :data="usedcarforecastList" border :stripe="false" class="forecast-table">
							<el-table-column :resizable="false" :sortable="false" prop="brand" label="品牌"></el-table-column>
							<el-table-column :resizable="false" :sortable="false" prop="model1" label="型号"></el-table-column>
							<el-table-column :resizable="false" :sortable="false" prop="discountprice" label="预测价"></el-table-column>
							<el-table-column :resizable="false" :sortable="false" prop="vehicleage" label="年份"></el-table-column>
							<el-table-column :resizable="false" :sortable="false" prop="kilometer" label="里程"></el-table-column>
							<el-table-column :resizable="false" :sortable="false" prop="city" label="城市"></el-table-column>
						</el-table>
					</div>
				</article>
			</section>
		</main>
	</div>
</template>

<script>
	import * as echarts from 'echarts'
	import chinaJson from "@/components/echarts/china.json";
	import {
		Loading
	} from 'element-ui';
	import router from '@/router/router-static'
	export default {
		data() {
			return {
				line: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":15,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"dashed","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"show":false},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":3000,"symbol":"circle","animationEasing":"backOut","showSymbol":true,"symbolSize":5,"itemStyle":{"color":"","borderColor":"rgba(156,196,224,0.3)","borderWidth":12},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","trigger":"axis","textStyle":{"color":"#fff"}},"title":{"show":false}},
				line2: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"dashed","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"show":false},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":3000,"symbol":"circle","animationEasing":"backOut","showSymbol":true,"symbolSize":5,"itemStyle":{"color":"","borderColor":"rgba(156,196,224,0.3)","borderWidth":12},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","trigger":"axis","textStyle":{"color":"#fff"}},"title":{"show":false}},
				line3: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":15,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":"","fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"dashed","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"show":false},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":6000,"symbol":"circle","animationEasing":"backOut","areaStyle":{"color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(156,196,224,0.5)"},{"offset":1,"color":"rgba(0,212,255,0)"}],"type":"linear"},"shadowBlur":10,"shadowColor":"rgba(0, 0, 0, 0.1)"},"showSymbol":true,"symbolSize":5,"itemStyle":{"color":"","borderColor":"rgba(84,112,198,0.3)","borderWidth":12},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","trigger":"axis","textStyle":{"color":"#fff"}},"title":{"show":false}},
				line4: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":15,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":"","fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"dashed","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"show":false},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":3000,"symbol":"circle","animationEasing":"backOut","areaStyle":{"color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(156,196,224,0.5)"},{"offset":1,"color":"rgba(0,212,255,0)"}],"type":"linear"},"shadowBlur":10,"shadowColor":"rgba(0, 0, 0, 0.1)"},"showSymbol":true,"symbolSize":5,"itemStyle":{"color":"","borderColor":"rgba(156,196,224,0.3)","borderWidth":12},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","trigger":"axis","textStyle":{"color":"#fff"}},"title":{"show":false}},
				line5: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":15,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":"","fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"dashed","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"shadowBlur":0,"itemHeight":14,"show":true,"icon":"roundRect","type":"scroll","top":"top","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":20,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":0,"itemGap":10,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"center","width":"80%","textStyle":{"textBorderWidth":0,"color":"#959aa5","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"grid":{"right":"20","top":"40","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":6000,"symbol":"circle","animationEasing":"backOut","areaStyle":{"color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(0, 251, 255, 0)"},{"offset":1,"color":"rgba(0, 251, 255, 0)"}],"type":"linear"},"shadowBlur":10,"shadowColor":"rgba(0, 0, 0, 0.1)"},"showSymbol":true,"symbolSize":5,"itemStyle":{"color":"","borderColor":"rgba(84,112,198,0.3)","borderWidth":8},"animation":true},"series2":{"barWidth":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"color":"","borderRadius":[0,0,0,0],"shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(156,196,224,1)"},{"offset":1,"color":"rgba(90,138,168,1)"}],"type":"linear"},"barCategoryGap":"20%"},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","trigger":"axis","textStyle":{"color":"#fff"}},"title":{"show":false}},
				bar: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":12,"backgroundColor":"transparent","borderColor":"#666","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":"","fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":30,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"padding":0,"itemGap":10,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#666","shadowOffsetY":0,"orient":"horizontal","shadowBlur":0,"bottom":"auto","itemHeight":14,"show":false,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","top":"bottom","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"center","borderWidth":0,"width":"80%","itemWidth":20,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":12,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":3000,"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"borderRadius":[0,0,0,0],"shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"animationEasing":"backOut","color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(156,196,224,1)"},{"offset":1,"color":"rgba(90,138,168,1)"}],"type":"linear"},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"title":{"show":false},"base":{"animate":true,"interval":6000}},
				bar2: {"backgroundColor":"transparent","yAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":6,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"truncate","borderRadius":0,"borderWidth":0,"width":120,"fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":true,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#666","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,0.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"xAxis":{"axisLabel":{"borderType":"solid","rotate":0,"padding":0,"shadowOffsetX":0,"margin":4,"backgroundColor":"transparent","borderColor":"#000","shadowOffsetY":0,"color":"#959aa5","shadowBlur":0,"show":true,"inside":false,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"width":"","fontSize":12,"lineHeight":24,"shadowColor":"transparent","fontWeight":"normal","height":""},"axisTick":{"show":false,"length":5,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"inside":false},"splitLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":false},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"cap":"butt","color":"#959aa5","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"rgba(0,0,0,.5)"},"show":true},"splitArea":{"show":false,"areaStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"rgba(25,25,25,.3)","opacity":1,"shadowBlur":10,"shadowColor":"rgba(0,0,0,.5)"}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"padding":0,"itemGap":10,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#666","shadowOffsetY":0,"orient":"horizontal","shadowBlur":0,"bottom":"auto","itemHeight":14,"show":false,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","top":"bottom","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"center","borderWidth":0,"width":"80%","itemWidth":20,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":12,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"grid":{"right":"20","top":"20","left":"20","bottom":"20","containLabel":true},"series":{"animationDuration":3000,"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"borderRadius":[0,0,0,0],"shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"animationEasing":"backOut","color":{"x":0,"y":0,"y2":0,"x2":1,"colorStops":[{"offset":0,"color":"rgba(156,196,224,1)"},{"offset":1,"color":"rgba(90,138,168,1)"}],"type":"linear"},"animation":true},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"title":{"show":false},"base":{"animate":true,"interval":2000}},
				bar3: {"polar":{"radius":[20,"80%"]},"backgroundColor":"transparent","radiusAxis":{"type":"category"},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"show":false},"series":{"barWidth":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#fff","shadowOffsetY":0,"color":{"x":0,"y":0,"y2":1,"x2":0,"colorStops":[{"offset":0,"color":"rgba(156,196,224,1)"},{"offset":1,"color":"rgba(90,138,168,1)"}],"type":"linear"},"shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"coordinateSystem":"polar","label":{"formatter":"{b}: {c}","show":true,"position":"middle"},"barCategoryGap":"20%"},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"},"trigger":"axis"},"title":{"show":false},"base":{"animate":false,"interval":2000},"angleAxis":{"startAngle":90}},
				pie: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"shadowBlur":0,"itemHeight":8,"show":true,"icon":"roundRect","type":"scroll","top":"bottom","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":16,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":0,"itemGap":6,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"center","width":"100%","textStyle":{"textBorderWidth":0,"color":"#959aa5","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"series":{"animationDuration":4000,"animationEasing":"quadraticOut","top":30,"left":30,"bottom":30,"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"right":30,"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"#fff","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","formatter":"{d}%","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"inside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"#fff","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"radius":[0,"75%"],"animation":true}},
				pie2: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"shadowBlur":0,"itemHeight":8,"show":true,"icon":"roundRect","type":"scroll","top":"top","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":12,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":0,"itemGap":4,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"center","width":"100%","textStyle":{"textBorderWidth":0,"color":"#959aa5","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"series":{"animationDuration":4000,"animationEasing":"quadraticOut","avoidLabelOverlap":false,"itemStyle":{"borderRadius":10,"borderColor":"#111","borderWidth":2},"label":{"color":"inherit","show":false,"position":"outside"},"labelLine":{"show":false},"padAngle":10,"radius":["30%","75%"],"animation":true}},
				pie3: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"shadowBlur":0,"itemHeight":8,"show":true,"icon":"roundRect","type":"scroll","top":"bottom","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":14,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":0,"itemGap":10,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"center","width":"100%","textStyle":{"textBorderWidth":0,"color":"#959aa5","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#111","shadowOffsetY":0,"color":"","borderRadius":5,"shadowBlur":0,"borderWidth":4,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"#fff","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"#fff","shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"radius":["20%","75%"]}},
				funnel: {"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"grid":{"right":"30","top":"30","left":"30","bottom":"30"},"legend":{"shadowOffsetX":0,"borderColor":"#666","shadowOffsetY":0,"shadowBlur":0,"itemHeight":8,"show":true,"icon":"roundRect","type":"scroll","top":"top","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":12,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":0,"itemGap":4,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"center","width":"100%","textStyle":{"textBorderWidth":0,"color":"#959aa5","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#000","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"gap":2},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"title":{"show":false}},
				funnel2: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"padding":0,"itemGap":0,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"orient":"vertical","shadowBlur":0,"bottom":"auto","itemHeight":8,"show":true,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"top":"auto","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"left","borderWidth":0,"width":"auto","itemWidth":14,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":20,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#000","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"gap":2}},
				funnel3: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"padding":0,"itemGap":0,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"orient":"vertical","shadowBlur":0,"bottom":"auto","itemHeight":8,"show":true,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"top":"auto","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"left","borderWidth":0,"width":"auto","itemWidth":14,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":20,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#000","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"gap":2}},
				funnel4: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"padding":0,"itemGap":0,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"orient":"vertical","shadowBlur":0,"bottom":"auto","itemHeight":8,"show":true,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"top":"auto","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"left","borderWidth":0,"width":"auto","itemWidth":14,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":20,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#000","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"gap":2}},
				funnel5: {"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"legend":{"padding":0,"itemGap":0,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"orient":"vertical","shadowBlur":0,"bottom":"auto","itemHeight":8,"show":true,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"top":"auto","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"left","borderWidth":0,"width":"auto","itemWidth":14,"textStyle":{"textBorderWidth":0,"color":"inherit","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":20,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"series":{"itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"#000","shadowOffsetY":0,"color":"","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"#000"},"label":{"borderType":"solid","rotate":0,"padding":0,"textBorderWidth":0,"backgroundColor":"transparent","borderColor":"#fff","color":"","show":true,"textShadowColor":"transparent","distanceToLabelLine":5,"ellipsis":"...","overflow":"none","borderRadius":0,"borderWidth":0,"fontSize":12,"lineHeight":18,"textShadowOffsetX":0,"position":"outside","textShadowOffsetY":0,"textBorderType":"solid","textBorderColor":"#fff","textShadowBlur":0},"labelLine":{"show":true,"length":10,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"shadowBlur":0,"width":1,"type":"solid","opacity":1,"shadowColor":"#000"},"length2":14,"smooth":false},"gap":2}},
				map: {"tooltip":{"formatter":"{b} : {c}","trigger":"item"},"backgroundColor":"transparent","title":{"borderType":"solid","padding":10,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"shadowBlur":0,"bottom":"auto","show":true,"right":"auto","top":"auto","borderRadius":0,"left":"left","borderWidth":0,"textStyle":{"textBorderWidth":0,"color":"#fff","textShadowColor":"transparent","fontSize":14,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"#ccc","textShadowBlur":0},"shadowColor":"transparent"},"legend":{"padding":5,"itemGap":10,"shadowOffsetX":0,"backgroundColor":"transparent","borderColor":"#ccc","shadowOffsetY":0,"orient":"horizontal","shadowBlur":0,"bottom":"auto","itemHeight":14,"show":false,"icon":"roundRect","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","top":"auto","borderRadius":0,"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"left":"right","borderWidth":0,"width":"auto","itemWidth":25,"textStyle":{"textBorderWidth":0,"color":"#fff","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0},"shadowColor":"rgba(0,0,0,.3)","height":"auto"},"series":{"aspectScale":0.75,"itemStyle":{"areaColor":"#a8d5fc"},"zoom":1.8,"label":{"emphasis":{"show":true,"textStyle":{"color":"#3ba372"}},"normal":{"color":"#3ba372","show":true}},"roam":true,"showLegendSymbol":false,"animation":false},"visualMap":{"min":0,"text":["High","Low"],"inRange":{"color":["#358aff","#39d3f9","#f2993d","#fce74e","#80d6eb","#a896ef","#5366f6","rgba(30, 144, 255, 1)","rgba(0, 251, 255, 1)","rgba(255, 120, 0, 1)","#f9d354","#e3faf7","#3c8883","#dda882"]},"max":80000,"calculable":true,"seriesIndex":[0]}},
				boardBase: {"funnelNum":6,"lineNum":8,"radarNum":8,"gaugeNum":8,"barNum":10,"pieNum":10},
				gauge: {"tooltip":{"formatter":"{b} : {c}","trigger":"item"},"backgroundColor":"transparent","color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"title":{"show":false},"series":{"pointer":{"offsetCenter":[0,"10%"],"icon":"path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z","width":8,"length":"80%"},"axisLine":{"lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"opacity":0.5,"shadowBlur":1,"shadowColor":"#000"},"roundCap":true},"anchor":{"show":true,"itemStyle":{"color":"inherit"},"size":18,"showAbove":true},"emphasis":{"disabled":false},"progress":{"show":true,"roundCap":true,"overlap":true},"splitNumber":10,"detail":{"formatter":"{value}","backgroundColor":"inherit","color":"#fff","borderRadius":3,"width":20,"fontSize":12,"height":12},"title":{"color":"#ccc","fontSize":12},"animation":true}},
				radar: {"backgroundColor":"transparent","radar":{"splitLine":{"lineStyle":{"color":"rgba(255, 255, 255, 0.1)"}},"name":{"textStyle":{"color":"#ddd","fontSize":13,"fontWeight":"bold"}},"shape":"circle","axisLine":{"lineStyle":{"color":"rgba(255, 255, 255, 0.2)"}},"splitArea":{"areaStyle":{"color":["rgba(0, 0, 0, 0.1)","rgba(20, 20, 20, 0.1)"],"opacity":1}}},"color":["#9cc4e0","#cfe0f0","#6b94b8","#a8c5e0","#7fb3d8","#5a8aa8","#3d6b8a"],"legend":{"shadowOffsetX":0,"borderColor":"#ccc","shadowOffsetY":0,"shadowBlur":0,"itemHeight":14,"show":true,"icon":"roundRect","type":"scroll","top":"auto","lineStyle":{"shadowOffsetX":0,"shadowOffsetY":0,"color":"inherit","shadowBlur":0,"width":"auto","type":"inherit","opacity":1,"shadowColor":"transparent"},"borderWidth":0,"itemWidth":25,"shadowColor":"rgba(0,0,0,.3)","height":"auto","padding":5,"itemGap":10,"backgroundColor":"transparent","orient":"horizontal","bottom":"auto","itemStyle":{"borderType":"solid","shadowOffsetX":0,"borderColor":"inherit","shadowOffsetY":0,"color":"inherit","shadowBlur":0,"borderWidth":0,"opacity":1,"shadowColor":"transparent"},"right":"auto","borderRadius":0,"left":"right","width":"auto","textStyle":{"textBorderWidth":0,"color":"#fff","textShadowColor":"transparent","ellipsis":"...","overflow":"none","fontSize":12,"lineHeight":24,"textShadowOffsetX":0,"textShadowOffsetY":0,"textBorderType":"solid","fontWeight":500,"textBorderColor":"transparent","textShadowBlur":0}},"series":{},"tooltip":{"backgroundColor":"rgba(8,12,21,0.9)","textStyle":{"color":"#fff"}},"title":{"top":"bottom","show":false,"left":"left"}},
				myChart0: null,
				chartPanels: [
					{id:'usedcarChart1', num:'B1', name:'品牌统计'},
					{id:'usedcarChart2', num:'B2', name:'型号统计'},
					{id:'usedcarChart3', num:'B3', name:'城市统计'},
					{id:'usedcarChart4', num:'B4', name:'年份统计'},
					{id:'usedcarChart5', num:'B5', name:'价格分布'},
					{id:'usedcarChart6', num:'B6', name:'里程统计'}
				],
				activeChartIndex: 0,
				chartTimer: null,
				currentCarIndex: 0,
				usedcarList: [],
				usedcarTimer: null,
				usedcarforecastList: [],
				usedcarforecastTimer: null,
				systemIntroductionDetail: null,
				dates: '',
				yonghuCount: 0,
				usedcarCount: 0,
				forecastForm: {},
				form: {},
				frontType: 0,
				usedcarchartQuery1: {},
				usedcarChartOptions1: [],
				usedcarchartQuery2: {},
				usedcarChartOptions2: [],
				usedcarchartQuery3: {},
				usedcarChartOptions3: [],
				usedcarchartQuery4: {},
				usedcarChartOptions4: [],
				usedcarchartQuery5: {},
				usedcarChartOptions5: [],
				usedcarchartQuery6: {},
				usedcarChartOptions6: [],
			};
		},
		mounted(){
			if(this.$route.query.frontType&&this.$route.query.frontType==1) {
				this.frontType = 1
			}
			this.init();
			this.getusedcarList()
			this.getusedcarforecastList()
			this.startChartCarousel()
		},
		computed: {
			sessionForm() {
				return JSON.parse(this.$storage.getObj('userForm'))
			},
			currentCar() {
				if (!this.usedcarList || !this.usedcarList.length) return null
				return this.usedcarList[this.currentCarIndex % this.usedcarList.length]
			},
			currentChart() {
				return this.chartPanels[this.activeChartIndex] || { num: '', name: '' }
			},
		},
		created() {
			this.$nextTick(()=>{
				this.times()
				setTimeout(()=>{
					this.getyonghuCount();
					this.getusedcarCount();
					this.usedcarChat1();
					this.usedcarChat2();
					this.usedcarChat3();
					this.usedcarChat4();
					this.usedcarChat5();
					this.usedcarChat6();
				},500)
			})
		},
		beforeDestroy() {
			clearInterval(this.usedcarTimer)
			clearInterval(this.usedcarforecastTimer)
			clearInterval(this.chartTimer)
		},
		methods:{
			changeStatQuery(arr) {
				if(arr.length==1) {
					if(arr[0] == 'users'&&this.$storage.get("sessionTable")=='users') {
						return true
					}
				}
				let role = this.$storage.get('role')
				for(let x in arr) {
					if(arr[x] == role) {
						return true
					}
				}
				return false
			},
			forecastClick(row) {
				this.$confirm(`是否进行数据预测?`, "提示", {
					confirmButtonText: "确定",
					cancelButtonText: "取消",
					type: "warning"
				}).then(()=>{
					let loading = null
					loading = Loading.service({
						target: this.$refs['roleMenuBox'],
						fullscreen: false,
						text: '数据预测中...'
					})
					this.$http({
						url: 'usedcarforecast/save',
						method: 'post',
						data: this.forecastForm
					}).then(res=>{
						if(res.data&&res.data.code==0){
							this.forecastForm.id = res.data.data
							this.$http({
								url: 'usedcarforecast/forecast',
								method: 'post',
								data: this.forecastForm
							}).then(obj=>{
								if(obj.data&&obj.data.code==0){
									this.$http({
										url: 'usedcarforecast/info/' + res.data.data,
										method: 'get'
									}).then(rs2=>{
										if(rs2.data&&rs2.data.code==0){
											if (loading) loading.close()
											this.$message({
												message: "数据预测完成！",
												type: "success",
												duration: 1500,
												onClose: () => {
													this.form = rs2.data.data
												}
											});
										}
									})
									
								}
							})
						}
					})
					
				})
			},
			getCarImg(item) {
				if (!item || !item.imgurl) return ''
				if (item.imgurl.substring(0, 4) === 'http') {
					if (item.imgurl.split(',w').length > 1) return item.imgurl
					return item.imgurl.split(',')[0]
				}
				return this.$base.url + item.imgurl.split(',')[0]
			},
			nextCar() {
				if (!this.usedcarList.length) return
				this.currentCarIndex = (this.currentCarIndex + 1) % this.usedcarList.length
			},
			prevCar() {
				if (!this.usedcarList.length) return
				this.currentCarIndex = (this.currentCarIndex - 1 + this.usedcarList.length) % this.usedcarList.length
			},
			goToCar(idx) {
				this.currentCarIndex = idx
			},
			pauseCarousel() {
				clearInterval(this.usedcarTimer)
			},
			resumeCarousel() {
				this.startCarousel()
			},
			startCarousel() {
				clearInterval(this.usedcarTimer)
				this.usedcarTimer = setInterval(() => {
					this.nextCar()
				}, 5000)
			},
			nextChart() {
				if (!this.chartPanels.length) return
				this.activeChartIndex = (this.activeChartIndex + 1) % this.chartPanels.length
			},
			prevChart() {
				if (!this.chartPanels.length) return
				this.activeChartIndex = (this.activeChartIndex - 1 + this.chartPanels.length) % this.chartPanels.length
			},
			goToChart(idx) {
				this.activeChartIndex = idx
			},
			startChartCarousel() {
				clearInterval(this.chartTimer)
				this.chartTimer = setInterval(() => {
					this.nextChart()
				}, 4500)
			},
			pauseChartCarousel() {
				clearInterval(this.chartTimer)
			},
			resumeChartCarousel() {
				this.startChartCarousel()
			},
			getusedcarList() {
				let params = {
					page: 1,
					limit: 20,
				}
				this.$http({
					url: "usedcar/page",
					method: "get",
					params: params
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.usedcarList = data.data.list
						this.startCarousel()
					}
				});
			},
			getusedcarforecastList() {
				let params = {
					page: 1,
					limit: 20,
				}
				this.$http({
					url: "usedcarforecast/page",
					method: "get",
					params: params
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.usedcarforecastList = data.data.list;
						let div = document.getElementById('usedcarforecastTable')
						var scrollTop = -1
						function move() {
							if (div){
								if(div.scrollTop==scrollTop){
									div.scrollTo({
										top: 0, 
										behavior: "smooth"
									});
									return false
								}
								scrollTop = div.scrollTop
								div.scrollTo({ 
									top: div.scrollTop + 40, 
									behavior: "smooth"
								});
							}
								
						}
						this.usedcarforecastTimer = setInterval(move, 2000);
						div.addEventListener('mouseenter', e => {
							e.stopPropagation()
							clearInterval(this.usedcarforecastTimer);
						})
						div.addEventListener('mouseleave', e => {
							e.stopPropagation()
							this.usedcarforecastTimer = setInterval(move, 2000);
						})
					}
				});
			},
			backClick(){
				if(this.frontType==1) {
					window.location.href = `${this.$base.indexUrl}`
					return false
				}
				this.$router.replace({ path: "/" });
			},
			getNeonBarStyle(direction = 'vertical') {
				const isHorizontal = direction === 'horizontal'
				return {
					color: new echarts.graphic.LinearGradient(
						isHorizontal ? 0 : 0,
						isHorizontal ? 0 : 1,
						isHorizontal ? 1 : 0,
						isHorizontal ? 0 : 0,
						[
							{ offset: 0, color: 'rgba(122, 201, 164, 0.98)' },
							{ offset: 0.6, color: 'rgba(86, 176, 136, 0.95)' },
							{ offset: 1, color: 'rgba(60, 145, 108, 0.92)' },
						]
					),
					borderRadius: [8, 8, 0, 0],
					shadowBlur: 8,
					shadowColor: 'rgba(91, 162, 132, 0.28)',
				}
			},
			getNeonAxisLabelStyle() {
				return {
					color: '#5c7069',
					fontSize: 12,
				}
			},
			myChartInterval(type, xAxisData, seriesData, myChart) {
				this.$nextTick(() => {
					setInterval(() => {
						let xAxis = xAxisData.shift()
						xAxisData.push(xAxis)
						let series = seriesData.shift()
						seriesData.push(series)
			
						if (type == 1) {
							myChart.setOption({
								xAxis: [{
									data: xAxisData
								}],
								series: [{
									data: seriesData
								}]
							});
						}
						if (type == 2) {
							myChart.setOption({
								yAxis: [{
									data: xAxisData
								}],
								series: [{
									data: seriesData
								}]
							});
						}
					}, 6000);
				})
			},
			wordclouds(wordcloudData,echartsId) {
				let wordcloud = {"maskImage":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAALW0lEQVR4Xu2dCawmRRHHgUhAQERFBEFdEIxGNCIgxJiwckNACAtGVORp5FIieAAqoMgpKIiAeGDisou4cYOIxAMhihFBYEU0REFAN5GoyG00WW7/v7c9m7fvfe97c1TNdM90JZVvj5nqqur/9FldveYaw6J1Ze7B4u3FWwfm3+4LfI9+rxA/PBS3rDkQQ98hOw8UHxAqfZzZ/9B//lB8jfjnfffPEABwhCrxxBIVP72uH9I/fFF8QZ9B0GcArBUq/iT9blSzEp8OIDhXv/+rKSPq1/oMgPfL84uNvH+m5JxqJCsqMX0FwB7y8rfE84y8/W/JoSv5kZG8aMT0EQAbyruXid9t7OVrAwgeNJbbqbg+AmB3efR6J69+XHIvdJLdidi+AWADefEHYroAD7pZQg8S96YV6BsADlPlLPKo+Skyj9Gfv+FcRmvi+wQAbOHrZ8HHk1gcWiD+r2chbcnuEwBomq9qyXEfUDlWU8yWVB5dTJ8AQIUw92+Drg6twPNtFOZZRl8AsFdo/tfzdNY02XQDdDlJU18AwKDsqJZrgl1DBp1JUx8AwE4fff8mLdcEewO0Ate1XK5pcX0AwPnyyCdMvVJe2Df16NHlH4/vydQBsF34+rfsyLXsEdAK3NRR+Y2LTR0Ap8sDXe/SES/wycY10ZGAlAHwuvD1b9uR74pi/6Y/sAZxZ8d61Co+ZQAQ6EHETgx0hpT4XAyKVNUhVQC8UoYyB9+pqsFOz98VWoF7neS7iU0VAMfKIxe7eaWeYFqk8+q92t1bKQLgxeHr37U7t40s+dbQChBVnAylCIAJefc7kXqYlulrkeo2Uq3UAPCC8PXvH6mTfxFagSci1W+GWqkB4BBZ8P3InftB6bcwch1XqZcaAK6U5odG7lwih1kdfCZyPSfVSwkA+4bmf50EHEtE8tIE9EwKAIR6fzgFp0rH74nfm4KuqbQAu4Sv/6UpOFU6rgjdwE9i1zcVABCLf1zszpym37f1d04TRU0pAGAHeZCAj1dH7cmZyj0SWoFfxax3CgA4Sw78bMxOHKPbV/V/x8ese6wA4ITP68Vk8fiKeNOYnThGN6aCHCRhs+hu8eOx2dElANjR22oW3iw2Rxnp80/JuV/81xG/nRw38wYAYdpFJRO2Nb3Cyc+TaeUpo1GgKP7tOS8nWQFg8zFfc6rNt5fPq8pdPqbVaNylVAXA1L75jVP6afrr/DVXrdpmz1P5ZDdjfEF2M8YY/J3f0svQcwGA3TfSqnHyZr54XjOd89steIBFKECwTPw78RLxrC3FOACw7Pp58RYtKJ2L8PPAvySaqTSnp2a0DKMAQFP+dfGEn05ZcgceoHtgq3q1MwzTAbC3HiDGnTQrmfrnAcYLRC9zunmSpgKAXHp/FudRe/8qfqpFdAnvFDNOWA0ARNkS05ap/x54QCZuI15RtADsXS8Ur91/27OFwQMf0+/FAIAm/3Lxntk1g/LAr2XtwQBgZ/EtgzI9G1t44BgA0OX5+lwV3XrgIgDwUzHTv0zD88AyAMDckHX9TMPzwD0AgPPt84Zne7YYDwAANgzemt0xSA88BAAIXd5nkOZno+8CAGTZ4Gx7puF5YBEA4CYtbsnKNDwPTK4DQHkgOLzKJzZgmwIAxK4Tfp1pOB4gSOSUAgCEfv1e3HXKteG4v1tLiUJ+k3j51HiA+fqHL4u5VjVTfz1AqPkJ4slM59Mjgki8zNIw0b+Z+umB1S6+GhUT+D7Z/QXxa/tp/2CtelSWE+R7yVQPzBYVzJUo5OF9zWDd1S/D/yNziAXksOpqNC4s/EOhJchh4WmDgXsN+PLZ9p9Bcx0MIcEB3UFfD2umXbVza/9k+PJnzWA6FwAoggsRAEHbN3LMbV5+YpwHng2Vf/a4h8oAgPc/KmZMkEqOngyNlc0+dTaWygIAIeTooSUgV2+muD1AxQOAOakKABDG3TyAIK8TzOnazh6gyafyS50QrgoArGIVCRC8sDMTc8GzeYDBHtM9Bn+lqA4AEPyZAIJ8kKSUm1t5iGkeXz7TvtJUFwAUcEoAwVqlS8sPenmABR6+fBZ8KlETAFAQiDutUon5YWsPcD8Blc9Sb2VqCgDeZzzQ9dVtlQ3vyQskfeAj5P7CWtQUABTKOAAQMC7I1J4HSEXLl0/qudpkAQAKJ6sIIDixtib5xSoe4Mocvvy/V3lp1LNWAED2+gEEyd6i2dSZLb2/OFQ+cZyNyRIAKLOhmFWo1DJ7N3ZkSwK4h4Bmn3w/JmQNAJRiv4DuIGcbMamiVUK4K4lmfzK1ixV5AADdXh5AQKLkTM09QPwelc9BXlPyAgBKknmEluBIU42HJ4xLqGj2/+BhuicA0JdoIkBAdFGm6h74cfjyOcDrQt4AQOl85qB+1b1Br5r2+dNVaQMAlPkXMWnJMpX3AIc38Bl5/dyoDQBwRwDTljbKcnNUR4I5p/Ebz7LbqBTSz13naUSPZU/Itss97WsDAB+RAUndqO3p8Iqyz9DzzADcqA0A5DR09avP/QbSNgBwjex/V30fDPrN22X92zw90AYAchq6+jVIkAczgVrBHmWK9QbAq6TEveIUbvwu468untlJhd7mVbA3AOZL8V96KT8QuWRyZyzgQt4A4N4hrn3PVN8DzAKYDbiQNwDOkdafdtF8OEJZB5jwMtcbAEulONfOZarvAVYCWRF0IW8A3CGtt3PRfDhC2QtgJsDegDl5AuAV0pYZwIvMtR6eQD6iOz3M9gTA26Ww60aGh0MilUk3epWHbp4AIM+Q60aGh0MilclA+lwP3TwBQCSQ60aGh0MilckhENL1mJMnAL4rbVnEyNTcAyym7dpczEwJngC4VcW5bmR4OCRSmZwA2lr8lLV+XgB4iRRlBvAya4UHLI97nf5kbb8XAHaQomxlZrLzAFvq19qJWynJCwDvkWy3DQxrJyQij/xM5in9vQBA9hC3DYxEKsxazUslkHR9puQFAI4vT5hqmoURWGt+wacXALiY2G0DY6BYuF92MxMwJQ8AkCeAcwCcDcxk6wE2hcyOhqOaBwDeLLkuBxltfZmkNLoA0zMWHgA4SEq6bFwkWWW2SpNzwfSMhQcAyBPksnFh68skpV0orbnyxYw8APAlafcpMw19Bf0s9KmkxOcUc+y0TAruaKmkBwBYrdrPUkkHWQRXkPP4hiCb0TXAPdChLEuRRAWZBth4ACDmTSAuyr5SzE7lKAIAXJoVaxzjA9KNsxZm5AGAGE8C3TKl4h+bw3scYmEbGyDsZuZpG0HEB5pe3+MBgJgWgciZTzpVglMerlgHJL9k1H2yeKOK73o+blpnpsKC1Yv0e5inB0rIflDP0MzT3DfNr0OaFloDeF6Jsj0fYdC6j2UBHgDociOIgImi4osBnpW/CHItgNDVtTlnSgfTxNweAHiLlOQi6raJJVKcs8S54J0lnxlDF3sdh1rb5wEA/H+1uK0p1eMqiz6eK1FL3ZNjBBDsAwjmGzSz6IedW4r5NSMvAOwrDUltysaQF/1RgovmnulRF7SxCi1mDN7xjyTcND9o6wUAKsPzXOAVkk9zv7yLWh9RJrOEk8THi5k9WBNTa04HmbdwngDgajmuorfsK2+UPNbCXY5JGdQamVGJhJowkFWIYPVvD/FvDWWuEuUJAArZVnyaeEFD5elOaO7Jm5sC7SUlixlDk0u1WFMh/b71jKY1AFAQLcH1YkbPVYmVL5r6hWLz5q+qMjWeZ0+EHAl8CFUJ2w8R31T1xSrPe7cAhS7stJEthJTnZSKFGOmypcz254oqBkX4LLZPiLlEowwQqHhsZwXT3fa2AFDUCwMkolroEnAGfSYj6eVi+jrQTobsG8PfI6zPRiqxRnK4mJYBYGA7vwzy6ONZtWQdw73iCyv+DzyVlSePahBpAAAAAElFTkSuQmCC","option":{"tooltip":{"show":false},"backgroundColor":"transparent","series":[{"sizeRange":[9,32],"layoutAnimation":true,"shape":"circle","data":[{"name":"花鸟市场","value":1446},{"name":"汽车","value":928},{"name":"视频","value":906},{"name":"电视","value":825},{"name":"Lover Boy 88","value":514},{"name":"动漫","value":486},{"name":"音乐","value":53},{"name":"直播","value":163},{"name":"广播电台","value":86},{"name":"戏曲曲艺","value":17},{"name":"演出票务","value":6},{"name":"给陌生的你听","value":1},{"name":"资讯","value":1437},{"name":"商业财经","value":422},{"name":"娱乐八卦","value":353},{"name":"军事","value":331},{"name":"科技资讯","value":313},{"name":"社会时政","value":307},{"name":"时尚","value":43},{"name":"网络奇闻","value":15},{"name":"旅游出行","value":438},{"name":"景点类型","value":957},{"name":"国内游","value":927},{"name":"远途出行方式","value":908},{"name":"酒店","value":693},{"name":"关注景点","value":611},{"name":"旅游网站偏好","value":512},{"name":"出国游","value":382},{"name":"交通票务","value":312},{"name":"旅游方式","value":187},{"name":"旅游主题","value":163},{"name":"港澳台","value":104},{"name":"本地周边游","value":3},{"name":"小卖家","value":1331},{"name":"全日制学校","value":941},{"name":"基础教育科目","value":585},{"name":"考试培训","value":473},{"name":"语言学习","value":358},{"name":"留学","value":246},{"name":"K12课程培训","value":207},{"name":"艺术培训","value":194},{"name":"技能培训","value":104},{"name":"IT培训","value":87},{"name":"高等教育专业","value":63},{"name":"家教","value":48},{"name":"体育培训","value":23},{"name":"职场培训","value":5},{"name":"金融财经","value":1328},{"name":"银行","value":765},{"name":"股票","value":452},{"name":"保险","value":415},{"name":"贷款","value":253},{"name":"基金","value":211},{"name":"信用卡","value":180},{"name":"外汇","value":138},{"name":"P2P","value":116},{"name":"贵金属","value":98},{"name":"债券","value":93},{"name":"网络理财","value":92},{"name":"信托","value":90},{"name":"征信","value":76},{"name":"期货","value":76},{"name":"公积金","value":40},{"name":"银行理财","value":36},{"name":"银行业务","value":30},{"name":"典当","value":7},{"name":"海外置业","value":1},{"name":"汽车","value":1309},{"name":"汽车档次","value":965},{"name":"汽车品牌","value":900},{"name":"汽车车型","value":727},{"name":"购车阶段","value":461},{"name":"二手车","value":309},{"name":"汽车美容","value":260},{"name":"新能源汽车","value":173},{"name":"汽车维修","value":155},{"name":"租车服务","value":136},{"name":"车展","value":121},{"name":"违章查询","value":76},{"name":"汽车改装","value":62},{"name":"汽车用品","value":37},{"name":"路况查询","value":32},{"name":"汽车保险","value":28},{"name":"陪驾代驾","value":4},{"name":"网络购物","value":1275},{"name":"做我的猫","value":1088},{"name":"只想要你知道","value":907},{"name":"团购","value":837},{"name":"比价","value":201},{"name":"海淘","value":195},{"name":"移动APP购物","value":179},{"name":"支付方式","value":119},{"name":"代购","value":43},{"name":"体育健身","value":1234},{"name":"体育赛事项目","value":802},{"name":"运动项目","value":405},{"name":"体育类赛事","value":337},{"name":"健身项目","value":199},{"name":"健身房健身","value":78},{"name":"运动健身","value":77},{"name":"家庭健身","value":36},{"name":"健身器械","value":29},{"name":"办公室健身","value":3},{"name":"商务服务","value":1201},{"name":"法律咨询","value":508},{"name":"化工材料","value":147},{"name":"广告服务","value":125},{"name":"会计审计","value":115},{"name":"人员招聘","value":101},{"name":"印刷打印","value":66},{"name":"知识产权","value":32},{"name":"翻译","value":22},{"name":"安全安保","value":9},{"name":"公关服务","value":8},{"name":"商旅服务","value":2},{"name":"展会服务","value":2},{"name":"特许经营","value":1},{"name":"休闲爱好","value":1169},{"name":"收藏","value":412},{"name":"摄影","value":393},{"name":"温泉","value":230},{"name":"博彩彩票","value":211},{"name":"美术","value":207},{"name":"书法","value":139},{"name":"DIY手工","value":75},{"name":"舞蹈","value":23},{"name":"钓鱼","value":21},{"name":"棋牌桌游","value":17},{"name":"KTV","value":6},{"name":"密室","value":5},{"name":"采摘","value":4},{"name":"电玩","value":1},{"name":"真人CS","value":1},{"name":"轰趴","value":1},{"name":"家电数码","value":1111},{"name":"手机","value":885},{"name":"电脑","value":543},{"name":"大家电","value":321},{"name":"家电关注品牌","value":253},{"name":"网络设备","value":162},{"name":"摄影器材","value":149},{"name":"影音设备","value":133},{"name":"办公数码设备","value":113},{"name":"生活电器","value":67},{"name":"厨房电器","value":54},{"name":"智能设备","value":45},{"name":"个人护理电器","value":22},{"name":"服饰鞋包","value":1047},{"name":"服装","value":566},{"name":"饰品","value":289},{"name":"鞋","value":184},{"name":"箱包","value":168},{"name":"奢侈品","value":137},{"name":"母婴亲子","value":1041},{"name":"孕婴保健","value":505},{"name":"母婴社区","value":299},{"name":"早教","value":103},{"name":"奶粉辅食","value":66},{"name":"童车童床","value":41},{"name":"关注品牌","value":271},{"name":"宝宝玩乐","value":30},{"name":"母婴护理服务","value":25},{"name":"纸尿裤湿巾","value":16},{"name":"妈妈用品","value":15},{"name":"宝宝起名","value":12},{"name":"童装童鞋","value":9},{"name":"胎教","value":8},{"name":"宝宝安全","value":1},{"name":"宝宝洗护用品","value":1},{"name":"软件应用","value":1018},{"name":"系统工具","value":896},{"name":"理财购物","value":440},{"name":"生活实用","value":365},{"name":"影音图像","value":256},{"name":"社交通讯","value":214},{"name":"手机美化","value":39},{"name":"办公学习","value":28},{"name":"应用市场","value":23},{"name":"母婴育儿","value":14},{"name":"游戏","value":946},{"name":"手机游戏","value":565},{"name":"PC游戏","value":353},{"name":"网页游戏","value":254},{"name":"游戏机","value":188},{"name":"模拟辅助","value":166},{"name":"个护美容","value":942},{"name":"护肤品","value":177},{"name":"彩妆","value":133},{"name":"美发","value":80},{"name":"香水","value":50},{"name":"个人护理","value":46},{"name":"美甲","value":26},{"name":"SPA美体","value":21},{"name":"花鸟萌宠","value":914},{"name":"绿植花卉","value":311},{"name":"狗","value":257},{"name":"其他宠物","value":131},{"name":"水族","value":125},{"name":"猫","value":122},{"name":"动物","value":81},{"name":"鸟","value":67},{"name":"宠物用品","value":41},{"name":"宠物服务","value":26},{"name":"书籍阅读","value":913},{"name":"网络小说","value":483},{"name":"关注书籍","value":128},{"name":"文学","value":105},{"name":"报刊杂志","value":77},{"name":"人文社科","value":22},{"name":"建材家居","value":907},{"name":"装修建材","value":644},{"name":"家具","value":273},{"name":"家居风格","value":187},{"name":"家居家装关注品牌","value":140},{"name":"家纺","value":107},{"name":"厨具","value":47},{"name":"灯具","value":43},{"name":"家居饰品","value":29},{"name":"家居日常用品","value":10},{"name":"生活服务","value":883},{"name":"物流配送","value":536},{"name":"家政服务","value":108},{"name":"摄影服务","value":49},{"name":"搬家服务","value":38},{"name":"物业维修","value":37},{"name":"婚庆服务","value":24},{"name":"二手回收","value":24},{"name":"鲜花配送","value":3},{"name":"维修服务","value":3},{"name":"殡葬服务","value":1},{"name":"求职创业","value":874},{"name":"创业","value":363},{"name":"目标职位","value":162},{"name":"目标行业","value":50},{"name":"兼职","value":21},{"name":"期望年薪","value":20},{"name":"实习","value":16},{"name":"雇主类型","value":10},{"name":"星座运势","value":789},{"name":"星座","value":316},{"name":"算命","value":303},{"name":"解梦","value":196},{"name":"风水","value":93},{"name":"面相分析","value":47},{"name":"手相","value":32},{"name":"公益","value":90}],"keepAspect":false,"type":"wordCloud","rotationRange":[-90,90],"gridSize":8,"shrinkToFit":false,"top":"center","left":"center","width":"80%","emphasis":{"focus":"self","textStyle":{"textShadowColor":"#333","textShadowBlur":4}},"drawOutOfBound":false,"rotationStep":45,"textStyle":{"color":"function(){return\"rgb(\"+[Math.round(Math.floor(Math.random() * (100 - 255)) + 255),Math.round(Math.floor(Math.random() * (100 - 255)) + 255),Math.round(Math.floor(Math.random() * (100 - 255)) + 255)].join(\",\")+\")\"}","fontWeight":500,"fontFamily":"sans-serif"},"height":"80%","maskImage":{}}]}}
				wordcloud = JSON.parse(JSON.stringify(wordcloud), (k, v) => {
					if(typeof v == 'string' && v.indexOf('function') > -1){
						return eval("(function(){return "+v+" })()")
					}
					return v;
				})
				wordcloud.option.series[0].data=wordcloudData;
				
				this.myChart0 = echarts.init(document.getElementById(echartsId));
				let myChart = this.myChart0
				let img = wordcloud.maskImage
			
				if (img) {
					var maskImage = new Image();
					maskImage.src = img
					maskImage.onload = function() {
						wordcloud.option.series[0].maskImage = maskImage
						myChart.clear()
						myChart.setOption(wordcloud.option)
					}
				} else {
					delete wordcloud.option.series[0].maskImage
					myChart.clear()
					myChart.setOption(wordcloud.option)
				}
			},
			getTimeStrToDay(game_over_timestamp) {
				if (game_over_timestamp == 0)
					return "";
				var date = new Date(parseInt(game_over_timestamp));
				var now = new Date();
				var hours = date.getHours() >= 10 ? date.getHours().toString() : "0" + date.getHours();
				var minutes = date.getMinutes() >= 10 ? date.getMinutes().toString() : "0" + date.getMinutes();
				var seconds = date.getSeconds() >= 10 ? date.getSeconds().toString() : "0" + date.getSeconds();
				let arr = ["日", "一", "二", "三", "四", "五", "六"];
				let d = arr[date.getDay()]
				return date.getFullYear() + "年" + (date.getMonth() + 1) + "月" + date.getDate() + '日' + ' ' + ' ' + '星期' + d  + ' ' + "  " + hours + ":" + minutes + ":" + seconds
			},
			times() {
				setInterval(()=>{
					let date = new Date().getTime()
					this.dates = this.getTimeStrToDay(date)
				}, 1000)
			},
			filterTime(time) {
				const date = new Date(time)
				const Y = date.getFullYear()
				const M = date.getMonth() + 1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1 
				const D = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
			  
				const H = date.getHours() < 10 ? '0' + date.getHours() : date.getHours() // 小时
				const I = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes() // 分钟
				const S = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds() // 秒
			  
				return `${Y}-${M}-${D} ${H}:${I}:${S}`
			},
			getSystemIntroduction() {
				this.$http({
					url: `systemintro/detail/1`,
					method: "get"
				}).then(({
					data
				}) => {
					if (data && data.code == 0) {
						this.systemIntroductionDetail = data.data
					}
				})
			},
			init(){
				if(this.$storage.get('Token')){
					this.$http({
						url: `${this.$storage.get('sessionTable')}/session`,
						method: "get"
					}).then(({ data }) => {
						if (data && data.code != 0) {
						router.push({ name: 'login' })
						}
					});
				}else{
					router.push({ name: 'login' })
				}
				this.getSystemIntroduction();
			},
			getyonghuCount() {
				this.$http({
					url: `yonghu/count`,
					method: "get"
				}).then(({
					data
				}) => {
					if (data && data.code == 0) {
						this.yonghuCount = data.data
					}
				})
			},
			getusedcarCount() {
				this.$http({
					url: `usedcar/count`,
					method: "get"
				}).then(({
					data
				}) => {
					if (data && data.code == 0) {
						this.usedcarCount = data.data
					}
				})
			},
			//统计接口1
			usedcarChat1(e=null) {
				this.$nextTick(()=>{

					var usedcarChart1 = echarts.init(document.getElementById("usedcarChart1"),'macarons');
					let params = {
					}
					this.$http({
						url: "usedcar/group/brand",
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.barNum){
									break;
								}
								xAxis.push(res[i].brand);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].brand
								})
							}
							var option = {};
							let titleObj = this.bar.title
							titleObj.text = '品牌统计'
							
							const legendObj = this.bar.legend
							
							let xAxisObj = this.bar.xAxis
							xAxisObj.type = 'category'
							xAxisObj.data = xAxis
							xAxisObj.axisLabel = Object.assign({}, xAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							xAxisObj.axisLine = Object.assign({}, xAxisObj.axisLine, {
								lineStyle: Object.assign({}, (xAxisObj.axisLine || {}).lineStyle, {
									color: 'rgba(142, 165, 155, 0.72)'
								})
							})
							
							
							let yAxisObj = this.bar.yAxis
							yAxisObj.type = 'value'
							yAxisObj.axisLabel = Object.assign({}, yAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							yAxisObj.splitLine = Object.assign({}, yAxisObj.splitLine, {
								lineStyle: Object.assign({}, (yAxisObj.splitLine || {}).lineStyle, {
									color: 'rgba(187, 204, 198, 0.8)'
								})
							})
							
							let seriesObj = {
								data: yAxis,
								type: 'bar'
							}
							seriesObj = Object.assign(seriesObj , this.bar.series)
							seriesObj.itemStyle = Object.assign({}, seriesObj.itemStyle, this.getNeonBarStyle('vertical'))
							seriesObj.emphasis = Object.assign({}, seriesObj.emphasis, {
								itemStyle: {
									shadowBlur: 12,
									shadowColor: 'rgba(92, 167, 136, 0.42)'
								}
							})
							const gridObj = this.bar.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: '{b} : {c}'
							}
							tooltipObj = Object.assign(tooltipObj , this.bar.tooltip?this.bar.tooltip:{})
							option = {
								backgroundColor: this.bar.backgroundColor,
								color: ['#79c9a4', '#5cb88f', '#419e78'],
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								xAxis: xAxisObj,
								yAxis: yAxisObj,
								grid: gridObj,
								series: [seriesObj]
							};
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart1.setOption(option);
				
							this.myChartInterval(1, option.xAxis.data, option.series[0].data, usedcarChart1)

							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart1.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
			//统计接口2
			usedcarChat2(e=null) {
				this.$nextTick(()=>{

					var usedcarChart2 = echarts.init(document.getElementById("usedcarChart2"),'macarons');
					let params = {
					}
					this.$http({
						url: "usedcar/group/model1",
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.barNum){
									break;
								}
								xAxis.push(res[i].model1);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].model1
								})
							}
							var option = {};
							let titleObj = this.bar2.title
							titleObj.text = '型号统计'
							
							const legendObj = this.bar2.legend
							
							let xAxisObj = this.bar2.xAxis
							xAxisObj.type = 'value'
							xAxisObj.axisLabel = Object.assign({}, xAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							xAxisObj.splitLine = Object.assign({}, xAxisObj.splitLine, {
								lineStyle: Object.assign({}, (xAxisObj.splitLine || {}).lineStyle, {
									color: 'rgba(187, 204, 198, 0.8)'
								})
							})
							
							
							let yAxisObj = this.bar2.yAxis
							yAxisObj.type = 'category'
							yAxisObj.data = xAxis
							yAxisObj.axisLabel = Object.assign({}, yAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							yAxisObj.axisLine = Object.assign({}, yAxisObj.axisLine, {
								lineStyle: Object.assign({}, (yAxisObj.axisLine || {}).lineStyle, {
									color: 'rgba(142, 165, 155, 0.72)'
								})
							})
							let seriesObj = {
								data: yAxis,
								type: 'bar'
							}
							seriesObj = Object.assign(seriesObj , this.bar2.series)
							seriesObj.itemStyle = Object.assign({}, seriesObj.itemStyle, this.getNeonBarStyle('horizontal'), {
								borderRadius: [0, 8, 8, 0]
							})
							seriesObj.emphasis = Object.assign({}, seriesObj.emphasis, {
								itemStyle: {
									shadowBlur: 12,
									shadowColor: 'rgba(92, 167, 136, 0.42)'
								}
							})
							const gridObj = this.bar2.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: '{b} : {c}'
							}
							tooltipObj = Object.assign(tooltipObj , this.bar2.tooltip?this.bar2.tooltip:{})
							option = {
								backgroundColor: this.bar2.backgroundColor,
								color: ['#79c9a4', '#5cb88f', '#419e78'],
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								grid: gridObj,
								xAxis: xAxisObj,
								yAxis: yAxisObj,
								series: [seriesObj]
							};
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart2.setOption(option);
				
							this.myChartInterval(2, option.yAxis.data, option.series[0].data, usedcarChart2)

							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart2.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
			//统计接口3
			usedcarChat3(e=null) {
				this.$nextTick(()=>{

					var usedcarChart3 = echarts.init(document.getElementById("usedcarChart3"),'macarons');
					let params = {
					}
					this.$http({
						url: "usedcar/group/city",
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.barNum){
									break;
								}
								xAxis.push(res[i].city);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].city
								})
							}
							var option = {};
							let titleObj = this.bar3.title
							titleObj.text = '城市统计'
							
							const legendObj = this.bar3.legend
							
							let seriesObj = {
								data: yAxis,
								type: 'bar'
							}
							seriesObj = Object.assign(seriesObj , this.bar3.series)
							seriesObj.itemStyle = Object.assign({}, seriesObj.itemStyle, this.getNeonBarStyle('horizontal'), {
								borderRadius: 6
							})
							seriesObj.emphasis = Object.assign({}, seriesObj.emphasis, {
								itemStyle: {
									shadowBlur: 12,
									shadowColor: 'rgba(92, 167, 136, 0.42)'
								}
							})
							const gridObj = this.bar3.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: '{b} : {c}'
							}
							tooltipObj = Object.assign(tooltipObj , this.bar3.tooltip?this.bar3.tooltip:{})
							const polarObj = this.bar3.polar
							const angleAxisObj = this.bar3.angleAxis
							angleAxisObj.axisLabel = Object.assign({}, angleAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							angleAxisObj.axisLine = Object.assign({}, angleAxisObj.axisLine, {
								lineStyle: Object.assign({}, (angleAxisObj.axisLine || {}).lineStyle, {
									color: 'rgba(142, 165, 155, 0.72)'
								})
							})
							let radiusAxisObj = {
								data: xAxis
							}
							radiusAxisObj = Object.assign(radiusAxisObj,this.bar3.radiusAxis)
							radiusAxisObj.axisLabel = Object.assign({}, radiusAxisObj.axisLabel, this.getNeonAxisLabelStyle())
							option = {
								backgroundColor: this.bar3.backgroundColor,
								color: ['#79c9a4', '#5cb88f', '#419e78'],
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								grid: gridObj,
								polar: polarObj,
								angleAxis: angleAxisObj,
								radiusAxis: radiusAxisObj,
								series: [seriesObj]
							};
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart3.setOption(option);
				

							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart3.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
			//统计接口4
			usedcarChat4(e=null) {
				this.$nextTick(()=>{

					var usedcarChart4 = echarts.init(document.getElementById("usedcarChart4"),'macarons');
					let params = {
					}
					this.$http({
						url: "usedcar/group/vehicleage",
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.pieNum){
									break;
								}
								xAxis.push(res[i].vehicleage);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].vehicleage
								})
							}
							var option = {};
							let titleObj = this.pie.title
							titleObj.text = '年份统计'
							
							const legendObj = this.pie.legend
							
							let seriesObj = {
								type: 'pie',
								radius: '55%',
								center: ['50%', '60%'],
								data: pArray,
								emphasis: {
									itemStyle: {
										shadowBlur: 10,
										shadowOffsetX: 0,
										shadowColor: 'rgba(0, 0, 0, 0.5)'
									}
								}
							}
							seriesObj = Object.assign(seriesObj , this.pie.series)
							const gridObj = this.pie.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: '{b} : {c} ({d}%)'
							}
							tooltipObj = Object.assign(tooltipObj , this.pie.tooltip?this.pie.tooltip:{})
							option = {
								backgroundColor: this.pie.backgroundColor,
								color: this.pie.color,
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								grid: gridObj,
								series: [seriesObj]
							};
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart4.setOption(option);
				

							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart4.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
			//统计接口5
			usedcarChat5(e=null) {
				this.$nextTick(()=>{

					var usedcarChart5 = echarts.init(document.getElementById("usedcarChart5"),'macarons');
					let params = {
						order: 'desc',
					}
					this.$http({
						url: `usedcar/value/model1/discountprice`,
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.lineNum){
									break;
								}
								xAxis.push(res[i].model1);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].model1
								})
							}
							var option = {};
							let titleObj = this.line.title
							titleObj.text = '车辆现价'
							
							const legendObj = this.line.legend
							
							let xAxisObj = this.line.xAxis
							xAxisObj.type = 'category'
							xAxisObj.boundaryGap = false
							xAxisObj.data = xAxis
							
							
							let yAxisObj = this.line.yAxis
							yAxisObj.type = 'value'
							
							let seriesObj = {
								data: yAxis,
								type: 'line',
							}
							seriesObj = Object.assign(seriesObj , this.line.series)
							const gridObj = this.line.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: '{b} : {c}'
							}
							tooltipObj = Object.assign(tooltipObj , this.line.tooltip?this.line.tooltip:{})
							option = {
								backgroundColor: this.line.backgroundColor,
								color: this.line.color,
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								grid: gridObj,
								xAxis: xAxisObj,
								yAxis: yAxisObj,
								series: [seriesObj]
							};
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart5.setOption(option);


							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart5.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
			// 统计接口6
			usedcarChat6(e=null) {
				this.$nextTick(()=>{

					var usedcarChart6 = echarts.init(document.getElementById("usedcarChart6"),'macarons');
					let params = {
						order: 'desc',
					}
					this.$http({
						url: `usedcar/value/model1/kilometer`,
						method: "get",
						params
					}).then(({ data }) => {
						if (data && data.code === 0) {
							let res = data.data;
							// 统计图设置对了吗
							let xAxis = [];
							let yAxis = [];
							let pArray = []
							for(let i=0;i<res.length;i++){
								if(this.boardBase&&i==this.boardBase.funnelNum){
									break;
								}
								xAxis.push(res[i].model1);
								yAxis.push(parseFloat((res[i].total)));
								pArray.push({
									value: parseFloat((res[i].total)),
									name: res[i].model1
								})
							}
							var option = {};
							let titleObj = this.funnel.title
							titleObj.text = '里程统计'
							
							let legendObj = {
								data: xAxis,
							}
							legendObj = Object.assign(legendObj , this.funnel.legend)
							let seriesObj = {
								name: '里程统计',
								data: pArray,
								type: 'funnel',
								left: '10%',
								top: 60,
								bottom: 60,
								width: '80%',
								minSize: '0%',
								maxSize: '100%',
							}
							seriesObj = Object.assign(seriesObj , this.funnel.series)
							const gridObj = this.funnel.grid
							let tooltipObj = {
								trigger: 'item',
								formatter: "{b} : {c}"
							}
							tooltipObj = Object.assign(tooltipObj , this.funnel.tooltip?this.funnel.tooltip:{})
							option = {
								backgroundColor: this.funnel.backgroundColor,
								color: this.funnel.color,
								title: titleObj,
								legend: legendObj,
								tooltip: tooltipObj,
								grid: gridObj,
								series: seriesObj,
							}
							// 使用刚指定的配置项和数据显示图表。
							usedcarChart6.setOption(option);


							//根据窗口的大小变动图表
							window.addEventListener('resize', () => {
								usedcarChart6.resize();
							},false);
						}else{
							this.$message({
								message: data.msg,
								type: "warning",
								duration: 1500,
							})
						}
					});
				})
			},
		}
	};
</script>

<style lang="scss" scoped>
.apple-board {
	position: relative;
	box-sizing: border-box;
	height: 100vh;
	min-height: 100vh;
	padding: 20px;
	overflow: hidden;
	font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Segoe UI", sans-serif;
	color: #1d1d1f;
	--apple-ink: #1d1d1f;
	--apple-muted: #6f7b8f;
	--apple-accent: #0a84ff;
	--apple-accent-soft: rgba(10, 132, 255, 0.14);
	--panel-enter-y: 18px;
	--panel-green-bg:
		radial-gradient(circle at 18% 16%, rgba(196, 248, 219, 0.3), transparent 34%),
		radial-gradient(circle at 82% 22%, rgba(126, 228, 182, 0.26), transparent 42%),
		linear-gradient(135deg, #0f7f5b 0%, #1e9c70 52%, #2db783 100%);
	--panel-green-border: rgba(94, 188, 141, 0.54);
	--panel-green-text: #effff5;
	--panel-green-subtext: rgba(228, 255, 241, 0.78);
	--panel-green-chip: rgba(6, 57, 38, 0.3);
	--panel-green-btn: rgba(236, 255, 246, 0.22);
	background:
		radial-gradient(1200px 500px at 100% -20%, rgba(84, 132, 255, 0.24), transparent 62%),
		radial-gradient(900px 480px at -10% 100%, rgba(100, 212, 255, 0.22), transparent 58%),
		linear-gradient(160deg, #f5f7fb 0%, #edf2f8 55%, #e8eef6 100%);
}

.ambient-layer {
	position: absolute;
	inset: -120px;
	background:
		radial-gradient(circle at 25% 30%, rgba(255, 255, 255, 0.66), transparent 42%),
		radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.52), transparent 36%);
	filter: blur(18px);
	pointer-events: none;
}

.board-header,
.board-body {
	position: relative;
	z-index: 1;
}

.board-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	gap: 16px;
	margin-bottom: 10px;
	animation: rise-in 0.52s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.header-left .product-title {
	font-size: clamp(24px, 2vw, 34px);
	font-weight: 700;
	letter-spacing: -0.02em;
	color: #0f1729;
}

.header-left .product-sub {
	margin-top: 4px;
	font-size: 13px;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: #6a7487;
}

.header-right {
	display: flex;
	gap: 10px;
	align-items: center;
	flex-wrap: wrap;
	justify-content: flex-end;
}

.status-chip,
.date-chip {
	display: inline-flex;
	align-items: center;
	gap: 7px;
	padding: 8px 12px;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.7);
	backdrop-filter: blur(8px);
	border: 1px solid rgba(146, 163, 189, 0.35);
	font-size: 12px;
	font-weight: 600;
	color: #364153;
}

.live-dot {
	display: inline-block;
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: #30d158;
	box-shadow: 0 0 0 6px rgba(48, 209, 88, 0.18);
}

.back-btn {
	border: 0;
	outline: none;
	cursor: pointer;
	padding: 9px 14px;
	border-radius: 999px;
	font-size: 12px;
	font-weight: 600;
	color: #ffffff;
	background: linear-gradient(135deg, #0a84ff 0%, #3478f6 100%);
	box-shadow: 0 8px 22px rgba(10, 132, 255, 0.28);
	transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.back-btn:hover {
	transform: translateY(-1px);
	box-shadow: 0 12px 28px rgba(10, 132, 255, 0.34);
}

.board-body {
	display: grid;
	grid-template-columns: minmax(0, 0.98fr) minmax(0, 1.22fr);
	gap: 10px;
	height: calc(100vh - 108px);
}

.left-column {
	display: grid;
	grid-template-rows: minmax(0, 248px) 82px minmax(0, 1fr);
	gap: 10px;
	min-width: 0;
	min-height: 0;
}

.right-column {
	display: grid;
	grid-template-rows: minmax(0, 340px) minmax(0, 1fr);
	gap: 10px;
	min-width: 0;
	min-height: 0;
}

.right-column > .glass {
	min-height: 0;
}

.glass {
	background: var(--panel-green-bg);
	backdrop-filter: blur(18px);
	border: 1px solid var(--panel-green-border);
	border-radius: 24px;
	box-shadow:
		inset 0 1px 0 rgba(233, 255, 244, 0.34),
		0 16px 28px rgba(8, 62, 43, 0.26);
	transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
	overflow: hidden;
	color: var(--panel-green-text);
}

.left-column > .glass,
.right-column > .glass {
	opacity: 0;
	animation: rise-in 0.56s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.left-column > .glass:nth-child(1) { animation-delay: 0.06s; }
.left-column > .glass:nth-child(2) { animation-delay: 0.12s; }
.left-column > .glass:nth-child(3) { animation-delay: 0.18s; }
.right-column > .glass:nth-child(1) { animation-delay: 0.1s; }
.right-column > .glass:nth-child(2) { animation-delay: 0.16s; }

.glass:hover {
	transform: translateY(-2px);
	border-color: rgba(137, 221, 180, 0.66);
	box-shadow:
		inset 0 1px 0 rgba(233, 255, 244, 0.38),
		0 20px 34px rgba(9, 71, 49, 0.34);
}

.panel-head {
	display: flex;
	align-items: center;
	gap: 10px;
	padding: 12px 14px 6px;
}

.panel-head.compact {
	padding-bottom: 8px;
}

.panel-index {
	width: 26px;
	height: 26px;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 10px;
	font-size: 12px;
	font-weight: 700;
	color: #0f7f5b;
	background: rgba(235, 255, 245, 0.88);
}

.panel-head h2 {
	margin: 0;
	font-size: 15px;
	font-weight: 640;
	color: var(--panel-green-text);
}

.panel-head p {
	margin: 2px 0 0;
	font-size: 11px;
	letter-spacing: 0.08em;
	text-transform: uppercase;
	color: var(--panel-green-subtext);
}

.counter {
	margin-left: auto;
	padding: 4px 9px;
	border-radius: 999px;
	font-size: 11px;
	font-weight: 600;
	color: rgba(233, 255, 244, 0.92);
	background: var(--panel-green-chip);
}

.hero-panel {
	padding-bottom: 8px;
	display: flex;
	flex-direction: column;
	min-height: 0;
	background: var(--panel-green-bg);
	border-color: var(--panel-green-border);
	box-shadow:
		inset 0 1px 0 rgba(233, 255, 244, 0.34),
		0 16px 28px rgba(8, 62, 43, 0.26);
}

.hero-panel .panel-head {
	margin-bottom: 6px;
	background: transparent;
	border-bottom: 0;
	padding: 12px 14px 8px;
}

.hero-panel .panel-head h2 {
	color: #effff5;
}

.hero-panel .panel-head p {
	color: rgba(228, 255, 241, 0.78);
}

.hero-panel .panel-index {
	color: #0f7f5b;
	background: rgba(235, 255, 245, 0.88);
}

.hero-panel .counter {
	margin-left: auto;
	color: rgba(233, 255, 244, 0.92);
	background: rgba(6, 57, 38, 0.3);
}

.hero-panel:hover {
	border-color: rgba(130, 187, 161, 0.66);
	box-shadow:
		inset 0 1px 0 rgba(233, 255, 244, 0.38),
		0 20px 34px rgba(9, 71, 49, 0.34);
}

.hero-main {
	position: relative;
	padding: 0 12px;
	flex: 1;
	min-height: 0;
	display: flex;
	align-items: stretch;
	justify-content: center;
}

.hero-main,
.hero-main > .hmi-stage {
	min-width: 0;
}

.hmi-stage {
	position: relative;
	width: 100%;
	height: 100%;
	min-height: 156px;
	border-radius: 0;
	overflow: hidden;
	background: transparent;
	border: 0;
	box-shadow: none;
}

.hmi-stage::before {
	display: none;
}

.hmi-stage::after {
	content: "";
	position: absolute;
	left: 50%;
	top: 50%;
	width: 76%;
	height: 1px;
	background: linear-gradient(to right, transparent, rgba(223, 255, 239, 0.56), transparent);
	transform: translate(-50%, -50%);
	pointer-events: none;
}

.hmi-center {
	position: absolute;
	left: 50%;
	top: 51%;
	width: 56%;
	max-width: 460px;
	transform: translate(-50%, -50%);
	display: flex;
	align-items: center;
	justify-content: center;
	filter: drop-shadow(0 18px 24px rgba(3, 12, 30, 0.74));
}

.hero-image {
	width: 100%;
	height: 100%;
	max-height: 184px;
	object-fit: contain;
}

.hmi-image {
	filter: brightness(1.05) saturate(1.1) contrast(1.03);
}

.hero-brand {
	position: absolute;
	left: 50%;
	bottom: 10px;
	padding: 4px 14px;
	transform: translateX(-50%);
	border-radius: 999px;
	font-size: 10px;
	font-weight: 600;
	letter-spacing: 0.09em;
	text-transform: uppercase;
	color: #edfff4;
	background: rgba(7, 52, 35, 0.42);
	border: 1px solid rgba(193, 255, 224, 0.36);
	backdrop-filter: blur(6px);
}

.hmi-meta {
	position: absolute;
	display: flex;
	flex-direction: column;
	gap: 2px;
	max-width: 34%;
	color: #f0fff7;
	z-index: 2;
	font-variant-numeric: tabular-nums;
	text-shadow: 0 2px 12px rgba(4, 34, 21, 0.5);
}

.hmi-meta::after {
	content: "";
	position: absolute;
	top: 50%;
	width: 34px;
	border-top: 1px solid rgba(212, 255, 231, 0.5);
	opacity: 0.74;
	transform: translateY(-50%);
}

.hmi-meta span {
	font-size: 10px;
	letter-spacing: 0.1em;
	color: rgba(219, 255, 235, 0.78);
	text-transform: uppercase;
}

.hmi-meta strong {
	font-size: 24px;
	line-height: 1.05;
	font-weight: 600;
	color: #ffffff;
}

.hmi-meta-price {
	left: 22px;
	top: 20px;
}

.hmi-meta-price::after {
	left: calc(100% + 8px);
}

.hmi-meta-year {
	right: 24px;
	top: 20px;
	text-align: right;
}

.hmi-meta-year strong {
	font-size: 20px;
}

.hmi-meta-year::after {
	right: calc(100% + 8px);
}

.hmi-meta-km {
	left: 22px;
	bottom: 40px;
}

.hmi-meta-km strong {
	font-size: 18px;
}

.hmi-meta-km::after {
	left: calc(100% + 8px);
}

.hmi-meta-city {
	right: 24px;
	bottom: 40px;
	text-align: right;
}

.hmi-meta-city strong {
	font-size: 18px;
}

.hmi-meta-city::after {
	right: calc(100% + 8px);
}

.hero-empty {
	padding: 16px 12px;
	text-align: center;
	font-size: 12px;
	color: rgba(233, 255, 244, 0.9);
}

.hero-controls {
	display: grid;
	width: 100%;
	grid-template-columns: 30px minmax(0, 1fr) 30px;
	align-items: center;
	gap: 10px;
	padding: 6px 12px 0;
	margin: 0;
}

.hero-panel .nav-btn {
	background: rgba(236, 255, 246, 0.22);
	color: rgba(239, 255, 247, 0.96);
}

.hero-panel .nav-btn:hover {
	background: rgba(236, 255, 246, 0.42);
	color: #0b5f42;
}

.hero-panel .dot {
	background: rgba(234, 255, 244, 0.36);
}

.hero-panel .dot.active {
	background: #effff5;
}

.nav-btn {
	border: 0;
	outline: none;
	width: 30px;
	height: 30px;
	border-radius: 50%;
	cursor: pointer;
	background: var(--panel-green-btn);
	color: rgba(239, 255, 247, 0.96);
	font-size: 17px;
	line-height: 1;
	transition: all 0.2s ease;
}

.nav-btn:hover {
	background: rgba(236, 255, 246, 0.42);
	color: #0b5f42;
}

.dot-wrap {
	display: flex;
	justify-content: center;
	gap: 8px;
	flex-wrap: wrap;
}

.dot {
	border: 0;
	outline: none;
	width: 6px;
	height: 6px;
	border-radius: 50%;
	cursor: pointer;
	background: rgba(234, 255, 244, 0.36);
	transition: all 0.2s ease;
}

.dot.active {
	width: 16px;
	border-radius: 999px;
	background: #effff5;
}

.kpi-panel {
	padding: 0;
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 8px;
	background: transparent;
	border-color: transparent;
	box-shadow: none;
	backdrop-filter: none;
	overflow: visible;
}

.kpi-panel:hover {
	border-color: transparent;
	box-shadow: none;
	transform: none;
}

.kpi-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 8px;
	padding: 9px 12px;
	min-height: 64px;
	border-radius: 14px;
	background: linear-gradient(165deg, #f7f9fa 0%, #edf1f2 58%, #e8eeef 100%);
	border: 1px solid rgba(188, 202, 197, 0.85);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.96),
		0 8px 16px rgba(120, 141, 132, 0.16);
}

.kpi-left {
	display: flex;
	align-items: center;
	gap: 8px;
	min-width: 0;
}

.kpi-icon {
	width: 20px;
	height: 20px;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	background: linear-gradient(135deg, #8bd1ad 0%, #5baa84 100%);
	color: #ffffff;
	font-size: 12px;
	flex-shrink: 0;
	box-shadow: 0 4px 10px rgba(86, 152, 121, 0.28);
}

.kpi-copy {
	display: flex;
	align-items: baseline;
	gap: 8px;
	min-width: 0;
}

.kpi-copy span {
	font-size: 10px;
	font-weight: 600;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: #a0ada8;
	white-space: nowrap;
}

.kpi-item strong {
	font-size: 36px;
	line-height: 1;
	font-weight: 700;
	color: #243d39;
	letter-spacing: -0.02em;
	font-variant-numeric: tabular-nums;
}

.kpi-copy em {
	font-style: normal;
	font-size: 18px;
	font-weight: 600;
	color: #384a45;
	white-space: nowrap;
}

.forecast-panel {
	padding-bottom: 10px;
	display: flex;
	flex-direction: column;
	min-height: 0;
	background: linear-gradient(165deg, #f6f8f9 0%, #edf1f2 58%, #e9eeef 100%);
	border-color: rgba(179, 199, 193, 0.54);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.92),
		0 12px 30px rgba(108, 130, 122, 0.2);
	color: #32423d;
}

.forecast-panel:hover {
	border-color: rgba(130, 187, 161, 0.66);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.98),
		0 16px 34px rgba(90, 116, 106, 0.24);
}

.forecast-panel .panel-head {
	margin-bottom: 6px;
	background: transparent;
	border-bottom: 0;
	padding: 12px 14px 8px;
}

.forecast-panel .panel-head.compact {
	padding-bottom: 8px;
}

.forecast-panel .panel-head h2 {
	color: #2f4e43;
}

.forecast-panel .panel-head p {
	color: #7f928b;
}

.forecast-panel .panel-index {
	width: 30px;
	height: 30px;
	color: #ffffff;
	border-radius: 999px;
	background: linear-gradient(135deg, #66c496 0%, #409f78 100%);
	box-shadow: 0 6px 14px rgba(63, 150, 113, 0.34);
}

.forecast-panel .forecast-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 8px;
	padding: 0 14px;
	flex: 1;
	align-content: start;
}

.forecast-panel .input-wrap {
	display: flex;
	flex-direction: column;
	gap: 3px;
}

.forecast-panel .input-wrap.full {
	grid-column: auto;
}

.forecast-panel .input-wrap span {
	font-size: 11px;
	color: #6f827b;
}

.forecast-panel .input-wrap input {
	height: 34px;
	border: 1px solid rgba(195, 207, 204, 0.9);
	border-radius: 10px;
	padding: 0 12px;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(246, 250, 249, 0.98) 100%);
	font-size: 13px;
	color: #31433e;
	outline: none;
	box-shadow: inset 0 1px 2px rgba(86, 110, 101, 0.08);
	transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.forecast-panel .input-wrap input::placeholder {
	color: #94a49d;
}

.forecast-panel .input-wrap input:focus {
	border-color: rgba(107, 180, 145, 0.9);
	box-shadow: 0 0 0 3px rgba(86, 171, 133, 0.22);
	background: #ffffff;
}

.forecast-panel .result-card {
	grid-column: auto;
	border-radius: 12px;
	padding: 6px 10px;
	background: linear-gradient(165deg, rgba(241, 246, 244, 0.96) 0%, rgba(233, 240, 237, 0.96) 100%);
	border: 1px solid rgba(187, 203, 198, 0.9);
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.forecast-panel .result-card span {
	font-size: 12px;
	color: #758781;
}

.forecast-panel .result-card strong {
	font-size: 16px;
	line-height: 1;
	color: #2f7c5b;
}

.forecast-panel .predict-btn {
	border: 0;
	outline: none;
	cursor: pointer;
	border-radius: 10px;
	font-size: 15px;
	font-weight: 600;
	color: #fff;
	background: linear-gradient(135deg, #62c99b 0%, #3da676 100%);
	box-shadow: 0 10px 22px rgba(66, 142, 108, 0.36);
	height: 36px;
	grid-column: 1 / -1;
	letter-spacing: 0.03em;
}

.table-panel {
	padding-bottom: 10px;
	min-height: 0;
	display: flex;
	flex-direction: column;
	background: linear-gradient(165deg, #f6f8f9 0%, #edf1f2 58%, #e9eeef 100%);
	border-color: rgba(179, 199, 193, 0.54);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.92),
		0 12px 30px rgba(108, 130, 122, 0.2);
}

.table-panel-side .panel-head {
	padding-top: 12px;
	padding-bottom: 8px;
	margin-bottom: 6px;
	background: transparent;
	border-bottom: 0;
}

.table-panel .panel-head h2 {
	color: #2f4e43;
}

.table-panel .panel-head p {
	color: #7f928b;
}

.table-panel .panel-index {
	width: 30px;
	height: 30px;
	color: #ffffff;
	border-radius: 999px;
	background: linear-gradient(135deg, #66c496 0%, #409f78 100%);
	box-shadow: 0 6px 14px rgba(63, 150, 113, 0.34);
}

.table-wrap {
	flex: 1;
	min-height: 0;
	overflow: auto;
	padding: 0 12px 8px;
}

.table-wrap::-webkit-scrollbar {
	width: 6px;
}

.table-wrap::-webkit-scrollbar-thumb {
	border-radius: 10px;
	background: rgba(120, 161, 145, 0.46);
}

.table-panel ::v-deep .forecast-table {
	background: transparent;
	border-radius: 12px;
	overflow: hidden;
	border: 1px solid rgba(187, 202, 197, 0.72);
}

.table-panel ::v-deep .el-table,
.table-panel ::v-deep .el-table__expanded-cell {
	background-color: transparent;
	color: #3a4a45;
}

.table-panel ::v-deep .el-table th,
.table-panel ::v-deep .el-table tr {
	background-color: transparent;
	color: #445650;
}

.table-panel ::v-deep .el-table td,
.table-panel ::v-deep .el-table th.is-leaf {
	border-bottom: 1px solid rgba(204, 215, 211, 0.8);
	padding: 6px 0;
	border-right: 1px solid rgba(214, 224, 220, 0.76);
}

.table-panel ::v-deep .el-table td .cell,
.table-panel ::v-deep .el-table th .cell {
	color: #3f514b;
	font-size: 13px;
}

.table-panel ::v-deep .el-table--enable-row-hover .el-table__body tr:hover > td {
	background-color: rgba(208, 224, 217, 0.66);
}

.table-panel ::v-deep .el-table th {
	padding: 8px 0;
	background-color: rgba(226, 233, 232, 0.95);
}

.table-panel ::v-deep .el-table th .cell {
	font-weight: 600;
	color: #576963;
}

.table-panel ::v-deep .el-table__body tr:nth-child(odd) > td {
	background-color: rgba(252, 253, 253, 0.72);
}

.table-panel ::v-deep .el-table__body tr:nth-child(even) > td {
	background-color: rgba(239, 244, 243, 0.8);
}

.table-panel ::v-deep .el-table--border::after {
	display: none;
}

.table-panel ::v-deep .el-table::before {
	height: 0;
}

.chart-carousel {
	height: 100%;
	min-height: 0;
	padding-bottom: 10px;
	position: relative;
	overflow: hidden;
	display: flex;
	flex-direction: column;
	background: linear-gradient(165deg, #f6f8f9 0%, #edf1f2 58%, #e9eeef 100%);
	border-color: rgba(179, 199, 193, 0.54);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.92),
		0 12px 30px rgba(108, 130, 122, 0.2);
	color: #32423d;
	isolation: isolate;
}

.chart-carousel::before {
	content: "";
	position: absolute;
	inset: 12px;
	border-radius: 16px;
	border: 1px solid rgba(193, 208, 203, 0.72);
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
	pointer-events: none;
	z-index: 0;
}

.chart-carousel:hover {
	border-color: rgba(130, 187, 161, 0.66);
	box-shadow:
		inset 0 1px 0 rgba(255, 255, 255, 0.98),
		0 16px 34px rgba(90, 116, 106, 0.24);
}

.chart-carousel .panel-head {
	margin-bottom: 6px;
	background: transparent;
	border-bottom: 0;
	padding: 12px 14px 8px;
	position: relative;
	z-index: 1;
}

.chart-carousel .panel-head.compact {
	padding-bottom: 8px;
}

.chart-carousel .panel-head h2 {
	color: #2f4e43;
}

.chart-carousel .panel-head p {
	color: #7f928b;
}

.chart-carousel .panel-index {
	width: 30px;
	height: 30px;
	color: #ffffff;
	border-radius: 999px;
	background: linear-gradient(135deg, #66c496 0%, #409f78 100%);
	box-shadow: 0 6px 14px rgba(63, 150, 113, 0.34);
}

.chart-carousel .counter {
	color: #50635d;
	background: rgba(230, 236, 234, 0.9);
	border: 1px solid rgba(186, 203, 197, 0.78);
}

.chart-carousel .nav-btn {
	background: linear-gradient(165deg, #f4f7f7 0%, #e8eeec 100%);
	color: #537169;
	border: 1px solid rgba(184, 201, 196, 0.86);
	box-shadow: 0 6px 12px rgba(127, 151, 141, 0.18);
}

.chart-carousel .nav-btn:hover {
	background: linear-gradient(165deg, #6dc89b 0%, #49aa7f 100%);
	color: #ffffff;
	border-color: rgba(91, 160, 129, 0.9);
}

.chart-carousel .dot {
	background: rgba(167, 187, 179, 0.7);
}

.chart-carousel .dot.active {
	background: #5aa87f;
	box-shadow: 0 4px 10px rgba(92, 161, 129, 0.3);
}

.chart-carousel::after {
	content: "";
	position: absolute;
	top: -40%;
	right: -55%;
	width: 220px;
	height: 220px;
	background: radial-gradient(circle, rgba(163, 216, 191, 0.38) 0%, rgba(163, 216, 191, 0) 68%);
	opacity: 0;
	transition: opacity 0.28s ease;
	pointer-events: none;
}

.chart-carousel:hover::after {
	opacity: 1;
}

.chart-stage-wrap {
	position: relative;
	flex: 1;
	min-height: 0;
	margin: 0 14px;
	z-index: 1;
	border-radius: 14px;
	background:
		repeating-linear-gradient(
			to right,
			rgba(183, 201, 195, 0.22) 0,
			rgba(183, 201, 195, 0.22) 1px,
			transparent 1px,
			transparent 44px
		),
		repeating-linear-gradient(
			to bottom,
			rgba(183, 201, 195, 0.2) 0,
			rgba(183, 201, 195, 0.2) 1px,
			transparent 1px,
			transparent 34px
		);
	box-shadow:
		inset 0 0 0 1px rgba(186, 202, 197, 0.86),
		inset 0 1px 0 rgba(255, 255, 255, 0.78);
}

.chart-stage {
	position: absolute;
	inset: 0;
	opacity: 0;
	transform: translateX(20px) scale(0.99);
	transition: opacity 0.32s ease, transform 0.32s ease;
	pointer-events: none;
}

.chart-stage.active {
	opacity: 1;
	transform: translateX(0) scale(1);
	pointer-events: auto;
}

.chart-controls {
	display: grid;
	grid-template-columns: 30px minmax(0, 1fr) 30px;
	align-items: center;
	gap: 10px;
	padding: 8px 14px 0;
}

.chart-canvas {
	height: 100%;
	width: 100%;
}

.car-fade-enter-active,
.car-fade-leave-active {
	transition: opacity 0.35s ease, transform 0.35s ease;
}

.car-fade-enter,
.car-fade-leave-to {
	opacity: 0;
	transform: scale(0.98);
}

@keyframes rise-in {
	from {
		opacity: 0;
		transform: translateY(var(--panel-enter-y));
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

@media (prefers-reduced-motion: reduce) {
	.board-header,
	.left-column > .glass,
	.right-column > .glass {
		animation: none;
		opacity: 1;
	}

	.glass,
	.chart-carousel::after,
	.chart-stage,
	.nav-btn,
	.dot,
	.back-btn {
		transition: none;
	}
}

@media (max-width: 1500px) {
	.apple-board {
		padding: 16px;
	}

	.board-body {
		height: calc(100vh - 106px);
		gap: 10px;
	}

	.left-column {
		gap: 10px;
	}

	.right-column {
		grid-template-rows: minmax(0, 340px) minmax(0, 1fr);
	}

	.hero-main {
		padding: 0 10px;
	}

	.hmi-stage {
		min-height: 146px;
	}

	.hmi-meta strong {
		font-size: 22px;
	}

	.hmi-meta::after {
		width: 28px;
	}

	.hmi-meta-year strong {
		font-size: 18px;
	}

	.hmi-meta-km strong,
	.hmi-meta-city strong {
		font-size: 16px;
	}

	.chart-stage-wrap {
		margin: 0 12px;
	}
}

@media (max-width: 1180px) {
	.apple-board {
		height: auto;
		min-height: 100vh;
	}

	.board-body {
		grid-template-columns: minmax(0, 1fr);
		height: auto;
	}

	.left-column {
		grid-template-rows: auto auto auto;
	}

	.right-column {
		min-height: 0;
		grid-template-rows: minmax(0, 360px) minmax(0, 240px);
	}

	.hmi-stage {
		width: 100%;
		min-height: 182px;
	}

	.hero-controls {
		width: 100%;
	}

	.hmi-center {
		width: 62%;
		max-width: 420px;
	}

	.hmi-meta {
		max-width: 32%;
	}

	.hmi-meta strong {
		font-size: 20px;
	}

	.hmi-meta-year strong {
		font-size: 17px;
	}

	.hmi-meta-km strong,
	.hmi-meta-city strong {
		font-size: 15px;
	}
}

@media (max-width: 768px) {
	.apple-board {
		padding: 14px;
		height: auto;
	}

	.board-header {
		flex-direction: column;
		align-items: flex-start;
	}

	.header-right {
		justify-content: flex-start;
	}

	.forecast-grid {
		grid-template-columns: 1fr;
	}

	.input-wrap.full,
	.result-card {
		grid-column: auto;
	}

	.kpi-panel {
		grid-template-columns: 1fr;
		gap: 10px;
	}

	.kpi-item strong {
		font-size: 32px;
	}

	.right-column,
	.chart-carousel,
	.table-panel {
		min-height: 0;
	}

	.right-column {
		grid-template-rows: minmax(0, 320px) minmax(0, 220px);
	}

	.hmi-stage {
		width: 100%;
		min-height: 170px;
	}

	.hero-controls {
		width: 100%;
	}

	.hmi-center {
		width: 68%;
	}

	.hmi-meta {
		max-width: 38%;
	}

	.hmi-meta-price {
		top: 14px;
		left: 22px;
	}

	.hmi-meta-km {
		bottom: 36px;
		left: 22px;
	}

	.hmi-meta-year {
		top: 14px;
		right: 24px;
	}

	.hmi-meta-city {
		right: 24px;
		bottom: 36px;
	}

	.hmi-meta strong {
		font-size: 18px;
	}

	.hmi-meta::after {
		display: none;
	}

	.hmi-meta-year strong,
	.hmi-meta-km strong,
	.hmi-meta-city strong {
		font-size: 14px;
	}

	.hero-brand {
		padding: 8px 14px;
		font-size: 12px;
	}

	.chart-canvas {
		height: 100%;
	}
}
</style>


