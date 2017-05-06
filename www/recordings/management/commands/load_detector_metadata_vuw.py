"""By writing the detector database entries inside a command we can ensure
the CNN objects are properly closed - we need to do this as we can't pass
a tensorflow object to a multiprocessing routine - it needs to be instatiated
in that process.

Here we temporarily load the detectors and add some meta data from them into
the database."""

from django.core.management.base import BaseCommand
from django import db
import time

from kokako.detectors.hihi import HihiCNN
from kokako.detectors.kakariki import KakarikiRNN
from kokako.detectors.tieke import TiekeRNN

from www.recordings.models import Score, Recording, Snippet, Detector
from www.settings import DETECTOR_CORES, HIHI_DETECTOR, KAKARIKI_DETECTOR, TIEKE_DETECTOR


class Command(BaseCommand):
    def handle(self, *args, **options):

        detectors=[HihiCNN(HIHI_DETECTOR, prediction_block_size=10, num_cores = DETECTOR_CORES),
            kakarikiRNN(KAKARIKI_DETECTOR, prediction_block_size=10, num_cores = DETECTOR_CORES),
            TiekeRNN(TIEKE_DETECTOR, prediction_block_size=10, num_cores = DETECTOR_CORES)]
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
