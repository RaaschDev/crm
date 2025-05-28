from django.shortcuts import render

def landing_page(request):
    """
    View for the landing page of CRM Pro
    """
    return render(request, 'pages/landing.html') 