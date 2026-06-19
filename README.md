# 📖 NoneBot-Plugin-JM-Crawler

基于 NoneBot2 框架的轻量级、全自动 JM 漫画抓取与 PDF 打包群聊插件。

本插件致力于解决群聊场景下的本子分享痛点。只需一行指令，即可在机器人后端全自动完成**“代理下载 -> 目录快照比对 -> 碎图提取 -> PDF 无损合并 -> 隔离区销毁 -> 群文件 API 直传”**的完整闭环。

---

## ✨ 核心特性

* 🚀 **极简指令触发**：原生适配 OneBot V11 协议，通过简单的 QQ 群指令 `/jm [ID]` 即可唤起自动化工作流。
* 🛡️ **沙盒快照隔离技术 (Snapshot Isolation)**：针对原生下载库乱建目录的痛点，创新性采用“下载前后根目录快照求差集”的算法，100% 精准捕捉目标文件夹。**用完即焚**，绝不污染宿主机服务器目录。
* 📄 **PDF 无损合并封装**：自动深度遍历目标文件夹，过滤提取所有图片（jpg/png/webp 等），按正确的字母顺序无损渲染并合成为单一高清 PDF 文件。
* 📤 **原生 API 直传**：彻底抛弃极易因路径格式、权限报错的传统 `[CQ:file]` 本地文件发送模式，采用更底层的 `upload_group_file` API，大文件上传更加稳定可靠。

---

## 📦 环境与依赖

运行本插件，你需要具备以下基础环境：
* Python 3.8+
* [NoneBot2](https://github.com/nonebot/nonebot2) >= 2.0.0
* nonebot-adapter-onebot >= 2.0.0

安装核心依赖库：
```bash
pip install nonebot2 nonebot-adapter-onebot jmcomic img2pdf

## 🙏 鸣谢 (Acknowledgments)

本项目核心的底层抓取与 API 交互逻辑强依赖于优秀的开源项目 [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python)。
特此向原作者 [hect0x7](https://github.com/hect0x7) 及所有代码贡献者表示诚挚的感谢！