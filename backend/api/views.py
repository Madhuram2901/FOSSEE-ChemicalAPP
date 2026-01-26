from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """
    Root API endpoint - Health check
    Returns initialization status
    """
    return Response({
        'status': 'Backend initialized'
    })
