import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi_id')
        clipping = Detector.objects.get(code='amplitude')
        snippets = Snippet.objects.all()
        code = 'simple-north-island-brown-kiwi'
        version = '0.1.2'
        detector = Detector.objects.get(code=code, version=version)
        already = snippets.filter(sets__analysis=analysis)
        score= Score.objects.all()

        #select snippets by kiwi score
        #max_score=max(score)
        max_score=40
        threshold_score=25
        category_length=5
        score_categories=range(threshold_score,max_score+category_length,category_length)
        #number of snippets per category
        snippet_category=3
        hihi_snippets = snippets.filter(scores__detector=detector,
            scores__score__gt=threshold_score).exclude(id__in=already)
        #Now select random snippets within each score category
        #hihi_snippets
        random_snippets = []
        for category in score_categories:
            #print(hihi_snippets.count(),"category",category,category+category_length)
            random_snippets = list(hihi_snippets.filter(scores__score__range=(category,category+category_length)))
            #Save the snippets selected
            for snip in random_snippets[:snippet_category]:
                #print(snip)
                AnalysisSet(analysis=analysis, snippet=snip,selection_method=detector).save()
