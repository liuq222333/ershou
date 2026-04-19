<template>
	<div class="menu-preview">
		<el-menu
			:default-active="activeMenu"
			:unique-opened="true"
			mode="horizontal"
			class="admin-nav-menu"
		>
			<el-menu-item index="/" @click="menuHandler('')">
				<span class="admin-nav-menu__label">首页</span>
			</el-menu-item>
			<template
				v-for="(menu, index) in menuList.backMenu"
				v-if="menuList.backMenu && menu.child.length && menu.child[0].tableName != 'hasBoard' && menu.child[0].tableName != 'storeup' && (menu.child[0].tableName.length <= 7 || (menu.child[0].tableName.length > 7 && menu.child[0].tableName.substring(0, 7) != 'chapter'))"
			>
				<el-submenu
					v-if="menu.child.length > 1 || !horizontalIsMultiple"
					:key="'sub-' + index"
					:index="index + ''"
					:popper-append-to-body="true"
					popper-class="admin-nav-popper"
				>
					<template slot="title">
						<span class="admin-nav-menu__label">{{ nameChange(menu.menu, horizontalFlag) }}</span>
					</template>
					<el-menu-item
						v-for="(child, sort) in menu.child"
						:key="'child-' + index + '-' + sort"
						:index="'/' + child.tableName"
						@click="menuHandler(child.tableName)"
					>
						{{ child.menu }}
					</el-menu-item>
				</el-submenu>

				<el-menu-item
					v-if="menu.child.length <= 1 && horizontalIsMultiple"
					:key="'item-' + index"
					:index="'/' + menu.child[0].tableName"
					@click="menuHandler(menu.child[0].tableName)"
				>
					<span class="admin-nav-menu__label">{{ nameChange(menu.child[0].menu, horizontalFlag) }}</span>
				</el-menu-item>
			</template>
		</el-menu>
	</div>
</template>

<script>
	import menu from '@/utils/menu'

	export default {
		data() {
			return {
				menuList: [],
				role: '',
				horizontalFlag: false,
				horizontalIsMultiple: true
			}
		},
		computed: {
			activeMenu() {
				const route = this.$route
				const { meta, path } = route
				if (meta.activeMenu) {
					return meta.activeMenu
				}
				return path
			}
		},
		mounted() {
			let menus = menu.list()
			if (menus) {
				this.menuList = menus
			} else {
				let params = {
					page: 1,
					limit: 1,
					sort: 'id'
				}

				this.$http({
					url: 'menu/list',
					method: 'get',
					params: params
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.menuList = JSON.parse(data.data.list[0].menujson)
						this.$storage.set('menus', this.menuList)
					}
				})
			}

			this.role = this.$storage.get('role')

			for (let i = 0; i < this.menuList.length; i++) {
				if (this.menuList[i].roleName == this.role) {
					this.menuList = this.menuList[i]
					break
				}
			}
		},
		methods: {
			nameChange(value, type) {
				if (value === '订单管理') {
					return value
				}
				if (type) {
					return value + '管理'
				}
				return value
			},
			menuHandler(name) {
				this.$router.push('/' + name)
			}
		}
	}
</script>

<style lang="scss" scoped>
	.menu-preview {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		width: 100%;
		min-width: 0;
		overflow-x: auto;
		overflow-y: hidden;
		scrollbar-width: none;
	}

	.menu-preview::-webkit-scrollbar {
		display: none;
	}

	.admin-nav-menu {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		gap: 6px;
		width: max-content;
		min-width: 100%;
		border: 0;
		background: transparent;
	}

	.admin-nav-menu > .el-menu-item,
	.admin-nav-menu ::v-deep .el-submenu__title {
		position: relative;
		height: 48px;
		padding: 0 14px;
		border: 0 !important;
		border-radius: 12px;
		background: transparent !important;
		color: rgba(21, 33, 24, 0.74);
		font-size: 14px;
		font-weight: 560;
		line-height: 48px;
		transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
	}

	.admin-nav-menu > .el-menu-item:hover,
	.admin-nav-menu > .el-menu-item.is-active,
	.admin-nav-menu ::v-deep .el-submenu__title:hover,
	.admin-nav-menu ::v-deep .el-submenu.is-active .el-submenu__title {
		background: rgba(31, 143, 99, 0.12) !important;
		color: var(--admin-text) !important;
		box-shadow: inset 0 -2px 0 #42bf84;
	}

	.admin-nav-menu__label {
		display: inline-block;
		white-space: nowrap;
		letter-spacing: 0.01em;
	}

	.admin-nav-menu ::v-deep .el-submenu .el-submenu__icon-arrow {
		margin-top: -3px;
		color: currentColor;
	}
</style>
