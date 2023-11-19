from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages
# Create your views here.
def character_list(request):
    equipements= Equipement.objects.all()
    characters=Character.objects.all()
    return render(request, 'blog/character_list.html', {'equipements': equipements, 'characters': characters})
def character_detail(request, id_character):
    message = ''
    error = None
    character = get_object_or_404(Character, id_character=id_character)
    form = MoveForm(request.POST, instance=character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    if request.method == 'POST' and form.is_valid():
        
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        if nouveau_lieu.disponibilite == 'libre' and check_etats(character, nouveau_lieu.id_equip):
            refresh_etats(character, nouveau_lieu.id_equip)
            form.save()
            if nouveau_lieu.id_equip == 'Terrain de foot':
                nouveau_lieu.disponibilite = "libre"
            else:
                nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            message = f'{character.id_character} est maintenant à {nouveau_lieu.id_equip} et il/elle est {character.etat}.'
            error = False
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
        else:
            # Error message
            message = 'Cette modification ne peut pas être realisée.'
            error = True

        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': ancien_lieu, 'form': form, 'message': message, 'error': error})

    else:
        form = MoveForm()
        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': ancien_lieu, 'form': form, 'message': message, 'error': error})

def check_etats (character, n_lieu):
    if n_lieu == 'Terrain de foot' and character.etat == 'endormi':
        return True
    elif n_lieu == 'Cantine' and character.etat == 'affamé':
        return True
    elif n_lieu == 'Salle de musculation' and character.etat == 'repus':
        return True
    elif n_lieu == 'Dortoir' and character.etat == 'fatigué':
        return True
    else:
        return False

def refresh_etats (character,lieu):
    if lieu == 'Terrain de foot':
        character.etat = 'affamé'
    elif lieu == 'Cantine':
        character.etat = 'repus'
    elif lieu == 'Salle de musculation':
        character.etat = 'fatigué'
    elif lieu == 'Dortoir':
        character.etat = 'endormi'
    character.save()
    pass
def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    characters=Character.objects.all()
    return render(request, 'blog/equipement_detail.html', {'equipement': equipement,'characters': characters})

def characters_list(request):
    characters = Character.objects.all()
    return render(request, 'blog/characters_list.html', {'characters': characters})

def equipements_list(request):
    equipements = Equipement.objects.all()
    return render(request, 'blog/equipements_list.html', {'equipements': equipements})
def base(request):
    equipements = Equipement.objects.all()
    characters=Character.objects.all()
    return render(request, 'blog/base.html', {'equipements': equipements, 'characters': characters})
  