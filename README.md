# petoken

petoken 是一个 Windows 桌宠：它自动跟随当前打开的 Codex 任务，并在需要时显示精确的本地 token 用量、5 小时/每周额度、重置倒计时和 CAD API 等价成本估算。平时只显示已批准的角色；鼠标停留或单击角色时，用量面板才会出现在旁边。

![Python](https://img.shields.io/badge/Python-3.13-3776AB) ![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4) ![License](https://img.shields.io/badge/code-MIT-91E4F2)

## 使用

1. 在 GitHub Releases 下载 `CodexWisp-Windows-x64.zip`。
2. 解压整个文件夹，双击 `CodexWisp.exe`。不要只复制 exe；旁边的 `_internal` 文件夹也是程序的一部分。
3. 保持 Codex 桌面客户端开启。桌宠会读取当前任务标题和本机已经记录的数字用量。

交互方式：

- 鼠标悬停约 0.35 秒或单击桌宠：显示用量面板。
- 鼠标离开桌宠和面板约 0.7 秒：回到当前桌宠状态。
- 拖动桌宠或面板：移动位置；`Alt + 方向键` 可移动面板。
- 右键桌宠或托盘图标：设置、完整 Token Analytics、暂停动画或退出。
- 面板中的 `Token Analytics`：查看全部原始字段、派生指标、模型、会话和本地历史。

## 桌宠状态

状态优先级固定为：打开的用量面板 → 麦克风使用中 → 音乐播放 → 正在打字 → 待机。输入检测只记最后一次按键的时间，不读取或保存输入内容；麦克风检测只查看 Windows 捕获会话状态，程序不会打开或录制麦克风；音乐检测使用 Windows 系统媒体控制，不读取曲名。

短暂变化会经过进入/退出延迟，避免姿势闪烁。未发生特殊活动时始终使用批准的原始待机角色与默认 UI。

## Token Analytics

紧凑面板保留 Total、Input、Output、Cache hit、New work、Context、5-hour、Weekly 和 CAD 估算。展开窗口另外显示：

- 原始：`input_tokens`、`cached_input_tokens`、`cache_write_input_tokens`、`output_tokens`、`reasoning_output_tokens`、`total_tokens`
- 派生：未缓存输入、非推理输出、缓存命中率、新工作量、输出比例、推理占比
- 比较：Claude-style Raw Processed，并清楚标记为比较指标，不替代 OpenAI 官方 total
- 分组：按模型、会话、本地日期，以及今天、最近 7/30 个日历日、本地已记录 lifetime
- 原始快照：当前会话最新 `total_token_usage` / `last_token_usage`，包括未解释的额外字段

缓存输入已包含在 input 中，推理 token 已包含在 output 中，因此两者不会再次加入官方总量。字段缺失或覆盖不完整时显示 `N/A` 和已知小计，不用假零补齐。完整公式和本机实际字段见 [Token accounting](docs/TOKEN_ACCOUNTING.md)。

成本是按已记录模型、服务档位、长上下文规则和加拿大央行 USD/CAD 汇率计算的 API 等价估算，不是 ChatGPT/Codex 订阅账单。未知模型价格或未知 cache-write 拆分会明确标成部分估算

## 数据与隐私

petoken 只读取：

- Codex 的只读 SQLite 任务元数据和 JSONL 中的数字用量事件
- Codex 自己的只读 `account/rateLimits/read` 结果
- Windows 当前任务标题、按键活动时间、音频捕获/媒体播放布尔状态
- 加拿大央行的公开 USD/CAD 日汇率

它不发送模型请求，不导出对话，不读取 Codex 凭据，不保存按键内容、音频或媒体名称，也不会把本地用量上传到本仓库。

## 从源码运行

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe widget.py
```

测试和独立本地记录核对：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools\verify_local.py
```

构建 Windows 发行版：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\build.ps1 -Package
```

输出位于 `dist\CodexWisp\`，压缩包为 `dist\CodexWisp-Windows-x64.zip`。

## 技术限制

- “Lifetime”仅表示当前机器仍在 Codex 索引中的记录，不包括已删除、仅云端或尚未同步的数据。
- 当前任务依赖 Codex 窗口的 Windows Accessibility 标题；识别不唯一时会明确退回最近任务，也可在设置中固定。
- 只有接入 Windows System Media Transport Controls 的播放器能可靠触发音乐状态。
- Context 是最新记录的上下文比例，可能与 CLI 为输出保留空间后的显示略有差别。

源代码采用 [MIT License](LICENSE)。角色图片不在 MIT 授权范围内，具体见 [Artwork and attribution](docs/ARTWORK.md)。本项目是独立工具，与 OpenAI 或任何游戏发行商无隶属或背书关系。
