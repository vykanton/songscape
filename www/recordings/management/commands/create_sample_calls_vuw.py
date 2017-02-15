import os
import random
import shutil
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Identification, CallLabel, Tag

# Normalise the call time
def standardize(t):
    return min(60, max(float(t), 0))

class Command(BaseCommand):
    def handle(self,*args,**options):
        species="Hihi"
        call_labels = CallLabel.objects.filter(tag__name=species)
        print(dir(call_labels))
        calls={}
        # for tag in call_labels:
        #     calls[tag.analysisset.snippet.get_soundfile_name()].append((standardize(tag.start_time), standardize(tag.end_time)))
        # print('calls',calls)

        # path = settings.TRAINING_PATH
