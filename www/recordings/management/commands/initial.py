import csv
import os

from datetime import datetime

from django.core.management.base import BaseCommand

from www.recordings.models import Organisation, Site, Recorder, Deployment

from www.settings import ORG

DIR = 'www/fixtures'


class Command(BaseCommand):
    def handle(self, **options):
        organisation = csv.DictReader(open(os.path.join(DIR, 'Organisations.csv')))
        for row in organisation:
            o = Organisation(code=row['Code'], name=row['Name'])
            o.save()

        if ORG == "vuw":
            vicu_org = Organisation.objects.get(code='VICU')
        else:
            rfpt_org = Organisation.objects.get(code='RFPT')

        sites = csv.DictReader(open(os.path.join(DIR, 'Sites.csv')))
        for row in sites:
            if not row['Latitude'].strip():
                row['Latitude'] = None
            if not row['Longitude'].strip():
                row['Longitude'] = None

            if ORG == "vuw":
                o = Site(code=row['Code'], latitude=row['Latitude'], longitude=row['Longitude'], description=row['Comments'], organisation=vicu_org)
                o.save()
            else:
                o = Site(code=row['Code'], latitude=row['Latitude'], longitude=row['Longitude'], description=row['Comments'], organisation=rfpt_org)
                o.save()

        recorders = csv.DictReader(open(os.path.join(DIR, 'Recorders.csv')))
        for row in recorders:
            if ORG == "vuw":
                o = Recorder(code=row['Code'], organisation=vicu_org)
                o.save()
            else:
                o = Recorder(code=row['Code'], organisation=rfpt_org)
                o.save()

        deployments = csv.DictReader(open(os.path.join(DIR, 'Deployments.csv')))
        for row in deployments:
            site = Site.objects.get(code=row['Site'])
            recorder = Recorder.objects.get(code=row['Recorder'].strip())

            if not row['Deploy_time']:
                row['Deploy_time'] = '00:00:00'
            if not row['Recovery_time']:
                row['Recovery_time'] = '00:00:00'
            start = datetime.strptime(row['Deploy_date'] + ' ' + row['Deploy_time'], '%d/%m/%Y %H:%M:%S')
            if row['Recovery_date'].strip():
                end = datetime.strptime(row['Recovery_date'] + ' ' + row['Recovery_time'], '%d/%m/%Y %H:%M:%S')
            else:
                end = None
            if ORG == "vuw":
                o = Deployment(site=site, recorder=recorder, start=start, end=end, comments=row['Comments'], owner=vicu_org)
                o.save()
            else:
                o = Deployment(site=site, recorder=recorder, start=start, end=end, comments=row['Comments'], owner=rfpt_org)
                o.save()
