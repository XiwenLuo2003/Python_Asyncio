# References_Project 参考项目

本文件夹存放学习用的开源项目，**只在本地使用**。项目源码已在 `.gitignore` 中排除，远程仓库只上传本 README。

## 项目列表

| 编号 | 项目 | 仓库地址 | 学习方向 | 对应学习目录 |
|---|---|---|---|---|
| 01 | 500lines | https://github.com/aosabook/500lines | asyncio 原理：重点看 `crawler/`（Guido 写的异步爬虫） | `01_500lines_crawler/` |
| 02 | aiohttp-demos | https://github.com/aio-libs/aiohttp-demos | asyncio 实战：基于 aiohttp 的完整 Web 示例项目 | `02_aiohttp_demos/` |
| 03 | objgraph | https://github.com/mgedmin/objgraph | 垃圾回收：对象引用图、循环引用、内存泄漏排查 | `03_objgraph/` |
| 04 | memray | https://github.com/bloomberg/memray | 内存分析：内存分配追踪、火焰图 | `04_memray/` |

## 换电脑后重新获取

远程仓库里没有这四个项目的源码，在本文件夹下执行：

```bash
git clone --depth 1 https://github.com/aosabook/500lines.git
git clone --depth 1 https://github.com/aio-libs/aiohttp-demos.git
git clone --depth 1 https://github.com/mgedmin/objgraph.git
git clone --depth 1 https://github.com/bloomberg/memray.git
```

`--depth 1` 只拉取最新一次提交，体积更小；需要查看完整历史时去掉该参数。

## 更新参考项目

```bash
cd <项目文件夹>
git pull
```

## 学习建议

1. **01 500lines/crawler**：先读 `crawler/crawler.md` 这篇文章，再对照代码理解事件循环、协程、`Future`、`Queue`。
2. **02 aiohttp-demos**：挑 `chat`、`polls` 等示例运行起来，看真实项目里怎样组织异步代码。
3. **03 objgraph**：用 `show_growth()`、`show_backrefs()` 找出循环引用，配合 `gc` 模块理解引用计数和分代回收。
4. **04 memray**：用 `memray run` + `memray flamegraph` 分析自己写的异步程序的内存分配。

> 注：memray 仅支持 Linux / macOS，Windows 上需要在 WSL 中运行。
