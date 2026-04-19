# 会话重点备忘（方便下次继续）

> 最近更新：2026-04-16

## 1. 项目基本信息

- **项目路径**：`C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin`
- **技术栈**：Vue 2.6.14 + Element UI + SCSS (node-sass 4.14.1) + webpack 4 + ECharts 5
- **启动脚本**：`npm run serve`（不是 `dev`）
- **大屏文件**：`src/views/board.vue`
- **首页文件**：`src/views/home.vue`
- **导航组件**：`src/components/index/IndexAsideStatic.vue`
- **面包屑**：`src/components/common/BreadCrumbs.vue`

## 2. 已完成的改动（board.vue）

上一轮会话里已经把 `board.vue` 从原来的"4 列车辆网格 + 传统图表"改造为 **HMI 驾驶舱风格**：

- 顶部品牌条（ONLINE 呼吸点 + 日期 + 返回）
- A1 车辆舞台：单车轮播（fade 过渡）+ 四角浮动信息（价格/年份/里程/城市）+ SVG 发光曲线 + 网格底纹
- 统计条（USERS / VEHICLES，细字重 200，48px 大数字）
- 下方 60/36 分栏：左=A2 预测表 + A3 价格预测输入框；右=B1~B6 六个 ECharts 图表
- 色系从霓虹色（#00d4ff）迁移到冰蓝白（`#9cc4e0` / `#cfe0f0` / `#6b94b8`）
- ECharts tooltip 背景统一改为 `rgba(8,12,21,0.9)`
- SCSS 色板 token 化：`$bg-deep #05080f` / `$accent #9cc4e0` / `$text-primary #f2f6fa` 等

## 3. 当前待决策事项

用户让我"先说改动意见再实施"，我提了 **五个下一步方向**，等用户回字母：

- **A. 增强仪表盘金属质感**：雷达扫描光圈 + L 型 HUD 装饰角 + 等宽工程字体
- **B. 极简杂志感（去科技化）**：去发光 trail，车图占更大，水墨灰蓝近黑白
- **C. 数据流动态**：顶部滚动 tick 数据流 + 平移等高线 + 图表"实时"脉冲点
- **D. 三列式布局重构**：左 KPI 栈 / 中车辆 / 右图表堆栈（特斯拉中控感）
- **E. 局部微调**：表格加 LIVE 标、A3 换指针 gauge、底部脚注状态栏

## 4. 启动环境问题（未解决）

本机 **Node 24 + npm 11** 与项目依赖 `node-sass@4.14.1` 不兼容，所有 `npm install` 都会崩在：

```
npm error Exit handler never called!
```

已尝试失败：
- `npm install`
- `npm install --legacy-peer-deps`
- `npm install sass@1.32.13 --legacy-peer-deps`（想换 dart-sass 也崩）

### 下次可尝试的修复路径（按推荐度）

**方案 A（推荐）：用 nvm 切回 Node 16**
```bash
nvm install 16.20.2
nvm use 16.20.2
cd api/templates/front/admin
rd /s /q node_modules
del package-lock.json
npm install
npm run serve
```

**方案 B：把 node-sass 换成 dart-sass**
- 改 `package.json`：删 `node-sass`，加 `"sass": "^1.70.0"`
- 全局把 `<style lang="scss" scoped>` 里的 `/deep/` 替换成 `::v-deep`（dart-sass 不认 `/deep/`）
- 需要检查的位置：`board.vue` / `IndexAsideStatic.vue` / `BreadCrumbs.vue` 以及其他视图

**方案 C：用 cnpm 或 pnpm**
```bash
npm i -g pnpm
pnpm install
pnpm run serve
```

## 5. 开工前的第一步

下次进来先问用户两件事：
1. **样式方向选哪个字母？**（A/B/C/D/E，可多选）
2. **环境修复走哪条路？**（nvm 切 Node 16 / 换 dart-sass / pnpm）

样式方向定了就改 `board.vue`，环境方向定了再决定是否自动执行命令。

## 6. 风格参考

用户最早发的 4 张参考图是特斯拉/奔驰类的 HMI 驾驶舱大屏（深色 + 冰蓝 + 细字重 + 网格底纹 + 发光曲线）。当前 `board.vue` 已经基本对齐这个风格，五个方向里 A/C/D 都是在此基础上再深化，B 是推倒重来，E 是细节补强。
