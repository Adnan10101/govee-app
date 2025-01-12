#!/bin/bash

echo "Building docker image...."
echo "Enter version...."
read DOCKER_IMAGE_TAG
DOCKER_IMAGE_NAME="govee-control-system"
DOCKER_REGISTRY="adnan10101"
DEPLOYMENT="govee-app"

sudo docker build --no-cache -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .


echo "Pushing docker image to repo......"
sudo docker login
sudo docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG  $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG
sudo docker push $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG

echo "Govee deployment already exists.....?"
if kubectl get deployment $DEPLOYMENT > /dev/null 2>&1; then
    echo "Govee exists, deleting....."
    kubectl delete deployment $DEPLOYMENT 
    if [ $? -ne 0 ]; then
        echo "Failed to delete deployment. Exiting."
        exit 1
  fi
else
  echo "Deployment does not exist."
fi

#sed -i "s|image: $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:.*|image: $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$NEW_TAG|g" deploy/deployment.yaml
# this line to change the tag version of the dpeloyment.yaml file dynamically
#echo "Creating deployment......"
#kubectl create -f deploy/deployment.yaml


