from BulkCropper.crop.pipeline import run_pipeline as run_crop
from BulkCropper.find.pipeline import run_pipeline as run_find

class PipelineController:

    def crop(self):
        run_crop(None)

    def find(self):
        run_find(None)