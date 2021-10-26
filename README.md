# Introduction :brain:
![image](https://github.com/haakwi/mlautomation/blob/master/diagram/1_Technologie%20Overview%20%E2%80%93%20Continuous%20Deployment%20ML%20Model.png?raw=true)

This repository contains the current state of the art contionous delivery approaches for machine learning models.

Machine Learning models are managed via [MLflow](https://mlflow.org/) and deployed to [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) by using [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/index.html). 
 

MLflow Projects are trained on Kubernetes. Different hardware like GPU, CPU or Memory for specific model training needs can be choosen using the declarative Kubernetes configuration capabilities. For more details please refer to https://www.mlflow.org/docs/latest/projects.html#kubernetes-execution. 

# ML Model to Build :bricks:

<kbd>
  <img src="https://github.com/haakwi/mlautomation/blob/master/diagram/2_SD%20-%20ML%20Model%20Build.svg">
</kbd>
</br>

---
**GitHubAction workflows is available [Pipeline] : mlflow-build.yml**
***

This workflow runs on every push to the main branch. MLflow supports the already mentioned Kubernetes based model trainings. This workflow runs the mlflow run command with Kubernetes as backend. For further details on how this works in detail please refer to the official documentation in https://www.mlflow.org/docs/latest/projects.html#kubernetes-execution.

Most importantly the workflow delegates the training of the model to Kubernetes by using a Kubernetes Job and finishes after it applied the Job configuration. This process takes at most 2 minutes. Where as the training is supposed to take, depending of the complexity and data size, by far longer. The Kubernetes Job reports the model training result to MLflow server.

---


# ML Model to Production :parachute:

<kbd>
  <img src="https://github.com/haakwi/mlautomation/blob/master/diagram/3_SD%20-%20ML%20Model%20Production.svg">
</kbd>

---
**GitHubAction workflows is available [Pipeline] : mlflow-production.yml**
***

This workflow loads the latest model from the MLFlow Server and executes the Kubernetes deployment defined in deployment/seldon_deployment.yml. As of today MLflow server does not provide any eventing for stage transitions (https://github.com/mlflow/mlflow/issues/2383), therefore the workflow runs every minute. Kubernetes by default schedules a deployment only when a change in the configuration is made. Hence, executing the workflow multiple times does not have any affect as long as there are no new "Production" models available.

---


# Showcase :tv:

<table>
  <tr>
     <td>1. ML Model - Build</td>
     <td>2. ML Model - Production</td>
     <td>3. ML Model - Load Test & Monitoring</td>
  </tr>
  <tr>
    <td><img src="https://github.com/haakwi/mlautomation/blob/master/showcase/1%20-%20ML%20Model%20-%20Build%20-%20Cover.png" ></td>
    <td><img src=https://github.com/haakwi/mlautomation/blob/master/showcase/2%20-%20ML%20Model%20-%20Production%20-%20Cover.png ></td>
    <td><img src=https://github.com/haakwi/mlautomation/blob/master/showcase/3%20-%20ML%20Model%20-%20Load%20Test%20%26%20Monitoring%20-%20Cover.png ></td>
  </tr>
 </table>

**Showcases are stored here:  [mlautomation/showcase/](https://github.com/haakwi/mlautomation/tree/master/showcase)**



# Installation :rocket:

This installation is tested on GKE. There are no custom GKE resources used so that it should work on different Kubernetes installations as well.
To execute the installation as described below, it is assumed that an GKE instance is already available to use.

The installation files for the core components MLFlow, Seldon and Seldon Analytics is located in `infrastructure_installation`.

<table>
    <tr>
    <td>Steps</td>
    <td>Description</td>
  </tr>
  <tr>
     <td>1. Create namespaces</td>
     <td>`kubectl apply -f ./infrastructure_installation/kubernetes/1_namespaces.yml`

This will create all required kubernetes namespaces. Those are:
   - ambassador    - This namespace is for the Ambassador LoadBalancer
   - seldon-system - This namespace is for the seldon core components 
   - seldon        - This namespace is for the custom seldon based ML Models
   - mlflow        - This namespace is for the self hosted MLFlow Server
</td>
  </tr>
  <tr>
    <td>2. Install ambassador </td>
    <td>    
     `
    helm repo add datawire https://www.getambassador.io
    helm install ambassador datawire/ambassador \
      --set image.repository=docker.io/datawire/ambassador \
      --set enableAES=false \
      --set crds.keep=false \
      --namespace ambassador
    `
     </td>
  </tr>
  <tr>
    <td>3. Install seldon core and seldon analytics</td>
    <td>
         `
    helm install seldon-core seldon-core-operator \
        --repo https://storage.googleapis.com/seldon-charts \
        --set usageMetrics.enabled=true \
        --namespace seldon-system \
        --set ambassador.enabled=true
    `
    `
    helm install seldon-core-analytics seldon-core-analytics \
        --repo https://storage.googleapis.com/seldon-charts \
        --namespace seldon-system
    `
</td>
  </tr>
   <tr>
    <td>4. Create seldon ambassador routes</td>
    <td>  `kubectl apply -f ./infrastructure_installation/kubernetes/2_seldon_monitoring_route.yml` </td>
  </tr>
   <tr>
    <td>5. Install MLFlow server</td>
    <td>  `kubectl apply -f ./infrastructure_installation/kubernetes/3_mlflow_server.yml`
  
  MLFlow does not provide a official docker image. A custom build image is used for the deployment. The image can be found here:
  https://hub.docker.com/layers/akhuy/mlflow/1.20.2/images/sha256-08c69813acd510148f44119351dd26348ba8675b083349262fad84eb4021679b?context=repo

</td>
  </tr>
      <tr>
    <td>6. Lookup the public IP Address and validate the installation</td>
    <td> 
         `kubectl get svc -n ambassador -o jsonpath='{.items[*].status.loadBalancer.ingress[*].ip}'`
  
  This command returns the IP address from which the deployment is accessible.
  Copy the IP and enter the following to a Browser:
    `http://IP_ADDRESS/mlflow`
  This will open the MLflow UI.

</td>
  </tr>
 </table>

# Accessing deployed models :boom:

The API of a deployed model can be accessed via:  **http://IP_ADDRESS/seldon/seldon/iris-model/api/v1.0/doc/**

[Link to Seldon Core Documentation](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/serving.html)
