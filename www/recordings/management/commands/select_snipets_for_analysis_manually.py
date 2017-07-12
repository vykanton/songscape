import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment, Site


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

class Command(BaseCommand):
    def add_arguments(self, parser):
	parser.add_argument('site_code', type=str)
	parser.add_argument('-s', "--startdate", 
                    help="The date - format YYYY-MM-DD ", 
                    required=True, 
                    type=valid_date)
	parser.add_argument('minute_code',type=int)
    def handle(self, *args, **options):
        site_code = options['site_code']
	date_code = options['startdate']
	minute_code = options['minute_code']
	snip = snippets.filter(recording__deployment__site__code=site_code,recording__deployment__date=date_code,recording__deployment__site__minute=minute_code)
	analysis = Analysis.objects.get(code='tieke_id')
	print(snip)
        AnalysisSet(analysis=analysis, snippet=snip,selection_method=detector).save()
	print('snippet added to analysis')

        snippets = [x.snippet for x in AnalysisSet.objects.filter(analysis=analysis)]
        count = 0
        for snippet in snippets:
            count += 1
            print len(snippets), count
            snippet.save_sonogram()
            snippet.save_soundfile()
