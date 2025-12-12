from rest_framework.views import APIView
from workorder_api.models import WorkOrderComments
from workorder_api.serializers.workorder_comments_serializer import WorkOrderCommentsSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class WorkOrderCommentsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderCommentsSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order comment created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order comment creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order comment creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderCommentsListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,workorder_id):
        try:
            workorder_comments = WorkOrderComments.objects.filter(workorder=workorder_id).order_by('-created_at')
            serializer = WorkOrderCommentsSerializer(workorder_comments, many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order comments fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order comments fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )