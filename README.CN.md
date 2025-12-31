[English](README.md) 

# FastGithub 介绍 

FastGithub 是一个基于 PyQt5 开发的图形化 Github 加速器工具，通过自动更新本地 hosts 文件来解决 Github 访问慢或无法访问的问题。工具界面简洁直观，操作简单，支持 Windows/macOS/Linux 多平台，所有操作结果均会通过弹窗提示，并提供详细的操作日志。

### ✨ 核心功能

- 🚀 一键更新 Github 相关 hosts 条目，自动获取最新的 IP 地址
- 🔄 一键恢复本地 hosts 文件至默认状态（移除 Github 相关条目）
- 📝 实时日志记录，带时间戳显示所有操作过程
- 🎨 仿主流加速器的简洁图形界面，状态实时显示
- 🚨 操作结果弹窗提示（成功/失败），错误信息清晰
- ⚡ 后台线程处理，避免界面卡顿
- 💻 跨平台支持（Windows/macOS/Linux）

### 📋 环境要求

- Python 3.6 及以上版本
- Windows/macOS/Linux 操作系统
- 管理员/root 权限（修改 hosts 文件必需）

### 🚀 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/YuxuanBai1/FastGithub.git
cd FastGithub
```

### 2. 安装依赖
```bash
pip install requests PyQt5
```

### 📖 使用指南

### 1. 运行程序
#### Windows 系统
- **必须以管理员身份运行**：右键点击命令提示符/终端，选择「以管理员身份运行」，然后执行：
  ```bash
  python main.py
  ```

#### macOS/Linux 系统
- 使用 root 权限运行：
  ```bash
  sudo python main.py
  ```

### 2. 操作说明
| 按钮       | 功能说明                                              |
| ---------- | ----------------------------------------------------- |
| 更新 Hosts | 自动获取最新的 Github hosts 信息并更新本地 hosts 文件 |
| 恢复默认   | 移除 hosts 文件中的 Github 相关条目，恢复至原始状态   |

### 3. 界面说明
- **状态显示**：实时展示当前操作状态（未启动/正在更新/更新成功/更新失败/已恢复默认）
- **操作日志**：记录所有操作的时间和详细信息，便于排查问题
- **底部提示**：提醒用户以管理员/root 身份运行程序

### 📁 项目目录说明

```text
FastGithub/
├── main.py          # 项目入口文件（核心逻辑实现）
├── app.ico          # 程序图标（可选）
└── LICENSE # 许可证
```

### 🔧 常见问题解决

- Q: 运行程序提示「权限不足」？A: 该工具需要修改系统级的 hosts 文件，必须以**管理员（Windows）** 或 **root（macOS/Linux）** 身份运行程序。

- Q: 程序启动后界面无图标？A: 确保 `app.ico` 文件放在项目根目录下，或删除代码中 `self.setWindowIcon(QIcon("app.ico"))` 行即可。

### ⚠️注意事项

1. 请确保网络可以访问 `https://raw.hellogithub.com/hosts.json`（该接口提供最新的 Github hosts 信息）
2. 修改 hosts 文件前，工具会自动保留原有内容，仅替换/添加 Github 相关条目
3. 若使用代理工具，建议先关闭代理再使用本工具
4. 本工具仅用于学习和自用，请勿用于商业用途

### 📄 许可证

本项目采用 MIT 许可证开源，可自由修改、分发和商用，详见 LICENSE 文件。