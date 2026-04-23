#!/usr/bin/env python3
"""
Git 上传工具 - 封装将代码上传到 GitHub 的完整过程

功能：
1. 初始化 git 仓库（如果尚未初始化）
2. 创建 .gitignore 文件（如果不存在）
3. 添加所有文件并提交
4. 配置 git 用户名和邮箱
5. 在 GitHub 上创建仓库（如果不存在）
6. 配置 SSH 密钥（如果需要）
7. 推送代码到 GitHub

使用方法：
python git_upload.py --repo_name "repository-name" --github_username "your-username" --email "your-email@example.com"
"""

import os
import subprocess
import sys
import argparse
import json
import time

class GitUploader:
    def __init__(self, repo_name, github_username, email):
        self.repo_name = repo_name
        self.github_username = github_username
        self.email = email
        self.current_dir = os.getcwd()
        self.ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')
    
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
        self.run_command(f"git config user.name \"{self.github_username}"")
        self.run_command(f"git config user.email \"{self.email}"")
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
            return True
    
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
    
    def get_ssh_public_key(self):
        """获取 SSH 公钥内容"""
        public_key_path = f"{self.ssh_key_path}.pub"
        if os.path.exists(public_key_path):
            with open(public_key_path, 'r') as f:
                return f.read().strip()
        return None
    
    def create_github_repo(self):
        """在 GitHub 上创建仓库
        注意：此功能需要 GitHub CLI 或手动创建仓库
        这里提供手动创建的指导
        """
        print(f"请在 GitHub 上创建名为 '{self.repo_name}' 的仓库")
        print(f"访问：https://github.com/new")
        print("创建完成后按 Enter 键继续...")
        input()
        return True
    
    def add_ssh_key_to_github(self):
        """添加 SSH 密钥到 GitHub
        注意：此功能需要手动操作
        """
        public_key = self.get_ssh_public_key()
        if public_key:
            print("请将以下 SSH 公钥添加到 GitHub:")
            print("=" * 80)
            print(public_key)
            print("=" * 80)
            print("访问：https://github.com/settings/keys")
            print("点击 'New SSH key'，粘贴公钥并保存")
            print("添加完成后按 Enter 键继续...")
            input()
            return True
        else:
            print("✗ 无法获取 SSH 公钥")
            return False
    
    def set_remote_url(self):
        """设置远程仓库地址"""
        remote_url = f"git@github.com:{self.github_username}/{self.repo_name}.git"
        print(f"设置远程仓库地址: {remote_url}")
        self.run_command(f"git remote add origin {remote_url}")
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
            print(f"错误信息: {result.stderr if result else '未知错误'}")
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
        
        # 步骤 6: 创建 GitHub 仓库
        if not self.create_github_repo():
            return False
        
        # 步骤 7: 添加 SSH 密钥到 GitHub
        if not self.add_ssh_key_to_github():
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
    
    args = parser.parse_args()
    
    uploader = GitUploader(
        repo_name=args.repo_name,
        github_username=args.github_username,
        email=args.email
    )
    
    success = uploader.upload()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()