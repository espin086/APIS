#!/usr/bin/env python3

import aws_cdk as cdk

from api_text_talking_points.api_text_talking_points_stack import ApiTextTalkingPointsStack


app = cdk.App()
ApiTextTalkingPointsStack(app, "api-text-talking-points")

app.synth()
