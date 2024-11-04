# employees/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, ValidationError
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Employee model with custom response messages.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
        Optionally restricts the returned employees to a given department or role,
        by filtering against query parameters in the URL.
        """
        queryset = Employee.objects.all()
        department = self.request.query_params.get('department')
        role = self.request.query_params.get('role')

        if department:
            queryset = queryset.filter(department=department)
        if role:
            queryset = queryset.filter(role=role)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handle creation of a new employee with custom response for success or validation errors.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data = {
                "message": "Employee created successfully.",
                "employee": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)  # 201 Created
        except ValidationError:
            return Response(
                {"detail": "Bad request - invalid input data.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST  # 400 Bad Request
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single employee with a custom 404 error message if not found.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Employee.DoesNotExist:
            raise NotFound({"detail": "Employee not found with the given ID."})  # 404 Not Found

    def update(self, request, *args, **kwargs):
        """
        Update an employee with custom validation error handling.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_data = {
                "message": "Employee updated successfully.",
                "employee": serializer.data
            }
            return Response(response_data)  # 200 OK by default for successful update
        except ValidationError:
            return Response(
                {"detail": "Bad request - invalid input data.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST  # 400 Bad Request
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an employee with a custom 204 No Content response on success.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Employee deleted successfully."},
            status=status.HTTP_204_NO_CONTENT  # 204 No Content
        )
