from rest_framework.views import APIView
from workorder_api.models import WorkOrderTimeline
from workorder_api.serializers.workorder_timeline_serializer import WorkOrderTimelineSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class WorkOrderTimelineCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderTimelineSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order timeline created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
        except Exception as e:
            print(""""e""""",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order timeline creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderTimelineListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,workorder_id):
        try:
            workorder_timeline = WorkOrderTimeline.objects.filter(workorder=workorder_id).order_by('-created_at')
            serializer = WorkOrderTimelineSerializer(workorder_timeline, many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order timeline fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order timeline fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )