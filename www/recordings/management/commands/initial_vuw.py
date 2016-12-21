import csv
import os
import pytz

from datetime import datetime

from django.core.management.base import BaseCommand

from www.recordings.models import Organisation, Site, Recorder, Deployment, Tag, Analysis

from www.settings import ORG

DIR = 'www/fixtures'


class Command(BaseCommand):
    def handle(self, **options):
        organisation = csv.DictReader(open(os.path.join(DIR, 'Organisations.csv')))
        for row in organisation:
            o = Organisation(code=row['Code'], name=row['Name'])
            o.save()

        vicu_org = Organisation.objects.get(code='VICU')

        sites = csv.DictReader(open(os.path.join(DIR, 'Sites.csv')))
        for row in sites:
            if not row['Latitude'].strip():
                row['Latitude'] = None
            if not row['Longitude'].strip():
                row['Longitude'] = None

            o = Site(code=row['Code'], latitude=row['Latitude'], longitude=row['Longitude'], description=row['Comments'], organisation=vicu_org)
            o.save()

        recorders = csv.DictReader(open(os.path.join(DIR, 'Recorders.csv')))
        for row in recorders:
            o = Recorder(code=row['Code'], organisation=vicu_org)
            o.save()

        deployments = csv.DictReader(open(os.path.join(DIR, 'Deployments.csv')))
        for row in deployments:
            site = Site.objects.get(code=row['Site'])
            recorder = Recorder.objects.get(code=row['Recorder'].strip())
            start = row['Start']
            start = pytz.utc.localize(datetime.strptime(start,'%d/%m/%y'))
            end = row['End']
            end = pytz.utc.localize(datetime.strptime(end,'%d/%m/%y'))
            o = Deployment(site=site, recorder=recorder, start=start, end=end, comments='NA', owner=vicu_org, start_timezone='UTC')
            o.save()

        tags = csv.DictReader(open(os.path.join(DIR, 'Tags.csv')))
        for row in tags:
            o = Tag(code=row['Code'], name=row['Name'])
            o.save()

        analysis = csv.DictReader(open(os.path.join(DIR, 'Analysis.csv')))
        for row in analysis:
            o = Analysis(name=row['Name'], code=row['Code'], description=row['Description'], user_id=row['User_id'])
            o.save()
