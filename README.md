# PIRI: Atención prenatal, apoyo total.

Tu acompañante en la maternidad en WhatsApp y Telegram: pregunta, conversa y monitorea.

<div style="text-align: center;">
  <img src="images/piri.png" width="400px">
</div>

## Arquitectura de solución

<div style="text-align: center;">
  <img src="images/solution.png">
</div>

## Deployment

El despliegue de la aplicación en AWS se realizó utilizando AWS CDK, definiendo la infraestructura como código. Los pasos principales incluyen la inicialización del proyecto, instalación de dependencias, empaquetado de la función Lambda y despliegue en la nube.

Comandos clave:

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

## Demo

<div style="text-align: center;">
  <img src="images/demo1.jpg" width="300px" style="margin: 10px;">
  <img src="images/demo2.jpg" width="300px" style="margin: 10px;">
</div>