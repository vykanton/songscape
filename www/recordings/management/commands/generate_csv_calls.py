import os
import shutil
from www.settings import TRAINING_PATH
from django.core.management.base import BaseCommand, CommandError
from www.recordings.models import Identification, CallLabel, Score, Snippet, Tag

import datetime
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        call_labels = CallLabel.objects.all()
        csv_filename='labels'+str(datetime.datetime.now().strftime('%y%m%d%H%M%S') )+'.csv'
        csv_path = os.path.join(TRAINING_PATH,csv_filename)
        print("csv_path",csv_path)
        csv_file = open(csv_path, 'w')
        print("csv_created")
        writer = csv.writer(csv_file)
        writer.writerow(['filename','snippet_start','snippet_end','call',"call_start","call_end",'high_frequency','low_frequency',
                        'score_tieke','score_hihi','score_kakariki'])
        for call in call_labels:
            snippet_call = call.analysisset.snippet
            snippet_id = snippet_call.id
            filename = str(snippet_call.recording.path)[44:70]
            call_id = call.id
            species = call.tag.code
            snippet_start = snippet_call.offset
            snippet_end = snippet_call.offset+60
            call_start = call.start_time
            call_end = call.end_time            
            high_frequency = call.high_frequency
            low_frequency = call.low_frequency
            score_tieke = Score.objects.filter(snippet__id=snippet_id,detector__code='tieke')
            score_hihi = Score.objects.filter(snippet__id=snippet_id,detector__code='hihi')
            score_kakariki = Score.objects.filter(snippet__id=snippet_id,detector__code='kakariki')
            writer.writerow([filename,snippet_start,snippet_end,species,call_start,call_end,high_frequency,low_frequency,
                            score_tieke,score_hihi,score_kakariki])
        
        print('file cereated')                                             
