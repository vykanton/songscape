import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment, Site

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('detector_code', type=str)
    def handle(self, *args, **options):
        detector_code = options['detector_code']
        detector = Detector.objects.get(code = detector_code)
        analysis = Analysis.objects.get(code=detector_code)
        snippets = Snippet.objects.all()        
        already = snippets.filter(sets__analysis=analysis)
        score= Score.objects.all()
        #Select only sites outside Zealandia
        outside_sites=Site.objects.exclude(code__startswith='000').values_list('code',flat=True)

        #select snippets by score
        #max_score=max(score)
        max_score=100
        threshold_score=60
        category_length=5
        score_categories=range(threshold_score,max_score+category_length,category_length)
        #number of snippets per category
        snippet_category=10
        scored_snippets = snippets.filter(scores__detector=detector,
            scores__score__gt=threshold_score,recording__deployment__site__code__in=outside_sites).exclude(id__in=already)

        #Now select random snippets within each score category
        #scored_snippets
        random_snippets = []
        for category in score_categories:
            #print(scored_snippets.count(),"category",category,category+category_length)
            random_snippets = list(scored_snippets.filter(scores__score__range=(category,category+category_length)))
            #Save the snippets selected
            for snip in random_snippets[:snippet_category]:
                #print(snip)
                AnalysisSet(analysis=analysis, snippet=snip,selection_method=detector).save()
