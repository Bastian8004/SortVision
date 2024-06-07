from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from .models import Main, Kraj, Polfinal, Final
from .forms import ListaForm, JuryGlosowanieForm
import random
import logging
from django.db import transaction

def main(request):
    mains = Main.objects.all().order_by()
    return render(request, 'main.html', {'mains': mains})

def lista(request):
    kraje = Kraj.objects.all()
    polfinal1 = request.session.get('polfinal1', [])
    polfinal2 = request.session.get('polfinal2', [])

    return render(request, 'lista.html', {
        'kraje': kraje,
        'polfinal1': [Kraj.objects.get(id=pk) for pk in polfinal1],
        'polfinal2': [Kraj.objects.get(id=pk) for pk in polfinal2],
    })

def kraj_new(request):
    if request.method == "POST":
        form = ListaForm(request.POST, request.FILES)
        if form.is_valid():
            kraj = form.save(commit=False)
            kraj.save()
            return redirect('lista_detail', pk=kraj.pk)
    else:
        form = ListaForm()
    return render(request, 'Lista/lista_edit.html', {'form': form})

def lista_detail(request, pk):
    kraj = get_object_or_404(Kraj, pk=pk)
    return render(request, 'Lista/lista_detail.html', {'kraj': kraj})

logger = logging.getLogger(__name__)

def losuj_polfinaly(request):
    kraje = list(Kraj.objects.all())
    random.shuffle(kraje)
    midpoint = len(kraje) // 2

    polfinal1_kraje = kraje[:midpoint]
    polfinal2_kraje = kraje[midpoint:]

    # Clear previous assignments
    Polfinal.objects.all().delete()

    # Assign countries to Polfinal instances
    with transaction.atomic():
        for kraj in polfinal1_kraje:
            Polfinal.objects.create(kraj=kraj, polfinal='1')

        for kraj in polfinal2_kraje:
            Polfinal.objects.create(kraj=kraj, polfinal='2')

    # Store only IDs in session
    request.session['polfinal1'] = [kraj.id for kraj in polfinal1_kraje]
    request.session['polfinal2'] = [kraj.id for kraj in polfinal2_kraje]

    logger.debug(f'Półfinał 1 kraje: {[kraj.nazwa for kraj in polfinal1_kraje]}')
    logger.debug(f'Półfinał 2 kraje: {[kraj.nazwa for kraj in polfinal2_kraje]}')

    return redirect('polfinal')


from django.db.models import F

def polfinal_vote(request, polfinal_num, kraj_id, points):
    if request.method == "POST":
        kraj = Kraj.objects.get(pk=kraj_id)
        polfinal = Polfinal.objects.get(polfinal=polfinal_num, kraj=kraj)
        polfinal.punkty = F('punkty') + points
        polfinal.save()

    return redirect('polfinal_detail', polfinal_num=polfinal_num)


def polfinal_detail(request, polfinal_num):
    # Pobierz indeks kraju, który aktualnie oddaje głosy
    current_index = request.session.get('current_index', 0)

    # Pobierz listę krajów z danego półfinału
    polfinal_kraje = Polfinal.objects.filter(polfinal=polfinal_num).select_related('kraj').order_by('-punkty')
    kraje = [p.kraj for p in polfinal_kraje]

    # Pobierz aktualny kraj, który oddaje głosy
    if current_index < len(kraje):
        current_kraj = kraje[current_index]
    else:
        current_kraj = None

    if request.method == 'POST' and current_kraj:
        form = JuryGlosowanieForm(kraje, current_kraj, request.POST)
        if form.is_valid():
            # Pobierz dane z formularza i przetwórz punkty
            points_map = {
                'points_1': 1,
                'points_2': 2,
                'points_3': 3,
                'points_4': 4,
                'points_5': 5,
                'points_6': 6,
                'points_7': 7,
                'points_8': 8,
                'points_10': 10,
                'points_12': 12
            }

            with transaction.atomic():
                for field, points in points_map.items():
                    kraj_id = form.cleaned_data.get(field)
                    if kraj_id:
                        Polfinal.objects.filter(polfinal=polfinal_num, kraj_id=kraj_id).update(punkty=F('punkty') + points)

            # Zwiększ indeks, aby kolejny kraj mógł oddać głosy
            current_index += 1
            request.session['current_index'] = current_index

            # Przekieruj do tego samego widoku, aby zresetować formularz i odświeżyć dane
            return redirect('polfinal_detail', polfinal_num=polfinal_num)

    else:
        form = JuryGlosowanieForm(kraje, current_kraj)

    # Pobierz zaktualizowaną listę krajów z danego półfinału (aby odświeżyć dane w tabeli)
    polfinal_kraje = Polfinal.objects.filter(polfinal=polfinal_num).select_related('kraj').order_by('-punkty')
    kraje_z_punktami = [{'kraj': p.kraj, 'punkty': p.punkty} for p in polfinal_kraje]

    return render(request, 'Polfinaly/polfinal_detail.html', {
        'polfinal_num': polfinal_num,
        'kraje': kraje_z_punktami,
        'current_kraj': current_kraj,
        'form': form if current_kraj else None,
    })




def polfinal(request):
    polfinal1_kraje = Polfinal.objects.filter(polfinal='1').select_related('kraj')
    polfinal2_kraje = Polfinal.objects.filter(polfinal='2').select_related('kraj')

    context = {
        'polfinal1_kraje': [p.kraj for p in polfinal1_kraje],
        'polfinal2_kraje': [p.kraj for p in polfinal2_kraje],
    }

    return render(request, 'polfinal.html', context)


def polfinal1(request):
    return redirect('polfinal_detail', polfinal_num='1')

def polfinal2(request):
    return redirect('polfinal_detail', polfinal_num='2')


def final(request):
    final = Final.objects.first()
    kraje = final.kraje.all()