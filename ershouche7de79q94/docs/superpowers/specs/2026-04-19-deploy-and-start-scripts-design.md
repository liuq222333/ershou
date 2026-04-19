# 部署检查与启动脚本设计

## 背景

当前项目已经能在本机跑通，但启动路径仍然分散：

- 后端依赖项目虚拟环境中的 Python 解释器，不能直接依赖全局 `python`
- 管理端和用户端都需要分别进入各自目录执行 `npm run serve`
- 历史文档和旧脚本仍然引用 `manage.py run`、旧端口和过期说明，容易误导后续启动

这次不做“自动安装依赖”的重部署，而是先提供一套稳定的本地脚本：

- 一个“部署检查脚本”，只检查环境是否满足启动条件
- 一个“项目启动脚本”，按当前项目真实命令拉起三端服务

## 目标

- 提供统一的本地环境检查入口
- 提供统一的本地启动入口
- 不自动安装、不自动修改依赖、不自动建库
- 把检查结果和启动日志落到项目内，方便排查
- 兼容当前项目的真实运行方式和端口配置

## 非目标

- 不接入 Docker、pm2、Supervisor 等额外进程方案
- 不自动执行 `pip install`、`npm install`
- 不自动初始化数据库表结构
- 不处理生产部署，仅面向当前 Windows 本地开发/演示环境

## 当前真实运行约束

### 后端

- 项目根目录：`C:\Users\36018\Desktop\ershouche\ershouche7de79q94`
- 实际启动命令：`.\.venv311\Scripts\python.exe .\run.py`
- 默认端口：`8080`
- 数据库配置来源：`config.ini`
- 已确认依赖中包含 `Flask==1.1.2`、`PyMySQL==1.0.2`

### 管理端

- 目录：`api\templates\front\admin`
- 启动命令：`npm run serve`
- 前端开发端口：`8081`
- 代理后端前缀：`/ershouche7de79q94`

### 用户端

- 目录：`api\templates\front\front`
- 启动命令：`npm run serve`
- 前端开发端口：`8082`
- 代理后端前缀：`/ershouche7de79q94`

### 环境假设

- Windows + PowerShell
- Node 16 可用
- 项目虚拟环境 `.venv311` 已存在
- 前端依赖目录 `node_modules` 可能已经存在，也可能缺失，需要由检查脚本显式给出状态

## 方案对比

### 方案 A：仅保留 `.bat` 脚本

优点：

- 双击即可执行

缺点：

- 结构化检查能力弱
- 错误输出不够清晰
- 三端联动启动和日志管理不够稳

### 方案 B：PowerShell 主脚本 + `.bat` 包装入口（采用）

优点：

- 更适合 Windows 本地环境
- 可以做清晰的检查、端口检测和日志输出
- 同时保留双击入口

缺点：

- 会新增多个脚本文件

### 方案 C：Python 启动器

优点：

- 逻辑可读性较好

缺点：

- 反而会把脚本能力依赖到 Python 环境本身
- 对“先检查再启动”的本地场景并不比 PowerShell 更简单

## 采用方案

采用方案 B：使用 PowerShell 作为主入口，`.bat` 作为包装入口。

这次会新增四个脚本：

- `deploy-check.ps1`
- `deploy-check.bat`
- `start-project.ps1`
- `start-project.bat`

必要时可以额外补一个日志目录：

