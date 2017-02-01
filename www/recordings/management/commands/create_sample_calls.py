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

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

BASE_PATH = '/sample_calls/hihi'

#code to create sample calls of hihi

#code to copy snippets that not contain hihi calls
