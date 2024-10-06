from django.shortcuts import render, get_object_or_404
from core_imoveis.models import Casa, Bairro, User
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

#Mostra a página inicial do site
def tela_login(request):
    return render(request, 'login.html')



def login_submit(request):
    if request.POST:
        usuario = request.POST.get('usuario')   #Pega o campo usuario do formulario de login
        senha = request.POST.get('senha')       #Pega o campo senha do formulario de login
        user = authenticate(username=usuario,password=senha) #  Autentica o usuario
        if user is not None: #Se o usuario não for vazio
            login(request,user)
            return redirect('/imoveis/')
        else:
            messages.error(request,"Usuario e senha invalidos")
            return redirect('/')




def tela_novouser(request):
    return render(request,'novo-user.html')



def novouser_submit(request):
    if request.POST:
        usuario = request.POST.get('novo_user')
        senha = request.POST.get('nova_senha')
        if User.objects.filter(username=usuario).exists():
            novo_usuario = User.objects.filter(username=usuario) #Se o nome do usuario já existir retorne "Usuário já existente"
            return HttpResponse('Usuário já existente') #mostra a mensagem se o usuario já existir
        else:
            User.objects.create_user(username = usuario, #username=campo PADRÃO DO DJANGO, SEMPRE vai ser USADO tanto em QuerySet e parâmetros
                            password = senha, #password = campo PADRÃO DO DJANGO, SEMPRE vai ser USADO tanto em QuerySet e parâmetros
                            is_staff=True, # para ter acesso ao admin
                            is_active=True) #Verifica se está ativo
            return redirect('/imoveis/')
    else:
        return HttpResponse('Refaça o cadastro')




@login_required(login_url="/login/")
def tela_imoveis(request):
    return render(request,'inicial.html') #Mostra a página inicial do site





#Ao apertar o botão "COMPRA CASA" abre a página para procurar uma casa para comprar
@login_required(login_url="/login/")
def compra_casa(request):
    return render(request,'comprar.html') #mostra a página html de comprar casa
    #PESQUISAR POR CASAS PARA COMPRAR




@login_required(login_url="/login/")
def buscar_casa(request):
    pesquisa = request.GET.get('busca') #variavel que guarda o termo pequisado pelo usuario através do GET.get (que é quando o usuario pede pra ver algo do servidor)
    if pesquisa: #Se existir o que foi pesquisado
        resultado = Casa.objects.filter(                                #busca o que foi digitado dentro do modelo casa
            Q(endereco__icontains=pesquisa)                 #__icontains:lookup que verifica o valor de bairro    # =pesquisa: comparativo usado para verificar se o valor de "bairro___icontains" é igual ao da variável pesquisa
        ) 
    else: #se não
        resultado = Casa.objects.all() #mostra todas as casas registradas para vendas
    busca = {'resultados':resultado}
    return render(request,'buscar-casas.html',busca)






#Ao apertar o botão "VENDA CASA" abre a página pra colocas as informações da casa e vende-lá
@login_required(login_url="/login/")
def venda_casa(request):
    return render(request,'vendas.html') #Mostra a página para quem deseja vender casas





#Função usada para armazenar o valor dos campos no formulario, ao ser preenchido vai ser criado e salvado no modelo criado anteriormente no models(Casa)
@login_required(login_url="/login/")
def vendacasa_submit(request):
    if request.POST:                                                        #se o formulário foi enviado
        nome_bairro = request.POST.get('bairro') #guarda o valor do campo "bairro" do formulario de vendas dentro da variável "nome_bairro" do modeelo Casa
        if Bairro.objects.filter(bairro=nome_bairro).exists(): # Se existir ele cria uma variável contendo o bairro do modelo Bairro e vê que não precisa adiciona o mesmo bairro duas vezes
            bairro_objeto = Bairro.objects.get(bairro=nome_bairro)
        else:# Se não existir ele cria uma varável contendo o valor de bairro do modelo Bairro
            bairro_objeto = Bairro.objects.create(bairro=nome_bairro)
        valor = request.POST.get('valor') #armazena o valor do campo valor 
        quartos = request.POST.get('quartos') #armazena o valor do campo quartos na variável referente ao modelo Casa
        area = request.POST.get('area')#armazena o valor do campo area na variável referente ao modelo Casa
        endereco = request.POST.get('endereco')#armazena o valor do campo endereco na variavel referente ao modelo Casa
         #armazena a instância de Bairro(valor do campo bairro) e joga para o bairro do modelo Casa

        #Cria e salva o objeto dentro do django admin
        Casa.objects.create(valor=valor,
                            quartos=quartos,
                            area=area,
                            endereco=endereco,
                            usuario=request.user,
                            nome_bairro=bairro_objeto)
    return redirect('/imoveis/')




@login_required(login_url="/login/")
#Aparece a lista de casas que foi criado pelo usuario logado para pôr á venda
def listacasa(request):
    usuario_logado = request.user #Pega o usúario logado
    casa = Casa.objects.filter(usuario=usuario_logado)                               #É um QuerySet de Casa, função: Pega todas as instâncias(casas criadas) de Casa CRIADA PELO USUÁRIO LOGADO
    dados = {'casas':casa}                                      # Imagine um arquivo contendo vários outros arquivos: meu arquivo CASAS guarda todos os meus arquivos, ou seja,MINHA CHAVE CASAS GUARDA TODAS MINHAS INSTÂSNCIAS(casas criadas) DO MODELO CASA 
    return render(request,'lista-casa.html',dados)              # Renderiza a página html contendo a lista de casa que o usuario criou para pôr a venda



@login_required(login_url="/login/")
def edite_casa(request,id_casa):
    dados = {}                                                              # Dicionario vazio que irá armazenar o objeto
    dados['casa'] = Casa.objects.get(id=id_casa)                            # O dicionário "dados" armazena o objeto "Evento.objects.get(id=id_evento)" que por sua vez armazena os dados da página html.
                                                                            # QUE DADOS SÃO ESSES ? 
                                                                            # O valor(formulario)=valor(modelo 'Casa'),quartos(formulario)=quartos(modelo 'Evento'),area(formulario)=area(modelo 'Evento') e por aí vai.
    return render(request,'vendas.html',dados)                              # Renderiza a página html que o usuario deseja ver e passa os dados para o template permitindo a exibição dos dados de cada Casa. 




def delete_casa(request, id_casa):
    usuario = request.user #Pega o usuário atualmente da sessão
    casa = get_object_or_404(Casa, id=id_casa) # Busca a casa pelo ID fornecido
    if usuario == casa.usuario: # Verifica se a casa pertence ao Usuário logado
        casa.delete() #se for o dono da casa, ela pode ser excluída
    return redirect('/imoveis/mostrarlista/')#Retorna pra lista de casas do usuário



'''def delete_casa(request, id_casa):
    usuario = request.user #Pega o usuário atualmente da sessão
    casa = Casa.objects.get(Casa, id=id_casa) # Busca a casa pelo ID fornecido
    if usuario == casa.usuario: # Verifica se a casa pertence ao Usuário logado
        casa.delete() #se for o dono da casa, ela pode ser excluída
    return redirect('/imoveis/mostrarlista/')#Retorna pra lista de casas do usuário'''
