"""A detector for Hihi. This is just a specific version of
TFGraphDetector with some hardcoded parameters to point to a pre-trained
Hihi detector."""
import os
import sys
import time

from django.core.management.base import BaseCommand
from django import db

from kokako.score import Audio
from kokako.detectors.hihi import HihiCNN
from kokako.detectors.kakariki import KakarikiRNN
from kokako.detectors.tieke import TiekeRNN
from wavy import get_audio
from wave import Error as WaveError

from www.recordings.models import Score, Recording, Snippet, Detector
from www.settings import DETECTOR_CORES, HIHI_DETECTOR, KAKARIKI_DETECTOR, TIEKE_DETECTOR

import multiprocessing as mp
import numpy as np

def worker(cpu_recording_ids, detector_id):
    '''
    Score snippets multiprocessing worker.
    It is ok to make database connections from inside the worker
    as long as non are passed between workers
    or from spawning processes
    '''

    #Check that this CPU actually has recordigns to processes
    if len(cpu_recording_ids>0):
        
        # create new database connections for this worker.
        recordings = Recording.objects.filter(pk__in = cpu_recording_ids)
        detector_model = Detector.objects.get(pk = detector_id)

        # Reinitialise detectors for multiprocessing - TODO this could be done in a cleaner way.
        if detector_model.code == 'hihi':
            detector = HihiCNN(HIHI_DETECTOR, prediction_block_size=10, num_cores = DETECTOR_CORES)
        elif detector_model.code == 'kakariki':
            detector = KakarikiRNN(KAKARIKI_DETECTOR, num_cores = DETECTOR_CORES)
        elif detector_model.code == 'tieke':
            detector = TiekeRNN(TIEKE_DETECTOR, num_cores = DETECTOR_CORES)
        else:
            raise ValueError('Unknown detector code! - Make sure new detectors are added to code here!')
            detector = None


        now = time.time()

        for recording in recordings:
	    snippets = Snippet.objects.filter(recording=recording).order_by('offset')
            if len(snippets):
                for snippet in snippets:
                    try:
                        audio = Audio(*get_audio(recording.path, snippet.offset, snippet.duration))
                        count = 0
                        score = detector.score(audio)
                        if not count:
                            print '%s %0.1f %0.1f' % (snippet, time.time() - now, score)
                            now = time.time()
                        try:
                            s = Score.objects.get(detector=detector_model, snippet=snippet)
                            s.delete()
                        except Score.DoesNotExist:
                            pass
                        s = Score(detector=detector_model, snippet=snippet,
                            score=score)
                        s.save()
                        count += 1
                    except KeyboardInterrupt:
                        raise
                    except WaveError:
                        print recording.path, 'scoring failed because of a WAV error'
                        break
                    except:
                        print detector, snippet, 'Scoring failed', sys.exc_info()[0]
            else:
                raise ValueError("Can't find the snippets for the recording %s" % (recording))
    else:
        #no recordings to process
        pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('detector_code', type=str)
    def handle(self, *args, **options):
        detector_code = options['detector_code']
        detector = Detector.objects.get(code = detector_code)
        recordings = Recording.objects.all().order_by('?')
        recordings = recordings.filter(datetime__hour__range=(05, 10))
        print ('Warning! only using morning snippets!') #FIXME more elegant way for the user to select this

        #prep for multiprocessing - don't pass database objects into the multiprocessing pool.
        recording_ids = [recording.id for recording in recordings]
        detector_id = detector.id

        l = recording_ids
        cpus = mp.cpu_count()

        #Divide recordings as evenly as possible betwen cpus. A nested array, each subarray is the recording ids for a cpu.
        recordings_per_cpu = np.array_split(recording_ids,cpus) #If there are more cpus, than recordings this will just create an empty array for that cpu

        # close db all db connections before going multicore
        db.connections.close_all()

        jobs=[]
        for cpu in range(cpus):
            p = mp.Process(target=worker, args=(recordings_per_cpu[cpu], detector_id))
            jobs.append(p)
            p.start()

        #wait for all jobs to end
        for p in jobs:
            p.join()
        print ('mutiprocessing done')
        # worker(recordings_per_cpu[0], detector_id, detectors)
