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
from wavy import get_audio
from wave import Error as WaveError

from www.recordings.models import Score, Recording, Snippet, Detector
from www.settings import HIHI_DETECTOR

import multiprocessing as mp

def worker(cpu_recording_ids, hihi_detector_id, detectors):
    '''
    Score snippets multiprocessing worker.
    It is ok to make database connections from inside the worker
    as long as non are passed between workers
    or from spawning processes
    '''

    # create new database connections for this worker.
    recordings = Recording.objects.filter(pk__in = cpu_recording_ids)
    hihi_detector = Detector.objects.get(pk = hihi_detector_id)

    now = time.time()

    for recording in recordings:
        snippets = Snippet.objects.filter(recording=recording).exclude(scores__detector=hihi_detector).order_by('offset')
        if len(snippets):
            for snippet in snippets:
                try:
                    audio = Audio(*get_audio(recording.path, snippet.offset, snippet.duration))
                    count = 0
                    for detector in detectors:
                        score = detector.score(audio)
                        if not count:
                            print '%s %0.1f %0.1f' % (snippet, time.time() - now, score)
                            now = time.time()
                        try:
                            s = Score.objects.get(detector=hihi_detector, snippet=snippet)
                            s.delete()
                        except Score.DoesNotExist:
                            pass
                        s = Score(detector=hihi_detector, snippet=snippet,
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

class Command(BaseCommand):
    def handle(self, *args, **options):
        detectors=[HihiCNN(HIHI_DETECTOR)]
        db_detectors = []
        now = time.time()
        for d in detectors:
            try:
                db_detectors.append(Detector.objects.get(code=d.code, version=d.version))
            except Detector.DoesNotExist:
                db_detectors.append(Detector(code=d.code,
                    version=d.version,
                    description=d.description))
                db_detectors[-1].save()
        #detectors = zip(detectors, db_detectors)
        hihi_detector = Detector.objects.get(code = 'hihi')
        recordings = Recording.objects.all().order_by('?')

        #prep for multiprocessing - don't pass database objects into the multiprocessing pool.
        recording_ids = [recording.id for recording in recordings]
        hihi_detector_id = hihi_detector.id

        l = recording_ids
        cpus = mp.cpu_count()
        n = cpus-1 # as we want the remainder of jobs in the last CPU. FIXME cases where it divides evenly

        #Divide recordings as evenly as possible betwen cpus. A nested list, each sublist is the recording ids for a cpu.
        recordings_per_cpu = [l[i:i + n] for i in xrange(0, len(l), n)]

        #test worker code
        worker(recordings_per_cpu[0], hihi_detector_id, detectors)
