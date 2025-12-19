from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrderFollowers
from workorder_api.serializers.workorder_follower_serializer import WorkOrderFollowerSerializer
from core_api.response_utils.custom_response import CustomResponse
from django.db.models import F,Concat
from rest_framework import status


class WorkOrderFollowerCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderFollowerSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order follower created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order follower creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order follower creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderFollowerDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            workorder_follower = WorkOrderFollowers.objects.get(id=id)
            serializer = WorkOrderFollowerSerializer(workorder_follower)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order follower fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order follower fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )   
    
    def put(self, request, id):
        try:
            workorder_follower = WorkOrderFollowers.objects.get(id=id)
            serializer = WorkOrderFollowerSerializer(workorder_follower, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order follower updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",   
                    message=["Error in Work order follower updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order follower updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def delete(self, request, id):
        try:
            workorder_follower = WorkOrderFollowers.objects.get(id=id)
            workorder_follower.delete()
            return CustomResponse(
                data=None,
                status="success",
                message=["Work order follower deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order follower deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderFollowerListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, workorder_id):
        try:
            workorder_followers = WorkOrderFollowers.objects.filter(workorder=workorder_id).annotate(
                follower_name=Concat(F('follower__first_name'),Value(' '),F('follower__last_name'))
            ).order_by('created_at')
            return CustomResponse(
                data=workorder_followers,
                status="success",
                message=["Work order followers fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e: 
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order follower fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )