#Stage 2 Update (Python 3)
import datetime
import json
import urllib.parse
import urllib.request
from builtins import object

import http.client
from future import standard_library

from scraper.models import Scraper
from scrapy.utils.project import get_project_settings

standard_library.install_aliases()
settings = get_project_settings()

class TaskUtils(object):
    
    conf = {
        "MAX_SPIDER_RUNS_PER_TASK": 10,
        "MAX_CHECKER_RUNS_PER_TASK": 25,
    }
    
    def _run_spider(self, **kwargs):
        param_dict = {
            'project': 'default',
            'spider': kwargs['spider'],
            'id': kwargs['id'],
            'run_type': kwargs['run_type'],
            'do_action': kwargs['do_action']
        }
        params = urllib.parse.urlencode(param_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection("localhost:6800")
        conn.request("POST", "/schedule.json", params, headers)
        conn.getresponse()
    
    
    def _pending_jobs(self, spider):
        # Ommit scheduling new jobs if there are still pending jobs for same spider
        resp = urllib.request.urlopen('http://localhost:6800/listjobs.json?project=default')
        data = json.loads(resp.read().decode('utf-8'))
        if 'pending' in data:
            for item in data['pending']:
                if item['spider'] == spider:
                    return True
        return False
    
    
    def run_spiders(self, ref_obj_class, scraper_field_name, runtime_field_name, spider_name, *args, **kwargs):
        filter_kwargs = {
            scraper_field_name + '__status': 'A',
            runtime_field_name + '__next_action_time__lt': datetime.datetime.now(),
        }
        for key in kwargs:
            filter_kwargs[key] = kwargs[key]
        
        max = settings.get('DSCRAPER_MAX_SPIDER_RUNS_PER_TASK', self.conf['MAX_SPIDER_RUNS_PER_TASK'])
        ref_obj_list = ref_obj_class.objects.filter(*args, **filter_kwargs).order_by(runtime_field_name + '__next_action_time')[:max]
        if not self._pending_jobs(spider_name):
            for ref_object in ref_obj_list:
                self._run_spider(id=ref_object.pk, spider=spider_name, run_type='TASK', do_action='yes')
        

    def run_checkers(self, ref_obj_class, scraper_field_path, runtime_field_name, checker_name, *args, **kwargs):
        filter_kwargs = {
            scraper_field_path + '__status': 'A',
            runtime_field_name + '__next_action_time__lt': datetime.datetime.now(),
        }
        for key in kwargs:
            filter_kwargs[key] = kwargs[key]
        
        max = settings.get('DSCRAPER_MAX_CHECKER_RUNS_PER_TASK', self.conf['MAX_CHECKER_RUNS_PER_TASK'])
        ref_obj_list = ref_obj_class.objects.filter(*args, **filter_kwargs).order_by(runtime_field_name + '__next_action_time')[:max]
        if not self._pending_jobs(checker_name):
            for ref_object in ref_obj_list:
                self._run_spider(id=ref_object.pk, spider=checker_name, run_type='TASK', do_action='yes')
