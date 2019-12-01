# ecs-flask
Learning - getting flask app to work on AWS using ECS

## deploying

Follow steps in this link to test https://linuxacademy.com/blog/linux-academy/deploying-a-containerized-flask-application-with-aws-ecs-and-docker/

docker build -t flask-ecs-demo .

docker run -p 80:80 flask-ecs-demo

docker tag flask-ecs-demo:latest 782247268784.dkr.ecr.eu-west-2.amazonaws.com/flask-ecs-demo

docker push 782247268784.dkr.ecr.eu-west-2.amazonaws.com/flask-ecs-demo

## testing 

    import requests
    data = {'Price Grade': 1.0,
 'Face Value': 1.0,
 'Advance': 1.0,
 'Advance %': 1.0,
 'Discount %': 1.0,
 'Outstanding Principal': 1.0,
 'Face Value (GBP)': 1.0,
 'Advance (GBP)': 1.0,
 'Outstanding Principal (GBP)': 1.0,
 'Annualised Gross Yield %': 1.0,
 'expected_duration': 1.0,
 'prev_settles': 1.0,
 'Currency_EUR': 1.0,
 'Currency_GBP': 1.0,
 'Currency_USD': 1.0,
 'Discount On (Advance or Face Value)_Advance': 1.0,
 'Discount On (Advance or Face Value)_Facevalue': 1.0}
 
   payload = {'model_features':data}  
   
   r2 = requests.post('http://18.130.191.184/score', json=payload)          
   r2.text # should give you model score

