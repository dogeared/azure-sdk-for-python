# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar

from msrest import Serializer

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from .._vendor import _convert_request, _format_url_section
T = TypeVar('T')
JSONType = Any
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False

def build_list_request(
    subscription_id: str,
    resource_group_name: str,
    parent_provider_namespace: str,
    parent_resource_type: str,
    parent_resource_name: str,
    *,
    continuation_token_parameter: Optional[str] = None,
    **kwargs: Any
) -> HttpRequest:
    api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', pattern=r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.\(\)]*[a-zA-Z0-9_\-\(\)]$'),
        "parentProviderNamespace": _SERIALIZER.url("parent_provider_namespace", parent_provider_namespace, 'str', pattern=r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'),
        "parentResourceType": _SERIALIZER.url("parent_resource_type", parent_resource_type, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "parentResourceName": _SERIALIZER.url("parent_resource_name", parent_resource_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')
    if continuation_token_parameter is not None:
        _query_parameters['continuationToken'] = _SERIALIZER.query("continuation_token_parameter", continuation_token_parameter, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_get_request(
    subscription_id: str,
    resource_group_name: str,
    parent_provider_namespace: str,
    parent_resource_type: str,
    parent_resource_name: str,
    target_name: str,
    **kwargs: Any
) -> HttpRequest:
    api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', pattern=r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.\(\)]*[a-zA-Z0-9_\-\(\)]$'),
        "parentProviderNamespace": _SERIALIZER.url("parent_provider_namespace", parent_provider_namespace, 'str', pattern=r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'),
        "parentResourceType": _SERIALIZER.url("parent_resource_type", parent_resource_type, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "parentResourceName": _SERIALIZER.url("parent_resource_name", parent_resource_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "targetName": _SERIALIZER.url("target_name", target_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_delete_request(
    subscription_id: str,
    resource_group_name: str,
    parent_provider_namespace: str,
    parent_resource_type: str,
    parent_resource_name: str,
    target_name: str,
    **kwargs: Any
) -> HttpRequest:
    api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', pattern=r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.\(\)]*[a-zA-Z0-9_\-\(\)]$'),
        "parentProviderNamespace": _SERIALIZER.url("parent_provider_namespace", parent_provider_namespace, 'str', pattern=r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'),
        "parentResourceType": _SERIALIZER.url("parent_resource_type", parent_resource_type, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "parentResourceName": _SERIALIZER.url("parent_resource_name", parent_resource_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "targetName": _SERIALIZER.url("target_name", target_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="DELETE",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_create_or_update_request(
    subscription_id: str,
    resource_group_name: str,
    parent_provider_namespace: str,
    parent_resource_type: str,
    parent_resource_name: str,
    target_name: str,
    *,
    json: JSONType = None,
    content: Any = None,
    **kwargs: Any
) -> HttpRequest:
    api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', pattern=r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.\(\)]*[a-zA-Z0-9_\-\(\)]$'),
        "parentProviderNamespace": _SERIALIZER.url("parent_provider_namespace", parent_provider_namespace, 'str', pattern=r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'),
        "parentResourceType": _SERIALIZER.url("parent_resource_type", parent_resource_type, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "parentResourceName": _SERIALIZER.url("parent_resource_name", parent_resource_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
        "targetName": _SERIALIZER.url("target_name", target_name, 'str', pattern=r'^[a-zA-Z0-9_\-\.]+$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        _header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="PUT",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        json=json,
        content=content,
        **kwargs
    )

class TargetsOperations(object):
    """TargetsOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.chaos.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    @distributed_trace
    def list(
        self,
        resource_group_name: str,
        parent_provider_namespace: str,
        parent_resource_type: str,
        parent_resource_name: str,
        continuation_token_parameter: Optional[str] = None,
        **kwargs: Any
    ) -> Iterable["_models.TargetListResult"]:
        """Get a list of Target resources that extend a tracked regional resource.

        :param resource_group_name: String that represents an Azure resource group.
        :type resource_group_name: str
        :param parent_provider_namespace: String that represents a resource provider namespace.
        :type parent_provider_namespace: str
        :param parent_resource_type: String that represents a resource type.
        :type parent_resource_type: str
        :param parent_resource_name: String that represents a resource name.
        :type parent_resource_name: str
        :param continuation_token_parameter: String that sets the continuation token. Default value is
         None.
        :type continuation_token_parameter: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either TargetListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.chaos.models.TargetListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.TargetListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    parent_provider_namespace=parent_provider_namespace,
                    parent_resource_type=parent_resource_type,
                    parent_resource_name=parent_resource_name,
                    api_version=api_version,
                    continuation_token_parameter=continuation_token_parameter,
                    template_url=self.list.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    parent_provider_namespace=parent_provider_namespace,
                    parent_resource_type=parent_resource_type,
                    parent_resource_name=parent_resource_name,
                    api_version=api_version,
                    continuation_token_parameter=continuation_token_parameter,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize("TargetListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response


        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets"}  # type: ignore

    @distributed_trace
    def get(
        self,
        resource_group_name: str,
        parent_provider_namespace: str,
        parent_resource_type: str,
        parent_resource_name: str,
        target_name: str,
        **kwargs: Any
    ) -> "_models.Target":
        """Get a Target resource that extends a tracked regional resource.

        :param resource_group_name: String that represents an Azure resource group.
        :type resource_group_name: str
        :param parent_provider_namespace: String that represents a resource provider namespace.
        :type parent_provider_namespace: str
        :param parent_resource_type: String that represents a resource type.
        :type parent_resource_type: str
        :param parent_resource_name: String that represents a resource name.
        :type parent_resource_name: str
        :param target_name: String that represents a Target resource name.
        :type target_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Target, or the result of cls(response)
        :rtype: ~azure.mgmt.chaos.models.Target
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Target"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

        
        request = build_get_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            parent_provider_namespace=parent_provider_namespace,
            parent_resource_type=parent_resource_type,
            parent_resource_name=parent_resource_name,
            target_name=target_name,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Target', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}"}  # type: ignore


    @distributed_trace
    def delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name: str,
        parent_provider_namespace: str,
        parent_resource_type: str,
        parent_resource_name: str,
        target_name: str,
        **kwargs: Any
    ) -> None:
        """Delete a Target resource that extends a tracked regional resource.

        :param resource_group_name: String that represents an Azure resource group.
        :type resource_group_name: str
        :param parent_provider_namespace: String that represents a resource provider namespace.
        :type parent_provider_namespace: str
        :param parent_resource_type: String that represents a resource type.
        :type parent_resource_type: str
        :param parent_resource_name: String that represents a resource name.
        :type parent_resource_name: str
        :param target_name: String that represents a Target resource name.
        :type target_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str

        
        request = build_delete_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            parent_provider_namespace=parent_provider_namespace,
            parent_resource_type=parent_resource_type,
            parent_resource_name=parent_resource_name,
            target_name=target_name,
            api_version=api_version,
            template_url=self.delete.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}"}  # type: ignore


    @distributed_trace
    def create_or_update(
        self,
        resource_group_name: str,
        parent_provider_namespace: str,
        parent_resource_type: str,
        parent_resource_name: str,
        target_name: str,
        target: "_models.Target",
        **kwargs: Any
    ) -> "_models.Target":
        """Create or update a Target resource that extends a tracked regional resource.

        :param resource_group_name: String that represents an Azure resource group.
        :type resource_group_name: str
        :param parent_provider_namespace: String that represents a resource provider namespace.
        :type parent_provider_namespace: str
        :param parent_resource_type: String that represents a resource type.
        :type parent_resource_type: str
        :param parent_resource_name: String that represents a resource name.
        :type parent_resource_name: str
        :param target_name: String that represents a Target resource name.
        :type target_name: str
        :param target: Target resource to be created or updated.
        :type target: ~azure.mgmt.chaos.models.Target
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Target, or the result of cls(response)
        :rtype: ~azure.mgmt.chaos.models.Target
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Target"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-09-15-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(target, 'Target')

        request = build_create_or_update_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            parent_provider_namespace=parent_provider_namespace,
            parent_resource_type=parent_resource_type,
            parent_resource_name=parent_resource_name,
            target_name=target_name,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.create_or_update.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Target', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_or_update.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{parentProviderNamespace}/{parentResourceType}/{parentResourceName}/providers/Microsoft.Chaos/targets/{targetName}"}  # type: ignore

