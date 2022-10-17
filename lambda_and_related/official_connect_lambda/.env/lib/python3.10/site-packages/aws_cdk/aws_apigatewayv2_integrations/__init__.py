'''
# AWS APIGatewayv2 Integrations

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [HTTP APIs](#http-apis)

  * [Lambda Integration](#lambda)
  * [HTTP Proxy Integration](#http-proxy)
  * [Private Integration](#private-integration)
  * [Request Parameters](#request-parameters)
* [WebSocket APIs](#websocket-apis)

  * [Lambda WebSocket Integration](#lambda-websocket-integration)

## HTTP APIs

Integrations connect a route to backend resources. HTTP APIs support Lambda proxy, AWS service, and HTTP proxy integrations. HTTP proxy integrations are also known as private integrations.

### Lambda

Lambda integrations enable integrating an HTTP API route with a Lambda function. When a client invokes the route, the
API Gateway service forwards the request to the Lambda function and returns the function's response to the client.

The API Gateway service will invoke the lambda function with an event payload of a specific format. The service expects
the function to respond in a specific format. The details on this format is available at [Working with AWS Lambda
proxy integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html).

The following code configures a route `GET /books` with a Lambda proxy integration.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

# books_default_fn: lambda.Function

books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### HTTP Proxy

HTTP Proxy integrations enables connecting an HTTP API route to a publicly routable HTTP endpoint. When a client
invokes the route, the API Gateway service forwards the entire request and response between the API Gateway endpoint
and the integrating HTTP endpoint. More information can be found at [Working with HTTP proxy
integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-http.html).

The following code configures a route `GET /books` with an HTTP proxy integration to an HTTP endpoint
`get-books-proxy.myproxy.internal`.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration


books_integration = HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal")

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

The following integrations are supported for private resources in a VPC.

#### Application Load Balancer

The following code is a basic application load balancer private integration of HTTP API:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.ApplicationLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpAlbIntegration`.

#### Network Load Balancer

The following code is a basic network load balancer private integration of HTTP API:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpNlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpNlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpNlbIntegration`.

#### Cloud Map Service Discovery

The following code is a basic discovery service private integration of HTTP API:

```python
import aws_cdk.aws_servicediscovery as servicediscovery
from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration


vpc = ec2.Vpc(self, "VPC")
vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
    name="boobar.com",
    vpc=vpc
)
service = namespace.create_service("Service")

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
        vpc_link=vpc_link
    )
)
```

### Request Parameters

Request parameter mapping allows API requests from clients to be modified before they reach backend integrations.
Parameter mapping can be used to specify modifications to request parameters. See [Transforming API requests and
responses](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html).

The following example creates a new header - `header2` - as a copy of `header1` and removes `header1`.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
    )
)
```

To add mapping keys and values not yet supported by the CDK, use the `custom()` method:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
    )
)
```

## WebSocket APIs

WebSocket integrations connect a route to backend resources. The following integrations are supported in the CDK.

### Lambda WebSocket Integration

Lambda integrations enable integrating a WebSocket API route with a Lambda function. When a client connects/disconnects
or sends message specific to a route, the API Gateway service forwards the request to the Lambda function

The API Gateway service will invoke the lambda function with an event payload of a specific format.

The following code configures a `sendmessage` route with a Lambda integration

```python
from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration

# message_handler: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev",
    auto_deploy=True
)
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_apigatewayv2
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_lambda
import aws_cdk.aws_servicediscovery
import aws_cdk.core


class HttpAlbIntegration(
    aws_cdk.aws_apigatewayv2.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegration",
):
    '''(experimental) The Application Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration
        
        # lb: elbv2.ApplicationLoadBalancer
        
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: aws_cdk.aws_elasticloadbalancingv2.IApplicationListener,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB application listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAlbIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpAlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpAlbIntegration, "_connection_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpAlbIntegration, "_http_method").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpAlbIntegration, "_integration_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpAlbIntegration, "_payload_format_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


