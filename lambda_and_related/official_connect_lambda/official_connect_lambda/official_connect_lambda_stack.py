from aws_cdk import core as cdk
from aws_cdk import aws_lambda
# from aws_cdk.aws_apigatewayv2_integrations  import LambdaProxyIntegration
from aws_cdk.aws_apigatewayv2 import HttpApi,HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

from constructs import Construct
class OfficialConnectLambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        python_runtime = aws_lambda.Runtime(
            "python3.14", aws_lambda.RuntimeFamily.PYTHON
        )
        result_lambda = aws_lambda.Function(
        self,"Results",code=aws_lambda.Code.from_asset("./compute/"),handler="result_function.lambda_handler",runtime=python_runtime)
        result_integration = HttpLambdaIntegration(
            "Result",
            handler = result_lambda
        )
        result_http_api = HttpApi(self, "ResultsApi")
        result_http_api.add_routes(path='/result',methods=[HttpMethod.ANY],integration=result_integration)

        sis_lambda = aws_lambda.Function(
        self,"sis",code=aws_lambda.Code.from_asset("./compute/"),handler="sis.lambda_handler",
        runtime=python_runtime,
        timeout=cdk.Duration.seconds(60),memory_size=512)
        sis_integration = HttpLambdaIntegration(
            "sis",
            handler = sis_lambda
        )
        sis_http_api = HttpApi(self, "sisScraperApi")
        sis_http_api.add_routes(path='/sis',methods=[HttpMethod.ANY],integration=sis_integration)

        proctor_lambda = aws_lambda.Function(
        self,"Proctor",code=aws_lambda.Code.from_asset("./compute/"),handler="proctor_functions.lambda_handler",runtime=python_runtime)
        proctor_integration = HttpLambdaIntegration(
            "proctor",
            handler = proctor_lambda
        )
        proctor_http_api = HttpApi(self, "ProctorApi")
        proctor_http_api.add_routes(path='/proctor',methods=[HttpMethod.ANY],integration=proctor_integration)
