from .models import FinancialData
from .serializers import (
    FinancialDataSerializer,
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.db.models import Avg
from django.db.models import Q


class CustomResponse:
    """
    Custom response format. If there is no pagination then it will be ommited from response.
    """

    def get_response(
        self, data=[], error="", status_code=200, pagination=None
    ):
        if pagination:
            return Response(
                {
                    "data": data,
                    "pagination": {
                        "count": pagination.get("count", 0),
                        "page": pagination.get("page", 0),
                        "limit": pagination.get("limit", 0),
                        "pages": pagination.get("pages", 0),
                    },
                    "info": {"error": error},
                }
            )
        else:
            return Response(
                {
                    "data": data,
                    "info": {"error": error},
                },
                status=status_code,
            )


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class to provide default page size is 5 and accept limit
    and page param and filter the data accordingly
    """

    page_size = 5
    page_size_query_param = "limit"
    max_page_size = 5
    page_query_param = "page"

    def get_paginated_response(self, data=[]):
        return Response(
            {
                "data": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "page": self.page.number,
                    "limit": self.page.paginator.per_page,
                    "pages": self.page.paginator.num_pages,
                },
            }
        )


class FinancialDataViewSet(viewsets.ModelViewSet):
    """
    Financial Data model view set provided necessary list generation according
    to filter criteria.

    - start_date, end_date and symbol query params are optional
    - response is formated using CustomResponse class
    - Unpredictable error and param value not found error was checked by execptions
    """

    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer
    pagination_class = CustomPagination

    def __init__(self, **kwargs):
        super(FinancialDataViewSet, self).__init__(**kwargs)

    def list(self, request):
        try:
            start_date = request.GET.get("start_date", None)
            end_date = request.GET.get("end_date", None)
            symbol = request.GET.get("symbol", None)

            if start_date:
                self.queryset = self.queryset.filter(date__lte=start_date)

            if end_date:
                self.queryset = self.queryset.filter(date__gte=end_date)

            if symbol:
                self.queryset = self.queryset.filter(symbol=symbol)

            result = super(FinancialDataViewSet, self).list(request).data

            return CustomResponse().get_response(
                data=result.get("data"), pagination=result.get("pagination")
            )

        except NotFound as err:
            return CustomResponse().get_response(
                error=err.args[0], status_code=400
            )
        except Exception as err:
            return CustomResponse().get_response(
                error=err.args[0], status_code=500
            )


class StatisticsApiView(APIView):
    """
    Statistics API end point will be serve from this view

    - start_date, end_date and symbol query params are not optional and errors are raised accordingly
    - reponse is formated using CustomResponse class
    - Unpredictable error and param value not found error was checked
    """

    def get(self, request, *args, **kwargs):
        try:
            start_date = request.GET.get("start_date", None)
            end_date = request.GET.get("end_date", None)
            symbol = request.GET.get("symbol", None)

            if not (start_date and end_date and symbol):
                raise NotFound("Essential query param was not found!")

            queryset = FinancialData.objects.filter(
                Q(date__gte=start_date)
                & Q(date__lte=end_date)
                & Q(symbol=symbol)
            )

            result = queryset.values("symbol").annotate(
                average_daily_open_price=Avg("open_price"),
                average_daily_close_price=Avg("close_price"),
                average_daily_volume=Avg("volume"),
            )
            if result:
                result = result[0]
                result["start_date"] = start_date
                result["end_date"] = end_date

            return CustomResponse().get_response(data=result)

        except NotFound as err:
            return CustomResponse().get_response(
                error=err.args[0], status_code=400
            )
        except Exception as err:
            return CustomResponse().get_response(
                error=err.args[0], status_code=500
            )
