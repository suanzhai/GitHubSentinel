from datetime import date

import requests
import os  # 导入os模块用于文件和目录操作
from logger import LOG  # 导入日志模块
from bs4 import BeautifulSoup

class HackerNewsClient:
    def __init__(self):
        pass

    def fetch_news(self):
        """发送HTTP请求并获取页面内容"""
        top_stories = []
        try:
            response = requests.get("https://news.ycombinator.com/")
            response.raise_for_status()  # 请求失败时抛出异常
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select(".titleline > a")

            for link in links[:10]:
                title = link.get_text()
                url = link.get("href")

                content = ''
                try:
                    content_response = requests.get(url)
                    content_response.raise_for_status()
                    content_soup = BeautifulSoup(content_response.text, "html.parser")
                    content = content_soup.get_text()
                except Exception as e:
                    LOG.error(e)

                top_stories.append({"title": title, "url": url, "content": content.replace('\n',  '')})
        except Exception as e:
            LOG.error(e)

        return top_stories

    def export_hacker_news(self):
        top_stories = self.fetch_news()
        news_dir = os.path.join('hacker_news')  # 构建存储路径
        os.makedirs(news_dir, exist_ok=True)  # 确保目录存在
        today = date.today()  # 获取当前日期
        file_path = os.path.join(news_dir, f'{today}.md')  # 构建文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Hacker News for ({today})\n\n")
            file.write("| Title ｜ Content ｜\n")
            file.write("| --- | :------------ |\n")
            for story in top_stories:  # 写入今天关闭的问题
                file.write(f"| {story['title']} | {story['content']} |\n")

        LOG.info(f"[Hacker News 最新热门科技生成： {file_path}")  # 记录日志
        return file_path