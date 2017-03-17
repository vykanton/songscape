import os
import random
import shutil
import argparse
from django.core.management.base import BaseCommand, CommandError
from www.settings import TRAINING_PATH, MEDIA_ROOT, SNIPPET_DIR
from www.recordings.models import Identification, CallLabel, Score, Snippet, Tag

import wavy
import datetime
import csv


# Normalise the call time
def standardize(t):
    return min(60, max(float(t), 0))

class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--user',action="store",dest='user',default=False,
            help='Restrict to analysis by this user')
        parser.add_argument(
            '--analysis_id',action="store",dest='analysis',default=False,
            help='Restrict to this analysis')
        parser.add_argument(
            "--snippets",action="store",
            dest="get_snippets",default=False,
            help="Get the snippets")
        parser.add_argument(
            "--tags",action="store",dest="tag",
            default=False,help="Restric only to these tags")

    def handle(self, *args, **options):
        analysis = options.get('analysis', '')
        user = options.get('user', '')
        tags = options.get('tag', '')
        get_snippets=options.get('get_snippets', '')
        if tags == False:
            tags = Tag.objects.values_list('code', flat=True)
        identifications = Identification.objects.filter(analysisset__analysis__code=analysis)
        if user:
            identifications = identifications.filter(user__username=user)

        call_labels = CallLabel.objects.filter(analysisset__analysis__code=analysis)
        if user:
            call_labels = call_labels.filter(user__username=user)

        if options['get_snippets']:
            print "Creating snippets"
            #Save the audio calls of the species into the species folder
            buffer_label=0.1
            snippets_call=[]
            for call in call_labels:
                if call.tag.code in tags:
                    call_start=call.start_time-buffer_label
                    call_length=buffer_label+call.end_time-call_start
                    #audioname = call.analysisset.snippet.get_soundfile_name()
                    #Get filename based on the style used by victor
                    snippet=call.analysisset.snippet
                    recording_date= snippet.recording.datetime
                    rec_day=str("%02d" % (recording_date.day))
                    rec_month=str("%02d" % (recording_date.month))
                    rec_year=str(recording_date.year)[2:4]
                    rec_hour=str("%02d" % (recording_date.hour))
                    rec_min=str("%02d" % (recording_date.minute))
                    rec_sec=str("%02d" % (recording_date.second))
                    filename_date=rec_day+rec_month+rec_year+rec_hour+rec_min+rec_sec
                    filename_site=str(snippet.recording.deployment.site.code)
                    filename_recorder=str(snippet.recording.deployment.recorder.code)
                    filename_call=str(call.id)
                    filename_path=filename_date+filename_site+filename_recorder+"_"+filename_call+"_call"+".wav"
                    species=tags
                    path = os.path.join(TRAINING_PATH,species,filename_path)
                    call.analysisset.snippet.save_call(replace=False, path=path,call_start=call_start,call_length=call_length, max_framerate=24000)
                    #save the snippets that had a call from the species of interest
                    snippets_call.append(str(call.analysisset.id))

            #Save the snippets with the calls of the species into the species folder
            snippets_call=list(set(snippets_call))
            for snippet_id in snippets_call:
                snippet=identifications.get(analysisset__id=snippet_id).analysisset.snippet
                snippet_start=snippet.offset
                snippet_length=snippet.duration
                recording_date= snippet.recording.datetime
                rec_day=str("%02d" % (recording_date.day))
                rec_month=str("%02d" % (recording_date.month))
                rec_year=str(recording_date.year)[2:4]
                rec_hour=str("%02d" % (recording_date.hour))
                rec_min=str("%02d" % (recording_date.minute))
                rec_sec=str("%02d" % (recording_date.second))
                filename_date=rec_day+rec_month+rec_year+rec_hour+rec_min+rec_sec
                filename_site=str(snippet.recording.deployment.site.code)
                filename_recorder=str(snippet.recording.deployment.recorder.code)
                filename_minutes=str(int(snippet_start))
                filename_path=filename_date+filename_site+filename_recorder+"_"+filename_minutes+"_snippet"+".wav"
                species=tags
                path = os.path.join(TRAINING_PATH,species,filename_path)
                snippet.save_call(replace=False, path=path,call_start=snippet_start,call_length=snippet_length, max_framerate=24000)

            #Save the audio without species call into the non-species folder
            no_species_identifications=identifications.exclude(analysisset__id__in=snippets_call)
            for no_id in no_species_identifications:
                snippet=no_id.analysisset.snippet
                snippet_start=snippet.offset
                snippet_length=snippet.duration
                recording_date= snippet.recording.datetime
                rec_day=str("%02d" % (recording_date.day))
                rec_month=str("%02d" % (recording_date.month))
                rec_year=str(recording_date.year)[2:4]
                rec_hour=str("%02d" % (recording_date.hour))
                rec_min=str("%02d" % (recording_date.minute))
                rec_sec=str("%02d" % (recording_date.second))
                filename_date=rec_day+rec_month+rec_year+rec_hour+rec_min+rec_sec
                filename_site=str(snippet.recording.deployment.site.code)
                filename_recorder=str(snippet.recording.deployment.recorder.code)
                filename_minutes=str(int(snippet_start))
                filename_path=filename_date+filename_site+filename_recorder+"_"+filename_minutes+".wav"
                species="no_"+tags
                path = os.path.join(TRAINING_PATH,species,filename_path)
                snippet.save_call(replace=False, path=path,call_start=snippet_start,call_length=snippet_length, max_framerate=24000)

        #Save a csv file of the snippets scored and the detection
        #Save the labels submitted for each snippet
        filename='labels'+str(analysis[0:])+str(datetime.datetime.now().strftime('%y%m%d%H%M%S') )+'.csv'
        csv_path=os.path.join(TRAINING_PATH,filename)
        print(csv_path)
        csv_file = open(csv_path, 'w')
        writer = csv.writer(csv_file)
        writer.writerow(['snippet_id','username','call_id','call',"call_start","call_length",'high_frequency','low_frequency'])
        for call in call_labels:
            snippet=call.analysisset.snippet
            snippet_id=snippet.id
            username=call.user.username
            call_id=call.id
            species=call.tag.code
            call_start=call.start_time
            call_length=call.end_time-call.start_time
            high_frequency=call.high_frequency
            low_frequency=call.low_frequency
            writer.writerow([snippet_id,username,call_id,species,call_start,call_length,high_frequency,low_frequency])

        #Save the snippets analysed, site info and their scores
        filename='analysed'+str(analysis[0:])+str(datetime.datetime.now().strftime('%y%m%d%H%M%S') )+'.csv'
        csv_path=os.path.join(TRAINING_PATH,filename)
        print(csv_path)
        csv_file = open(csv_path, 'w')
        writer = csv.writer(csv_file)
        writer.writerow(['snippet_id','username','site','date','snippet_start','recorder','score','detector','version'])
        for identification in identifications:
            snippet=identification.analysisset.snippet
            snippet_id=snippet.id
            username=identification.user.username
            site=snippet.recording.deployment.site.code
            date= snippet.recording.datetime
            snippet_start=snippet.offset
            recorder=snippet.recording.deployment.recorder.code
            score=Score.objects.filter(snippet__id=snippet_id)
            for score_detector in score:
                detector=score_detector.detector.code
                version=score_detector.detector.version
                writer.writerow([snippet_id,username,site,date,snippet_start,recorder,score_detector,detector,version])
