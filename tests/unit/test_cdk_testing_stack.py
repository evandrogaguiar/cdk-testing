import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from cdk_testing.cdk_testing_stack import CdkTestingStack
from aws_cdk.assertions import Match, Capture


@pytest.fixture(scope="session")
def simple_template():
    app = core.App()
    stack = CdkTestingStack(app, "cdk-testing")
    template = assertions.Template.from_stack(stack)
    return template


def test_lambda_props(simple_template):
    simple_template.has_resource_properties(
        "AWS::Lambda::Function", {"Runtime": "python3.11"}
    )
    simple_template.resource_count_is("AWS::Lambda::Function", 1)


def test_lambda_runtime_with_matcher(simple_template):
    simple_template.has_resource_properties(
        "AWS::Lambda::Function", {"Runtime": Match.string_like_regexp("python")}
    )


def test_lambda_bucket_with_matchers(simple_template):
    simple_template.has_resource_properties(
        "AWS::IAM::Policy",
        Match.object_like(
            {
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Resource": [
                                {
                                    "Fn::GetAtt": [
                                        Match.string_like_regexp("SimpleBucket"),
                                        "Arn",
                                    ]
                                },
                                Match.any_value(),
                            ]
                        }
                    ]
                }
            }
        ),
    )


def test_lambda_actions_with_captors(simple_template):
    lambda_actions_captor = Capture()
    simple_template.has_resource_properties(
        "AWS::IAM::Policy",
        {"PolicyDocument": {"Statement": [{"Action": lambda_actions_captor}]}},
    )

    excepted_actions = ["s3:GetBucket*", "s3:GetObject*", "s3:List*"]

    assert sorted(lambda_actions_captor.as_array()) == sorted(excepted_actions)


def test_bucket_props_with_snapshot(simple_template, snapshot):
    bucket_template = simple_template.find_resources("AWS::S3::Bucket")
    assert bucket_template == snapshot
