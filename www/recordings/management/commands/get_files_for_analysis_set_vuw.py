import random

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score

class Command(BaseCommand):
    def add_arguments(self, parser):
	parser.add_argument('code_analysis',type=str)
    def handle(self, *args, **options):
        analysis_code=str(options['code_analysis'])+str('_id')
	analysis = Analysis.objects.get(code=analysis_code)
        snippets = [x.snippet for x in AnalysisSet.objects.filter(analysis=analysis)]
        count = 0
        for snippet in snippets:
            count += 1
            print len(snippets), count
            snippet.save_sonogram()
            snippet.save_soundfile()
