from import_export import resources
from .models import QuestionMaster,UserProfile

class QuestionMasterResource(resources.ModelResource):
    class Meta:
        model = QuestionMaster

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile