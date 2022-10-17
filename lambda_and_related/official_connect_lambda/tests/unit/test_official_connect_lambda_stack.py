import aws_cdk as core
import aws_cdk.assertions as assertions

from official_connect_lambda.official_connect_lambda_stack import OfficialConnectLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in official_connect_lambda/official_connect_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OfficialConnectLambdaStack(app, "official-connect-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