class HttpLambdaIntegration(
    aws_cdk.aws_apigatewayv2.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpLambdaIntegration",
):
    '''(experimental) The Lambda Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
        
        # books_default_fn: lambda.Function
        
        books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)
        
        http_api = apigwv2.HttpApi(self, "HttpApi")
        
        http_api.add_routes(
            path="/books",
            methods=[apigwv2.HttpMethod.GET],
            integration=books_integration
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        handler: aws_cdk.aws_lambda.IFunction,
        *,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        payload_format_version: typing.Optional[aws_cdk.aws_apigatewayv2.PayloadFormatVersion] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda handler to integrate with.
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpLambdaIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        props = HttpLambdaIntegrationProps(
            parameter_mapping=parameter_mapping,
            payload_format_version=payload_format_version,
        )

        jsii.create(self.__class__, self, [id, handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))

    @jsii.member(jsii_name="completeBind")
    def _complete_bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> None:
        '''(experimental) Complete the binding of the integration to the route.

        In some cases, there is
        some additional work to do, such as adding permissions for the API to access
        the target. This work is necessary whether the integration has just been
        created for this route or it is an existing one, previously created for other
        routes. In most cases, however, concrete implementations do not need to
        override this method.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "completeBind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpLambdaIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_mapping": "parameterMapping",
        "payload_format_version": "payloadFormatVersion",
    },
)
class HttpLambdaIntegrationProps:
    def __init__(
        self,
        *,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        payload_format_version: typing.Optional[aws_cdk.aws_apigatewayv2.PayloadFormatVersion] = None,
    ) -> None:
        '''(experimental) Lambda Proxy integration properties.

        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # payload_format_version: apigatewayv2.PayloadFormatVersion
            
            http_lambda_integration_props = apigatewayv2_integrations.HttpLambdaIntegrationProps(
                parameter_mapping=parameter_mapping,
                payload_format_version=payload_format_version
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpLambdaIntegrationProps.__init__)
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    @builtins.property
    def payload_format_version(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.PayloadFormatVersion]:
        '''(experimental) Version of the payload sent to the lambda handler.

        :default: PayloadFormatVersion.VERSION_2_0

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.PayloadFormatVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpLambdaIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpNlbIntegration(
    aws_cdk.aws_apigatewayv2.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegration",
):
    '''(experimental) The Network Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpNlbIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpNlbIntegration("DefaultIntegration", listener)
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: aws_cdk.aws_elasticloadbalancingv2.INetworkListener,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB network listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpNlbIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpNlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpNlbIntegration, "_connection_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpNlbIntegration, "_http_method").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpNlbIntegration, "_integration_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpNlbIntegration, "_payload_format_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpPrivateIntegrationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpPrivateIntegrationOptions:
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''(experimental) Base options for private integration.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_private_integration_options = apigatewayv2_integrations.HttpPrivateIntegrationOptions(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpPrivateIntegrationOptions.__init__)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpPrivateIntegrationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpServiceDiscoveryIntegration(
    aws_cdk.aws_apigatewayv2.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegration",
):
    '''(experimental) The Service Discovery integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_servicediscovery as servicediscovery
        from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
        namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
            name="boobar.com",
            vpc=vpc
        )
        service = namespace.create_service("Service")
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                vpc_link=vpc_link
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        service: aws_cdk.aws_servicediscovery.IService,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param service: the service discovery resource to integrate with.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpServiceDiscoveryIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        props = HttpServiceDiscoveryIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, service, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpServiceDiscoveryIntegration, "_connection_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpServiceDiscoveryIntegration, "_http_method").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpServiceDiscoveryIntegration, "_integration_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigatewayv2.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(HttpServiceDiscoveryIntegration, "_payload_format_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpServiceDiscoveryIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpServiceDiscoveryIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_servicediscovery as servicediscovery
            from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
            
            
            vpc = ec2.Vpc(self, "VPC")
            vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
            namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
                name="boobar.com",
                vpc=vpc
            )
            service = namespace.create_service("Service")
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                    vpc_link=vpc_link
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpServiceDiscoveryIntegrationProps.__init__)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpServiceDiscoveryIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpUrlIntegration(
    aws_cdk.aws_apigatewayv2.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpUrlIntegration",
):
    '''(experimental) The HTTP Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_authorizers import HttpLambdaAuthorizer, HttpLambdaResponseType
        from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration
        
        # This function handles your auth logic
        # auth_handler: lambda.Function
        
        
        authorizer = HttpLambdaAuthorizer("BooksAuthorizer", auth_handler,
            response_types=[HttpLambdaResponseType.SIMPLE]
        )
        
        api = apigwv2.HttpApi(self, "HttpApi")
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books",
            authorizer=authorizer
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        url: builtins.str,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param url: the URL to proxy to.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpUrlIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        props = HttpUrlIntegrationProps(
            method=method, parameter_mapping=parameter_mapping
        )

        jsii.create(self.__class__, self, [id, url, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpUrlIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "parameter_mapping": "parameterMapping"},
)
class HttpUrlIntegrationProps:
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new ``HttpProxyIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            
            http_url_integration_props = apigatewayv2_integrations.HttpUrlIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpUrlIntegrationProps.__init__)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpUrlIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketLambdaIntegration(
    aws_cdk.aws_apigatewayv2.WebSocketRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.WebSocketLambdaIntegration",
):
    '''(experimental) Lambda WebSocket Integration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
        
        # message_handler: lambda.Function
        
        
        web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
        apigwv2.WebSocketStage(self, "mystage",
            web_socket_api=web_socket_api,
            stage_name="dev",
            auto_deploy=True
        )
        web_socket_api.add_route("sendmessage",
            integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
        )
    '''

    def __init__(self, id: builtins.str, handler: aws_cdk.aws_lambda.IFunction) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda function handler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketLambdaIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        jsii.create(self.__class__, self, [id, handler])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IWebSocketRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))


class WebSocketMockIntegration(
    aws_cdk.aws_apigatewayv2.WebSocketRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.WebSocketMockIntegration",
):
    '''(experimental) Mock WebSocket Integration.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
        
        web_socket_mock_integration = apigatewayv2_integrations.WebSocketMockIntegration("id")
    '''

    def __init__(self, id: builtins.str) -> None:
        '''
        :param id: id of the underlying integration construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketMockIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IWebSocketRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.WebSocketRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpAlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpAlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration
            
            # lb: elbv2.ApplicationLoadBalancer
            
            listener = lb.add_listener("listener", port=80)
            listener.add_targets("target",
                port=80
            )
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                    parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAlbIntegrationProps.__init__)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpNlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        parameter_mapping: typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpNlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_nlb_integration_props = apigatewayv2_integrations.HttpNlbIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpNlbIntegrationProps.__init__)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpAlbIntegration",
    "HttpAlbIntegrationProps",
    "HttpLambdaIntegration",
    "HttpLambdaIntegrationProps",
    "HttpNlbIntegration",
    "HttpNlbIntegrationProps",
    "HttpPrivateIntegrationOptions",
    "HttpServiceDiscoveryIntegration",
    "HttpServiceDiscoveryIntegrationProps",
    "HttpUrlIntegration",
    "HttpUrlIntegrationProps",
    "WebSocketLambdaIntegration",
    "WebSocketMockIntegration",
]

publication.publish()
