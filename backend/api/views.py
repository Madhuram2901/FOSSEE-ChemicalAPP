from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import UploadedDataset
from .serializers import UploadedDatasetSerializer
from .utils import analyze_csv


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Root API endpoint - Health check
    Returns initialization status
    """
    return Response({
        'status': 'Backend initialized'
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload a CSV file and analyze it
    """
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "CSV file required"}, status=400)

    # Store the original filename provided by the client
    original_filename = file.name
    
    # Django will automatically handle duplicate filenames for the 'file' field
    dataset = UploadedDataset.objects.create(
        file=file, 
        original_filename=original_filename, 
        summary={}
    )

    try:
        summary = analyze_csv(dataset.file.path)
    except Exception as e:
        dataset.delete()
        return Response({"error": str(e)}, status=400)

    dataset.summary = summary
    dataset.save()

    # Keep only last 5 datasets
    qs = UploadedDataset.objects.order_by("-uploaded_at")
    if qs.count() > 5:
        for old in qs[5:]:
            old.delete()

    return Response({
        "dataset_id": dataset.id,
        "message": "File uploaded successfully"
    })


from django.http import FileResponse
from .reports import generate_pdf_report

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary(request, dataset_id):
    """
    Get summary for a specific dataset
    """
    try:
        dataset = UploadedDataset.objects.get(id=dataset_id)
    except UploadedDataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    return Response(dataset.summary)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_report(request, dataset_id):
    """
    Generate and download PDF report for a dataset
    """
    try:
        dataset = UploadedDataset.objects.get(id=dataset_id)
    except UploadedDataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    pdf_buffer = generate_pdf_report(dataset)
    
    response = FileResponse(pdf_buffer, as_attachment=True, filename=f"report_{dataset.id}.pdf")
    return response


from .comparison import compare_datasets

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def compare_datasets_view(request):
    """
    Compare two datasets
    """
    id_a = request.GET.get('dataset_a')
    id_b = request.GET.get('dataset_b')

    if not id_a or not id_b:
        return Response({"error": "Both dataset_a and dataset_b parameters are required"}, status=400)

    try:
        dataset_a = UploadedDataset.objects.get(id=id_a)
        dataset_b = UploadedDataset.objects.get(id=id_b)
    except UploadedDataset.DoesNotExist:
        return Response({"error": "One or both datasets not found"}, status=404)
    except ValueError:
        return Response({"error": "Invalid ID format"}, status=400)

    result = compare_datasets(dataset_a, dataset_b)
    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history(request):
    """
    Get list of recent uploads (last 5)
    """
    datasets = UploadedDataset.objects.order_by("-uploaded_at")[:5]
    return Response([
        {
            "id": d.id,
            # Use original_filename if available, otherwise fall back to file name
            "filename": d.original_filename if d.original_filename else (d.file.name.split("/")[-1] if d.file else "Unknown"),
            "uploaded_at": d.uploaded_at
        }
        for d in datasets
    ])

