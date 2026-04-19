<template>
	<div class="front-detail">
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">返回列表</el-button>
		</div>

		<section class="front-detail-hero">
			<div class="front-detail-hero__gallery">
				<div class="front-detail-hero__lead">
					<img :src="swiperBigUrl || require('@/assets/chapter.jpg')" alt="used car">
				</div>
				<div class="front-detail-hero__thumbs" v-if="detailBanner.length">
					<div
						v-for="(item, index) in detailBanner"
						:key="index"
						:class="['front-detail-hero__thumb', { 'is-active': thumbUrl(item) === swiperBigUrl }]"
						@click="swiperClick3(thumbUrl(item))"
					>
						<img :src="thumbUrl(item)" alt="thumb">
					</div>
				</div>
			</div>

			<aside class="front-detail-hero__summary">
				<span class="front-pill">Used Car Detail</span>
				<h1>{{ detail.brand }} {{ detail.model1 }}</h1>
				<p>将车辆信息从旧式字段回显重构成更利于决策阅读的详情布局，重点展示价格、年份、里程与城市。</p>
				<div class="front-detail-price">
					<strong>{{ detail.discountprice || '--' }}</strong>
					<span>现价 / 元</span>
				</div>
				<div class="front-detail-facts">
					<div class="front-detail-fact"><small>年份</small><strong>{{ detail.vehicleage || '--' }}</strong></div>
					<div class="front-detail-fact"><small>里程</small><strong>{{ detail.kilometer || '--' }}</strong></div>
					<div class="front-detail-fact"><small>城市</small><strong>{{ detail.city || '--' }}</strong></div>
					<div class="front-detail-fact"><small>已减</small><strong>{{ detail.originalprice || '--' }}</strong></div>
					<div class="front-detail-fact"><small>浏览量</small><strong>{{ detail.clicknum || 0 }}</strong></div>
					<div class="front-detail-fact"><small>链接</small><strong class="front-clickable" @click="linkOthers(detail.xqurl)">{{ detail.xqurl || '--' }}</strong></div>
				</div>
				<div class="front-detail-actions">
					<el-button v-show="!isStoreup" type="primary" @click="storeup(1)">收藏 {{ detail.storeupnum || 0 }}</el-button>
					<el-button v-show="isStoreup" @click="storeup(-1)">已收藏 {{ detail.storeupnum || 0 }}</el-button>
					<el-button v-if="!isThumbsupnum && !isCrazilynum" @click="thumbsupOrCrazily(21)">赞一下 {{ detail.thumbsupnum || 0 }}</el-button>
					<el-button v-if="!isThumbsupnum && !isCrazilynum" @click="thumbsupOrCrazily(22)">踩一下 {{ detail.crazilynum || 0 }}</el-button>
					<el-button v-if="isThumbsupnum" @click="cancelThumbsupOrCrazily(21)">取消点赞</el-button>
					<el-button v-if="isCrazilynum" @click="cancelThumbsupOrCrazily(22)">取消点踩</el-button>
				</div>
				<div class="front-detail-actions">
					<el-button v-if="btnAuth('usedcar','修改')" @click="editClick">修改</el-button>
					<el-button v-if="btnAuth('usedcar','删除')" type="danger" @click="delClick">删除</el-button>
					<el-button v-if="btnAuth('usedcar','章节管理')" @click="allchapterClick()">章节管理</el-button>
					<el-button v-if="btnAuth('usedcar','查看评论')" @click="discussClick()">查看评论</el-button>
				</div>
			</aside>
		</section>

		<section class="front-detail-section">
			<h2>关键数据</h2>
			<div class="front-detail-section__grid">
				<div class="front-detail-section__panel"><small class="front-muted">现价</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.discountprice || '--' }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">收藏数</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.storeupnum || 0 }}</div></div>
				<div class="front-detail-section__panel"><small class="front-muted">点赞数</small><div style="margin-top: 8px; font-size: 22px; font-weight: 700;">{{ detail.thumbsupnum || 0 }}</div></div>
			</div>
		</section>

		<section class="front-detail-section" v-if="tabsNum > 0">
			<h2>评论互动</h2>
			<el-form class="commentForm" :model="form" :rules="rules" ref="form">
				<el-form-item prop="content">
					<editor myQuillEditor="content" v-model="form.content" class="editor" action="file/upload"></editor>
				</el-form-item>
				<div class="front-detail-actions">
					<el-button type="primary" @click="submitForm('form')">提交评论</el-button>
					<el-button @click="resetForm('form')">重置</el-button>
				</div>
			</el-form>

			<div v-if="infoList.length" class="front-page-grid" style="margin-top: 20px;">
				<div class="front-detail-section__panel" v-for="item in infoList" :key="item.id" @mouseenter="discussEnter(item.id)" @mouseleave="discussLeave">
					<div style="display: flex; gap: 14px; align-items: flex-start;">
						<el-image v-if="item.avatarurl" :src="baseUrl + item.avatarurl" style="width: 52px; height: 52px; border-radius: 16px; overflow: hidden;"></el-image>
						<el-image v-else :src="require('@/assets/touxiang.png')" style="width: 52px; height: 52px; border-radius: 16px; overflow: hidden;"></el-image>
						<div style="flex: 1;">
							<div style="display: flex; justify-content: space-between; gap: 16px; align-items: center;">
								<strong>{{ item.nickname }}</strong>
								<span class="front-muted">{{ item.addtime }}</span>
							</div>
							<div class="ql-snow ql-editor" v-html="item.content" style="padding: 8px 0 0;"></div>
							<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; color: #5f6f65; font-size: 12px;">
								<span class="front-clickable" v-if="!comcaiChange(item)" @click="comzanClick(item)">{{ comzanChange(item) ? '已赞' : '赞' }} ({{ item.thumbsupnum }})</span>
								<span class="front-clickable" v-if="!comzanChange(item)" @click="comcaiClick(item)">{{ comcaiChange(item) ? '已踩' : '踩' }} ({{ item.crazilynum }})</span>
								<span class="front-clickable" v-if="showIndex == item.id && userid == item.userid" @click="discussDel(item.id)">删除</span>
							</div>
							<div v-if="item.reply" style="margin-top: 12px; padding: 12px 14px; border-radius: 14px; background: rgba(47,123,87,.06);">
								<strong>回复：</strong>
								<span class="ql-snow ql-editor" v-html="item.reply"></span>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div v-else class="front-empty">暂无评论内容</div>

			<el-pagination
				background
				id="pagination"
				class="pagination"
				:page-size="pageSize"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				@current-change="curChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				@size-change="sizeChange"
			></el-pagination>
		</section>
	</div>
