from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def list(self, request):
        """Get all orders"""
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'message': 'Orders retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request):
        """Create a new order"""
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Order created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
