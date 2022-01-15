from django.http import HttpResponse
from django.shortcuts import render
from loguru import logger


class ErrorLogMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    # TO DO: page for exceptions
    def process_exception(self, request, exception):
        logger.error(f'Error middleware: {exception}')
        # return render(request, 'includes/404.html')


