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
        #tags = CallLabel.objects.filter(tag__name="Hihi")
        tags = args[1:]
        print ("tags=",tags,"analysis=",analysis)
        identifications = Identification.objects.filter(analysisset__analysis__code=analysis)
        #print ("identifications=",identifications)
        if user:
            identifications = identifications.filter(user__username=user)

        call_labels = CallLabel.objects.filter(analysisset__analysis__code=analysis)
        #print ("call_lables=",call_labels)
        if user:
            call_labels = call_labels.filter(user__username=user)

        #FIrstly, ensure that all the snippets are present
        # if options['get_snippets']:
        #     print "Creating snippets"
        #     path = '/sample_calls'
        #     #scores = Scores.objects.filter(analysisset__snippet=snippet)
        #     #print scores
        #     for call in calls:
        #         if call.tag.code in tags:
        #             audioname = call.analysisset.snippet.get_soundfile_name()
        #             identification.analysisset.snippet.save_calls(replace=False, path=path, max_framerate=24000)
        buffer_label=0.1
        for call in call_labels:
            if call.tag.code in tags:
                hihi_snippets=Snippet.objects.filter(id=call.analysisset.snippet.id)
                #print(hihi_snippets)
                for snippet in hihi_snippets:
                    #snippet.save_call(replace=False,  max_framerate=24000)                    
                    call_start=round(call.start_time-buffer_label,1)
                    call_length=round(buffer_label+call.end_time-call_start,1)
                    audioname = call.analysisset.snippet.get_soundfile_name()
                    output_name= audioname
                    #TODO output_name= call_start,audioname
                    print(call_start,output_name)
                    outputpath = os.path.join(TRAINING_PATH, output_name)
                    inputpath = os.path.join(MEDIA_ROOT,SNIPPET_DIR,audioname)
                    print(inputpath,outputpath,call_start,call_length,24000)
                    wavy.slice_wave(inputpath,outputpath,call_start,call_length, max_framerate=24000)

                    # buffer_label=0.1
                    # call_start=round(call.start_time-buffer_label,1)
                    # call_length=round(buffer_label+call.end_time-call_start,1)
                    # audioname = call.analysisset.snippet.get_soundfile_name()
                    # output_name= audioname
                    # #TODO output_name= call_start,audioname
                    # print(call_start,audioname)
                    # outputpath = os.path.join(TRAINING_PATH, output_name)
                    # inputpath = os.path.join(MEDIA_ROOT,SNIPPET_DIR,audioname)
                    # print(inputpath,outputpath,call_start,call_length,24000)
                    # wav_file = open(inputpath, 'w')
                    # wavy.slice_wave(inputpath,outputpath,call_start,call_length, max_framerate=24000)
                    # wav_file.close()
                    # #identification.analysisset.snippet.save_call(replace=False, path=path, max_framerate=24000)


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
