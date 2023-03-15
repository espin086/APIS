#!/usr/bin/env python3

import aws_cdk as cdk

from api_detect_language.api_detect_language_stack import ApiDetectLanguageStack


app = cdk.App()
ApiDetectLanguageStack(app, "api-detect-language")

app.synth()
