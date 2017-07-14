import random
import shutil
import argparse
from django.utils import timezone
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment, Site

def valid_datetime_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.strptime(arg_datetime_str, "%Y-%m-%d_%H:%M:%S")
    except ValueError:
        msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD_HH:mm:ss'!".format(arg_datetime_str)
        raise argparse.ArgumentTypeError(msg)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--site_code', type=str)
        parser.add_argument('-s', '--date_code',
                        dest='date_code',
                        type=valid_datetime_type,
                        default=None,
                        required=True,
                        help='date in format "YYYY-MM-DD_HH:mm:ss"')
        parser.add_argument('--minute_code',type=int)
    def handle(self, *args, **options):
        site_code = options['site_code']
        date_code = options['date_code']
        minute_code = options['minute_code']
        print(site_code,date_code,minute_code)
        snippets = Snippet.objects.all()
        snip = snippets.filter(recording__deployment__site__code=site_code,recording__datetime=date_code,offset=minute_code)
        analysis = Analysis.objects.get(code='tieke_id')
        print(snip)
	
        AnalysisSet(analysis=analysis, snippet=snip,selection_method=detector).save()
	print('snippet added to analysis')

        snippets = [x.snippet for x in AnalysisSet.objects.filter(analysis=analysis)]
        print(snippets)
	count = 0
        for snippet in snippets:
            count += 1
            print len(snippets), count
            snippet.save_sonogram()
            snippet.save_soundfile()
