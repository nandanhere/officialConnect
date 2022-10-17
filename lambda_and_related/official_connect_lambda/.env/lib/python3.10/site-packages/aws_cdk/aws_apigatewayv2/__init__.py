'''
# AWS::APIGatewayv2 Construct Library

<!--BEGIN STABILITY BANNER-->---


Features                                   | Stability
-------------------------------------------|--------------------------------------------------------
CFN Resources                              | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge)
Higher level constructs for HTTP APIs      | ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)
Higher level constructs for Websocket APIs | ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always
> stable and safe to use.

<!-- -->

> **Experimental:** Higher level constructs in this module that are marked as experimental are
> under active development. They are subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and
> breaking changes will be announced in the release notes. This means that while you may use them,
> you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [Introduction](#introduction)
* [HTTP API](#http-api)

  * [Defining HTTP APIs](#defining-http-apis)
  * [Cross Origin Resource Sharing (CORS)](#cross-origin-resource-sharing-cors)
  * [Publishing HTTP APIs](#publishing-http-apis)
  * [Custom Domain](#custom-domain)
  * [Mutual TLS](#mutual-tls-mtls)
  * [Managing access to HTTP APIs](#managing-access-to-http-apis)
  * [Metrics](#metrics)
  * [VPC Link](#vpc-link)
  * [Private Integration](#private-integration)
* [WebSocket API](#websocket-api)

  * [Manage Connections Permission](#manage-connections-permission)
  * [Managing access to WebSocket APIs](#managing-access-to-websocket-apis)

## Introduction

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket
APIs at any scale. API developers can create APIs that access AWS or other web services, as well as data stored in the AWS Cloud.
As an API Gateway API developer, you can create APIs for use in your own client applications. Read the
[Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html).

This module supports features under [API Gateway v2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html)
that lets users set up Websocket and HTTP APIs.
REST APIs can be created using the `@aws-cdk/aws-apigateway` module.

## HTTP API

HTTP APIs enable creation of RESTful APIs that integrate with AWS Lambda functions, known as Lambda proxy integration,
or to any routable HTTP endpoint, known as HTTP proxy integration.

### Defining HTTP APIs

HTTP APIs have two fundamental concepts - Routes and Integrations.

Routes direct incoming API requests to backend resources. Routes consist of two parts: an HTTP method and a resource
path, such as, `GET /books`. Learn more at [Working with
routes](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-routes.html). Use the `ANY` method
to match any methods for a route that are not explicitly defined.

Integrations define how the HTTP API responds when a client reaches a specific Route. HTTP APIs support Lambda proxy
integration, HTTP proxy integration and, AWS service integrations, also known as private integrations. Learn more at
[Configuring integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations.html).

Integrations are available at the `aws-apigatewayv2-integrations` module and more information is available in that module.
As an early example, the following code snippet configures a route `GET /books` with an HTTP proxy integration all
configures all other HTTP method calls to `/books` to a lambda proxy.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration, HttpLambdaIntegration

# books_default_fn: lambda.Function


get_books_integration = HttpUrlIntegration("GetBooksIntegration", "https://get-books-proxy.myproxy.internal")
books_default_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=get_books_integration
)
http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.ANY],
    integration=books_default_integration
)
```

The URL to the endpoint can be retrieved via the `apiEndpoint` attribute. By default this URL is enabled for clients. Use `disableExecuteApiEndpoint` to disable it.

```python
http_api = apigwv2.HttpApi(self, "HttpApi",
    disable_execute_api_endpoint=True
)
```

The `defaultIntegration` option while defining HTTP APIs lets you create a default catch-all integration that is
matched when a client reaches a route that is not explicitly defined.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration


apigwv2.HttpApi(self, "HttpProxyApi",
    default_integration=HttpUrlIntegration("DefaultIntegration", "https://example.com")
)
```

### Cross Origin Resource Sharing (CORS)

[Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a browser security
feature that restricts HTTP requests that are initiated from scripts running in the browser. Enabling CORS will allow
requests to your API from a web application hosted in a domain different from your API domain.

When configured CORS for an HTTP API, API Gateway automatically sends a response to preflight `OPTIONS` requests, even
if there isn't an `OPTIONS` route configured. Note that, when this option is used, API Gateway will ignore CORS headers
returned from your backend integration. Learn more about [Configuring CORS for an HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html).

The `corsPreflight` option lets you specify a CORS configuration for an API.

```python
apigwv2.HttpApi(self, "HttpProxyApi",
    cors_preflight=apigwv2.CorsPreflightOptions(
        allow_headers=["Authorization"],
        allow_methods=[apigwv2.CorsHttpMethod.GET, apigwv2.CorsHttpMethod.HEAD, apigwv2.CorsHttpMethod.OPTIONS, apigwv2.CorsHttpMethod.POST
        ],
        allow_origins=["*"],
        max_age=Duration.days(10)
    )
)
```

### Publishing HTTP APIs

A Stage is a logical reference to a lifecycle state of your API (for example, `dev`, `prod`, `beta`, or `v2`). API
stages are identified by their stage name. Each stage is a named reference to a deployment of the API made available for
client applications to call.

Use `HttpStage` to create a Stage resource for HTTP APIs. The following code sets up a Stage, whose URL is available at
`https://{api_id}.execute-api.{region}.amazonaws.com/beta`.

```python
# api: apigwv2.HttpApi


apigwv2.HttpStage(self, "Stage",
    http_api=api,
    stage_name="beta"
)
```

If you omit the `stageName` will create a `$default` stage. A `$default` stage is one that is served from the base of
the API's URL - `https://{api_id}.execute-api.{region}.amazonaws.com/`.

Note that, `HttpApi` will always creates a `$default` stage, unless the `createDefaultStage` property is unset.

### Custom Domain

Custom domain names are simpler and more intuitive URLs that you can provide to your API users. Custom domain name are associated to API stages.

The code snippet below creates a custom domain and configures a default domain mapping for your API that maps the
custom domain to the `$default` stage of the API.

```python
import aws_cdk.aws_certificatemanager as acm
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

# handler: lambda.Function


cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
domain_name = "example.com"

dn = apigwv2.DomainName(self, "DN",
    domain_name=domain_name,
    certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn)
)
api = apigwv2.HttpApi(self, "HttpProxyProdApi",
    default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
    # https://${dn.domainName}/foo goes to prodApi $default stage
    default_domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="foo"
    )
)
```

To migrate a domain endpoint from one type to another, you can add a new endpoint configuration via `addEndpoint()`
and then configure DNS records to route traffic to the new endpoint. After that, you can remove the previous endpoint configuration.
Learn more at [Migrating a custom domain name](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-regional-api-custom-domain-migrate.html)

To associate a specific `Stage` to a custom domain mapping -

```python
# api: apigwv2.HttpApi
# dn: apigwv2.DomainName


api.add_stage("beta",
    stage_name="beta",
    auto_deploy=True,
    # https://${dn.domainName}/bar goes to the beta stage
    domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="bar"
    )
)
```

The same domain name can be associated with stages across different `HttpApi` as so -

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

# handler: lambda.Function
# dn: apigwv2.DomainName


api_demo = apigwv2.HttpApi(self, "DemoApi",
    default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
    # https://${dn.domainName}/demo goes to apiDemo $default stage
    default_domain_mapping=apigwv2.DomainMappingOptions(
        domain_name=dn,
        mapping_key="demo"
    )
)
```

The `mappingKey` determines the base path of the URL with the custom domain. Each custom domain is only allowed
to have one API mapping with undefined `mappingKey`. If more than one API mappings are specified, `mappingKey` will be required for all of them. In the sample above, the custom domain is associated
with 3 API mapping resources across different APIs and Stages.

|        API     |     Stage   |   URL  |
| :------------: | :---------: | :----: |
| api | $default  |   `https://${domainName}/foo`  |
| api | beta  |   `https://${domainName}/bar`  |
| apiDemo | $default  |   `https://${domainName}/demo`  |

You can retrieve the full domain URL with mapping key using the `domainUrl` property as so -

```python
# api_demo: apigwv2.HttpApi

demo_domain_url = api_demo.default_stage.domain_url
```

### Mutual TLS (mTLS)

Mutual TLS can be configured to limit access to your API based by using client certificates instead of (or as an extension of) using authorization headers.

```python
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_certificatemanager as acm
# bucket: s3.Bucket


cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
domain_name = "example.com"

apigwv2.DomainName(self, "DomainName",
    domain_name=domain_name,
    certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn),
    mtls=apigwv2.MTLSConfig(
        bucket=bucket,
        key="someca.pem",
        version="version"
    )
)
```

Instructions for configuring your trust store can be found [here](https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/)

### Managing access to HTTP APIs

API Gateway supports multiple mechanisms for [controlling and managing access to your HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html) through authorizers.

These authorizers can be found in the [APIGatewayV2-Authorizers](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-authorizers-readme.html) constructs library.

### Metrics

The API Gateway v2 service sends metrics around the performance of HTTP APIs to Amazon CloudWatch.
These metrics can be referred to using the metric APIs available on the `HttpApi` construct.
The APIs with the `metric` prefix can be used to get reference to specific metrics for this API. For example,
the method below refers to the client side errors metric for this API.

```python
api = apigwv2.HttpApi(self, "my-api")
client_error_metric = api.metric_client_error()
```

Please note that this will return a metric for all the stages defined in the api. It is also possible to refer to metrics for a specific Stage using
the `metric` methods from the `Stage` construct.

```python
api = apigwv2.HttpApi(self, "my-api")
stage = apigwv2.HttpStage(self, "Stage",
    http_api=api
)
client_error_metric = stage.metric_client_error()
```

### VPC Link

Private integrations let HTTP APIs connect with AWS resources that are placed behind a VPC. These are usually Application
Load Balancers, Network Load Balancers or a Cloud Map service. The `VpcLink` construct enables this integration.
The following code creates a `VpcLink` to a private VPC.

```python
import aws_cdk.aws_ec2 as ec2


vpc = ec2.Vpc(self, "VPC")
vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
```

Any existing `VpcLink` resource can be imported into the CDK app via the `VpcLink.fromVpcLinkAttributes()`.

```python
import aws_cdk.aws_ec2 as ec2

# vpc: ec2.Vpc

awesome_link = apigwv2.VpcLink.from_vpc_link_attributes(self, "awesome-vpc-link",
    vpc_link_id="us-east-1_oiuR12Abd",
    vpc=vpc
)
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

These integrations can be found in the [aws-apigatewayv2-integrations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-integrations-readme.html) constructs library.

## WebSocket API

A WebSocket API in API Gateway is a collection of WebSocket routes that are integrated with backend HTTP endpoints,
Lambda functions, or other AWS services. You can use API Gateway features to help you with all aspects of the API
lifecycle, from creation through monitoring your production APIs. [Read more](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-overview.html)

WebSocket APIs have two fundamental concepts - Routes and Integrations.

WebSocket APIs direct JSON messages to backend integrations based on configured routes. (Non-JSON messages are directed
to the configured `$default` route.)

Integrations define how the WebSocket API behaves when a client reaches a specific Route. Learn more at
[Configuring integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-requests.html).

Integrations are available in the `aws-apigatewayv2-integrations` module and more information is available in that module.

To add the default WebSocket routes supported by API Gateway (`$connect`, `$disconnect` and `$default`), configure them as part of api props:

```python
from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration

# connect_handler: lambda.Function
# disconnect_handler: lambda.Function
# default_handler: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi",
    connect_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("ConnectIntegration", connect_handler)),
    disconnect_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("DisconnectIntegration", disconnect_handler)),
    default_route_options=apigwv2.WebSocketRouteOptions(integration=WebSocketLambdaIntegration("DefaultIntegration", default_handler))
)

apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev",
    auto_deploy=True
)
```

To retrieve a websocket URL and a callback URL:

```python
# web_socket_stage: apigwv2.WebSocketStage


web_socket_uRL = web_socket_stage.url
# wss://${this.api.apiId}.execute-api.${s.region}.${s.urlSuffix}/${urlPath}
callback_uRL = web_socket_stage.callback_url
```

To add any other route:

```python
from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration

# message_handler: lambda.Function

web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
)
```

To import an existing WebSocketApi:

```python
web_socket_api = apigwv2.WebSocketApi.from_web_socket_api_attributes(self, "mywsapi", web_socket_id="api-1234")
```

### Manage Connections Permission

Grant permission to use API Gateway Management API of a WebSocket API by calling the `grantManageConnections` API.
You can use Management API to send a callback message to a connected client, get connection information, or disconnect the client. Learn more at [Use @connections commands in your backend service](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html).

```python
# fn: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
stage = apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev"
)
# per stage permission
stage.grant_management_api_access(fn)
# for all the stages permission
web_socket_api.grant_manage_connections(fn)
```

### Managing access to WebSocket APIs

API Gateway supports multiple mechanisms for [controlling and managing access to a WebSocket API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-control-access.html) through authorizers.

These authorizers can be found in the [APIGatewayV2-Authorizers](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-authorizers-readme.html) constructs library.

### API Keys

Websocket APIs also support usage of API Keys. An API Key is a key that is used to grant access to an API. These are useful for controlling and tracking access to an API, when used together with [usage plans](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). These together allow you to configure controls around API access such as quotas and throttling, along with per-API Key metrics on usage.

To require an API Key when accessing the Websocket API:

```python
web_socket_api = apigwv2.WebSocketApi(self, "mywsapi",
    api_key_selection_expression=apigwv2.WebSocketApiKeySelectionExpression.HEADER_X_API_KEY
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.ApiMappingAttributes",
    jsii_struct_bases=[],
    name_mapping={"api_mapping_id": "apiMappingId"},
)
class ApiMappingAttributes:
    def __init__(self, *, api_mapping_id: builtins.str) -> None:
        '''(experimental) The attributes used to import existing ApiMapping.

        :param api_mapping_id: (experimental) The API mapping ID.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            api_mapping_attributes = apigatewayv2.ApiMappingAttributes(
                api_mapping_id="apiMappingId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApiMappingAttributes.__init__)
            check_type(argname="argument api_mapping_id", value=api_mapping_id, expected_type=type_hints["api_mapping_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_mapping_id": api_mapping_id,
        }

    @builtins.property
    def api_mapping_id(self) -> builtins.str:
        '''(experimental) The API mapping ID.

        :stability: experimental
        '''
        result = self._values.get("api_mapping_id")
        assert result is not None, "Required property 'api_mapping_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiMappingAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.ApiMappingProps",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "domain_name": "domainName",
        "api_mapping_key": "apiMappingKey",
        "stage": "stage",
    },
)
class ApiMappingProps:
    def __init__(
        self,
        *,
        api: "IApi",
        domain_name: "IDomainName",
        api_mapping_key: typing.Optional[builtins.str] = None,
        stage: typing.Optional["IStage"] = None,
    ) -> None:
        '''(experimental) Properties used to create the ApiMapping resource.

        :param api: (experimental) The Api to which this mapping is applied.
        :param domain_name: (experimental) custom domain name of the mapping target.
        :param api_mapping_key: (experimental) Api mapping key. The path where this stage should be mapped to on the domain Default: - undefined for the root path mapping.
        :param stage: (experimental) stage for the ApiMapping resource required for WebSocket API defaults to default stage of an HTTP API. Default: - Default stage of the passed API for HTTP API, required for WebSocket API

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # api: apigatewayv2.IApi
            # domain_name: apigatewayv2.DomainName
            # stage: apigatewayv2.IStage
            
            api_mapping_props = apigatewayv2.ApiMappingProps(
                api=api,
                domain_name=domain_name,
            
                # the properties below are optional
                api_mapping_key="apiMappingKey",
                stage=stage
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApiMappingProps.__init__)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument api_mapping_key", value=api_mapping_key, expected_type=type_hints["api_mapping_key"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[str, typing.Any] = {
            "api": api,
            "domain_name": domain_name,
        }
        if api_mapping_key is not None:
            self._values["api_mapping_key"] = api_mapping_key
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def api(self) -> "IApi":
        '''(experimental) The Api to which this mapping is applied.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast("IApi", result)

    @builtins.property
    def domain_name(self) -> "IDomainName":
        '''(experimental) custom domain name of the mapping target.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast("IDomainName", result)

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) Api mapping key.

        The path where this stage should be mapped to on the domain

        :default: - undefined for the root path mapping.

        :stability: experimental
        '''
        result = self._values.get("api_mapping_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional["IStage"]:
        '''(experimental) stage for the ApiMapping resource required for WebSocket API defaults to default stage of an HTTP API.

        :default: - Default stage of the passed API for HTTP API, required for WebSocket API

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional["IStage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiMappingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.AuthorizerPayloadVersion")
class AuthorizerPayloadVersion(enum.Enum):
    '''(experimental) Payload format version for lambda authorizers.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    :stability: experimental
    '''

    VERSION_1_0 = "VERSION_1_0"
    '''(experimental) Version 1.0.

    :stability: experimental
    '''
    VERSION_2_0 = "VERSION_2_0"
    '''(experimental) Version 2.0.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.BatchHttpRouteOptions",
    jsii_struct_bases=[],
    name_mapping={"integration": "integration"},
)
class BatchHttpRouteOptions:
    def __init__(self, *, integration: "HttpRouteIntegration") -> None:
        '''(experimental) Options used when configuring multiple routes, at once.

        The options here are the ones that would be configured for all being set up.

        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # http_route_integration: apigatewayv2.HttpRouteIntegration
            
            batch_http_route_options = apigatewayv2.BatchHttpRouteOptions(
                integration=http_route_integration
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BatchHttpRouteOptions.__init__)
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
        }

    @builtins.property
    def integration(self) -> "HttpRouteIntegration":
        '''(experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return typing.cast("HttpRouteIntegration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchHttpRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApi(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Api``.

    The ``AWS::ApiGatewayV2::Api`` resource creates an API. WebSocket APIs and HTTP APIs are supported. For more information about WebSocket APIs, see `About WebSocket APIs in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-overview.html>`_ in the *API Gateway Developer Guide* . For more information about HTTP APIs, see `HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html>`_ in the *API Gateway Developer Guide.*

    :cloudformationResource: AWS::ApiGatewayV2::Api
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # body: Any
        # tags: Any
        
        cfn_api = apigatewayv2.CfnApi(self, "MyCfnApi",
            api_key_selection_expression="apiKeySelectionExpression",
            base_path="basePath",
            body=body,
            body_s3_location=apigatewayv2.CfnApi.BodyS3LocationProperty(
                bucket="bucket",
                etag="etag",
                key="key",
                version="version"
            ),
            cors_configuration=apigatewayv2.CfnApi.CorsProperty(
                allow_credentials=False,
                allow_headers=["allowHeaders"],
                allow_methods=["allowMethods"],
                allow_origins=["allowOrigins"],
                expose_headers=["exposeHeaders"],
                max_age=123
            ),
            credentials_arn="credentialsArn",
            description="description",
            disable_execute_api_endpoint=False,
            disable_schema_validation=False,
            fail_on_warnings=False,
            name="name",
            protocol_type="protocolType",
            route_key="routeKey",
            route_selection_expression="routeSelectionExpression",
            tags=tags,
            target="target",
            version="version"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_key_selection_expression: typing.Optional[builtins.str] = None,
        base_path: typing.Optional[builtins.str] = None,
        body: typing.Any = None,
        body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApi.BodyS3LocationProperty", typing.Dict[str, typing.Any]]]] = None,
        cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApi.CorsProperty", typing.Dict[str, typing.Any]]]] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        disable_schema_validation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        target: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key_selection_expression: An API key selection expression. Supported only for WebSocket APIs. See `API Key Selection Expressions <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-selection-expressions.html#apigateway-websocket-api-apikey-selection-expressions>`_ .
        :param base_path: Specifies how to interpret the base path of the API during import. Valid values are ``ignore`` , ``prepend`` , and ``split`` . The default value is ``ignore`` . To learn more, see `Set the OpenAPI basePath Property <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-basePath.html>`_ . Supported only for HTTP APIs.
        :param body: The OpenAPI definition. Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.
        :param body_s3_location: The S3 location of an OpenAPI definition. Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.
        :param cors_configuration: A CORS configuration. Supported only for HTTP APIs. See `Configuring CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`_ for more information.
        :param credentials_arn: This property is part of quick create. It specifies the credentials required for the integration, if any. For a Lambda integration, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, specify ``null`` . Currently, this property is not used for HTTP integrations. Supported only for HTTP APIs.
        :param description: The description of the API.
        :param disable_execute_api_endpoint: Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint. By default, clients can invoke your API with the default https://{api_id}.execute-api.{region}.amazonaws.com endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint.
        :param disable_schema_validation: Avoid validating models when creating a deployment. Supported only for WebSocket APIs.
        :param fail_on_warnings: Specifies whether to rollback the API creation when a warning is encountered. By default, API creation continues if a warning is encountered.
        :param name: The name of the API. Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .
        :param protocol_type: The API protocol. Valid values are ``WEBSOCKET`` or ``HTTP`` . Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .
        :param route_key: This property is part of quick create. If you don't specify a ``routeKey`` , a default route of ``$default`` is created. The ``$default`` route acts as a catch-all for any request made to your API, for a particular stage. The ``$default`` route key can't be modified. You can add routes after creating the API, and you can update the route keys of additional routes. Supported only for HTTP APIs.
        :param route_selection_expression: The route selection expression for the API. For HTTP APIs, the ``routeSelectionExpression`` must be ``${request.method} ${request.path}`` . If not provided, this will be the default for HTTP APIs. This property is required for WebSocket APIs.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        :param target: This property is part of quick create. Quick create produces an API with an integration, a default catch-all route, and a default stage which is configured to automatically deploy changes. For HTTP integrations, specify a fully qualified URL. For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively. Supported only for HTTP APIs.
        :param version: A version identifier for the API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApi.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiProps(
            api_key_selection_expression=api_key_selection_expression,
            base_path=base_path,
            body=body,
            body_s3_location=body_s3_location,
            cors_configuration=cors_configuration,
            credentials_arn=credentials_arn,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            disable_schema_validation=disable_schema_validation,
            fail_on_warnings=fail_on_warnings,
            name=name,
            protocol_type=protocol_type,
            route_key=route_key,
            route_selection_expression=route_selection_expression,
            tags=tags,
            target=target,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApi.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApi._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApiEndpoint")
    def attr_api_endpoint(self) -> builtins.str:
        '''The default endpoint for an API.

        For example: ``https://abcdef.execute-api.us-west-2.amazonaws.com`` .

        :cloudformationAttribute: ApiEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Any:
        '''The OpenAPI definition.

        Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        '''
        return typing.cast(typing.Any, jsii.get(self, "body"))

    @body.setter
    def body(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "body").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeySelectionExpression")
    def api_key_selection_expression(self) -> typing.Optional[builtins.str]:
        '''An API key selection expression.

        Supported only for WebSocket APIs. See `API Key Selection Expressions <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-selection-expressions.html#apigateway-websocket-api-apikey-selection-expressions>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySelectionExpression"))

    @api_key_selection_expression.setter
    def api_key_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "api_key_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> typing.Optional[builtins.str]:
        '''Specifies how to interpret the base path of the API during import.

        Valid values are ``ignore`` , ``prepend`` , and ``split`` . The default value is ``ignore`` . To learn more, see `Set the OpenAPI basePath Property <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-basePath.html>`_ . Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basePath"))

    @base_path.setter
    def base_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "base_path").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basePath", value)

    @builtins.property
    @jsii.member(jsii_name="bodyS3Location")
    def body_s3_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]]:
        '''The S3 location of an OpenAPI definition.

        Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]], jsii.get(self, "bodyS3Location"))

    @body_s3_location.setter
    def body_s3_location(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "body_s3_location").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]]:
        '''A CORS configuration.

        Supported only for HTTP APIs. See `Configuring CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]], jsii.get(self, "corsConfiguration"))

    @cors_configuration.setter
    def cors_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "cors_configuration").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        It specifies the credentials required for the integration, if any. For a Lambda integration, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, specify ``null`` . Currently, this property is not used for HTTP integrations. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsArn"))

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "credentials_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint.

        By default, clients can invoke your API with the default https://{api_id}.execute-api.{region}.amazonaws.com endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableexecuteapiendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "disableExecuteApiEndpoint"))

    @disable_execute_api_endpoint.setter
    def disable_execute_api_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "disable_execute_api_endpoint").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="disableSchemaValidation")
    def disable_schema_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Avoid validating models when creating a deployment.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "disableSchemaValidation"))

    @disable_schema_validation.setter
    def disable_schema_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "disable_schema_validation").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSchemaValidation", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether to rollback the API creation when a warning is encountered.

        By default, API creation continues if a warning is encountered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "failOnWarnings"))

    @fail_on_warnings.setter
    def fail_on_warnings(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "fail_on_warnings").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the API.

        Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''The API protocol.

        Valid values are ``WEBSOCKET`` or ``HTTP`` . Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "protocol_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        If you don't specify a ``routeKey`` , a default route of ``$default`` is created. The ``$default`` route acts as a catch-all for any request made to your API, for a particular stage. The ``$default`` route key can't be modified. You can add routes after creating the API, and you can update the route keys of additional routes. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeKey"))

    @route_key.setter
    def route_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "route_key").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="routeSelectionExpression")
    def route_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The route selection expression for the API.

        For HTTP APIs, the ``routeSelectionExpression`` must be ``${request.method} ${request.path}`` . If not provided, this will be the default for HTTP APIs. This property is required for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeSelectionExpression"))

    @route_selection_expression.setter
    def route_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "route_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        Quick create produces an API with an integration, a default catch-all route, and a default stage which is configured to automatically deploy changes. For HTTP integrations, specify a fully qualified URL. For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "target"))

    @target.setter
    def target(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "target").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        '''A version identifier for the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))

    @version.setter
    def version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApi, "version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.BodyS3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "etag": "etag",
            "key": "key",
            "version": "version",
        },
    )
    class BodyS3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            etag: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``BodyS3Location`` property specifies an S3 location from which to import an OpenAPI definition.

            Supported only for HTTP APIs.

            :param bucket: The S3 bucket that contains the OpenAPI definition to import. Required if you specify a ``BodyS3Location`` for an API.
            :param etag: The Etag of the S3 object.
            :param key: The key of the S3 object. Required if you specify a ``BodyS3Location`` for an API.
            :param version: The version of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                body_s3_location_property = apigatewayv2.CfnApi.BodyS3LocationProperty(
                    bucket="bucket",
                    etag="etag",
                    key="key",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApi.BodyS3LocationProperty.__init__)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if etag is not None:
                self._values["etag"] = etag
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket that contains the OpenAPI definition to import.

            Required if you specify a ``BodyS3Location`` for an API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def etag(self) -> typing.Optional[builtins.str]:
            '''The Etag of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-etag
            '''
            result = self._values.get("etag")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the S3 object.

            Required if you specify a ``BodyS3Location`` for an API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BodyS3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.CorsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origins": "allowOrigins",
            "expose_headers": "exposeHeaders",
            "max_age": "maxAge",
        },
    )
    class CorsProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``Cors`` property specifies a CORS configuration for an API.

            Supported only for HTTP APIs. See `Configuring CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`_ for more information.

            :param allow_credentials: Specifies whether credentials are included in the CORS request. Supported only for HTTP APIs.
            :param allow_headers: Represents a collection of allowed headers. Supported only for HTTP APIs.
            :param allow_methods: Represents a collection of allowed HTTP methods. Supported only for HTTP APIs.
            :param allow_origins: Represents a collection of allowed origins. Supported only for HTTP APIs.
            :param expose_headers: Represents a collection of exposed headers. Supported only for HTTP APIs.
            :param max_age: The number of seconds that the browser should cache preflight request results. Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                cors_property = apigatewayv2.CfnApi.CorsProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApi.CorsProperty.__init__)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
                check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origins is not None:
                self._values["allow_origins"] = allow_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether credentials are included in the CORS request.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowcredentials
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a collection of allowed headers.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowheaders
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a collection of allowed HTTP methods.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowmethods
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a collection of allowed origins.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-alloworigins
            '''
            result = self._values.get("allow_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents a collection of exposed headers.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-exposeheaders
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds that the browser should cache preflight request results.

            Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiGatewayManagedOverrides(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides``.

    The ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides`` resource overrides the default properties of API Gateway-managed resources that are implicitly configured for you when you use quick create. When you create an API by using quick create, an ``AWS::ApiGatewayV2::Route`` , ``AWS::ApiGatewayV2::Integration`` , and ``AWS::ApiGatewayV2::Stage`` are created for you and associated with your ``AWS::ApiGatewayV2::Api`` . The ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides`` resource enables you to set, or override the properties of these implicit resources. Supported only for HTTP APIs.

    :cloudformationResource: AWS::ApiGatewayV2::ApiGatewayManagedOverrides
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # route_settings: Any
        # stage_variables: Any
        
        cfn_api_gateway_managed_overrides = apigatewayv2.CfnApiGatewayManagedOverrides(self, "MyCfnApiGatewayManagedOverrides",
            api_id="apiId",
        
            # the properties below are optional
            integration=apigatewayv2.CfnApiGatewayManagedOverrides.IntegrationOverridesProperty(
                description="description",
                integration_method="integrationMethod",
                payload_format_version="payloadFormatVersion",
                timeout_in_millis=123
            ),
            route=apigatewayv2.CfnApiGatewayManagedOverrides.RouteOverridesProperty(
                authorization_scopes=["authorizationScopes"],
                authorization_type="authorizationType",
                authorizer_id="authorizerId",
                operation_name="operationName",
                target="target"
            ),
            stage=apigatewayv2.CfnApiGatewayManagedOverrides.StageOverridesProperty(
                access_log_settings=apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auto_deploy=False,
                default_route_settings=apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                description="description",
                route_settings=route_settings,
                stage_variables=stage_variables
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApiGatewayManagedOverrides.IntegrationOverridesProperty", typing.Dict[str, typing.Any]]]] = None,
        route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApiGatewayManagedOverrides.RouteOverridesProperty", typing.Dict[str, typing.Any]]]] = None,
        stage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApiGatewayManagedOverrides.StageOverridesProperty", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The ID of the API for which to override the configuration of API Gateway-managed resources.
        :param integration: Overrides the integration configuration for an API Gateway-managed integration.
        :param route: Overrides the route configuration for an API Gateway-managed route.
        :param stage: Overrides the stage configuration for an API Gateway-managed stage.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiGatewayManagedOverridesProps(
            api_id=api_id, integration=integration, route=route, stage=stage
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The ID of the API for which to override the configuration of API Gateway-managed resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiGatewayManagedOverrides, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integration")
    def integration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.IntegrationOverridesProperty"]]:
        '''Overrides the integration configuration for an API Gateway-managed integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.IntegrationOverridesProperty"]], jsii.get(self, "integration"))

    @integration.setter
    def integration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.IntegrationOverridesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiGatewayManagedOverrides, "integration").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integration", value)

    @builtins.property
    @jsii.member(jsii_name="route")
    def route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]]:
        '''Overrides the route configuration for an API Gateway-managed route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-route
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]], jsii.get(self, "route"))

    @route.setter
    def route(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiGatewayManagedOverrides, "route").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "route", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]]:
        '''Overrides the stage configuration for an API Gateway-managed stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stage
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]], jsii.get(self, "stage"))

    @stage.setter
    def stage(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiGatewayManagedOverrides, "stage").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingsProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AccessLogSettings`` property overrides the access log settings for an API Gateway-managed stage.

            :param destination_arn: The ARN of the CloudWatch Logs log group to receive access logs.
            :param format: A single line format of the access logs of data, as specified by selected $context variables. The format must include at least $context.requestId.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                access_log_settings_property = apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.AccessLogSettingsProperty.__init__)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch Logs log group to receive access logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''A single line format of the access logs of data, as specified by selected $context variables.

            The format must include at least $context.requestId.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.IntegrationOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "integration_method": "integrationMethod",
            "payload_format_version": "payloadFormatVersion",
            "timeout_in_millis": "timeoutInMillis",
        },
    )
    class IntegrationOverridesProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            integration_method: typing.Optional[builtins.str] = None,
            payload_format_version: typing.Optional[builtins.str] = None,
            timeout_in_millis: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``IntegrationOverrides`` property overrides the integration settings for an API Gateway-managed integration.

            If you remove this property, API Gateway restores the default values.

            :param description: The description of the integration.
            :param integration_method: Specifies the integration's HTTP method type.
            :param payload_format_version: Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .
            :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                integration_overrides_property = apigatewayv2.CfnApiGatewayManagedOverrides.IntegrationOverridesProperty(
                    description="description",
                    integration_method="integrationMethod",
                    payload_format_version="payloadFormatVersion",
                    timeout_in_millis=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.__init__)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument integration_method", value=integration_method, expected_type=type_hints["integration_method"])
                check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
                check_type(argname="argument timeout_in_millis", value=timeout_in_millis, expected_type=type_hints["timeout_in_millis"])
            self._values: typing.Dict[str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if integration_method is not None:
                self._values["integration_method"] = integration_method
            if payload_format_version is not None:
                self._values["payload_format_version"] = payload_format_version
            if timeout_in_millis is not None:
                self._values["timeout_in_millis"] = timeout_in_millis

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the integration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integration_method(self) -> typing.Optional[builtins.str]:
            '''Specifies the integration's HTTP method type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-integrationmethod
            '''
            result = self._values.get("integration_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload_format_version(self) -> typing.Optional[builtins.str]:
            '''Specifies the format of the payload sent to an integration.

            Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-payloadformatversion
            '''
            result = self._values.get("payload_format_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            '''Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs.

            The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-timeoutinmillis
            '''
            result = self._values.get("timeout_in_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.RouteOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_scopes": "authorizationScopes",
            "authorization_type": "authorizationType",
            "authorizer_id": "authorizerId",
            "operation_name": "operationName",
            "target": "target",
        },
    )
    class RouteOverridesProperty:
        def __init__(
            self,
            *,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorization_type: typing.Optional[builtins.str] = None,
            authorizer_id: typing.Optional[builtins.str] = None,
            operation_name: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``RouteOverrides`` property overrides the route configuration for an API Gateway-managed route.

            If you remove this property, API Gateway restores the default values.

            :param authorization_scopes: The authorization scopes supported by this route.
            :param authorization_type: The authorization type for the route. To learn more, see `AuthorizationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype>`_ .
            :param authorizer_id: The identifier of the ``Authorizer`` resource to be associated with this route. The authorizer identifier is generated by API Gateway when you created the authorizer.
            :param operation_name: The operation name for the route.
            :param target: For HTTP integrations, specify a fully qualified URL. For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                route_overrides_property = apigatewayv2.CfnApiGatewayManagedOverrides.RouteOverridesProperty(
                    authorization_scopes=["authorizationScopes"],
                    authorization_type="authorizationType",
                    authorizer_id="authorizerId",
                    operation_name="operationName",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.RouteOverridesProperty.__init__)
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
                check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
                check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[str, typing.Any] = {}
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorization_type is not None:
                self._values["authorization_type"] = authorization_type
            if authorizer_id is not None:
                self._values["authorizer_id"] = authorizer_id
            if operation_name is not None:
                self._values["operation_name"] = operation_name
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The authorization scopes supported by this route.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizationscopes
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorization_type(self) -> typing.Optional[builtins.str]:
            '''The authorization type for the route.

            To learn more, see `AuthorizationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizationtype
            '''
            result = self._values.get("authorization_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def authorizer_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the ``Authorizer`` resource to be associated with this route.

            The authorizer identifier is generated by API Gateway when you created the authorizer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizerid
            '''
            result = self._values.get("authorizer_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation_name(self) -> typing.Optional[builtins.str]:
            '''The operation name for the route.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-operationname
            '''
            result = self._values.get("operation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''For HTTP integrations, specify a fully qualified URL.

            For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``RouteSettings`` property overrides the route settings for an API Gateway-managed route.

            :param data_trace_enabled: Specifies whether ( ``true`` ) or not ( ``false`` ) data trace logging is enabled for this route. This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.
            :param detailed_metrics_enabled: Specifies whether detailed metrics are enabled.
            :param logging_level: Specifies the logging level for this route: ``INFO`` , ``ERROR`` , or ``OFF`` . This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.
            :param throttling_burst_limit: Specifies the throttling burst limit.
            :param throttling_rate_limit: Specifies the throttling rate limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                route_settings_property = apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.RouteSettingsProperty.__init__)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether ( ``true`` ) or not ( ``false`` ) data trace logging is enabled for this route.

            This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether detailed metrics are enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the logging level for this route: ``INFO`` , ``ERROR`` , or ``OFF`` .

            This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling burst limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling rate limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.StageOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_log_settings": "accessLogSettings",
            "auto_deploy": "autoDeploy",
            "default_route_settings": "defaultRouteSettings",
            "description": "description",
            "route_settings": "routeSettings",
            "stage_variables": "stageVariables",
        },
    )
    class StageOverridesProperty:
        def __init__(
            self,
            *,
            access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApiGatewayManagedOverrides.AccessLogSettingsProperty", typing.Dict[str, typing.Any]]]] = None,
            auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnApiGatewayManagedOverrides.RouteSettingsProperty", typing.Dict[str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            route_settings: typing.Any = None,
            stage_variables: typing.Any = None,
        ) -> None:
            '''The ``StageOverrides`` property overrides the stage configuration for an API Gateway-managed stage.

            If you remove this property, API Gateway restores the default values.

            :param access_log_settings: Settings for logging access in a stage.
            :param auto_deploy: Specifies whether updates to an API automatically trigger a new deployment. The default value is ``true`` .
            :param default_route_settings: The default route settings for the stage.
            :param description: The description for the API stage.
            :param route_settings: Route settings for the stage.
            :param stage_variables: A map that defines the stage variables for a ``Stage`` . Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                # route_settings: Any
                # stage_variables: Any
                
                stage_overrides_property = apigatewayv2.CfnApiGatewayManagedOverrides.StageOverridesProperty(
                    access_log_settings=apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty(
                        destination_arn="destinationArn",
                        format="format"
                    ),
                    auto_deploy=False,
                    default_route_settings=apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty(
                        data_trace_enabled=False,
                        detailed_metrics_enabled=False,
                        logging_level="loggingLevel",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    ),
                    description="description",
                    route_settings=route_settings,
                    stage_variables=stage_variables
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnApiGatewayManagedOverrides.StageOverridesProperty.__init__)
                check_type(argname="argument access_log_settings", value=access_log_settings, expected_type=type_hints["access_log_settings"])
                check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
                check_type(argname="argument default_route_settings", value=default_route_settings, expected_type=type_hints["default_route_settings"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
                check_type(argname="argument stage_variables", value=stage_variables, expected_type=type_hints["stage_variables"])
            self._values: typing.Dict[str, typing.Any] = {}
            if access_log_settings is not None:
                self._values["access_log_settings"] = access_log_settings
            if auto_deploy is not None:
                self._values["auto_deploy"] = auto_deploy
            if default_route_settings is not None:
                self._values["default_route_settings"] = default_route_settings
            if description is not None:
                self._values["description"] = description
            if route_settings is not None:
                self._values["route_settings"] = route_settings
            if stage_variables is not None:
                self._values["stage_variables"] = stage_variables

        @builtins.property
        def access_log_settings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.AccessLogSettingsProperty"]]:
            '''Settings for logging access in a stage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-accesslogsettings
            '''
            result = self._values.get("access_log_settings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.AccessLogSettingsProperty"]], result)

        @builtins.property
        def auto_deploy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether updates to an API automatically trigger a new deployment.

            The default value is ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-autodeploy
            '''
            result = self._values.get("auto_deploy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def default_route_settings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteSettingsProperty"]]:
            '''The default route settings for the stage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-defaultroutesettings
            '''
            result = self._values.get("default_route_settings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteSettingsProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description for the API stage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route_settings(self) -> typing.Any:
            '''Route settings for the stage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-routesettings
            '''
            result = self._values.get("route_settings")
            return typing.cast(typing.Any, result)

        @builtins.property
        def stage_variables(self) -> typing.Any:
            '''A map that defines the stage variables for a ``Stage`` .

            Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-stagevariables
            '''
            result = self._values.get("stage_variables")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverridesProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration": "integration",
        "route": "route",
        "stage": "stage",
    },
)
class CfnApiGatewayManagedOverridesProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnApiGatewayManagedOverrides.IntegrationOverridesProperty, typing.Dict[str, typing.Any]]]] = None,
        route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnApiGatewayManagedOverrides.RouteOverridesProperty, typing.Dict[str, typing.Any]]]] = None,
        stage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnApiGatewayManagedOverrides.StageOverridesProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApiGatewayManagedOverrides``.

        :param api_id: The ID of the API for which to override the configuration of API Gateway-managed resources.
        :param integration: Overrides the integration configuration for an API Gateway-managed integration.
        :param route: Overrides the route configuration for an API Gateway-managed route.
        :param stage: Overrides the stage configuration for an API Gateway-managed stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # route_settings: Any
            # stage_variables: Any
            
            cfn_api_gateway_managed_overrides_props = apigatewayv2.CfnApiGatewayManagedOverridesProps(
                api_id="apiId",
            
                # the properties below are optional
                integration=apigatewayv2.CfnApiGatewayManagedOverrides.IntegrationOverridesProperty(
                    description="description",
                    integration_method="integrationMethod",
                    payload_format_version="payloadFormatVersion",
                    timeout_in_millis=123
                ),
                route=apigatewayv2.CfnApiGatewayManagedOverrides.RouteOverridesProperty(
                    authorization_scopes=["authorizationScopes"],
                    authorization_type="authorizationType",
                    authorizer_id="authorizerId",
                    operation_name="operationName",
                    target="target"
                ),
                stage=apigatewayv2.CfnApiGatewayManagedOverrides.StageOverridesProperty(
                    access_log_settings=apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty(
                        destination_arn="destinationArn",
                        format="format"
                    ),
                    auto_deploy=False,
                    default_route_settings=apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty(
                        data_trace_enabled=False,
                        detailed_metrics_enabled=False,
                        logging_level="loggingLevel",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    ),
                    description="description",
                    route_settings=route_settings,
                    stage_variables=stage_variables
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiGatewayManagedOverridesProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
        }
        if integration is not None:
            self._values["integration"] = integration
        if route is not None:
            self._values["route"] = route
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The ID of the API for which to override the configuration of API Gateway-managed resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.IntegrationOverridesProperty]]:
        '''Overrides the integration configuration for an API Gateway-managed integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integration
        '''
        result = self._values.get("integration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.IntegrationOverridesProperty]], result)

    @builtins.property
    def route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.RouteOverridesProperty]]:
        '''Overrides the route configuration for an API Gateway-managed route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-route
        '''
        result = self._values.get("route")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.RouteOverridesProperty]], result)

    @builtins.property
    def stage(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.StageOverridesProperty]]:
        '''Overrides the stage configuration for an API Gateway-managed stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.StageOverridesProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiGatewayManagedOverridesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiMapping(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMapping",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::ApiMapping``.

    The ``AWS::ApiGatewayV2::ApiMapping`` resource contains an API mapping. An API mapping relates a path of your custom domain name to a stage of your API. A custom domain name can have multiple API mappings, but the paths can't overlap. A custom domain can map only to APIs of the same protocol type. For more information, see `CreateApiMapping <https://docs.aws.amazon.com/apigatewayv2/latest/api-reference/domainnames-domainname-apimappings.html#CreateApiMapping>`_ in the *Amazon API Gateway V2 API Reference* .

    :cloudformationResource: AWS::ApiGatewayV2::ApiMapping
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        cfn_api_mapping = apigatewayv2.CfnApiMapping(self, "MyCfnApiMapping",
            api_id="apiId",
            domain_name="domainName",
            stage="stage",
        
            # the properties below are optional
            api_mapping_key="apiMappingKey"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        domain_name: builtins.str,
        stage: builtins.str,
        api_mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::ApiMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The identifier of the API.
        :param domain_name: The domain name.
        :param stage: The API stage.
        :param api_mapping_key: The API mapping key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiMapping.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiMappingProps(
            api_id=api_id,
            domain_name=domain_name,
            stage=stage,
            api_mapping_key=api_mapping_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiMapping.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiMapping._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The identifier of the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiMapping, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiMapping, "domain_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        '''The API stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        '''
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiMapping, "stage").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)

    @builtins.property
    @jsii.member(jsii_name="apiMappingKey")
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        '''The API mapping key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiMappingKey"))

    @api_mapping_key.setter
    def api_mapping_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnApiMapping, "api_mapping_key").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiMappingKey", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMappingProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "domain_name": "domainName",
        "stage": "stage",
        "api_mapping_key": "apiMappingKey",
    },
)
class CfnApiMappingProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        domain_name: builtins.str,
        stage: builtins.str,
        api_mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApiMapping``.

        :param api_id: The identifier of the API.
        :param domain_name: The domain name.
        :param stage: The API stage.
        :param api_mapping_key: The API mapping key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            cfn_api_mapping_props = apigatewayv2.CfnApiMappingProps(
                api_id="apiId",
                domain_name="domainName",
                stage="stage",
            
                # the properties below are optional
                api_mapping_key="apiMappingKey"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiMappingProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument api_mapping_key", value=api_mapping_key, expected_type=type_hints["api_mapping_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "domain_name": domain_name,
            "stage": stage,
        }
        if api_mapping_key is not None:
            self._values["api_mapping_key"] = api_mapping_key

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The identifier of the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''The API stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        '''The API mapping key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        '''
        result = self._values.get("api_mapping_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiMappingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_selection_expression": "apiKeySelectionExpression",
        "base_path": "basePath",
        "body": "body",
        "body_s3_location": "bodyS3Location",
        "cors_configuration": "corsConfiguration",
        "credentials_arn": "credentialsArn",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "disable_schema_validation": "disableSchemaValidation",
        "fail_on_warnings": "failOnWarnings",
        "name": "name",
        "protocol_type": "protocolType",
        "route_key": "routeKey",
        "route_selection_expression": "routeSelectionExpression",
        "tags": "tags",
        "target": "target",
        "version": "version",
    },
)
class CfnApiProps:
    def __init__(
        self,
        *,
        api_key_selection_expression: typing.Optional[builtins.str] = None,
        base_path: typing.Optional[builtins.str] = None,
        body: typing.Any = None,
        body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnApi.BodyS3LocationProperty, typing.Dict[str, typing.Any]]]] = None,
        cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnApi.CorsProperty, typing.Dict[str, typing.Any]]]] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        disable_schema_validation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        target: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApi``.

        :param api_key_selection_expression: An API key selection expression. Supported only for WebSocket APIs. See `API Key Selection Expressions <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-selection-expressions.html#apigateway-websocket-api-apikey-selection-expressions>`_ .
        :param base_path: Specifies how to interpret the base path of the API during import. Valid values are ``ignore`` , ``prepend`` , and ``split`` . The default value is ``ignore`` . To learn more, see `Set the OpenAPI basePath Property <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-basePath.html>`_ . Supported only for HTTP APIs.
        :param body: The OpenAPI definition. Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.
        :param body_s3_location: The S3 location of an OpenAPI definition. Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.
        :param cors_configuration: A CORS configuration. Supported only for HTTP APIs. See `Configuring CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`_ for more information.
        :param credentials_arn: This property is part of quick create. It specifies the credentials required for the integration, if any. For a Lambda integration, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, specify ``null`` . Currently, this property is not used for HTTP integrations. Supported only for HTTP APIs.
        :param description: The description of the API.
        :param disable_execute_api_endpoint: Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint. By default, clients can invoke your API with the default https://{api_id}.execute-api.{region}.amazonaws.com endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint.
        :param disable_schema_validation: Avoid validating models when creating a deployment. Supported only for WebSocket APIs.
        :param fail_on_warnings: Specifies whether to rollback the API creation when a warning is encountered. By default, API creation continues if a warning is encountered.
        :param name: The name of the API. Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .
        :param protocol_type: The API protocol. Valid values are ``WEBSOCKET`` or ``HTTP`` . Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .
        :param route_key: This property is part of quick create. If you don't specify a ``routeKey`` , a default route of ``$default`` is created. The ``$default`` route acts as a catch-all for any request made to your API, for a particular stage. The ``$default`` route key can't be modified. You can add routes after creating the API, and you can update the route keys of additional routes. Supported only for HTTP APIs.
        :param route_selection_expression: The route selection expression for the API. For HTTP APIs, the ``routeSelectionExpression`` must be ``${request.method} ${request.path}`` . If not provided, this will be the default for HTTP APIs. This property is required for WebSocket APIs.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        :param target: This property is part of quick create. Quick create produces an API with an integration, a default catch-all route, and a default stage which is configured to automatically deploy changes. For HTTP integrations, specify a fully qualified URL. For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively. Supported only for HTTP APIs.
        :param version: A version identifier for the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # body: Any
            # tags: Any
            
            cfn_api_props = apigatewayv2.CfnApiProps(
                api_key_selection_expression="apiKeySelectionExpression",
                base_path="basePath",
                body=body,
                body_s3_location=apigatewayv2.CfnApi.BodyS3LocationProperty(
                    bucket="bucket",
                    etag="etag",
                    key="key",
                    version="version"
                ),
                cors_configuration=apigatewayv2.CfnApi.CorsProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                ),
                credentials_arn="credentialsArn",
                description="description",
                disable_execute_api_endpoint=False,
                disable_schema_validation=False,
                fail_on_warnings=False,
                name="name",
                protocol_type="protocolType",
                route_key="routeKey",
                route_selection_expression="routeSelectionExpression",
                tags=tags,
                target="target",
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnApiProps.__init__)
            check_type(argname="argument api_key_selection_expression", value=api_key_selection_expression, expected_type=type_hints["api_key_selection_expression"])
            check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument body_s3_location", value=body_s3_location, expected_type=type_hints["body_s3_location"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument credentials_arn", value=credentials_arn, expected_type=type_hints["credentials_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument disable_schema_validation", value=disable_schema_validation, expected_type=type_hints["disable_schema_validation"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument route_selection_expression", value=route_selection_expression, expected_type=type_hints["route_selection_expression"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if api_key_selection_expression is not None:
            self._values["api_key_selection_expression"] = api_key_selection_expression
        if base_path is not None:
            self._values["base_path"] = base_path
        if body is not None:
            self._values["body"] = body
        if body_s3_location is not None:
            self._values["body_s3_location"] = body_s3_location
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if credentials_arn is not None:
            self._values["credentials_arn"] = credentials_arn
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if disable_schema_validation is not None:
            self._values["disable_schema_validation"] = disable_schema_validation
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if name is not None:
            self._values["name"] = name
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if route_key is not None:
            self._values["route_key"] = route_key
        if route_selection_expression is not None:
            self._values["route_selection_expression"] = route_selection_expression
        if tags is not None:
            self._values["tags"] = tags
        if target is not None:
            self._values["target"] = target
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def api_key_selection_expression(self) -> typing.Optional[builtins.str]:
        '''An API key selection expression.

        Supported only for WebSocket APIs. See `API Key Selection Expressions <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-selection-expressions.html#apigateway-websocket-api-apikey-selection-expressions>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        '''
        result = self._values.get("api_key_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def base_path(self) -> typing.Optional[builtins.str]:
        '''Specifies how to interpret the base path of the API during import.

        Valid values are ``ignore`` , ``prepend`` , and ``split`` . The default value is ``ignore`` . To learn more, see `Set the OpenAPI basePath Property <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api-basePath.html>`_ . Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        '''
        result = self._values.get("base_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def body(self) -> typing.Any:
        '''The OpenAPI definition.

        Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        '''
        result = self._values.get("body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def body_s3_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.BodyS3LocationProperty]]:
        '''The S3 location of an OpenAPI definition.

        Supported only for HTTP APIs. To import an HTTP API, you must specify a ``Body`` or ``BodyS3Location`` . If you specify a ``Body`` or ``BodyS3Location`` , don't specify CloudFormation resources such as ``AWS::ApiGatewayV2::Authorizer`` or ``AWS::ApiGatewayV2::Route`` . API Gateway doesn't support the combination of OpenAPI and CloudFormation resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        '''
        result = self._values.get("body_s3_location")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.BodyS3LocationProperty]], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.CorsProperty]]:
        '''A CORS configuration.

        Supported only for HTTP APIs. See `Configuring CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.CorsProperty]], result)

    @builtins.property
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        It specifies the credentials required for the integration, if any. For a Lambda integration, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, specify ``null`` . Currently, this property is not used for HTTP integrations. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        '''
        result = self._values.get("credentials_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint.

        By default, clients can invoke your API with the default https://{api_id}.execute-api.{region}.amazonaws.com endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def disable_schema_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Avoid validating models when creating a deployment.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        '''
        result = self._values.get("disable_schema_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether to rollback the API creation when a warning is encountered.

        By default, API creation continues if a warning is encountered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the API.

        Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''The API protocol.

        Valid values are ``WEBSOCKET`` or ``HTTP`` . Required unless you specify an OpenAPI definition for ``Body`` or ``S3BodyLocation`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_key(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        If you don't specify a ``routeKey`` , a default route of ``$default`` is created. The ``$default`` route acts as a catch-all for any request made to your API, for a particular stage. The ``$default`` route key can't be modified. You can add routes after creating the API, and you can update the route keys of additional routes. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        '''
        result = self._values.get("route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The route selection expression for the API.

        For HTTP APIs, the ``routeSelectionExpression`` must be ``${request.method} ${request.path}`` . If not provided, this will be the default for HTTP APIs. This property is required for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        '''
        result = self._values.get("route_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''This property is part of quick create.

        Quick create produces an API with an integration, a default catch-all route, and a default stage which is configured to automatically deploy changes. For HTTP integrations, specify a fully qualified URL. For Lambda integrations, specify a function ARN. The type of the integration will be HTTP_PROXY or AWS_PROXY, respectively. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''A version identifier for the API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAuthorizer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Authorizer``.

    The ``AWS::ApiGatewayV2::Authorizer`` resource creates an authorizer for a WebSocket API or an HTTP API. To learn more, see `Controlling and managing access to a WebSocket API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-control-access.html>`_ and `Controlling and managing access to an HTTP API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::Authorizer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        cfn_authorizer = apigatewayv2.CfnAuthorizer(self, "MyCfnAuthorizer",
            api_id="apiId",
            authorizer_type="authorizerType",
            name="name",
        
            # the properties below are optional
            authorizer_credentials_arn="authorizerCredentialsArn",
            authorizer_payload_format_version="authorizerPayloadFormatVersion",
            authorizer_result_ttl_in_seconds=123,
            authorizer_uri="authorizerUri",
            enable_simple_responses=False,
            identity_source=["identitySource"],
            identity_validation_expression="identityValidationExpression",
            jwt_configuration=apigatewayv2.CfnAuthorizer.JWTConfigurationProperty(
                audience=["audience"],
                issuer="issuer"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        authorizer_type: builtins.str,
        name: builtins.str,
        authorizer_credentials_arn: typing.Optional[builtins.str] = None,
        authorizer_payload_format_version: typing.Optional[builtins.str] = None,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        identity_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
        jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnAuthorizer.JWTConfigurationProperty", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Authorizer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param authorizer_type: The authorizer type. Specify ``REQUEST`` for a Lambda function using incoming request parameters. Specify ``JWT`` to use JSON Web Tokens (supported only for HTTP APIs).
        :param name: The name of the authorizer.
        :param authorizer_credentials_arn: Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null. Supported only for ``REQUEST`` authorizers.
        :param authorizer_payload_format_version: Specifies the format of the payload sent to an HTTP API Lambda authorizer. Required for HTTP API Lambda authorizers. Supported values are ``1.0`` and ``2.0`` . To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .
        :param authorizer_result_ttl_in_seconds: The time to live (TTL) for cached authorizer results, in seconds. If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.
        :param authorizer_uri: The authorizer's Uniform Resource Identifier (URI). For ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2: *{account_id}* :function: *{lambda_function_name}* /invocations`` . In general, the URI has this form: ``arn:aws:apigateway: *{region}* :lambda:path/ *{service_api}*`` , where *{region}* is the same as the region hosting the Lambda function, path indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .
        :param enable_simple_responses: Specifies whether a Lambda authorizer returns a response in a simple format. By default, a Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .
        :param identity_source: The identity source for which authorization is requested. For a ``REQUEST`` authorizer, this is optional. The value is a set of one or more mapping expressions of the specified request parameters. The identity source can be headers, query string parameters, stage variables, and context parameters. For example, if an Auth header and a Name query string parameter are defined as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for WebSocket APIs. For HTTP APIs, use selection expressions prefixed with ``$`` , for example, ``$request.header.Auth`` , ``$request.querystring.Name`` . These parameters are used to perform runtime validation for Lambda-based authorizers by verifying all of the identity-related request parameters are present in the request, not null, and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized response without calling the Lambda function. For HTTP APIs, identity sources are also used as the cache key when caching is enabled. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ . For ``JWT`` , a single entry that specifies where to extract the JSON Web Token (JWT) from inbound requests. Currently only header-based and query parameter-based selections are supported, for example ``$request.header.Authorization`` .
        :param identity_validation_expression: This parameter is not used.
        :param jwt_configuration: The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer. Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnAuthorizer.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAuthorizerProps(
            api_id=api_id,
            authorizer_type=authorizer_type,
            name=name,
            authorizer_credentials_arn=authorizer_credentials_arn,
            authorizer_payload_format_version=authorizer_payload_format_version,
            authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds,
            authorizer_uri=authorizer_uri,
            enable_simple_responses=enable_simple_responses,
            identity_source=identity_source,
            identity_validation_expression=identity_validation_expression,
            jwt_configuration=jwt_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnAuthorizer.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnAuthorizer._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerType")
    def authorizer_type(self) -> builtins.str:
        '''The authorizer type.

        Specify ``REQUEST`` for a Lambda function using incoming request parameters. Specify ``JWT`` to use JSON Web Tokens (supported only for HTTP APIs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizerType"))

    @authorizer_type.setter
    def authorizer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "authorizer_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialsArn")
    def authorizer_credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer.

        To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null. Supported only for ``REQUEST`` authorizers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerCredentialsArn"))

    @authorizer_credentials_arn.setter
    def authorizer_credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "authorizer_credentials_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerCredentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerPayloadFormatVersion")
    def authorizer_payload_format_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the format of the payload sent to an HTTP API Lambda authorizer.

        Required for HTTP API Lambda authorizers. Supported values are ``1.0`` and ``2.0`` . To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerpayloadformatversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerPayloadFormatVersion"))

    @authorizer_payload_format_version.setter
    def authorizer_payload_format_version(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "authorizer_payload_format_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerPayloadFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time to live (TTL) for cached authorizer results, in seconds.

        If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authorizerResultTtlInSeconds"))

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "authorizer_result_ttl_in_seconds").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerResultTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        '''The authorizer's Uniform Resource Identifier (URI).

        For ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2: *{account_id}* :function: *{lambda_function_name}* /invocations`` . In general, the URI has this form: ``arn:aws:apigateway: *{region}* :lambda:path/ *{service_api}*`` , where *{region}* is the same as the region hosting the Lambda function, path indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerUri"))

    @authorizer_uri.setter
    def authorizer_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "authorizer_uri").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerUri", value)

    @builtins.property
    @jsii.member(jsii_name="enableSimpleResponses")
    def enable_simple_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether a Lambda authorizer returns a response in a simple format.

        By default, a Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-enablesimpleresponses
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "enableSimpleResponses"))

    @enable_simple_responses.setter
    def enable_simple_responses(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "enable_simple_responses").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSimpleResponses", value)

    @builtins.property
    @jsii.member(jsii_name="identitySource")
    def identity_source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identity source for which authorization is requested.

        For a ``REQUEST`` authorizer, this is optional. The value is a set of one or more mapping expressions of the specified request parameters. The identity source can be headers, query string parameters, stage variables, and context parameters. For example, if an Auth header and a Name query string parameter are defined as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for WebSocket APIs. For HTTP APIs, use selection expressions prefixed with ``$`` , for example, ``$request.header.Auth`` , ``$request.querystring.Name`` . These parameters are used to perform runtime validation for Lambda-based authorizers by verifying all of the identity-related request parameters are present in the request, not null, and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized response without calling the Lambda function. For HTTP APIs, identity sources are also used as the cache key when caching is enabled. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        For ``JWT`` , a single entry that specifies where to extract the JSON Web Token (JWT) from inbound requests. Currently only header-based and query parameter-based selections are supported, for example ``$request.header.Authorization`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitySource"))

    @identity_source.setter
    def identity_source(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "identity_source").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identitySource", value)

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''This parameter is not used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityValidationExpression"))

    @identity_validation_expression.setter
    def identity_validation_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "identity_validation_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityValidationExpression", value)

    @builtins.property
    @jsii.member(jsii_name="jwtConfiguration")
    def jwt_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]]:
        '''The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer.

        Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]], jsii.get(self, "jwtConfiguration"))

    @jwt_configuration.setter
    def jwt_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnAuthorizer, "jwt_configuration").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer.JWTConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audience": "audience", "issuer": "issuer"},
    )
    class JWTConfigurationProperty:
        def __init__(
            self,
            *,
            audience: typing.Optional[typing.Sequence[builtins.str]] = None,
            issuer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer.

            Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

            :param audience: A list of the intended recipients of the JWT. A valid JWT must provide an ``aud`` that matches at least one entry in this list. See `RFC 7519 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc7519#section-4.1.3>`_ . Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.
            :param issuer: The base domain of the identity provider that issues JSON Web Tokens. For example, an Amazon Cognito user pool has the following format: ``https://cognito-idp. {region} .amazonaws.com/ {userPoolId}`` . Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                j_wTConfiguration_property = apigatewayv2.CfnAuthorizer.JWTConfigurationProperty(
                    audience=["audience"],
                    issuer="issuer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnAuthorizer.JWTConfigurationProperty.__init__)
                check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            self._values: typing.Dict[str, typing.Any] = {}
            if audience is not None:
                self._values["audience"] = audience
            if issuer is not None:
                self._values["issuer"] = issuer

        @builtins.property
        def audience(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the intended recipients of the JWT.

            A valid JWT must provide an ``aud`` that matches at least one entry in this list. See `RFC 7519 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc7519#section-4.1.3>`_ . Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-audience
            '''
            result = self._values.get("audience")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The base domain of the identity provider that issues JSON Web Tokens.

            For example, an Amazon Cognito user pool has the following format: ``https://cognito-idp. {region} .amazonaws.com/ {userPoolId}`` . Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JWTConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "authorizer_type": "authorizerType",
        "name": "name",
        "authorizer_credentials_arn": "authorizerCredentialsArn",
        "authorizer_payload_format_version": "authorizerPayloadFormatVersion",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "authorizer_uri": "authorizerUri",
        "enable_simple_responses": "enableSimpleResponses",
        "identity_source": "identitySource",
        "identity_validation_expression": "identityValidationExpression",
        "jwt_configuration": "jwtConfiguration",
    },
)
class CfnAuthorizerProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        authorizer_type: builtins.str,
        name: builtins.str,
        authorizer_credentials_arn: typing.Optional[builtins.str] = None,
        authorizer_payload_format_version: typing.Optional[builtins.str] = None,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        identity_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
        jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnAuthorizer.JWTConfigurationProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAuthorizer``.

        :param api_id: The API identifier.
        :param authorizer_type: The authorizer type. Specify ``REQUEST`` for a Lambda function using incoming request parameters. Specify ``JWT`` to use JSON Web Tokens (supported only for HTTP APIs).
        :param name: The name of the authorizer.
        :param authorizer_credentials_arn: Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null. Supported only for ``REQUEST`` authorizers.
        :param authorizer_payload_format_version: Specifies the format of the payload sent to an HTTP API Lambda authorizer. Required for HTTP API Lambda authorizers. Supported values are ``1.0`` and ``2.0`` . To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .
        :param authorizer_result_ttl_in_seconds: The time to live (TTL) for cached authorizer results, in seconds. If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.
        :param authorizer_uri: The authorizer's Uniform Resource Identifier (URI). For ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2: *{account_id}* :function: *{lambda_function_name}* /invocations`` . In general, the URI has this form: ``arn:aws:apigateway: *{region}* :lambda:path/ *{service_api}*`` , where *{region}* is the same as the region hosting the Lambda function, path indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .
        :param enable_simple_responses: Specifies whether a Lambda authorizer returns a response in a simple format. By default, a Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .
        :param identity_source: The identity source for which authorization is requested. For a ``REQUEST`` authorizer, this is optional. The value is a set of one or more mapping expressions of the specified request parameters. The identity source can be headers, query string parameters, stage variables, and context parameters. For example, if an Auth header and a Name query string parameter are defined as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for WebSocket APIs. For HTTP APIs, use selection expressions prefixed with ``$`` , for example, ``$request.header.Auth`` , ``$request.querystring.Name`` . These parameters are used to perform runtime validation for Lambda-based authorizers by verifying all of the identity-related request parameters are present in the request, not null, and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized response without calling the Lambda function. For HTTP APIs, identity sources are also used as the cache key when caching is enabled. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ . For ``JWT`` , a single entry that specifies where to extract the JSON Web Token (JWT) from inbound requests. Currently only header-based and query parameter-based selections are supported, for example ``$request.header.Authorization`` .
        :param identity_validation_expression: This parameter is not used.
        :param jwt_configuration: The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer. Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            cfn_authorizer_props = apigatewayv2.CfnAuthorizerProps(
                api_id="apiId",
                authorizer_type="authorizerType",
                name="name",
            
                # the properties below are optional
                authorizer_credentials_arn="authorizerCredentialsArn",
                authorizer_payload_format_version="authorizerPayloadFormatVersion",
                authorizer_result_ttl_in_seconds=123,
                authorizer_uri="authorizerUri",
                enable_simple_responses=False,
                identity_source=["identitySource"],
                identity_validation_expression="identityValidationExpression",
                jwt_configuration=apigatewayv2.CfnAuthorizer.JWTConfigurationProperty(
                    audience=["audience"],
                    issuer="issuer"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnAuthorizerProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument authorizer_type", value=authorizer_type, expected_type=type_hints["authorizer_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorizer_credentials_arn", value=authorizer_credentials_arn, expected_type=type_hints["authorizer_credentials_arn"])
            check_type(argname="argument authorizer_payload_format_version", value=authorizer_payload_format_version, expected_type=type_hints["authorizer_payload_format_version"])
            check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument enable_simple_responses", value=enable_simple_responses, expected_type=type_hints["enable_simple_responses"])
            check_type(argname="argument identity_source", value=identity_source, expected_type=type_hints["identity_source"])
            check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
            check_type(argname="argument jwt_configuration", value=jwt_configuration, expected_type=type_hints["jwt_configuration"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "authorizer_type": authorizer_type,
            "name": name,
        }
        if authorizer_credentials_arn is not None:
            self._values["authorizer_credentials_arn"] = authorizer_credentials_arn
        if authorizer_payload_format_version is not None:
            self._values["authorizer_payload_format_version"] = authorizer_payload_format_version
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None:
            self._values["authorizer_uri"] = authorizer_uri
        if enable_simple_responses is not None:
            self._values["enable_simple_responses"] = enable_simple_responses
        if identity_source is not None:
            self._values["identity_source"] = identity_source
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression
        if jwt_configuration is not None:
            self._values["jwt_configuration"] = jwt_configuration

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_type(self) -> builtins.str:
        '''The authorizer type.

        Specify ``REQUEST`` for a Lambda function using incoming request parameters. Specify ``JWT`` to use JSON Web Tokens (supported only for HTTP APIs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        '''
        result = self._values.get("authorizer_type")
        assert result is not None, "Required property 'authorizer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer.

        To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null. Supported only for ``REQUEST`` authorizers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        '''
        result = self._values.get("authorizer_credentials_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_payload_format_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the format of the payload sent to an HTTP API Lambda authorizer.

        Required for HTTP API Lambda authorizers. Supported values are ``1.0`` and ``2.0`` . To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerpayloadformatversion
        '''
        result = self._values.get("authorizer_payload_format_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time to live (TTL) for cached authorizer results, in seconds.

        If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        '''
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        '''The authorizer's Uniform Resource Identifier (URI).

        For ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2: *{account_id}* :function: *{lambda_function_name}* /invocations`` . In general, the URI has this form: ``arn:aws:apigateway: *{region}* :lambda:path/ *{service_api}*`` , where *{region}* is the same as the region hosting the Lambda function, path indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        '''
        result = self._values.get("authorizer_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_simple_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether a Lambda authorizer returns a response in a simple format.

        By default, a Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-enablesimpleresponses
        '''
        result = self._values.get("enable_simple_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def identity_source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identity source for which authorization is requested.

        For a ``REQUEST`` authorizer, this is optional. The value is a set of one or more mapping expressions of the specified request parameters. The identity source can be headers, query string parameters, stage variables, and context parameters. For example, if an Auth header and a Name query string parameter are defined as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for WebSocket APIs. For HTTP APIs, use selection expressions prefixed with ``$`` , for example, ``$request.header.Auth`` , ``$request.querystring.Name`` . These parameters are used to perform runtime validation for Lambda-based authorizers by verifying all of the identity-related request parameters are present in the request, not null, and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized response without calling the Lambda function. For HTTP APIs, identity sources are also used as the cache key when caching is enabled. To learn more, see `Working with AWS Lambda authorizers for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html>`_ .

        For ``JWT`` , a single entry that specifies where to extract the JSON Web Token (JWT) from inbound requests. Currently only header-based and query parameter-based selections are supported, for example ``$request.header.Authorization`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        '''
        result = self._values.get("identity_source")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''This parameter is not used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        '''
        result = self._values.get("identity_validation_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAuthorizer.JWTConfigurationProperty]]:
        '''The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer.

        Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        '''
        result = self._values.get("jwt_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAuthorizer.JWTConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeployment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeployment",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Deployment``.

    The ``AWS::ApiGatewayV2::Deployment`` resource creates a deployment for an API.

    :cloudformationResource: AWS::ApiGatewayV2::Deployment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        cfn_deployment = apigatewayv2.CfnDeployment(self, "MyCfnDeployment",
            api_id="apiId",
        
            # the properties below are optional
            description="description",
            stage_name="stageName"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param description: The description for the deployment resource.
        :param stage_name: The name of an existing stage to associate with the deployment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDeployment.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentProps(
            api_id=api_id, description=description, stage_name=stage_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDeployment.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDeployment._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDeployment, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the deployment resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDeployment, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The name of an existing stage to associate with the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDeployment, "stage_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "description": "description",
        "stage_name": "stageName",
    },
)
class CfnDeploymentProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeployment``.

        :param api_id: The API identifier.
        :param description: The description for the deployment resource.
        :param stage_name: The name of an existing stage to associate with the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            cfn_deployment_props = apigatewayv2.CfnDeploymentProps(
                api_id="apiId",
            
                # the properties below are optional
                description="description",
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDeploymentProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
        }
        if description is not None:
            self._values["description"] = description
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the deployment resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The name of an existing stage to associate with the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDomainName(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::DomainName``.

    The ``AWS::ApiGatewayV2::DomainName`` resource specifies a custom domain name for your API in Amazon API Gateway (API Gateway).

    You can use a custom domain name to provide a URL that's more intuitive and easier to recall. For more information about using custom domain names, see `Set up Custom Domain Name for an API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::DomainName
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # tags: Any
        
        cfn_domain_name = apigatewayv2.CfnDomainName(self, "MyCfnDomainName",
            domain_name="domainName",
        
            # the properties below are optional
            domain_name_configurations=[apigatewayv2.CfnDomainName.DomainNameConfigurationProperty(
                certificate_arn="certificateArn",
                certificate_name="certificateName",
                endpoint_type="endpointType",
                ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                security_policy="securityPolicy"
            )],
            mutual_tls_authentication=apigatewayv2.CfnDomainName.MutualTlsAuthenticationProperty(
                truststore_uri="truststoreUri",
                truststore_version="truststoreVersion"
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnDomainName.DomainNameConfigurationProperty", typing.Dict[str, typing.Any]]]]]] = None,
        mutual_tls_authentication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnDomainName.MutualTlsAuthenticationProperty", typing.Dict[str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: The custom domain name for your API in Amazon API Gateway. Uppercase letters are not supported.
        :param domain_name_configurations: The domain name configurations.
        :param mutual_tls_authentication: The mutual TLS authentication configuration for a custom domain name.
        :param tags: The collection of tags associated with a domain name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDomainName.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainNameProps(
            domain_name=domain_name,
            domain_name_configurations=domain_name_configurations,
            mutual_tls_authentication=mutual_tls_authentication,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDomainName.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDomainName._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> builtins.str:
        '''The domain name associated with the regional endpoint for this custom domain name.

        You set up this association by adding a DNS record that points the custom domain name to this regional domain name.

        :cloudformationAttribute: RegionalDomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegionalDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrRegionalHostedZoneId")
    def attr_regional_hosted_zone_id(self) -> builtins.str:
        '''The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :cloudformationAttribute: RegionalHostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegionalHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''The collection of tags associated with a domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The custom domain name for your API in Amazon API Gateway.

        Uppercase letters are not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDomainName, "domain_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="domainNameConfigurations")
    def domain_name_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]]:
        '''The domain name configurations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]], jsii.get(self, "domainNameConfigurations"))

    @domain_name_configurations.setter
    def domain_name_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDomainName, "domain_name_configurations").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNameConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="mutualTlsAuthentication")
    def mutual_tls_authentication(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]]:
        '''The mutual TLS authentication configuration for a custom domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-mutualtlsauthentication
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]], jsii.get(self, "mutualTlsAuthentication"))

    @mutual_tls_authentication.setter
    def mutual_tls_authentication(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnDomainName, "mutual_tls_authentication").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutualTlsAuthentication", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName.DomainNameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "certificate_name": "certificateName",
            "endpoint_type": "endpointType",
            "ownership_verification_certificate_arn": "ownershipVerificationCertificateArn",
            "security_policy": "securityPolicy",
        },
    )
    class DomainNameConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            certificate_name: typing.Optional[builtins.str] = None,
            endpoint_type: typing.Optional[builtins.str] = None,
            ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``DomainNameConfiguration`` property type specifies the configuration for a an API's domain name.

            ``DomainNameConfiguration`` is a property of the `AWS::ApiGatewayV2::DomainName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html>`_ resource.

            :param certificate_arn: An AWS -managed certificate that will be used by the edge-optimized endpoint for this domain name. AWS Certificate Manager is the only supported source.
            :param certificate_name: The user-friendly name of the certificate that will be used by the edge-optimized endpoint for this domain name.
            :param endpoint_type: The endpoint type.
            :param ownership_verification_certificate_arn: The ARN of the public certificate issued by ACM to validate ownership of your custom domain. Only required when configuring mutual TLS and using an ACM imported or private CA certificate ARN as the RegionalCertificateArn.
            :param security_policy: The Transport Layer Security (TLS) version of the security policy for this domain name. The valid values are ``TLS_1_0`` and ``TLS_1_2`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                domain_name_configuration_property = apigatewayv2.CfnDomainName.DomainNameConfigurationProperty(
                    certificate_arn="certificateArn",
                    certificate_name="certificateName",
                    endpoint_type="endpointType",
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnDomainName.DomainNameConfigurationProperty.__init__)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument ownership_verification_certificate_arn", value=ownership_verification_certificate_arn, expected_type=type_hints["ownership_verification_certificate_arn"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if certificate_name is not None:
                self._values["certificate_name"] = certificate_name
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if ownership_verification_certificate_arn is not None:
                self._values["ownership_verification_certificate_arn"] = ownership_verification_certificate_arn
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''An AWS -managed certificate that will be used by the edge-optimized endpoint for this domain name.

            AWS Certificate Manager is the only supported source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_name(self) -> typing.Optional[builtins.str]:
            '''The user-friendly name of the certificate that will be used by the edge-optimized endpoint for this domain name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatename
            '''
            result = self._values.get("certificate_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The endpoint type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ownership_verification_certificate_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ARN of the public certificate issued by ACM to validate ownership of your custom domain.

            Only required when configuring mutual TLS and using an ACM imported or private CA certificate ARN as the RegionalCertificateArn.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-ownershipverificationcertificatearn
            '''
            result = self._values.get("ownership_verification_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''The Transport Layer Security (TLS) version of the security policy for this domain name.

            The valid values are ``TLS_1_0`` and ``TLS_1_2`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-securitypolicy
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainNameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If specified, API Gateway performs two-way authentication between the client and the server.

            Clients must present a trusted certificate to access your API.

            :param truststore_uri: An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, ``s3:// bucket-name / key-name`` . The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version. To update the truststore, you must have permissions to access the S3 object.
            :param truststore_version: The version of the S3 object that contains your truststore. To specify a version, you must have versioning enabled for the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                mutual_tls_authentication_property = apigatewayv2.CfnDomainName.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnDomainName.MutualTlsAuthenticationProperty.__init__)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, ``s3:// bucket-name / key-name`` .

            The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version. To update the truststore, you must have permissions to access the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            '''The version of the S3 object that contains your truststore.

            To specify a version, you must have versioning enabled for the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "domain_name_configurations": "domainNameConfigurations",
        "mutual_tls_authentication": "mutualTlsAuthentication",
        "tags": "tags",
    },
)
class CfnDomainNameProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnDomainName.DomainNameConfigurationProperty, typing.Dict[str, typing.Any]]]]]] = None,
        mutual_tls_authentication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnDomainName.MutualTlsAuthenticationProperty, typing.Dict[str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnDomainName``.

        :param domain_name: The custom domain name for your API in Amazon API Gateway. Uppercase letters are not supported.
        :param domain_name_configurations: The domain name configurations.
        :param mutual_tls_authentication: The mutual TLS authentication configuration for a custom domain name.
        :param tags: The collection of tags associated with a domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # tags: Any
            
            cfn_domain_name_props = apigatewayv2.CfnDomainNameProps(
                domain_name="domainName",
            
                # the properties below are optional
                domain_name_configurations=[apigatewayv2.CfnDomainName.DomainNameConfigurationProperty(
                    certificate_arn="certificateArn",
                    certificate_name="certificateName",
                    endpoint_type="endpointType",
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    security_policy="securityPolicy"
                )],
                mutual_tls_authentication=apigatewayv2.CfnDomainName.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnDomainNameProps.__init__)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_name_configurations", value=domain_name_configurations, expected_type=type_hints["domain_name_configurations"])
            check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if domain_name_configurations is not None:
            self._values["domain_name_configurations"] = domain_name_configurations
        if mutual_tls_authentication is not None:
            self._values["mutual_tls_authentication"] = mutual_tls_authentication
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The custom domain name for your API in Amazon API Gateway.

        Uppercase letters are not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.DomainNameConfigurationProperty]]]]:
        '''The domain name configurations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        '''
        result = self._values.get("domain_name_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.DomainNameConfigurationProperty]]]], result)

    @builtins.property
    def mutual_tls_authentication(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.MutualTlsAuthenticationProperty]]:
        '''The mutual TLS authentication configuration for a custom domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-mutualtlsauthentication
        '''
        result = self._values.get("mutual_tls_authentication")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.MutualTlsAuthenticationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The collection of tags associated with a domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegration(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Integration``.

    The ``AWS::ApiGatewayV2::Integration`` resource creates an integration for an API.

    :cloudformationResource: AWS::ApiGatewayV2::Integration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # request_parameters: Any
        # request_templates: Any
        # response_parameters: Any
        
        cfn_integration = apigatewayv2.CfnIntegration(self, "MyCfnIntegration",
            api_id="apiId",
            integration_type="integrationType",
        
            # the properties below are optional
            connection_id="connectionId",
            connection_type="connectionType",
            content_handling_strategy="contentHandlingStrategy",
            credentials_arn="credentialsArn",
            description="description",
            integration_method="integrationMethod",
            integration_subtype="integrationSubtype",
            integration_uri="integrationUri",
            passthrough_behavior="passthroughBehavior",
            payload_format_version="payloadFormatVersion",
            request_parameters=request_parameters,
            request_templates=request_templates,
            response_parameters=response_parameters,
            template_selection_expression="templateSelectionExpression",
            timeout_in_millis=123,
            tls_config=apigatewayv2.CfnIntegration.TlsConfigProperty(
                server_name_to_verify="serverNameToVerify"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration_type: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_method: typing.Optional[builtins.str] = None,
        integration_subtype: typing.Optional[builtins.str] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        passthrough_behavior: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[builtins.str] = None,
        request_parameters: typing.Any = None,
        request_templates: typing.Any = None,
        response_parameters: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
        timeout_in_millis: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnIntegration.TlsConfigProperty", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Integration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param integration_type: The integration type of an integration. One of the following:. ``AWS`` : for integrating the route or method request with an AWS service action, including the Lambda function-invoking action. With the Lambda function-invoking action, this is referred to as the Lambda custom integration. With any other AWS service action, this is known as AWS integration. Supported only for WebSocket APIs. ``AWS_PROXY`` : for integrating the route or method request with a Lambda function or other AWS service action. This integration is also referred to as a Lambda proxy integration. ``HTTP`` : for integrating the route or method request with an HTTP endpoint. This integration is also referred to as the HTTP custom integration. Supported only for WebSocket APIs. ``HTTP_PROXY`` : for integrating the route or method request with an HTTP endpoint, with the client request passed through as-is. This is also referred to as HTTP proxy integration. For HTTP API private integrations, use an ``HTTP_PROXY`` integration. ``MOCK`` : for integrating the route or method request with API Gateway as a "loopback" endpoint without invoking any backend. Supported only for WebSocket APIs.
        :param connection_id: The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        :param connection_type: The type of the network connection to the integration endpoint. Specify ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and resources in a VPC. The default value is ``INTERNET`` .
        :param content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob. ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string. If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.
        :param credentials_arn: Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, don't specify this parameter.
        :param description: The description of the integration.
        :param integration_method: Specifies the integration's HTTP method type.
        :param integration_subtype: Supported only for HTTP API ``AWS_PROXY`` integrations. Specifies the AWS service action to invoke. To learn more, see `Integration subtype reference <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html>`_ .
        :param integration_uri: For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service. If you specify the ARN of an AWS Cloud Map service, API Gateway uses ``DiscoverInstances`` to identify resources. You can use query parameters to target specific resources. To learn more, see `DiscoverInstances <https://docs.aws.amazon.com/cloud-map/latest/api/API_DiscoverInstances.html>`_ . For private integrations, all resources must be owned by the same AWS account .
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the ``Content-Type`` header in the request, and the available mapping templates specified as the ``requestTemplates`` property on the ``Integration`` resource. There are three valid values: ``WHEN_NO_MATCH`` , ``WHEN_NO_TEMPLATES`` , and ``NEVER`` . Supported only for WebSocket APIs. ``WHEN_NO_MATCH`` passes the request body for unmapped content types through to the integration backend without transformation. ``NEVER`` rejects unmapped content types with an ``HTTP 415 Unsupported Media Type`` response. ``WHEN_NO_TEMPLATES`` allows pass-through when the integration has no content types mapped to templates. However, if there is at least one content type defined, unmapped content types will be rejected with the same ``HTTP 415 Unsupported Media Type`` response.
        :param payload_format_version: Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .
        :param request_parameters: For WebSocket APIs, a key-value map specifying request parameters that are passed from the method request to the backend. The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the backend. The method request parameter value must match the pattern of ``method.request. {location} . {name}`` , where ``{location}`` is ``querystring`` , ``path`` , or ``header`` ; and ``{name}`` must be a valid and unique method request parameter name. For HTTP API integrations with a specified ``integrationSubtype`` , request parameters are a key-value map specifying parameters that are passed to ``AWS_PROXY`` integrations. You can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Working with AWS service integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services.html>`_ . For HTTP API integrations without a specified ``integrationSubtype`` request parameters are a key-value map specifying how to transform HTTP requests before sending them to the backend. The key should follow the pattern :<header|querystring|path>. where action can be ``append`` , ``overwrite`` or ``remove`` . For values, you can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .
        :param request_templates: Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client. The content type value is the key in this map, and the template (as a String) is the value. Supported only for WebSocket APIs.
        :param response_parameters: Supported only for HTTP APIs. You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. The value is of type ```ResponseParameterList`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html>`_ . To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .
        :param template_selection_expression: The template selection expression for the integration. Supported only for WebSocket APIs.
        :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        :param tls_config: The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegration.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIntegrationProps(
            api_id=api_id,
            integration_type=integration_type,
            connection_id=connection_id,
            connection_type=connection_type,
            content_handling_strategy=content_handling_strategy,
            credentials_arn=credentials_arn,
            description=description,
            integration_method=integration_method,
            integration_subtype=integration_subtype,
            integration_uri=integration_uri,
            passthrough_behavior=passthrough_behavior,
            payload_format_version=payload_format_version,
            request_parameters=request_parameters,
            request_templates=request_templates,
            response_parameters=response_parameters,
            template_selection_expression=template_selection_expression,
            timeout_in_millis=timeout_in_millis,
            tls_config=tls_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegration.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegration._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        '''The integration type of an integration. One of the following:.

        ``AWS`` : for integrating the route or method request with an AWS service action, including the Lambda function-invoking action. With the Lambda function-invoking action, this is referred to as the Lambda custom integration. With any other AWS service action, this is known as AWS integration. Supported only for WebSocket APIs.

        ``AWS_PROXY`` : for integrating the route or method request with a Lambda function or other AWS service action. This integration is also referred to as a Lambda proxy integration.

        ``HTTP`` : for integrating the route or method request with an HTTP endpoint. This integration is also referred to as the HTTP custom integration. Supported only for WebSocket APIs.

        ``HTTP_PROXY`` : for integrating the route or method request with an HTTP endpoint, with the client request passed through as-is. This is also referred to as HTTP proxy integration. For HTTP API private integrations, use an ``HTTP_PROXY`` integration.

        ``MOCK`` : for integrating the route or method request with API Gateway as a "loopback" endpoint without invoking any backend. Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @integration_type.setter
    def integration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "integration_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        '''For WebSocket APIs, a key-value map specifying request parameters that are passed from the method request to the backend.

        The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the backend. The method request parameter value must match the pattern of ``method.request. {location} . {name}`` , where ``{location}`` is ``querystring`` , ``path`` , or ``header`` ; and ``{name}`` must be a valid and unique method request parameter name.

        For HTTP API integrations with a specified ``integrationSubtype`` , request parameters are a key-value map specifying parameters that are passed to ``AWS_PROXY`` integrations. You can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Working with AWS service integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services.html>`_ .

        For HTTP API integrations without a specified ``integrationSubtype`` request parameters are a key-value map specifying how to transform HTTP requests before sending them to the backend. The key should follow the pattern :<header|querystring|path>. where action can be ``append`` , ``overwrite`` or ``remove`` . For values, you can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "requestParameters"))

    @request_parameters.setter
    def request_parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "request_parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="requestTemplates")
    def request_templates(self) -> typing.Any:
        '''Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.

        The content type value is the key in this map, and the template (as a String) is the value. Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        '''
        return typing.cast(typing.Any, jsii.get(self, "requestTemplates"))

    @request_templates.setter
    def request_templates(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "request_templates").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        '''Supported only for HTTP APIs.

        You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. The value is of type ```ResponseParameterList`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html>`_ . To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-responseparameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "responseParameters"))

    @response_parameters.setter
    def response_parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "response_parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "connection_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value)

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The type of the network connection to the integration endpoint.

        Specify ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and resources in a VPC. The default value is ``INTERNET`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionType"))

    @connection_type.setter
    def connection_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "connection_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        '''Supported only for WebSocket APIs.

        Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

        ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob.

        ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string.

        If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentHandlingStrategy"))

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "content_handling_strategy").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the credentials required for the integration, if any.

        For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, don't specify this parameter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsArn"))

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "credentials_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="integrationMethod")
    def integration_method(self) -> typing.Optional[builtins.str]:
        '''Specifies the integration's HTTP method type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationMethod"))

    @integration_method.setter
    def integration_method(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "integration_method").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationSubtype")
    def integration_subtype(self) -> typing.Optional[builtins.str]:
        '''Supported only for HTTP API ``AWS_PROXY`` integrations.

        Specifies the AWS service action to invoke. To learn more, see `Integration subtype reference <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationsubtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationSubtype"))

    @integration_subtype.setter
    def integration_subtype(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "integration_subtype").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationSubtype", value)

    @builtins.property
    @jsii.member(jsii_name="integrationUri")
    def integration_uri(self) -> typing.Optional[builtins.str]:
        '''For a Lambda integration, specify the URI of a Lambda function.

        For an HTTP integration, specify a fully-qualified URL.

        For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service. If you specify the ARN of an AWS Cloud Map service, API Gateway uses ``DiscoverInstances`` to identify resources. You can use query parameters to target specific resources. To learn more, see `DiscoverInstances <https://docs.aws.amazon.com/cloud-map/latest/api/API_DiscoverInstances.html>`_ . For private integrations, all resources must be owned by the same AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationUri"))

    @integration_uri.setter
    def integration_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "integration_uri").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationUri", value)

    @builtins.property
    @jsii.member(jsii_name="passthroughBehavior")
    def passthrough_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the pass-through behavior for incoming requests based on the ``Content-Type`` header in the request, and the available mapping templates specified as the ``requestTemplates`` property on the ``Integration`` resource.

        There are three valid values: ``WHEN_NO_MATCH`` , ``WHEN_NO_TEMPLATES`` , and ``NEVER`` . Supported only for WebSocket APIs.

        ``WHEN_NO_MATCH`` passes the request body for unmapped content types through to the integration backend without transformation.

        ``NEVER`` rejects unmapped content types with an ``HTTP 415 Unsupported Media Type`` response.

        ``WHEN_NO_TEMPLATES`` allows pass-through when the integration has no content types mapped to templates. However, if there is at least one content type defined, unmapped content types will be rejected with the same ``HTTP 415 Unsupported Media Type`` response.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passthroughBehavior"))

    @passthrough_behavior.setter
    def passthrough_behavior(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "passthrough_behavior").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passthroughBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def payload_format_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the format of the payload sent to an integration.

        Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFormatVersion"))

    @payload_format_version.setter
    def payload_format_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "payload_format_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The template selection expression for the integration.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateSelectionExpression"))

    @template_selection_expression.setter
    def template_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "template_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMillis")
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        '''Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs.

        The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMillis"))

    @timeout_in_millis.setter
    def timeout_in_millis(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "timeout_in_millis").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMillis", value)

    @builtins.property
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]]:
        '''The TLS configuration for a private integration.

        If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]], jsii.get(self, "tlsConfig"))

    @tls_config.setter
    def tls_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegration, "tls_config").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration.ResponseParameterListProperty",
        jsii_struct_bases=[],
        name_mapping={"response_parameters": "responseParameters"},
    )
    class ResponseParameterListProperty:
        def __init__(
            self,
            *,
            response_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnIntegration.ResponseParameterProperty", typing.Dict[str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a list of response parameters for an HTTP API.

            :param response_parameters: Supported only for HTTP APIs. You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. Response parameters are a key-value map. The key must match the pattern ``<action>:<header>.<location>`` or ``overwrite.statuscode`` . The action can be ``append`` , ``overwrite`` or ``remove`` . The value can be a static value, or map to response data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                response_parameter_list_property = apigatewayv2.CfnIntegration.ResponseParameterListProperty(
                    response_parameters=[apigatewayv2.CfnIntegration.ResponseParameterProperty(
                        destination="destination",
                        source="source"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnIntegration.ResponseParameterListProperty.__init__)
                check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
            self._values: typing.Dict[str, typing.Any] = {}
            if response_parameters is not None:
                self._values["response_parameters"] = response_parameters

        @builtins.property
        def response_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.ResponseParameterProperty"]]]]:
            '''Supported only for HTTP APIs.

            You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. Response parameters are a key-value map. The key must match the pattern ``<action>:<header>.<location>`` or ``overwrite.statuscode`` . The action can be ``append`` , ``overwrite`` or ``remove`` . The value can be a static value, or map to response data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html#cfn-apigatewayv2-integration-responseparameterlist-responseparameters
            '''
            result = self._values.get("response_parameters")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.ResponseParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponseParameterListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration.ResponseParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "source": "source"},
    )
    class ResponseParameterProperty:
        def __init__(self, *, destination: builtins.str, source: builtins.str) -> None:
            '''Supported only for HTTP APIs.

            You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. Response parameters are a key-value map. The key must match the pattern ``<action>:<header>.<location>`` or ``overwrite.statuscode`` . The action can be ``append`` , ``overwrite`` or ``remove`` . The value can be a static value, or map to response data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :param destination: Specifies the location of the response to modify, and how to modify it. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .
            :param source: Specifies the data to update the parameter with. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                response_parameter_property = apigatewayv2.CfnIntegration.ResponseParameterProperty(
                    destination="destination",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnIntegration.ResponseParameterProperty.__init__)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "source": source,
            }

        @builtins.property
        def destination(self) -> builtins.str:
            '''Specifies the location of the response to modify, and how to modify it.

            To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameter.html#cfn-apigatewayv2-integration-responseparameter-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source(self) -> builtins.str:
            '''Specifies the data to update the parameter with.

            To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameter.html#cfn-apigatewayv2-integration-responseparameter-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponseParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration.TlsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"server_name_to_verify": "serverNameToVerify"},
    )
    class TlsConfigProperty:
        def __init__(
            self,
            *,
            server_name_to_verify: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``TlsConfig`` property specifies the TLS configuration for a private integration.

            If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.

            :param server_name_to_verify: If you specify a server name, API Gateway uses it to verify the hostname on the integration's certificate. The server name is also included in the TLS handshake to support Server Name Indication (SNI) or virtual hosting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                tls_config_property = apigatewayv2.CfnIntegration.TlsConfigProperty(
                    server_name_to_verify="serverNameToVerify"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnIntegration.TlsConfigProperty.__init__)
                check_type(argname="argument server_name_to_verify", value=server_name_to_verify, expected_type=type_hints["server_name_to_verify"])
            self._values: typing.Dict[str, typing.Any] = {}
            if server_name_to_verify is not None:
                self._values["server_name_to_verify"] = server_name_to_verify

        @builtins.property
        def server_name_to_verify(self) -> typing.Optional[builtins.str]:
            '''If you specify a server name, API Gateway uses it to verify the hostname on the integration's certificate.

            The server name is also included in the TLS handshake to support Server Name Indication (SNI) or virtual hosting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html#cfn-apigatewayv2-integration-tlsconfig-servernametoverify
            '''
            result = self._values.get("server_name_to_verify")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration_type": "integrationType",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "content_handling_strategy": "contentHandlingStrategy",
        "credentials_arn": "credentialsArn",
        "description": "description",
        "integration_method": "integrationMethod",
        "integration_subtype": "integrationSubtype",
        "integration_uri": "integrationUri",
        "passthrough_behavior": "passthroughBehavior",
        "payload_format_version": "payloadFormatVersion",
        "request_parameters": "requestParameters",
        "request_templates": "requestTemplates",
        "response_parameters": "responseParameters",
        "template_selection_expression": "templateSelectionExpression",
        "timeout_in_millis": "timeoutInMillis",
        "tls_config": "tlsConfig",
    },
)
class CfnIntegrationProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration_type: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_method: typing.Optional[builtins.str] = None,
        integration_subtype: typing.Optional[builtins.str] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        passthrough_behavior: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[builtins.str] = None,
        request_parameters: typing.Any = None,
        request_templates: typing.Any = None,
        response_parameters: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
        timeout_in_millis: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnIntegration.TlsConfigProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIntegration``.

        :param api_id: The API identifier.
        :param integration_type: The integration type of an integration. One of the following:. ``AWS`` : for integrating the route or method request with an AWS service action, including the Lambda function-invoking action. With the Lambda function-invoking action, this is referred to as the Lambda custom integration. With any other AWS service action, this is known as AWS integration. Supported only for WebSocket APIs. ``AWS_PROXY`` : for integrating the route or method request with a Lambda function or other AWS service action. This integration is also referred to as a Lambda proxy integration. ``HTTP`` : for integrating the route or method request with an HTTP endpoint. This integration is also referred to as the HTTP custom integration. Supported only for WebSocket APIs. ``HTTP_PROXY`` : for integrating the route or method request with an HTTP endpoint, with the client request passed through as-is. This is also referred to as HTTP proxy integration. For HTTP API private integrations, use an ``HTTP_PROXY`` integration. ``MOCK`` : for integrating the route or method request with API Gateway as a "loopback" endpoint without invoking any backend. Supported only for WebSocket APIs.
        :param connection_id: The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        :param connection_type: The type of the network connection to the integration endpoint. Specify ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and resources in a VPC. The default value is ``INTERNET`` .
        :param content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob. ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string. If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.
        :param credentials_arn: Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, don't specify this parameter.
        :param description: The description of the integration.
        :param integration_method: Specifies the integration's HTTP method type.
        :param integration_subtype: Supported only for HTTP API ``AWS_PROXY`` integrations. Specifies the AWS service action to invoke. To learn more, see `Integration subtype reference <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html>`_ .
        :param integration_uri: For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service. If you specify the ARN of an AWS Cloud Map service, API Gateway uses ``DiscoverInstances`` to identify resources. You can use query parameters to target specific resources. To learn more, see `DiscoverInstances <https://docs.aws.amazon.com/cloud-map/latest/api/API_DiscoverInstances.html>`_ . For private integrations, all resources must be owned by the same AWS account .
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the ``Content-Type`` header in the request, and the available mapping templates specified as the ``requestTemplates`` property on the ``Integration`` resource. There are three valid values: ``WHEN_NO_MATCH`` , ``WHEN_NO_TEMPLATES`` , and ``NEVER`` . Supported only for WebSocket APIs. ``WHEN_NO_MATCH`` passes the request body for unmapped content types through to the integration backend without transformation. ``NEVER`` rejects unmapped content types with an ``HTTP 415 Unsupported Media Type`` response. ``WHEN_NO_TEMPLATES`` allows pass-through when the integration has no content types mapped to templates. However, if there is at least one content type defined, unmapped content types will be rejected with the same ``HTTP 415 Unsupported Media Type`` response.
        :param payload_format_version: Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .
        :param request_parameters: For WebSocket APIs, a key-value map specifying request parameters that are passed from the method request to the backend. The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the backend. The method request parameter value must match the pattern of ``method.request. {location} . {name}`` , where ``{location}`` is ``querystring`` , ``path`` , or ``header`` ; and ``{name}`` must be a valid and unique method request parameter name. For HTTP API integrations with a specified ``integrationSubtype`` , request parameters are a key-value map specifying parameters that are passed to ``AWS_PROXY`` integrations. You can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Working with AWS service integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services.html>`_ . For HTTP API integrations without a specified ``integrationSubtype`` request parameters are a key-value map specifying how to transform HTTP requests before sending them to the backend. The key should follow the pattern :<header|querystring|path>. where action can be ``append`` , ``overwrite`` or ``remove`` . For values, you can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .
        :param request_templates: Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client. The content type value is the key in this map, and the template (as a String) is the value. Supported only for WebSocket APIs.
        :param response_parameters: Supported only for HTTP APIs. You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. The value is of type ```ResponseParameterList`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html>`_ . To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .
        :param template_selection_expression: The template selection expression for the integration. Supported only for WebSocket APIs.
        :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        :param tls_config: The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # request_parameters: Any
            # request_templates: Any
            # response_parameters: Any
            
            cfn_integration_props = apigatewayv2.CfnIntegrationProps(
                api_id="apiId",
                integration_type="integrationType",
            
                # the properties below are optional
                connection_id="connectionId",
                connection_type="connectionType",
                content_handling_strategy="contentHandlingStrategy",
                credentials_arn="credentialsArn",
                description="description",
                integration_method="integrationMethod",
                integration_subtype="integrationSubtype",
                integration_uri="integrationUri",
                passthrough_behavior="passthroughBehavior",
                payload_format_version="payloadFormatVersion",
                request_parameters=request_parameters,
                request_templates=request_templates,
                response_parameters=response_parameters,
                template_selection_expression="templateSelectionExpression",
                timeout_in_millis=123,
                tls_config=apigatewayv2.CfnIntegration.TlsConfigProperty(
                    server_name_to_verify="serverNameToVerify"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegrationProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument content_handling_strategy", value=content_handling_strategy, expected_type=type_hints["content_handling_strategy"])
            check_type(argname="argument credentials_arn", value=credentials_arn, expected_type=type_hints["credentials_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument integration_method", value=integration_method, expected_type=type_hints["integration_method"])
            check_type(argname="argument integration_subtype", value=integration_subtype, expected_type=type_hints["integration_subtype"])
            check_type(argname="argument integration_uri", value=integration_uri, expected_type=type_hints["integration_uri"])
            check_type(argname="argument passthrough_behavior", value=passthrough_behavior, expected_type=type_hints["passthrough_behavior"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
            check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
            check_type(argname="argument request_templates", value=request_templates, expected_type=type_hints["request_templates"])
            check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
            check_type(argname="argument template_selection_expression", value=template_selection_expression, expected_type=type_hints["template_selection_expression"])
            check_type(argname="argument timeout_in_millis", value=timeout_in_millis, expected_type=type_hints["timeout_in_millis"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "integration_type": integration_type,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if content_handling_strategy is not None:
            self._values["content_handling_strategy"] = content_handling_strategy
        if credentials_arn is not None:
            self._values["credentials_arn"] = credentials_arn
        if description is not None:
            self._values["description"] = description
        if integration_method is not None:
            self._values["integration_method"] = integration_method
        if integration_subtype is not None:
            self._values["integration_subtype"] = integration_subtype
        if integration_uri is not None:
            self._values["integration_uri"] = integration_uri
        if passthrough_behavior is not None:
            self._values["passthrough_behavior"] = passthrough_behavior
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version
        if request_parameters is not None:
            self._values["request_parameters"] = request_parameters
        if request_templates is not None:
            self._values["request_templates"] = request_templates
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters
        if template_selection_expression is not None:
            self._values["template_selection_expression"] = template_selection_expression
        if timeout_in_millis is not None:
            self._values["timeout_in_millis"] = timeout_in_millis
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_type(self) -> builtins.str:
        '''The integration type of an integration. One of the following:.

        ``AWS`` : for integrating the route or method request with an AWS service action, including the Lambda function-invoking action. With the Lambda function-invoking action, this is referred to as the Lambda custom integration. With any other AWS service action, this is known as AWS integration. Supported only for WebSocket APIs.

        ``AWS_PROXY`` : for integrating the route or method request with a Lambda function or other AWS service action. This integration is also referred to as a Lambda proxy integration.

        ``HTTP`` : for integrating the route or method request with an HTTP endpoint. This integration is also referred to as the HTTP custom integration. Supported only for WebSocket APIs.

        ``HTTP_PROXY`` : for integrating the route or method request with an HTTP endpoint, with the client request passed through as-is. This is also referred to as HTTP proxy integration. For HTTP API private integrations, use an ``HTTP_PROXY`` integration.

        ``MOCK`` : for integrating the route or method request with API Gateway as a "loopback" endpoint without invoking any backend. Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The type of the network connection to the integration endpoint.

        Specify ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and resources in a VPC. The default value is ``INTERNET`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        '''Supported only for WebSocket APIs.

        Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

        ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob.

        ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string.

        If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        '''
        result = self._values.get("content_handling_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the credentials required for the integration, if any.

        For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::*:user/*`` . To use resource-based permissions on supported AWS services, don't specify this parameter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        '''
        result = self._values.get("credentials_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_method(self) -> typing.Optional[builtins.str]:
        '''Specifies the integration's HTTP method type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        '''
        result = self._values.get("integration_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_subtype(self) -> typing.Optional[builtins.str]:
        '''Supported only for HTTP API ``AWS_PROXY`` integrations.

        Specifies the AWS service action to invoke. To learn more, see `Integration subtype reference <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationsubtype
        '''
        result = self._values.get("integration_subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_uri(self) -> typing.Optional[builtins.str]:
        '''For a Lambda integration, specify the URI of a Lambda function.

        For an HTTP integration, specify a fully-qualified URL.

        For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service. If you specify the ARN of an AWS Cloud Map service, API Gateway uses ``DiscoverInstances`` to identify resources. You can use query parameters to target specific resources. To learn more, see `DiscoverInstances <https://docs.aws.amazon.com/cloud-map/latest/api/API_DiscoverInstances.html>`_ . For private integrations, all resources must be owned by the same AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        '''
        result = self._values.get("integration_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the pass-through behavior for incoming requests based on the ``Content-Type`` header in the request, and the available mapping templates specified as the ``requestTemplates`` property on the ``Integration`` resource.

        There are three valid values: ``WHEN_NO_MATCH`` , ``WHEN_NO_TEMPLATES`` , and ``NEVER`` . Supported only for WebSocket APIs.

        ``WHEN_NO_MATCH`` passes the request body for unmapped content types through to the integration backend without transformation.

        ``NEVER`` rejects unmapped content types with an ``HTTP 415 Unsupported Media Type`` response.

        ``WHEN_NO_TEMPLATES`` allows pass-through when the integration has no content types mapped to templates. However, if there is at least one content type defined, unmapped content types will be rejected with the same ``HTTP 415 Unsupported Media Type`` response.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        '''
        result = self._values.get("passthrough_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_format_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the format of the payload sent to an integration.

        Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are ``1.0`` and ``2.0`` . For all other integrations, ``1.0`` is the only supported value. To learn more, see `Working with AWS Lambda proxy integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_parameters(self) -> typing.Any:
        '''For WebSocket APIs, a key-value map specifying request parameters that are passed from the method request to the backend.

        The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the backend. The method request parameter value must match the pattern of ``method.request. {location} . {name}`` , where ``{location}`` is ``querystring`` , ``path`` , or ``header`` ; and ``{name}`` must be a valid and unique method request parameter name.

        For HTTP API integrations with a specified ``integrationSubtype`` , request parameters are a key-value map specifying parameters that are passed to ``AWS_PROXY`` integrations. You can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Working with AWS service integrations for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services.html>`_ .

        For HTTP API integrations without a specified ``integrationSubtype`` request parameters are a key-value map specifying how to transform HTTP requests before sending them to the backend. The key should follow the pattern :<header|querystring|path>. where action can be ``append`` , ``overwrite`` or ``remove`` . For values, you can provide static values, or map request data, stage variables, or context variables that are evaluated at runtime. To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        '''
        result = self._values.get("request_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def request_templates(self) -> typing.Any:
        '''Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.

        The content type value is the key in this map, and the template (as a String) is the value. Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        '''
        result = self._values.get("request_templates")
        return typing.cast(typing.Any, result)

    @builtins.property
    def response_parameters(self) -> typing.Any:
        '''Supported only for HTTP APIs.

        You use response parameters to transform the HTTP response from a backend integration before returning the response to clients. Specify a key-value map from a selection key to response parameters. The selection key must be a valid HTTP status code within the range of 200-599. The value is of type ```ResponseParameterList`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-responseparameterlist.html>`_ . To learn more, see `Transforming API requests and responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-responseparameters
        '''
        result = self._values.get("response_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The template selection expression for the integration.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        '''
        result = self._values.get("template_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        '''Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and between 50 and 30,000 milliseconds for HTTP APIs.

        The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        '''
        result = self._values.get("timeout_in_millis")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIntegration.TlsConfigProperty]]:
        '''The TLS configuration for a private integration.

        If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIntegration.TlsConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegrationResponse(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponse",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::IntegrationResponse``.

    The ``AWS::ApiGatewayV2::IntegrationResponse`` resource updates an integration response for an WebSocket API. For more information, see `Set up WebSocket API Integration Responses in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-responses.html>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::IntegrationResponse
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # response_parameters: Any
        # response_templates: Any
        
        cfn_integration_response = apigatewayv2.CfnIntegrationResponse(self, "MyCfnIntegrationResponse",
            api_id="apiId",
            integration_id="integrationId",
            integration_response_key="integrationResponseKey",
        
            # the properties below are optional
            content_handling_strategy="contentHandlingStrategy",
            response_parameters=response_parameters,
            response_templates=response_templates,
            template_selection_expression="templateSelectionExpression"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration_id: builtins.str,
        integration_response_key: builtins.str,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        response_parameters: typing.Any = None,
        response_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :param integration_response_key: The integration response key.
        :param content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob. ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string. If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.
        :param response_parameters: A key-value map specifying response parameters that are passed to the method response from the backend. The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header. *{name}*`` , where name is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header. *{name}*`` or ``integration.response.body. *{JSON-expression}*`` , where ``*{name}*`` is a valid and unique response header name and ``*{JSON-expression}*`` is a valid JSON expression without the ``$`` prefix.
        :param response_templates: The collection of response templates for the integration response as a string-to-string map of key-value pairs. Response templates are represented as a key/value map, with a content-type as the key and a template as the value.
        :param template_selection_expression: The template selection expression for the integration response. Supported only for WebSocket APIs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegrationResponse.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIntegrationResponseProps(
            api_id=api_id,
            integration_id=integration_id,
            integration_response_key=integration_response_key,
            content_handling_strategy=content_handling_strategy,
            response_parameters=response_parameters,
            response_templates=response_templates,
            template_selection_expression=template_selection_expression,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegrationResponse.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegrationResponse._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        '''The integration ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationId"))

    @integration_id.setter
    def integration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "integration_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationResponseKey")
    def integration_response_key(self) -> builtins.str:
        '''The integration response key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationResponseKey"))

    @integration_response_key.setter
    def integration_response_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "integration_response_key").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        '''A key-value map specifying response parameters that are passed to the method response from the backend.

        The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header. *{name}*`` , where name is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header. *{name}*`` or ``integration.response.body. *{JSON-expression}*`` , where ``*{name}*`` is a valid and unique response header name and ``*{JSON-expression}*`` is a valid JSON expression without the ``$`` prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "responseParameters"))

    @response_parameters.setter
    def response_parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "response_parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="responseTemplates")
    def response_templates(self) -> typing.Any:
        '''The collection of response templates for the integration response as a string-to-string map of key-value pairs.

        Response templates are represented as a key/value map, with a content-type as the key and a template as the value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        '''
        return typing.cast(typing.Any, jsii.get(self, "responseTemplates"))

    @response_templates.setter
    def response_templates(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "response_templates").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        '''Supported only for WebSocket APIs.

        Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

        ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob.

        ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string.

        If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentHandlingStrategy"))

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "content_handling_strategy").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The template selection expression for the integration response.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateSelectionExpression"))

    @template_selection_expression.setter
    def template_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnIntegrationResponse, "template_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateSelectionExpression", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponseProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration_id": "integrationId",
        "integration_response_key": "integrationResponseKey",
        "content_handling_strategy": "contentHandlingStrategy",
        "response_parameters": "responseParameters",
        "response_templates": "responseTemplates",
        "template_selection_expression": "templateSelectionExpression",
    },
)
class CfnIntegrationResponseProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration_id: builtins.str,
        integration_response_key: builtins.str,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        response_parameters: typing.Any = None,
        response_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnIntegrationResponse``.

        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :param integration_response_key: The integration response key.
        :param content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob. ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string. If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.
        :param response_parameters: A key-value map specifying response parameters that are passed to the method response from the backend. The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header. *{name}*`` , where name is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header. *{name}*`` or ``integration.response.body. *{JSON-expression}*`` , where ``*{name}*`` is a valid and unique response header name and ``*{JSON-expression}*`` is a valid JSON expression without the ``$`` prefix.
        :param response_templates: The collection of response templates for the integration response as a string-to-string map of key-value pairs. Response templates are represented as a key/value map, with a content-type as the key and a template as the value.
        :param template_selection_expression: The template selection expression for the integration response. Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # response_parameters: Any
            # response_templates: Any
            
            cfn_integration_response_props = apigatewayv2.CfnIntegrationResponseProps(
                api_id="apiId",
                integration_id="integrationId",
                integration_response_key="integrationResponseKey",
            
                # the properties below are optional
                content_handling_strategy="contentHandlingStrategy",
                response_parameters=response_parameters,
                response_templates=response_templates,
                template_selection_expression="templateSelectionExpression"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnIntegrationResponseProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument integration_id", value=integration_id, expected_type=type_hints["integration_id"])
            check_type(argname="argument integration_response_key", value=integration_response_key, expected_type=type_hints["integration_response_key"])
            check_type(argname="argument content_handling_strategy", value=content_handling_strategy, expected_type=type_hints["content_handling_strategy"])
            check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
            check_type(argname="argument response_templates", value=response_templates, expected_type=type_hints["response_templates"])
            check_type(argname="argument template_selection_expression", value=template_selection_expression, expected_type=type_hints["template_selection_expression"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "integration_id": integration_id,
            "integration_response_key": integration_response_key,
        }
        if content_handling_strategy is not None:
            self._values["content_handling_strategy"] = content_handling_strategy
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters
        if response_templates is not None:
            self._values["response_templates"] = response_templates
        if template_selection_expression is not None:
            self._values["template_selection_expression"] = template_selection_expression

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_id(self) -> builtins.str:
        '''The integration ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        '''
        result = self._values.get("integration_id")
        assert result is not None, "Required property 'integration_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_response_key(self) -> builtins.str:
        '''The integration response key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        '''
        result = self._values.get("integration_response_key")
        assert result is not None, "Required property 'integration_response_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        '''Supported only for WebSocket APIs.

        Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

        ``CONVERT_TO_BINARY`` : Converts a response payload from a Base64-encoded string to the corresponding binary blob.

        ``CONVERT_TO_TEXT`` : Converts a response payload from a binary blob to a Base64-encoded string.

        If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        '''
        result = self._values.get("content_handling_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_parameters(self) -> typing.Any:
        '''A key-value map specifying response parameters that are passed to the method response from the backend.

        The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header. *{name}*`` , where name is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header. *{name}*`` or ``integration.response.body. *{JSON-expression}*`` , where ``*{name}*`` is a valid and unique response header name and ``*{JSON-expression}*`` is a valid JSON expression without the ``$`` prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        '''
        result = self._values.get("response_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def response_templates(self) -> typing.Any:
        '''The collection of response templates for the integration response as a string-to-string map of key-value pairs.

        Response templates are represented as a key/value map, with a content-type as the key and a template as the value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        '''
        result = self._values.get("response_templates")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The template selection expression for the integration response.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        '''
        result = self._values.get("template_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModel(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnModel",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Model``.

    The ``AWS::ApiGatewayV2::Model`` resource updates data model for a WebSocket API. For more information, see `Model Selection Expressions <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-selection-expressions.html#apigateway-websocket-api-model-selection-expressions>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::Model
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # schema: Any
        
        cfn_model = apigatewayv2.CfnModel(self, "MyCfnModel",
            api_id="apiId",
            name="name",
            schema=schema,
        
            # the properties below are optional
            content_type="contentType",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        name: builtins.str,
        schema: typing.Any,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param name: The name of the model.
        :param schema: The schema for the model. For application/json models, this should be JSON schema draft 4 model.
        :param content_type: The content-type for the model, for example, "application/json".
        :param description: The description of the model.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModel.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnModelProps(
            api_id=api_id,
            name=name,
            schema=schema,
            content_type=content_type,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModel.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModel._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModel, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModel, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        '''The schema for the model.

        For application/json models, this should be JSON schema draft 4 model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        '''
        return typing.cast(typing.Any, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModel, "schema").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The content-type for the model, for example, "application/json".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModel, "content_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModel, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "name": "name",
        "schema": "schema",
        "content_type": "contentType",
        "description": "description",
    },
)
class CfnModelProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        name: builtins.str,
        schema: typing.Any,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnModel``.

        :param api_id: The API identifier.
        :param name: The name of the model.
        :param schema: The schema for the model. For application/json models, this should be JSON schema draft 4 model.
        :param content_type: The content-type for the model, for example, "application/json".
        :param description: The description of the model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # schema: Any
            
            cfn_model_props = apigatewayv2.CfnModelProps(
                api_id="apiId",
                name="name",
                schema=schema,
            
                # the properties below are optional
                content_type="contentType",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModelProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "name": name,
            "schema": schema,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> typing.Any:
        '''The schema for the model.

        For application/json models, this should be JSON schema draft 4 model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The content-type for the model, for example, "application/json".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRoute(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Route``.

    The ``AWS::ApiGatewayV2::Route`` resource creates a route for an API.

    :cloudformationResource: AWS::ApiGatewayV2::Route
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # request_models: Any
        # request_parameters: Any
        
        cfn_route = apigatewayv2.CfnRoute(self, "MyCfnRoute",
            api_id="apiId",
            route_key="routeKey",
        
            # the properties below are optional
            api_key_required=False,
            authorization_scopes=["authorizationScopes"],
            authorization_type="authorizationType",
            authorizer_id="authorizerId",
            model_selection_expression="modelSelectionExpression",
            operation_name="operationName",
            request_models=request_models,
            request_parameters=request_parameters,
            route_response_selection_expression="routeResponseSelectionExpression",
            target="target"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        route_key: builtins.str,
        api_key_required: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
        model_selection_expression: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Any = None,
        request_parameters: typing.Any = None,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param route_key: The route key for the route. For HTTP APIs, the route key can be either ``$default`` , or a combination of an HTTP method and resource path, for example, ``GET /pets`` .
        :param api_key_required: Specifies whether an API key is required for the route. Supported only for WebSocket APIs.
        :param authorization_scopes: The authorization scopes supported by this route.
        :param authorization_type: The authorization type for the route. For WebSocket APIs, valid values are ``NONE`` for open access, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer. For HTTP APIs, valid values are ``NONE`` for open access, ``JWT`` for using JSON Web Tokens, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer.
        :param authorizer_id: The identifier of the ``Authorizer`` resource to be associated with this route. The authorizer identifier is generated by API Gateway when you created the authorizer.
        :param model_selection_expression: The model selection expression for the route. Supported only for WebSocket APIs.
        :param operation_name: The operation name for the route.
        :param request_models: The request models for the route. Supported only for WebSocket APIs.
        :param request_parameters: The request parameters for the route. Supported only for WebSocket APIs.
        :param route_response_selection_expression: The route response selection expression for the route. Supported only for WebSocket APIs.
        :param target: The target for the route.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRoute.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRouteProps(
            api_id=api_id,
            route_key=route_key,
            api_key_required=api_key_required,
            authorization_scopes=authorization_scopes,
            authorization_type=authorization_type,
            authorizer_id=authorizer_id,
            model_selection_expression=model_selection_expression,
            operation_name=operation_name,
            request_models=request_models,
            request_parameters=request_parameters,
            route_response_selection_expression=route_response_selection_expression,
            target=target,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRoute.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRoute._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="requestModels")
    def request_models(self) -> typing.Any:
        '''The request models for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        '''
        return typing.cast(typing.Any, jsii.get(self, "requestModels"))

    @request_models.setter
    def request_models(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "request_models").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestModels", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        '''The request parameters for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "requestParameters"))

    @request_parameters.setter
    def request_parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "request_parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        '''The route key for the route.

        For HTTP APIs, the route key can be either ``$default`` , or a combination of an HTTP method and resource path, for example, ``GET /pets`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeKey"))

    @route_key.setter
    def route_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "route_key").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeyRequired")
    def api_key_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether an API key is required for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "apiKeyRequired"))

    @api_key_required.setter
    def api_key_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "api_key_required").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeyRequired", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationScopes")
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The authorization scopes supported by this route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "authorizationScopes"))

    @authorization_scopes.setter
    def authorization_scopes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "authorization_scopes").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationScopes", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional[builtins.str]:
        '''The authorization type for the route.

        For WebSocket APIs, valid values are ``NONE`` for open access, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer. For HTTP APIs, valid values are ``NONE`` for open access, ``JWT`` for using JSON Web Tokens, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationType"))

    @authorization_type.setter
    def authorization_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "authorization_type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationType", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the ``Authorizer`` resource to be associated with this route.

        The authorizer identifier is generated by API Gateway when you created the authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "authorizer_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The model selection expression for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelSelectionExpression"))

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "model_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> typing.Optional[builtins.str]:
        '''The operation name for the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationName"))

    @operation_name.setter
    def operation_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "operation_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationName", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseSelectionExpression")
    def route_response_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The route response selection expression for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeResponseSelectionExpression"))

    @route_response_selection_expression.setter
    def route_response_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "route_response_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeResponseSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[builtins.str]:
        '''The target for the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "target"))

    @target.setter
    def target(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRoute, "target").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute.ParameterConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"required": "required"},
    )
    class ParameterConstraintsProperty:
        def __init__(
            self,
            *,
            required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        ) -> None:
            '''Specifies whether the parameter is required.

            :param required: Specifies whether the parameter is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                parameter_constraints_property = apigatewayv2.CfnRoute.ParameterConstraintsProperty(
                    required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnRoute.ParameterConstraintsProperty.__init__)
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            self._values: typing.Dict[str, typing.Any] = {
                "required": required,
            }

        @builtins.property
        def required(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            '''Specifies whether the parameter is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html#cfn-apigatewayv2-route-parameterconstraints-required
            '''
            result = self._values.get("required")
            assert result is not None, "Required property 'required' is missing"
            return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "route_key": "routeKey",
        "api_key_required": "apiKeyRequired",
        "authorization_scopes": "authorizationScopes",
        "authorization_type": "authorizationType",
        "authorizer_id": "authorizerId",
        "model_selection_expression": "modelSelectionExpression",
        "operation_name": "operationName",
        "request_models": "requestModels",
        "request_parameters": "requestParameters",
        "route_response_selection_expression": "routeResponseSelectionExpression",
        "target": "target",
    },
)
class CfnRouteProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        route_key: builtins.str,
        api_key_required: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
        model_selection_expression: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Any = None,
        request_parameters: typing.Any = None,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnRoute``.

        :param api_id: The API identifier.
        :param route_key: The route key for the route. For HTTP APIs, the route key can be either ``$default`` , or a combination of an HTTP method and resource path, for example, ``GET /pets`` .
        :param api_key_required: Specifies whether an API key is required for the route. Supported only for WebSocket APIs.
        :param authorization_scopes: The authorization scopes supported by this route.
        :param authorization_type: The authorization type for the route. For WebSocket APIs, valid values are ``NONE`` for open access, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer. For HTTP APIs, valid values are ``NONE`` for open access, ``JWT`` for using JSON Web Tokens, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer.
        :param authorizer_id: The identifier of the ``Authorizer`` resource to be associated with this route. The authorizer identifier is generated by API Gateway when you created the authorizer.
        :param model_selection_expression: The model selection expression for the route. Supported only for WebSocket APIs.
        :param operation_name: The operation name for the route.
        :param request_models: The request models for the route. Supported only for WebSocket APIs.
        :param request_parameters: The request parameters for the route. Supported only for WebSocket APIs.
        :param route_response_selection_expression: The route response selection expression for the route. Supported only for WebSocket APIs.
        :param target: The target for the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # request_models: Any
            # request_parameters: Any
            
            cfn_route_props = apigatewayv2.CfnRouteProps(
                api_id="apiId",
                route_key="routeKey",
            
                # the properties below are optional
                api_key_required=False,
                authorization_scopes=["authorizationScopes"],
                authorization_type="authorizationType",
                authorizer_id="authorizerId",
                model_selection_expression="modelSelectionExpression",
                operation_name="operationName",
                request_models=request_models,
                request_parameters=request_parameters,
                route_response_selection_expression="routeResponseSelectionExpression",
                target="target"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRouteProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument model_selection_expression", value=model_selection_expression, expected_type=type_hints["model_selection_expression"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument request_models", value=request_models, expected_type=type_hints["request_models"])
            check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
            check_type(argname="argument route_response_selection_expression", value=route_response_selection_expression, expected_type=type_hints["route_response_selection_expression"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "route_key": route_key,
        }
        if api_key_required is not None:
            self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None:
            self._values["authorization_type"] = authorization_type
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if model_selection_expression is not None:
            self._values["model_selection_expression"] = model_selection_expression
        if operation_name is not None:
            self._values["operation_name"] = operation_name
        if request_models is not None:
            self._values["request_models"] = request_models
        if request_parameters is not None:
            self._values["request_parameters"] = request_parameters
        if route_response_selection_expression is not None:
            self._values["route_response_selection_expression"] = route_response_selection_expression
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_key(self) -> builtins.str:
        '''The route key for the route.

        For HTTP APIs, the route key can be either ``$default`` , or a combination of an HTTP method and resource path, for example, ``GET /pets`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        '''
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether an API key is required for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        '''
        result = self._values.get("api_key_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The authorization scopes supported by this route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorization_type(self) -> typing.Optional[builtins.str]:
        '''The authorization type for the route.

        For WebSocket APIs, valid values are ``NONE`` for open access, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer. For HTTP APIs, valid values are ``NONE`` for open access, ``JWT`` for using JSON Web Tokens, ``AWS_IAM`` for using AWS IAM permissions, and ``CUSTOM`` for using a Lambda authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        '''
        result = self._values.get("authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the ``Authorizer`` resource to be associated with this route.

        The authorizer identifier is generated by API Gateway when you created the authorizer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        '''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The model selection expression for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        '''
        result = self._values.get("model_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_name(self) -> typing.Optional[builtins.str]:
        '''The operation name for the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        '''
        result = self._values.get("operation_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_models(self) -> typing.Any:
        '''The request models for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        '''
        result = self._values.get("request_models")
        return typing.cast(typing.Any, result)

    @builtins.property
    def request_parameters(self) -> typing.Any:
        '''The request parameters for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        '''
        result = self._values.get("request_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def route_response_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The route response selection expression for the route.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        '''
        result = self._values.get("route_response_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''The target for the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRouteResponse(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::RouteResponse``.

    The ``AWS::ApiGatewayV2::RouteResponse`` resource creates a route response for a WebSocket API. For more information, see `Set up Route Responses for a WebSocket API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-route-response.html>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::RouteResponse
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # response_models: Any
        # response_parameters: Any
        
        cfn_route_response = apigatewayv2.CfnRouteResponse(self, "MyCfnRouteResponse",
            api_id="apiId",
            route_id="routeId",
            route_response_key="routeResponseKey",
        
            # the properties below are optional
            model_selection_expression="modelSelectionExpression",
            response_models=response_models,
            response_parameters=response_parameters
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        route_id: builtins.str,
        route_response_key: builtins.str,
        model_selection_expression: typing.Optional[builtins.str] = None,
        response_models: typing.Any = None,
        response_parameters: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::RouteResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param route_id: The route ID.
        :param route_response_key: The route response key.
        :param model_selection_expression: The model selection expression for the route response. Supported only for WebSocket APIs.
        :param response_models: The response models for the route response.
        :param response_parameters: The route response parameters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRouteResponse.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRouteResponseProps(
            api_id=api_id,
            route_id=route_id,
            route_response_key=route_response_key,
            model_selection_expression=model_selection_expression,
            response_models=response_models,
            response_parameters=response_parameters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRouteResponse.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRouteResponse._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="responseModels")
    def response_models(self) -> typing.Any:
        '''The response models for the route response.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        '''
        return typing.cast(typing.Any, jsii.get(self, "responseModels"))

    @response_models.setter
    def response_models(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "response_models").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseModels", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        '''The route response parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "responseParameters"))

    @response_parameters.setter
    def response_parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "response_parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        '''The route ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeId"))

    @route_id.setter
    def route_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "route_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeId", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseKey")
    def route_response_key(self) -> builtins.str:
        '''The route response key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeResponseKey"))

    @route_response_key.setter
    def route_response_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "route_response_key").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The model selection expression for the route response.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelSelectionExpression"))

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnRouteResponse, "model_selection_expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelSelectionExpression", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse.ParameterConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"required": "required"},
    )
    class ParameterConstraintsProperty:
        def __init__(
            self,
            *,
            required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        ) -> None:
            '''Specifies whether the parameter is required.

            :param required: Specifies whether the parameter is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                parameter_constraints_property = apigatewayv2.CfnRouteResponse.ParameterConstraintsProperty(
                    required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnRouteResponse.ParameterConstraintsProperty.__init__)
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            self._values: typing.Dict[str, typing.Any] = {
                "required": required,
            }

        @builtins.property
        def required(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            '''Specifies whether the parameter is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html#cfn-apigatewayv2-routeresponse-parameterconstraints-required
            '''
            result = self._values.get("required")
            assert result is not None, "Required property 'required' is missing"
            return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponseProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "route_id": "routeId",
        "route_response_key": "routeResponseKey",
        "model_selection_expression": "modelSelectionExpression",
        "response_models": "responseModels",
        "response_parameters": "responseParameters",
    },
)
class CfnRouteResponseProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        route_id: builtins.str,
        route_response_key: builtins.str,
        model_selection_expression: typing.Optional[builtins.str] = None,
        response_models: typing.Any = None,
        response_parameters: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnRouteResponse``.

        :param api_id: The API identifier.
        :param route_id: The route ID.
        :param route_response_key: The route response key.
        :param model_selection_expression: The model selection expression for the route response. Supported only for WebSocket APIs.
        :param response_models: The response models for the route response.
        :param response_parameters: The route response parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # response_models: Any
            # response_parameters: Any
            
            cfn_route_response_props = apigatewayv2.CfnRouteResponseProps(
                api_id="apiId",
                route_id="routeId",
                route_response_key="routeResponseKey",
            
                # the properties below are optional
                model_selection_expression="modelSelectionExpression",
                response_models=response_models,
                response_parameters=response_parameters
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnRouteResponseProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument route_id", value=route_id, expected_type=type_hints["route_id"])
            check_type(argname="argument route_response_key", value=route_response_key, expected_type=type_hints["route_response_key"])
            check_type(argname="argument model_selection_expression", value=model_selection_expression, expected_type=type_hints["model_selection_expression"])
            check_type(argname="argument response_models", value=response_models, expected_type=type_hints["response_models"])
            check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "route_id": route_id,
            "route_response_key": route_response_key,
        }
        if model_selection_expression is not None:
            self._values["model_selection_expression"] = model_selection_expression
        if response_models is not None:
            self._values["response_models"] = response_models
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_id(self) -> builtins.str:
        '''The route ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        '''
        result = self._values.get("route_id")
        assert result is not None, "Required property 'route_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_response_key(self) -> builtins.str:
        '''The route response key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        '''
        result = self._values.get("route_response_key")
        assert result is not None, "Required property 'route_response_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        '''The model selection expression for the route response.

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        '''
        result = self._values.get("model_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_models(self) -> typing.Any:
        '''The response models for the route response.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        '''
        result = self._values.get("response_models")
        return typing.cast(typing.Any, result)

    @builtins.property
    def response_parameters(self) -> typing.Any:
        '''The route response parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        '''
        result = self._values.get("response_parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStage(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::Stage``.

    The ``AWS::ApiGatewayV2::Stage`` resource specifies a stage for an API. Each stage is a named reference to a deployment of the API and is made available for client applications to call. To learn more, see `Working with stages for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-stages.html>`_ and `Deploy a WebSocket API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-set-up-websocket-deployment.html>`_ .

    :cloudformationResource: AWS::ApiGatewayV2::Stage
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # route_settings: Any
        # stage_variables: Any
        # tags: Any
        
        cfn_stage = apigatewayv2.CfnStage(self, "MyCfnStage",
            api_id="apiId",
            stage_name="stageName",
        
            # the properties below are optional
            access_log_settings=apigatewayv2.CfnStage.AccessLogSettingsProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            access_policy_id="accessPolicyId",
            auto_deploy=False,
            client_certificate_id="clientCertificateId",
            default_route_settings=apigatewayv2.CfnStage.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            deployment_id="deploymentId",
            description="description",
            route_settings=route_settings,
            stage_variables=stage_variables,
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        stage_name: builtins.str,
        access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStage.AccessLogSettingsProperty", typing.Dict[str, typing.Any]]]] = None,
        access_policy_id: typing.Optional[builtins.str] = None,
        auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        client_certificate_id: typing.Optional[builtins.str] = None,
        default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStage.RouteSettingsProperty", typing.Dict[str, typing.Any]]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        route_settings: typing.Any = None,
        stage_variables: typing.Any = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::Stage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API identifier.
        :param stage_name: The stage name. Stage names can contain only alphanumeric characters, hyphens, and underscores, or be ``$default`` . Maximum length is 128 characters.
        :param access_log_settings: Settings for logging access in this stage.
        :param access_policy_id: This parameter is not currently supported.
        :param auto_deploy: Specifies whether updates to an API automatically trigger a new deployment. The default value is ``false`` .
        :param client_certificate_id: The identifier of a client certificate for a ``Stage`` . Supported only for WebSocket APIs.
        :param default_route_settings: The default route settings for the stage.
        :param deployment_id: The deployment identifier for the API stage. Can't be updated if ``autoDeploy`` is enabled.
        :param description: The description for the API stage.
        :param route_settings: Route settings for the stage.
        :param stage_variables: A map that defines the stage variables for a ``Stage`` . Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStage.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStageProps(
            api_id=api_id,
            stage_name=stage_name,
            access_log_settings=access_log_settings,
            access_policy_id=access_policy_id,
            auto_deploy=auto_deploy,
            client_certificate_id=client_certificate_id,
            default_route_settings=default_route_settings,
            deployment_id=deployment_id,
            description=description,
            route_settings=route_settings,
            stage_variables=stage_variables,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStage.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStage._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "api_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="routeSettings")
    def route_settings(self) -> typing.Any:
        '''Route settings for the stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        '''
        return typing.cast(typing.Any, jsii.get(self, "routeSettings"))

    @route_settings.setter
    def route_settings(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "route_settings").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''The stage name.

        Stage names can contain only alphanumeric characters, hyphens, and underscores, or be ``$default`` . Maximum length is 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "stage_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(self) -> typing.Any:
        '''A map that defines the stage variables for a ``Stage`` .

        Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        '''
        return typing.cast(typing.Any, jsii.get(self, "stageVariables"))

    @stage_variables.setter
    def stage_variables(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "stage_variables").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageVariables", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSettings")
    def access_log_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]]:
        '''Settings for logging access in this stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]], jsii.get(self, "accessLogSettings"))

    @access_log_settings.setter
    def access_log_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "access_log_settings").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLogSettings", value)

    @builtins.property
    @jsii.member(jsii_name="accessPolicyId")
    def access_policy_id(self) -> typing.Optional[builtins.str]:
        '''This parameter is not currently supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesspolicyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPolicyId"))

    @access_policy_id.setter
    def access_policy_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "access_policy_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether updates to an API automatically trigger a new deployment.

        The default value is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "autoDeploy"))

    @auto_deploy.setter
    def auto_deploy(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "auto_deploy").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeploy", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a client certificate for a ``Stage`` .

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateId"))

    @client_certificate_id.setter
    def client_certificate_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "client_certificate_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]]:
        '''The default route settings for the stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]], jsii.get(self, "defaultRouteSettings"))

    @default_route_settings.setter
    def default_route_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "default_route_settings").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''The deployment identifier for the API stage.

        Can't be updated if ``autoDeploy`` is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "deployment_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the API stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStage, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.AccessLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingsProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for logging access in a stage.

            :param destination_arn: The ARN of the CloudWatch Logs log group to receive access logs. This parameter is required to enable access logging.
            :param format: A single line format of the access logs of data, as specified by selected $context variables. The format must include at least $context.requestId. This parameter is required to enable access logging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                access_log_settings_property = apigatewayv2.CfnStage.AccessLogSettingsProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStage.AccessLogSettingsProperty.__init__)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch Logs log group to receive access logs.

            This parameter is required to enable access logging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''A single line format of the access logs of data, as specified by selected $context variables.

            The format must include at least $context.requestId. This parameter is required to enable access logging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents a collection of route settings.

            :param data_trace_enabled: Specifies whether ( ``true`` ) or not ( ``false`` ) data trace logging is enabled for this route. This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.
            :param detailed_metrics_enabled: Specifies whether detailed metrics are enabled.
            :param logging_level: Specifies the logging level for this route: ``INFO`` , ``ERROR`` , or ``OFF`` . This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.
            :param throttling_burst_limit: Specifies the throttling burst limit.
            :param throttling_rate_limit: Specifies the throttling rate limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apigatewayv2 as apigatewayv2
                
                route_settings_property = apigatewayv2.CfnStage.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStage.RouteSettingsProperty.__init__)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether ( ``true`` ) or not ( ``false`` ) data trace logging is enabled for this route.

            This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''Specifies whether detailed metrics are enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the logging level for this route: ``INFO`` , ``ERROR`` , or ``OFF`` .

            This property affects the log entries pushed to Amazon CloudWatch Logs. Supported only for WebSocket APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling burst limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling rate limit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnStageProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "stage_name": "stageName",
        "access_log_settings": "accessLogSettings",
        "access_policy_id": "accessPolicyId",
        "auto_deploy": "autoDeploy",
        "client_certificate_id": "clientCertificateId",
        "default_route_settings": "defaultRouteSettings",
        "deployment_id": "deploymentId",
        "description": "description",
        "route_settings": "routeSettings",
        "stage_variables": "stageVariables",
        "tags": "tags",
    },
)
class CfnStageProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        stage_name: builtins.str,
        access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStage.AccessLogSettingsProperty, typing.Dict[str, typing.Any]]]] = None,
        access_policy_id: typing.Optional[builtins.str] = None,
        auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        client_certificate_id: typing.Optional[builtins.str] = None,
        default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStage.RouteSettingsProperty, typing.Dict[str, typing.Any]]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        route_settings: typing.Any = None,
        stage_variables: typing.Any = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnStage``.

        :param api_id: The API identifier.
        :param stage_name: The stage name. Stage names can contain only alphanumeric characters, hyphens, and underscores, or be ``$default`` . Maximum length is 128 characters.
        :param access_log_settings: Settings for logging access in this stage.
        :param access_policy_id: This parameter is not currently supported.
        :param auto_deploy: Specifies whether updates to an API automatically trigger a new deployment. The default value is ``false`` .
        :param client_certificate_id: The identifier of a client certificate for a ``Stage`` . Supported only for WebSocket APIs.
        :param default_route_settings: The default route settings for the stage.
        :param deployment_id: The deployment identifier for the API stage. Can't be updated if ``autoDeploy`` is enabled.
        :param description: The description for the API stage.
        :param route_settings: Route settings for the stage.
        :param stage_variables: A map that defines the stage variables for a ``Stage`` . Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # route_settings: Any
            # stage_variables: Any
            # tags: Any
            
            cfn_stage_props = apigatewayv2.CfnStageProps(
                api_id="apiId",
                stage_name="stageName",
            
                # the properties below are optional
                access_log_settings=apigatewayv2.CfnStage.AccessLogSettingsProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                access_policy_id="accessPolicyId",
                auto_deploy=False,
                client_certificate_id="clientCertificateId",
                default_route_settings=apigatewayv2.CfnStage.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                deployment_id="deploymentId",
                description="description",
                route_settings=route_settings,
                stage_variables=stage_variables,
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStageProps.__init__)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument access_log_settings", value=access_log_settings, expected_type=type_hints["access_log_settings"])
            check_type(argname="argument access_policy_id", value=access_policy_id, expected_type=type_hints["access_policy_id"])
            check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
            check_type(argname="argument client_certificate_id", value=client_certificate_id, expected_type=type_hints["client_certificate_id"])
            check_type(argname="argument default_route_settings", value=default_route_settings, expected_type=type_hints["default_route_settings"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
            check_type(argname="argument stage_variables", value=stage_variables, expected_type=type_hints["stage_variables"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "stage_name": stage_name,
        }
        if access_log_settings is not None:
            self._values["access_log_settings"] = access_log_settings
        if access_policy_id is not None:
            self._values["access_policy_id"] = access_policy_id
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if client_certificate_id is not None:
            self._values["client_certificate_id"] = client_certificate_id
        if default_route_settings is not None:
            self._values["default_route_settings"] = default_route_settings
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id
        if description is not None:
            self._values["description"] = description
        if route_settings is not None:
            self._values["route_settings"] = route_settings
        if stage_variables is not None:
            self._values["stage_variables"] = stage_variables
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''The stage name.

        Stage names can contain only alphanumeric characters, hyphens, and underscores, or be ``$default`` . Maximum length is 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_log_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.AccessLogSettingsProperty]]:
        '''Settings for logging access in this stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        '''
        result = self._values.get("access_log_settings")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.AccessLogSettingsProperty]], result)

    @builtins.property
    def access_policy_id(self) -> typing.Optional[builtins.str]:
        '''This parameter is not currently supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesspolicyid
        '''
        result = self._values.get("access_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_deploy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Specifies whether updates to an API automatically trigger a new deployment.

        The default value is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        '''
        result = self._values.get("auto_deploy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a client certificate for a ``Stage`` .

        Supported only for WebSocket APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        '''
        result = self._values.get("client_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.RouteSettingsProperty]]:
        '''The default route settings for the stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        '''
        result = self._values.get("default_route_settings")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.RouteSettingsProperty]], result)

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''The deployment identifier for the API stage.

        Can't be updated if ``autoDeploy`` is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        '''
        result = self._values.get("deployment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the API stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_settings(self) -> typing.Any:
        '''Route settings for the stage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        '''
        result = self._values.get("route_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stage_variables(self) -> typing.Any:
        '''A map that defines the stage variables for a ``Stage`` .

        Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        '''
        result = self._values.get("stage_variables")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVpcLink(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnVpcLink",
):
    '''A CloudFormation ``AWS::ApiGatewayV2::VpcLink``.

    The ``AWS::ApiGatewayV2::VpcLink`` resource creates a VPC link. Supported only for HTTP APIs. The VPC link status must transition from ``PENDING`` to ``AVAILABLE`` to successfully create a VPC link, which can take up to 10 minutes. To learn more, see `Working with VPC Links for HTTP APIs <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vpc-links.html>`_ in the *API Gateway Developer Guide* .

    :cloudformationResource: AWS::ApiGatewayV2::VpcLink
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        cfn_vpc_link = apigatewayv2.CfnVpcLink(self, "MyCfnVpcLink",
            name="name",
            subnet_ids=["subnetIds"],
        
            # the properties below are optional
            security_group_ids=["securityGroupIds"],
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ApiGatewayV2::VpcLink``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the VPC link.
        :param subnet_ids: A list of subnet IDs to include in the VPC link.
        :param security_group_ids: A list of security group IDs for the VPC link.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnVpcLink.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVpcLinkProps(
            name=name,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnVpcLink.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnVpcLink._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcLinkId")
    def attr_vpc_link_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VpcLinkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcLinkId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnVpcLink, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of subnet IDs to include in the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnVpcLink, "subnet_ids").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs for the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnVpcLink, "security_group_ids").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnVpcLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "subnet_ids": "subnetIds",
        "security_group_ids": "securityGroupIds",
        "tags": "tags",
    },
)
class CfnVpcLinkProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVpcLink``.

        :param name: The name of the VPC link.
        :param subnet_ids: A list of subnet IDs to include in the VPC link.
        :param security_group_ids: A list of security group IDs for the VPC link.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            cfn_vpc_link_props = apigatewayv2.CfnVpcLinkProps(
                name="name",
                subnet_ids=["subnetIds"],
            
                # the properties below are optional
                security_group_ids=["securityGroupIds"],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnVpcLinkProps.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "subnet_ids": subnet_ids,
        }
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of subnet IDs to include in the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs for the VPC link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.CorsHttpMethod")
class CorsHttpMethod(enum.Enum):
    '''(experimental) Supported CORS HTTP methods.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apigwv2.HttpApi(self, "HttpProxyApi",
            cors_preflight=apigwv2.CorsPreflightOptions(
                allow_headers=["Authorization"],
                allow_methods=[apigwv2.CorsHttpMethod.GET, apigwv2.CorsHttpMethod.HEAD, apigwv2.CorsHttpMethod.OPTIONS, apigwv2.CorsHttpMethod.POST
                ],
                allow_origins=["*"],
                max_age=Duration.days(10)
            )
        )
    '''

    ANY = "ANY"
    '''(experimental) HTTP ANY.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) HTTP DELETE.

    :stability: experimental
    '''
    GET = "GET"
    '''(experimental) HTTP GET.

    :stability: experimental
    '''
    HEAD = "HEAD"
    '''(experimental) HTTP HEAD.

    :stability: experimental
    '''
    OPTIONS = "OPTIONS"
    '''(experimental) HTTP OPTIONS.

    :stability: experimental
    '''
    PATCH = "PATCH"
    '''(experimental) HTTP PATCH.

    :stability: experimental
    '''
    POST = "POST"
    '''(experimental) HTTP POST.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) HTTP PUT.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CorsPreflightOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_credentials": "allowCredentials",
        "allow_headers": "allowHeaders",
        "allow_methods": "allowMethods",
        "allow_origins": "allowOrigins",
        "expose_headers": "exposeHeaders",
        "max_age": "maxAge",
    },
)
class CorsPreflightOptions:
    def __init__(
        self,
        *,
        allow_credentials: typing.Optional[builtins.bool] = None,
        allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_methods: typing.Optional[typing.Sequence[CorsHttpMethod]] = None,
        allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''(experimental) Options for the CORS Configuration.

        :param allow_credentials: (experimental) Specifies whether credentials are included in the CORS request. Default: false
        :param allow_headers: (experimental) Represents a collection of allowed headers. Default: - No Headers are allowed.
        :param allow_methods: (experimental) Represents a collection of allowed HTTP methods. Default: - No Methods are allowed.
        :param allow_origins: (experimental) Represents a collection of allowed origins. Default: - No Origins are allowed.
        :param expose_headers: (experimental) Represents a collection of exposed headers. Default: - No Expose Headers are allowed.
        :param max_age: (experimental) The duration that the browser should cache preflight request results. Default: Duration.seconds(0)

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apigwv2.HttpApi(self, "HttpProxyApi",
                cors_preflight=apigwv2.CorsPreflightOptions(
                    allow_headers=["Authorization"],
                    allow_methods=[apigwv2.CorsHttpMethod.GET, apigwv2.CorsHttpMethod.HEAD, apigwv2.CorsHttpMethod.OPTIONS, apigwv2.CorsHttpMethod.POST
                    ],
                    allow_origins=["*"],
                    max_age=Duration.days(10)
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CorsPreflightOptions.__init__)
            check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
            check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
            check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
            check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
            check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None:
            self._values["allow_headers"] = allow_headers
        if allow_methods is not None:
            self._values["allow_methods"] = allow_methods
        if allow_origins is not None:
            self._values["allow_origins"] = allow_origins
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allow_credentials(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether credentials are included in the CORS request.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Represents a collection of allowed headers.

        :default: - No Headers are allowed.

        :stability: experimental
        '''
        result = self._values.get("allow_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[CorsHttpMethod]]:
        '''(experimental) Represents a collection of allowed HTTP methods.

        :default: - No Methods are allowed.

        :stability: experimental
        '''
        result = self._values.get("allow_methods")
        return typing.cast(typing.Optional[typing.List[CorsHttpMethod]], result)

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Represents a collection of allowed origins.

        :default: - No Origins are allowed.

        :stability: experimental
        '''
        result = self._values.get("allow_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Represents a collection of exposed headers.

        :default: - No Expose Headers are allowed.

        :stability: experimental
        '''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) The duration that the browser should cache preflight request results.

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CorsPreflightOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainMappingOptions",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "mapping_key": "mappingKey"},
)
class DomainMappingOptions:
    def __init__(
        self,
        *,
        domain_name: "IDomainName",
        mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for DomainMapping.

        :param domain_name: (experimental) The domain name for the mapping.
        :param mapping_key: (experimental) The API mapping key. Leave it undefined for the root path mapping. Default: - empty key for the root path mapping

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
            
            # handler: lambda.Function
            # dn: apigwv2.DomainName
            
            
            api_demo = apigwv2.HttpApi(self, "DemoApi",
                default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
                # https://${dn.domainName}/demo goes to apiDemo $default stage
                default_domain_mapping=apigwv2.DomainMappingOptions(
                    domain_name=dn,
                    mapping_key="demo"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainMappingOptions.__init__)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument mapping_key", value=mapping_key, expected_type=type_hints["mapping_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if mapping_key is not None:
            self._values["mapping_key"] = mapping_key

    @builtins.property
    def domain_name(self) -> "IDomainName":
        '''(experimental) The domain name for the mapping.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast("IDomainName", result)

    @builtins.property
    def mapping_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The API mapping key.

        Leave it undefined for the root path mapping.

        :default: - empty key for the root path mapping

        :stability: experimental
        '''
        result = self._values.get("mapping_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainMappingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainNameAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "regional_domain_name": "regionalDomainName",
        "regional_hosted_zone_id": "regionalHostedZoneId",
    },
)
class DomainNameAttributes:
    def __init__(
        self,
        *,
        name: builtins.str,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> None:
        '''(experimental) custom domain name attributes.

        :param name: (experimental) domain name string.
        :param regional_domain_name: (experimental) The domain name associated with the regional endpoint for this custom domain name.
        :param regional_hosted_zone_id: (experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            domain_name_attributes = apigatewayv2.DomainNameAttributes(
                name="name",
                regional_domain_name="regionalDomainName",
                regional_hosted_zone_id="regionalHostedZoneId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainNameAttributes.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regional_domain_name", value=regional_domain_name, expected_type=type_hints["regional_domain_name"])
            check_type(argname="argument regional_hosted_zone_id", value=regional_hosted_zone_id, expected_type=type_hints["regional_hosted_zone_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "regional_domain_name": regional_domain_name,
            "regional_hosted_zone_id": regional_hosted_zone_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) domain name string.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        '''
        result = self._values.get("regional_domain_name")
        assert result is not None, "Required property 'regional_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regional_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        '''
        result = self._values.get("regional_hosted_zone_id")
        assert result is not None, "Required property 'regional_hosted_zone_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainNameAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.EndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "certificate_name": "certificateName",
        "endpoint_type": "endpointType",
        "ownership_certificate": "ownershipCertificate",
        "security_policy": "securityPolicy",
    },
)
class EndpointOptions:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        certificate_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional["EndpointType"] = None,
        ownership_certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        security_policy: typing.Optional["SecurityPolicy"] = None,
    ) -> None:
        '''(experimental) properties for creating a domain name endpoint.

        :param certificate: (experimental) The ACM certificate for this domain name. Certificate can be both ACM issued or imported.
        :param certificate_name: (experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name. Default: - No friendly certificate name
        :param endpoint_type: (experimental) The type of endpoint for this DomainName. Default: EndpointType.REGIONAL
        :param ownership_certificate: (experimental) A public certificate issued by ACM to validate that you own a custom domain. This parameter is required only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate for ``certificate``. The ownership certificate validates that you have permissions to use the domain name. Default: - only required when configuring mTLS
        :param security_policy: (experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name. Default: SecurityPolicy.TLS_1_2

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_certificatemanager as certificatemanager
            
            # certificate: certificatemanager.Certificate
            
            endpoint_options = apigatewayv2.EndpointOptions(
                certificate=certificate,
            
                # the properties below are optional
                certificate_name="certificateName",
                endpoint_type=apigatewayv2.EndpointType.EDGE,
                ownership_certificate=certificate,
                security_policy=apigatewayv2.SecurityPolicy.TLS_1_0
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EndpointOptions.__init__)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument ownership_certificate", value=ownership_certificate, expected_type=type_hints["ownership_certificate"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
        }
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if ownership_certificate is not None:
            self._values["ownership_certificate"] = ownership_certificate
        if security_policy is not None:
            self._values["security_policy"] = security_policy

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        '''(experimental) The ACM certificate for this domain name.

        Certificate can be both ACM issued or imported.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(aws_cdk.aws_certificatemanager.ICertificate, result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name.

        :default: - No friendly certificate name

        :stability: experimental
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional["EndpointType"]:
        '''(experimental) The type of endpoint for this DomainName.

        :default: EndpointType.REGIONAL

        :stability: experimental
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional["EndpointType"], result)

    @builtins.property
    def ownership_certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        '''(experimental) A public certificate issued by ACM to validate that you own a custom domain.

        This parameter is required
        only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate
        for ``certificate``. The ownership certificate validates that you have permissions to use the domain name.

        :default: - only required when configuring mTLS

        :stability: experimental
        '''
        result = self._values.get("ownership_certificate")
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], result)

    @builtins.property
    def security_policy(self) -> typing.Optional["SecurityPolicy"]:
        '''(experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name.

        :default: SecurityPolicy.TLS_1_2

        :stability: experimental
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional["SecurityPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.EndpointType")
class EndpointType(enum.Enum):
    '''(experimental) Endpoint type for a domain name.

    :stability: experimental
    '''

    EDGE = "EDGE"
    '''(experimental) For an edge-optimized custom domain name.

    :stability: experimental
    '''
    REGIONAL = "REGIONAL"
    '''(experimental) For a regional custom domain name.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.GrantInvokeOptions",
    jsii_struct_bases=[],
    name_mapping={"http_methods": "httpMethods"},
)
class GrantInvokeOptions:
    def __init__(
        self,
        *,
        http_methods: typing.Optional[typing.Sequence["HttpMethod"]] = None,
    ) -> None:
        '''(experimental) Options for granting invoke access.

        :param http_methods: (experimental) The HTTP methods to allow. Default: - the HttpMethod of the route

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            grant_invoke_options = apigatewayv2.GrantInvokeOptions(
                http_methods=[apigatewayv2.HttpMethod.ANY]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GrantInvokeOptions.__init__)
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
        self._values: typing.Dict[str, typing.Any] = {}
        if http_methods is not None:
            self._values["http_methods"] = http_methods

    @builtins.property
    def http_methods(self) -> typing.Optional[typing.List["HttpMethod"]]:
        '''(experimental) The HTTP methods to allow.

        :default: - the HttpMethod of the route

        :stability: experimental
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional[typing.List["HttpMethod"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantInvokeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiAttributes",
    jsii_struct_bases=[],
    name_mapping={"http_api_id": "httpApiId", "api_endpoint": "apiEndpoint"},
)
class HttpApiAttributes:
    def __init__(
        self,
        *,
        http_api_id: builtins.str,
        api_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes for importing an HttpApi into the CDK.

        :param http_api_id: (experimental) The identifier of the HttpApi.
        :param api_endpoint: (experimental) The endpoint URL of the HttpApi. Default: - throws an error if apiEndpoint is accessed.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            http_api_attributes = apigatewayv2.HttpApiAttributes(
                http_api_id="httpApiId",
            
                # the properties below are optional
                api_endpoint="apiEndpoint"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpApiAttributes.__init__)
            check_type(argname="argument http_api_id", value=http_api_id, expected_type=type_hints["http_api_id"])
            check_type(argname="argument api_endpoint", value=api_endpoint, expected_type=type_hints["api_endpoint"])
        self._values: typing.Dict[str, typing.Any] = {
            "http_api_id": http_api_id,
        }
        if api_endpoint is not None:
            self._values["api_endpoint"] = api_endpoint

    @builtins.property
    def http_api_id(self) -> builtins.str:
        '''(experimental) The identifier of the HttpApi.

        :stability: experimental
        '''
        result = self._values.get("http_api_id")
        assert result is not None, "Required property 'http_api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The endpoint URL of the HttpApi.

        :default: - throws an error if apiEndpoint is accessed.

        :stability: experimental
        '''
        result = self._values.get("api_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpApiAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_name": "apiName",
        "cors_preflight": "corsPreflight",
        "create_default_stage": "createDefaultStage",
        "default_authorization_scopes": "defaultAuthorizationScopes",
        "default_authorizer": "defaultAuthorizer",
        "default_domain_mapping": "defaultDomainMapping",
        "default_integration": "defaultIntegration",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
    },
)
class HttpApiProps:
    def __init__(
        self,
        *,
        api_name: typing.Optional[builtins.str] = None,
        cors_preflight: typing.Optional[typing.Union[CorsPreflightOptions, typing.Dict[str, typing.Any]]] = None,
        create_default_stage: typing.Optional[builtins.bool] = None,
        default_authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_authorizer: typing.Optional["IHttpRouteAuthorizer"] = None,
        default_domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        default_integration: typing.Optional["HttpRouteIntegration"] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties to initialize an instance of ``HttpApi``.

        :param api_name: (experimental) Name for the HTTP API resource. Default: - id of the HttpApi construct.
        :param cors_preflight: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: (experimental) Whether a default stage and deployment should be automatically created. Default: true
        :param default_authorization_scopes: (experimental) Default OIDC scopes attached to all routes in the gateway, unless explicitly configured on the route. Default: - no default authorization scopes
        :param default_authorizer: (experimental) Default Authorizer to applied to all routes in the gateway. Default: - No authorizer
        :param default_domain_mapping: (experimental) Configure a custom domain with the API mapping resource to the HTTP API. Default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.
        :param default_integration: (experimental) An integration that will be configured on the catch-all route ($default). Default: - none
        :param description: (experimental) The description of the API. Default: - none
        :param disable_execute_api_endpoint: (experimental) Specifies whether clients can invoke your API using the default endpoint. By default, clients can invoke your API with the default ``https://{api_id}.execute-api.{region}.amazonaws.com`` endpoint. Enable this if you would like clients to use your custom domain name. Default: false execute-api endpoint enabled.

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
        if isinstance(cors_preflight, dict):
            cors_preflight = CorsPreflightOptions(**cors_preflight)
        if isinstance(default_domain_mapping, dict):
            default_domain_mapping = DomainMappingOptions(**default_domain_mapping)
        if __debug__:
            type_hints = typing.get_type_hints(HttpApiProps.__init__)
            check_type(argname="argument api_name", value=api_name, expected_type=type_hints["api_name"])
            check_type(argname="argument cors_preflight", value=cors_preflight, expected_type=type_hints["cors_preflight"])
            check_type(argname="argument create_default_stage", value=create_default_stage, expected_type=type_hints["create_default_stage"])
            check_type(argname="argument default_authorization_scopes", value=default_authorization_scopes, expected_type=type_hints["default_authorization_scopes"])
            check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            check_type(argname="argument default_domain_mapping", value=default_domain_mapping, expected_type=type_hints["default_domain_mapping"])
            check_type(argname="argument default_integration", value=default_integration, expected_type=type_hints["default_integration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
        self._values: typing.Dict[str, typing.Any] = {}
        if api_name is not None:
            self._values["api_name"] = api_name
        if cors_preflight is not None:
            self._values["cors_preflight"] = cors_preflight
        if create_default_stage is not None:
            self._values["create_default_stage"] = create_default_stage
        if default_authorization_scopes is not None:
            self._values["default_authorization_scopes"] = default_authorization_scopes
        if default_authorizer is not None:
            self._values["default_authorizer"] = default_authorizer
        if default_domain_mapping is not None:
            self._values["default_domain_mapping"] = default_domain_mapping
        if default_integration is not None:
            self._values["default_integration"] = default_integration
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the HTTP API resource.

        :default: - id of the HttpApi construct.

        :stability: experimental
        '''
        result = self._values.get("api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_preflight(self) -> typing.Optional[CorsPreflightOptions]:
        '''(experimental) Specifies a CORS configuration for an API.

        :default: - CORS disabled.

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
        :stability: experimental
        '''
        result = self._values.get("cors_preflight")
        return typing.cast(typing.Optional[CorsPreflightOptions], result)

    @builtins.property
    def create_default_stage(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether a default stage and deployment should be automatically created.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("create_default_stage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_authorization_scopes(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Default OIDC scopes attached to all routes in the gateway, unless explicitly configured on the route.

        :default: - no default authorization scopes

        :stability: experimental
        '''
        result = self._values.get("default_authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_authorizer(self) -> typing.Optional["IHttpRouteAuthorizer"]:
        '''(experimental) Default Authorizer to applied to all routes in the gateway.

        :default: - No authorizer

        :stability: experimental
        '''
        result = self._values.get("default_authorizer")
        return typing.cast(typing.Optional["IHttpRouteAuthorizer"], result)

    @builtins.property
    def default_domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        '''(experimental) Configure a custom domain with the API mapping resource to the HTTP API.

        :default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.

        :stability: experimental
        '''
        result = self._values.get("default_domain_mapping")
        return typing.cast(typing.Optional[DomainMappingOptions], result)

    @builtins.property
    def default_integration(self) -> typing.Optional["HttpRouteIntegration"]:
        '''(experimental) An integration that will be configured on the catch-all route ($default).

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("default_integration")
        return typing.cast(typing.Optional["HttpRouteIntegration"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the API.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether clients can invoke your API using the default endpoint.

        By default, clients can invoke your API with the default
        ``https://{api_id}.execute-api.{region}.amazonaws.com`` endpoint. Enable
        this if you would like clients to use your custom domain name.

        :default: false execute-api endpoint enabled.

        :stability: experimental
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpAuthorizerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_id": "authorizerId",
        "authorizer_type": "authorizerType",
    },
)
class HttpAuthorizerAttributes:
    def __init__(
        self,
        *,
        authorizer_id: builtins.str,
        authorizer_type: builtins.str,
    ) -> None:
        '''(experimental) Reference to an http authorizer.

        :param authorizer_id: (experimental) Id of the Authorizer.
        :param authorizer_type: (experimental) Type of authorizer. Possible values are: - JWT - JSON Web Token Authorizer - CUSTOM - Lambda Authorizer - NONE - No Authorization

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            http_authorizer_attributes = apigatewayv2.HttpAuthorizerAttributes(
                authorizer_id="authorizerId",
                authorizer_type="authorizerType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAuthorizerAttributes.__init__)
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument authorizer_type", value=authorizer_type, expected_type=type_hints["authorizer_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorizer_id": authorizer_id,
            "authorizer_type": authorizer_type,
        }

    @builtins.property
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        '''
        result = self._values.get("authorizer_id")
        assert result is not None, "Required property 'authorizer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_type(self) -> builtins.str:
        '''(experimental) Type of authorizer.

        Possible values are:

        - JWT - JSON Web Token Authorizer
        - CUSTOM - Lambda Authorizer
        - NONE - No Authorization

        :stability: experimental
        '''
        result = self._values.get("authorizer_type")
        assert result is not None, "Required property 'authorizer_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAuthorizerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "http_api": "httpApi",
        "identity_source": "identitySource",
        "type": "type",
        "authorizer_name": "authorizerName",
        "authorizer_uri": "authorizerUri",
        "enable_simple_responses": "enableSimpleResponses",
        "jwt_audience": "jwtAudience",
        "jwt_issuer": "jwtIssuer",
        "payload_format_version": "payloadFormatVersion",
        "results_cache_ttl": "resultsCacheTtl",
    },
)
class HttpAuthorizerProps:
    def __init__(
        self,
        *,
        http_api: "IHttpApi",
        identity_source: typing.Sequence[builtins.str],
        type: "HttpAuthorizerType",
        authorizer_name: typing.Optional[builtins.str] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[builtins.bool] = None,
        jwt_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwt_issuer: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[AuthorizerPayloadVersion] = None,
        results_cache_ttl: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''(experimental) Properties to initialize an instance of ``HttpAuthorizer``.

        :param http_api: (experimental) HTTP Api to attach the authorizer to.
        :param identity_source: (experimental) The identity source for which authorization is requested.
        :param type: (experimental) The type of authorizer.
        :param authorizer_name: (experimental) Name of the authorizer. Default: - id of the HttpAuthorizer construct.
        :param authorizer_uri: (experimental) The authorizer's Uniform Resource Identifier (URI). For REQUEST authorizers, this must be a well-formed Lambda function URI. Default: - required for Request authorizer types
        :param enable_simple_responses: (experimental) Specifies whether a Lambda authorizer returns a response in a simple format. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Default: - The lambda authorizer must return an IAM policy as its response
        :param jwt_audience: (experimental) A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list. Default: - required for JWT authorizer typess.
        :param jwt_issuer: (experimental) The base domain of the identity provider that issues JWT. Default: - required for JWT authorizer types.
        :param payload_format_version: (experimental) Specifies the format of the payload sent to an HTTP API Lambda authorizer. Default: AuthorizerPayloadVersion.VERSION_2_0 if the authorizer type is HttpAuthorizerType.LAMBDA
        :param results_cache_ttl: (experimental) How long APIGateway should cache the results. Max 1 hour. Default: - API Gateway will not cache authorizer responses

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.core as cdk
            
            # http_api: apigatewayv2.HttpApi
            
            http_authorizer_props = apigatewayv2.HttpAuthorizerProps(
                http_api=http_api,
                identity_source=["identitySource"],
                type=apigatewayv2.HttpAuthorizerType.IAM,
            
                # the properties below are optional
                authorizer_name="authorizerName",
                authorizer_uri="authorizerUri",
                enable_simple_responses=False,
                jwt_audience=["jwtAudience"],
                jwt_issuer="jwtIssuer",
                payload_format_version=apigatewayv2.AuthorizerPayloadVersion.VERSION_1_0,
                results_cache_ttl=cdk.Duration.minutes(30)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAuthorizerProps.__init__)
            check_type(argname="argument http_api", value=http_api, expected_type=type_hints["http_api"])
            check_type(argname="argument identity_source", value=identity_source, expected_type=type_hints["identity_source"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument authorizer_name", value=authorizer_name, expected_type=type_hints["authorizer_name"])
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument enable_simple_responses", value=enable_simple_responses, expected_type=type_hints["enable_simple_responses"])
            check_type(argname="argument jwt_audience", value=jwt_audience, expected_type=type_hints["jwt_audience"])
            check_type(argname="argument jwt_issuer", value=jwt_issuer, expected_type=type_hints["jwt_issuer"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
            check_type(argname="argument results_cache_ttl", value=results_cache_ttl, expected_type=type_hints["results_cache_ttl"])
        self._values: typing.Dict[str, typing.Any] = {
            "http_api": http_api,
            "identity_source": identity_source,
            "type": type,
        }
        if authorizer_name is not None:
            self._values["authorizer_name"] = authorizer_name
        if authorizer_uri is not None:
            self._values["authorizer_uri"] = authorizer_uri
        if enable_simple_responses is not None:
            self._values["enable_simple_responses"] = enable_simple_responses
        if jwt_audience is not None:
            self._values["jwt_audience"] = jwt_audience
        if jwt_issuer is not None:
            self._values["jwt_issuer"] = jwt_issuer
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version
        if results_cache_ttl is not None:
            self._values["results_cache_ttl"] = results_cache_ttl

    @builtins.property
    def http_api(self) -> "IHttpApi":
        '''(experimental) HTTP Api to attach the authorizer to.

        :stability: experimental
        '''
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return typing.cast("IHttpApi", result)

    @builtins.property
    def identity_source(self) -> typing.List[builtins.str]:
        '''(experimental) The identity source for which authorization is requested.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        :stability: experimental
        '''
        result = self._values.get("identity_source")
        assert result is not None, "Required property 'identity_source' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> "HttpAuthorizerType":
        '''(experimental) The type of authorizer.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("HttpAuthorizerType", result)

    @builtins.property
    def authorizer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the authorizer.

        :default: - id of the HttpAuthorizer construct.

        :stability: experimental
        '''
        result = self._values.get("authorizer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authorizer's Uniform Resource Identifier (URI).

        For REQUEST authorizers, this must be a well-formed Lambda function URI.

        :default: - required for Request authorizer types

        :stability: experimental
        '''
        result = self._values.get("authorizer_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_simple_responses(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether a Lambda authorizer returns a response in a simple format.

        If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy.

        :default: - The lambda authorizer must return an IAM policy as its response

        :stability: experimental
        '''
        result = self._values.get("enable_simple_responses")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jwt_audience(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of the intended recipients of the JWT.

        A valid JWT must provide an aud that matches at least one entry in this list.

        :default: - required for JWT authorizer typess.

        :stability: experimental
        '''
        result = self._values.get("jwt_audience")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jwt_issuer(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base domain of the identity provider that issues JWT.

        :default: - required for JWT authorizer types.

        :stability: experimental
        '''
        result = self._values.get("jwt_issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_format_version(self) -> typing.Optional[AuthorizerPayloadVersion]:
        '''(experimental) Specifies the format of the payload sent to an HTTP API Lambda authorizer.

        :default: AuthorizerPayloadVersion.VERSION_2_0 if the authorizer type is HttpAuthorizerType.LAMBDA

        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[AuthorizerPayloadVersion], result)

    @builtins.property
    def results_cache_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) How long APIGateway should cache the results.

        Max 1 hour.

        :default: - API Gateway will not cache authorizer responses

        :stability: experimental
        '''
        result = self._values.get("results_cache_ttl")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpAuthorizerType")
class HttpAuthorizerType(enum.Enum):
    '''(experimental) Supported Authorizer types.

    :stability: experimental
    '''

    IAM = "IAM"
    '''(experimental) IAM Authorizer.

    :stability: experimental
    '''
    JWT = "JWT"
    '''(experimental) JSON Web Tokens.

    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''(experimental) Lambda Authorizer.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpConnectionType")
class HttpConnectionType(enum.Enum):
    '''(experimental) Supported connection types.

    :stability: experimental
    '''

    VPC_LINK = "VPC_LINK"
    '''(experimental) For private connections between API Gateway and resources in a VPC.

    :stability: experimental
    '''
    INTERNET = "INTERNET"
    '''(experimental) For connections through public routable internet.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "http_api": "httpApi",
        "integration_type": "integrationType",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "credentials": "credentials",
        "integration_subtype": "integrationSubtype",
        "integration_uri": "integrationUri",
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "payload_format_version": "payloadFormatVersion",
        "secure_server_name": "secureServerName",
    },
)
class HttpIntegrationProps:
    def __init__(
        self,
        *,
        http_api: "IHttpApi",
        integration_type: "HttpIntegrationType",
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        credentials: typing.Optional["IntegrationCredentials"] = None,
        integration_subtype: typing.Optional["HttpIntegrationSubtype"] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        method: typing.Optional["HttpMethod"] = None,
        parameter_mapping: typing.Optional["ParameterMapping"] = None,
        payload_format_version: typing.Optional["PayloadFormatVersion"] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The integration properties.

        :param http_api: (experimental) The HTTP API to which this integration should be bound.
        :param integration_type: (experimental) Integration type.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param credentials: (experimental) The credentials with which to invoke the integration. Default: - no credentials, use resource-based permissions on supported AWS services
        :param integration_subtype: (experimental) Integration subtype. Used for AWS Service integrations, specifies the target of the integration. Default: - none, required if no ``integrationUri`` is defined.
        :param integration_uri: (experimental) Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.AWS_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``. Default: - none, required if no ``integrationSubtype`` is defined.
        :param method: (experimental) The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.AWS_PROXY`, irrelevant otherwise.
        :param secure_server_name: (experimental) Specifies the TLS configuration for a private integration. Default: undefined private integration traffic will use HTTP protocol

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # http_api: apigatewayv2.HttpApi
            # integration_credentials: apigatewayv2.IntegrationCredentials
            # parameter_mapping: apigatewayv2.ParameterMapping
            # payload_format_version: apigatewayv2.PayloadFormatVersion
            
            http_integration_props = apigatewayv2.HttpIntegrationProps(
                http_api=http_api,
                integration_type=apigatewayv2.HttpIntegrationType.HTTP_PROXY,
            
                # the properties below are optional
                connection_id="connectionId",
                connection_type=apigatewayv2.HttpConnectionType.VPC_LINK,
                credentials=integration_credentials,
                integration_subtype=apigatewayv2.HttpIntegrationSubtype.EVENTBRIDGE_PUT_EVENTS,
                integration_uri="integrationUri",
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                payload_format_version=payload_format_version,
                secure_server_name="secureServerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpIntegrationProps.__init__)
            check_type(argname="argument http_api", value=http_api, expected_type=type_hints["http_api"])
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument integration_subtype", value=integration_subtype, expected_type=type_hints["integration_subtype"])
            check_type(argname="argument integration_uri", value=integration_uri, expected_type=type_hints["integration_uri"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "http_api": http_api,
            "integration_type": integration_type,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if credentials is not None:
            self._values["credentials"] = credentials
        if integration_subtype is not None:
            self._values["integration_subtype"] = integration_subtype
        if integration_uri is not None:
            self._values["integration_uri"] = integration_uri
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name

    @builtins.property
    def http_api(self) -> "IHttpApi":
        '''(experimental) The HTTP API to which this integration should be bound.

        :stability: experimental
        '''
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return typing.cast("IHttpApi", result)

    @builtins.property
    def integration_type(self) -> "HttpIntegrationType":
        '''(experimental) Integration type.

        :stability: experimental
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast("HttpIntegrationType", result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[HttpConnectionType]:
        '''(experimental) The type of the network connection to the integration endpoint.

        :default: HttpConnectionType.INTERNET

        :stability: experimental
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[HttpConnectionType], result)

    @builtins.property
    def credentials(self) -> typing.Optional["IntegrationCredentials"]:
        '''(experimental) The credentials with which to invoke the integration.

        :default: - no credentials, use resource-based permissions on supported AWS services

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["IntegrationCredentials"], result)

    @builtins.property
    def integration_subtype(self) -> typing.Optional["HttpIntegrationSubtype"]:
        '''(experimental) Integration subtype.

        Used for AWS Service integrations, specifies the target of the integration.

        :default: - none, required if no ``integrationUri`` is defined.

        :stability: experimental
        '''
        result = self._values.get("integration_subtype")
        return typing.cast(typing.Optional["HttpIntegrationSubtype"], result)

    @builtins.property
    def integration_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) Integration URI.

        This will be the function ARN in the case of ``HttpIntegrationType.AWS_PROXY``,
        or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.

        :default: - none, required if no ``integrationSubtype`` is defined.

        :stability: experimental
        '''
        result = self._values.get("integration_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional["HttpMethod"]:
        '''(experimental) The HTTP method to use when calling the underlying HTTP proxy.

        :default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["HttpMethod"], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional["ParameterMapping"]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional["ParameterMapping"], result)

    @builtins.property
    def payload_format_version(self) -> typing.Optional["PayloadFormatVersion"]:
        '''(experimental) The version of the payload format.

        :default: - defaults to latest in the case of HttpIntegrationType.AWS_PROXY`, irrelevant otherwise.

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional["PayloadFormatVersion"], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the TLS configuration for a private integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationSubtype")
class HttpIntegrationSubtype(enum.Enum):
    '''(experimental) Supported integration subtypes.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html
    :stability: experimental
    '''

    EVENTBRIDGE_PUT_EVENTS = "EVENTBRIDGE_PUT_EVENTS"
    '''(experimental) EventBridge PutEvents integration.

    :stability: experimental
    '''
    SQS_SEND_MESSAGE = "SQS_SEND_MESSAGE"
    '''(experimental) SQS SendMessage integration.

    :stability: experimental
    '''
    SQS_RECEIVE_MESSAGE = "SQS_RECEIVE_MESSAGE"
    '''(experimental) SQS ReceiveMessage integration,.

    :stability: experimental
    '''
    SQS_DELETE_MESSAGE = "SQS_DELETE_MESSAGE"
    '''(experimental) SQS DeleteMessage integration,.

    :stability: experimental
    '''
    SQS_PURGE_QUEUE = "SQS_PURGE_QUEUE"
    '''(experimental) SQS PurgeQueue integration.

    :stability: experimental
    '''
    APPCONFIG_GET_CONFIGURATION = "APPCONFIG_GET_CONFIGURATION"
    '''(experimental) AppConfig GetConfiguration integration.

    :stability: experimental
    '''
    KINESIS_PUT_RECORD = "KINESIS_PUT_RECORD"
    '''(experimental) Kinesis PutRecord integration.

    :stability: experimental
    '''
    STEPFUNCTIONS_START_EXECUTION = "STEPFUNCTIONS_START_EXECUTION"
    '''(experimental) Step Functions StartExecution integration.

    :stability: experimental
    '''
    STEPFUNCTIONS_START_SYNC_EXECUTION = "STEPFUNCTIONS_START_SYNC_EXECUTION"
    '''(experimental) Step Functions StartSyncExecution integration.

    :stability: experimental
    '''
    STEPFUNCTIONS_STOP_EXECUTION = "STEPFUNCTIONS_STOP_EXECUTION"
    '''(experimental) Step Functions StopExecution integration.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationType")
class HttpIntegrationType(enum.Enum):
    '''(experimental) Supported integration types.

    :stability: experimental
    '''

    HTTP_PROXY = "HTTP_PROXY"
    '''(experimental) Integration type is an HTTP proxy.

    For integrating the route or method request with an HTTP endpoint, with the
    client request passed through as-is. This is also referred to as HTTP proxy
    integration. For HTTP API private integrations, use an HTTP_PROXY integration.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-http.html
    :stability: experimental
    '''
    AWS_PROXY = "AWS_PROXY"
    '''(experimental) Integration type is an AWS proxy.

    For integrating the route or method request with a Lambda function or other
    AWS service action. This integration is also referred to as a Lambda proxy
    integration.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpMethod")
class HttpMethod(enum.Enum):
    '''(experimental) Supported HTTP methods.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration, HttpLambdaIntegration
        
        # books_default_fn: lambda.Function
        
        
        get_books_integration = HttpUrlIntegration("GetBooksIntegration", "https://get-books-proxy.myproxy.internal")
        books_default_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)
        
        http_api = apigwv2.HttpApi(self, "HttpApi")
        
        http_api.add_routes(
            path="/books",
            methods=[apigwv2.HttpMethod.GET],
            integration=get_books_integration
        )
        http_api.add_routes(
            path="/books",
            methods=[apigwv2.HttpMethod.ANY],
            integration=books_default_integration
        )
    '''

    ANY = "ANY"
    '''(experimental) HTTP ANY.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) HTTP DELETE.

    :stability: experimental
    '''
    GET = "GET"
    '''(experimental) HTTP GET.

    :stability: experimental
    '''
    HEAD = "HEAD"
    '''(experimental) HTTP HEAD.

    :stability: experimental
    '''
    OPTIONS = "OPTIONS"
    '''(experimental) HTTP OPTIONS.

    :stability: experimental
    '''
    PATCH = "PATCH"
    '''(experimental) HTTP PATCH.

    :stability: experimental
    '''
    POST = "POST"
    '''(experimental) HTTP POST.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) HTTP PUT.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteAuthorizerBindOptions",
    jsii_struct_bases=[],
    name_mapping={"route": "route", "scope": "scope"},
)
class HttpRouteAuthorizerBindOptions:
    def __init__(self, *, route: "IHttpRoute", scope: constructs.Construct) -> None:
        '''(experimental) Input to the bind() operation, that binds an authorizer to a route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import constructs as constructs
            
            # construct: constructs.Construct
            # http_route: apigatewayv2.HttpRoute
            
            http_route_authorizer_bind_options = apigatewayv2.HttpRouteAuthorizerBindOptions(
                route=http_route,
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteAuthorizerBindOptions.__init__)
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[str, typing.Any] = {
            "route": route,
            "scope": scope,
        }

    @builtins.property
    def route(self) -> "IHttpRoute":
        '''(experimental) The route to which the authorizer is being bound.

        :stability: experimental
        '''
        result = self._values.get("route")
        assert result is not None, "Required property 'route' is missing"
        return typing.cast("IHttpRoute", result)

    @builtins.property
    def scope(self) -> constructs.Construct:
        '''(experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(constructs.Construct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteAuthorizerBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_type": "authorizationType",
        "authorization_scopes": "authorizationScopes",
        "authorizer_id": "authorizerId",
    },
)
class HttpRouteAuthorizerConfig:
    def __init__(
        self,
        *,
        authorization_type: builtins.str,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Results of binding an authorizer to an http route.

        :param authorization_type: (experimental) The type of authorization. Possible values are: - AWS_IAM - IAM Authorizer - JWT - JSON Web Token Authorizer - CUSTOM - Lambda Authorizer - NONE - No Authorization
        :param authorization_scopes: (experimental) The list of OIDC scopes to include in the authorization. Default: - no authorization scopes
        :param authorizer_id: (experimental) The authorizer id. Default: - No authorizer id (useful for AWS_IAM route authorizer)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            http_route_authorizer_config = apigatewayv2.HttpRouteAuthorizerConfig(
                authorization_type="authorizationType",
            
                # the properties below are optional
                authorization_scopes=["authorizationScopes"],
                authorizer_id="authorizerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteAuthorizerConfig.__init__)
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorization_type": authorization_type,
        }
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id

    @builtins.property
    def authorization_type(self) -> builtins.str:
        '''(experimental) The type of authorization.

        Possible values are:

        - AWS_IAM - IAM Authorizer
        - JWT - JSON Web Token Authorizer
        - CUSTOM - Lambda Authorizer
        - NONE - No Authorization

        :stability: experimental
        '''
        result = self._values.get("authorization_type")
        assert result is not None, "Required property 'authorization_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of OIDC scopes to include in the authorization.

        :default: - no authorization scopes

        :stability: experimental
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authorizer id.

        :default: - No authorizer id (useful for AWS_IAM route authorizer)

        :stability: experimental
        '''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpRouteIntegration(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegration",
):
    '''(experimental) The interface that various route integration classes will inherit.

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

    def __init__(self, id: builtins.str) -> None:
        '''(experimental) Initialize an integration for a route on http api.

        :param id: id of the underlying ``HttpIntegration`` construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: aws_cdk.core.Construct,
    ) -> "HttpRouteIntegrationConfig":
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="completeBind")
    def _complete_bind(
        self,
        *,
        route: "IHttpRoute",
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
        _options = HttpRouteIntegrationBindOptions(route=route, scope=scope)

        return typing.cast(None, jsii.invoke(self, "completeBind", [_options]))


class _HttpRouteIntegrationProxy(HttpRouteIntegration):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: aws_cdk.core.Construct,
    ) -> "HttpRouteIntegrationConfig":
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = HttpRouteIntegrationBindOptions(route=route, scope=scope)

        return typing.cast("HttpRouteIntegrationConfig", jsii.invoke(self, "bind", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, HttpRouteIntegration).__jsii_proxy_class__ = lambda : _HttpRouteIntegrationProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegrationBindOptions",
    jsii_struct_bases=[],
    name_mapping={"route": "route", "scope": "scope"},
)
class HttpRouteIntegrationBindOptions:
    def __init__(self, *, route: "IHttpRoute", scope: aws_cdk.core.Construct) -> None:
        '''(experimental) Options to the HttpRouteIntegration during its bind operation.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.core as cdk
            
            # construct: cdk.Construct
            # http_route: apigatewayv2.HttpRoute
            
            http_route_integration_bind_options = apigatewayv2.HttpRouteIntegrationBindOptions(
                route=http_route,
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteIntegrationBindOptions.__init__)
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[str, typing.Any] = {
            "route": route,
            "scope": scope,
        }

    @builtins.property
    def route(self) -> "IHttpRoute":
        '''(experimental) The route to which this is being bound.

        :stability: experimental
        '''
        result = self._values.get("route")
        assert result is not None, "Required property 'route' is missing"
        return typing.cast("IHttpRoute", result)

    @builtins.property
    def scope(self) -> aws_cdk.core.Construct:
        '''(experimental) The current scope in which the bind is occurring.

        If the ``HttpRouteIntegration`` being bound creates additional constructs,
        this will be used as their parent scope.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(aws_cdk.core.Construct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteIntegrationBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "payload_format_version": "payloadFormatVersion",
        "type": "type",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "credentials": "credentials",
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "subtype": "subtype",
        "uri": "uri",
    },
)
class HttpRouteIntegrationConfig:
    def __init__(
        self,
        *,
        payload_format_version: "PayloadFormatVersion",
        type: HttpIntegrationType,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        credentials: typing.Optional["IntegrationCredentials"] = None,
        method: typing.Optional[HttpMethod] = None,
        parameter_mapping: typing.Optional["ParameterMapping"] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        subtype: typing.Optional[HttpIntegrationSubtype] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Config returned back as a result of the bind.

        :param payload_format_version: (experimental) Payload format version in the case of lambda proxy integration. Default: - undefined
        :param type: (experimental) Integration type.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param credentials: (experimental) The credentials with which to invoke the integration. Default: - no credentials, use resource-based permissions on supported AWS services
        :param method: (experimental) The HTTP method that must be used to invoke the underlying proxy. Required for ``HttpIntegrationType.HTTP_PROXY`` Default: - undefined
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param subtype: (experimental) Integration subtype. Default: - none, required if no ``integrationUri`` is defined.
        :param uri: (experimental) Integration URI. Default: - none, required if no ``integrationSubtype`` is defined.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # integration_credentials: apigatewayv2.IntegrationCredentials
            # parameter_mapping: apigatewayv2.ParameterMapping
            # payload_format_version: apigatewayv2.PayloadFormatVersion
            
            http_route_integration_config = apigatewayv2.HttpRouteIntegrationConfig(
                payload_format_version=payload_format_version,
                type=apigatewayv2.HttpIntegrationType.HTTP_PROXY,
            
                # the properties below are optional
                connection_id="connectionId",
                connection_type=apigatewayv2.HttpConnectionType.VPC_LINK,
                credentials=integration_credentials,
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                subtype=apigatewayv2.HttpIntegrationSubtype.EVENTBRIDGE_PUT_EVENTS,
                uri="uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteIntegrationConfig.__init__)
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[str, typing.Any] = {
            "payload_format_version": payload_format_version,
            "type": type,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if credentials is not None:
            self._values["credentials"] = credentials
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if subtype is not None:
            self._values["subtype"] = subtype
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def payload_format_version(self) -> "PayloadFormatVersion":
        '''(experimental) Payload format version in the case of lambda proxy integration.

        :default: - undefined

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        assert result is not None, "Required property 'payload_format_version' is missing"
        return typing.cast("PayloadFormatVersion", result)

    @builtins.property
    def type(self) -> HttpIntegrationType:
        '''(experimental) Integration type.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(HttpIntegrationType, result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[HttpConnectionType]:
        '''(experimental) The type of the network connection to the integration endpoint.

        :default: HttpConnectionType.INTERNET

        :stability: experimental
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[HttpConnectionType], result)

    @builtins.property
    def credentials(self) -> typing.Optional["IntegrationCredentials"]:
        '''(experimental) The credentials with which to invoke the integration.

        :default: - no credentials, use resource-based permissions on supported AWS services

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["IntegrationCredentials"], result)

    @builtins.property
    def method(self) -> typing.Optional[HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying proxy.

        Required for ``HttpIntegrationType.HTTP_PROXY``

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[HttpMethod], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional["ParameterMapping"]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional["ParameterMapping"], result)

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
    def subtype(self) -> typing.Optional[HttpIntegrationSubtype]:
        '''(experimental) Integration subtype.

        :default: - none, required if no ``integrationUri`` is defined.

        :stability: experimental
        '''
        result = self._values.get("subtype")
        return typing.cast(typing.Optional[HttpIntegrationSubtype], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) Integration URI.

        :default: - none, required if no ``integrationSubtype`` is defined.

        :stability: experimental
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpRouteKey(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteKey",
):
    '''(experimental) HTTP route in APIGateway is a combination of the HTTP method and the path component.

    This class models that combination.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        http_route_key = apigatewayv2.HttpRouteKey.with("path", apigatewayv2.HttpMethod.ANY)
    '''

    @jsii.member(jsii_name="with")
    @builtins.classmethod
    def with_(
        cls,
        path: builtins.str,
        method: typing.Optional[HttpMethod] = None,
    ) -> "HttpRouteKey":
        '''(experimental) Create a route key with the combination of the path and the method.

        :param path: -
        :param method: default is 'ANY'.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteKey.with_)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
        return typing.cast("HttpRouteKey", jsii.sinvoke(cls, "with", [path, method]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "HttpRouteKey":
        '''(experimental) The catch-all route of the API, i.e., when no other routes match.

        :stability: experimental
        '''
        return typing.cast("HttpRouteKey", jsii.sget(cls, "DEFAULT"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''(experimental) The key to the RouteKey as recognized by APIGateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> HttpMethod:
        '''(experimental) The method of the route.

        :stability: experimental
        '''
        return typing.cast(HttpMethod, jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path part of this RouteKey.

        Returns ``undefined`` when ``RouteKey.DEFAULT`` is used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteProps",
    jsii_struct_bases=[BatchHttpRouteOptions],
    name_mapping={
        "integration": "integration",
        "http_api": "httpApi",
        "route_key": "routeKey",
        "authorization_scopes": "authorizationScopes",
        "authorizer": "authorizer",
    },
)
class HttpRouteProps(BatchHttpRouteOptions):
    def __init__(
        self,
        *,
        integration: HttpRouteIntegration,
        http_api: "IHttpApi",
        route_key: HttpRouteKey,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional["IHttpRouteAuthorizer"] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new Route.

        :param integration: (experimental) The integration to be configured on this route.
        :param http_api: (experimental) the API the route is associated with.
        :param route_key: (experimental) The key to this route. This is a combination of an HTTP method and an HTTP path.
        :param authorization_scopes: (experimental) The list of OIDC scopes to include in the authorization. These scopes will be merged with the scopes from the attached authorizer Default: - no additional authorization scopes
        :param authorizer: (experimental) Authorizer for a WebSocket API or an HTTP API. Default: - No authorizer

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # http_api: apigatewayv2.HttpApi
            # http_route_authorizer: apigatewayv2.IHttpRouteAuthorizer
            # http_route_integration: apigatewayv2.HttpRouteIntegration
            # http_route_key: apigatewayv2.HttpRouteKey
            
            http_route_props = apigatewayv2.HttpRouteProps(
                http_api=http_api,
                integration=http_route_integration,
                route_key=http_route_key,
            
                # the properties below are optional
                authorization_scopes=["authorizationScopes"],
                authorizer=http_route_authorizer
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRouteProps.__init__)
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument http_api", value=http_api, expected_type=type_hints["http_api"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
            "http_api": http_api,
            "route_key": route_key,
        }
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorizer is not None:
            self._values["authorizer"] = authorizer

    @builtins.property
    def integration(self) -> HttpRouteIntegration:
        '''(experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return typing.cast(HttpRouteIntegration, result)

    @builtins.property
    def http_api(self) -> "IHttpApi":
        '''(experimental) the API the route is associated with.

        :stability: experimental
        '''
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return typing.cast("IHttpApi", result)

    @builtins.property
    def route_key(self) -> HttpRouteKey:
        '''(experimental) The key to this route.

        This is a combination of an HTTP method and an HTTP path.

        :stability: experimental
        '''
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return typing.cast(HttpRouteKey, result)

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of OIDC scopes to include in the authorization.

        These scopes will be merged with the scopes from the attached authorizer

        :default: - no additional authorization scopes

        :stability: experimental
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorizer(self) -> typing.Optional["IHttpRouteAuthorizer"]:
        '''(experimental) Authorizer for a WebSocket API or an HTTP API.

        :default: - No authorizer

        :stability: experimental
        '''
        result = self._values.get("authorizer")
        return typing.cast(typing.Optional["IHttpRouteAuthorizer"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IApi")
class IApi(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a API Gateway HTTP/WebSocket API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        '''(experimental) The default endpoint for an API.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) The identifier of this API Gateway API.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        ...


class _IApiProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a API Gateway HTTP/WebSocket API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IApi"

    @builtins.property
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        '''(experimental) The default endpoint for an API.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) The identifier of this API Gateway API.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IApi.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApi).__jsii_proxy_class__ = lambda : _IApiProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IApiMapping")
class IApiMapping(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an ApiGatewayV2 ApiMapping resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        '''(experimental) ID of the api mapping.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IApiMappingProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an ApiGatewayV2 ApiMapping resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IApiMapping"

    @builtins.property
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        '''(experimental) ID of the api mapping.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiMappingId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApiMapping).__jsii_proxy_class__ = lambda : _IApiMappingProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IAuthorizer")
class IAuthorizer(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an Authorizer.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAuthorizerProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an Authorizer.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IAuthorizer"

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAuthorizer).__jsii_proxy_class__ = lambda : _IAuthorizerProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IDomainName")
class IDomainName(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an APIGatewayV2 DomainName.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The custom domain name.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IDomainNameProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an APIGatewayV2 DomainName.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IDomainName"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The custom domain name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalDomainName"))

    @builtins.property
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalHostedZoneId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomainName).__jsii_proxy_class__ = lambda : _IDomainNameProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpApi")
class IHttpApi(IApi, typing_extensions.Protocol):
    '''(experimental) Represents an HTTP API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        '''(deprecated) The identifier of this API Gateway HTTP API.

        :deprecated: - use apiId instead

        :stability: deprecated
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> "VpcLink":
        '''(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...


class _IHttpApiProxy(
    jsii.proxy_for(IApi), # type: ignore[misc]
):
    '''(experimental) Represents an HTTP API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpApi"

    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        '''(deprecated) The identifier of this API Gateway HTTP API.

        :deprecated: - use apiId instead

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpApiId"))

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> "VpcLink":
        '''(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        '''
        options = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        return typing.cast("VpcLink", jsii.invoke(self, "addVpcLink", [options]))

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricClientError", [props]))

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricCount", [props]))

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataProcessed", [props]))

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIntegrationLatency", [props]))

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricLatency", [props]))

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricServerError", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpApi).__jsii_proxy_class__ = lambda : _IHttpApiProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpAuthorizer")
class IHttpAuthorizer(IAuthorizer, typing_extensions.Protocol):
    '''(experimental) An authorizer for HTTP APIs.

    :stability: experimental
    '''

    pass


class _IHttpAuthorizerProxy(
    jsii.proxy_for(IAuthorizer), # type: ignore[misc]
):
    '''(experimental) An authorizer for HTTP APIs.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpAuthorizer"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpAuthorizer).__jsii_proxy_class__ = lambda : _IHttpAuthorizerProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRouteAuthorizer")
class IHttpRouteAuthorizer(typing_extensions.Protocol):
    '''(experimental) An authorizer that can attach to an Http Route.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: constructs.Construct,
    ) -> HttpRouteAuthorizerConfig:
        '''(experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        ...


class _IHttpRouteAuthorizerProxy:
    '''(experimental) An authorizer that can attach to an Http Route.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpRouteAuthorizer"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: constructs.Construct,
    ) -> HttpRouteAuthorizerConfig:
        '''(experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = HttpRouteAuthorizerBindOptions(route=route, scope=scope)

        return typing.cast(HttpRouteAuthorizerConfig, jsii.invoke(self, "bind", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpRouteAuthorizer).__jsii_proxy_class__ = lambda : _IHttpRouteAuthorizerProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IIntegration")
class IIntegration(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an integration to an API Route.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        '''(experimental) Id of the integration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IIntegrationProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an integration to an API Route.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IIntegration"

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        '''(experimental) Id of the integration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIntegration).__jsii_proxy_class__ = lambda : _IIntegrationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IMappingValue")
class IMappingValue(typing_extensions.Protocol):
    '''(experimental) Represents a Mapping Value.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) Represents a Mapping Value.

        :stability: experimental
        '''
        ...


class _IMappingValueProxy:
    '''(experimental) Represents a Mapping Value.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IMappingValue"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) Represents a Mapping Value.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMappingValue).__jsii_proxy_class__ = lambda : _IMappingValueProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IRoute")
class IRoute(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a route.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        '''(experimental) Id of the Route.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IRouteProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a route.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IRoute"

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        '''(experimental) Id of the Route.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRoute).__jsii_proxy_class__ = lambda : _IRouteProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IStage")
class IStage(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Stage.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''(experimental) The URL to this stage.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this HTTP Api Gateway Stage.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        ...


class _IStageProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Stage.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IStage"

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''(experimental) The URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this HTTP Api Gateway Stage.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IStage.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStage).__jsii_proxy_class__ = lambda : _IStageProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IVpcLink")
class IVpcLink(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an API Gateway VpcLink.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC to which this VPC Link is associated with.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        '''(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVpcLinkProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an API Gateway VpcLink.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IVpcLink"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC to which this VPC Link is associated with.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        '''(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcLinkId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcLink).__jsii_proxy_class__ = lambda : _IVpcLinkProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketApi")
class IWebSocketApi(IApi, typing_extensions.Protocol):
    '''(experimental) Represents a WebSocket API.

    :stability: experimental
    '''

    pass


class _IWebSocketApiProxy(
    jsii.proxy_for(IApi), # type: ignore[misc]
):
    '''(experimental) Represents a WebSocket API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketApi"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketApi).__jsii_proxy_class__ = lambda : _IWebSocketApiProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketAuthorizer")
class IWebSocketAuthorizer(IAuthorizer, typing_extensions.Protocol):
    '''(experimental) An authorizer for WebSocket APIs.

    :stability: experimental
    '''

    pass


class _IWebSocketAuthorizerProxy(
    jsii.proxy_for(IAuthorizer), # type: ignore[misc]
):
    '''(experimental) An authorizer for WebSocket APIs.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketAuthorizer"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketAuthorizer).__jsii_proxy_class__ = lambda : _IWebSocketAuthorizerProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketIntegration")
class IWebSocketIntegration(IIntegration, typing_extensions.Protocol):
    '''(experimental) Represents an Integration for an WebSocket API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this integration.

        :stability: experimental
        '''
        ...


class _IWebSocketIntegrationProxy(
    jsii.proxy_for(IIntegration), # type: ignore[misc]
):
    '''(experimental) Represents an Integration for an WebSocket API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketIntegration"

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this integration.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "webSocketApi"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketIntegration).__jsii_proxy_class__ = lambda : _IWebSocketIntegrationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketRoute")
class IWebSocketRoute(IRoute, typing_extensions.Protocol):
    '''(experimental) Represents a Route for an WebSocket API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        '''(experimental) The key to this route.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this route.

        :stability: experimental
        '''
        ...


class _IWebSocketRouteProxy(
    jsii.proxy_for(IRoute), # type: ignore[misc]
):
    '''(experimental) Represents a Route for an WebSocket API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketRoute"

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        '''(experimental) The key to this route.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeKey"))

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this route.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "webSocketApi"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketRoute).__jsii_proxy_class__ = lambda : _IWebSocketRouteProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketRouteAuthorizer")
class IWebSocketRouteAuthorizer(typing_extensions.Protocol):
    '''(experimental) An authorizer that can attach to an WebSocket Route.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: IWebSocketRoute,
        scope: constructs.Construct,
    ) -> "WebSocketRouteAuthorizerConfig":
        '''(experimental) Bind this authorizer to a specified WebSocket route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        ...


class _IWebSocketRouteAuthorizerProxy:
    '''(experimental) An authorizer that can attach to an WebSocket Route.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketRouteAuthorizer"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: IWebSocketRoute,
        scope: constructs.Construct,
    ) -> "WebSocketRouteAuthorizerConfig":
        '''(experimental) Bind this authorizer to a specified WebSocket route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = WebSocketRouteAuthorizerBindOptions(route=route, scope=scope)

        return typing.cast("WebSocketRouteAuthorizerConfig", jsii.invoke(self, "bind", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketRouteAuthorizer).__jsii_proxy_class__ = lambda : _IWebSocketRouteAuthorizerProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IWebSocketStage")
class IWebSocketStage(IStage, typing_extensions.Protocol):
    '''(experimental) Represents the WebSocketStage.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IWebSocketApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="callbackUrl")
    def callback_url(self) -> builtins.str:
        '''(experimental) The callback URL to this stage.

        You can use the callback URL to send messages to the client from the backend system.
        https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html

        :stability: experimental
        '''
        ...


class _IWebSocketStageProxy(
    jsii.proxy_for(IStage), # type: ignore[misc]
):
    '''(experimental) Represents the WebSocketStage.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IWebSocketStage"

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IWebSocketApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "api"))

    @builtins.property
    @jsii.member(jsii_name="callbackUrl")
    def callback_url(self) -> builtins.str:
        '''(experimental) The callback URL to this stage.

        You can use the callback URL to send messages to the client from the backend system.
        https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "callbackUrl"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWebSocketStage).__jsii_proxy_class__ = lambda : _IWebSocketStageProxy


class IntegrationCredentials(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apigatewayv2.IntegrationCredentials",
):
    '''(experimental) Credentials used for AWS Service integrations.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        import aws_cdk.aws_iam as iam
        
        # role: iam.Role
        
        integration_credentials = apigatewayv2.IntegrationCredentials.from_role(role)
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromRole")
    @builtins.classmethod
    def from_role(cls, role: aws_cdk.aws_iam.IRole) -> "IntegrationCredentials":
        '''(experimental) Use the specified role for integration requests.

        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IntegrationCredentials.from_role)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast("IntegrationCredentials", jsii.sinvoke(cls, "fromRole", [role]))

    @jsii.member(jsii_name="useCallerIdentity")
    @builtins.classmethod
    def use_caller_identity(cls) -> "IntegrationCredentials":
        '''(experimental) Use the calling user's identity to call the integration.

        :stability: experimental
        '''
        return typing.cast("IntegrationCredentials", jsii.sinvoke(cls, "useCallerIdentity", []))

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    @abc.abstractmethod
    def credentials_arn(self) -> builtins.str:
        '''(experimental) The ARN of the credentials.

        :stability: experimental
        '''
        ...


class _IntegrationCredentialsProxy(IntegrationCredentials):
    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> builtins.str:
        '''(experimental) The ARN of the credentials.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "credentialsArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IntegrationCredentials).__jsii_proxy_class__ = lambda : _IntegrationCredentialsProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.MTLSConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
)
class MTLSConfig:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        key: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The mTLS authentication configuration for a custom domain name.

        :param bucket: (experimental) The bucket that the trust store is hosted in.
        :param key: (experimental) The key in S3 to look at for the trust store.
        :param version: (experimental) The version of the S3 object that contains your truststore. To specify a version, you must have versioning enabled for the S3 bucket. Default: - latest version

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_certificatemanager as acm
            # bucket: s3.Bucket
            
            
            cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
            domain_name = "example.com"
            
            apigwv2.DomainName(self, "DomainName",
                domain_name=domain_name,
                certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn),
                mtls=apigwv2.MTLSConfig(
                    bucket=bucket,
                    key="someca.pem",
                    version="version"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MTLSConfig.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''(experimental) The bucket that the trust store is hosted in.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) The key in S3 to look at for the trust store.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the S3 object that contains your truststore.

        To specify a version, you must have versioning enabled for the S3 bucket.

        :default: - latest version

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MTLSConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMappingValue)
class MappingValue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.MappingValue",
):
    '''(experimental) Represents a Mapping Value.

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

    def __init__(self, value: builtins.str) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.__init__)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="contextVariable")
    @builtins.classmethod
    def context_variable(cls, variable_name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a context variable mapping value.

        :param variable_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.context_variable)
            check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "contextVariable", [variable_name]))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, value: builtins.str) -> "MappingValue":
        '''(experimental) Creates a custom mapping value.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.custom)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "custom", [value]))

    @jsii.member(jsii_name="requestBody")
    @builtins.classmethod
    def request_body(cls, name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a request body mapping value.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.request_body)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "requestBody", [name]))

    @jsii.member(jsii_name="requestHeader")
    @builtins.classmethod
    def request_header(cls, name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a header mapping value.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.request_header)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "requestHeader", [name]))

    @jsii.member(jsii_name="requestPath")
    @builtins.classmethod
    def request_path(cls) -> "MappingValue":
        '''(experimental) Creates a request path mapping value.

        :stability: experimental
        '''
        return typing.cast("MappingValue", jsii.sinvoke(cls, "requestPath", []))

    @jsii.member(jsii_name="requestPathParam")
    @builtins.classmethod
    def request_path_param(cls, name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a request path parameter mapping value.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.request_path_param)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "requestPathParam", [name]))

    @jsii.member(jsii_name="requestQueryString")
    @builtins.classmethod
    def request_query_string(cls, name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a query string mapping value.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.request_query_string)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "requestQueryString", [name]))

    @jsii.member(jsii_name="stageVariable")
    @builtins.classmethod
    def stage_variable(cls, variable_name: builtins.str) -> "MappingValue":
        '''(experimental) Creates a stage variable mapping value.

        :param variable_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MappingValue.stage_variable)
            check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
        return typing.cast("MappingValue", jsii.sinvoke(cls, "stageVariable", [variable_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NONE")
    def NONE(cls) -> "MappingValue":
        '''(experimental) Creates an empty mapping value.

        :stability: experimental
        '''
        return typing.cast("MappingValue", jsii.sget(cls, "NONE"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) Represents a Mapping Value.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class ParameterMapping(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.ParameterMapping",
):
    '''(experimental) Represents a Parameter Mapping.

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

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        obj: typing.Mapping[builtins.str, MappingValue],
    ) -> "ParameterMapping":
        '''(experimental) Creates a mapping from an object.

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.from_object)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("ParameterMapping", jsii.sinvoke(cls, "fromObject", [obj]))

    @jsii.member(jsii_name="appendHeader")
    def append_header(
        self,
        name: builtins.str,
        value: MappingValue,
    ) -> "ParameterMapping":
        '''(experimental) Creates a mapping to append a header.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.append_header)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "appendHeader", [name, value]))

    @jsii.member(jsii_name="appendQueryString")
    def append_query_string(
        self,
        name: builtins.str,
        value: MappingValue,
    ) -> "ParameterMapping":
        '''(experimental) Creates a mapping to append a query string.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.append_query_string)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "appendQueryString", [name, value]))

    @jsii.member(jsii_name="custom")
    def custom(self, key: builtins.str, value: builtins.str) -> "ParameterMapping":
        '''(experimental) Creates a custom mapping.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.custom)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "custom", [key, value]))

    @jsii.member(jsii_name="overwriteHeader")
    def overwrite_header(
        self,
        name: builtins.str,
        value: MappingValue,
    ) -> "ParameterMapping":
        '''(experimental) Creates a mapping to overwrite a header.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.overwrite_header)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "overwriteHeader", [name, value]))

    @jsii.member(jsii_name="overwritePath")
    def overwrite_path(self, value: MappingValue) -> "ParameterMapping":
        '''(experimental) Creates a mapping to overwrite a path.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.overwrite_path)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "overwritePath", [value]))

    @jsii.member(jsii_name="overwriteQueryString")
    def overwrite_query_string(
        self,
        name: builtins.str,
        value: MappingValue,
    ) -> "ParameterMapping":
        '''(experimental) Creates a mapping to overwrite a querystring.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.overwrite_query_string)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "overwriteQueryString", [name, value]))

    @jsii.member(jsii_name="removeHeader")
    def remove_header(self, name: builtins.str) -> "ParameterMapping":
        '''(experimental) Creates a mapping to remove a header.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.remove_header)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "removeHeader", [name]))

    @jsii.member(jsii_name="removeQueryString")
    def remove_query_string(self, name: builtins.str) -> "ParameterMapping":
        '''(experimental) Creates a mapping to remove a querystring.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParameterMapping.remove_query_string)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("ParameterMapping", jsii.invoke(self, "removeQueryString", [name]))

    @builtins.property
    @jsii.member(jsii_name="mappings")
    def mappings(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Represents all created parameter mappings.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "mappings"))


class PayloadFormatVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.PayloadFormatVersion",
):
    '''(experimental) Payload format version for lambda proxy integration.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        payload_format_version = apigatewayv2.PayloadFormatVersion.custom("version")
    '''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, version: builtins.str) -> "PayloadFormatVersion":
        '''(experimental) A custom payload version.

        Typically used if there is a version number that the CDK doesn't support yet

        :param version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PayloadFormatVersion.custom)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("PayloadFormatVersion", jsii.sinvoke(cls, "custom", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION_1_0")
    def VERSION_1_0(cls) -> "PayloadFormatVersion":
        '''(experimental) Version 1.0.

        :stability: experimental
        '''
        return typing.cast("PayloadFormatVersion", jsii.sget(cls, "VERSION_1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION_2_0")
    def VERSION_2_0(cls) -> "PayloadFormatVersion":
        '''(experimental) Version 2.0.

        :stability: experimental
        '''
        return typing.cast("PayloadFormatVersion", jsii.sget(cls, "VERSION_2_0"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) version as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.SecurityPolicy")
class SecurityPolicy(enum.Enum):
    '''(experimental) The minimum version of the SSL protocol that you want API Gateway to use for HTTPS connections.

    :stability: experimental
    '''

    TLS_1_0 = "TLS_1_0"
    '''(experimental) Cipher suite TLS 1.0.

    :stability: experimental
    '''
    TLS_1_2 = "TLS_1_2"
    '''(experimental) Cipher suite TLS 1.2.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.StageAttributes",
    jsii_struct_bases=[],
    name_mapping={"stage_name": "stageName"},
)
class StageAttributes:
    def __init__(self, *, stage_name: builtins.str) -> None:
        '''(experimental) The attributes used to import existing Stage.

        :param stage_name: (experimental) The name of the stage.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            stage_attributes = apigatewayv2.StageAttributes(
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StageAttributes.__init__)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
        }

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.StageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "domain_mapping": "domainMapping",
        "throttle": "throttle",
    },
)
class StageOptions:
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union["ThrottleSettings", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options required to create a new stage.

        Options that are common between HTTP and Websocket APIs.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # domain_name: apigatewayv2.DomainName
            
            stage_options = apigatewayv2.StageOptions(
                auto_deploy=False,
                domain_mapping=apigatewayv2.DomainMappingOptions(
                    domain_name=domain_name,
            
                    # the properties below are optional
                    mapping_key="mappingKey"
                ),
                throttle=apigatewayv2.ThrottleSettings(
                    burst_limit=123,
                    rate_limit=123
                )
            )
        '''
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        if isinstance(throttle, dict):
            throttle = ThrottleSettings(**throttle)
        if __debug__:
            type_hints = typing.get_type_hints(StageOptions.__init__)
            check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
            check_type(argname="argument domain_mapping", value=domain_mapping, expected_type=type_hints["domain_mapping"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping
        if throttle is not None:
            self._values["throttle"] = throttle

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        '''(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        '''
        result = self._values.get("domain_mapping")
        return typing.cast(typing.Optional[DomainMappingOptions], result)

    @builtins.property
    def throttle(self) -> typing.Optional["ThrottleSettings"]:
        '''(experimental) Throttle settings for the routes of this stage.

        :default: - no throttling configuration

        :stability: experimental
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional["ThrottleSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.ThrottleSettings",
    jsii_struct_bases=[],
    name_mapping={"burst_limit": "burstLimit", "rate_limit": "rateLimit"},
)
class ThrottleSettings:
    def __init__(
        self,
        *,
        burst_limit: typing.Optional[jsii.Number] = None,
        rate_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Container for defining throttling parameters to API stages.

        :param burst_limit: (experimental) The maximum API request rate limit over a time ranging from one to a few seconds. Default: none
        :param rate_limit: (experimental) The API request steady-state rate limit (average requests per second over an extended period of time). Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            throttle_settings = apigatewayv2.ThrottleSettings(
                burst_limit=123,
                rate_limit=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ThrottleSettings.__init__)
            check_type(argname="argument burst_limit", value=burst_limit, expected_type=type_hints["burst_limit"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
        self._values: typing.Dict[str, typing.Any] = {}
        if burst_limit is not None:
            self._values["burst_limit"] = burst_limit
        if rate_limit is not None:
            self._values["rate_limit"] = rate_limit

    @builtins.property
    def burst_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum API request rate limit over a time ranging from one to a few seconds.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("burst_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rate_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The API request steady-state rate limit (average requests per second over an extended period of time).

        :default: none

        :stability: experimental
        '''
        result = self._values.get("rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThrottleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVpcLink)
class VpcLink(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.VpcLink",
):
    '''(experimental) Define a new VPC Link Specifies an API Gateway VPC link for a HTTP API to access resources in an Amazon Virtual Private Cloud (VPC).

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ec2 as ec2
        
        
        vpc = ec2.Vpc(self, "VPC")
        vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpcLink.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromVpcLinkAttributes")
    @builtins.classmethod
    def from_vpc_link_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        vpc_link_id: builtins.str,
    ) -> IVpcLink:
        '''(experimental) Import a VPC Link by specifying its attributes.

        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC to which this VPC link is associated with.
        :param vpc_link_id: (experimental) The VPC Link id.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpcLink.from_vpc_link_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = VpcLinkAttributes(vpc=vpc, vpc_link_id=vpc_link_id)

        return typing.cast(IVpcLink, jsii.sinvoke(cls, "fromVpcLinkAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addSecurityGroups")
    def add_security_groups(self, *groups: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        '''(experimental) Adds the provided security groups to the vpc link.

        :param groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpcLink.add_security_groups)
            check_type(argname="argument groups", value=groups, expected_type=typing.Tuple[type_hints["groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSecurityGroups", [*groups]))

    @jsii.member(jsii_name="addSubnets")
    def add_subnets(self, *subnets: aws_cdk.aws_ec2.ISubnet) -> None:
        '''(experimental) Adds the provided subnets to the vpc link.

        :param subnets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpcLink.add_subnets)
            check_type(argname="argument subnets", value=subnets, expected_type=typing.Tuple[type_hints["subnets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSubnets", [*subnets]))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC to which this VPC Link is associated with.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        '''(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcLinkId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.VpcLinkAttributes",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "vpc_link_id": "vpcLinkId"},
)
class VpcLinkAttributes:
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, vpc_link_id: builtins.str) -> None:
        '''(experimental) Attributes when importing a new VpcLink.

        :param vpc: (experimental) The VPC to which this VPC link is associated with.
        :param vpc_link_id: (experimental) The VPC Link id.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            # vpc: ec2.Vpc
            
            awesome_link = apigwv2.VpcLink.from_vpc_link_attributes(self, "awesome-vpc-link",
                vpc_link_id="us-east-1_oiuR12Abd",
                vpc=vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VpcLinkAttributes.__init__)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_link_id", value=vpc_link_id, expected_type=type_hints["vpc_link_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "vpc_link_id": vpc_link_id,
        }

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC to which this VPC link is associated with.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def vpc_link_id(self) -> builtins.str:
        '''(experimental) The VPC Link id.

        :stability: experimental
        '''
        result = self._values.get("vpc_link_id")
        assert result is not None, "Required property 'vpc_link_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcLinkAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.VpcLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "vpc_link_name": "vpcLinkName",
    },
)
class VpcLinkProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            
            vpc = ec2.Vpc(self, "VPC")
            vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
        '''
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(VpcLinkProps.__init__)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc_link_name", value=vpc_link_name, expected_type=type_hints["vpc_link_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if vpc_link_name is not None:
            self._values["vpc_link_name"] = vpc_link_name

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC in which the private resources reside.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''(experimental) A list of security groups for the VPC link.

        :default: - no security groups. Use ``addSecurityGroups`` to add security groups

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) A list of subnets for the VPC link.

        :default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets

        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def vpc_link_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name used to label and identify the VPC link.

        :default: - automatically generated name

        :stability: experimental
        '''
        result = self._values.get("vpc_link_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWebSocketApi, IApi)
class WebSocketApi(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketApi",
):
    '''(experimental) Create a new API Gateway WebSocket API endpoint.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Api
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
        
        # message_handler: lambda.Function
        
        web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
        web_socket_api.add_route("sendmessage",
            integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_key_selection_expression: typing.Optional["WebSocketApiKeySelectionExpression"] = None,
        api_name: typing.Optional[builtins.str] = None,
        connect_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        default_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_key_selection_expression: (experimental) An API key selection expression. Providing this option will require an API Key be provided to access the API. Default: - Key is not required to access these APIs
        :param api_name: (experimental) Name for the WebSocket API resource. Default: - id of the WebSocketApi construct.
        :param connect_route_options: (experimental) Options to configure a '$connect' route. Default: - no '$connect' route configured
        :param default_route_options: (experimental) Options to configure a '$default' route. Default: - no '$default' route configured
        :param description: (experimental) The description of the API. Default: - none
        :param disconnect_route_options: (experimental) Options to configure a '$disconnect' route. Default: - no '$disconnect' route configured
        :param route_selection_expression: (experimental) The route selection expression for the API. Default: '$request.body.action'

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApi.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketApiProps(
            api_key_selection_expression=api_key_selection_expression,
            api_name=api_name,
            connect_route_options=connect_route_options,
            default_route_options=default_route_options,
            description=description,
            disconnect_route_options=disconnect_route_options,
            route_selection_expression=route_selection_expression,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromWebSocketApiAttributes")
    @builtins.classmethod
    def from_web_socket_api_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        web_socket_id: builtins.str,
        api_endpoint: typing.Optional[builtins.str] = None,
    ) -> IWebSocketApi:
        '''(experimental) Import an existing WebSocket API into this CDK app.

        :param scope: -
        :param id: -
        :param web_socket_id: (experimental) The identifier of the WebSocketApi.
        :param api_endpoint: (experimental) The endpoint URL of the WebSocketApi. Default: - throw san error if apiEndpoint is accessed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApi.from_web_socket_api_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = WebSocketApiAttributes(
            web_socket_id=web_socket_id, api_endpoint=api_endpoint
        )

        return typing.cast(IWebSocketApi, jsii.sinvoke(cls, "fromWebSocketApiAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        route_key: builtins.str,
        *,
        integration: "WebSocketRouteIntegration",
        authorizer: typing.Optional[IWebSocketRouteAuthorizer] = None,
    ) -> "WebSocketRoute":
        '''(experimental) Add a new route.

        :param route_key: -
        :param integration: (experimental) The integration to be configured on this route.
        :param authorizer: (experimental) The authorize to this route. You can only set authorizer to a $connect route. Default: - No Authorizer

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApi.add_route)
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
        options = WebSocketRouteOptions(integration=integration, authorizer=authorizer)

        return typing.cast("WebSocketRoute", jsii.invoke(self, "addRoute", [route_key, options]))

    @jsii.member(jsii_name="grantManageConnections")
    def grant_manage_connections(
        self,
        identity: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''(experimental) Grant access to the API Gateway management API for this WebSocket API to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApi.grant_manage_connections)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantManageConnections", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApi.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @builtins.property
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        '''(experimental) The default endpoint for an API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) The identifier of this API Gateway API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="webSocketApiName")
    def web_socket_api_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A human friendly name for this WebSocket API.

        Note that this is different from ``webSocketApiId``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webSocketApiName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketApiAttributes",
    jsii_struct_bases=[],
    name_mapping={"web_socket_id": "webSocketId", "api_endpoint": "apiEndpoint"},
)
class WebSocketApiAttributes:
    def __init__(
        self,
        *,
        web_socket_id: builtins.str,
        api_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes for importing a WebSocketApi into the CDK.

        :param web_socket_id: (experimental) The identifier of the WebSocketApi.
        :param api_endpoint: (experimental) The endpoint URL of the WebSocketApi. Default: - throw san error if apiEndpoint is accessed.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            web_socket_api = apigwv2.WebSocketApi.from_web_socket_api_attributes(self, "mywsapi", web_socket_id="api-1234")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApiAttributes.__init__)
            check_type(argname="argument web_socket_id", value=web_socket_id, expected_type=type_hints["web_socket_id"])
            check_type(argname="argument api_endpoint", value=api_endpoint, expected_type=type_hints["api_endpoint"])
        self._values: typing.Dict[str, typing.Any] = {
            "web_socket_id": web_socket_id,
        }
        if api_endpoint is not None:
            self._values["api_endpoint"] = api_endpoint

    @builtins.property
    def web_socket_id(self) -> builtins.str:
        '''(experimental) The identifier of the WebSocketApi.

        :stability: experimental
        '''
        result = self._values.get("web_socket_id")
        assert result is not None, "Required property 'web_socket_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The endpoint URL of the WebSocketApi.

        :default: - throw san error if apiEndpoint is accessed.

        :stability: experimental
        '''
        result = self._values.get("api_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketApiAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketApiKeySelectionExpression(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketApiKeySelectionExpression",
):
    '''(experimental) Represents the currently available API Key Selection Expressions.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        web_socket_api = apigwv2.WebSocketApi(self, "mywsapi",
            api_key_selection_expression=apigwv2.WebSocketApiKeySelectionExpression.HEADER_X_API_KEY
        )
    '''

    def __init__(self, custom_api_key_selector: builtins.str) -> None:
        '''
        :param custom_api_key_selector: The expression used by API Gateway.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApiKeySelectionExpression.__init__)
            check_type(argname="argument custom_api_key_selector", value=custom_api_key_selector, expected_type=type_hints["custom_api_key_selector"])
        jsii.create(self.__class__, self, [custom_api_key_selector])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTHORIZER_USAGE_IDENTIFIER_KEY")
    def AUTHORIZER_USAGE_IDENTIFIER_KEY(cls) -> "WebSocketApiKeySelectionExpression":
        '''(experimental) The API will extract the key value from the ``usageIdentifierKey`` attribute in the ``context`` map, returned by the Lambda Authorizer.

        See https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html

        :stability: experimental
        '''
        return typing.cast("WebSocketApiKeySelectionExpression", jsii.sget(cls, "AUTHORIZER_USAGE_IDENTIFIER_KEY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HEADER_X_API_KEY")
    def HEADER_X_API_KEY(cls) -> "WebSocketApiKeySelectionExpression":
        '''(experimental) The API will extract the key value from the ``x-api-key`` header in the user request.

        :stability: experimental
        '''
        return typing.cast("WebSocketApiKeySelectionExpression", jsii.sget(cls, "HEADER_X_API_KEY"))

    @builtins.property
    @jsii.member(jsii_name="customApiKeySelector")
    def custom_api_key_selector(self) -> builtins.str:
        '''(experimental) The expression used by API Gateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "customApiKeySelector"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_selection_expression": "apiKeySelectionExpression",
        "api_name": "apiName",
        "connect_route_options": "connectRouteOptions",
        "default_route_options": "defaultRouteOptions",
        "description": "description",
        "disconnect_route_options": "disconnectRouteOptions",
        "route_selection_expression": "routeSelectionExpression",
    },
)
class WebSocketApiProps:
    def __init__(
        self,
        *,
        api_key_selection_expression: typing.Optional[WebSocketApiKeySelectionExpression] = None,
        api_name: typing.Optional[builtins.str] = None,
        connect_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        default_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_route_options: typing.Optional[typing.Union["WebSocketRouteOptions", typing.Dict[str, typing.Any]]] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Props for WebSocket API.

        :param api_key_selection_expression: (experimental) An API key selection expression. Providing this option will require an API Key be provided to access the API. Default: - Key is not required to access these APIs
        :param api_name: (experimental) Name for the WebSocket API resource. Default: - id of the WebSocketApi construct.
        :param connect_route_options: (experimental) Options to configure a '$connect' route. Default: - no '$connect' route configured
        :param default_route_options: (experimental) Options to configure a '$default' route. Default: - no '$default' route configured
        :param description: (experimental) The description of the API. Default: - none
        :param disconnect_route_options: (experimental) Options to configure a '$disconnect' route. Default: - no '$disconnect' route configured
        :param route_selection_expression: (experimental) The route selection expression for the API. Default: '$request.body.action'

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_apigatewayv2_authorizers import WebSocketLambdaAuthorizer
            from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
            
            # This function handles your auth logic
            # auth_handler: lambda.Function
            
            # This function handles your WebSocket requests
            # handler: lambda.Function
            
            
            authorizer = WebSocketLambdaAuthorizer("Authorizer", auth_handler)
            
            integration = WebSocketLambdaIntegration("Integration", handler)
            
            apigwv2.WebSocketApi(self, "WebSocketApi",
                connect_route_options=apigwv2.WebSocketRouteOptions(
                    integration=integration,
                    authorizer=authorizer
                )
            )
        '''
        if isinstance(connect_route_options, dict):
            connect_route_options = WebSocketRouteOptions(**connect_route_options)
        if isinstance(default_route_options, dict):
            default_route_options = WebSocketRouteOptions(**default_route_options)
        if isinstance(disconnect_route_options, dict):
            disconnect_route_options = WebSocketRouteOptions(**disconnect_route_options)
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketApiProps.__init__)
            check_type(argname="argument api_key_selection_expression", value=api_key_selection_expression, expected_type=type_hints["api_key_selection_expression"])
            check_type(argname="argument api_name", value=api_name, expected_type=type_hints["api_name"])
            check_type(argname="argument connect_route_options", value=connect_route_options, expected_type=type_hints["connect_route_options"])
            check_type(argname="argument default_route_options", value=default_route_options, expected_type=type_hints["default_route_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disconnect_route_options", value=disconnect_route_options, expected_type=type_hints["disconnect_route_options"])
            check_type(argname="argument route_selection_expression", value=route_selection_expression, expected_type=type_hints["route_selection_expression"])
        self._values: typing.Dict[str, typing.Any] = {}
        if api_key_selection_expression is not None:
            self._values["api_key_selection_expression"] = api_key_selection_expression
        if api_name is not None:
            self._values["api_name"] = api_name
        if connect_route_options is not None:
            self._values["connect_route_options"] = connect_route_options
        if default_route_options is not None:
            self._values["default_route_options"] = default_route_options
        if description is not None:
            self._values["description"] = description
        if disconnect_route_options is not None:
            self._values["disconnect_route_options"] = disconnect_route_options
        if route_selection_expression is not None:
            self._values["route_selection_expression"] = route_selection_expression

    @builtins.property
    def api_key_selection_expression(
        self,
    ) -> typing.Optional[WebSocketApiKeySelectionExpression]:
        '''(experimental) An API key selection expression.

        Providing this option will require an API Key be provided to access the API.

        :default: - Key is not required to access these APIs

        :stability: experimental
        '''
        result = self._values.get("api_key_selection_expression")
        return typing.cast(typing.Optional[WebSocketApiKeySelectionExpression], result)

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the WebSocket API resource.

        :default: - id of the WebSocketApi construct.

        :stability: experimental
        '''
        result = self._values.get("api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_route_options(self) -> typing.Optional["WebSocketRouteOptions"]:
        '''(experimental) Options to configure a '$connect' route.

        :default: - no '$connect' route configured

        :stability: experimental
        '''
        result = self._values.get("connect_route_options")
        return typing.cast(typing.Optional["WebSocketRouteOptions"], result)

    @builtins.property
    def default_route_options(self) -> typing.Optional["WebSocketRouteOptions"]:
        '''(experimental) Options to configure a '$default' route.

        :default: - no '$default' route configured

        :stability: experimental
        '''
        result = self._values.get("default_route_options")
        return typing.cast(typing.Optional["WebSocketRouteOptions"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the API.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_route_options(self) -> typing.Optional["WebSocketRouteOptions"]:
        '''(experimental) Options to configure a '$disconnect' route.

        :default: - no '$disconnect' route configured

        :stability: experimental
        '''
        result = self._values.get("disconnect_route_options")
        return typing.cast(typing.Optional["WebSocketRouteOptions"], result)

    @builtins.property
    def route_selection_expression(self) -> typing.Optional[builtins.str]:
        '''(experimental) The route selection expression for the API.

        :default: '$request.body.action'

        :stability: experimental
        '''
        result = self._values.get("route_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWebSocketAuthorizer)
class WebSocketAuthorizer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketAuthorizer",
):
    '''(experimental) An authorizer for WebSocket Apis.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Authorizer
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # web_socket_api: apigatewayv2.WebSocketApi
        
        web_socket_authorizer = apigatewayv2.WebSocketAuthorizer(self, "MyWebSocketAuthorizer",
            identity_source=["identitySource"],
            type=apigatewayv2.WebSocketAuthorizerType.LAMBDA,
            web_socket_api=web_socket_api,
        
            # the properties below are optional
            authorizer_name="authorizerName",
            authorizer_uri="authorizerUri"
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        identity_source: typing.Sequence[builtins.str],
        type: "WebSocketAuthorizerType",
        web_socket_api: IWebSocketApi,
        authorizer_name: typing.Optional[builtins.str] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param identity_source: (experimental) The identity source for which authorization is requested.
        :param type: (experimental) The type of authorizer.
        :param web_socket_api: (experimental) WebSocket Api to attach the authorizer to.
        :param authorizer_name: (experimental) Name of the authorizer. Default: - id of the WebSocketAuthorizer construct.
        :param authorizer_uri: (experimental) The authorizer's Uniform Resource Identifier (URI). For REQUEST authorizers, this must be a well-formed Lambda function URI. Default: - required for Request authorizer types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketAuthorizer.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketAuthorizerProps(
            identity_source=identity_source,
            type=type,
            web_socket_api=web_socket_api,
            authorizer_name=authorizer_name,
            authorizer_uri=authorizer_uri,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromWebSocketAuthorizerAttributes")
    @builtins.classmethod
    def from_web_socket_authorizer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        authorizer_id: builtins.str,
        authorizer_type: builtins.str,
    ) -> IWebSocketRouteAuthorizer:
        '''(experimental) Import an existing WebSocket Authorizer into this CDK app.

        :param scope: -
        :param id: -
        :param authorizer_id: (experimental) Id of the Authorizer.
        :param authorizer_type: (experimental) Type of authorizer. Possible values are: - CUSTOM - Lambda Authorizer - NONE - No Authorization

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketAuthorizer.from_web_socket_authorizer_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = WebSocketAuthorizerAttributes(
            authorizer_id=authorizer_id, authorizer_type=authorizer_type
        )

        return typing.cast(IWebSocketRouteAuthorizer, jsii.sinvoke(cls, "fromWebSocketAuthorizerAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketAuthorizerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_id": "authorizerId",
        "authorizer_type": "authorizerType",
    },
)
class WebSocketAuthorizerAttributes:
    def __init__(
        self,
        *,
        authorizer_id: builtins.str,
        authorizer_type: builtins.str,
    ) -> None:
        '''(experimental) Reference to an WebSocket authorizer.

        :param authorizer_id: (experimental) Id of the Authorizer.
        :param authorizer_type: (experimental) Type of authorizer. Possible values are: - CUSTOM - Lambda Authorizer - NONE - No Authorization

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            web_socket_authorizer_attributes = apigatewayv2.WebSocketAuthorizerAttributes(
                authorizer_id="authorizerId",
                authorizer_type="authorizerType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketAuthorizerAttributes.__init__)
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument authorizer_type", value=authorizer_type, expected_type=type_hints["authorizer_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorizer_id": authorizer_id,
            "authorizer_type": authorizer_type,
        }

    @builtins.property
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        '''
        result = self._values.get("authorizer_id")
        assert result is not None, "Required property 'authorizer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_type(self) -> builtins.str:
        '''(experimental) Type of authorizer.

        Possible values are:

        - CUSTOM - Lambda Authorizer
        - NONE - No Authorization

        :stability: experimental
        '''
        result = self._values.get("authorizer_type")
        assert result is not None, "Required property 'authorizer_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketAuthorizerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_source": "identitySource",
        "type": "type",
        "web_socket_api": "webSocketApi",
        "authorizer_name": "authorizerName",
        "authorizer_uri": "authorizerUri",
    },
)
class WebSocketAuthorizerProps:
    def __init__(
        self,
        *,
        identity_source: typing.Sequence[builtins.str],
        type: "WebSocketAuthorizerType",
        web_socket_api: IWebSocketApi,
        authorizer_name: typing.Optional[builtins.str] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to initialize an instance of ``WebSocketAuthorizer``.

        :param identity_source: (experimental) The identity source for which authorization is requested.
        :param type: (experimental) The type of authorizer.
        :param web_socket_api: (experimental) WebSocket Api to attach the authorizer to.
        :param authorizer_name: (experimental) Name of the authorizer. Default: - id of the WebSocketAuthorizer construct.
        :param authorizer_uri: (experimental) The authorizer's Uniform Resource Identifier (URI). For REQUEST authorizers, this must be a well-formed Lambda function URI. Default: - required for Request authorizer types

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # web_socket_api: apigatewayv2.WebSocketApi
            
            web_socket_authorizer_props = apigatewayv2.WebSocketAuthorizerProps(
                identity_source=["identitySource"],
                type=apigatewayv2.WebSocketAuthorizerType.LAMBDA,
                web_socket_api=web_socket_api,
            
                # the properties below are optional
                authorizer_name="authorizerName",
                authorizer_uri="authorizerUri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketAuthorizerProps.__init__)
            check_type(argname="argument identity_source", value=identity_source, expected_type=type_hints["identity_source"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument web_socket_api", value=web_socket_api, expected_type=type_hints["web_socket_api"])
            check_type(argname="argument authorizer_name", value=authorizer_name, expected_type=type_hints["authorizer_name"])
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
        self._values: typing.Dict[str, typing.Any] = {
            "identity_source": identity_source,
            "type": type,
            "web_socket_api": web_socket_api,
        }
        if authorizer_name is not None:
            self._values["authorizer_name"] = authorizer_name
        if authorizer_uri is not None:
            self._values["authorizer_uri"] = authorizer_uri

    @builtins.property
    def identity_source(self) -> typing.List[builtins.str]:
        '''(experimental) The identity source for which authorization is requested.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        :stability: experimental
        '''
        result = self._values.get("identity_source")
        assert result is not None, "Required property 'identity_source' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> "WebSocketAuthorizerType":
        '''(experimental) The type of authorizer.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("WebSocketAuthorizerType", result)

    @builtins.property
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) WebSocket Api to attach the authorizer to.

        :stability: experimental
        '''
        result = self._values.get("web_socket_api")
        assert result is not None, "Required property 'web_socket_api' is missing"
        return typing.cast(IWebSocketApi, result)

    @builtins.property
    def authorizer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the authorizer.

        :default: - id of the WebSocketAuthorizer construct.

        :stability: experimental
        '''
        result = self._values.get("authorizer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authorizer's Uniform Resource Identifier (URI).

        For REQUEST authorizers, this must be a well-formed Lambda function URI.

        :default: - required for Request authorizer types

        :stability: experimental
        '''
        result = self._values.get("authorizer_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketAuthorizerType")
class WebSocketAuthorizerType(enum.Enum):
    '''(experimental) Supported Authorizer types.

    :stability: experimental
    '''

    LAMBDA = "LAMBDA"
    '''(experimental) Lambda Authorizer.

    :stability: experimental
    '''


@jsii.implements(IWebSocketIntegration)
class WebSocketIntegration(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketIntegration",
):
    '''(experimental) The integration for an API route.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Integration
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # web_socket_api: apigatewayv2.WebSocketApi
        
        web_socket_integration = apigatewayv2.WebSocketIntegration(self, "MyWebSocketIntegration",
            integration_type=apigatewayv2.WebSocketIntegrationType.AWS_PROXY,
            integration_uri="integrationUri",
            web_socket_api=web_socket_api
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        integration_type: "WebSocketIntegrationType",
        integration_uri: builtins.str,
        web_socket_api: IWebSocketApi,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param integration_type: (experimental) Integration type.
        :param integration_uri: (experimental) Integration URI.
        :param web_socket_api: (experimental) The WebSocket API to which this integration should be bound.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketIntegration.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketIntegrationProps(
            integration_type=integration_type,
            integration_uri=integration_uri,
            web_socket_api=web_socket_api,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        '''(experimental) Id of the integration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationId"))

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this integration.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "webSocketApi"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "integration_type": "integrationType",
        "integration_uri": "integrationUri",
        "web_socket_api": "webSocketApi",
    },
)
class WebSocketIntegrationProps:
    def __init__(
        self,
        *,
        integration_type: "WebSocketIntegrationType",
        integration_uri: builtins.str,
        web_socket_api: IWebSocketApi,
    ) -> None:
        '''(experimental) The integration properties.

        :param integration_type: (experimental) Integration type.
        :param integration_uri: (experimental) Integration URI.
        :param web_socket_api: (experimental) The WebSocket API to which this integration should be bound.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # web_socket_api: apigatewayv2.WebSocketApi
            
            web_socket_integration_props = apigatewayv2.WebSocketIntegrationProps(
                integration_type=apigatewayv2.WebSocketIntegrationType.AWS_PROXY,
                integration_uri="integrationUri",
                web_socket_api=web_socket_api
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketIntegrationProps.__init__)
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
            check_type(argname="argument integration_uri", value=integration_uri, expected_type=type_hints["integration_uri"])
            check_type(argname="argument web_socket_api", value=web_socket_api, expected_type=type_hints["web_socket_api"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration_type": integration_type,
            "integration_uri": integration_uri,
            "web_socket_api": web_socket_api,
        }

    @builtins.property
    def integration_type(self) -> "WebSocketIntegrationType":
        '''(experimental) Integration type.

        :stability: experimental
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast("WebSocketIntegrationType", result)

    @builtins.property
    def integration_uri(self) -> builtins.str:
        '''(experimental) Integration URI.

        :stability: experimental
        '''
        result = self._values.get("integration_uri")
        assert result is not None, "Required property 'integration_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API to which this integration should be bound.

        :stability: experimental
        '''
        result = self._values.get("web_socket_api")
        assert result is not None, "Required property 'web_socket_api' is missing"
        return typing.cast(IWebSocketApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketIntegrationType")
class WebSocketIntegrationType(enum.Enum):
    '''(experimental) WebSocket Integration Types.

    :stability: experimental
    '''

    AWS_PROXY = "AWS_PROXY"
    '''(experimental) AWS Proxy Integration Type.

    :stability: experimental
    '''
    MOCK = "MOCK"
    '''(experimental) Mock Integration Type.

    :stability: experimental
    '''


@jsii.implements(IWebSocketRouteAuthorizer)
class WebSocketNoneAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketNoneAuthorizer",
):
    '''(experimental) Explicitly configure no authorizers on specific WebSocket API routes.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        web_socket_none_authorizer = apigatewayv2.WebSocketNoneAuthorizer()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: IWebSocketRoute,
        scope: constructs.Construct,
    ) -> "WebSocketRouteAuthorizerConfig":
        '''(experimental) Bind this authorizer to a specified WebSocket route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        _ = WebSocketRouteAuthorizerBindOptions(route=route, scope=scope)

        return typing.cast("WebSocketRouteAuthorizerConfig", jsii.invoke(self, "bind", [_]))


@jsii.implements(IWebSocketRoute)
class WebSocketRoute(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRoute",
):
    '''(experimental) Route class that creates the Route for API Gateway WebSocket API.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Route
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # web_socket_api: apigatewayv2.WebSocketApi
        # web_socket_route_authorizer: apigatewayv2.IWebSocketRouteAuthorizer
        # web_socket_route_integration: apigatewayv2.WebSocketRouteIntegration
        
        web_socket_route = apigatewayv2.WebSocketRoute(self, "MyWebSocketRoute",
            integration=web_socket_route_integration,
            route_key="routeKey",
            web_socket_api=web_socket_api,
        
            # the properties below are optional
            api_key_required=False,
            authorizer=web_socket_route_authorizer
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        route_key: builtins.str,
        web_socket_api: IWebSocketApi,
        api_key_required: typing.Optional[builtins.bool] = None,
        integration: "WebSocketRouteIntegration",
        authorizer: typing.Optional[IWebSocketRouteAuthorizer] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param route_key: (experimental) The key to this route.
        :param web_socket_api: (experimental) The API the route is associated with.
        :param api_key_required: (experimental) Whether the route requires an API Key to be provided. Default: false
        :param integration: (experimental) The integration to be configured on this route.
        :param authorizer: (experimental) The authorize to this route. You can only set authorizer to a $connect route. Default: - No Authorizer

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRoute.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketRouteProps(
            route_key=route_key,
            web_socket_api=web_socket_api,
            api_key_required=api_key_required,
            integration=integration,
            authorizer=authorizer,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        '''(experimental) Id of the Route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeId"))

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        '''(experimental) The key to this route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeKey"))

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API associated with this route.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "webSocketApi"))

    @builtins.property
    @jsii.member(jsii_name="integrationResponseId")
    def integration_response_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Integration response ID.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationResponseId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteAuthorizerBindOptions",
    jsii_struct_bases=[],
    name_mapping={"route": "route", "scope": "scope"},
)
class WebSocketRouteAuthorizerBindOptions:
    def __init__(self, *, route: IWebSocketRoute, scope: constructs.Construct) -> None:
        '''(experimental) Input to the bind() operation, that binds an authorizer to a route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import constructs as constructs
            
            # construct: constructs.Construct
            # web_socket_route: apigatewayv2.WebSocketRoute
            
            web_socket_route_authorizer_bind_options = apigatewayv2.WebSocketRouteAuthorizerBindOptions(
                route=web_socket_route,
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteAuthorizerBindOptions.__init__)
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[str, typing.Any] = {
            "route": route,
            "scope": scope,
        }

    @builtins.property
    def route(self) -> IWebSocketRoute:
        '''(experimental) The route to which the authorizer is being bound.

        :stability: experimental
        '''
        result = self._values.get("route")
        assert result is not None, "Required property 'route' is missing"
        return typing.cast(IWebSocketRoute, result)

    @builtins.property
    def scope(self) -> constructs.Construct:
        '''(experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(constructs.Construct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteAuthorizerBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_type": "authorizationType",
        "authorizer_id": "authorizerId",
    },
)
class WebSocketRouteAuthorizerConfig:
    def __init__(
        self,
        *,
        authorization_type: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Results of binding an authorizer to an WebSocket route.

        :param authorization_type: (experimental) The type of authorization. Possible values are: - CUSTOM - Lambda Authorizer - NONE - No Authorization
        :param authorizer_id: (experimental) The authorizer id. Default: - No authorizer id (useful for AWS_IAM route authorizer)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            web_socket_route_authorizer_config = apigatewayv2.WebSocketRouteAuthorizerConfig(
                authorization_type="authorizationType",
            
                # the properties below are optional
                authorizer_id="authorizerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteAuthorizerConfig.__init__)
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorization_type": authorization_type,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id

    @builtins.property
    def authorization_type(self) -> builtins.str:
        '''(experimental) The type of authorization.

        Possible values are:

        - CUSTOM - Lambda Authorizer
        - NONE - No Authorization

        :stability: experimental
        '''
        result = self._values.get("authorization_type")
        assert result is not None, "Required property 'authorization_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authorizer id.

        :default: - No authorizer id (useful for AWS_IAM route authorizer)

        :stability: experimental
        '''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketRouteIntegration(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteIntegration",
):
    '''(experimental) The interface that various route integration classes will inherit.

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

    def __init__(self, id: builtins.str) -> None:
        '''(experimental) Initialize an integration for a route on websocket api.

        :param id: id of the underlying ``WebSocketIntegration`` construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteIntegration.__init__)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        *,
        route: IWebSocketRoute,
        scope: aws_cdk.core.Construct,
    ) -> "WebSocketRouteIntegrationConfig":
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        ...


class _WebSocketRouteIntegrationProxy(WebSocketRouteIntegration):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: IWebSocketRoute,
        scope: aws_cdk.core.Construct,
    ) -> "WebSocketRouteIntegrationConfig":
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = WebSocketRouteIntegrationBindOptions(route=route, scope=scope)

        return typing.cast("WebSocketRouteIntegrationConfig", jsii.invoke(self, "bind", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, WebSocketRouteIntegration).__jsii_proxy_class__ = lambda : _WebSocketRouteIntegrationProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteIntegrationBindOptions",
    jsii_struct_bases=[],
    name_mapping={"route": "route", "scope": "scope"},
)
class WebSocketRouteIntegrationBindOptions:
    def __init__(
        self,
        *,
        route: IWebSocketRoute,
        scope: aws_cdk.core.Construct,
    ) -> None:
        '''(experimental) Options to the WebSocketRouteIntegration during its bind operation.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.core as cdk
            
            # construct: cdk.Construct
            # web_socket_route: apigatewayv2.WebSocketRoute
            
            web_socket_route_integration_bind_options = apigatewayv2.WebSocketRouteIntegrationBindOptions(
                route=web_socket_route,
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteIntegrationBindOptions.__init__)
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[str, typing.Any] = {
            "route": route,
            "scope": scope,
        }

    @builtins.property
    def route(self) -> IWebSocketRoute:
        '''(experimental) The route to which this is being bound.

        :stability: experimental
        '''
        result = self._values.get("route")
        assert result is not None, "Required property 'route' is missing"
        return typing.cast(IWebSocketRoute, result)

    @builtins.property
    def scope(self) -> aws_cdk.core.Construct:
        '''(experimental) The current scope in which the bind is occurring.

        If the ``WebSocketRouteIntegration`` being bound creates additional constructs,
        this will be used as their parent scope.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(aws_cdk.core.Construct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteIntegrationBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class WebSocketRouteIntegrationConfig:
    def __init__(self, *, type: WebSocketIntegrationType, uri: builtins.str) -> None:
        '''(experimental) Config returned back as a result of the bind.

        :param type: (experimental) Integration type.
        :param uri: (experimental) Integration URI.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            web_socket_route_integration_config = apigatewayv2.WebSocketRouteIntegrationConfig(
                type=apigatewayv2.WebSocketIntegrationType.AWS_PROXY,
                uri="uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteIntegrationConfig.__init__)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
            "uri": uri,
        }

    @builtins.property
    def type(self) -> WebSocketIntegrationType:
        '''(experimental) Integration type.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(WebSocketIntegrationType, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''(experimental) Integration URI.

        :stability: experimental
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteOptions",
    jsii_struct_bases=[],
    name_mapping={"integration": "integration", "authorizer": "authorizer"},
)
class WebSocketRouteOptions:
    def __init__(
        self,
        *,
        integration: WebSocketRouteIntegration,
        authorizer: typing.Optional[IWebSocketRouteAuthorizer] = None,
    ) -> None:
        '''(experimental) Options used to add route to the API.

        :param integration: (experimental) The integration to be configured on this route.
        :param authorizer: (experimental) The authorize to this route. You can only set authorizer to a $connect route. Default: - No Authorizer

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
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteOptions.__init__)
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
        }
        if authorizer is not None:
            self._values["authorizer"] = authorizer

    @builtins.property
    def integration(self) -> WebSocketRouteIntegration:
        '''(experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return typing.cast(WebSocketRouteIntegration, result)

    @builtins.property
    def authorizer(self) -> typing.Optional[IWebSocketRouteAuthorizer]:
        '''(experimental) The authorize to this route.

        You can only set authorizer to a $connect route.

        :default: - No Authorizer

        :stability: experimental
        '''
        result = self._values.get("authorizer")
        return typing.cast(typing.Optional[IWebSocketRouteAuthorizer], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketRouteProps",
    jsii_struct_bases=[WebSocketRouteOptions],
    name_mapping={
        "integration": "integration",
        "authorizer": "authorizer",
        "route_key": "routeKey",
        "web_socket_api": "webSocketApi",
        "api_key_required": "apiKeyRequired",
    },
)
class WebSocketRouteProps(WebSocketRouteOptions):
    def __init__(
        self,
        *,
        integration: WebSocketRouteIntegration,
        authorizer: typing.Optional[IWebSocketRouteAuthorizer] = None,
        route_key: builtins.str,
        web_socket_api: IWebSocketApi,
        api_key_required: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new Route.

        :param integration: (experimental) The integration to be configured on this route.
        :param authorizer: (experimental) The authorize to this route. You can only set authorizer to a $connect route. Default: - No Authorizer
        :param route_key: (experimental) The key to this route.
        :param web_socket_api: (experimental) The API the route is associated with.
        :param api_key_required: (experimental) Whether the route requires an API Key to be provided. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # web_socket_api: apigatewayv2.WebSocketApi
            # web_socket_route_authorizer: apigatewayv2.IWebSocketRouteAuthorizer
            # web_socket_route_integration: apigatewayv2.WebSocketRouteIntegration
            
            web_socket_route_props = apigatewayv2.WebSocketRouteProps(
                integration=web_socket_route_integration,
                route_key="routeKey",
                web_socket_api=web_socket_api,
            
                # the properties below are optional
                api_key_required=False,
                authorizer=web_socket_route_authorizer
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketRouteProps.__init__)
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument web_socket_api", value=web_socket_api, expected_type=type_hints["web_socket_api"])
            check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
            "route_key": route_key,
            "web_socket_api": web_socket_api,
        }
        if authorizer is not None:
            self._values["authorizer"] = authorizer
        if api_key_required is not None:
            self._values["api_key_required"] = api_key_required

    @builtins.property
    def integration(self) -> WebSocketRouteIntegration:
        '''(experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return typing.cast(WebSocketRouteIntegration, result)

    @builtins.property
    def authorizer(self) -> typing.Optional[IWebSocketRouteAuthorizer]:
        '''(experimental) The authorize to this route.

        You can only set authorizer to a $connect route.

        :default: - No Authorizer

        :stability: experimental
        '''
        result = self._values.get("authorizer")
        return typing.cast(typing.Optional[IWebSocketRouteAuthorizer], result)

    @builtins.property
    def route_key(self) -> builtins.str:
        '''(experimental) The key to this route.

        :stability: experimental
        '''
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The API the route is associated with.

        :stability: experimental
        '''
        result = self._values.get("web_socket_api")
        assert result is not None, "Required property 'web_socket_api' is missing"
        return typing.cast(IWebSocketApi, result)

    @builtins.property
    def api_key_required(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the route requires an API Key to be provided.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("api_key_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWebSocketStage, IStage)
class WebSocketStage(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketStage",
):
    '''(experimental) Represents a stage where an instance of the API is deployed.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Stage
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

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        stage_name: builtins.str,
        web_socket_api: IWebSocketApi,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stage_name: (experimental) The name of the stage.
        :param web_socket_api: (experimental) The WebSocket API to which this stage is associated.
        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStage.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketStageProps(
            stage_name=stage_name,
            web_socket_api=web_socket_api,
            auto_deploy=auto_deploy,
            domain_mapping=domain_mapping,
            throttle=throttle,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromWebSocketStageAttributes")
    @builtins.classmethod
    def from_web_socket_stage_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api: IWebSocketApi,
        stage_name: builtins.str,
    ) -> IWebSocketStage:
        '''(experimental) Import an existing stage into this CDK app.

        :param scope: -
        :param id: -
        :param api: (experimental) The API to which this stage is associated.
        :param stage_name: (experimental) The name of the stage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStage.from_web_socket_stage_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = WebSocketStageAttributes(api=api, stage_name=stage_name)

        return typing.cast(IWebSocketStage, jsii.sinvoke(cls, "fromWebSocketStageAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="grantManagementApiAccess")
    def grant_management_api_access(
        self,
        identity: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''(experimental) Grant access to the API Gateway management API for this WebSocket API Stage to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStage.grant_management_api_access)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantManagementApiAccess", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this HTTP Api Gateway Stage.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStage.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IWebSocketApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        return typing.cast(IWebSocketApi, jsii.get(self, "api"))

    @builtins.property
    @jsii.member(jsii_name="baseApi")
    def _base_api(self) -> IApi:
        '''
        :stability: experimental
        '''
        return typing.cast(IApi, jsii.get(self, "baseApi"))

    @builtins.property
    @jsii.member(jsii_name="callbackUrl")
    def callback_url(self) -> builtins.str:
        '''(experimental) The callback URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "callbackUrl"))

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''(experimental) The websocket URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketStageAttributes",
    jsii_struct_bases=[StageAttributes],
    name_mapping={"stage_name": "stageName", "api": "api"},
)
class WebSocketStageAttributes(StageAttributes):
    def __init__(self, *, stage_name: builtins.str, api: IWebSocketApi) -> None:
        '''(experimental) The attributes used to import existing WebSocketStage.

        :param stage_name: (experimental) The name of the stage.
        :param api: (experimental) The API to which this stage is associated.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # web_socket_api: apigatewayv2.WebSocketApi
            
            web_socket_stage_attributes = apigatewayv2.WebSocketStageAttributes(
                api=web_socket_api,
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStageAttributes.__init__)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
            "api": api,
        }

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api(self) -> IWebSocketApi:
        '''(experimental) The API to which this stage is associated.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IWebSocketApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketStageAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.WebSocketStageProps",
    jsii_struct_bases=[StageOptions],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "domain_mapping": "domainMapping",
        "throttle": "throttle",
        "stage_name": "stageName",
        "web_socket_api": "webSocketApi",
    },
)
class WebSocketStageProps(StageOptions):
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
        stage_name: builtins.str,
        web_socket_api: IWebSocketApi,
    ) -> None:
        '''(experimental) Properties to initialize an instance of ``WebSocketStage``.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration
        :param stage_name: (experimental) The name of the stage.
        :param web_socket_api: (experimental) The WebSocket API to which this stage is associated.

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
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        if isinstance(throttle, dict):
            throttle = ThrottleSettings(**throttle)
        if __debug__:
            type_hints = typing.get_type_hints(WebSocketStageProps.__init__)
            check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
            check_type(argname="argument domain_mapping", value=domain_mapping, expected_type=type_hints["domain_mapping"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument web_socket_api", value=web_socket_api, expected_type=type_hints["web_socket_api"])
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
            "web_socket_api": web_socket_api,
        }
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping
        if throttle is not None:
            self._values["throttle"] = throttle

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        '''(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        '''
        result = self._values.get("domain_mapping")
        return typing.cast(typing.Optional[DomainMappingOptions], result)

    @builtins.property
    def throttle(self) -> typing.Optional[ThrottleSettings]:
        '''(experimental) Throttle settings for the routes of this stage.

        :default: - no throttling configuration

        :stability: experimental
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[ThrottleSettings], result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_socket_api(self) -> IWebSocketApi:
        '''(experimental) The WebSocket API to which this stage is associated.

        :stability: experimental
        '''
        result = self._values.get("web_socket_api")
        assert result is not None, "Required property 'web_socket_api' is missing"
        return typing.cast(IWebSocketApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.AddRoutesOptions",
    jsii_struct_bases=[BatchHttpRouteOptions],
    name_mapping={
        "integration": "integration",
        "path": "path",
        "authorization_scopes": "authorizationScopes",
        "authorizer": "authorizer",
        "methods": "methods",
    },
)
class AddRoutesOptions(BatchHttpRouteOptions):
    def __init__(
        self,
        *,
        integration: HttpRouteIntegration,
        path: builtins.str,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional[IHttpRouteAuthorizer] = None,
        methods: typing.Optional[typing.Sequence[HttpMethod]] = None,
    ) -> None:
        '''(experimental) Options for the Route with Integration resource.

        :param integration: (experimental) The integration to be configured on this route.
        :param path: (experimental) The path at which all of these routes are configured.
        :param authorization_scopes: (experimental) The list of OIDC scopes to include in the authorization. These scopes will override the default authorization scopes on the gateway. Set to [] to remove default scopes Default: - uses defaultAuthorizationScopes if configured on the API, otherwise none.
        :param authorizer: (experimental) Authorizer to be associated to these routes. Use NoneAuthorizer to remove the default authorizer for the api Default: - uses the default authorizer if one is specified on the HttpApi
        :param methods: (experimental) The HTTP methods to be configured. Default: HttpMethod.ANY

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
        if __debug__:
            type_hints = typing.get_type_hints(AddRoutesOptions.__init__)
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
            "path": path,
        }
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorizer is not None:
            self._values["authorizer"] = authorizer
        if methods is not None:
            self._values["methods"] = methods

    @builtins.property
    def integration(self) -> HttpRouteIntegration:
        '''(experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return typing.cast(HttpRouteIntegration, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) The path at which all of these routes are configured.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of OIDC scopes to include in the authorization.

        These scopes will override the default authorization scopes on the gateway.
        Set to [] to remove default scopes

        :default: - uses defaultAuthorizationScopes if configured on the API, otherwise none.

        :stability: experimental
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorizer(self) -> typing.Optional[IHttpRouteAuthorizer]:
        '''(experimental) Authorizer to be associated to these routes.

        Use NoneAuthorizer to remove the default authorizer for the api

        :default: - uses the default authorizer if one is specified on the HttpApi

        :stability: experimental
        '''
        result = self._values.get("authorizer")
        return typing.cast(typing.Optional[IHttpRouteAuthorizer], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[HttpMethod]]:
        '''(experimental) The HTTP methods to be configured.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[HttpMethod]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRoutesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApiMapping)
class ApiMapping(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.ApiMapping",
):
    '''(experimental) Create a new API mapping for API Gateway API endpoint.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::ApiMapping
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # api: apigatewayv2.IApi
        # domain_name: apigatewayv2.DomainName
        # stage: apigatewayv2.IStage
        
        api_mapping = apigatewayv2.ApiMapping(self, "MyApiMapping",
            api=api,
            domain_name=domain_name,
        
            # the properties below are optional
            api_mapping_key="apiMappingKey",
            stage=stage
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api: IApi,
        domain_name: IDomainName,
        api_mapping_key: typing.Optional[builtins.str] = None,
        stage: typing.Optional[IStage] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) The Api to which this mapping is applied.
        :param domain_name: (experimental) custom domain name of the mapping target.
        :param api_mapping_key: (experimental) Api mapping key. The path where this stage should be mapped to on the domain Default: - undefined for the root path mapping.
        :param stage: (experimental) stage for the ApiMapping resource required for WebSocket API defaults to default stage of an HTTP API. Default: - Default stage of the passed API for HTTP API, required for WebSocket API

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApiMapping.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiMappingProps(
            api=api,
            domain_name=domain_name,
            api_mapping_key=api_mapping_key,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApiMappingAttributes")
    @builtins.classmethod
    def from_api_mapping_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_mapping_id: builtins.str,
    ) -> IApiMapping:
        '''(experimental) import from API ID.

        :param scope: -
        :param id: -
        :param api_mapping_id: (experimental) The API mapping ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApiMapping.from_api_mapping_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ApiMappingAttributes(api_mapping_id=api_mapping_id)

        return typing.cast(IApiMapping, jsii.sinvoke(cls, "fromApiMappingAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        '''(experimental) ID of the API Mapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiMappingId"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> IDomainName:
        '''(experimental) API domain name.

        :stability: experimental
        '''
        return typing.cast(IDomainName, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="mappingKey")
    def mapping_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) API Mapping key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingKey"))


@jsii.implements(IDomainName)
class DomainName(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainName",
):
    '''(experimental) Custom domain resource for the API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_certificatemanager as acm
        from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
        
        # handler: lambda.Function
        
        
        cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
        domain_name = "example.com"
        
        dn = apigwv2.DomainName(self, "DN",
            domain_name=domain_name,
            certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn)
        )
        api = apigwv2.HttpApi(self, "HttpProxyProdApi",
            default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
            # https://${dn.domainName}/foo goes to prodApi $default stage
            default_domain_mapping=apigwv2.DomainMappingOptions(
                domain_name=dn,
                mapping_key="foo"
            )
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        mtls: typing.Optional[typing.Union[MTLSConfig, typing.Dict[str, typing.Any]]] = None,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        certificate_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[EndpointType] = None,
        ownership_certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        security_policy: typing.Optional[SecurityPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain_name: (experimental) The custom domain name.
        :param mtls: (experimental) The mutual TLS authentication configuration for a custom domain name. Default: - mTLS is not configured.
        :param certificate: (experimental) The ACM certificate for this domain name. Certificate can be both ACM issued or imported.
        :param certificate_name: (experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name. Default: - No friendly certificate name
        :param endpoint_type: (experimental) The type of endpoint for this DomainName. Default: EndpointType.REGIONAL
        :param ownership_certificate: (experimental) A public certificate issued by ACM to validate that you own a custom domain. This parameter is required only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate for ``certificate``. The ownership certificate validates that you have permissions to use the domain name. Default: - only required when configuring mTLS
        :param security_policy: (experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name. Default: SecurityPolicy.TLS_1_2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainName.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainNameProps(
            domain_name=domain_name,
            mtls=mtls,
            certificate=certificate,
            certificate_name=certificate_name,
            endpoint_type=endpoint_type,
            ownership_certificate=ownership_certificate,
            security_policy=security_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainNameAttributes")
    @builtins.classmethod
    def from_domain_name_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> IDomainName:
        '''(experimental) Import from attributes.

        :param scope: -
        :param id: -
        :param name: (experimental) domain name string.
        :param regional_domain_name: (experimental) The domain name associated with the regional endpoint for this custom domain name.
        :param regional_hosted_zone_id: (experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DomainName.from_domain_name_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DomainNameAttributes(
            name=name,
            regional_domain_name=regional_domain_name,
            regional_hosted_zone_id=regional_hosted_zone_id,
        )

        return typing.cast(IDomainName, jsii.sinvoke(cls, "fromDomainNameAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addEndpoint")
    def add_endpoint(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        certificate_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[EndpointType] = None,
        ownership_certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        security_policy: typing.Optional[SecurityPolicy] = None,
    ) -> None:
        '''(experimental) Adds an endpoint to a domain name.

        :param certificate: (experimental) The ACM certificate for this domain name. Certificate can be both ACM issued or imported.
        :param certificate_name: (experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name. Default: - No friendly certificate name
        :param endpoint_type: (experimental) The type of endpoint for this DomainName. Default: EndpointType.REGIONAL
        :param ownership_certificate: (experimental) A public certificate issued by ACM to validate that you own a custom domain. This parameter is required only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate for ``certificate``. The ownership certificate validates that you have permissions to use the domain name. Default: - only required when configuring mTLS
        :param security_policy: (experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name. Default: SecurityPolicy.TLS_1_2

        :stability: experimental
        '''
        options = EndpointOptions(
            certificate=certificate,
            certificate_name=certificate_name,
            endpoint_type=endpoint_type,
            ownership_certificate=ownership_certificate,
            security_policy=security_policy,
        )

        return typing.cast(None, jsii.invoke(self, "addEndpoint", [options]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The custom domain name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalDomainName"))

    @builtins.property
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalHostedZoneId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainNameProps",
    jsii_struct_bases=[EndpointOptions],
    name_mapping={
        "certificate": "certificate",
        "certificate_name": "certificateName",
        "endpoint_type": "endpointType",
        "ownership_certificate": "ownershipCertificate",
        "security_policy": "securityPolicy",
        "domain_name": "domainName",
        "mtls": "mtls",
    },
)
class DomainNameProps(EndpointOptions):
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        certificate_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[EndpointType] = None,
        ownership_certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        security_policy: typing.Optional[SecurityPolicy] = None,
        domain_name: builtins.str,
        mtls: typing.Optional[typing.Union[MTLSConfig, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) properties used for creating the DomainName.

        :param certificate: (experimental) The ACM certificate for this domain name. Certificate can be both ACM issued or imported.
        :param certificate_name: (experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name. Default: - No friendly certificate name
        :param endpoint_type: (experimental) The type of endpoint for this DomainName. Default: EndpointType.REGIONAL
        :param ownership_certificate: (experimental) A public certificate issued by ACM to validate that you own a custom domain. This parameter is required only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate for ``certificate``. The ownership certificate validates that you have permissions to use the domain name. Default: - only required when configuring mTLS
        :param security_policy: (experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name. Default: SecurityPolicy.TLS_1_2
        :param domain_name: (experimental) The custom domain name.
        :param mtls: (experimental) The mutual TLS authentication configuration for a custom domain name. Default: - mTLS is not configured.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_certificatemanager as acm
            from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
            
            # handler: lambda.Function
            
            
            cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
            domain_name = "example.com"
            
            dn = apigwv2.DomainName(self, "DN",
                domain_name=domain_name,
                certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn)
            )
            api = apigwv2.HttpApi(self, "HttpProxyProdApi",
                default_integration=HttpLambdaIntegration("DefaultIntegration", handler),
                # https://${dn.domainName}/foo goes to prodApi $default stage
                default_domain_mapping=apigwv2.DomainMappingOptions(
                    domain_name=dn,
                    mapping_key="foo"
                )
            )
        '''
        if isinstance(mtls, dict):
            mtls = MTLSConfig(**mtls)
        if __debug__:
            type_hints = typing.get_type_hints(DomainNameProps.__init__)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument ownership_certificate", value=ownership_certificate, expected_type=type_hints["ownership_certificate"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument mtls", value=mtls, expected_type=type_hints["mtls"])
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "domain_name": domain_name,
        }
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if ownership_certificate is not None:
            self._values["ownership_certificate"] = ownership_certificate
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if mtls is not None:
            self._values["mtls"] = mtls

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        '''(experimental) The ACM certificate for this domain name.

        Certificate can be both ACM issued or imported.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(aws_cdk.aws_certificatemanager.ICertificate, result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user-friendly name of the certificate that will be used by the endpoint for this domain name.

        :default: - No friendly certificate name

        :stability: experimental
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[EndpointType]:
        '''(experimental) The type of endpoint for this DomainName.

        :default: EndpointType.REGIONAL

        :stability: experimental
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[EndpointType], result)

    @builtins.property
    def ownership_certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        '''(experimental) A public certificate issued by ACM to validate that you own a custom domain.

        This parameter is required
        only when you configure mutual TLS authentication and you specify an ACM imported or private CA certificate
        for ``certificate``. The ownership certificate validates that you have permissions to use the domain name.

        :default: - only required when configuring mTLS

        :stability: experimental
        '''
        result = self._values.get("ownership_certificate")
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[SecurityPolicy]:
        '''(experimental) The Transport Layer Security (TLS) version + cipher suite for this domain name.

        :default: SecurityPolicy.TLS_1_2

        :stability: experimental
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[SecurityPolicy], result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The custom domain name.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mtls(self) -> typing.Optional[MTLSConfig]:
        '''(experimental) The mutual TLS authentication configuration for a custom domain name.

        :default: - mTLS is not configured.

        :stability: experimental
        '''
        result = self._values.get("mtls")
        return typing.cast(typing.Optional[MTLSConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IHttpApi, IApi)
class HttpApi(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApi",
):
    '''(experimental) Create a new API Gateway HTTP API endpoint.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Api
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
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_name: typing.Optional[builtins.str] = None,
        cors_preflight: typing.Optional[typing.Union[CorsPreflightOptions, typing.Dict[str, typing.Any]]] = None,
        create_default_stage: typing.Optional[builtins.bool] = None,
        default_authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_authorizer: typing.Optional[IHttpRouteAuthorizer] = None,
        default_domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        default_integration: typing.Optional[HttpRouteIntegration] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_name: (experimental) Name for the HTTP API resource. Default: - id of the HttpApi construct.
        :param cors_preflight: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: (experimental) Whether a default stage and deployment should be automatically created. Default: true
        :param default_authorization_scopes: (experimental) Default OIDC scopes attached to all routes in the gateway, unless explicitly configured on the route. Default: - no default authorization scopes
        :param default_authorizer: (experimental) Default Authorizer to applied to all routes in the gateway. Default: - No authorizer
        :param default_domain_mapping: (experimental) Configure a custom domain with the API mapping resource to the HTTP API. Default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.
        :param default_integration: (experimental) An integration that will be configured on the catch-all route ($default). Default: - none
        :param description: (experimental) The description of the API. Default: - none
        :param disable_execute_api_endpoint: (experimental) Specifies whether clients can invoke your API using the default endpoint. By default, clients can invoke your API with the default ``https://{api_id}.execute-api.{region}.amazonaws.com`` endpoint. Enable this if you would like clients to use your custom domain name. Default: false execute-api endpoint enabled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpApi.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpApiProps(
            api_name=api_name,
            cors_preflight=cors_preflight,
            create_default_stage=create_default_stage,
            default_authorization_scopes=default_authorization_scopes,
            default_authorizer=default_authorizer,
            default_domain_mapping=default_domain_mapping,
            default_integration=default_integration,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpApiAttributes")
    @builtins.classmethod
    def from_http_api_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api_id: builtins.str,
        api_endpoint: typing.Optional[builtins.str] = None,
    ) -> IHttpApi:
        '''(experimental) Import an existing HTTP API into this CDK app.

        :param scope: -
        :param id: -
        :param http_api_id: (experimental) The identifier of the HttpApi.
        :param api_endpoint: (experimental) The endpoint URL of the HttpApi. Default: - throws an error if apiEndpoint is accessed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpApi.from_http_api_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = HttpApiAttributes(http_api_id=http_api_id, api_endpoint=api_endpoint)

        return typing.cast(IHttpApi, jsii.sinvoke(cls, "fromHttpApiAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addRoutes")
    def add_routes(
        self,
        *,
        path: builtins.str,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional[IHttpRouteAuthorizer] = None,
        methods: typing.Optional[typing.Sequence[HttpMethod]] = None,
        integration: HttpRouteIntegration,
    ) -> typing.List["HttpRoute"]:
        '''(experimental) Add multiple routes that uses the same configuration.

        The routes all go to the same path, but for different
        methods.

        :param path: (experimental) The path at which all of these routes are configured.
        :param authorization_scopes: (experimental) The list of OIDC scopes to include in the authorization. These scopes will override the default authorization scopes on the gateway. Set to [] to remove default scopes Default: - uses defaultAuthorizationScopes if configured on the API, otherwise none.
        :param authorizer: (experimental) Authorizer to be associated to these routes. Use NoneAuthorizer to remove the default authorizer for the api Default: - uses the default authorizer if one is specified on the HttpApi
        :param methods: (experimental) The HTTP methods to be configured. Default: HttpMethod.ANY
        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        options = AddRoutesOptions(
            path=path,
            authorization_scopes=authorization_scopes,
            authorizer=authorizer,
            methods=methods,
            integration=integration,
        )

        return typing.cast(typing.List["HttpRoute"], jsii.invoke(self, "addRoutes", [options]))

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        id: builtins.str,
        *,
        stage_name: typing.Optional[builtins.str] = None,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
    ) -> "HttpStage":
        '''(experimental) Add a new stage.

        :param id: -
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpApi.add_stage)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = HttpStageOptions(
            stage_name=stage_name,
            auto_deploy=auto_deploy,
            domain_mapping=domain_mapping,
            throttle=throttle,
        )

        return typing.cast("HttpStage", jsii.invoke(self, "addStage", [id, options]))

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> VpcLink:
        '''(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        '''
        options = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        return typing.cast(VpcLink, jsii.invoke(self, "addVpcLink", [options]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpApi.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricClientError", [props]))

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricCount", [props]))

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataProcessed", [props]))

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIntegrationLatency", [props]))

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricLatency", [props]))

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricServerError", [props]))

    @builtins.property
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        '''(experimental) Get the default endpoint for this API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) The identifier of this API Gateway API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        '''(experimental) The identifier of this API Gateway HTTP API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpApiId"))

    @builtins.property
    @jsii.member(jsii_name="defaultStage")
    def default_stage(self) -> typing.Optional["IHttpStage"]:
        '''(experimental) The default stage of this API.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IHttpStage"], jsii.get(self, "defaultStage"))

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether clients can invoke this HTTP API by using the default execute-api endpoint.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "disableExecuteApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="httpApiName")
    def http_api_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A human friendly name for this HTTP API.

        Note that this is different from ``httpApiId``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpApiName"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Get the URL to the default stage of this API.

        Returns ``undefined`` if ``createDefaultStage`` is unset.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "url"))


@jsii.implements(IHttpAuthorizer)
class HttpAuthorizer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpAuthorizer",
):
    '''(experimental) An authorizer for Http Apis.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Authorizer
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        import aws_cdk.core as cdk
        
        # http_api: apigatewayv2.HttpApi
        
        http_authorizer = apigatewayv2.HttpAuthorizer(self, "MyHttpAuthorizer",
            http_api=http_api,
            identity_source=["identitySource"],
            type=apigatewayv2.HttpAuthorizerType.IAM,
        
            # the properties below are optional
            authorizer_name="authorizerName",
            authorizer_uri="authorizerUri",
            enable_simple_responses=False,
            jwt_audience=["jwtAudience"],
            jwt_issuer="jwtIssuer",
            payload_format_version=apigatewayv2.AuthorizerPayloadVersion.VERSION_1_0,
            results_cache_ttl=cdk.Duration.minutes(30)
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        identity_source: typing.Sequence[builtins.str],
        type: HttpAuthorizerType,
        authorizer_name: typing.Optional[builtins.str] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[builtins.bool] = None,
        jwt_audience: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwt_issuer: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[AuthorizerPayloadVersion] = None,
        results_cache_ttl: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param http_api: (experimental) HTTP Api to attach the authorizer to.
        :param identity_source: (experimental) The identity source for which authorization is requested.
        :param type: (experimental) The type of authorizer.
        :param authorizer_name: (experimental) Name of the authorizer. Default: - id of the HttpAuthorizer construct.
        :param authorizer_uri: (experimental) The authorizer's Uniform Resource Identifier (URI). For REQUEST authorizers, this must be a well-formed Lambda function URI. Default: - required for Request authorizer types
        :param enable_simple_responses: (experimental) Specifies whether a Lambda authorizer returns a response in a simple format. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Default: - The lambda authorizer must return an IAM policy as its response
        :param jwt_audience: (experimental) A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list. Default: - required for JWT authorizer typess.
        :param jwt_issuer: (experimental) The base domain of the identity provider that issues JWT. Default: - required for JWT authorizer types.
        :param payload_format_version: (experimental) Specifies the format of the payload sent to an HTTP API Lambda authorizer. Default: AuthorizerPayloadVersion.VERSION_2_0 if the authorizer type is HttpAuthorizerType.LAMBDA
        :param results_cache_ttl: (experimental) How long APIGateway should cache the results. Max 1 hour. Default: - API Gateway will not cache authorizer responses

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAuthorizer.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpAuthorizerProps(
            http_api=http_api,
            identity_source=identity_source,
            type=type,
            authorizer_name=authorizer_name,
            authorizer_uri=authorizer_uri,
            enable_simple_responses=enable_simple_responses,
            jwt_audience=jwt_audience,
            jwt_issuer=jwt_issuer,
            payload_format_version=payload_format_version,
            results_cache_ttl=results_cache_ttl,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpAuthorizerAttributes")
    @builtins.classmethod
    def from_http_authorizer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        authorizer_id: builtins.str,
        authorizer_type: builtins.str,
    ) -> IHttpRouteAuthorizer:
        '''(experimental) Import an existing HTTP Authorizer into this CDK app.

        :param scope: -
        :param id: -
        :param authorizer_id: (experimental) Id of the Authorizer.
        :param authorizer_type: (experimental) Type of authorizer. Possible values are: - JWT - JSON Web Token Authorizer - CUSTOM - Lambda Authorizer - NONE - No Authorization

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpAuthorizer.from_http_authorizer_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = HttpAuthorizerAttributes(
            authorizer_id=authorizer_id, authorizer_type=authorizer_type
        )

        return typing.cast(IHttpRouteAuthorizer, jsii.sinvoke(cls, "fromHttpAuthorizerAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        '''(experimental) Id of the Authorizer.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))


@jsii.implements(IHttpRouteAuthorizer)
class HttpNoneAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpNoneAuthorizer",
):
    '''(experimental) Explicitly configure no authorizers on specific HTTP API routes.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_authorizers import HttpJwtAuthorizer
        from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration
        
        
        issuer = "https://test.us.auth0.com"
        authorizer = HttpJwtAuthorizer("DefaultAuthorizer", issuer,
            jwt_audience=["3131231"]
        )
        
        api = apigwv2.HttpApi(self, "HttpApi",
            default_authorizer=authorizer,
            default_authorization_scopes=["read:books"]
        )
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books",
            methods=[apigwv2.HttpMethod.GET]
        )
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIdIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books/{id}",
            methods=[apigwv2.HttpMethod.GET]
        )
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books",
            methods=[apigwv2.HttpMethod.POST],
            authorization_scopes=["write:books"]
        )
        
        api.add_routes(
            integration=HttpUrlIntegration("LoginIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/login",
            methods=[apigwv2.HttpMethod.POST],
            authorizer=apigwv2.HttpNoneAuthorizer()
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: constructs.Construct,
    ) -> HttpRouteAuthorizerConfig:
        '''(experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        _ = HttpRouteAuthorizerBindOptions(route=route, scope=scope)

        return typing.cast(HttpRouteAuthorizerConfig, jsii.invoke(self, "bind", [_]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageAttributes",
    jsii_struct_bases=[StageAttributes],
    name_mapping={"stage_name": "stageName", "api": "api"},
)
class HttpStageAttributes(StageAttributes):
    def __init__(self, *, stage_name: builtins.str, api: IHttpApi) -> None:
        '''(experimental) The attributes used to import existing HttpStage.

        :param stage_name: (experimental) The name of the stage.
        :param api: (experimental) The API to which this stage is associated.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            
            # http_api: apigatewayv2.HttpApi
            
            http_stage_attributes = apigatewayv2.HttpStageAttributes(
                api=http_api,
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpStageAttributes.__init__)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
            "api": api,
        }

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api(self) -> IHttpApi:
        '''(experimental) The API to which this stage is associated.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IHttpApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpStageAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageOptions",
    jsii_struct_bases=[StageOptions],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "domain_mapping": "domainMapping",
        "throttle": "throttle",
        "stage_name": "stageName",
    },
)
class HttpStageOptions(StageOptions):
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The options to create a new Stage for an HTTP API.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: apigwv2.HttpApi
            # dn: apigwv2.DomainName
            
            
            api.add_stage("beta",
                stage_name="beta",
                auto_deploy=True,
                # https://${dn.domainName}/bar goes to the beta stage
                domain_mapping=apigwv2.DomainMappingOptions(
                    domain_name=dn,
                    mapping_key="bar"
                )
            )
        '''
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        if isinstance(throttle, dict):
            throttle = ThrottleSettings(**throttle)
        if __debug__:
            type_hints = typing.get_type_hints(HttpStageOptions.__init__)
            check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
            check_type(argname="argument domain_mapping", value=domain_mapping, expected_type=type_hints["domain_mapping"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping
        if throttle is not None:
            self._values["throttle"] = throttle
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        '''(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        '''
        result = self._values.get("domain_mapping")
        return typing.cast(typing.Optional[DomainMappingOptions], result)

    @builtins.property
    def throttle(self) -> typing.Optional[ThrottleSettings]:
        '''(experimental) Throttle settings for the routes of this stage.

        :default: - no throttling configuration

        :stability: experimental
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[ThrottleSettings], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the stage.

        See ``StageName`` class for more details.

        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageProps",
    jsii_struct_bases=[HttpStageOptions],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "domain_mapping": "domainMapping",
        "throttle": "throttle",
        "stage_name": "stageName",
        "http_api": "httpApi",
    },
)
class HttpStageProps(HttpStageOptions):
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        http_api: IHttpApi,
    ) -> None:
        '''(experimental) Properties to initialize an instance of ``HttpStage``.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param http_api: (experimental) The HTTP API to which this stage is associated.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: apigwv2.HttpApi
            
            
            apigwv2.HttpStage(self, "Stage",
                http_api=api,
                stage_name="beta"
            )
        '''
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        if isinstance(throttle, dict):
            throttle = ThrottleSettings(**throttle)
        if __debug__:
            type_hints = typing.get_type_hints(HttpStageProps.__init__)
            check_type(argname="argument auto_deploy", value=auto_deploy, expected_type=type_hints["auto_deploy"])
            check_type(argname="argument domain_mapping", value=domain_mapping, expected_type=type_hints["domain_mapping"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument http_api", value=http_api, expected_type=type_hints["http_api"])
        self._values: typing.Dict[str, typing.Any] = {
            "http_api": http_api,
        }
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping
        if throttle is not None:
            self._values["throttle"] = throttle
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        '''(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        '''
        result = self._values.get("domain_mapping")
        return typing.cast(typing.Optional[DomainMappingOptions], result)

    @builtins.property
    def throttle(self) -> typing.Optional[ThrottleSettings]:
        '''(experimental) Throttle settings for the routes of this stage.

        :default: - no throttling configuration

        :stability: experimental
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[ThrottleSettings], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the stage.

        See ``StageName`` class for more details.

        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API to which this stage is associated.

        :stability: experimental
        '''
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return typing.cast(IHttpApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpIntegration")
class IHttpIntegration(IIntegration, typing_extensions.Protocol):
    '''(experimental) Represents an Integration for an HTTP API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this integration.

        :stability: experimental
        '''
        ...


class _IHttpIntegrationProxy(
    jsii.proxy_for(IIntegration), # type: ignore[misc]
):
    '''(experimental) Represents an Integration for an HTTP API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpIntegration"

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this integration.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "httpApi"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpIntegration).__jsii_proxy_class__ = lambda : _IHttpIntegrationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRoute")
class IHttpRoute(IRoute, typing_extensions.Protocol):
    '''(experimental) Represents a Route for an HTTP API.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this route.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) Returns the arn of the route.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *,
        http_methods: typing.Optional[typing.Sequence[HttpMethod]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''(experimental) Grant access to invoke the route.

        This method requires that the authorizer of the route is undefined or is
        an ``HttpIamAuthorizer``.

        :param grantee: -
        :param http_methods: (experimental) The HTTP methods to allow. Default: - the HttpMethod of the route

        :stability: experimental
        '''
        ...


class _IHttpRouteProxy(
    jsii.proxy_for(IRoute), # type: ignore[misc]
):
    '''(experimental) Represents a Route for an HTTP API.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpRoute"

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this route.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "httpApi"))

    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) Returns the arn of the route.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeArn"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *,
        http_methods: typing.Optional[typing.Sequence[HttpMethod]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''(experimental) Grant access to invoke the route.

        This method requires that the authorizer of the route is undefined or is
        an ``HttpIamAuthorizer``.

        :param grantee: -
        :param http_methods: (experimental) The HTTP methods to allow. Default: - the HttpMethod of the route

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IHttpRoute.grant_invoke)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        options = GrantInvokeOptions(http_methods=http_methods)

        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantInvoke", [grantee, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpRoute).__jsii_proxy_class__ = lambda : _IHttpRouteProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpStage")
class IHttpStage(IStage, typing_extensions.Protocol):
    '''(experimental) Represents the HttpStage.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IHttpApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainUrl")
    def domain_url(self) -> builtins.str:
        '''(experimental) The custom domain URL to this stage.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...


class _IHttpStageProxy(
    jsii.proxy_for(IStage), # type: ignore[misc]
):
    '''(experimental) Represents the HttpStage.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpStage"

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IHttpApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "api"))

    @builtins.property
    @jsii.member(jsii_name="domainUrl")
    def domain_url(self) -> builtins.str:
        '''(experimental) The custom domain URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainUrl"))

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricClientError", [props]))

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricCount", [props]))

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataProcessed", [props]))

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIntegrationLatency", [props]))

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricLatency", [props]))

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricServerError", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpStage).__jsii_proxy_class__ = lambda : _IHttpStageProxy


@jsii.implements(IHttpIntegration)
class HttpIntegration(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegration",
):
    '''(experimental) The integration for an API route.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Integration
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # http_api: apigatewayv2.HttpApi
        # integration_credentials: apigatewayv2.IntegrationCredentials
        # parameter_mapping: apigatewayv2.ParameterMapping
        # payload_format_version: apigatewayv2.PayloadFormatVersion
        
        http_integration = apigatewayv2.HttpIntegration(self, "MyHttpIntegration",
            http_api=http_api,
            integration_type=apigatewayv2.HttpIntegrationType.HTTP_PROXY,
        
            # the properties below are optional
            connection_id="connectionId",
            connection_type=apigatewayv2.HttpConnectionType.VPC_LINK,
            credentials=integration_credentials,
            integration_subtype=apigatewayv2.HttpIntegrationSubtype.EVENTBRIDGE_PUT_EVENTS,
            integration_uri="integrationUri",
            method=apigatewayv2.HttpMethod.ANY,
            parameter_mapping=parameter_mapping,
            payload_format_version=payload_format_version,
            secure_server_name="secureServerName"
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        integration_type: HttpIntegrationType,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        credentials: typing.Optional[IntegrationCredentials] = None,
        integration_subtype: typing.Optional[HttpIntegrationSubtype] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        method: typing.Optional[HttpMethod] = None,
        parameter_mapping: typing.Optional[ParameterMapping] = None,
        payload_format_version: typing.Optional[PayloadFormatVersion] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param http_api: (experimental) The HTTP API to which this integration should be bound.
        :param integration_type: (experimental) Integration type.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param credentials: (experimental) The credentials with which to invoke the integration. Default: - no credentials, use resource-based permissions on supported AWS services
        :param integration_subtype: (experimental) Integration subtype. Used for AWS Service integrations, specifies the target of the integration. Default: - none, required if no ``integrationUri`` is defined.
        :param integration_uri: (experimental) Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.AWS_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``. Default: - none, required if no ``integrationSubtype`` is defined.
        :param method: (experimental) The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.AWS_PROXY`, irrelevant otherwise.
        :param secure_server_name: (experimental) Specifies the TLS configuration for a private integration. Default: undefined private integration traffic will use HTTP protocol

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpIntegration.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpIntegrationProps(
            http_api=http_api,
            integration_type=integration_type,
            connection_id=connection_id,
            connection_type=connection_type,
            credentials=credentials,
            integration_subtype=integration_subtype,
            integration_uri=integration_uri,
            method=method,
            parameter_mapping=parameter_mapping,
            payload_format_version=payload_format_version,
            secure_server_name=secure_server_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this integration.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "httpApi"))

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        '''(experimental) Id of the integration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationId"))


@jsii.implements(IHttpRoute)
class HttpRoute(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRoute",
):
    '''(experimental) Route class that creates the Route for API Gateway HTTP API.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Route
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2 as apigatewayv2
        
        # http_api: apigatewayv2.HttpApi
        # http_route_authorizer: apigatewayv2.IHttpRouteAuthorizer
        # http_route_integration: apigatewayv2.HttpRouteIntegration
        # http_route_key: apigatewayv2.HttpRouteKey
        
        http_route = apigatewayv2.HttpRoute(self, "MyHttpRoute",
            http_api=http_api,
            integration=http_route_integration,
            route_key=http_route_key,
        
            # the properties below are optional
            authorization_scopes=["authorizationScopes"],
            authorizer=http_route_authorizer
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        route_key: HttpRouteKey,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional[IHttpRouteAuthorizer] = None,
        integration: HttpRouteIntegration,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param http_api: (experimental) the API the route is associated with.
        :param route_key: (experimental) The key to this route. This is a combination of an HTTP method and an HTTP path.
        :param authorization_scopes: (experimental) The list of OIDC scopes to include in the authorization. These scopes will be merged with the scopes from the attached authorizer Default: - no additional authorization scopes
        :param authorizer: (experimental) Authorizer for a WebSocket API or an HTTP API. Default: - No authorizer
        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRoute.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpRouteProps(
            http_api=http_api,
            route_key=route_key,
            authorization_scopes=authorization_scopes,
            authorizer=authorizer,
            integration=integration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *,
        http_methods: typing.Optional[typing.Sequence[HttpMethod]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''(experimental) Grant access to invoke the route.

        This method requires that the authorizer of the route is undefined or is
        an ``HttpIamAuthorizer``.

        :param grantee: -
        :param http_methods: (experimental) The HTTP methods to allow. Default: - the HttpMethod of the route

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpRoute.grant_invoke)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        options = GrantInvokeOptions(http_methods=http_methods)

        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantInvoke", [grantee, options]))

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        '''(experimental) The HTTP API associated with this route.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "httpApi"))

    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) Returns the arn of the route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeArn"))

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        '''(experimental) Id of the Route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeId"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))


@jsii.implements(IHttpStage, IStage)
class HttpStage(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStage",
):
    '''(experimental) Represents a stage where an instance of the API is deployed.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Stage
    :exampleMetadata: infused

    Example::

        # api: apigwv2.HttpApi
        
        
        apigwv2.HttpStage(self, "Stage",
            http_api=api,
            stage_name="beta"
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        stage_name: typing.Optional[builtins.str] = None,
        auto_deploy: typing.Optional[builtins.bool] = None,
        domain_mapping: typing.Optional[typing.Union[DomainMappingOptions, typing.Dict[str, typing.Any]]] = None,
        throttle: typing.Optional[typing.Union[ThrottleSettings, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param http_api: (experimental) The HTTP API to which this stage is associated.
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param throttle: (experimental) Throttle settings for the routes of this stage. Default: - no throttling configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpStage.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpStageProps(
            http_api=http_api,
            stage_name=stage_name,
            auto_deploy=auto_deploy,
            domain_mapping=domain_mapping,
            throttle=throttle,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpStageAttributes")
    @builtins.classmethod
    def from_http_stage_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api: IHttpApi,
        stage_name: builtins.str,
    ) -> IHttpStage:
        '''(experimental) Import an existing stage into this CDK app.

        :param scope: -
        :param id: -
        :param api: (experimental) The API to which this stage is associated.
        :param stage_name: (experimental) The name of the stage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpStage.from_http_stage_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = HttpStageAttributes(api=api, stage_name=stage_name)

        return typing.cast(IHttpStage, jsii.sinvoke(cls, "fromHttpStageAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Return the given named metric for this HTTP Api Gateway Stage.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpStage.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricClientError", [props]))

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricCount", [props]))

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataProcessed", [props]))

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIntegrationLatency", [props]))

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricLatency", [props]))

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricServerError", [props]))

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> IHttpApi:
        '''(experimental) The API this stage is associated to.

        :stability: experimental
        '''
        return typing.cast(IHttpApi, jsii.get(self, "api"))

    @builtins.property
    @jsii.member(jsii_name="baseApi")
    def _base_api(self) -> IApi:
        '''
        :stability: experimental
        '''
        return typing.cast(IApi, jsii.get(self, "baseApi"))

    @builtins.property
    @jsii.member(jsii_name="domainUrl")
    def domain_url(self) -> builtins.str:
        '''(experimental) The custom domain URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainUrl"))

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''(experimental) The URL to this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))


__all__ = [
    "AddRoutesOptions",
    "ApiMapping",
    "ApiMappingAttributes",
    "ApiMappingProps",
    "AuthorizerPayloadVersion",
    "BatchHttpRouteOptions",
    "CfnApi",
    "CfnApiGatewayManagedOverrides",
    "CfnApiGatewayManagedOverridesProps",
    "CfnApiMapping",
    "CfnApiMappingProps",
    "CfnApiProps",
    "CfnAuthorizer",
    "CfnAuthorizerProps",
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnDomainName",
    "CfnDomainNameProps",
    "CfnIntegration",
    "CfnIntegrationProps",
    "CfnIntegrationResponse",
    "CfnIntegrationResponseProps",
    "CfnModel",
    "CfnModelProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnRouteResponse",
    "CfnRouteResponseProps",
    "CfnStage",
    "CfnStageProps",
    "CfnVpcLink",
    "CfnVpcLinkProps",
    "CorsHttpMethod",
    "CorsPreflightOptions",
    "DomainMappingOptions",
    "DomainName",
    "DomainNameAttributes",
    "DomainNameProps",
    "EndpointOptions",
    "EndpointType",
    "GrantInvokeOptions",
    "HttpApi",
    "HttpApiAttributes",
    "HttpApiProps",
    "HttpAuthorizer",
    "HttpAuthorizerAttributes",
    "HttpAuthorizerProps",
    "HttpAuthorizerType",
    "HttpConnectionType",
    "HttpIntegration",
    "HttpIntegrationProps",
    "HttpIntegrationSubtype",
    "HttpIntegrationType",
    "HttpMethod",
    "HttpNoneAuthorizer",
    "HttpRoute",
    "HttpRouteAuthorizerBindOptions",
    "HttpRouteAuthorizerConfig",
    "HttpRouteIntegration",
    "HttpRouteIntegrationBindOptions",
    "HttpRouteIntegrationConfig",
    "HttpRouteKey",
    "HttpRouteProps",
    "HttpStage",
    "HttpStageAttributes",
    "HttpStageOptions",
    "HttpStageProps",
    "IApi",
    "IApiMapping",
    "IAuthorizer",
    "IDomainName",
    "IHttpApi",
    "IHttpAuthorizer",
    "IHttpIntegration",
    "IHttpRoute",
    "IHttpRouteAuthorizer",
    "IHttpStage",
    "IIntegration",
    "IMappingValue",
    "IRoute",
    "IStage",
    "IVpcLink",
    "IWebSocketApi",
    "IWebSocketAuthorizer",
    "IWebSocketIntegration",
    "IWebSocketRoute",
    "IWebSocketRouteAuthorizer",
    "IWebSocketStage",
    "IntegrationCredentials",
    "MTLSConfig",
    "MappingValue",
    "ParameterMapping",
    "PayloadFormatVersion",
    "SecurityPolicy",
    "StageAttributes",
    "StageOptions",
    "ThrottleSettings",
    "VpcLink",
    "VpcLinkAttributes",
    "VpcLinkProps",
    "WebSocketApi",
    "WebSocketApiAttributes",
    "WebSocketApiKeySelectionExpression",
    "WebSocketApiProps",
    "WebSocketAuthorizer",
    "WebSocketAuthorizerAttributes",
    "WebSocketAuthorizerProps",
    "WebSocketAuthorizerType",
    "WebSocketIntegration",
    "WebSocketIntegrationProps",
    "WebSocketIntegrationType",
    "WebSocketNoneAuthorizer",
    "WebSocketRoute",
    "WebSocketRouteAuthorizerBindOptions",
    "WebSocketRouteAuthorizerConfig",
    "WebSocketRouteIntegration",
    "WebSocketRouteIntegrationBindOptions",
    "WebSocketRouteIntegrationConfig",
    "WebSocketRouteOptions",
    "WebSocketRouteProps",
    "WebSocketStage",
    "WebSocketStageAttributes",
    "WebSocketStageProps",
]

publication.publish()
