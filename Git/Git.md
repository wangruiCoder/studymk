# Git学习笔记
---
## 克隆项目
`git clone https://github.com/wangruiCoder/studymk.git`

## git ssh key
需要本地已经安装了git
电脑桌面右键选择git bash here
- cd ~/.ssh
- git config --global user.name "***"
- git config --global user.email  "邮箱"
- ssh-keygen -t rsa -C "邮箱"
- cd ~/.ssh
- cat id_rsa.pub
- 进入git的管理界面，点击头像`setting`菜单，进入页面后选择`SSH and GPG keys`，选择`new ssh key`，拷贝密钥内容到编辑框中
