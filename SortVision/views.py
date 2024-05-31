from django.shortcuts import render, redirect
from .models import Main, Kraj, Polfinal, Final, PunktacjaJury, PunktacjaWidzowie
from .forms import PunktacjaJuryForm, PunktacjaWidzowieForm
import random

# Create your views here.

def main(request):
    mains = Main.objects.all().order_by()
    return render(request, 'main.html', {'mains': mains})



def lista(request):
    kraje = Kraj.objects.all()
    return render(request, 'lista.html', {'kraje': kraje})


def polfinal(request, numer):
    polfinal = Polfinal.objects.get(numer=numer)
    kraje = polfinal.kraje.all()

    if request.method == "POST":
        if 'jury_form' in request.POST:
            form = PunktacjaJuryForm(request.POST)
            if form.is_valid():
                punktacja = form.save(commit=False)
                punktacja.polfinal = polfinal
                punktacja.save()
                return redirect('polfinal', numer=numer)
        elif 'widzowie_form' in request.POST:
            widzowie_form = PunktacjaWidzowieForm(request.POST)
            if widzowie_form.is_valid():
                punktacja = widzowie_form.save(commit=False)
                punktacja.polfinal = polfinal
                punktacja.save()
                return redirect('polfinal', numer=numer)
    else:
        form = PunktacjaJuryForm()
        widzowie_form = PunktacjaWidzowieForm()

    punktacje_jury = PunktacjaJury.objects.filter(polfinal=polfinal).order_by('-punkty')
    punktacje_widzowie = PunktacjaWidzowie.objects.filter(polfinal=polfinal).order_by('-punkty')

    return render(request, 'polfinal.html', {
        'kraje': kraje,
        'numer': numer,
        'form': form,
        'widzowie_form': widzowie_form,
        'punktacje_jury': punktacje_jury,
        'punktacje_widzowie': punktacje_widzowie,
    })


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


def losowanie_polfinalow(request):
    kraje = list(Kraj.objects.all())
    random.shuffle(kraje)
    polfinal1_kraje = kraje[:len(kraje) // 2]
    polfinal2_kraje = kraje[len(kraje) // 2:]

    polfinal1 = Polfinal.objects.create(numer=1)
    polfinal2 = Polfinal.objects.create(numer=2)

    polfinal1.kraje.set(polfinal1_kraje)
    polfinal2.kraje.set(polfinal2_kraje)

    return redirect('lista_krajow')

