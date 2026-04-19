# Admin Login Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the admin login page so it matches the current management UI system with a minimalist glass-workspace layout while preserving the existing login flow.

**Architecture:** Keep the work inside the existing Vue 2 single-file component at `admin/src/views/login.vue`. Replace the legacy background-image template with a left-brand / right-panel shell, migrate the form controls to Element UI components so they inherit shared admin tokens, and keep the current role-loading plus login redirect logic intact.

**Tech Stack:** Vue 2 SFC, Element UI, SCSS, Vue CLI 4, existing admin design tokens in `src/assets/css/style.scss`

---

### Task 1: Replace the Legacy Login Markup with the New Split-Screen Shell

**Files:**
- Modify: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue`
- Test: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\admin-dev.log`

- [ ] **Step 1: Capture the current failing UI baseline**

Run:

```bash
cd C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin
npm run serve
```

Expected:

```text
DONE  Compiled successfully
App running at:
- Local:   http://localhost:8081/
```

Then open `http://localhost:8081/#/login` and confirm the current page still shows:

```text
- full-screen background image
- old centered white login box
- old title "基于python的瓜子二手车销售数据采集与趋势分析登录"
```

- [ ] **Step 2: Rewrite the `<template>` block into the approved left-brand / right-panel layout**

Replace the legacy template structure with this shell:

```vue
<template>
  <div class="admin-login">
    <div class="admin-login__ambient admin-login__ambient--left"></div>
    <div class="admin-login__ambient admin-login__ambient--right"></div>

    <section class="admin-login__shell">
      <aside class="admin-login__brand">
        <span class="admin-login__eyebrow">USED CAR INTELLIGENCE</span>
        <h1 class="admin-login__brand-title">二手车数据平台</h1>
        <p class="admin-login__brand-note">管理端入口</p>
      </aside>

      <el-form class="admin-login__panel" @submit.native.prevent="login">
        <div class="admin-login__panel-head">
          <span class="admin-login__tag">Admin Access</span>
          <h2>登录管理端</h2>
          <p>输入账号后进入工作台</p>
        </div>

        <div class="admin-login__fields">
          <el-input
            v-model="rulesForm.username"
            placeholder="请输入账号"
            autocomplete="username"
          />

          <el-input
            v-model="rulesForm.password"
            placeholder="请输入密码"
            :show-password="true"
            type="password"
            autocomplete="current-password"
            @keyup.enter.native="login"
          />

          <el-select
            v-if="roles.length > 1 && loginType <= 2"
            v-model="rulesForm.role"
            placeholder="请选择角色"
          >
            <el-option
              v-for="item in roles"
              v-if="loginType == 1 || (loginType == 2 && item.role != 'users')"
              :key="item.roleName"
              :label="item.roleName"
              :value="item.roleName"
            />
          </el-select>
        </div>

        <div class="admin-login__actions">
          <el-button
            v-if="loginType == 1 || loginType == 3 || loginType == 4"
            type="primary"
            class="admin-login__submit"
            @click="login"
          >
            进入系统
          </el-button>
          <p class="admin-login__hint">请使用已分配账号登录</p>
        </div>
      </el-form>
    </section>
  </div>
</template>
```

- [ ] **Step 3: Run the dev server to verify the new structure mounts without template errors**

Run:

```bash
cd C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin
npm run serve
```

Expected:

```text
DONE  Compiled successfully
App running at:
- Local:   http://localhost:8081/
```

- [ ] **Step 4: Commit the structural rewrite**

```bash
git add C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue
git commit -m "feat: rebuild admin login layout shell"
```

### Task 2: Keep the Login Logic Intact While Removing Legacy Background Dependencies

**Files:**
- Modify: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue`
- Test: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\admin-dev.log`

- [ ] **Step 1: Remove script state that only supported the old background-image page**

Update `data()` so it no longer depends on `baseUrl` or `indexBgUrl`, while keeping the active login state untouched:

