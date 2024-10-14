def unseen_files_count_processor(request):
    from .models import zip_file_parent
    unseen_files_count = zip_file_parent.objects.filter(seen=False).count()
    return {'unseen_files_count': unseen_files_count}