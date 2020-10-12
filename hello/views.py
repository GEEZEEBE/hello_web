from django.shortcuts import render

# Create your views here.
def form(request):
    return render(request, 'hello/requestform.html')

def responsewithhtml(request):
    data = dict()
    data['first'] = request.GET['first']
    data['second'] = request.GET['second']
    return render(request, 'hello/responsewithhtml.html', context=data)