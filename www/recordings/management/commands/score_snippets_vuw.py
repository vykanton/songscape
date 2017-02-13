"""A detector for Hihi. This is just a specific version of
TFGraphDetector with some hardcoded parameters to point to a pre-trained
Hihi detector."""
import os
import sys
import time

from django.core.management.base import BaseCommand

from kokako.score import Audio
from kokako.detectors.hihi import HihiCNN
from wavy import get_audio
from wave import Error as WaveError

from www.recordings.models import Score, Recording, Snippet, Detector

class Command(BaseCommand):
    def handle(self, *args, **options):
        detectors=[HihiCNN()]
        db_detectors = []
        now = time.time()
        for detector in detectors:
            try:
                db_detectors.append(Detector.objects.get(code=detector.code, version=detector.version))
            except Detector.DoesNotExist:
                db_detectors.append(Detector(code=detector.code,
                    version=detector.version,
                    description=detector.description))
                db_detectors[-1].save()
        detectors = zip(detectors, db_detectors)
        hihi_detector = Detector.objects.get(code = 'hihi')
        recordings = Recording.objects.all().order_by('?')
        for recording in recordings:
            snippets = Snippet.objects.filter(recording=recording).exclude(scores__detector=hihi_detector).order_by('offset')
            if len(snippets):
                for snippet in snippets:
                    try:
                        audio = Audio(*get_audio(recording.path, snippet.offset, snippet.duration))
                        count = 0
                        for detector, db_detector in detectors:
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
