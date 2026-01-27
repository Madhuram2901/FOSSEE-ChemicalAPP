from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedDataset
from .serializers import UploadedDatasetSerializer
from .utils import analyze_csv


@api_view(['GET'])
def api_root(request):
    """
    Root API endpoint - Health check
    Returns initialization status
    """
    return Response({
        'status': 'Backend initialized'
    })


@api_view(["POST"])
def upload_csv(request):
    """
    Upload a CSV file and analyze it
    """
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "CSV file required"}, status=400)

    dataset = UploadedDataset.objects.create(file=file, summary={})

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


@api_view(["GET"])
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
def history(request):
    """
    Get list of recent uploads (last 5)
    """
    datasets = UploadedDataset.objects.order_by("-uploaded_at")[:5]
    return Response([
        {
            "id": d.id,
            "filename": d.file.name.split("/")[-1] if d.file else "Unknown",
            "uploaded_at": d.uploaded_at
        }
        for d in datasets
    ])

