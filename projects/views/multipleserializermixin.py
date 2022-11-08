"""
mixin class

    @get_queryset : returning the detail serializer or simple list serializer
                    following the request action type

@author : Sylvain GAUTHIER
@version : 1.0
"""


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' \
                and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
