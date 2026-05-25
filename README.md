# UnrealWwiseAssetTool

自动化 Wwise SoundBank 生成与 Unreal Engine 资产同步的命令行工具。

## 功能

1. **生成 SoundBank** — 调用 WwiseConsole.exe 为指定平台和语言生成 SoundBank
2. **Reconcile 同步** — 调用 Unreal Editor Commandlet（WwiseReconcileCommandlet）将生成的音频资产同步到 Unreal 项目中

## 环境要求

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) 包管理器
- Audiokinetic Wwise（已安装 WwiseConsole.exe）
- Unreal Engine（已安装 UnrealEditor-Cmd.exe）
- Wwise Unreal Integration 插件

## 安装

```bash
uv sync
```

## 配置

编辑 `config.json`：

```json
{
    "wwise_console_path": "D:\\Audiokinetic\\Wwise2024\\Authoring\\x64\\Release\\bin\\WwiseConsole.exe",
    "wwise_project_path": "../../YourWwiseProject/YourProject.wproj",
    "wwise_bank_output_path": "../../YourWwiseProject/GeneratedSoundBanks",
    "platforms": ["Windows"],
    "languages": ["English(US)"],
    "unreal_cmd_path": "D:\\Epic Games\\UE_5.7\\Engine\\Binaries\\Win64\\UnrealEditor-Cmd.exe",
    "unreal_uproject_path": "../../YourProject.uproject",
    "unreal_wwise_audio_path": "../../Content/WwiseAudio"
}
```

| 字段 | 说明 |
|------|------|
| `wwise_console_path` | WwiseConsole.exe 绝对路径 |
| `wwise_project_path` | Wwise 工程文件（.wproj）路径，支持相对路径 |
| `wwise_bank_output_path` | SoundBank 输出目录 |
| `platforms` | 目标平台列表，必须是 .wproj 中已定义的平台子集 |
| `languages` | 目标语言列表，必须是 .wproj 中已定义的语言子集 |
| `unreal_cmd_path` | UnrealEditor-Cmd.exe 绝对路径 |
| `unreal_uproject_path` | Unreal 工程文件（.uproject）路径 |
| `unreal_wwise_audio_path` | Unreal 项目中 Wwise 音频资产目录 |

相对路径基于 `config.json` 所在目录解析。

## 使用

```bash
uv run main.py
```

执行流程：加载配置 → 校验路径与平台/语言有效性 → 生成 SoundBank → Reconcile 同步到 Unreal。
