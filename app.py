#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_testing.cdk_testing_stack import CdkTestingStack
from cdk_testing.policy_checker import PolicyChecker


app = cdk.App()
others_stack = CdkTestingStack(app, "CdkTestingStack")

cdk.Tags.of(others_stack).add("stage", "test")

cdk.Tags.of(others_stack).add(
    "storage", "main", include_resource_types=["AWS::S3::Bucket"]
)

cdk.Aspects.of(app).add(PolicyChecker())


app.synth()