```js
data() {
  return {
    verifyCheck2: false,
    flag: false,
    loginType: 1,
    rulesForm: {
      username: "",
      password: "",
      role: "",
    },
    menus: [],
    roles: [],
    tableName: "",
  };
},
```

- [ ] **Step 2: Remove the background-image fetch from `created()` and keep role loading in `mounted()`**

Replace the lifecycle section with this:

```js
mounted() {
  let menus = menu.list();
  this.menus = menus;

  for (let i = 0; i < this.menus.length; i++) {
    if (this.menus[i].hasBackLogin == '是') {
      this.roles.push(this.menus[i]);
    }
  }

  if (this.roles.length === 1) {
    this.rulesForm.role = this.roles[0].roleName;
  }
},
```

Delete this old code:

```js
created() {
  this.$http.get('config/info?name=bLoginBackgroundImg',).then(rs => {
    this.indexBgUrl = rs.data.data ? rs.data.data.value : ''
  })
},
```

- [ ] **Step 3: Keep `login()` and `loginPost()` logic unchanged except for minimal cleanup**

The only allowed logic cleanup in this task is formatting plus preserving the single-role auto-fill behavior. The redirect logic, token writes, session fetch, and role-to-table mapping must stay the same:

```js
if (this.roles.length > 1) {
  if (!this.rulesForm.role) {
    this.$message.error("请选择角色");
    return;
  }

  for (let i = 0; i < this.roles.length; i++) {
    if (this.roles[i].roleName == this.rulesForm.role) {
      this.tableName = this.roles[i].tableName;
    }
  }
} else {
  this.tableName = this.roles[0].tableName;
  this.rulesForm.role = this.roles[0].roleName;
}
```

- [ ] **Step 4: Verify the login script still compiles**

Run:

```bash
cd C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin
npm run serve
```

Expected:

```text
DONE  Compiled successfully
```

- [ ] **Step 5: Commit the script cleanup**

```bash
git add C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue
git commit -m "refactor: simplify admin login page state"
```

### Task 3: Apply the Shared Admin Glass Styles to the Login Page

**Files:**
- Modify: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue`
- Reference: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\assets\css\style.scss`

- [ ] **Step 1: Replace the old scoped SCSS with the new page shell, glass panel, and form styles**

Rewrite the `<style scoped lang="scss">` block using the shared admin tokens:

```scss
.admin-login {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 32px;
  background:
    radial-gradient(circle at top left, rgba(31, 143, 99, 0.16), transparent 30%),
    radial-gradient(circle at bottom right, rgba(31, 143, 99, 0.1), transparent 28%),
    linear-gradient(180deg, #f8fbf8 0%, #f2f5f2 100%);
}

.admin-login__ambient {
  position: absolute;
  border-radius: 999px;
  filter: blur(24px);
  pointer-events: none;
}

.admin-login__ambient--left {
  top: 8%;
  left: -6%;
  width: 360px;
  height: 360px;
  background: rgba(31, 143, 99, 0.08);
}

.admin-login__ambient--right {
  right: -4%;
  bottom: 10%;
  width: 320px;
  height: 320px;
  background: rgba(31, 143, 99, 0.06);
}

.admin-login__shell {
  position: relative;
  z-index: 1;
  min-height: calc(100vh - 64px);
  width: min(calc(100% - 32px), 1320px);
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(320px, 1fr) minmax(460px, 520px);
  gap: 48px;
  align-items: center;
}

.admin-login__brand {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-width: 520px;
}

.admin-login__eyebrow,
.admin-login__tag {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  min-height: 40px;
  padding: 0 18px;
  border: 1px solid rgba(21, 33, 24, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.46);
  color: var(--admin-text-soft);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.admin-login__brand-title {
  margin: 0;
  color: var(--admin-text);
  font-size: clamp(46px, 6vw, 84px);
  line-height: 0.98;
  letter-spacing: -0.05em;
}

.admin-login__brand-note,
.admin-login__panel-head p,
.admin-login__hint {
  margin: 0;
  color: var(--admin-text-soft);
  font-size: 15px;
  line-height: 1.8;
}

.admin-login__panel {
  padding: 32px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(30px) saturate(150%);
  box-shadow: var(--admin-shadow-medium);
}

.admin-login__panel-head {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 28px;
}

.admin-login__panel-head h2 {
  margin: 0;
  color: var(--admin-text);
  font-size: 34px;
  line-height: 1.08;
  letter-spacing: -0.04em;
}

.admin-login__fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.admin-login__actions {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 24px;
}

.admin-login__submit {
  width: 100%;
  min-height: 48px;
  font-size: 15px;
}
```

