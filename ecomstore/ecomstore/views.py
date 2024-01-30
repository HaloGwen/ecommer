from django.shortcuts import render


def file_not_found_404(request):
    return render(
        request,
        "404.html",
        locals(),
        status=404, 
    )