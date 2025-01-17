from rest_framework.viewsets import GenericViewSet


class GenericGUIDViewSet(GenericViewSet):
    lookup_field = 'guid'
    lookup_value_regex = '[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'
