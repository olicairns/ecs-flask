# ECS demo

Example of deploying machine learning model API on AWS using docker+flask+nginx+conda

Based on these resources:

https://linuxacademy.com/blog/linux-academy/deploying-a-containerized-flask-application-with-aws-ecs-and-docker/

https://github.com/cameroncruz/flask-nginx-uwsgi-miniconda

## prerequestites

Conda - https://docs.conda.io/projects/conda/en/latest/user-guide/install/

Docker - https://docs.docker.com/docker-for-mac/install/

AWS - https://aws.amazon.com/

AWS cli - https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html

## rebuild model

Fits classifier based on bin/market-invoice-data.csv & saves model binary as .pkl file

Also fits 'Shap' explainer, that can explain feature impacts on model prediction, also saving as pkl.
    conda config --add channels conda-forge \
    conda env create -n ecsdemo -f environment.yml 
    conda activate ecsdemo
    python3 src/model/fit_model.py

TODO - add custom sklearn transformer to demo


## rebuild and run docker image locally

build a livescoring API as docker image (flask+nginx+conda)
    docker build -t oli5679/ecsdemo .
    docker run  -p 80:80 oli5679/ecsdemo

TODO - get gunicorn working on ecs

TODO - add NGINX

## test local api
post to localhost:80/score to test live scoring

body

    {"model_inputs": {"Price Grade": 6.0, "Face Value": 18318.0, "Advance": 16486.2, "Advance %": 90.0, "Discount %": 1.0,
    "Outstanding Principal": 0.0, "Face Value (GBP)": 18318.0, "Advance (GBP)": 16486.2, "Outstanding Principal (GBP)": 0.0,
    "Annualised Gross Yield %": 14.164038846995776, "expected_duration": 31, "prev_settles": 0, "Currency_EUR": 0,
    "Currency_GBP": 1, "Currency_USD": 0, "Discount On (Advance or Face Value)_Advance": 0, "Discount On (Advance or Face
    Value)_Facevalue": 1}, "model_score": 0.06014613151916984, "date_time": 1576418241.493108}

## push to ECR
setup AWS cli, look up account id and then run the following commands

    aws ecr create-repository --repository-name flask-ecs-demo

    aws ecr get-login --region eu-west-2 --no-include-email

[run the login snippet]

[replace with actual account id]

    docker tag oli5679/ecsdemo:latest 782247268784.dkr.ecr.eu-west-2.amazonaws.com/flask-ecs-demo

    docker push 782247268784.dkr.ecr.eu-west-2.amazonaws.com/flask-ecs-demo

TODO - investigate adding unit tests + Jenkins build pipeline 

## deploy app on ECS

follow step 4 and onwards from here https://linuxacademy.com/blog/linux-academy/deploying-a-containerized-flask-application-with-aws-ecs-and-docker/


TODO - investigate automating with teraform/jenkins, and also increasign security/IAM

TODO - investigate autoscaling and logging

TODO - investigate eks

## test app 

lookup url on ECS console, and post to url + /score

body

    {"model_inputs": {"Price Grade": 6.0, "Face Value": 18318.0, "Advance": 16486.2, "Advance %": 90.0, "Discount %": 1.0,
    "Outstanding Principal": 0.0, "Face Value (GBP)": 18318.0, "Advance (GBP)": 16486.2, "Outstanding Principal (GBP)": 0.0,
    "Annualised Gross Yield %": 14.164038846995776, "expected_duration": 31, "prev_settles": 0, "Currency_EUR": 0,
    "Currency_GBP": 1, "Currency_USD": 0, "Discount On (Advance or Face Value)_Advance": 0, "Discount On (Advance or Face
    Value)_Facevalue": 1}, "model_score": 0.06014613151916984, "date_time": 1576418241.493108}

## other useful resources

https://www.bogotobogo.com/DevOps/Docker/Docker-Flask-ALB-ECS.php

https://towardsdatascience.com/how-to-do-rapid-prototyping-with-flask-uwsgi-nginx-and-docker-on-openshift-f0ef144033cb

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04

https://aws.amazon.com/blogs/devops/set-up-a-build-pipeline-with-jenkins-and-amazon-ecs/