# Daily Tasks 每日任务

基于 GitHub Actions 的每日自动任务脚本，支持：

- **米游社签到** - 崩坏：星穹铁道、原神等游戏签到
- **天气推送** - 新加坡每日天气预报
- **番剧更新** - 每日番剧放送提醒

所有任务结果通过 **PushPlus** 推送到微信。

## 功能说明

### 1. 米游社签到
- 支持：崩坏：星穹铁道（已启用）、原神、崩坏3、绝区零
- 自动获取绑定角色并签到
- 启用/禁用游戏：编辑 `tasks/miyoushe.py` 中的 `GAMES` 配置

### 2. 天气推送
- 使用新加坡政府免费 API (data.gov.sg)
- 推送当日温度、湿度、天气预报
- 可自定义区域（默认：Queenstown / NUS 所在区域）

### 3. 番剧更新
- 使用 Bangumi API 获取每日放送
- 可配置追番列表，只提醒关注的番剧
- 未配置则推送当日所有更新

## 使用方法

### 1. Fork 本仓库

### 2. 配置 Secrets

进入仓库 `Settings` → `Secrets and variables` → `Actions`：

| Secret | 必填 | 说明 |
|--------|------|------|
| `MIYOUSHE_COOKIE` | 是 | 米游社 Cookie |
| `PUSHPLUS_TOKEN` | 是 | PushPlus Token |

### 3. 配置 Variables（可选）

在 `Settings` → `Secrets and variables` → `Actions` → `Variables`：

| Variable | 默认值 | 说明 |
|----------|--------|------|
| `WEATHER_AREA` | `Queenstown` | 新加坡天气区域 |
| `BANGUMI_WATCHLIST` | 空 | 追番列表，逗号分隔 |

**新加坡区域示例**：
- `Queenstown` - NUS 主校区
- `Bukit Timah` - NUS 法学院
- `Orchard` - 乌节路
- `Jurong East` / `Jurong West`
- `Tampines` / `Bedok` / `Pasir Ris`

**追番列表示例**：
```
葬送的芙莉莲,咒术回战,进击的巨人
```

### 4. 启用 Actions

进入 `Actions` 标签页，启用 workflow。

### 5. 手动测试

点击 `Run workflow` 手动运行测试。

## 运行时间

默认每天 **北京时间 8:00** (UTC 0:00) 自动运行。

修改时间：编辑 `.github/workflows/sign.yml` 中的 cron 表达式。

## 项目结构

```
├── main.py                 # 主入口
├── tasks/
│   ├── miyoushe.py         # 米游社签到
│   ├── weather.py          # 天气推送
│   └── bangumi.py          # 番剧更新
├── utils/
│   └── push.py             # 推送模块
├── .github/workflows/
│   └── sign.yml            # GitHub Actions 配置
└── README.md
```

## 添加新任务

1. 在 `tasks/` 目录创建新模块
2. 实现 `run()` 函数，返回消息字符串或列表
3. 在 `main.py` 中导入并调用

## 免责声明

本项目仅供学习交流使用。
