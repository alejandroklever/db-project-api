from rest_framework.filters import BaseFilterBackend


class GenericFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        dic = {item: request.query_params[item] for item in request.query_params if item not in ('many', 'page')}
        many = 'page' in request.query_params or 'many' not in request.query_params or (
                    'many' in request.query_params and
                    request.query_params['many'] != 'false')
        try:
            queryset = queryset.filter(**dic) if many else [queryset.get(**dic)]
        except queryset.model.DoesNotExist:
            queryset = queryset.none()
        return queryset
