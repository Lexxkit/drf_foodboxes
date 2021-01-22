from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Item


@api_view(http_method_names=['GET'])
def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)

    response = {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'image': request.build_absolute_uri(item.image.url),
        'weight': item.weight,
        'price': str(item.price),
    }
    return Response(response)
