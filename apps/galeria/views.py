from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from django.contrib import messages
from apps.galeria.forms import FotografiaForms


def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar a galeria.')
        return redirect('login')

    fotografias = Fotografia.objects.order_by('data_criacao').filter(publicada=True)

    return render(request, 'galeria/index.html', {'cards': fotografias} )

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk = foto_id)
    return render (request, 'galeria/imagem.html', {'fotografia': fotografia})

def buscar(request): 
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar a galeria.')
        return redirect('login')
    # Verificar se o usuario está autenticado
    fotografias = Fotografia.objects.order_by('data_criacao').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, 'galeria/index.html', {'cards': fotografias})

def nova_imagem(request):
    if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar a galeria.')
            return redirect('login')

    form = FotografiaForms
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia adicionada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao adicionar fotografia. Verifique os dados e tente novamente.')

    else:
        form = FotografiaForms()
    return render(request, 'galeria/nova_imagem.html', {'form' : form,})

def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia editada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao editar fotografia. Verifique os dados e tente novamente.')

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})

def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, 'Fotografia deletada com sucesso!')
    return redirect('index') 

def filtro(request, categoria):
    fotografias = Fotografia.objects.order_by('data_criacao').filter(publicada=True, categoria=categoria)

    return render(request, 'galeria/index.html', {'cards': fotografias,})