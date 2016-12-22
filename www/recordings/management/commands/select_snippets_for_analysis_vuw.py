import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi_id')
        snippet = Snippet.objects.all()
        for snip in snippet:
            AnalysisSet(analysis=analysis, snippet=snip, selection_method='all').save()
