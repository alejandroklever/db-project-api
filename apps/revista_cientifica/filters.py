from rest_framework.filters import BaseFilterBackend


class GenericFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        dic = {}
        for item in request.query_params.keys():
            if item != 'many':
                dic[item] = request.query_params[item]
        many = True
        if 'many' in request.query_params.keys():
            many = request.query_params['many']
        try:
            if many:
                queryset = queryset.filter(**dic)
            else:
                queryset = queryset.get(**dic)
        except Exception as e:
            queryset = queryset.none()
        return queryset


