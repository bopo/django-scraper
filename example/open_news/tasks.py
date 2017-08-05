from celery.task import task
from scraper.utils.task_utils import TaskUtils
from open_news.models import Article, NewsWebsite


@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(NewsWebsite, 'scraper', 'scraper_runtime', 'article_spider')
    
@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Article, 'news_website__scraper', 'checker_runtime', 'article_checker')
