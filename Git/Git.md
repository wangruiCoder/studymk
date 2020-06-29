# Git学习笔记
---
## 克隆项目
`git clone https://github.com/****.git`

## git ssh key
需要本地已经安装了git
电脑桌面右键选择git bash here
1. cd ~/.ssh
2. git config --global user.name "***"
3. git config --global user.email  "邮箱"
4. ssh-keygen -t rsa -C "邮箱"
5. cd ~/.ssh
6. cat id_rsa.pub
7. 进入git的管理界面，点击头像`setting`菜单，进入页面后选择`SSH and GPG keys`，选择`new ssh key`，拷贝密钥内容到编辑框中

配置多个ssh key
1. 重复执行 1 2 3 
2. ssh-keygen -t rsa -C "邮箱" -f ~/.ssh/gitlab_id-rsa
3. ssh-keygen -t rsa -C "邮箱" -f ~/.ssh/github_id-rsa
4. ssh -T java-wangrui@www.newstrength.cn

## 常用诊断命令
- git status 查看git状态，可以看见本地是否有未提交的内容
- git log 查看提交日志
- git reset --hard commitid(提交id) 回退commit命令后的版本
- git reset HEAD (回退add命令提交的内容)
- git reset HEAD filename (回退add命令提交的指定文件)
- git add filename (手动增加提交文件)
- git commit -m "add README" (提交并增加注释)
- git push -u origin master (推送到远程仓库)
