import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi')
        deployments = Deployment.objects.all()
        clipping = Detector.objects.get(code='amplitude')
        code = 'hihi'
        version = '0.1'
        detector = Detector.objects.get(code=code, version=version)
        for deployment in deployments:
            snippets = Snippet.objects.all()
            n_snippets = snippets.count()
            #Select only morning recordings
            morn_recordings = []
            for r in recording_datetime:
                recording_hour = r.hour
                if recordings_start < 11 and recordings_start > 06:
                    morn_recordings = morn_recordings.append(recording_file)
            #Select a random 5 snippets
            random_snippets = []
            five_snippets = []
            for recording_file in recording:
                random_snippets = list(snippets.order_by('?'))
                five_snippets = random_snippets[0:5]

            snippet_set = zip(random_snippets, ['Randomly selected 2%']*len(random_snippets)) +\
                zip(list(kiwi_snippets), ['Simple NIBK score higher than 25 ']*len(kiwi_snippets))
            random.shuffle(snippet_set)

            print deployment, n_snippets, len(already), len(kiwi_snippets), len(random_snippets)
            for snip, reason in snippet_set:
                AnalysisSet(analysis=analysis, snippet=snip, selection_method=reason).save()
