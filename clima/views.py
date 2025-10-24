import requests
from django.shortcuts import render

def home(request):
    cidade_digitada = request.GET.get('cidade', '')
    estado_digitado = request.GET.get('estado', '')
    pais_digitado = request.GET.get('pais', '')

    resultado = None
    sucesso = False

    if cidade_digitada:
        api_key = '439cddad5af6ab2ff0239d37043ce597'
        
        query = cidade_digitada
        if estado_digitado:
            query += f',{estado_digitado}'
        if pais_digitado:
            query += f',{pais_digitado}'

        geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={query}&limit=1&appid={api_key}'

        try:
            geo_res = requests.get(geo_url, timeout=5).json()
            if geo_res:
                city_info = geo_res[0]
                nome = city_info['name']
                estado = city_info.get('state', '')
                pais = city_info['country']
                lat = city_info['lat']
                lon = city_info['lon']

                weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=pt_br&appid={api_key}'
                weather_res = requests.get(weather_url, timeout=5).json()

                if weather_res.get('cod') == 200:
                    temp = weather_res['main']['temp']

                    if temp < 0:
                        roupa = "❄️ Super frio! Use roupa pesada, casaco grosso, luvas e cachecol."
                    elif temp < 10:
                        roupa = "🥶 Muito frio! Use casaco quente, luvas e gorro."
                    elif temp < 15:
                        roupa = "🧥 Frio! Jaqueta ou casaco leve, calça comprida."
                    elif temp < 20:
                        roupa = "🧤 Friozinho! Use luvas e roupa de frio leve."
                    elif temp < 25:
                        roupa = "👕 Roupa leve, confortável para o dia."
                    elif temp < 30:
                        roupa = "🌞 Roupa de calor, leve e fresca, use protetor solar."
                    else:
                        roupa = "🔥 Super calor! Use protetor solar, leve água e roupas bem leves."

                    resultado = {
                        'nome': nome,
                        'estado': estado,
                        'pais': pais,
                        'temp': temp,
                        'desc': weather_res['weather'][0]['description'].capitalize(),
                        'icone': weather_res['weather'][0]['icon'],
                        'roupa': roupa
                    }
                    sucesso = True
                else:
                    resultado = {'erro': weather_res.get('message', 'Clima não encontrado')}
            else:
                resultado = {'erro': 'Cidade não encontrada'}

        except Exception as e:
            resultado = {'erro': str(e)}

    return render(request, 'clima/home.html', {
        'resultado': resultado,
        'cidade_digitada': cidade_digitada,
        'estado_digitado': estado_digitado,
        'pais_digitado': pais_digitado,
        'sucesso': sucesso
    })