</template>
<script>
	import axios from 'axios'
	import Swiper from "swiper";
	export default {
		//数据集合
		data() {
			return {
				tablename: 'usedcar',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '二手车'
					}
				],
				title: '',
				detailBanner: [],
				userid: Number(localStorage.getItem('frontUserid')),
				id: 0,
				detail: {},
				tabsNum: 1,
				activeName: '1',
				form: {
					content: '',
					userid: Number(localStorage.getItem('frontUserid')),
					nickname: localStorage.getItem('username'),
					avatarurl: '',
				},
				showIndex: -1,
				infoList: [],
				rules: {
					content: [
						{ required: true, message: '请输入内容', trigger: 'blur' }
					],
				},
				total: 1,
				pageSize: 10,
				totalPage: 1,
				storeupParams: {
					name: '',
					picture: '',
					refid: 0,
					tablename: 'usedcar',
					userid: Number(localStorage.getItem('frontUserid'))
				},
				isStoreup: false,
				storeupInfo: {},
				isCrazilynum: false,
				isThumbsupnum: false,
				thumbsupOrCrazilyInfo: {},
				buynumber: 1,
				centerType: false,
				storeupType: false,
				swiperBigUrl: null,
			}
		},
		created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0) {
				this.centerType = true
			}
			if(this.$route.query.storeupType&&this.$route.query.storeupType!=0) {
				this.storeupType = true
			}
			
			this.init();
		},
		mounted() {
		},
		computed: {
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			thumbUrl(item) {
				if (!item) {
					return require('@/assets/chapter.jpg')
				}
				return item.substr(0,4)=='http' ? item : this.baseUrl + item
			},
			swiperClick3(src) {
				this.swiperBigUrl = src
			},
			init() {
				this.id = this.$route.query.id
				this.baseUrl = this.$config.baseUrl;
				this.$http.get(this.tablename + '/detail/'  + this.id, {}).then(async res => {
					if (res.data.code == 0) {
						this.detail = res.data.data;
						this.title = this.detail.brand;
						if(this.detail.imgurl) {
							this.detailBanner = this.detail.imgurl.split(",w").length>1?[this.detail.imgurl]:this.detail.imgurl.split(',');
						}
						this.$forceUpdate();
						this.getDiscussList(1);
						if(localStorage.getItem('frontToken')){
							this.getStoreupStatus();
							this.getThumbsupOrCrazilyStatus();
						}

					}
					if (this.detailBanner.length) {
						if (this.detailBanner[0].substr(0,4)=='http') {
							this.swiperBigUrl = this.detailBanner[0]
						} else {
							this.swiperBigUrl = this.baseUrl + this.detailBanner[0]
						}
					}
				});
			},
			linkOthers(url) {
				window.open(url);//打开一个新的标签页
			},
			storeup(type) {
				if (type == 1 && !this.isStoreup) {
					this.storeupParams.name = this.title;
					this.storeupParams.picture = this.detailBanner[0];
					this.storeupParams.refid = this.detail.id;
					this.storeupParams.type = String(type);
					this.$http.post('storeup/add', this.storeupParams).then(res => {
						if (res.data.code == 0) {
							this.isStoreup = true;
							this.detail.storeupnum++
							this.$http.post('usedcar/update', this.detail).then(res => {});
							this.$message({
								type: 'success',
								message: '收藏成功!',
								duration: 1500,
							});
						}
					});
				}
				if (type == -1 && this.isStoreup) {
					this.$http.get('storeup/list', {params: {page: 1, limit: 1, type: '1', refid: this.detail.id, tablename: 'usedcar', userid: Number(localStorage.getItem('frontUserid'))}}).then(res => {
						if (res.data.code == 0 && res.data.data.list.length > 0) {
							this.isStoreup = true;
							this.storeupInfo = res.data.data.list[0];
							let delIds = new Array();
							delIds.push(this.storeupInfo.id);
							this.$http.post('storeup/delete', delIds).then(res => {
								if (res.data.code == 0) {
									this.isStoreup = false;
									this.detail.storeupnum--
									this.$http.post('usedcar/update', this.detail).then(res => {});
									this.$message({
										type: 'success',
										message: '取消成功!',
										duration: 1500,
									});
								}
							});
						}
					});
				}
			},
			getStoreupStatus(){
				if(localStorage.getItem("frontToken")) {
					this.$http.get('storeup/list', {params: {page: 1, limit: 1, type: '1', refid: this.detail.id, tablename: 'usedcar', userid: Number(localStorage.getItem('frontUserid'))}}).then(res => {
						if (res.data.code == 0 && res.data.data.list.length > 0) {
							this.isStoreup = true;
							this.storeupInfo = res.data.data.list[0];
						}
					});
				}
			},
			async thumbsupOrCrazily(type) {
				this.storeupParams.name = this.title;
				this.storeupParams.picture = this.detailBanner[0];
				this.storeupParams.refid = this.detail.id;
				this.storeupParams.type = String(type);
				await this.$http.post('storeup/add', this.storeupParams).then(res => {
					if (res.data.code == 0) {
						let detail = JSON.parse(JSON.stringify(this.detail))
						if (type == 21) detail.thumbsupnum = Number(detail.thumbsupnum) + 1;
						if (type == 22) detail.crazilynum = Number(detail.crazilynum) + 1;
						this.$http.post('usedcar/update', detail).then(res => {
							this.detail = detail
						});
						this.getThumbsupOrCrazilyStatus();
						this.$message({
							type: 'success',
							message: '操作成功!',
							duration: 1500,
						});
						
					}
				});
				
			},
			async cancelThumbsupOrCrazily(type) {
				let delIds = new Array();
				delIds.push(this.thumbsupOrCrazilyInfo.id);
				await this.$http.post('storeup/delete', delIds).then(res => {
					if (res.data.code == 0) {
						let detail = JSON.parse(JSON.stringify(this.detail))
						if (type == 21) detail.thumbsupnum -= 1;
						if (type == 22) detail.crazilynum -= 1;
						this.$http.post('usedcar/update', detail).then(res => {
							this.detail = detail
						});
						this.isThumbsupnum = false;
						this.isCrazilynum = false;
						this.$message({
							type: 'success',
							message: '取消成功!',
							duration: 1500,
						});
					}
				});
				
			},
			getThumbsupOrCrazilyStatus() {
				if(localStorage.getItem("frontToken")) {
					this.$http.get('storeup/list', {params: {page: 1, limit: 1, type: '21', refid: this.detail.id, tablename: 'usedcar', userid: Number(localStorage.getItem('frontUserid'))}}).then(res => {
						if (res.data.code == 0 && res.data.data.list.length > 0) {
							this.isThumbsupnum = true;
							this.thumbsupOrCrazilyInfo = res.data.data.list[0];
						}
					});
					this.$http.get('storeup/list', {params: {page: 1, limit: 1, type: '22', refid: this.detail.id, tablename: 'usedcar', userid: Number(localStorage.getItem('frontUserid'))}}).then(res => {
						if (res.data.code == 0 && res.data.data.list.length > 0) {
							this.isCrazilynum = true;
							this.thumbsupOrCrazilyInfo = res.data.data.list[0];
						}
					});
				}
			},
			curChange(page) {
				this.getDiscussList(page);
			},
			prevClick(page) {
				this.getDiscussList(page);
			},
			nextClick(page) {
				this.getDiscussList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getDiscussList(1);
			},
			// 返回按钮
			backClick(){
				if(this.storeupType){
					history.back()
				}else{
					let params = {}
					if(this.centerType){
						params.centerType = 1
					}
					this.$router.push({path: '/index/usedcar', query: params});
				}
			},
			// 下载
			download(file ){
				if(!file) {
					this.$message({
						type: 'error',
						message: '文件不存在',
						duration: 1500,
					});
					return;
				}
				let arr = file.replace(new RegExp('upload/', "g"), "")
				axios.get(this.baseUrl + 'file/download?fileName=' + arr, {
					headers: {
						token: localStorage.getItem("frontToken")
					},
					responseType: "blob"
				}).then(({
					data
				}) => {
					const binaryData = [];
					binaryData.push(data);
					const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
						type: 'application/pdf;chartset=UTF-8'
					}))
					const a = document.createElement('a')
					a.href = objectUrl
					a.download = arr
					// a.click()
					// 下面这个写法兼容火狐
					a.dispatchEvent(new MouseEvent('click', {
						bubbles: true,
						cancelable: true,
						view: window
					}))
					window.URL.revokeObjectURL(data)
				},err=>{
					axios.get((location.href.split(this.$config.name).length>1 ? location.href.split(this.$config.name)[0] :'') + this.$config.name + 'file/download?fileName=' + arr, {
						headers: {
							token: localStorage.getItem("frontToken")
						},
						responseType: "blob"
					}).then(({
						data
					}) => {
						const binaryData = [];
						binaryData.push(data);
						const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
							type: 'application/pdf;chartset=UTF-8'
						}))
						const a = document.createElement('a')
						a.href = objectUrl
						a.download = arr
						// a.click()
						// 下面这个写法兼容火狐
						a.dispatchEvent(new MouseEvent('click', {
							bubbles: true,
							cancelable: true,
							view: window
						}))
						window.URL.revokeObjectURL(data)
					})
				})
			},
			getDiscussList(page,type=1) {
				this.$http.get('discussusedcar/list', {
					params: {
						page, 
						limit: this.pageSize, 
						refid: this.detail.id,
						sort: 'istop',
						order: 'desc',
					}
				}).then(res => {
					if (res.data.code == 0) {
						for(let x in res.data.data.list) {
							res.data.data.list[x].content = res.data.data.list[x].content.replace(/img src/gi,"img style=\"width:30%;\" src");
						}
						this.infoList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(type==1) {
							if(this.$route.query.discussId&&this.$route.query.discussId!=0) {
								this.$nextTick(()=>{
									document.getElementById('discuss' + this.$route.query.discussId).scrollIntoView({
										behavior: 'smooth'
									});
								})
							}
						}
					}
				});
			},
			comzanChange(row){
				if(row.tuserids){
					let arr = row.tuserids.split(',')
					for(let x in arr){
						if(arr[x] == this.userid){
							return true
						}
					}
				}
				return false
			},
			comzanClick(row){
				if(!this.userid){
					return false
				}
				if(!this.comzanChange(row)){
					row.thumbsupnum++
					if(row.tuserids){
						row.tuserids = row.tuserids + ',' + this.userid
					}else {
						row.tuserids = String(this.userid)
					}
					this.$http.post('discussusedcar/update',row).then(rs=>{
						this.$message.success('点赞成功')
					})
				}else {
					row.thumbsupnum--
					let arr = row.tuserids.split(',')
					for(let x in arr){
						if(arr[x] == this.userid){
							arr.splice(x,1)
						}
					}
					row.tuserids = arr.join(',')
					this.$http.post('discussusedcar/update',row).then(rs=>{
						this.$message.success('取消成功')
					})
				}
			},
			comcaiChange(row){
				if(row.cuserids){
					let arr = row.cuserids.split(',')
					for(let x in arr){
						if(arr[x] == this.userid){
							return true
						}
					}
				}
				return false
			},
			comcaiClick(row){
				if(!this.userid){
					return false
				}
				if(!this.comcaiChange(row)){
					row.crazilynum++
					if(row.cuserids){
						row.cuserids = row.cuserids + ',' + this.userid
					}else {
						row.cuserids = String(this.userid)
					}
					this.$http.post('discussusedcar/update',row).then(rs=>{
						this.$message.success('点踩成功')
					})
				}else {
					row.crazilynum--
					let arr = row.cuserids.split(',')
					for(let x in arr){
						if(arr[x] == this.userid){
							arr.splice(x,1)
						}
					}
					row.cuserids = arr.join(',')
					this.$http.post('discussusedcar/update',row).then(rs=>{
						this.$message.success('取消成功')
					})
				}
			},
			discussEnter(index){
				this.showIndex = index
			},
			discussLeave(){
				this.showIndex = -1
			},
			discussDel(id){
				this.$confirm('是否删除此评论？').then(_ => {
					this.$http.post('discussusedcar/delete',[id]).then(res=>{
						if(res.data&&res.data.code==0){
							this.addDiscussNum(1)
							this.$message({
								type: 'success',
								message: '删除成功!',
								duration: 1500,
								onClose: () => {
									this.getDiscussList(1);
								}
							});
						}
					})
				}).catch(_ => {});
			},
			submitForm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.addComments()
					} else {
						return false;
					}
				});
			},
			addComments(content=null,type=1) {
				let data = JSON.parse(JSON.stringify(this.form))
				data.refid = this.detail.id;
				data.avatarurl = localStorage.getItem('frontHeadportrait')?localStorage.getItem('frontHeadportrait'):'';
				if(type==2) {
					data.content = content
				}
				this.$http.post('discussusedcar/add', data).then(rs2 => {
					if (rs2.data.code == 0) {
						if(type==1) {
							this.form.content = '';
						}
						this.addDiscussNum(2)
						this.getDiscussList(1,type);
						this.$message({
							type: 'success',
							message: '评论成功!',
							duration: 1500,
						});
					}
				});
			},
			resetForm(formName) {
				this.$refs[formName].resetFields();
			},
			addDiscussNum(type){
				if(type==2){
					this.detail.discussnum++
				}else if(type==1){
					if(this.detail.discussnum!=0){
						this.detail.discussnum--
					}else{
						this.detail.discussnum = 0
					}
				}
				this.$http.post('usedcar/update',this.detail).then(res=>{})
			},


			// 权限判断
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			// 修改
			editClick(){
				this.$router.push(`/index/usedcarAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此二手车？') .then(_ => {
					this.$http.post('usedcar/delete', [this.detail.id]).then(async res => {
						if (res.data.code == 0) {
							this.$http.get('storeup/list',{params:{
								page: 1,
								limit: 100,
								refid: this.detail.id,
								tablename: 'usedcar',
							}}).then(async obj=>{
								if(obj.data&&obj.data.code==0){
									let arr = []
									for(let x in obj.data.data.list){
										arr.push(obj.data.data.list[x].id)
									}
									if(arr.length){
										await this.$http.post('storeup/delete',arr).then(()=>{})
									}
									this.$message({
										type: 'success',
										message: '删除成功!',
										duration: 1500,
										onClose: () => {
											history.back()
										}
									});
								}
							})
						}
					});
				}).catch(_ => {});
			},
			allchapterClick (){
				let params = {
					refid: this.detail.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chapterusedcar', query: params});
			},
			discussClick (){
				let params = {
					refid: this.detail.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/discussusedcar', query: params});
			},
			// 获取uuid
			getUUID() {
				return new Date().getTime();
			},
		},
		components: {
		}
	}
</script>

