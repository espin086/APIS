# APIS

A collection of small serverless APIs deployed to AWS with the CDK. Right now the repo holds
one API: **Talking Points**, an HTTP endpoint that takes a chunk of text and returns the key
phrases in it using Amazon Comprehend. The idea is that each API lives in its own subfolder
with its own CDK app, requirements, and Lambda handler, so they deploy and version
independently.

The Talking Points API is published on RapidAPI:
https://rapidapi.com/jjespinozala/api/text-talking-point-api

## Features

- One CDK stack per API, self-contained in its own folder.
- `talkingpoints`: API Gateway REST API in front of a Python Lambda that calls
  `comprehend:DetectKeyPhrases` and returns the raw Comprehend response as JSON.
- IAM group, IAM user, and an inline Lambda role policy defined in the stack.
- pytest unit tests that assert against the synthesized CloudFormation template.

## Requirements

- Python 3 (the Lambda runtime is pinned to Python 3.7 in the stack).
- AWS CDK v2 CLI (`npm install -g aws-cdk`).
- AWS credentials with permission to deploy Lambda, API Gateway, and IAM resources.
- Python packages from `talkingpoints/requirements.txt`: `aws-cdk-lib==2.44.0`,
  `constructs>=10.0.0,<11.0.0`. Dev extras in `requirements-dev.txt`: `pytest==6.2.5`.

Comprehend is called with a hard-coded `region_name='us-east-1'` in the Lambda, so the API
talks to Comprehend in us-east-1 regardless of where the stack itself is deployed.

## Installation

```bash
git clone https://github.com/espin086/APIS.git
cd APIS/talkingpoints

python3 -m venv .venv
source .venv/bin/activate        # Windows: source.bat
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Usage

Everything runs from inside `talkingpoints/`.

```bash
cdk synth                # emit the CloudFormation template
cdk diff                 # compare against what is deployed
cdk bootstrap            # once per account/region
cdk deploy               # deploy the stack
cdk destroy              # tear it down
```

Run the tests:

```bash
pytest unit
```

Call the deployed endpoint. The Lambda reads the text from the `text` query string
parameter:

```bash
curl "https://<api-id>.execute-api.<region>.amazonaws.com/prod/?text=Amazon%20Comprehend%20finds%20key%20phrases%20in%20text"
```

Response body:

```json
{
  "text ": "Amazon Comprehend finds key phrases in text",
  "talking_points ": { "KeyPhrases": [ ... ], "ResponseMetadata": { ... } }
}
```

Both JSON keys have a trailing space in the name, which is what the handler writes today.

There are no environment variables. Language is fixed to `en` by the
`detect_talking_points(text, language_code='en')` default, and nothing in the handler
overrides it.

## Project structure

```
README.md                                   this file
talkingpoints/                              the Talking Points API
├── app.py                                  CDK entry point, instantiates the stack
├── cdk.json                                tells the CDK to run `python3 app.py`
├── api_text_talking_points_stack.py        the stack: Lambda, API Gateway, IAM
├── lambda/
│   └── api_text_talking_points.py          handler, calls Comprehend DetectKeyPhrases
├── unit/
│   └── test_api_text_talking_points_stack.py  template assertions
├── requirements.txt                        CDK runtime deps
├── requirements-dev.txt                    pytest
├── source.bat                              Windows venv activation helper
├── .gitignore
└── README.md                               link to the RapidAPI listing
```

## How it works

`cdk.json` points the CDK CLI at `app.py`, which builds one `ApiTextTalkingPointsStack`. The
stack creates:

1. An IAM group and an IAM user, with the user added to the group. Neither is attached to the
   Lambda; they look like leftovers from earlier work on the stack.
2. A Lambda function on the Python 3.7 runtime, with code bundled from the `lambda/` folder
   and `api_text_talking_points.lambda_handler` as the entry point.
3. An inline policy on the Lambda role allowing `comprehend:DetectKeyPhrases` and
   `execute-api:*` on `*`.
4. A `LambdaRestApi` that proxies every API Gateway request to the Lambda.

The handler logs the raw event, pulls `event["queryStringParameters"]["text"]`, calls
`comprehend.detect_key_phrases`, and returns the full boto3 response inside a 200 JSON body.
There is no error handling, so a request without a `text` parameter raises and API Gateway
returns a 502.

## Known rough edges

- `app.py` and the unit test import from `api_text_talking_points.api_text_talking_points_stack`,
  but the module actually sits at `talkingpoints/api_text_talking_points_stack.py`. As checked
  in, `cdk synth` and `pytest` will fail on the import until the package path is fixed.
- The unit tests assert that an SQS queue and an SNS topic exist. The stack creates neither.
  These are the tests from the `cdk init` template and were never updated.
- A comment in the stack says "add Rekognition permissions"; the policy actually grants
  Comprehend.

No LICENSE file is checked in.
