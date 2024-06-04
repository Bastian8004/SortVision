from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .models import Main, Kraj, Polfinal, Final, PunktacjaJury, PunktacjaWidzowie
from .forms import PunktacjaJuryForm, PunktacjaWidzowieForm, ListaForm
from django.shortcuts import render
from django.http import JsonResponse
from .models import Kraj
import random



# Create your views here.

def main(request):
    mains = Main.objects.all().order_by()
    return render(request, 'main.html', {'mains': mains})

def losuj_polfinaly(request):
    # Sprawdź, czy półfinały zostały już wylosowane
    if 'polfinal1' in request.session and 'polfinal2' in request.session:
        polfinal1_kraje_ids = request.session.get('polfinal1', [])
        polfinal2_kraje_ids = request.session.get('polfinal2', [])

        polfinal1_kraje = Kraj.objects.filter(id__in=polfinal1_kraje_ids)
        polfinal2_kraje = Kraj.objects.filter(id__in=polfinal2_kraje_ids)

        return render(request, 'polfinal.html', {
            'polfinal1_kraje': polfinal1_kraje,
            'polfinal2_kraje': polfinal2_kraje,
        })

    kraje = list(Kraj.objects.all())
    random.shuffle(kraje)
    midpoint = len(kraje) // 2

    polfinal1_kraje = kraje[:midpoint]
    polfinal2_kraje = kraje[midpoint:]

    # Clear previous assignments
    Polfinal.objects.all().delete()

    # Assign countries to Polfinal instances
    for kraj in polfinal1_kraje:
        Polfinal.objects.create(kraj=kraj, polfinal='1')

    for kraj in polfinal2_kraje:
        Polfinal.objects.create(kraj=kraj, polfinal='2')

    # Store only IDs in session
    request.session['polfinal1'] = [kraj.id for kraj in polfinal1_kraje]
    request.session['polfinal2'] = [kraj.id for kraj in polfinal2_kraje]

    return render(request, 'polfinal.html', {
        'polfinal1_kraje': polfinal1_kraje,
        'polfinal2_kraje': polfinal2_kraje,
    })


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
def polfinaly(request):
    return render(request, 'polfinal.html')

def polfinal_detail(request, polfinal_num):
    # Pobierz wylosowane listy krajów z sesji
    polfinal_kraje_ids = request.session.get('polfinal{}'.format(polfinal_num), [])
    polfinal_kraje = Kraj.objects.filter(id__in=polfinal_kraje_ids)
    print("Kraje w półfinale {}: {}".format(polfinal_num, polfinal_kraje))
    return render(request, 'Polfinaly/polfinal_detail.html', {
        'polfinal_num': polfinal_num,
        'kraje': polfinal_kraje,
    })


from django.db import transaction

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

def potwierdzenie_polfinaly(request):
    return render(request, 'polfinal.html')