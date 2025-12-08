from rest_framework.response import Response
from rest_framework import generics,status
from workorder_api.models import Services
from workorder_api.serializers.service_serializer import ServiceSerializer
from core_api.response_utils.custom_response import CustomResponse

class ServiceCreateView(generics.CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            serializer = ServiceSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Service creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class ServiceUpdateView(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Service fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def put(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Service updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def patch(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(  
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Service updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def delete(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            service.is_delete = True
            service.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Service deleted successfully"],
                status_code=status.HTTP_204_NO_CONTENT,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )