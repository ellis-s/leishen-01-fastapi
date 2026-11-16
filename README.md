# 介绍

这是看过 fastapi 模块后的一个自己手动练习的项目，主要包含下面内容

1. 搭建一个常见的项目工程化结构
2. 创建一个 user 模块
3. 包含 middleware
4. 包含 异常处理
5. 包含 依赖注入
6. 需要有连接数据库，支持常规 CURD 操作
7. 做成一个 Docker 镜像，支持通过容器部署

# 项目

创建项目

```bash
cd leishen-01-fastapi
uv init .
```

创建环境

```bash
# 查看已有的python解释器
uv python list

# 选择Python解释器
uv python pin 3.12

# 运行同步命令
uv sync
```

安装 fastapi

```bash
uv add "fastapi[standard]"
```