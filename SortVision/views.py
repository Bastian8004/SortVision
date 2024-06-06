from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from .models import Main, Kraj, Polfinal, Final, PunktacjaJury, PunktacjaWidzowie
from .forms import PunktacjaJuryForm, PunktacjaWidzowieForm, ListaForm
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


def polfinal_detail(request, polfinal_num):
    # Pobierz kraje z bazy danych dla odpowiedniego półfinału
    polfinal_kraje = Polfinal.objects.filter(polfinal=polfinal_num).select_related('kraj')
    kraje = [p.kraj for p in polfinal_kraje]

    return render(request, 'Polfinaly/polfinal_detail.html', {
        'polfinal_num': polfinal_num,
        'kraje': kraje,
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


@transaction.atomic
def zapisz_polfinaly(request):
    if request.method == 'POST':
        polfinal1_ids = request.session.get('polfinal1', [])
        polfinal2_ids = request.session.get('polfinal2', [])

        polfinal1_kraje = Kraj.objects.filter(id__in=polfinal1_ids)
        polfinal2_kraje = Kraj.objects.filter(id__in=polfinal2_ids)

        # Clear previous assignments
        Polfinal.objects.all().delete()

        # Assign countries to Polfinal instances
        for kraj in polfinal1_kraje:
            Polfinal.objects.create(kraj=kraj, polfinal=1)

        for kraj in polfinal2_kraje:
            Polfinal.objects.create(kraj=kraj, polfinal=2)

        # Redirect to a confirmation page or the main page
        return redirect(reverse('potwierdzenie_polfinaly'))

    return redirect(reverse('potwierdzenie_polfinaly'))

def potwierdzenie_polfinaly(request):
    return render(request, 'polfinal.html')

def final(request):
    final = Final.objects.first()
    kraje = final.kraje.all()

    if request.method == "POST":
        if 'jury_form' in request.POST:
            form = PunktacjaJuryForm(request.POST)
            if form.is_valid():
                punktacja = form.save(commit=False)
                punktacja.final = final
                punktacja.save()
                return redirect('final')
        elif 'widzowie_form' in request.POST:
            widzowie_form = PunktacjaWidzowieForm(request.POST)
            if widzowie_form.is_valid():
                punktacja = widzowie_form.save(commit=False)
                punktacja.final = final
                punktacja.save()
                return redirect('final')
    else:
        form = PunktacjaJuryForm()
        widzowie_form = PunktacjaWidzowieForm()

    punktacje_jury = PunktacjaJury.objects.filter(final=final).order_by('-punkty')
    punktacje_widzowie = PunktacjaWidzowie.objects.filter(final=final).order_by('-punkty')

    return render(request, 'final.html', {
        'kraje': kraje,
        'form': form,
        'widzowie_form': widzowie_form,
        'punktacje_jury': punktacje_jury,
        'punktacje_widzowie': punktacje_widzowie,
    })

