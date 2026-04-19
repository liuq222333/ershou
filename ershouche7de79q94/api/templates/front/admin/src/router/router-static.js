	import Vue from 'vue';
//配置路由
	import VueRouter from 'vue-router'
	Vue.use(VueRouter);
//1.创建组件
	import Index from '@/views/index'
	import Home from '@/views/home'
	import Board from '@/views/board'
	import Login from '@/views/login'
	import NotFound from '@/views/404'
	import pay from '@/views/pay'
	import register from '@/views/register'
	import center from '@/views/center'
	import yonghu from '@/views/modules/yonghu/list'
	import usedcar from '@/views/modules/usedcar/list'
	import usedcarforecast from '@/views/modules/usedcarforecast/list'
	import news from '@/views/modules/news/list'
	import systemintro from '@/views/modules/systemintro/list'
	import smsregistercode from '@/views/modules/smsregistercode/list'
	import users from '@/views/modules/users/list'
	import discussusedcar from '@/views/modules/discussusedcar/list'
import config from '@/views/modules/config/list'

//2.配置路由   注意：名字
export const routes = [{
	path: '/',
	name: '系统首页',
	component: Index,
	children: [{
		// 这里不设置值，是把main作为默认页面
		path: '/',
		name: '系统首页',
		component: Home,
		meta: {icon:'', title:'center', affix: true}
	}, {
		path: '/updatePassword',
		redirect: '/center'
	}, {
		path: '/pay',
		name: '支付',
		component: pay,
		meta: {icon:'', title:'pay'}
	}, {
		path: '/center',
		name: '个人信息',
		component: center,
		meta: {icon:'', title:'center'}
	}
	,{
		path: '/yonghu',
		name: '用户',
		component: yonghu
	}
	,{
		path: '/usedcar',
		name: '二手车',
		component: usedcar
	}
	,{
		path: '/usedcarforecast',
		name: '二手车预测',
		component: usedcarforecast
	}
	,{
		path: '/news',
		name: '公告',
		component: news
	}
	,{
		path: '/systemintro',
		name: '系统简介',
		component: systemintro
	}
	,{
		path: '/smsregistercode',
		name: '短信验证码',
		component: smsregistercode
	}
	,{
		path: '/users',
		name: '管理员',
		component: users
	}
	,{
		path: '/discussusedcar',
		name: '二手车',
		component: discussusedcar
	}
	,{
		path: '/config/:type',
		name: '配置管理',
		component: config
	}
	]
	},
	{
		path: '/login',
		name: 'login',
		component: Login,
		meta: {icon:'', title:'login'}
	},
	{
		path: '/board',
		name: 'board',
		component: Board,
		meta: {icon:'', title:'board'}
	},
	{
		path: '/register',
		name: 'register',
		component: register,
		meta: {icon:'', title:'register'}
	},
	{
		path: '*',
		component: NotFound
	}
]
//3.实例化VueRouter  注意：名字
const router = new VueRouter({
	mode: 'hash',
	/*hash模式改为history*/
	routes // （缩写）相当于 routes: routes
})
const originalPush = VueRouter.prototype.push
//修改原型对象中的push方法
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}
export default router;
