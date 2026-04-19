import VueRouter from 'vue-router'
//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Storeup from '../pages/storeup/list'
import payList from '../pages/pay'

import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import usedcarList from '../pages/usedcar/list'
import usedcarDetail from '../pages/usedcar/detail'
import usedcarAdd from '../pages/usedcar/add'
import usedcarforecastList from '../pages/usedcarforecast/list'
import usedcarforecastDetail from '../pages/usedcarforecast/detail'
import usedcarforecastAdd from '../pages/usedcarforecast/add'
import News from '../pages/news/news-list'
import NewsDetail from '../pages/news/news-detail'
import systemintroList from '../pages/systemintro/list'
import systemintroDetail from '../pages/systemintro/detail'
import systemintroAdd from '../pages/systemintro/add'
import smsregistercodeList from '../pages/smsregistercode/list'
import smsregistercodeDetail from '../pages/smsregistercode/detail'
import smsregistercodeAdd from '../pages/smsregistercode/add'
import discussusedcarList from '../pages/discussusedcar/list'
import discussusedcarDetail from '../pages/discussusedcar/detail'
import discussusedcarAdd from '../pages/discussusedcar/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'usedcar',
					component: usedcarList
				},
				{
					path: 'usedcarDetail',
					component: usedcarDetail
				},
				{
					path: 'usedcarAdd',
					component: usedcarAdd
				},
				{
					path: 'usedcarforecast',
					component: usedcarforecastList
				},
				{
					path: 'usedcarforecastDetail',
					component: usedcarforecastDetail
				},
				{
					path: 'usedcarforecastAdd',
					component: usedcarforecastAdd
				},
				{
					path: 'news',
					component: News
				},
				{
					path: 'newsDetail',
					component: NewsDetail
				},
				{
					path: 'systemintro',
					component: systemintroList
				},
				{
					path: 'systemintroDetail',
					component: systemintroDetail
				},
				{
					path: 'systemintroAdd',
					component: systemintroAdd
				},
				{
					path: 'smsregistercode',
					component: smsregistercodeList
				},
				{
					path: 'smsregistercodeDetail',
					component: smsregistercodeDetail
				},
				{
					path: 'smsregistercodeAdd',
					component: smsregistercodeAdd
				},
				{
					path: 'discussusedcar',
					component: discussusedcarList
				},
				{
					path: 'discussusedcarDetail',
					component: discussusedcarDetail
				},
				{
					path: 'discussusedcarAdd',
					component: discussusedcarAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
