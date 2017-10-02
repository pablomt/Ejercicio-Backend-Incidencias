# coding=utf-8
import json
import copy

from decimal import Decimal
from datetime import date


class Utilities():
    # Toma un queryset, lo vuelve serializable y lo serializa para poder devolverlo al cliente.
    @staticmethod
    def query_set_to_dumps(query_set_object):
        return json.dumps(map(lambda model_object: model_object.to_serializable_dict(), query_set_object),
                          indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False
                          )

    # Toma un objeto tipo json, y lo serializa para poder mandarlo al cliente.
    @staticmethod
    def json_to_dumps(json_object):
        return json.dumps(json_object, indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False)

    # Transforma un queryset a un objeto tipo JSON.
    @staticmethod
    def query_set_to_dictionary(query_set_object):
        return map(lambda model_object: model_object.to_serializable_dict(), query_set_object)

    @staticmethod
    def clean_generic_queryset(query_set_object):
        """
        Cleans a QuerySet object, converting it's decimal properties to strings.
        :param query_set_object: object to clean
        :return: the QuerySet object with the decimal attributes converted to strings
        """
        response = []
        for obj in query_set_object:
            for obj_attr in obj.keys():
                if type(obj[obj_attr]) is Decimal or type(obj[obj_attr]) is date:
                    obj[obj_attr] = str(obj[obj_attr])
            response.append(obj)
        return response
