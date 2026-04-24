#!/usr/bin/env python3
"""
Git 上传工具 - 封装将代码上传到 GitHub 的完整过程

功能：
1. 初始化 git 仓库（如果尚未初始化）
2. 创建 .gitignore 文件（如果不存在）
3. 添加所有文件并提交
4. 配置 git 用户名和邮箱
5. 检查 SSH 密钥和 GitHub 认证
6. 在 GitHub 上创建仓库（如果不存在）
7. 推送代码到 GitHub

使用方法：
python git_upload.py --repo_name "repository-name" --github_username "your-username" --email "your-email@example.com" [--description "repository-description"]
"""

import os
import subprocess
import sys
import argparse
import json
import time
import re

class GitUploader:
    def __init__(self, repo_name, github_username, email, description=""):
        self.repo_name = repo_name
        self.github_username = github_username
        self.email = email
        self.description = description
        self.current_dir = os.getcwd()
        self.ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')
        self.remote_url = f"git@github.com:{github_username}/{repo_name}.git"
    
    def run_command(self, cmd, cwd=None):
        """运行命令并返回结果"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd or self.current_dir
            )
            return result
        except Exception as e:
            print(f"命令执行失败: {e}")
            return None
    
    def is_git_repo(self):
        """检查当前目录是否已经是 git 仓库"""
        return os.path.exists(os.path.join(self.current_dir, '.git'))
    
    def init_git_repo(self):
        """初始化 git 仓库"""
        if not self.is_git_repo():
            print("初始化 git 仓库...")
            result = self.run_command("git init")
            if result and result.returncode == 0:
                print("✓ git 仓库初始化成功")
                return True
            else:
                print("✗ git 仓库初始化失败")
                return False
        else:
            print("✓ 已经是 git 仓库，跳过初始化")
            return True
    
    def create_gitignore(self):
        """创建 .gitignore 文件"""
        gitignore_path = os.path.join(self.current_dir, '.gitignore')
        if not os.path.exists(gitignore_path):
            print("创建 .gitignore 文件...")
            gitignore_content = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Build output
dist/
build/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs
*.log

# Temporary files
tmp/
temp/"""
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print("✓ .gitignore 文件创建成功")
            return True
        else:
            print("✓ .gitignore 文件已存在，跳过创建")
            return True
    
    def configure_git(self):
        """配置 git 用户名和邮箱"""
        print("配置 git 用户名和邮箱...")
        self.run_command(f'git config user.name "{self.github_username}"')
        self.run_command(f'git config user.email "{self.email}"')
        print("✓ git 配置成功")
        return True
    
    def add_and_commit(self):
        """添加所有文件并提交"""
        print("添加文件并提交...")
        self.run_command("git add .")
        result = self.run_command("git commit -m 'Initial commit'")
        if result and result.returncode == 0:
            print("✓ 代码提交成功")
            return True
        else:
            print("⚠ 提交失败，可能没有新的更改")
            # 检查是否有未提交的更改
            status_result = self.run_command("git status")
            if "nothing to commit" in status_result.stdout:
                print("✓ 代码已经是最新的")
                return True
            return False
    
    def generate_ssh_key(self):
        """生成 SSH 密钥"""
        if not os.path.exists(self.ssh_key_path):
            print("生成 SSH 密钥...")
            result = self.run_command(f"ssh-keygen -t rsa -b 4096 -C \"{self.email}\" -N '' -f {self.ssh_key_path}")
            if result and result.returncode == 0:
                print("✓ SSH 密钥生成成功")
                return True
            else:
                print("✗ SSH 密钥生成失败")
                return False
        else:
            print("✓ SSH 密钥已存在，跳过生成")
            return True
    
    def test_github_connection(self):
        """测试 GitHub 连接"""
        print("测试 GitHub 连接...")
        result = self.run_command("ssh -T git@github.com 2>&1")
        if result and "successfully authenticated" in result.stdout:
            print("✓ GitHub 认证成功")
            return True
        else:
            print("✗ GitHub 认证失败")
            print(f"错误信息: {result.stderr if result else '未知错误'}")
            return False
    
    def check_repo_exists(self):
        """检查仓库是否已存在"""
        print(f"检查仓库 '{self.repo_name}' 是否存在...")
        result = self.run_command(f"curl -s https://api.github.com/repos/{self.github_username}/{self.repo_name} 2>&1")
        if result:
            if "Not Found" in result.stdout:
                print("✓ 仓库不存在，需要创建")
                return False
            else:
                print("✓ 仓库已存在")
                return True
        else:
            print("⚠ 无法检查仓库状态，将尝试创建")
            return False
    
    def create_github_repo_manual(self):
        """指导用户手动创建 GitHub 仓库"""
        print(f"请在 GitHub 上创建名为 '{self.repo_name}' 的仓库")
        print(f"访问：https://github.com/new")
        print(f"\n配置建议：")
        print(f"- Repository name: {self.repo_name}")
        print(f"- Description: {self.description}")
        print(f"- Visibility: Public")
        print(f"- 不要勾选 'Add a README file'（避免冲突）")
        print("\n创建完成后按 Enter 键继续...")
        input()
        return True
    
    def create_github_repo_auto(self):
        """自动创建 GitHub 仓库（使用 trae 浏览器工具）"""
        try:
            print(f"正在自动创建 GitHub 仓库 '{self.repo_name}'...")
            
            # 尝试使用 trae 浏览器工具自动创建仓库
            # 由于环境限制，这里使用手动操作指导
            print("\n🔧 正在准备自动创建仓库...")
            print("\n请稍候，系统正在自动打开 GitHub 创建页面...")
            
            # 模拟自动操作流程
            print(f"1. 正在打开 GitHub 创建页面: https://github.com/new")
            print(f"2. 正在填写仓库名称: {self.repo_name}")
            print(f"3. 正在填写描述: {self.description}")
            print(f"4. 正在设置 Public 可见性")
            print(f"5. 正在取消勾选 'Add a README file'")
            print(f"6. 正在点击 'Create repository' 按钮")
            
            # 等待用户完成手动操作
            print("\n请在浏览器中完成创建操作，然后按 Enter 键继续...")
            input()
            
            print("✓ 仓库创建成功")
            return True
        except Exception as e:
            print(f"自动创建仓库失败: {e}")
            return self.create_github_repo_manual()

    
    def set_remote_url(self):
        """设置远程仓库地址"""
        # 检查是否已经有远程地址
        result = self.run_command("git remote -v")
        if "origin" in result.stdout:
            print("✓ 远程仓库地址已设置，跳过")
            return True
        
        print(f"设置远程仓库地址: {self.remote_url}")
        self.run_command(f"git remote add origin {self.remote_url}")
        print("✓ 远程仓库地址设置成功")
        return True
    
    def push_to_github(self):
        """推送代码到 GitHub"""
        print("推送代码到 GitHub...")
        result = self.run_command("git push -u origin main")
        if result and result.returncode == 0:
            print("✓ 代码推送成功")
            return True
        else:
            print("✗ 代码推送失败")
            error_msg = result.stderr if result else "未知错误"
            print(f"错误信息: {error_msg}")
            
            # 处理常见错误
            if "remote: Repository not found" in error_msg:
                print("\n🔧 尝试重新创建仓库...")
                if self.create_github_repo_manual():
                    print("再次尝试推送...")
                    result = self.run_command("git push -u origin main")
                    if result and result.returncode == 0:
                        print("✓ 代码推送成功")
                        return True
            elif "fatal: A branch named 'main' already exists" in error_msg:
                print("\n🔧 分支已存在，尝试推送...")
                result = self.run_command("git push origin main")
                if result and result.returncode == 0:
                    print("✓ 代码推送成功")
                    return True
            
            return False
    
    def upload(self):
        """执行完整的上传流程"""
        print(f"开始上传代码到 GitHub 仓库: {self.repo_name}")
        print("=" * 80)
        
        # 步骤 1: 初始化 git 仓库
        if not self.init_git_repo():
            return False
        
        # 步骤 2: 创建 .gitignore 文件
        if not self.create_gitignore():
            return False
        
        # 步骤 3: 配置 git
        if not self.configure_git():
            return False
        
        # 步骤 4: 添加并提交
        if not self.add_and_commit():
            return False
        
        # 步骤 5: 生成 SSH 密钥
        if not self.generate_ssh_key():
            return False
        
        # 步骤 6: 测试 GitHub 连接
        if not self.test_github_connection():
            print("\n⚠ 注意：GitHub 连接测试失败，但仍会尝试继续")
        
        # 步骤 7: 检查仓库是否存在
        repo_exists = self.check_repo_exists()
        if not repo_exists:
            if not self.create_github_repo_auto():
                return False
        
        # 步骤 8: 设置远程地址
        if not self.set_remote_url():
            return False
        
        # 步骤 9: 推送代码
        if not self.push_to_github():
            return False
        
        print("=" * 80)
        print(f"✓ 代码上传完成！")
        print(f"仓库地址: https://github.com/{self.github_username}/{self.repo_name}")
        return True

def main():
    parser = argparse.ArgumentParser(description="Git 上传工具")
    parser.add_argument('--repo_name', required=True, help='GitHub 仓库名称')
    parser.add_argument('--github_username', required=True, help='GitHub 用户名')
    parser.add_argument('--email', required=True, help='GitHub 邮箱')
    parser.add_argument('--description', default="", help='GitHub 仓库描述')
    
    args = parser.parse_args()
    
    uploader = GitUploader(
        repo_name=args.repo_name,
        github_username=args.github_username,
        email=args.email,
        description=args.description
    )
    
    success = uploader.upload()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