- [ ] **Step 2: Add scoped deep selectors so the embedded Element UI controls match the admin system**

Append these selectors in the same style block:

```scss
.admin-login ::v-deep .el-input__inner,
.admin-login ::v-deep .el-select .el-input__inner {
  min-height: 52px;
  border-radius: 14px !important;
  background: rgba(255, 255, 255, 0.84) !important;
  box-shadow: inset 0 0 0 1px rgba(21, 33, 24, 0.08);
}

.admin-login ::v-deep .el-input__inner:focus,
.admin-login ::v-deep .el-select .el-input.is-focus .el-input__inner {
  box-shadow:
    inset 0 0 0 1px rgba(31, 143, 99, 0.22),
    0 0 0 4px rgba(31, 143, 99, 0.08) !important;
}

.admin-login ::v-deep .el-input__suffix {
  display: flex;
  align-items: center;
  right: 14px;
}

.admin-login ::v-deep .el-input__suffix-inner {
  color: rgba(21, 33, 24, 0.45);
}
```

- [ ] **Step 3: Add responsive rules so the login page collapses into a vertical layout on narrow screens**

Append:

```scss
@media (max-width: 1100px) {
  .admin-login__shell {
    grid-template-columns: 1fr;
    gap: 24px;
    align-items: start;
  }

  .admin-login__brand-title {
    font-size: clamp(38px, 9vw, 64px);
  }
}

@media (max-width: 640px) {
  .admin-login {
    padding: 18px;
  }

  .admin-login__shell {
    width: 100%;
    min-height: calc(100vh - 36px);
  }

  .admin-login__panel {
    padding: 24px 18px;
  }
}
```

- [ ] **Step 4: Run the dev server and visually verify the new page**

Run:

```bash
cd C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin
npm run serve
```

Open `http://localhost:8081/#/login` and confirm:

```text
- no legacy background image
- left brand copy + right glass panel layout
- green primary button
- inputs match the current admin token system
- mobile width stacks vertically
```

- [ ] **Step 5: Commit the visual rewrite**

```bash
git add C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue
git commit -m "feat: restyle admin login page with glass workspace theme"
```

### Task 4: Manual Regression Check for Login Flow and Build Output

**Files:**
- Modify: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue`
- Test: `C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\package.json`

- [ ] **Step 1: Verify runtime login behavior using the real page**

With the dev server running, test these manual cases in the browser:

```text
1. Empty username -> shows "请输入用户名"
2. Empty password -> shows "请输入密码"
3. Multi-role mode without role -> shows "请选择角色"
4. Correct credentials -> redirects to /board or /
```

- [ ] **Step 2: Run a production build to catch packaging regressions**

Run:

```bash
cd C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin
npm run build
```

Expected:

```text
Build complete
```

If the build emits the known `vue-aplayer` / `hls.js` warning elsewhere in the app, note it as pre-existing and continue only if the login page bundle itself builds successfully.

- [ ] **Step 3: Review the final diff to ensure only the login page changed**

Run:

```bash
git diff -- C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue
```

Expected:

```text
Only template, script cleanup, and scoped style changes for the admin login page
```

- [ ] **Step 4: Commit the verification pass**

```bash
git add C:\Users\36018\Desktop\ershouche\ershouche7de79q94\api\templates\front\admin\src\views\login.vue
git commit -m "chore: verify admin login redesign"
```
