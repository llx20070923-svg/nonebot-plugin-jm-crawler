import os
import shutil
from pathlib import Path

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.params import CommandArg
import jmcomic
from jmcomic import JmOption
import img2pdf

# 配置 PDF 存放目录
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

jm = on_command("jm", priority=5, block=True)

@jm.handle()
async def handle_jm(bot: Bot, event: GroupMessageEvent, args=CommandArg()):
    jm_id = args.extract_plain_text().strip()
    if not jm_id or not jm_id.isdigit():
        await jm.finish("请发送 /jm 数字编号")
    
    await jm.send(f"🔍 正在获取 JM {jm_id}，这可能需要一点时间，请稍候...")

    try:
        pdf_path = await download_jm_to_pdf(jm_id)
        
        if pdf_path and os.path.exists(pdf_path):
            size_kb = os.path.getsize(pdf_path) // 1024
            await jm.send(f"✅ PDF生成成功（{size_kb} KB），正在打包上传至群文件...")
            
            # 使用 API 上传群文件
            await bot.upload_group_file(
                group_id=event.group_id,
                file=str(os.path.abspath(pdf_path)),
                name=f"{jm_id}.pdf"
            )
            # 正常结束使用 send，避免触发 FinishedException 报错
            await jm.send("🚀 群文件上传完成！")
        else:
            await jm.send("❌ PDF 未生成或文件不存在。")
            
    except Exception as e:
        logger.exception("处理失败")
        # 只有遇到真正的代码异常时，才使用 finish 抛出错误并中断
        await jm.finish(f"❌ 发生错误: {str(e)[:50]}")

async def download_jm_to_pdf(jm_id: str) -> str:
    pdf_path = DOWNLOAD_DIR / f"{jm_id}.pdf"
    root_dir = os.path.abspath(".")
    
    # 核心战术：下载前，拍一个根目录的“快照”
    before_items = set(os.listdir(root_dir))
    
    # 读取配置并下载
    option = JmOption.default()
    logger.info(f"开始下载 JM {jm_id} (采用快照对比模式)")
    jmcomic.download_album(jm_id, option)
    
    # 下载后，再拍一个快照
    after_items = set(os.listdir(root_dir))
    
    # 找出多出来的东西
    new_items = after_items - before_items
    
    # 定位新增的文件夹
    album_dir = None
    for item in new_items:
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            album_dir = item_path
            break
            
    if not album_dir:
        raise Exception("未在根目录发现新增文件夹，可能下载失败")
        
    logger.info(f"成功捕捉到新文件夹: {album_dir}")
    
    # 遍历新文件夹抓取所有图片
    images = []
    for root, _, files in os.walk(album_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.png', '.webp', '.jpeg')):
                images.append(os.path.join(root, f))
                
    # 排序图片，防止乱序
    images.sort()
    
    if not images:
        shutil.rmtree(album_dir, ignore_errors=True)
        raise Exception("新增的文件夹内没有找到任何图片")
        
    # 生成 PDF 到 downloads 文件夹下
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(images))
        
    # 过河拆桥：生成完 PDF 后，直接删除原始文件夹
    try:
        shutil.rmtree(album_dir)
        logger.info(f"已清理原始图片文件夹，根目录保持干净")
    except Exception as e:
        logger.warning(f"清理文件夹失败: {e}")
        
    return str(pdf_path)