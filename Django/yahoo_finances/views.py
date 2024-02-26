from django.shortcuts import render, get_object_or_404
from .models import Company, DailyStockHistory


def company_details(request, company_id):
    # Obtenha os detalhes da Company
    company = get_object_or_404(Company, pk=company_id)

    # Obtenha os dados do DailyStockHistory para essa Company
    stock_history = DailyStockHistory.objects.filter(symbol=company.symbol)

    # Passe os dados para o template
    return render(request, 'company_details.html', {'company': company, 'stock_history': stock_history})