- `logs\`

## 脚本职责设计

### 1. `deploy-check.ps1`

这是“只检查、不安装”的部署检查脚本。

职责：

- 校验项目是否在正确根目录执行
- 检查 `config.ini` 是否存在
- 检查 `.venv311\Scripts\python.exe` 是否存在
- 使用项目虚拟环境执行最小导入检查：
  - `import flask`
  - `import pymysql`
- 检查管理端 `package.json` 是否存在
- 检查用户端 `package.json` 是否存在
- 检查 `node` / `npm` 是否可用
- 检查 Node 主版本是否为 16
- 检查两个前端目录下是否存在 `node_modules`
- 检查 `8080`、`8081`、`8082` 是否已被占用
- 输出统一检查报告，明确区分：
  - `PASS`
  - `WARN`
  - `FAIL`

输出要求：

- 屏幕打印简明结果
- 同时写入 `logs\deploy-check.log`
- 检查失败时给出可执行建议，但不自动处理

### 2. `deploy-check.bat`

这是面向双击和传统命令行习惯的包装入口。

职责：

- 切换到项目根目录
- 调用 `powershell -ExecutionPolicy Bypass -File .\deploy-check.ps1`

### 3. `start-project.ps1`

这是统一启动脚本。

职责：

- 先执行与启动强相关的基础检查：
  - Python 虚拟环境是否存在
  - Node / npm 是否可用
  - 管理端和用户端 `node_modules` 是否存在
- 创建 `logs\` 目录
- 检查 `8080`、`8081`、`8082` 是否被占用
- 若端口空闲，则启动对应服务
- 若端口已被占用，则提示该端口可能已有实例，不重复拉起
- 分别将输出写入：
  - `logs\backend.log`
  - `logs\backend-error.log`
  - `logs\admin.log`
  - `logs\admin-error.log`
  - `logs\front.log`
  - `logs\front-error.log`
- 启动后输出访问地址：
  - 后端：`http://localhost:8080`
  - 管理端：`http://localhost:8081/#/login`
  - 用户端：`http://localhost:8082`

进程启动方式：

- 后端在项目根目录执行：
  - `.\.venv311\Scripts\python.exe .\run.py`
- 管理端在 `api\templates\front\admin` 执行：
  - `npm run serve`
- 用户端在 `api\templates\front\front` 执行：
  - `npm run serve`

### 4. `start-project.bat`

职责：

- 切换到项目根目录
- 调用 `powershell -ExecutionPolicy Bypass -File .\start-project.ps1`

## 运行策略

### 检查策略

脚本不尝试修复环境，只报告真实状态。

例如：

- 若 `python.exe` 缺失，报告 `FAIL: 未找到 .venv311`
- 若 `pymysql` 导入失败，报告 `FAIL: Python 依赖不完整`
- 若 Node 不是 16.x，报告 `WARN: 当前 Node 版本与项目推荐版本不一致`
- 若 `node_modules` 缺失，报告 `FAIL: 前端依赖未安装`

### 端口策略

端口检查使用：

- `8080`
- `8081`
- `8082`

处理规则：

- 端口空闲：允许启动
- 端口已占用：不强制关闭，不覆盖，只提示

### 日志策略

所有脚本日志都写入项目内 `logs` 目录，避免把输出散落到系统临时目录。

日志目标：

- 检查脚本用于确认环境状态
- 启动脚本用于后续追踪前后端报错

## 文件变更范围

### 新增文件

- `deploy-check.ps1`
- `deploy-check.bat`
- `start-project.ps1`
- `start-project.bat`

### 可能新增目录

- `logs\`

### 本轮不改动

- 不修改数据库结构
- 不修改业务页面
- 不改动前后端接口
- 不新增自动安装依赖逻辑

## 验收标准

满足以下条件则视为本轮完成：

1. 执行 `.\deploy-check.ps1` 能输出完整环境检查结果
2. 执行 `.\deploy-check.bat` 能正确转发到 PowerShell 检查脚本
3. 执行 `.\start-project.ps1` 能按真实命令启动后端、管理端、用户端
4. 执行 `.\start-project.bat` 能正确转发到 PowerShell 启动脚本
5. 启动成功后能看到正确访问地址和日志路径
6. 检查脚本不会自动安装依赖
7. 启动脚本不会自动停止其他未知进程

## 后续实施说明

下一步实施时，优先顺序如下：

1. 先写设计对应的实施计划
2. 再创建 PowerShell 主脚本
3. 再补 `.bat` 包装入口
4. 最后执行一次本地验证，确认检查输出与启动输出符合预期
