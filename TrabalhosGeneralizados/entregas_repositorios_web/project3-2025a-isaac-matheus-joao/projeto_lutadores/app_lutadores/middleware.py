from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

# URLs públicas que não exigem autenticação
EXEMPT_URLS = [reverse('login'), reverse('logout')]

# Prefixos de caminhos públicos (estáticos e mídia)
EXEMPT_PATH_PREFIXES = ['/static/', '/media/']

class LoginRequiredMiddleware:
    """
    Middleware que bloqueia acesso a todas as views,
    exceto para as URLs e caminhos públicos listados em EXEMPT_URLS e EXEMPT_PATH_PREFIXES.
    Redireciona para settings.LOGIN_URL se não estiver autenticado.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permite acesso a arquivos estáticos e mídia
        if any(request.path.startswith(prefix) for prefix in EXEMPT_PATH_PREFIXES):
            return self.get_response(request)

        # Permite acesso a URLs públicas (login, logout)
        if request.path in EXEMPT_URLS:
            return self.get_response(request)

        # Se não estiver autenticado, redireciona para página de login
        if not request.session.get('usuario_id'):
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
