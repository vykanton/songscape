import os
import random
import shutil
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from www.settings import TRAINING_PATH, MEDIA_ROOT, SNIPPET_DIR
from www.recordings.models import Identification, CallLabel, Score, Snippet

import wavy


# Normalise the call time
def standardize(t):
    return min(60, max(float(t), 0))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--user',
            dest='user',
            help='restrict to analysis by this user'),
        make_option("--no-snippets",
            action="store_false",
            dest="get_snippets",
            default=True,
            help="Get the snippets"),
        )


    def handle(self, *args, **options):
        analysis = args[0]
        user = options.get('user', '')
        tags = args[1:]
        identifications = Identification.objects.filter(analysisset__analysis__code=analysis)
        if user:
            identifications = identifications.filter(user__username=user)

        call_labels = CallLabel.objects.filter(analysisset__analysis__code=analysis)
        if user:
            call_labels = call_labels.filter(user__username=user)

        #Save the calls of the species into the species folder
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
                filename_path=filename_date+filename_site+filename_recorder+"_"+filename_call+".wav"
                species=tags[0]
                path = os.path.join(TRAINING_PATH,species,filename_path)
                call.analysisset.snippet.save_call(replace=False, path=path,call_start=call_start,call_length=call_length, max_framerate=24000)
                #save the snippets that had a call from the species of interest
                snippets_call.append(str(call.analysisset.id))
        #Save the audio without species call into the non-species folder
        snippets_call=snippets_call[-1]
        no_species_identifications=identifications.exclude(analysisset__id=snippets_call)
        for snippet in no_species_identifications:
            species="no_"+tags[0]
            path=os.path.join(TRAINING_PATH, species)
            snippet.analysisset.snippet.save_soundfile(replace=False, path=path, max_framerate=24000)


        # #process the calls
        # calls = {}
        # for identification in identifications:
        #     snippet_score=Score.objects.filter(snippet__id=identification.analysisset.snippet.id).values_list('score',flat=True)[0]
        #     print("score1=",snippet_score)
        #     calls[identification.analysisset.snippet.get_soundfile_name()] = []
        #
        # for call in call_labels:
        #     if call.tag.code in tags:
        #         snippet_score=Score.objects.filter(snippet__id=call.analysisset.snippet.id).values_list('score',flat=True)[0]
        #         print("score2=",snippet_score)
        #         calls[call.analysisset.snippet.get_soundfile_name()].append((standardize(call.start_time),standardize(call.end_time),snippet_score))
        #         print calls
        #
        # # Now output the data
        # output = open('call-labels-%s.txt' % ('-'.join(tags)), 'w')
        # for soundfile, labels in calls.items():
        #     labels.sort()
        #     stack = []
        #     for i, label in enumerate(labels):
        #         if i == 0:
        #             stack.append(label[0])
        #             stack.append(label[1])
        #         if i > 0:
        #             if label[0] > stack[-1]:
        #                 stack.append(label[0])
        #                 stack.append(label[1])
        #                 stack.append(label[2])
        #             else:
        #                 stack.pop()
        #                 stack.append(label[1])
        #     if not sorted(stack) == stack:
        #         print stack
        #         raise ValueError, 'call times should be sorted'
        #     #print stack
        #     output.write(soundfile + ' ')
        #     output.write(' '.join([str(s) for s in stack]))
        #     output.write('\n')
        # output.close()
