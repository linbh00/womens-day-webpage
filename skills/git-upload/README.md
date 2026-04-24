# Git 上传 Skill

一个封装了将代码上传到 GitHub 完整过程的工具，可作为其他 AI 模型的调用接口。

## 功能

1. 初始化 git 仓库（如果尚未初始化）
2. 创建 .gitignore 文件（如果不存在）
3. 配置 git 用户名和邮箱
4. 添加所有文件并提交
5. 生成 SSH 密钥（如果需要）
6. 测试 GitHub 连接和认证
7. 检查仓库是否已存在
8. 指导用户在 GitHub 上创建仓库
9. 设置远程仓库地址
10. 推送代码到 GitHub
11. 智能处理常见错误和重试

## 目录结构

```
skills/git-upload/
├── git_upload.py    # 主脚本
└── README.md        # 说明文档
```

## 依赖

- Python 3.6+
- git
- SSH (用于生成密钥和推送代码)

## 使用方法

### 命令行方式

```bash
# 在项目根目录执行
python skills/git-upload/git_upload.py --repo_name "repository-name" --github_username "your-username" --email "your-email@example.com" [--description "repository-description"]
```

### 作为模块导入

```python
from skills.git_upload.git_upload import GitUploader

uploader = GitUploader(
    repo_name="my-project",
    github_username="your-username",
    email="your-email@example.com",
    description="Project description"
)
uploader.upload()
```

## 工作流程

1. 检查当前目录是否为 git 仓库，若不是则初始化
2. 创建 .gitignore 文件（如果不存在）
3. 配置 git 用户名和邮箱
4. 添加所有文件并提交
5. 生成 SSH 密钥（如果不存在）
6. 测试 GitHub 连接和认证
7. 检查仓库是否已存在
8. 如果仓库不存在，指导用户在 GitHub 上创建
9. 设置远程仓库地址为 SSH 方式
10. 推送代码到 GitHub
11. 智能处理常见错误并提供重试机制

## 注意事项

- 此工具需要用户手动在 GitHub 上创建仓库（通过浏览器）
- 确保网络连接正常，能够访问 GitHub
- 确保 git 和 SSH 已正确安装
- 首次使用需要在 GitHub 上添加 SSH 公钥

## 示例

### 示例 1：上传新项目

```bash
# 在新项目目录执行
python skills/git-upload/git_upload.py --repo_name "my-new-project" --github_username "linbh00" --email "lineric@qq.com" --description "My new project"
```

### 示例 2：上传现有项目

```bash
# 在现有项目目录执行
python skills/git-upload/git_upload.py --repo_name "existing-project" --github_username "linbh00" --email "lineric@qq.com"
```

## 错误处理

- 若 git 命令执行失败，会显示错误信息
- 若 SSH 密钥生成失败，会提示用户手动生成
- 若 GitHub 连接失败，会尝试继续执行
- 若仓库不存在，会指导用户创建
- 若推送失败，会分析错误并提供解决方案
- 支持常见错误的智能处理和重试

## 许可证

MIT
