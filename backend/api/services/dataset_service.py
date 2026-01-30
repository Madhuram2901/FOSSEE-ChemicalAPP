from ..models import UploadedDataset
from ..utils import analyze_csv
from django.db.models import Q

def handle_upload(file, user=None):
    """
    Orchestrates the upload process:
    1. Creates dataset record
    2. Runs analysis
    3. Cleans up old datasets
    """
    original_filename = file.name
    
    # Create initial record
    dataset = UploadedDataset.objects.create(
        file=file,
        original_filename=original_filename,
        user=user,
        summary={}
    )
    
    # Run analysis
    try:
        # Note: dataset.file.path is available because we saved the object
        summary = analyze_csv(dataset.file.path)
        dataset.summary = summary
        dataset.save()
    except Exception as e:
        # If analysis fails, remove the file/record to avoid junk
        dataset.delete()
        raise e 
        
    # Cleanup old datasets for this user context
    cleanup_old_datasets(user)
    
    return dataset

def cleanup_old_datasets(user=None, limit=5):
    """
    Enforces the limit on number of datasets per user (or anonymous context)
    """
    if user:
        qs = UploadedDataset.objects.filter(user=user).order_by("-uploaded_at")
    else:
        qs = UploadedDataset.objects.filter(user__isnull=True).order_by("-uploaded_at")
        
    if qs.count() > limit:
        # Delete oldest
        # Using slice [limit:] returns the list logic in python, but for queryset delete()
        # we need to be careful. slicing returns a new queryset.
        # We can collect IDs to delete.
        ids_to_delete = qs[limit:].values_list('id', flat=True)
        UploadedDataset.objects.filter(id__in=list(ids_to_delete)).delete()
