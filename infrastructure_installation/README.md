# Installations

## Helm
`
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
`

## Ambassador
helm repo add datawire https://www.getambassador.io
helm install ambassador datawire/ambassador \
  --set image.repository=docker.io/datawire/ambassador \
  --set enableAES=false \
  --set crds.keep=false \
  --namespace ambassador

## Seldon
`
kubectl config set-context --current --namespace=seldon-system

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --namespace seldon-system \
    --set ambassador.enabled=true
`
### Analytics
`
helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system
`

## Google Cloud
`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk

`

## MLFlow

`
cd mlflow
docker build -t mlflow:test-0.0.1 .

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root gs://mlopshhz --host 0.0.0.0


`

## Kubernetes URL

http://35.241.233.235/mlflow/#/

http://35.241.233.235/seldon/seldon/iris-model/api/v1.0/doc/#/%23
