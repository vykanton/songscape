import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi_id')
        deployments = Deployment.objects.all()
        clipping = Detector.objects.get(code='amplitude')
        snippet = Snippet.objects.all()
        code = 'simple-north-island-brown-kiwi'
        version = '0.1.2'
        detector = Detector.objects.get(code=code, version=version)
        for deployment in deployments:
            snippets = Snippet.objects.\
                filter(recording__deployment=deployment)
            already = snippets.filter(sets__analysis=analysis)

            #select by kiwi score
            hihi_snippets = snippets.filter(scores__detector=detector,
                scores__score__gt=25).exclude(id__in=already)

            print deployment, len(already), len(hihi_snippets)

            for snip in hihi_snippets:
                AnalysisSet(analysis=analysis, snippet=snip,selection_method=detector).save()
