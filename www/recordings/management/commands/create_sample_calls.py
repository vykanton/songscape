from datetime import datetime
import os, sys
import shutil
from time import time, strptime, strftime, mktime
import re
import wave
import hashlib
from contextlib import closing
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from www.recordings.models import CallLabel,Snippet, Analysis, AnalysisSet, Detector, Score, Deployment, Identification

HIHI_PATH = '/sample_calls/hihi'
NONHIHI_PATH = '/sample_calls/nonhihi'
class Command(BaseCommand):
    def handle(self, *args, **options):
        #code to create sample calls of hihi
        hihitag= Tag.objects.filter(name='Hihi').values('id')
        allanalysisset=AnalysisSet.objects.all()
        for analysissetid in allanalysisset:
            snippet_offset= Snippet.objects.filter(id=snippet_id).values(offset)
            snippet_recording= Snippet.objects.filter(id=snippet_id).values(recording_id)
            recording_path=Recording.objects.filter(id=snippet_recording).values(path)
            hihicalls = CallLabel.objects.filter(analysisset_id=analysissetid,tag_id=hihitag)
            snippet_length=Snippet.objects.filter(id=snippet_id).values(duration)
            non_hihicalls=Identification.objects.filter(analysisset_id!=hihicalls)
            for call in hihicalls:
                call_start=snippet_offset+start_time
                call_length=end_time-start_time
                try:
                    wavy.slice_wave(recording.path, os.path.join(HIHI_PATH, snippet.get_soundfile_name()), call_start, call_length, 12000)
                except Recording.DoesNotExist:
                    print "Can't find the recording on row %s at path %s" % (i, path)
                except:
                    print 'Something went wrong on row %s with recording %s' % (i, path)
                    raise
            #Code to create non_hihi calls
            for call in non_hihicalls:
                try:
                    wavy.slice_wave(recording.path, os.path.join(NONHIHI_PATH, snippet.get_soundfile_name()), snippet_start, snippet_length, 12000)
                except Recording.DoesNotExist:
                    print "Can't find the recording on row %s at path %s" % (i, path)
                except:
                    print 'Something went wrong on row %s with recording %s' % (i, path)
                    raise
