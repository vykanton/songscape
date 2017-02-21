import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment, Site

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi_id')
        snippets = Snippet.objects.all()
        code = 'hihi'
        version = '0.0.1'
        detector = Detector.objects.get(code=code, version=version)
        already = snippets.filter(sets__analysis=analysis)
        score= Score.objects.all()
        #Select only sites outside Zealandia
        outside_sites=Site.objects.exclude(code__startswith='000').values_list('code',flat=True)

        #select snippets by hihi score
        #max_score=max(score)
        max_score=20
        threshold_score=1
        category_length=3
        score_categories=range(threshold_score,max_score+category_length,category_length)
        #number of snippets per category
        snippet_category=2
        hihi_snippets = snippets.filter(scores__detector=detector,
            scores__score__gt=threshold_score,recording__deployment__site__code__in=outside_sites).exclude(id__in=already)

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
