
# PIRI

```shell
cdk init app --language python
./.venv/Scripts/activate
pip install -r requirements.txt
pip install aws-cdk-lib constructs aws-cdk.aws-lambda aws-cdk.aws-apigateway
cd lambda
pip install -r requirements.txt -t .
cd ..
cdk synth
cdk deploy
```