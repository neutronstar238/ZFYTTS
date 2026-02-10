#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动清理 outputs 目录下的旧文件
定期删除超过 1 天的音频文件
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cleanup.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 配置参数
OUTPUTS_DIR = "outputs"
MAX_AGE_DAYS = 1  # 文件保留天数
CHECK_INTERVAL = 3600  # 检查间隔（秒），默认 1 小时


def get_file_age_days(file_path):
    """获取文件的年龄（天数）"""
    file_mtime = os.path.getmtime(file_path)
    file_age = time.time() - file_mtime
    return file_age / (24 * 3600)


def cleanup_old_files(directory, max_age_days):
    """清理超过指定天数的文件"""
    if not os.path.exists(directory):
        logging.warning(f"目录不存在: {directory}")
        return
    
    deleted_count = 0
    deleted_size = 0
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # 跳过目录
            if os.path.isdir(file_path):
                continue
            
            # 检查文件年龄
            try:
                age_days = get_file_age_days(file_path)
                
                if age_days > max_age_days:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    deleted_size += file_size
                    logging.info(f"删除文件: {filename} (年龄: {age_days:.1f} 天, 大小: {file_size/1024:.1f} KB)")
            
            except Exception as e:
                logging.error(f"处理文件 {filename} 时出错: {e}")
        
        if deleted_count > 0:
            logging.info(f"清理完成: 删除 {deleted_count} 个文件, 释放 {deleted_size/1024/1024:.2f} MB 空间")
        else:
            logging.info("没有需要清理的文件")
    
    except Exception as e:
        logging.error(f"清理过程出错: {e}")


def run_cleanup_service():
    """运行清理服务（持续运行）"""
    logging.info("=" * 60)
    logging.info("自动清理服务已启动")
    logging.info(f"监控目录: {OUTPUTS_DIR}")
    logging.info(f"文件保留时间: {MAX_AGE_DAYS} 天")
    logging.info(f"检查间隔: {CHECK_INTERVAL} 秒 ({CHECK_INTERVAL/3600:.1f} 小时)")
    logging.info("=" * 60)
    
    while True:
        try:
            logging.info("开始清理检查...")
            cleanup_old_files(OUTPUTS_DIR, MAX_AGE_DAYS)
            
            next_check = datetime.now() + timedelta(seconds=CHECK_INTERVAL)
            logging.info(f"下次检查时间: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
            
            time.sleep(CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logging.info("收到停止信号，正在退出...")
            break
        
        except Exception as e:
            logging.error(f"服务运行出错: {e}")
            time.sleep(60)  # 出错后等待 1 分钟再继续


def run_once():
    """运行一次清理（用于手动清理或定时任务）"""
    logging.info("执行单次清理...")
    cleanup_old_files(OUTPUTS_DIR, MAX_AGE_DAYS)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="自动清理 outputs 目录下的旧文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 持续运行清理服务
  python cleanup_outputs.py --service
  
  # 执行一次清理
  python cleanup_outputs.py --once
  
  # 自定义保留天数
  python cleanup_outputs.py --service --days 2
  
  # 自定义检查间隔（秒）
  python cleanup_outputs.py --service --interval 7200
        """
    )
    
    parser.add_argument(
        "--service",
        action="store_true",
        help="持续运行清理服务"
    )
    
    parser.add_argument(
        "--once",
        action="store_true",
        help="执行一次清理后退出"
    )
    
    parser.add_argument(
        "--days",
        type=float,
        default=MAX_AGE_DAYS,
        help=f"文件保留天数（默认: {MAX_AGE_DAYS}）"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=CHECK_INTERVAL,
        help=f"检查间隔（秒）（默认: {CHECK_INTERVAL}）"
    )
    
    parser.add_argument(
        "--dir",
        type=str,
        default=OUTPUTS_DIR,
        help=f"要清理的目录（默认: {OUTPUTS_DIR}）"
    )
    
    args = parser.parse_args()
    
    # 更新配置
    MAX_AGE_DAYS = args.days
    CHECK_INTERVAL = args.interval
    OUTPUTS_DIR = args.dir
    
    # 确保输出目录存在
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    
    if args.service:
        run_cleanup_service()
    elif args.once:
        run_once()
    else:
        # 默认运行服务
        run_cleanup_service()
