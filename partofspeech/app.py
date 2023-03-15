#!/usr/bin/env python3

import aws_cdk as cdk

from api_part_of_speech.api_part_of_speech_stack import ApiPartOfSpeechStack


app = cdk.App()
ApiPartOfSpeechStack(app, "api-part-of-speech")

app.synth()
