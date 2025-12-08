from ...serializers.room_serializer import RoomSerializer
from ...models import Rooms
from core_api.response_utils.custom_response import CustomResponse
from rest_framework.views import APIView

class RoomCreateView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            serializer = RoomSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Room creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoomUpdateView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request,pk):
        try:
            room = Rooms.objects.get(id=pk,is_delete=False)
            serializer = RoomSerializer(room)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Room fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )   
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def put(self, request,pk):
        try:
            data=request.data
            room = Rooms.objects.get(id=pk,is_delete=False)
            serializer = RoomSerializer(room, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Room updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def patch(self, request,pk):
        try:
            data=request.data
            room = Rooms.objects.get(id=pk,is_delete=False)
            serializer = RoomSerializer(room, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room updated successfully"],
                        status_code=status.HTTP_200_OK,
                        content_type="application/json"
                    )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Room updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    def delete(self, request,pk):
        try:
            room = Rooms.objects.get(id=pk,is_delete=False)
            room.is_delete = True
            room.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Room deleted successfully"],
                status_code=status.HTTP_204_NO_CONTENT,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )