import csv, os
import hashlib

from django.core.management.base import BaseCommand
from www.recordings.models import Snippet, Recording
from www.settings import SNIP_SUBSAMPLE_STEP, SNIPPETS_PATH

import wavy

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_recordings = Recording.objects.all()
        #Select only morning recordings
        morn_recordings = all_recordings.filter(datetime__hour__range=(05, 10))
        for recording in morn_recordings:
            matching_snippets = Snippet.objects.filter(recording=recording)
            maching_snippets_subsample = matching_snippets[0::SNIP_SUBSAMPLE_STEP] # last number in bracket is subsample step.  ie [0:4] is every 4th
            for snippet in maching_snippets_subsample:
                try:
                    wavy.slice_wave(recording.path, os.path.join(SNIPPETS_PATH, snippet.get_soundfile_name()), snippet.offset, snippet.duration, 12000)
                except Recording.DoesNotExist:
                    print "Can't find the recording on row %s at path %s" % (i, path)
                except:
                    print 'Something went wrong on row %s with recording %s' % (i, path)
                    raise
