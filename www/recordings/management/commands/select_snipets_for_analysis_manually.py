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
        snippets = Snippet.objects.all()
	analysis = Analysis.objects.get(code='tieke_id')
	analysis_already1=Analysis.objects.get(code='kakariki_id')
        analysis_already2=Analysis.objects.get(code='tieke_id')
        analysis_already3=Analysis.objects.get(code='hihi_id')
	already = snippets.filter(sets__analysis__in=[analysis_already1,analysis_already2,analysis_already3])
	call_snippet = list(snippets.filter(recording__deployment__site__code=site_code,recording__datetime=date_code,offset=minute_code).exclude(id__in=already))
        selected_snippet=[]
	selected_snippet=list(call_snippet)
	for snip in selected_snippet:
		AnalysisSet(analysis=analysis,snippet=snip,selection_method="tieke 1.0.0").save()
	print('snippet added to analysis')
