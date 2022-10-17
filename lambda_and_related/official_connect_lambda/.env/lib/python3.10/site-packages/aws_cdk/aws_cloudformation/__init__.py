'''
# AWS CloudFormation Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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

import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCustomResource(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResource",
):
    '''A CloudFormation ``AWS::CloudFormation::CustomResource``.

    In a CloudFormation template, you use the ``AWS::CloudFormation::CustomResource`` or ``Custom:: *String*`` resource type to specify custom resources.

    Custom resources provide a way for you to write custom provisioning logic in CloudFormation template and have CloudFormation run it during a stack operation, such as when you create, update or delete a stack. For more information, see `Custom resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html>`_ .
    .. epigraph::

       If you use the `VPC endpoints <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html>`_ feature, custom resources in the VPC must have access to CloudFormation -specific Amazon Simple Storage Service ( Amazon S3 ) buckets. Custom resources must send responses to a presigned Amazon S3 URL. If they can't send responses to Amazon S3 , CloudFormation won't receive a response and the stack operation fails. For more information, see `Setting up VPC endpoints for AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-vpce-bucketnames.html>`_ .

    :cloudformationResource: AWS::CloudFormation::CustomResource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_custom_resource = cloudformation.CfnCustomResource(self, "MyCfnCustomResource",
            service_token="serviceToken"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        service_token: builtins.str,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::CustomResource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_token: .. epigraph:: Only one property is defined by AWS for a custom resource: ``ServiceToken`` . All other properties are defined by the service provider. The service token that was given to the template developer by the service provider to access the service, such as an Amazon SNS topic ARN or Lambda function ARN. The service token must be from the same Region in which you are creating the stack. Updates aren't supported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnCustomResource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCustomResourceProps(service_token=service_token)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnCustomResource.inspect)
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
            type_hints = typing.get_type_hints(CfnCustomResource._render_properties)
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
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''.. epigraph::

   Only one property is defined by AWS for a custom resource: ``ServiceToken`` .

        All other properties are defined by the service provider.

        The service token that was given to the template developer by the service provider to access the service, such as an Amazon SNS topic ARN or Lambda function ARN. The service token must be from the same Region in which you are creating the stack.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnCustomResource, "service_token").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceToken", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={"service_token": "serviceToken"},
)
class CfnCustomResourceProps:
    def __init__(self, *, service_token: builtins.str) -> None:
        '''Properties for defining a ``CfnCustomResource``.

        :param service_token: .. epigraph:: Only one property is defined by AWS for a custom resource: ``ServiceToken`` . All other properties are defined by the service provider. The service token that was given to the template developer by the service provider to access the service, such as an Amazon SNS topic ARN or Lambda function ARN. The service token must be from the same Region in which you are creating the stack. Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_custom_resource_props = cloudformation.CfnCustomResourceProps(
                service_token="serviceToken"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnCustomResourceProps.__init__)
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[str, typing.Any] = {
            "service_token": service_token,
        }

    @builtins.property
    def service_token(self) -> builtins.str:
        '''.. epigraph::

   Only one property is defined by AWS for a custom resource: ``ServiceToken`` .

        All other properties are defined by the service provider.

        The service token that was given to the template developer by the service provider to access the service, such as an Amazon SNS topic ARN or Lambda function ARN. The service token must be from the same Region in which you are creating the stack.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        '''
        result = self._values.get("service_token")
        assert result is not None, "Required property 'service_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnHookDefaultVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookDefaultVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::HookDefaultVersion``.

    The ``HookDefaultVersion`` resource specifies the default version of the hook. The default version of the hook is used in CloudFormation operations for this AWS account and AWS Region .

    :cloudformationResource: AWS::CloudFormation::HookDefaultVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_hook_default_version = cloudformation.CfnHookDefaultVersion(self, "MyCfnHookDefaultVersion",
            type_name="typeName",
            type_version_arn="typeVersionArn",
            version_id="versionId"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::HookDefaultVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type_name: The name of the hook. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The version ID of the type configuration. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The version ID of the type specified. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookDefaultVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHookDefaultVersionProps(
            type_name=type_name,
            type_version_arn=type_version_arn,
            version_id=version_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookDefaultVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnHookDefaultVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the activated extension, in this account and Region.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the hook.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookDefaultVersion, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="typeVersionArn")
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type configuration.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typeversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionArn"))

    @type_version_arn.setter
    def type_version_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookDefaultVersion, "type_version_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type specified.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookDefaultVersion, "version_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookDefaultVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "type_name": "typeName",
        "type_version_arn": "typeVersionArn",
        "version_id": "versionId",
    },
)
class CfnHookDefaultVersionProps:
    def __init__(
        self,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnHookDefaultVersion``.

        :param type_name: The name of the hook. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The version ID of the type configuration. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The version ID of the type specified. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_hook_default_version_props = cloudformation.CfnHookDefaultVersionProps(
                type_name="typeName",
                type_version_arn="typeVersionArn",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookDefaultVersionProps.__init__)
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_version_arn", value=type_version_arn, expected_type=type_hints["type_version_arn"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[str, typing.Any] = {}
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_version_arn is not None:
            self._values["type_version_arn"] = type_version_arn
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the hook.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type configuration.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typeversionarn
        '''
        result = self._values.get("type_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type specified.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookDefaultVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnHookTypeConfig(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookTypeConfig",
):
    '''A CloudFormation ``AWS::CloudFormation::HookTypeConfig``.

    The ``HookTypeConfig`` resource specifies the configuration of a hook.

    :cloudformationResource: AWS::CloudFormation::HookTypeConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_hook_type_config = cloudformation.CfnHookTypeConfig(self, "MyCfnHookTypeConfig",
            configuration="configuration",
        
            # the properties below are optional
            configuration_alias="configurationAlias",
            type_arn="typeArn",
            type_name="typeName"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        configuration: builtins.str,
        configuration_alias: typing.Optional[builtins.str] = None,
        type_arn: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::HookTypeConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration: Specifies the activated hook type configuration, in this AWS account and AWS Region . You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .
        :param configuration_alias: Specifies the activated hook type configuration, in this AWS account and AWS Region . Defaults to ``default`` alias. Hook types currently support default configuration alias.
        :param type_arn: The Amazon Resource Number (ARN) for the hook to set ``Configuration`` for. You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .
        :param type_name: The unique name for your hook. Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` . You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookTypeConfig.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHookTypeConfigProps(
            configuration=configuration,
            configuration_alias=configuration_alias,
            type_arn=type_arn,
            type_name=type_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookTypeConfig.inspect)
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
            type_hints = typing.get_type_hints(CfnHookTypeConfig._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationArn")
    def attr_configuration_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the activated hook type configuration, in this account and Region.

        :cloudformationAttribute: ConfigurationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> builtins.str:
        '''Specifies the activated hook type configuration, in this AWS account and AWS Region .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configuration
        '''
        return typing.cast(builtins.str, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookTypeConfig, "configuration").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="configurationAlias")
    def configuration_alias(self) -> typing.Optional[builtins.str]:
        '''Specifies the activated hook type configuration, in this AWS account and AWS Region .

        Defaults to ``default`` alias. Hook types currently support default configuration alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configurationalias
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationAlias"))

    @configuration_alias.setter
    def configuration_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookTypeConfig, "configuration_alias").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationAlias", value)

    @builtins.property
    @jsii.member(jsii_name="typeArn")
    def type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) for the hook to set ``Configuration`` for.

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeArn"))

    @type_arn.setter
    def type_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookTypeConfig, "type_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeArn", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The unique name for your hook.

        Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookTypeConfig, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookTypeConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "configuration_alias": "configurationAlias",
        "type_arn": "typeArn",
        "type_name": "typeName",
    },
)
class CfnHookTypeConfigProps:
    def __init__(
        self,
        *,
        configuration: builtins.str,
        configuration_alias: typing.Optional[builtins.str] = None,
        type_arn: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnHookTypeConfig``.

        :param configuration: Specifies the activated hook type configuration, in this AWS account and AWS Region . You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .
        :param configuration_alias: Specifies the activated hook type configuration, in this AWS account and AWS Region . Defaults to ``default`` alias. Hook types currently support default configuration alias.
        :param type_arn: The Amazon Resource Number (ARN) for the hook to set ``Configuration`` for. You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .
        :param type_name: The unique name for your hook. Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` . You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_hook_type_config_props = cloudformation.CfnHookTypeConfigProps(
                configuration="configuration",
            
                # the properties below are optional
                configuration_alias="configurationAlias",
                type_arn="typeArn",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookTypeConfigProps.__init__)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument configuration_alias", value=configuration_alias, expected_type=type_hints["configuration_alias"])
            check_type(argname="argument type_arn", value=type_arn, expected_type=type_hints["type_arn"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "configuration": configuration,
        }
        if configuration_alias is not None:
            self._values["configuration_alias"] = configuration_alias
        if type_arn is not None:
            self._values["type_arn"] = type_arn
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def configuration(self) -> builtins.str:
        '''Specifies the activated hook type configuration, in this AWS account and AWS Region .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_alias(self) -> typing.Optional[builtins.str]:
        '''Specifies the activated hook type configuration, in this AWS account and AWS Region .

        Defaults to ``default`` alias. Hook types currently support default configuration alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configurationalias
        '''
        result = self._values.get("configuration_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) for the hook to set ``Configuration`` for.

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typearn
        '''
        result = self._values.get("type_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The unique name for your hook.

        Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeARN`` and ``Configuration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookTypeConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnHookVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::HookVersion``.

    The ``HookVersion`` resource publishes new or first hook version to the AWS CloudFormation registry.

    :cloudformationResource: AWS::CloudFormation::HookVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_hook_version = cloudformation.CfnHookVersion(self, "MyCfnHookVersion",
            schema_handler_package="schemaHandlerPackage",
            type_name="typeName",
        
            # the properties below are optional
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation.CfnHookVersion.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[typing.Union["CfnHookVersion.LoggingConfigProperty", typing.Dict[str, typing.Any]], aws_cdk.core.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::HookVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param schema_handler_package: A URL to the Amazon S3 bucket containing the hook project package that contains the necessary files for the hook you want to register. For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide for Extension Development* . .. epigraph:: The user registering the resource must be able to access the package in the S3 bucket. That's, the user must have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param type_name: The unique name for your hook. Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` . .. epigraph:: The following organization namespaces are reserved and can't be used in your hook type names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``ASK`` - ``AWS`` - ``Custom`` - ``Dev``
        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants the hook permission.
        :param logging_config: Contains logging configuration information for an extension.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHookVersionProps(
            schema_handler_package=schema_handler_package,
            type_name=type_name,
            execution_role_arn=execution_role_arn,
            logging_config=logging_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnHookVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the hook.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIsDefaultVersion")
    def attr_is_default_version(self) -> aws_cdk.core.IResolvable:
        '''Whether the specified hook version is set as the default version.

        :cloudformationAttribute: IsDefaultVersion
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrIsDefaultVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrTypeArn")
    def attr_type_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) assigned to this version of the hook.

        :cloudformationAttribute: TypeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTypeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''The ID of this version of the hook.

        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property
    @jsii.member(jsii_name="attrVisibility")
    def attr_visibility(self) -> builtins.str:
        '''The scope at which the resource is visible and usable in CloudFormation operations.

        Valid values include:

        - ``PRIVATE`` : The resource is only visible and usable within the account in which it's registered. CloudFormation marks any resources you register as ``PRIVATE`` .
        - ``PUBLIC`` : The resource is publicly visible and usable within any Amazon account.

        :cloudformationAttribute: Visibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVisibility"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="schemaHandlerPackage")
    def schema_handler_package(self) -> builtins.str:
        '''A URL to the Amazon S3 bucket containing the hook project package that contains the necessary files for the hook you want to register.

        For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide for Extension Development* .
        .. epigraph::

           The user registering the resource must be able to access the package in the S3 bucket. That's, the user must have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-schemahandlerpackage
        '''
        return typing.cast(builtins.str, jsii.get(self, "schemaHandlerPackage"))

    @schema_handler_package.setter
    def schema_handler_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookVersion, "schema_handler_package").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaHandlerPackage", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        '''The unique name for your hook.

        Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your hook type names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``ASK``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-typename
        '''
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookVersion, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the task execution role that grants the hook permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-executionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookVersion, "execution_role_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union["CfnHookVersion.LoggingConfigProperty", aws_cdk.core.IResolvable]]:
        '''Contains logging configuration information for an extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-loggingconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHookVersion.LoggingConfigProperty", aws_cdk.core.IResolvable]], jsii.get(self, "loggingConfig"))

    @logging_config.setter
    def logging_config(
        self,
        value: typing.Optional[typing.Union["CfnHookVersion.LoggingConfigProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnHookVersion, "logging_config").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnHookVersion.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LoggingConfig`` property type specifies logging configuration information for an extension.

            :param log_group_name: The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.
            :param log_role_arn: The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                logging_config_property = cloudformation.CfnHookVersion.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnHookVersion.LoggingConfigProperty.__init__)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html#cfn-cloudformation-hookversion-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html#cfn-cloudformation-hookversion-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnHookVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_handler_package": "schemaHandlerPackage",
        "type_name": "typeName",
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
    },
)
class CfnHookVersionProps:
    def __init__(
        self,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[typing.Union[CfnHookVersion.LoggingConfigProperty, typing.Dict[str, typing.Any]], aws_cdk.core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHookVersion``.

        :param schema_handler_package: A URL to the Amazon S3 bucket containing the hook project package that contains the necessary files for the hook you want to register. For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide for Extension Development* . .. epigraph:: The user registering the resource must be able to access the package in the S3 bucket. That's, the user must have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param type_name: The unique name for your hook. Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` . .. epigraph:: The following organization namespaces are reserved and can't be used in your hook type names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``ASK`` - ``AWS`` - ``Custom`` - ``Dev``
        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants the hook permission.
        :param logging_config: Contains logging configuration information for an extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_hook_version_props = cloudformation.CfnHookVersionProps(
                schema_handler_package="schemaHandlerPackage",
                type_name="typeName",
            
                # the properties below are optional
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation.CfnHookVersion.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnHookVersionProps.__init__)
            check_type(argname="argument schema_handler_package", value=schema_handler_package, expected_type=type_hints["schema_handler_package"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "schema_handler_package": schema_handler_package,
            "type_name": type_name,
        }
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def schema_handler_package(self) -> builtins.str:
        '''A URL to the Amazon S3 bucket containing the hook project package that contains the necessary files for the hook you want to register.

        For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide for Extension Development* .
        .. epigraph::

           The user registering the resource must be able to access the package in the S3 bucket. That's, the user must have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-schemahandlerpackage
        '''
        result = self._values.get("schema_handler_package")
        assert result is not None, "Required property 'schema_handler_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''The unique name for your hook.

        Specifies a three-part namespace for your hook, with a recommended pattern of ``Organization::Service::Hook`` .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your hook type names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``ASK``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-typename
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the task execution role that grants the hook permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[CfnHookVersion.LoggingConfigProperty, aws_cdk.core.IResolvable]]:
        '''Contains logging configuration information for an extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[CfnHookVersion.LoggingConfigProperty, aws_cdk.core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMacro(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnMacro",
):
    '''A CloudFormation ``AWS::CloudFormation::Macro``.

    The ``AWS::CloudFormation::Macro`` resource is a CloudFormation resource type that creates a CloudFormation macro to perform custom processing on CloudFormation templates. For more information, see `Using AWS CloudFormation macros to perform custom processing on templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html>`_ .

    :cloudformationResource: AWS::CloudFormation::Macro
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_macro = cloudformation.CfnMacro(self, "MyCfnMacro",
            function_name="functionName",
            name="name",
        
            # the properties below are optional
            description="description",
            log_group_name="logGroupName",
            log_role_arn="logRoleArn"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::Macro``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: The Amazon Resource Name (ARN) of the underlying AWS Lambda function that you want AWS CloudFormation to invoke when the macro is run.
        :param name: The name of the macro. The name of the macro must be unique across all macros in the account.
        :param description: A description of the macro.
        :param log_group_name: The CloudWatch Logs group to which AWS CloudFormation sends error logging information when invoking the macro's underlying AWS Lambda function.
        :param log_role_arn: The ARN of the role AWS CloudFormation should assume when sending log entries to CloudWatch Logs .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnMacro.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMacroProps(
            function_name=function_name,
            name=name,
            description=description,
            log_group_name=log_group_name,
            log_role_arn=log_role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnMacro.inspect)
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
            type_hints = typing.get_type_hints(CfnMacro._render_properties)
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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the underlying AWS Lambda function that you want AWS CloudFormation to invoke when the macro is run.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnMacro, "function_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the macro.

        The name of the macro must be unique across all macros in the account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnMacro, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the macro.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnMacro, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The CloudWatch Logs group to which AWS CloudFormation sends error logging information when invoking the macro's underlying AWS Lambda function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnMacro, "log_group_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logRoleArn")
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role AWS CloudFormation should assume when sending log entries to CloudWatch Logs .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logRoleArn"))

    @log_role_arn.setter
    def log_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnMacro, "log_role_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logRoleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnMacroProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "name": "name",
        "description": "description",
        "log_group_name": "logGroupName",
        "log_role_arn": "logRoleArn",
    },
)
class CfnMacroProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMacro``.

        :param function_name: The Amazon Resource Name (ARN) of the underlying AWS Lambda function that you want AWS CloudFormation to invoke when the macro is run.
        :param name: The name of the macro. The name of the macro must be unique across all macros in the account.
        :param description: A description of the macro.
        :param log_group_name: The CloudWatch Logs group to which AWS CloudFormation sends error logging information when invoking the macro's underlying AWS Lambda function.
        :param log_role_arn: The ARN of the role AWS CloudFormation should assume when sending log entries to CloudWatch Logs .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_macro_props = cloudformation.CfnMacroProps(
                function_name="functionName",
                name="name",
            
                # the properties below are optional
                description="description",
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnMacroProps.__init__)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
        self._values: typing.Dict[str, typing.Any] = {
            "function_name": function_name,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_role_arn is not None:
            self._values["log_role_arn"] = log_role_arn

    @builtins.property
    def function_name(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the underlying AWS Lambda function that you want AWS CloudFormation to invoke when the macro is run.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the macro.

        The name of the macro must be unique across all macros in the account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the macro.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The CloudWatch Logs group to which AWS CloudFormation sends error logging information when invoking the macro's underlying AWS Lambda function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role AWS CloudFormation should assume when sending log entries to CloudWatch Logs .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        '''
        result = self._values.get("log_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMacroProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModuleDefaultVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnModuleDefaultVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ModuleDefaultVersion``.

    Specifies the default version of a module. The default version of the module will be used in CloudFormation operations for this account and Region.

    To register a module version, use the ``[AWS::CloudFormation::ModuleVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html)`` resource.

    For more information using modules, see `Using modules to encapsulate and reuse resource configurations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/modules.html>`_ and `Registering extensions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html#registry-register>`_ in the *CloudFormation User Guide* . For information on developing modules, see `Developing modules <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/modules.html>`_ in the *CloudFormation CLI User Guide* .

    :cloudformationResource: AWS::CloudFormation::ModuleDefaultVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_module_default_version = cloudformation.CfnModuleDefaultVersion(self, "MyCfnModuleDefaultVersion",
            arn="arn",
            module_name="moduleName",
            version_id="versionId"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        arn: typing.Optional[builtins.str] = None,
        module_name: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ModuleDefaultVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param arn: The Amazon Resource Name (ARN) of the module version to set as the default version. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param module_name: The name of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param version_id: The ID for the specific version of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleDefaultVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnModuleDefaultVersionProps(
            arn=arn, module_name=module_name, version_id=version_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleDefaultVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnModuleDefaultVersion._render_properties)
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
    @jsii.member(jsii_name="arn")
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the module version to set as the default version.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-arn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModuleDefaultVersion, "arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value)

    @builtins.property
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> typing.Optional[builtins.str]:
        '''The name of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-modulename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModuleDefaultVersion, "module_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleName", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the specific version of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModuleDefaultVersion, "version_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnModuleDefaultVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "module_name": "moduleName",
        "version_id": "versionId",
    },
)
class CfnModuleDefaultVersionProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        module_name: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnModuleDefaultVersion``.

        :param arn: The Amazon Resource Name (ARN) of the module version to set as the default version. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param module_name: The name of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param version_id: The ID for the specific version of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_module_default_version_props = cloudformation.CfnModuleDefaultVersionProps(
                arn="arn",
                module_name="moduleName",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleDefaultVersionProps.__init__)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if module_name is not None:
            self._values["module_name"] = module_name
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the module version to set as the default version.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_name(self) -> typing.Optional[builtins.str]:
        '''The name of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-modulename
        '''
        result = self._values.get("module_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the specific version of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleDefaultVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModuleVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnModuleVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ModuleVersion``.

    Registers the specified version of the module with the CloudFormation service. Registering a module makes it available for use in CloudFormation templates in your AWS account and Region.

    To specify a module version as the default version, use the ``[AWS::CloudFormation::ModuleDefaultVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html)`` resource.

    For more information using modules, see `Using modules to encapsulate and reuse resource configurations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/modules.html>`_ and `Registering extensions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html#registry-register>`_ in the *CloudFormation User Guide* . For information on developing modules, see `Developing modules <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/modules.html>`_ in the *CloudFormation CLI User Guide* .

    :cloudformationResource: AWS::CloudFormation::ModuleVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_module_version = cloudformation.CfnModuleVersion(self, "MyCfnModuleVersion",
            module_name="moduleName",
            module_package="modulePackage"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        module_name: builtins.str,
        module_package: builtins.str,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ModuleVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param module_name: The name of the module being registered.
        :param module_package: A URL to the S3 bucket containing the package that contains the template fragment and schema files for the module version to register. .. epigraph:: The user registering the module version must be able to access the module package in the S3 bucket. That's, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnModuleVersionProps(
            module_name=module_name, module_package=module_package
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnModuleVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the module.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''The description of the module.

        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrDocumentationUrl")
    def attr_documentation_url(self) -> builtins.str:
        '''The URL of a page providing detailed documentation for this module.

        :cloudformationAttribute: DocumentationUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDocumentationUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrIsDefaultVersion")
    def attr_is_default_version(self) -> aws_cdk.core.IResolvable:
        '''Whether the specified module version is set as the default version.

        :cloudformationAttribute: IsDefaultVersion
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrIsDefaultVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrSchema")
    def attr_schema(self) -> builtins.str:
        '''The schema that defines the module.

        :cloudformationAttribute: Schema
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchema"))

    @builtins.property
    @jsii.member(jsii_name="attrTimeCreated")
    def attr_time_created(self) -> builtins.str:
        '''When the specified module version was registered.

        :cloudformationAttribute: TimeCreated
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTimeCreated"))

    @builtins.property
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''The ID of this version of the module.

        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property
    @jsii.member(jsii_name="attrVisibility")
    def attr_visibility(self) -> builtins.str:
        '''The scope at which the module is visible and usable in CloudFormation operations.

        Valid values include:

        - ``PRIVATE`` : The module is only visible and usable within the account in which it's registered.
        - ``PUBLIC`` : The module is publicly visible and usable within any Amazon account.

        :cloudformationAttribute: Visibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVisibility"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> builtins.str:
        '''The name of the module being registered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulename
        '''
        return typing.cast(builtins.str, jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModuleVersion, "module_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleName", value)

    @builtins.property
    @jsii.member(jsii_name="modulePackage")
    def module_package(self) -> builtins.str:
        '''A URL to the S3 bucket containing the package that contains the template fragment and schema files for the module version to register.

        .. epigraph::

           The user registering the module version must be able to access the module package in the S3 bucket. That's, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulepackage
        '''
        return typing.cast(builtins.str, jsii.get(self, "modulePackage"))

    @module_package.setter
    def module_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnModuleVersion, "module_package").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modulePackage", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnModuleVersionProps",
    jsii_struct_bases=[],
    name_mapping={"module_name": "moduleName", "module_package": "modulePackage"},
)
class CfnModuleVersionProps:
    def __init__(
        self,
        *,
        module_name: builtins.str,
        module_package: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnModuleVersion``.

        :param module_name: The name of the module being registered.
        :param module_package: A URL to the S3 bucket containing the package that contains the template fragment and schema files for the module version to register. .. epigraph:: The user registering the module version must be able to access the module package in the S3 bucket. That's, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_module_version_props = cloudformation.CfnModuleVersionProps(
                module_name="moduleName",
                module_package="modulePackage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnModuleVersionProps.__init__)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument module_package", value=module_package, expected_type=type_hints["module_package"])
        self._values: typing.Dict[str, typing.Any] = {
            "module_name": module_name,
            "module_package": module_package,
        }

    @builtins.property
    def module_name(self) -> builtins.str:
        '''The name of the module being registered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulename
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def module_package(self) -> builtins.str:
        '''A URL to the S3 bucket containing the package that contains the template fragment and schema files for the module version to register.

        .. epigraph::

           The user registering the module version must be able to access the module package in the S3 bucket. That's, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulepackage
        '''
        result = self._values.get("module_package")
        assert result is not None, "Required property 'module_package' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPublicTypeVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnPublicTypeVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::PublicTypeVersion``.

    Tests and publishes a registered extension as a public, third-party extension.

    CloudFormation first tests the extension to make sure it meets all necessary requirements for being published in the CloudFormation registry. If it does, CloudFormation then publishes it to the registry as a public third-party extension in this Region. Public extensions are available for use by all CloudFormation users.

    - For resource types, testing includes passing all contracts tests defined for the type.
    - For modules, testing includes determining if the module's model meets all necessary requirements.

    For more information, see `Testing your public extension prior to publishing <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-testing>`_ in the *CloudFormation CLI User Guide* .

    If you don't specify a version, CloudFormation uses the default version of the extension in your account and Region for testing.

    To perform testing, CloudFormation assumes the execution role specified when the type was registered.

    An extension must have a test status of ``PASSED`` before it can be published. For more information, see `Publishing extensions to make them available for public use <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-publish.html>`_ in the *CloudFormation CLI User Guide* .

    :cloudformationResource: AWS::CloudFormation::PublicTypeVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_public_type_version = cloudformation.CfnPublicTypeVersion(self, "MyCfnPublicTypeVersion",
            arn="arn",
            log_delivery_bucket="logDeliveryBucket",
            public_version_number="publicVersionNumber",
            type="type",
            type_name="typeName"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        arn: typing.Optional[builtins.str] = None,
        log_delivery_bucket: typing.Optional[builtins.str] = None,
        public_version_number: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::PublicTypeVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param arn: The Amazon Resource Number (ARN) of the extension. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param log_delivery_bucket: The S3 bucket to which CloudFormation delivers the contract test execution logs. CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` . The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions: - GetObject - PutObject For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param public_version_number: The version number to assign to this version of the extension. Use the following format, and adhere to semantic versioning when assigning a version number to your extension: ``MAJOR.MINOR.PATCH`` For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ . If you don't specify a version number, CloudFormation increments the version number by one minor version release. You cannot specify a version number the first time you publish a type. AWS CloudFormation automatically sets the first version number to be ``1.0.0`` .
        :param type: The type of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param type_name: The name of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublicTypeVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPublicTypeVersionProps(
            arn=arn,
            log_delivery_bucket=log_delivery_bucket,
            public_version_number=public_version_number,
            type=type,
            type_name=type_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublicTypeVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnPublicTypeVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPublicTypeArn")
    def attr_public_type_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) assigned to the public extension upon publication.

        :cloudformationAttribute: PublicTypeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPublicTypeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPublisherId")
    def attr_publisher_id(self) -> builtins.str:
        '''The publisher ID of the extension publisher.

        :cloudformationAttribute: PublisherId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPublisherId"))

    @builtins.property
    @jsii.member(jsii_name="attrTypeVersionArn")
    def attr_type_version_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) assigned to this version of the extension.

        :cloudformationAttribute: TypeVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTypeVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the extension.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-arn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublicTypeVersion, "arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value)

    @builtins.property
    @jsii.member(jsii_name="logDeliveryBucket")
    def log_delivery_bucket(self) -> typing.Optional[builtins.str]:
        '''The S3 bucket to which CloudFormation delivers the contract test execution logs.

        CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` .

        The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions:

        - GetObject
        - PutObject

        For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-logdeliverybucket
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logDeliveryBucket"))

    @log_delivery_bucket.setter
    def log_delivery_bucket(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublicTypeVersion, "log_delivery_bucket").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDeliveryBucket", value)

    @builtins.property
    @jsii.member(jsii_name="publicVersionNumber")
    def public_version_number(self) -> typing.Optional[builtins.str]:
        '''The version number to assign to this version of the extension.

        Use the following format, and adhere to semantic versioning when assigning a version number to your extension:

        ``MAJOR.MINOR.PATCH``

        For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ .

        If you don't specify a version number, CloudFormation increments the version number by one minor version release.

        You cannot specify a version number the first time you publish a type. AWS CloudFormation automatically sets the first version number to be ``1.0.0`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-publicversionnumber
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicVersionNumber"))

    @public_version_number.setter
    def public_version_number(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublicTypeVersion, "public_version_number").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublicTypeVersion, "type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublicTypeVersion, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnPublicTypeVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "log_delivery_bucket": "logDeliveryBucket",
        "public_version_number": "publicVersionNumber",
        "type": "type",
        "type_name": "typeName",
    },
)
class CfnPublicTypeVersionProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        log_delivery_bucket: typing.Optional[builtins.str] = None,
        public_version_number: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPublicTypeVersion``.

        :param arn: The Amazon Resource Number (ARN) of the extension. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param log_delivery_bucket: The S3 bucket to which CloudFormation delivers the contract test execution logs. CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` . The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions: - GetObject - PutObject For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param public_version_number: The version number to assign to this version of the extension. Use the following format, and adhere to semantic versioning when assigning a version number to your extension: ``MAJOR.MINOR.PATCH`` For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ . If you don't specify a version number, CloudFormation increments the version number by one minor version release. You cannot specify a version number the first time you publish a type. AWS CloudFormation automatically sets the first version number to be ``1.0.0`` .
        :param type: The type of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param type_name: The name of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_public_type_version_props = cloudformation.CfnPublicTypeVersionProps(
                arn="arn",
                log_delivery_bucket="logDeliveryBucket",
                public_version_number="publicVersionNumber",
                type="type",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublicTypeVersionProps.__init__)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument log_delivery_bucket", value=log_delivery_bucket, expected_type=type_hints["log_delivery_bucket"])
            check_type(argname="argument public_version_number", value=public_version_number, expected_type=type_hints["public_version_number"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if log_delivery_bucket is not None:
            self._values["log_delivery_bucket"] = log_delivery_bucket
        if public_version_number is not None:
            self._values["public_version_number"] = public_version_number
        if type is not None:
            self._values["type"] = type
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the extension.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_bucket(self) -> typing.Optional[builtins.str]:
        '''The S3 bucket to which CloudFormation delivers the contract test execution logs.

        CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` .

        The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions:

        - GetObject
        - PutObject

        For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-logdeliverybucket
        '''
        result = self._values.get("log_delivery_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_version_number(self) -> typing.Optional[builtins.str]:
        '''The version number to assign to this version of the extension.

        Use the following format, and adhere to semantic versioning when assigning a version number to your extension:

        ``MAJOR.MINOR.PATCH``

        For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ .

        If you don't specify a version number, CloudFormation increments the version number by one minor version release.

        You cannot specify a version number the first time you publish a type. AWS CloudFormation automatically sets the first version number to be ``1.0.0`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-publicversionnumber
        '''
        result = self._values.get("public_version_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicTypeVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPublisher(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnPublisher",
):
    '''A CloudFormation ``AWS::CloudFormation::Publisher``.

    Registers your account as a publisher of public extensions in the CloudFormation registry. Public extensions are available for use by all CloudFormation users.

    For information on requirements for registering as a public extension publisher, see `Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *CloudFormation CLI User Guide* .

    :cloudformationResource: AWS::CloudFormation::Publisher
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_publisher = cloudformation.CfnPublisher(self, "MyCfnPublisher",
            accept_terms_and_conditions=False,
        
            # the properties below are optional
            connection_arn="connectionArn"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        accept_terms_and_conditions: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::Publisher``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accept_terms_and_conditions: Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry. The default is ``false`` .
        :param connection_arn: If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account. For more information, see `Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *CloudFormation CLI User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublisher.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPublisherProps(
            accept_terms_and_conditions=accept_terms_and_conditions,
            connection_arn=connection_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublisher.inspect)
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
            type_hints = typing.get_type_hints(CfnPublisher._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrIdentityProvider")
    def attr_identity_provider(self) -> builtins.str:
        '''The type of account used as the identity provider when registering this publisher with CloudFormation .

        Values include: ``AWS_Marketplace`` | ``Bitbucket`` | ``GitHub`` .

        :cloudformationAttribute: IdentityProvider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIdentityProvider"))

    @builtins.property
    @jsii.member(jsii_name="attrPublisherId")
    def attr_publisher_id(self) -> builtins.str:
        '''The ID of the extension publisher.

        This publisher ID applies to your account in all AWS Regions .

        :cloudformationAttribute: PublisherId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPublisherId"))

    @builtins.property
    @jsii.member(jsii_name="attrPublisherProfile")
    def attr_publisher_profile(self) -> builtins.str:
        '''The URL to the publisher's profile with the identity provider.

        :cloudformationAttribute: PublisherProfile
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPublisherProfile"))

    @builtins.property
    @jsii.member(jsii_name="attrPublisherStatus")
    def attr_publisher_status(self) -> builtins.str:
        '''Whether the publisher is verified.

        :cloudformationAttribute: PublisherStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPublisherStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="acceptTermsAndConditions")
    def accept_terms_and_conditions(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        '''Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry.

        The default is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-accepttermsandconditions
        '''
        return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], jsii.get(self, "acceptTermsAndConditions"))

    @accept_terms_and_conditions.setter
    def accept_terms_and_conditions(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublisher, "accept_terms_and_conditions").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptTermsAndConditions", value)

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account.

        For more information, see `Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *CloudFormation CLI User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-connectionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionArn"))

    @connection_arn.setter
    def connection_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnPublisher, "connection_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnPublisherProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_terms_and_conditions": "acceptTermsAndConditions",
        "connection_arn": "connectionArn",
    },
)
class CfnPublisherProps:
    def __init__(
        self,
        *,
        accept_terms_and_conditions: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPublisher``.

        :param accept_terms_and_conditions: Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry. The default is ``false`` .
        :param connection_arn: If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account. For more information, see `Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *CloudFormation CLI User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_publisher_props = cloudformation.CfnPublisherProps(
                accept_terms_and_conditions=False,
            
                # the properties below are optional
                connection_arn="connectionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnPublisherProps.__init__)
            check_type(argname="argument accept_terms_and_conditions", value=accept_terms_and_conditions, expected_type=type_hints["accept_terms_and_conditions"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
        self._values: typing.Dict[str, typing.Any] = {
            "accept_terms_and_conditions": accept_terms_and_conditions,
        }
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn

    @builtins.property
    def accept_terms_and_conditions(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        '''Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry.

        The default is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-accepttermsandconditions
        '''
        result = self._values.get("accept_terms_and_conditions")
        assert result is not None, "Required property 'accept_terms_and_conditions' is missing"
        return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account.

        For more information, see `Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *CloudFormation CLI User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublisherProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourceDefaultVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnResourceDefaultVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ResourceDefaultVersion``.

    Specifies the default version of a resource. The default version of a resource will be used in CloudFormation operations.

    :cloudformationResource: AWS::CloudFormation::ResourceDefaultVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_resource_default_version = cloudformation.CfnResourceDefaultVersion(self, "MyCfnResourceDefaultVersion",
            type_name="typeName",
            type_version_arn="typeVersionArn",
            version_id="versionId"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ResourceDefaultVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type_name: The name of the resource. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The Amazon Resource Name (ARN) of the resource version. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The ID of a specific version of the resource. The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceDefaultVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceDefaultVersionProps(
            type_name=type_name,
            type_version_arn=type_version_arn,
            version_id=version_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceDefaultVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnResourceDefaultVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceDefaultVersion, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="typeVersionArn")
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource version.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typeversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionArn"))

    @type_version_arn.setter
    def type_version_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceDefaultVersion, "type_version_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a specific version of the resource.

        The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceDefaultVersion, "version_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnResourceDefaultVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "type_name": "typeName",
        "type_version_arn": "typeVersionArn",
        "version_id": "versionId",
    },
)
class CfnResourceDefaultVersionProps:
    def __init__(
        self,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceDefaultVersion``.

        :param type_name: The name of the resource. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The Amazon Resource Name (ARN) of the resource version. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The ID of a specific version of the resource. The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_resource_default_version_props = cloudformation.CfnResourceDefaultVersionProps(
                type_name="typeName",
                type_version_arn="typeVersionArn",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceDefaultVersionProps.__init__)
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_version_arn", value=type_version_arn, expected_type=type_hints["type_version_arn"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[str, typing.Any] = {}
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_version_arn is not None:
            self._values["type_version_arn"] = type_version_arn
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource version.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typeversionarn
        '''
        result = self._values.get("type_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a specific version of the resource.

        The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefaultVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourceVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnResourceVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ResourceVersion``.

    Registers a resource version with the CloudFormation service. Registering a resource version makes it available for use in CloudFormation templates in your AWS account , and includes:

    - Validating the resource schema.
    - Determining which handlers, if any, have been specified for the resource.
    - Making the resource available for use in your account.

    For more information on how to develop resources and ready them for registration, see `Creating Resource Providers <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-types.html>`_ in the *CloudFormation CLI User Guide* .

    You can have a maximum of 50 resource versions registered at a time. This maximum is per account and per Region.

    :cloudformationResource: AWS::CloudFormation::ResourceVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_resource_version = cloudformation.CfnResourceVersion(self, "MyCfnResourceVersion",
            schema_handler_package="schemaHandlerPackage",
            type_name="typeName",
        
            # the properties below are optional
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation.CfnResourceVersion.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnResourceVersion.LoggingConfigProperty", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ResourceVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param schema_handler_package: A URL to the S3 bucket containing the resource project package that contains the necessary files for the resource you want to register. For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide* . .. epigraph:: The user registering the resource must be able to access the package in the S3 bucket. That is, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param type_name: The name of the resource being registered. We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* . .. epigraph:: The following organization namespaces are reserved and can't be used in your resource names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``AWS`` - ``Custom`` - ``Dev``
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource. If your resource calls AWS APIs in any of its handlers, you must create an *`IAM execution role <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_* that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.
        :param logging_config: Logging configuration information for a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceVersion.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceVersionProps(
            schema_handler_package=schema_handler_package,
            type_name=type_name,
            execution_role_arn=execution_role_arn,
            logging_config=logging_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceVersion.inspect)
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
            type_hints = typing.get_type_hints(CfnResourceVersion._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource version.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIsDefaultVersion")
    def attr_is_default_version(self) -> aws_cdk.core.IResolvable:
        '''Whether the resource version is set as the default version.

        :cloudformationAttribute: IsDefaultVersion
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrIsDefaultVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrProvisioningType")
    def attr_provisioning_type(self) -> builtins.str:
        '''The provisioning behavior of the resource type.

        CloudFormation determines the provisioning type during registration, based on the types of handlers in the schema handler package submitted.

        Valid values include:

        - ``FULLY_MUTABLE`` : The resource type includes an update handler to process updates to the type during stack update operations.
        - ``IMMUTABLE`` : The resource type doesn't include an update handler, so the type can't be updated and must instead be replaced during stack update operations.
        - ``NON_PROVISIONABLE`` : The resource type doesn't include all the following handlers, and therefore can't actually be provisioned.
        - create
        - read
        - delete

        :cloudformationAttribute: ProvisioningType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProvisioningType"))

    @builtins.property
    @jsii.member(jsii_name="attrTypeArn")
    def attr_type_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource.

        :cloudformationAttribute: TypeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTypeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''The ID of a specific version of the resource.

        The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it is registered.

        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property
    @jsii.member(jsii_name="attrVisibility")
    def attr_visibility(self) -> builtins.str:
        '''The scope at which the resource is visible and usable in CloudFormation operations.

        Valid values include:

        - ``PRIVATE`` : The resource is only visible and usable within the account in which it's registered. CloudFormation marks any resources you register as ``PRIVATE`` .
        - ``PUBLIC`` : The resource is publicly visible and usable within any Amazon account.

        :cloudformationAttribute: Visibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVisibility"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="schemaHandlerPackage")
    def schema_handler_package(self) -> builtins.str:
        '''A URL to the S3 bucket containing the resource project package that contains the necessary files for the resource you want to register.

        For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide* .
        .. epigraph::

           The user registering the resource must be able to access the package in the S3 bucket. That is, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-schemahandlerpackage
        '''
        return typing.cast(builtins.str, jsii.get(self, "schemaHandlerPackage"))

    @schema_handler_package.setter
    def schema_handler_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceVersion, "schema_handler_package").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaHandlerPackage", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        '''The name of the resource being registered.

        We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your resource names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-typename
        '''
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceVersion, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource.

        If your resource calls AWS APIs in any of its handlers, you must create an *`IAM execution role <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_* that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-executionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceVersion, "execution_role_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceVersion.LoggingConfigProperty"]]:
        '''Logging configuration information for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-loggingconfig
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceVersion.LoggingConfigProperty"]], jsii.get(self, "loggingConfig"))

    @logging_config.setter
    def logging_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceVersion.LoggingConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnResourceVersion, "logging_config").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnResourceVersion.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Logging configuration information for a resource.

            :param log_group_name: The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
            :param log_role_arn: The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                logging_config_property = cloudformation.CfnResourceVersion.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnResourceVersion.LoggingConfigProperty.__init__)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnResourceVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_handler_package": "schemaHandlerPackage",
        "type_name": "typeName",
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
    },
)
class CfnResourceVersionProps:
    def __init__(
        self,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnResourceVersion.LoggingConfigProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceVersion``.

        :param schema_handler_package: A URL to the S3 bucket containing the resource project package that contains the necessary files for the resource you want to register. For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide* . .. epigraph:: The user registering the resource must be able to access the package in the S3 bucket. That is, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param type_name: The name of the resource being registered. We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* . .. epigraph:: The following organization namespaces are reserved and can't be used in your resource names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``AWS`` - ``Custom`` - ``Dev``
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource. If your resource calls AWS APIs in any of its handlers, you must create an *`IAM execution role <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_* that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.
        :param logging_config: Logging configuration information for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_resource_version_props = cloudformation.CfnResourceVersionProps(
                schema_handler_package="schemaHandlerPackage",
                type_name="typeName",
            
                # the properties below are optional
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation.CfnResourceVersion.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnResourceVersionProps.__init__)
            check_type(argname="argument schema_handler_package", value=schema_handler_package, expected_type=type_hints["schema_handler_package"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "schema_handler_package": schema_handler_package,
            "type_name": type_name,
        }
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def schema_handler_package(self) -> builtins.str:
        '''A URL to the S3 bucket containing the resource project package that contains the necessary files for the resource you want to register.

        For information on generating a schema handler package for the resource you want to register, see `submit <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-cli-submit.html>`_ in the *CloudFormation CLI User Guide* .
        .. epigraph::

           The user registering the resource must be able to access the package in the S3 bucket. That is, the user needs to have `GetObject <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html>`_ permissions for the schema handler package. For more information, see `Actions, Resources, and Condition Keys for Amazon S3 <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-schemahandlerpackage
        '''
        result = self._values.get("schema_handler_package")
        assert result is not None, "Required property 'schema_handler_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''The name of the resource being registered.

        We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your resource names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-typename
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource.

        If your resource calls AWS APIs in any of its handlers, you must create an *`IAM execution role <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_* that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceVersion.LoggingConfigProperty]]:
        '''Logging configuration information for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceVersion.LoggingConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStack(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnStack",
):
    '''A CloudFormation ``AWS::CloudFormation::Stack``.

    The ``AWS::CloudFormation::Stack`` resource nests a stack as a resource in a top-level template.

    You can add output values from a nested stack within the containing template. You use the `GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ function with the nested stack's logical name and the name of the output value in the nested stack in the format ``Outputs. *NestedStackOutputName*`` .
    .. epigraph::

       We strongly recommend that updates to nested stacks are run from the parent stack.

    When you apply template changes to update a top-level stack, CloudFormation updates the top-level stack and initiates an update to its nested stacks. CloudFormation updates the resources of modified nested stacks, but doesn't update the resources of unmodified nested stacks. For more information, see `CloudFormation stack updates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html>`_ .
    .. epigraph::

       You must acknowledge IAM capabilities for nested stacks that contain IAM resources. Also, verify that you have cancel update stack permissions, which is required if an update rolls back. For more information about IAM and CloudFormation , see `Controlling access with AWS Identity and Access Management <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html>`_ .

    :cloudformationResource: AWS::CloudFormation::Stack
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_stack = cloudformation.CfnStack(self, "MyCfnStack",
            template_url="templateUrl",
        
            # the properties below are optional
            notification_arns=["notificationArns"],
            parameters={
                "parameters_key": "parameters"
            },
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout_in_minutes=123
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.core.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_url: Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. For more information, see `Template anatomy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html>`_ . Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param notification_arns: The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events. You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. .. epigraph:: If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks. Conditional. Required if the nested stack requires input parameters. Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param tags: Key-value pairs to associate with this stack. AWS CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.
        :param timeout_in_minutes: The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state. The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Updates aren't supported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStack.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackProps(
            template_url=template_url,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStack.inspect)
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
            type_hints = typing.get_type_hints(CfnStack._render_properties)
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
        '''Key-value pairs to associate with this stack.

        AWS CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> builtins.str:
        '''Location of file containing the template body.

        The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. For more information, see `Template anatomy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html>`_ .

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateUrl"))

    @template_url.setter
    def template_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStack, "template_url").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events.

        You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStack, "notification_arns").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter.
        .. epigraph::

           If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks.

        Conditional. Required if the nested stack requires input parameters.

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStack, "parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state.

        The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStack, "timeout_in_minutes").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMinutes", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_url": "templateUrl",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.core.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnStack``.

        :param template_url: Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. For more information, see `Template anatomy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html>`_ . Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param notification_arns: The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events. You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. .. epigraph:: If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks. Conditional. Required if the nested stack requires input parameters. Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param tags: Key-value pairs to associate with this stack. AWS CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.
        :param timeout_in_minutes: The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state. The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_stack_props = cloudformation.CfnStackProps(
                template_url="templateUrl",
            
                # the properties below are optional
                notification_arns=["notificationArns"],
                parameters={
                    "parameters_key": "parameters"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout_in_minutes=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStackProps.__init__)
            check_type(argname="argument template_url", value=template_url, expected_type=type_hints["template_url"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[str, typing.Any] = {
            "template_url": template_url,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def template_url(self) -> builtins.str:
        '''Location of file containing the template body.

        The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. For more information, see `Template anatomy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html>`_ .

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        '''
        result = self._values.get("template_url")
        assert result is not None, "Required property 'template_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events.

        You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter.
        .. epigraph::

           If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks.

        Conditional. Required if the nested stack requires input parameters.

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''Key-value pairs to associate with this stack.

        AWS CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state.

        The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStackSet(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet",
):
    '''A CloudFormation ``AWS::CloudFormation::StackSet``.

    The ``AWS::CloudFormation::StackSet`` enables you to provision stacks into AWS accounts and across Regions by using a single CloudFormation template. In the stack set, you specify the template to use, in addition to any parameters and capabilities that the template requires.

    :cloudformationResource: AWS::CloudFormation::StackSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        # managed_execution: Any
        
        cfn_stack_set = cloudformation.CfnStackSet(self, "MyCfnStackSet",
            permission_model="permissionModel",
            stack_set_name="stackSetName",
        
            # the properties below are optional
            administration_role_arn="administrationRoleArn",
            auto_deployment=cloudformation.CfnStackSet.AutoDeploymentProperty(
                enabled=False,
                retain_stacks_on_account_removal=False
            ),
            call_as="callAs",
            capabilities=["capabilities"],
            description="description",
            execution_role_name="executionRoleName",
            managed_execution=managed_execution,
            operation_preferences=cloudformation.CfnStackSet.OperationPreferencesProperty(
                failure_tolerance_count=123,
                failure_tolerance_percentage=123,
                max_concurrent_count=123,
                max_concurrent_percentage=123,
                region_concurrency_type="regionConcurrencyType",
                region_order=["regionOrder"]
            ),
            parameters=[cloudformation.CfnStackSet.ParameterProperty(
                parameter_key="parameterKey",
                parameter_value="parameterValue"
            )],
            stack_instances_group=[cloudformation.CfnStackSet.StackInstancesProperty(
                deployment_targets=cloudformation.CfnStackSet.DeploymentTargetsProperty(
                    account_filter_type="accountFilterType",
                    accounts=["accounts"],
                    organizational_unit_ids=["organizationalUnitIds"]
                ),
                regions=["regions"],
        
                # the properties below are optional
                parameter_overrides=[cloudformation.CfnStackSet.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )]
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_body="templateBody",
            template_url="templateUrl"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        permission_model: builtins.str,
        stack_set_name: builtins.str,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.AutoDeploymentProperty", typing.Dict[str, typing.Any]]]] = None,
        call_as: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        managed_execution: typing.Any = None,
        operation_preferences: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.OperationPreferencesProperty", typing.Dict[str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.ParameterProperty", typing.Dict[str, typing.Any]]]]]] = None,
        stack_instances_group: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.StackInstancesProperty", typing.Dict[str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.core.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::StackSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param permission_model: Describes how the IAM roles required for stack set operations are created. - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant Self-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ . - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Grant Service-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-service-managed.html>`_ . *Allowed Values* : ``SERVICE_MANAGED`` | ``SELF_MANAGED`` .. epigraph:: The ``PermissionModel`` property is required.
        :param stack_set_name: The name to associate with the stack set. The name must be unique in the Region where you create your stack set. *Maximum* : ``128`` *Pattern* : ``^[a-zA-Z][a-zA-Z0-9-]{0,127}$`` .. epigraph:: The ``StackSetName`` property is required.
        :param administration_role_arn: The Amazon Resource Number (ARN) of the IAM role to use to create this stack set. Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. Use customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. For more information, see `Prerequisites: Granting Permissions for Stack Set Operations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html>`_ in the *AWS CloudFormation User Guide* . *Minimum* : ``20`` *Maximum* : ``2048``
        :param auto_deployment: [ ``Service-managed`` permissions] Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).
        :param call_as: [Service-managed permissions] Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account. By default, ``SELF`` is specified. Use ``SELF`` for stack sets with self-managed permissions. - To create a stack set with service-managed permissions while signed in to the management account, specify ``SELF`` . - To create a stack set with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` . Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *AWS CloudFormation User Guide* . Stack sets with service-managed permissions are created in the management account, including stack sets that are created by delegated administrators. *Valid Values* : ``SELF`` | ``DELEGATED_ADMIN``
        :param capabilities: The capabilities that are allowed in the stack set. Some stack set templates might include resources that can affect permissions in your AWS account —for example, by creating new AWS Identity and Access Management ( IAM ) users. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities>`_ .
        :param description: A description of the stack set. *Minimum* : ``1`` *Maximum* : ``1024``
        :param execution_role_name: The name of the IAM execution role to use to create the stack set. If you don't specify an execution role, AWS CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the stack set operation. *Minimum* : ``1`` *Maximum* : ``64`` *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``
        :param managed_execution: Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations. When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. .. epigraph:: If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting. You can't modify your stack set's execution configuration while there are running or queued operations for that stack set. When inactive (default), StackSets performs one operation at a time in request order.
        :param operation_preferences: The user-specified preferences for how AWS CloudFormation performs a stack set operation.
        :param parameters: The input parameters for the stack set template.
        :param stack_instances_group: A group of stack instances with parameters in some specific accounts and Regions.
        :param tags: The key-value pairs to associate with this stack set and the stacks created from it. AWS CloudFormation also propagates these tags to supported resources that are created in the stacks. A maximum number of 50 tags can be specified.
        :param template_body: The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes. You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates containing dynamic references through ``TemplateUrl`` instead. *Minimum* : ``1`` *Maximum* : ``51200``
        :param template_url: Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. *Minimum* : ``1`` *Maximum* : ``1024``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStackSet.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackSetProps(
            permission_model=permission_model,
            stack_set_name=stack_set_name,
            administration_role_arn=administration_role_arn,
            auto_deployment=auto_deployment,
            call_as=call_as,
            capabilities=capabilities,
            description=description,
            execution_role_name=execution_role_name,
            managed_execution=managed_execution,
            operation_preferences=operation_preferences,
            parameters=parameters,
            stack_instances_group=stack_instances_group,
            tags=tags,
            template_body=template_body,
            template_url=template_url,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStackSet.inspect)
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
            type_hints = typing.get_type_hints(CfnStackSet._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrStackSetId")
    def attr_stack_set_id(self) -> builtins.str:
        '''The ID of the stack that you're creating.

        :cloudformationAttribute: StackSetId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStackSetId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''The key-value pairs to associate with this stack set and the stacks created from it.

        AWS CloudFormation also propagates these tags to supported resources that are created in the stacks. A maximum number of 50 tags can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="managedExecution")
    def managed_execution(self) -> typing.Any:
        '''Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations.

        When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order.
        .. epigraph::

           If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting.

           You can't modify your stack set's execution configuration while there are running or queued operations for that stack set.

        When inactive (default), StackSets performs one operation at a time in request order.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-managedexecution
        '''
        return typing.cast(typing.Any, jsii.get(self, "managedExecution"))

    @managed_execution.setter
    def managed_execution(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "managed_execution").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedExecution", value)

    @builtins.property
    @jsii.member(jsii_name="permissionModel")
    def permission_model(self) -> builtins.str:
        '''Describes how the IAM roles required for stack set operations are created.

        - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant Self-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ .
        - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Grant Service-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-service-managed.html>`_ .

        *Allowed Values* : ``SERVICE_MANAGED`` | ``SELF_MANAGED``
        .. epigraph::

           The ``PermissionModel`` property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        '''
        return typing.cast(builtins.str, jsii.get(self, "permissionModel"))

    @permission_model.setter
    def permission_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "permission_model").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionModel", value)

    @builtins.property
    @jsii.member(jsii_name="stackSetName")
    def stack_set_name(self) -> builtins.str:
        '''The name to associate with the stack set.

        The name must be unique in the Region where you create your stack set.

        *Maximum* : ``128``

        *Pattern* : ``^[a-zA-Z][a-zA-Z0-9-]{0,127}$``
        .. epigraph::

           The ``StackSetName`` property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackSetName"))

    @stack_set_name.setter
    def stack_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "stack_set_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackSetName", value)

    @builtins.property
    @jsii.member(jsii_name="administrationRoleArn")
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the IAM role to use to create this stack set.

        Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account.

        Use customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. For more information, see `Prerequisites: Granting Permissions for Stack Set Operations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html>`_ in the *AWS CloudFormation User Guide* .

        *Minimum* : ``20``

        *Maximum* : ``2048``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administrationRoleArn"))

    @administration_role_arn.setter
    def administration_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "administration_role_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrationRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="autoDeployment")
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.AutoDeploymentProperty"]]:
        '''[ ``Service-managed`` permissions] Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.AutoDeploymentProperty"]], jsii.get(self, "autoDeployment"))

    @auto_deployment.setter
    def auto_deployment(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.AutoDeploymentProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "auto_deployment").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployment", value)

    @builtins.property
    @jsii.member(jsii_name="callAs")
    def call_as(self) -> typing.Optional[builtins.str]:
        '''[Service-managed permissions] Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account.

        By default, ``SELF`` is specified. Use ``SELF`` for stack sets with self-managed permissions.

        - To create a stack set with service-managed permissions while signed in to the management account, specify ``SELF`` .
        - To create a stack set with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` .

        Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *AWS CloudFormation User Guide* .

        Stack sets with service-managed permissions are created in the management account, including stack sets that are created by delegated administrators.

        *Valid Values* : ``SELF`` | ``DELEGATED_ADMIN``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-callas
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callAs"))

    @call_as.setter
    def call_as(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "call_as").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callAs", value)

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The capabilities that are allowed in the stack set.

        Some stack set templates might include resources that can affect permissions in your AWS account —for example, by creating new AWS Identity and Access Management ( IAM ) users. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "capabilities").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack set.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleName")
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to create the stack set.

        If you don't specify an execution role, AWS CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the stack set operation.

        *Minimum* : ``1``

        *Maximum* : ``64``

        *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleName"))

    @execution_role_name.setter
    def execution_role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "execution_role_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleName", value)

    @builtins.property
    @jsii.member(jsii_name="operationPreferences")
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]]:
        '''The user-specified preferences for how AWS CloudFormation performs a stack set operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]], jsii.get(self, "operationPreferences"))

    @operation_preferences.setter
    def operation_preferences(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "operation_preferences").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationPreferences", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]]:
        '''The input parameters for the stack set template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "parameters").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="stackInstancesGroup")
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]]:
        '''A group of stack instances with parameters in some specific accounts and Regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]], jsii.get(self, "stackInstancesGroup"))

    @stack_instances_group.setter
    def stack_instances_group(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "stack_instances_group").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackInstancesGroup", value)

    @builtins.property
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> typing.Optional[builtins.str]:
        '''The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes.

        You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates containing dynamic references through ``TemplateUrl`` instead.

        *Minimum* : ``1``

        *Maximum* : ``51200``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateBody"))

    @template_body.setter
    def template_body(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "template_body").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateBody", value)

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> typing.Optional[builtins.str]:
        '''Location of file containing the template body.

        The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket.

        You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateUrl"))

    @template_url.setter
    def template_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnStackSet, "template_url").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateUrl", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.AutoDeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "retain_stacks_on_account_removal": "retainStacksOnAccountRemoval",
        },
    )
    class AutoDeploymentProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            retain_stacks_on_account_removal: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''[ ``Service-managed`` permissions] Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organizational unit (OU).

            :param enabled: If set to ``true`` , StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions. If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.
            :param retain_stacks_on_account_removal: If set to ``true`` , stack resources are retained when an account is removed from a target organization or OU. If set to ``false`` , stack resources are deleted. Specify only if ``Enabled`` is set to ``True`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                auto_deployment_property = cloudformation.CfnStackSet.AutoDeploymentProperty(
                    enabled=False,
                    retain_stacks_on_account_removal=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStackSet.AutoDeploymentProperty.__init__)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument retain_stacks_on_account_removal", value=retain_stacks_on_account_removal, expected_type=type_hints["retain_stacks_on_account_removal"])
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if retain_stacks_on_account_removal is not None:
                self._values["retain_stacks_on_account_removal"] = retain_stacks_on_account_removal

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''If set to ``true`` , StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions.

            If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def retain_stacks_on_account_removal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''If set to ``true`` , stack resources are retained when an account is removed from a target organization or OU.

            If set to ``false`` , stack resources are deleted. Specify only if ``Enabled`` is set to ``True`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-retainstacksonaccountremoval
            '''
            result = self._values.get("retain_stacks_on_account_removal")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoDeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.DeploymentTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_filter_type": "accountFilterType",
            "accounts": "accounts",
            "organizational_unit_ids": "organizationalUnitIds",
        },
    )
    class DeploymentTargetsProperty:
        def __init__(
            self,
            *,
            account_filter_type: typing.Optional[builtins.str] = None,
            accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The AWS OrganizationalUnitIds or Accounts for which to create stack instances in the specified Regions.

            :param account_filter_type: ``CfnStackSet.DeploymentTargetsProperty.AccountFilterType``.
            :param accounts: The names of one or more AWS accounts for which you want to deploy stack set updates. *Pattern* : ``^[0-9]{12}$``
            :param organizational_unit_ids: The organization root ID or organizational unit (OU) IDs to which StackSets deploys. *Pattern* : ``^(ou-[a-z0-9]{4,32}-[a-z0-9]{8,32}|r-[a-z0-9]{4,32})$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                deployment_targets_property = cloudformation.CfnStackSet.DeploymentTargetsProperty(
                    account_filter_type="accountFilterType",
                    accounts=["accounts"],
                    organizational_unit_ids=["organizationalUnitIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStackSet.DeploymentTargetsProperty.__init__)
                check_type(argname="argument account_filter_type", value=account_filter_type, expected_type=type_hints["account_filter_type"])
                check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
                check_type(argname="argument organizational_unit_ids", value=organizational_unit_ids, expected_type=type_hints["organizational_unit_ids"])
            self._values: typing.Dict[str, typing.Any] = {}
            if account_filter_type is not None:
                self._values["account_filter_type"] = account_filter_type
            if accounts is not None:
                self._values["accounts"] = accounts
            if organizational_unit_ids is not None:
                self._values["organizational_unit_ids"] = organizational_unit_ids

        @builtins.property
        def account_filter_type(self) -> typing.Optional[builtins.str]:
            '''``CfnStackSet.DeploymentTargetsProperty.AccountFilterType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accountfiltertype
            '''
            result = self._values.get("account_filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of one or more AWS accounts for which you want to deploy stack set updates.

            *Pattern* : ``^[0-9]{12}$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accounts
            '''
            result = self._values.get("accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def organizational_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The organization root ID or organizational unit (OU) IDs to which StackSets deploys.

            *Pattern* : ``^(ou-[a-z0-9]{4,32}-[a-z0-9]{8,32}|r-[a-z0-9]{4,32})$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-organizationalunitids
            '''
            result = self._values.get("organizational_unit_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.OperationPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_tolerance_count": "failureToleranceCount",
            "failure_tolerance_percentage": "failureTolerancePercentage",
            "max_concurrent_count": "maxConcurrentCount",
            "max_concurrent_percentage": "maxConcurrentPercentage",
            "region_concurrency_type": "regionConcurrencyType",
            "region_order": "regionOrder",
        },
    )
    class OperationPreferencesProperty:
        def __init__(
            self,
            *,
            failure_tolerance_count: typing.Optional[jsii.Number] = None,
            failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            max_concurrent_count: typing.Optional[jsii.Number] = None,
            max_concurrent_percentage: typing.Optional[jsii.Number] = None,
            region_concurrency_type: typing.Optional[builtins.str] = None,
            region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The user-specified preferences for how AWS CloudFormation performs a stack set operation.

            For more information on maximum concurrent accounts and failure tolerance, see `Stack set operation options <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html#stackset-ops-options>`_ .

            :param failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region. If the operation is stopped in a Region, AWS CloudFormation doesn't attempt the operation in any subsequent Regions. Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` (but not both).
            :param failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region. If the operation is stopped in a Region, AWS CloudFormation doesn't attempt the operation in any subsequent Regions. When calculating the number of accounts based on the specified percentage, AWS CloudFormation rounds *down* to the next whole number. Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` , but not both.
            :param max_concurrent_count: The maximum number of accounts in which to perform this operation at one time. This is dependent on the value of ``FailureToleranceCount`` . ``MaxConcurrentCount`` is at most one more than the ``FailureToleranceCount`` . Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.
            :param max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time. When calculating the number of accounts based on the specified percentage, AWS CloudFormation rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, CloudFormation sets the number as one instead. Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.
            :param region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time. *Allowed values* : ``SEQUENTIAL`` | ``PARALLEL``
            :param region_order: The order of the Regions where you want to perform the stack operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                operation_preferences_property = cloudformation.CfnStackSet.OperationPreferencesProperty(
                    failure_tolerance_count=123,
                    failure_tolerance_percentage=123,
                    max_concurrent_count=123,
                    max_concurrent_percentage=123,
                    region_concurrency_type="regionConcurrencyType",
                    region_order=["regionOrder"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStackSet.OperationPreferencesProperty.__init__)
                check_type(argname="argument failure_tolerance_count", value=failure_tolerance_count, expected_type=type_hints["failure_tolerance_count"])
                check_type(argname="argument failure_tolerance_percentage", value=failure_tolerance_percentage, expected_type=type_hints["failure_tolerance_percentage"])
                check_type(argname="argument max_concurrent_count", value=max_concurrent_count, expected_type=type_hints["max_concurrent_count"])
                check_type(argname="argument max_concurrent_percentage", value=max_concurrent_percentage, expected_type=type_hints["max_concurrent_percentage"])
                check_type(argname="argument region_concurrency_type", value=region_concurrency_type, expected_type=type_hints["region_concurrency_type"])
                check_type(argname="argument region_order", value=region_order, expected_type=type_hints["region_order"])
            self._values: typing.Dict[str, typing.Any] = {}
            if failure_tolerance_count is not None:
                self._values["failure_tolerance_count"] = failure_tolerance_count
            if failure_tolerance_percentage is not None:
                self._values["failure_tolerance_percentage"] = failure_tolerance_percentage
            if max_concurrent_count is not None:
                self._values["max_concurrent_count"] = max_concurrent_count
            if max_concurrent_percentage is not None:
                self._values["max_concurrent_percentage"] = max_concurrent_percentage
            if region_concurrency_type is not None:
                self._values["region_concurrency_type"] = region_concurrency_type
            if region_order is not None:
                self._values["region_order"] = region_order

        @builtins.property
        def failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.

            If the operation is stopped in a Region, AWS CloudFormation doesn't attempt the operation in any subsequent Regions.

            Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` (but not both).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancecount
            '''
            result = self._values.get("failure_tolerance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def failure_tolerance_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.

            If the operation is stopped in a Region, AWS CloudFormation doesn't attempt the operation in any subsequent Regions.

            When calculating the number of accounts based on the specified percentage, AWS CloudFormation rounds *down* to the next whole number.

            Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancepercentage
            '''
            result = self._values.get("failure_tolerance_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of accounts in which to perform this operation at one time.

            This is dependent on the value of ``FailureToleranceCount`` . ``MaxConcurrentCount`` is at most one more than the ``FailureToleranceCount`` .

            Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentcount
            '''
            result = self._values.get("max_concurrent_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of accounts in which to perform this operation at one time.

            When calculating the number of accounts based on the specified percentage, AWS CloudFormation rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, CloudFormation sets the number as one instead.

            Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentpercentage
            '''
            result = self._values.get("max_concurrent_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def region_concurrency_type(self) -> typing.Optional[builtins.str]:
            '''The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.

            *Allowed values* : ``SEQUENTIAL`` | ``PARALLEL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionconcurrencytype
            '''
            result = self._values.get("region_concurrency_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_order(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The order of the Regions where you want to perform the stack operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionorder
            '''
            result = self._values.get("region_order")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OperationPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_key": "parameterKey",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_key: builtins.str,
            parameter_value: builtins.str,
        ) -> None:
            '''The Parameter data type.

            :param parameter_key: The key associated with the parameter. If you don't specify a key and value for a particular parameter, AWS CloudFormation uses the default value that's specified in your template.
            :param parameter_value: The input value associated with the parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                parameter_property = cloudformation.CfnStackSet.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStackSet.ParameterProperty.__init__)
                check_type(argname="argument parameter_key", value=parameter_key, expected_type=type_hints["parameter_key"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[str, typing.Any] = {
                "parameter_key": parameter_key,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_key(self) -> builtins.str:
            '''The key associated with the parameter.

            If you don't specify a key and value for a particular parameter, AWS CloudFormation uses the default value that's specified in your template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parameterkey
            '''
            result = self._values.get("parameter_key")
            assert result is not None, "Required property 'parameter_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameter_value(self) -> builtins.str:
            '''The input value associated with the parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            assert result is not None, "Required property 'parameter_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.StackInstancesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_targets": "deploymentTargets",
            "regions": "regions",
            "parameter_overrides": "parameterOverrides",
        },
    )
    class StackInstancesProperty:
        def __init__(
            self,
            *,
            deployment_targets: typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.DeploymentTargetsProperty", typing.Dict[str, typing.Any]]],
            regions: typing.Sequence[builtins.str],
            parameter_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnStackSet.ParameterProperty", typing.Dict[str, typing.Any]]]]]] = None,
        ) -> None:
            '''Stack instances in some specific accounts and Regions.

            :param deployment_targets: The AWS ``OrganizationalUnitIds`` or ``Accounts`` for which to create stack instances in the specified Regions.
            :param regions: The names of one or more Regions where you want to create stack instances using the specified AWS accounts .
            :param parameter_overrides: A list of stack set parameters whose values you want to override in the selected stack instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                stack_instances_property = cloudformation.CfnStackSet.StackInstancesProperty(
                    deployment_targets=cloudformation.CfnStackSet.DeploymentTargetsProperty(
                        account_filter_type="accountFilterType",
                        accounts=["accounts"],
                        organizational_unit_ids=["organizationalUnitIds"]
                    ),
                    regions=["regions"],
                
                    # the properties below are optional
                    parameter_overrides=[cloudformation.CfnStackSet.ParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnStackSet.StackInstancesProperty.__init__)
                check_type(argname="argument deployment_targets", value=deployment_targets, expected_type=type_hints["deployment_targets"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument parameter_overrides", value=parameter_overrides, expected_type=type_hints["parameter_overrides"])
            self._values: typing.Dict[str, typing.Any] = {
                "deployment_targets": deployment_targets,
                "regions": regions,
            }
            if parameter_overrides is not None:
                self._values["parameter_overrides"] = parameter_overrides

        @builtins.property
        def deployment_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.DeploymentTargetsProperty"]:
            '''The AWS ``OrganizationalUnitIds`` or ``Accounts`` for which to create stack instances in the specified Regions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets
            '''
            result = self._values.get("deployment_targets")
            assert result is not None, "Required property 'deployment_targets' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.DeploymentTargetsProperty"], result)

        @builtins.property
        def regions(self) -> typing.List[builtins.str]:
            '''The names of one or more Regions where you want to create stack instances using the specified AWS accounts .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-regions
            '''
            result = self._values.get("regions")
            assert result is not None, "Required property 'regions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def parameter_overrides(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]]:
            '''A list of stack set parameters whose values you want to override in the selected stack instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-parameteroverrides
            '''
            result = self._values.get("parameter_overrides")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackInstancesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "permission_model": "permissionModel",
        "stack_set_name": "stackSetName",
        "administration_role_arn": "administrationRoleArn",
        "auto_deployment": "autoDeployment",
        "call_as": "callAs",
        "capabilities": "capabilities",
        "description": "description",
        "execution_role_name": "executionRoleName",
        "managed_execution": "managedExecution",
        "operation_preferences": "operationPreferences",
        "parameters": "parameters",
        "stack_instances_group": "stackInstancesGroup",
        "tags": "tags",
        "template_body": "templateBody",
        "template_url": "templateUrl",
    },
)
class CfnStackSetProps:
    def __init__(
        self,
        *,
        permission_model: builtins.str,
        stack_set_name: builtins.str,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStackSet.AutoDeploymentProperty, typing.Dict[str, typing.Any]]]] = None,
        call_as: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        managed_execution: typing.Any = None,
        operation_preferences: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStackSet.OperationPreferencesProperty, typing.Dict[str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStackSet.ParameterProperty, typing.Dict[str, typing.Any]]]]]] = None,
        stack_instances_group: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnStackSet.StackInstancesProperty, typing.Dict[str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.core.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnStackSet``.

        :param permission_model: Describes how the IAM roles required for stack set operations are created. - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant Self-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ . - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Grant Service-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-service-managed.html>`_ . *Allowed Values* : ``SERVICE_MANAGED`` | ``SELF_MANAGED`` .. epigraph:: The ``PermissionModel`` property is required.
        :param stack_set_name: The name to associate with the stack set. The name must be unique in the Region where you create your stack set. *Maximum* : ``128`` *Pattern* : ``^[a-zA-Z][a-zA-Z0-9-]{0,127}$`` .. epigraph:: The ``StackSetName`` property is required.
        :param administration_role_arn: The Amazon Resource Number (ARN) of the IAM role to use to create this stack set. Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. Use customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. For more information, see `Prerequisites: Granting Permissions for Stack Set Operations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html>`_ in the *AWS CloudFormation User Guide* . *Minimum* : ``20`` *Maximum* : ``2048``
        :param auto_deployment: [ ``Service-managed`` permissions] Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).
        :param call_as: [Service-managed permissions] Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account. By default, ``SELF`` is specified. Use ``SELF`` for stack sets with self-managed permissions. - To create a stack set with service-managed permissions while signed in to the management account, specify ``SELF`` . - To create a stack set with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` . Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *AWS CloudFormation User Guide* . Stack sets with service-managed permissions are created in the management account, including stack sets that are created by delegated administrators. *Valid Values* : ``SELF`` | ``DELEGATED_ADMIN``
        :param capabilities: The capabilities that are allowed in the stack set. Some stack set templates might include resources that can affect permissions in your AWS account —for example, by creating new AWS Identity and Access Management ( IAM ) users. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities>`_ .
        :param description: A description of the stack set. *Minimum* : ``1`` *Maximum* : ``1024``
        :param execution_role_name: The name of the IAM execution role to use to create the stack set. If you don't specify an execution role, AWS CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the stack set operation. *Minimum* : ``1`` *Maximum* : ``64`` *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``
        :param managed_execution: Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations. When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. .. epigraph:: If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting. You can't modify your stack set's execution configuration while there are running or queued operations for that stack set. When inactive (default), StackSets performs one operation at a time in request order.
        :param operation_preferences: The user-specified preferences for how AWS CloudFormation performs a stack set operation.
        :param parameters: The input parameters for the stack set template.
        :param stack_instances_group: A group of stack instances with parameters in some specific accounts and Regions.
        :param tags: The key-value pairs to associate with this stack set and the stacks created from it. AWS CloudFormation also propagates these tags to supported resources that are created in the stacks. A maximum number of 50 tags can be specified.
        :param template_body: The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes. You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates containing dynamic references through ``TemplateUrl`` instead. *Minimum* : ``1`` *Maximum* : ``51200``
        :param template_url: Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket. You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. *Minimum* : ``1`` *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            # managed_execution: Any
            
            cfn_stack_set_props = cloudformation.CfnStackSetProps(
                permission_model="permissionModel",
                stack_set_name="stackSetName",
            
                # the properties below are optional
                administration_role_arn="administrationRoleArn",
                auto_deployment=cloudformation.CfnStackSet.AutoDeploymentProperty(
                    enabled=False,
                    retain_stacks_on_account_removal=False
                ),
                call_as="callAs",
                capabilities=["capabilities"],
                description="description",
                execution_role_name="executionRoleName",
                managed_execution=managed_execution,
                operation_preferences=cloudformation.CfnStackSet.OperationPreferencesProperty(
                    failure_tolerance_count=123,
                    failure_tolerance_percentage=123,
                    max_concurrent_count=123,
                    max_concurrent_percentage=123,
                    region_concurrency_type="regionConcurrencyType",
                    region_order=["regionOrder"]
                ),
                parameters=[cloudformation.CfnStackSet.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )],
                stack_instances_group=[cloudformation.CfnStackSet.StackInstancesProperty(
                    deployment_targets=cloudformation.CfnStackSet.DeploymentTargetsProperty(
                        account_filter_type="accountFilterType",
                        accounts=["accounts"],
                        organizational_unit_ids=["organizationalUnitIds"]
                    ),
                    regions=["regions"],
            
                    # the properties below are optional
                    parameter_overrides=[cloudformation.CfnStackSet.ParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_body="templateBody",
                template_url="templateUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnStackSetProps.__init__)
            check_type(argname="argument permission_model", value=permission_model, expected_type=type_hints["permission_model"])
            check_type(argname="argument stack_set_name", value=stack_set_name, expected_type=type_hints["stack_set_name"])
            check_type(argname="argument administration_role_arn", value=administration_role_arn, expected_type=type_hints["administration_role_arn"])
            check_type(argname="argument auto_deployment", value=auto_deployment, expected_type=type_hints["auto_deployment"])
            check_type(argname="argument call_as", value=call_as, expected_type=type_hints["call_as"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_name", value=execution_role_name, expected_type=type_hints["execution_role_name"])
            check_type(argname="argument managed_execution", value=managed_execution, expected_type=type_hints["managed_execution"])
            check_type(argname="argument operation_preferences", value=operation_preferences, expected_type=type_hints["operation_preferences"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument stack_instances_group", value=stack_instances_group, expected_type=type_hints["stack_instances_group"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_body", value=template_body, expected_type=type_hints["template_body"])
            check_type(argname="argument template_url", value=template_url, expected_type=type_hints["template_url"])
        self._values: typing.Dict[str, typing.Any] = {
            "permission_model": permission_model,
            "stack_set_name": stack_set_name,
        }
        if administration_role_arn is not None:
            self._values["administration_role_arn"] = administration_role_arn
        if auto_deployment is not None:
            self._values["auto_deployment"] = auto_deployment
        if call_as is not None:
            self._values["call_as"] = call_as
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if execution_role_name is not None:
            self._values["execution_role_name"] = execution_role_name
        if managed_execution is not None:
            self._values["managed_execution"] = managed_execution
        if operation_preferences is not None:
            self._values["operation_preferences"] = operation_preferences
        if parameters is not None:
            self._values["parameters"] = parameters
        if stack_instances_group is not None:
            self._values["stack_instances_group"] = stack_instances_group
        if tags is not None:
            self._values["tags"] = tags
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_url is not None:
            self._values["template_url"] = template_url

    @builtins.property
    def permission_model(self) -> builtins.str:
        '''Describes how the IAM roles required for stack set operations are created.

        - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant Self-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ .
        - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Grant Service-Managed Stack Set Permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-service-managed.html>`_ .

        *Allowed Values* : ``SERVICE_MANAGED`` | ``SELF_MANAGED``
        .. epigraph::

           The ``PermissionModel`` property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        '''
        result = self._values.get("permission_model")
        assert result is not None, "Required property 'permission_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_set_name(self) -> builtins.str:
        '''The name to associate with the stack set.

        The name must be unique in the Region where you create your stack set.

        *Maximum* : ``128``

        *Pattern* : ``^[a-zA-Z][a-zA-Z0-9-]{0,127}$``
        .. epigraph::

           The ``StackSetName`` property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        '''
        result = self._values.get("stack_set_name")
        assert result is not None, "Required property 'stack_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the IAM role to use to create this stack set.

        Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account.

        Use customized administrator roles to control which users or groups can manage specific stack sets within the same administrator account. For more information, see `Prerequisites: Granting Permissions for Stack Set Operations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html>`_ in the *AWS CloudFormation User Guide* .

        *Minimum* : ``20``

        *Maximum* : ``2048``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        '''
        result = self._values.get("administration_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.AutoDeploymentProperty]]:
        '''[ ``Service-managed`` permissions] Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        '''
        result = self._values.get("auto_deployment")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.AutoDeploymentProperty]], result)

    @builtins.property
    def call_as(self) -> typing.Optional[builtins.str]:
        '''[Service-managed permissions] Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account.

        By default, ``SELF`` is specified. Use ``SELF`` for stack sets with self-managed permissions.

        - To create a stack set with service-managed permissions while signed in to the management account, specify ``SELF`` .
        - To create a stack set with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` .

        Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *AWS CloudFormation User Guide* .

        Stack sets with service-managed permissions are created in the management account, including stack sets that are created by delegated administrators.

        *Valid Values* : ``SELF`` | ``DELEGATED_ADMIN``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-callas
        '''
        result = self._values.get("call_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The capabilities that are allowed in the stack set.

        Some stack set templates might include resources that can affect permissions in your AWS account —for example, by creating new AWS Identity and Access Management ( IAM ) users. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack set.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to create the stack set.

        If you don't specify an execution role, AWS CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the stack set operation.

        *Minimum* : ``1``

        *Maximum* : ``64``

        *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        '''
        result = self._values.get("execution_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_execution(self) -> typing.Any:
        '''Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations.

        When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order.
        .. epigraph::

           If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting.

           You can't modify your stack set's execution configuration while there are running or queued operations for that stack set.

        When inactive (default), StackSets performs one operation at a time in request order.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-managedexecution
        '''
        result = self._values.get("managed_execution")
        return typing.cast(typing.Any, result)

    @builtins.property
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.OperationPreferencesProperty]]:
        '''The user-specified preferences for how AWS CloudFormation performs a stack set operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        '''
        result = self._values.get("operation_preferences")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.OperationPreferencesProperty]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.ParameterProperty]]]]:
        '''The input parameters for the stack set template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.ParameterProperty]]]], result)

    @builtins.property
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.StackInstancesProperty]]]]:
        '''A group of stack instances with parameters in some specific accounts and Regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        '''
        result = self._values.get("stack_instances_group")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.StackInstancesProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''The key-value pairs to associate with this stack set and the stacks created from it.

        AWS CloudFormation also propagates these tags to supported resources that are created in the stacks. A maximum number of 50 tags can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        '''The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes.

        You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates containing dynamic references through ``TemplateUrl`` instead.

        *Minimum* : ``1``

        *Maximum* : ``51200``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        '''
        result = self._values.get("template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_url(self) -> typing.Optional[builtins.str]:
        '''Location of file containing the template body.

        The URL must point to a template (max size: 460,800 bytes) that's located in an Amazon S3 bucket.

        You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        '''
        result = self._values.get("template_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTypeActivation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnTypeActivation",
):
    '''A CloudFormation ``AWS::CloudFormation::TypeActivation``.

    Activates a public third-party extension, making it available for use in stack templates. For more information, see `Using public extensions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html>`_ in the *AWS CloudFormation User Guide* .

    Once you have activated a public third-party extension in your account and region, use `SetTypeConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_SetTypeConfiguration.html>`_ to specify configuration properties for the extension. For more information, see `Configuring extensions at the account level <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-register.html#registry-set-configuration>`_ in the *CloudFormation User Guide* .

    :cloudformationResource: AWS::CloudFormation::TypeActivation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_type_activation = cloudformation.CfnTypeActivation(self, "MyCfnTypeActivation",
            auto_update=False,
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation.CfnTypeActivation.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            ),
            major_version="majorVersion",
            public_type_arn="publicTypeArn",
            publisher_id="publisherId",
            type="type",
            type_name="typeName",
            type_name_alias="typeNameAlias",
            version_bump="versionBump"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_update: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union["CfnTypeActivation.LoggingConfigProperty", typing.Dict[str, typing.Any]]]] = None,
        major_version: typing.Optional[builtins.str] = None,
        public_type_arn: typing.Optional[builtins.str] = None,
        publisher_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
        type_name_alias: typing.Optional[builtins.str] = None,
        version_bump: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::TypeActivation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_update: Whether to automatically update the extension in this account and region when a new *minor* version is published by the extension publisher. Major versions released by the publisher must be manually updated. The default is ``true`` .
        :param execution_role_arn: The name of the IAM execution role to use to activate the extension.
        :param logging_config: Specifies logging configuration information for an extension.
        :param major_version: The major version of this extension you want to activate, if multiple major versions are available. The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected. You can specify ``MajorVersion`` or ``VersionBump`` , but not both.
        :param public_type_arn: The Amazon Resource Number (ARN) of the public extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param publisher_id: The ID of the extension publisher. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type: The extension type. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name: The name of the extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name_alias: An alias to assign to the public extension, in this account and region. If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console. An extension alias must be unique within a given account and region. You can activate the same public resource multiple times in the same account and region, using different type name aliases.
        :param version_bump: Manually updates a previously-activated type to a new major or minor version, if available. You can also use this parameter to update the value of ``AutoUpdate`` . - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available. - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnTypeActivation.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTypeActivationProps(
            auto_update=auto_update,
            execution_role_arn=execution_role_arn,
            logging_config=logging_config,
            major_version=major_version,
            public_type_arn=public_type_arn,
            publisher_id=publisher_id,
            type=type,
            type_name=type_name,
            type_name_alias=type_name_alias,
            version_bump=version_bump,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnTypeActivation.inspect)
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
            type_hints = typing.get_type_hints(CfnTypeActivation._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the activated extension, in this account and Region.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="autoUpdate")
    def auto_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Whether to automatically update the extension in this account and region when a new *minor* version is published by the extension publisher.

        Major versions released by the publisher must be manually updated.

        The default is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-autoupdate
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "autoUpdate"))

    @auto_update.setter
    def auto_update(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "auto_update").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoUpdate", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to activate the extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-executionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "execution_role_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTypeActivation.LoggingConfigProperty"]]:
        '''Specifies logging configuration information for an extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-loggingconfig
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTypeActivation.LoggingConfigProperty"]], jsii.get(self, "loggingConfig"))

    @logging_config.setter
    def logging_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTypeActivation.LoggingConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "logging_config").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> typing.Optional[builtins.str]:
        '''The major version of this extension you want to activate, if multiple major versions are available.

        The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected.

        You can specify ``MajorVersion`` or ``VersionBump`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-majorversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "majorVersion"))

    @major_version.setter
    def major_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "major_version").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "majorVersion", value)

    @builtins.property
    @jsii.member(jsii_name="publicTypeArn")
    def public_type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the public extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publictypearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicTypeArn"))

    @public_type_arn.setter
    def public_type_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "public_type_arn").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicTypeArn", value)

    @builtins.property
    @jsii.member(jsii_name="publisherId")
    def publisher_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the extension publisher.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publisherid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherId"))

    @publisher_id.setter
    def publisher_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "publisher_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisherId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The extension type.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "type_name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="typeNameAlias")
    def type_name_alias(self) -> typing.Optional[builtins.str]:
        '''An alias to assign to the public extension, in this account and region.

        If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console.

        An extension alias must be unique within a given account and region. You can activate the same public resource multiple times in the same account and region, using different type name aliases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typenamealias
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeNameAlias"))

    @type_name_alias.setter
    def type_name_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "type_name_alias").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeNameAlias", value)

    @builtins.property
    @jsii.member(jsii_name="versionBump")
    def version_bump(self) -> typing.Optional[builtins.str]:
        '''Manually updates a previously-activated type to a new major or minor version, if available.

        You can also use this parameter to update the value of ``AutoUpdate`` .

        - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available.
        - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-versionbump
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionBump"))

    @version_bump.setter
    def version_bump(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnTypeActivation, "version_bump").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionBump", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnTypeActivation.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains logging configuration information for an extension.

            :param log_group_name: The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.
            :param log_role_arn: The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloudformation as cloudformation
                
                logging_config_property = cloudformation.CfnTypeActivation.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(CfnTypeActivation.LoggingConfigProperty.__init__)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html#cfn-cloudformation-typeactivation-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html#cfn-cloudformation-typeactivation-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnTypeActivationProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_update": "autoUpdate",
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
        "major_version": "majorVersion",
        "public_type_arn": "publicTypeArn",
        "publisher_id": "publisherId",
        "type": "type",
        "type_name": "typeName",
        "type_name_alias": "typeNameAlias",
        "version_bump": "versionBump",
    },
)
class CfnTypeActivationProps:
    def __init__(
        self,
        *,
        auto_update: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[CfnTypeActivation.LoggingConfigProperty, typing.Dict[str, typing.Any]]]] = None,
        major_version: typing.Optional[builtins.str] = None,
        public_type_arn: typing.Optional[builtins.str] = None,
        publisher_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
        type_name_alias: typing.Optional[builtins.str] = None,
        version_bump: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnTypeActivation``.

        :param auto_update: Whether to automatically update the extension in this account and region when a new *minor* version is published by the extension publisher. Major versions released by the publisher must be manually updated. The default is ``true`` .
        :param execution_role_arn: The name of the IAM execution role to use to activate the extension.
        :param logging_config: Specifies logging configuration information for an extension.
        :param major_version: The major version of this extension you want to activate, if multiple major versions are available. The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected. You can specify ``MajorVersion`` or ``VersionBump`` , but not both.
        :param public_type_arn: The Amazon Resource Number (ARN) of the public extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param publisher_id: The ID of the extension publisher. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type: The extension type. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name: The name of the extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name_alias: An alias to assign to the public extension, in this account and region. If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console. An extension alias must be unique within a given account and region. You can activate the same public resource multiple times in the same account and region, using different type name aliases.
        :param version_bump: Manually updates a previously-activated type to a new major or minor version, if available. You can also use this parameter to update the value of ``AutoUpdate`` . - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available. - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_type_activation_props = cloudformation.CfnTypeActivationProps(
                auto_update=False,
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation.CfnTypeActivation.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                ),
                major_version="majorVersion",
                public_type_arn="publicTypeArn",
                publisher_id="publisherId",
                type="type",
                type_name="typeName",
                type_name_alias="typeNameAlias",
                version_bump="versionBump"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnTypeActivationProps.__init__)
            check_type(argname="argument auto_update", value=auto_update, expected_type=type_hints["auto_update"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument public_type_arn", value=public_type_arn, expected_type=type_hints["public_type_arn"])
            check_type(argname="argument publisher_id", value=publisher_id, expected_type=type_hints["publisher_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_name_alias", value=type_name_alias, expected_type=type_hints["type_name_alias"])
            check_type(argname="argument version_bump", value=version_bump, expected_type=type_hints["version_bump"])
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_update is not None:
            self._values["auto_update"] = auto_update
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if major_version is not None:
            self._values["major_version"] = major_version
        if public_type_arn is not None:
            self._values["public_type_arn"] = public_type_arn
        if publisher_id is not None:
            self._values["publisher_id"] = publisher_id
        if type is not None:
            self._values["type"] = type
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_name_alias is not None:
            self._values["type_name_alias"] = type_name_alias
        if version_bump is not None:
            self._values["version_bump"] = version_bump

    @builtins.property
    def auto_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''Whether to automatically update the extension in this account and region when a new *minor* version is published by the extension publisher.

        Major versions released by the publisher must be manually updated.

        The default is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-autoupdate
        '''
        result = self._values.get("auto_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to activate the extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnTypeActivation.LoggingConfigProperty]]:
        '''Specifies logging configuration information for an extension.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnTypeActivation.LoggingConfigProperty]], result)

    @builtins.property
    def major_version(self) -> typing.Optional[builtins.str]:
        '''The major version of this extension you want to activate, if multiple major versions are available.

        The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected.

        You can specify ``MajorVersion`` or ``VersionBump`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-majorversion
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the public extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publictypearn
        '''
        result = self._values.get("public_type_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the extension publisher.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publisherid
        '''
        result = self._values.get("publisher_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The extension type.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name_alias(self) -> typing.Optional[builtins.str]:
        '''An alias to assign to the public extension, in this account and region.

        If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console.

        An extension alias must be unique within a given account and region. You can activate the same public resource multiple times in the same account and region, using different type name aliases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typenamealias
        '''
        result = self._values.get("type_name_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_bump(self) -> typing.Optional[builtins.str]:
        '''Manually updates a previously-activated type to a new major or minor version, if available.

        You can also use this parameter to update the value of ``AutoUpdate`` .

        - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available.
        - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-versionbump
        '''
        result = self._values.get("version_bump")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTypeActivationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitCondition(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitCondition",
):
    '''A CloudFormation ``AWS::CloudFormation::WaitCondition``.

    .. epigraph::

       For Amazon EC2 and Auto Scaling resources, we recommend that you use a ``CreationPolicy`` attribute instead of wait conditions. Add a CreationPolicy attribute to those resources, and use the cfn-signal helper script to signal when an instance creation process has completed successfully.

    You can use a wait condition for situations like the following:

    - To coordinate stack resource creation with configuration actions that are external to the stack creation.
    - To track the status of a configuration process.

    For these situations, we recommend that you associate a `CreationPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html>`_ attribute with the wait condition so that you don't have to use a wait condition handle. For more information and an example, see `Creating wait conditions in a template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-waitcondition.html>`_ . If you use a CreationPolicy with a wait condition, don't specify any of the wait condition's properties.
    .. epigraph::

       If you use the `VPC endpoints <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html>`_ feature, resources in the VPC that respond to wait conditions must have access to CloudFormation , specific Amazon Simple Storage Service ( Amazon S3 ) buckets. Resources must send wait condition responses to a presigned Amazon S3 URL. If they can't send responses to Amazon S3 , CloudFormation won't receive a response and the stack operation fails. For more information, see `Setting up VPC endpoints for AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-vpce-bucketnames.html>`_ .

    :cloudformationResource: AWS::CloudFormation::WaitCondition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_wait_condition = cloudformation.CfnWaitCondition(self, "MyCfnWaitCondition",
            count=123,
            handle="handle",
            timeout="timeout"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::WaitCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param count: The number of success signals that CloudFormation must receive before it continues the stack creation process. When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back. Updates aren't supported.
        :param handle: A reference to the wait condition handle used to signal this wait condition. Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html>`_ resource. Anytime you add a WaitCondition resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command. Updates aren't supported.
        :param timeout: The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies. ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds). Updates aren't supported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnWaitCondition.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWaitConditionProps(count=count, handle=handle, timeout=timeout)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnWaitCondition.inspect)
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
            type_hints = typing.get_type_hints(CfnWaitCondition._render_properties)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrData")
    def attr_data(self) -> aws_cdk.core.IResolvable:
        '''A JSON object that contains the ``UniqueId`` and ``Data`` values from the wait condition signal(s) for the specified wait condition.

        For more information about wait condition signals, see `Wait condition signal JSON format <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-waitcondition.html#using-cfn-waitcondition-signaljson>`_ .

        Example return value for a wait condition with 2 signals:

        ``{ "Signal1" : "Step 1 complete." , "Signal2" : "Step 2 complete." }``

        :cloudformationAttribute: Data
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrData"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of success signals that CloudFormation must receive before it continues the stack creation process.

        When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "count"))

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnWaitCondition, "count").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="handle")
    def handle(self) -> typing.Optional[builtins.str]:
        '''A reference to the wait condition handle used to signal this wait condition.

        Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html>`_ resource.

        Anytime you add a WaitCondition resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handle"))

    @handle.setter
    def handle(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnWaitCondition, "handle").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handle", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[builtins.str]:
        '''The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies.

        ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds).

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CfnWaitCondition, "timeout").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitConditionHandle(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionHandle",
):
    '''A CloudFormation ``AWS::CloudFormation::WaitConditionHandle``.

    .. epigraph::

       For Amazon EC2 and Auto Scaling resources, we recommend that you use a ``CreationPolicy`` attribute instead of wait conditions. Add a ``CreationPolicy`` attribute to those resources, and use the cfn-signal helper script to signal when an instance creation process has completed successfully.

       For more information, see `Deploying applications on Amazon EC2 with AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/deploying.applications.html>`_ .

    The ``AWS::CloudFormation::WaitConditionHandle`` type has no properties. When you reference the ``WaitConditionHandle`` resource by using the Ref function, AWS CloudFormation returns a presigned URL. You pass this URL to applications or scripts that are running on your Amazon EC2 instances to send signals to that URL. An associated ``AWS::CloudFormation::WaitCondition`` resource checks the URL for the required number of success signals or for a failure signal.
    .. epigraph::

       Anytime you add a ``WaitCondition`` resource during a stack update or update a resource with a wait condition, you must associate the wait condition with a new ``WaitConditionHandle`` resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command. > Updates aren't supported for this resource.

    :cloudformationResource: AWS::CloudFormation::WaitConditionHandle
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        
        cfn_wait_condition_handle = cloudformation.CfnWaitConditionHandle(self, "MyCfnWaitConditionHandle")
    '''

    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        '''Create a new ``AWS::CloudFormation::WaitConditionHandle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnWaitConditionHandle.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnWaitConditionHandle.inspect)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionProps",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "handle": "handle", "timeout": "timeout"},
)
class CfnWaitConditionProps:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnWaitCondition``.

        :param count: The number of success signals that CloudFormation must receive before it continues the stack creation process. When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back. Updates aren't supported.
        :param handle: A reference to the wait condition handle used to signal this wait condition. Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html>`_ resource. Anytime you add a WaitCondition resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command. Updates aren't supported.
        :param timeout: The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies. ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds). Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            cfn_wait_condition_props = cloudformation.CfnWaitConditionProps(
                count=123,
                handle="handle",
                timeout="timeout"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CfnWaitConditionProps.__init__)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument handle", value=handle, expected_type=type_hints["handle"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if handle is not None:
            self._values["handle"] = handle
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of success signals that CloudFormation must receive before it continues the stack creation process.

        When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        '''A reference to the wait condition handle used to signal this wait condition.

        Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html>`_ resource.

        Anytime you add a WaitCondition resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command.

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        '''
        result = self._values.get("handle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies.

        ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds).

        Updates aren't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaitConditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudformation.CloudFormationCapabilities")
class CloudFormationCapabilities(enum.Enum):
    '''(deprecated) Capabilities that affect whether CloudFormation is allowed to change IAM resources.

    :deprecated: use ``core.CfnCapabilities``

    :stability: deprecated
    '''

    NONE = "NONE"
    '''(deprecated) No IAM Capabilities.

    Pass this capability if you wish to block the creation IAM resources.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    '''
    ANONYMOUS_IAM = "ANONYMOUS_IAM"
    '''(deprecated) Capability to create anonymous IAM resources.

    Pass this capability if you're only creating anonymous resources.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    '''
    NAMED_IAM = "NAMED_IAM"
    '''(deprecated) Capability to create named IAM resources.

    Pass this capability if you're creating IAM resources that have physical
    names.

    ``CloudFormationCapabilities.NamedIAM`` implies ``CloudFormationCapabilities.IAM``; you don't have to pass both.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    '''
    AUTO_EXPAND = "AUTO_EXPAND"
    '''(deprecated) Capability to run CloudFormation macros.

    Pass this capability if your template includes macros, for example AWS::Include or AWS::Serverless.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStack.html
    '''


class CustomResource(
    aws_cdk.core.CustomResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CustomResource",
):
    '''(deprecated) Deprecated.

    :deprecated: use ``core.CustomResource``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloudformation as cloudformation
        import aws_cdk.core as cdk
        
        # custom_resource_provider: cloudformation.CustomResourceProvider
        # properties: Any
        
        custom_resource = cloudformation.CustomResource(self, "MyCustomResource",
            provider=custom_resource_provider,
        
            # the properties below are optional
            properties={
                "properties_key": properties
            },
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type="resourceType"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        provider: "ICustomResourceProvider",
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param provider: (deprecated) The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: import * as custom_resources from '@aws-cdk/custom-resources'; import * as lambda from '@aws-cdk/aws-lambda'; import { Stack } from '@aws-cdk/core'; declare const myOnEventLambda: lambda.Function; declare const myIsCompleteLambda: lambda.Function; const stack = new Stack(); const provider = new custom_resources.Provider(stack, 'myProvider', { onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: import * as cloudformation from '@aws-cdk/aws-cloudformation'; import * as lambda from '@aws-cdk/aws-lambda'; declare const myFunction: lambda.Function; // invoke an AWS Lambda function when a lifecycle event occurs: const provider = cloudformation.CustomResourceProvider.fromLambda(myFunction); Example:: import * as cloudformation from '@aws-cdk/aws-cloudformation'; import * as sns from '@aws-cdk/aws-sns'; declare const myTopic: sns.Topic; // publish lifecycle events to an SNS topic: const provider = cloudformation.CustomResourceProvider.fromTopic(myTopic);
        :param properties: (deprecated) Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: (deprecated) The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: (deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CustomResourceProps(
            provider=provider,
            properties=properties,
            removal_policy=removal_policy,
            resource_type=resource_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "properties": "properties",
        "removal_policy": "removalPolicy",
        "resource_type": "resourceType",
    },
)
class CustomResourceProps:
    def __init__(
        self,
        *,
        provider: "ICustomResourceProvider",
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Properties to provide a Lambda-backed custom resource.

        :param provider: (deprecated) The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: import * as custom_resources from '@aws-cdk/custom-resources'; import * as lambda from '@aws-cdk/aws-lambda'; import { Stack } from '@aws-cdk/core'; declare const myOnEventLambda: lambda.Function; declare const myIsCompleteLambda: lambda.Function; const stack = new Stack(); const provider = new custom_resources.Provider(stack, 'myProvider', { onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: import * as cloudformation from '@aws-cdk/aws-cloudformation'; import * as lambda from '@aws-cdk/aws-lambda'; declare const myFunction: lambda.Function; // invoke an AWS Lambda function when a lifecycle event occurs: const provider = cloudformation.CustomResourceProvider.fromLambda(myFunction); Example:: import * as cloudformation from '@aws-cdk/aws-cloudformation'; import * as sns from '@aws-cdk/aws-sns'; declare const myTopic: sns.Topic; // publish lifecycle events to an SNS topic: const provider = cloudformation.CustomResourceProvider.fromTopic(myTopic);
        :param properties: (deprecated) Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: (deprecated) The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: (deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        :deprecated: use ``core.CustomResourceProps``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            import aws_cdk.core as cdk
            
            # custom_resource_provider: cloudformation.CustomResourceProvider
            # properties: Any
            
            custom_resource_props = cloudformation.CustomResourceProps(
                provider=custom_resource_provider,
            
                # the properties below are optional
                properties={
                    "properties_key": properties
                },
                removal_policy=cdk.RemovalPolicy.DESTROY,
                resource_type="resourceType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProps.__init__)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "provider": provider,
        }
        if properties is not None:
            self._values["properties"] = properties
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def provider(self) -> "ICustomResourceProvider":
        '''(deprecated) The provider which implements the custom resource.

        You can implement a provider by listening to raw AWS CloudFormation events
        through an SNS topic or an AWS Lambda function or use the CDK's custom
        `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust
        providers::

           import aws_cdk.custom_resources as custom_resources
           import aws_cdk.aws_lambda as lambda_
           from aws_cdk.core import Stack
           # my_on_event_lambda: lambda.Function
           # my_is_complete_lambda: lambda.Function
           stack = Stack()

           provider = custom_resources.Provider(stack, "myProvider",
               on_event_handler=my_on_event_lambda,
               is_complete_handler=my_is_complete_lambda
           )

        Example::

           import aws_cdk.aws_cloudformation as cloudformation
           import aws_cdk.aws_lambda as lambda_
           # my_function: lambda.Function

           # invoke an AWS Lambda function when a lifecycle event occurs:
           provider = cloudformation.CustomResourceProvider.from_lambda(my_function)

        Example::

           import aws_cdk.aws_cloudformation as cloudformation
           import aws_cdk.aws_sns as sns
           # my_topic: sns.Topic

           # publish lifecycle events to an SNS topic:
           provider = cloudformation.CustomResourceProvider.from_topic(my_topic)

        :stability: deprecated
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("ICustomResourceProvider", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(deprecated) Properties to pass to the Lambda.

        :default: - No properties.

        :stability: deprecated
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        '''(deprecated) The policy to apply when this resource is removed from the application.

        :default: cdk.RemovalPolicy.Destroy

        :stability: deprecated
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.core.RemovalPolicy], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''(deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name.

        For example, you can use "Custom::MyCustomResourceTypeName".

        Custom resource type names must begin with "Custom::" and can include
        alphanumeric characters and the following characters: _@-. You can specify
        a custom resource type name up to a maximum length of 60 characters. You
        cannot change the type during an update.

        Using your own resource type names helps you quickly differentiate the
        types of custom resources in your stack. For example, if you had two custom
        resources that conduct two different ping tests, you could name their type
        as Custom::PingTester to make them easily identifiable as ping testers
        (instead of using AWS::CloudFormation::CustomResource).

        :default: - AWS::CloudFormation::CustomResource

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#aws-cfn-resource-type-name
        :stability: deprecated
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"service_token": "serviceToken"},
)
class CustomResourceProviderConfig:
    def __init__(self, *, service_token: builtins.str) -> None:
        '''(deprecated) Configuration options for custom resource providers.

        :param service_token: (deprecated) The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        :deprecated: used in {@link ICustomResourceProvider} which is now deprecated

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloudformation as cloudformation
            
            custom_resource_provider_config = cloudformation.CustomResourceProviderConfig(
                service_token="serviceToken"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProviderConfig.__init__)
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[str, typing.Any] = {
            "service_token": service_token,
        }

    @builtins.property
    def service_token(self) -> builtins.str:
        '''(deprecated) The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        :stability: deprecated
        '''
        result = self._values.get("service_token")
        assert result is not None, "Required property 'service_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResourceProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloudformation.ICustomResourceProvider")
class ICustomResourceProvider(typing_extensions.Protocol):
    '''(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :deprecated: use ``core.ICustomResourceProvider``

    :stability: deprecated
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        '''(deprecated) Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        :return: provider configuration

        :stability: deprecated
        '''
        ...


class _ICustomResourceProviderProxy:
    '''(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :deprecated: use ``core.ICustomResourceProvider``

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudformation.ICustomResourceProvider"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        '''(deprecated) Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        :return: provider configuration

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ICustomResourceProvider.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(CustomResourceProviderConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICustomResourceProvider).__jsii_proxy_class__ = lambda : _ICustomResourceProviderProxy


class NestedStack(
    aws_cdk.core.NestedStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.NestedStack",
):
    '''(deprecated) A CloudFormation nested stack.

    When you apply template changes to update a top-level stack, CloudFormation
    updates the top-level stack and initiates an update to its nested stacks.
    CloudFormation updates the resources of modified nested stacks, but does not
    update the resources of unmodified nested stacks.

    Furthermore, this stack will not be treated as an independent deployment
    artifact (won't be listed in "cdk list" or deployable through "cdk deploy"),
    but rather only synthesized as a template and uploaded as an asset to S3.

    Cross references of resource attributes between the parent stack and the
    nested stack will automatically be translated to stack parameters and
    outputs.

    :deprecated: use core.NestedStack instead

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        class MyNestedStack(cfn.NestedStack):
            def __init__(self, scope, id, *, parameters=None, timeout=None, notifications=None):
                super().__init__(scope, id, parameters=parameters, timeout=timeout, notifications=notifications)
        
                s3.Bucket(self, "NestedBucket")
        
        class MyParentStack(Stack):
            def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        
                MyNestedStack(self, "Nested1")
                MyNestedStack(self, "Nested2")
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        notifications: typing.Optional[typing.Sequence[aws_cdk.aws_sns.ITopic]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param notifications: (deprecated) The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: (deprecated) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: (deprecated) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NestedStack.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NestedStackProps(
            notifications=notifications, parameters=parameters, timeout=timeout
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.NestedStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "notifications": "notifications",
        "parameters": "parameters",
        "timeout": "timeout",
    },
)
class NestedStackProps:
    def __init__(
        self,
        *,
        notifications: typing.Optional[typing.Sequence[aws_cdk.aws_sns.ITopic]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''(deprecated) Initialization props for the ``NestedStack`` construct.

        :param notifications: (deprecated) The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: (deprecated) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: (deprecated) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        :deprecated: use core.NestedStackProps instead

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            class MyNestedStack(cfn.NestedStack):
                def __init__(self, scope, id, *, parameters=None, timeout=None, notifications=None):
                    super().__init__(scope, id, parameters=parameters, timeout=timeout, notifications=notifications)
            
                    s3.Bucket(self, "NestedBucket")
            
            class MyParentStack(Stack):
                def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
            
                    MyNestedStack(self, "Nested1")
                    MyNestedStack(self, "Nested2")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NestedStackProps.__init__)
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {}
        if notifications is not None:
            self._values["notifications"] = notifications
        if parameters is not None:
            self._values["parameters"] = parameters
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]]:
        '''(deprecated) The Simple Notification Service (SNS) topics to publish stack related events.

        :default: - notifications are not sent for this stack.

        :stability: deprecated
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding
        to a parameter defined in the embedded template and a value representing
        the value that you want to set for the parameter.

        The nested stack construct will automatically synthesize parameters in order
        to bind references from the parent stack(s) into the nested stack.

        :default: - no user-defined parameters are passed to the nested stack

        :stability: deprecated
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(deprecated) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state.

        When CloudFormation detects that the nested stack has reached the
        CREATE_COMPLETE state, it marks the nested stack resource as
        CREATE_COMPLETE in the parent stack and resumes creating the parent stack.
        If the timeout period expires before the nested stack reaches
        CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls
        back both the nested stack and parent stack.

        :default: - no timeout

        :stability: deprecated
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NestedStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICustomResourceProvider)
class CustomResourceProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProvider",
):
    '''(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :deprecated: use core.CustomResource instead

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_cloudformation as cloudformation
        import aws_cdk.aws_lambda as lambda_
        # my_function: lambda.Function
        
        # invoke an AWS Lambda function when a lifecycle event occurs:
        provider = cloudformation.CustomResourceProvider.from_lambda(my_function)
    '''

    @jsii.member(jsii_name="fromLambda")
    @builtins.classmethod
    def from_lambda(
        cls,
        handler: aws_cdk.aws_lambda.IFunction,
    ) -> "CustomResourceProvider":
        '''(deprecated) The Lambda provider that implements this custom resource.

        We recommend using a lambda.SingletonFunction for this.

        :param handler: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProvider.from_lambda)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        return typing.cast("CustomResourceProvider", jsii.sinvoke(cls, "fromLambda", [handler]))

    @jsii.member(jsii_name="fromTopic")
    @builtins.classmethod
    def from_topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        '''(deprecated) The SNS Topic for the provider that implements this custom resource.

        :param topic: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProvider.from_topic)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        return typing.cast("CustomResourceProvider", jsii.sinvoke(cls, "fromTopic", [topic]))

    @jsii.member(jsii_name="lambda")
    @builtins.classmethod
    def lambda_(cls, handler: aws_cdk.aws_lambda.IFunction) -> "CustomResourceProvider":
        '''(deprecated) Use AWS Lambda as a provider.

        :param handler: -

        :deprecated: use ``fromLambda``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProvider.lambda_)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        return typing.cast("CustomResourceProvider", jsii.sinvoke(cls, "lambda", [handler]))

    @jsii.member(jsii_name="topic")
    @builtins.classmethod
    def topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        '''(deprecated) Use an SNS topic as the provider.

        :param topic: -

        :deprecated: use ``fromTopic``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProvider.topic)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        return typing.cast("CustomResourceProvider", jsii.sinvoke(cls, "topic", [topic]))

    @jsii.member(jsii_name="bind")
    def bind(self, _: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        '''(deprecated) Called when this provider is used by a ``CustomResource``.

        :param _: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomResourceProvider.bind)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(CustomResourceProviderConfig, jsii.invoke(self, "bind", [_]))

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''(deprecated) the ServiceToken which contains the ARN for this provider.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))


__all__ = [
    "CfnCustomResource",
    "CfnCustomResourceProps",
    "CfnHookDefaultVersion",
    "CfnHookDefaultVersionProps",
    "CfnHookTypeConfig",
    "CfnHookTypeConfigProps",
    "CfnHookVersion",
    "CfnHookVersionProps",
    "CfnMacro",
    "CfnMacroProps",
    "CfnModuleDefaultVersion",
    "CfnModuleDefaultVersionProps",
    "CfnModuleVersion",
    "CfnModuleVersionProps",
    "CfnPublicTypeVersion",
    "CfnPublicTypeVersionProps",
    "CfnPublisher",
    "CfnPublisherProps",
    "CfnResourceDefaultVersion",
    "CfnResourceDefaultVersionProps",
    "CfnResourceVersion",
    "CfnResourceVersionProps",
    "CfnStack",
    "CfnStackProps",
    "CfnStackSet",
    "CfnStackSetProps",
    "CfnTypeActivation",
    "CfnTypeActivationProps",
    "CfnWaitCondition",
    "CfnWaitConditionHandle",
    "CfnWaitConditionProps",
    "CloudFormationCapabilities",
    "CustomResource",
    "CustomResourceProps",
    "CustomResourceProvider",
    "CustomResourceProviderConfig",
    "ICustomResourceProvider",
    "NestedStack",
    "NestedStackProps",
]

publication.publish()
