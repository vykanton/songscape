import os
import random
import shutil
import wavy
import wave
import hashlib
import csv

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Identification, CallLabel, Tag, Recording,Score


recordingpath = settings.TRAINING_PATH
species="Hihi"

class Command(BaseCommand):
    def handle(self,*args,**options):
        #Extract the calls
        call_labels = CallLabel.objects.filter(tag__name=species)
        buffer_label=0.2
        for call in call_labels:
            start_time=call.start_time-buffer_label
            offset=call.analysisset.snippet.offset
            call_start=offset+start_time
            call_length=buffer_label+call.end_time-start_time
            audiopath=call.analysisset.snippet.recording.path
            audio_filename=audiopath[-26:-4]
            rounded_call_start=round(call_start,2)
            filename=str(audio_filename)+"_"+str(rounded_call_start)+species
            outputpath=os.path.join(recordingpath,species,filename)
            #score=call.analysisset.analysis.__dict__.keys()
            #print("extracting",species,"calls")
            calls.append([species,detector,score,site,date_time,call_length])
            try:
                print(audiopath,filename,outputpath, call_start, call_length, 24000)
                #wavy.slice_wave(audiopath,trial1, call_start, call_length, 24000)
            except:
                print 'Something went wrong with snippet %s label %s'% (snippet_id, call)
                raise
        #Write a .csv with calls extracted
        # detector=call.analysisset.selection_method
        # date_time=call.analysisset.snippet.recording.datetime
        # site=call.analysisset.snippet.recording.deployment.site
        # snippet_id=call.analysisset.snippet.id
        # score=Score.objects.filter(snippet__id=snippet_id)
        # calls=[]
        # print(calls)
        #csv.writer(calls)


        # for call in hihicalls:
        #     call_start=snippet_offset+call.start_time
        #     call_length=(snippet_offset+tag.end_time)-start_time
        #     wavy.slice_wave(audiopath, os.path.join(recordingpath, snippet.get_soundfile_name(),species), call_start, call_length, 12000)
        #
#Code to create non_hihi calls
# for call in non_hihicalls:
#     try:
#         wavy.slice_wave(recording.path, os.path.join(NONHIHI_PATH, snippet.get_soundfile_name()), snippet_start, snippet_length, 12000)
#     except Recording.DoesNotExist:
#         print "Can't find the recording on row %s at path %s" % (i, path)
#     except:
#         print 'Something went wrong on row %s with recording %s' % (i, path)
#         raise
