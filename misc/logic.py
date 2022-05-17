from django.contrib.postgres.search import TrigramWordSimilarity
from django import forms

from .models import Medicine
from utils import getData


class QueryForm(forms.Form):
    query = forms.CharField(max_length=20)


def queryMedicines(req: dict):
    valid, data = getData(req, QueryForm)
    if not valid:
        return { 'medicines': [] }

    medicines = Medicine.objects.annotate(
        similarity=TrigramWordSimilarity(data['query'], 'name') + TrigramWordSimilarity(data['query'], 'description')
    ).filter(similarity__gt=0.7, searchable=True).order_by('-similarity')

    return { 'medicines': [{
        'uid': medicine.id.hex,
        'name': medicine.name,
        'description': medicine.description,
        'composition': medicine.composition,
        'expiration': medicine.expiration,
        'cost': medicine.cost
    } for medicine in medicines] }