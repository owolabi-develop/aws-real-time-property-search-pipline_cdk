import aws_cdk as core
import aws_cdk.assertions as assertions

from real_time_property_search.real_time_property_search_stack import RealTimePropertySearchStack

# example tests. To run these tests, uncomment this file along with the example
# resource in real_time_property_search/real_time_property_search_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RealTimePropertySearchStack(app, "real-time-property-search")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
