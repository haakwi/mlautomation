from mlflow.tracking import MlflowClient



def get_client(): 
    return MlflowClient(tracking_uri="http://host.docker.internal:5000", registry_uri="http://host.docker.internal:5000")

def create_run(experiment_id: str):
    # Create a run with a tag under the default experiment (whose id is '0').
    tags = {"engineering": "ML Platform"}
    client = get_client()
    run = client.create_run(experiment_id, tags=tags)

    # Show newly created run metadata info
    print("Run tags: {}".format(run.data.tags))
    print("Experiment id: {}".format(run.info.experiment_id))
    print("Run id: {}".format(run.info.run_id))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
    print("status: {}".format(run.info.status))    

def create_experiment():
    # Create an experiment with a name that is unique and case sensitive.
    client = get_client()
    experiment_id = client.create_experiment(name="Mlflow Example")
    client.set_experiment_tag(experiment_id, "nlp.framework", "Mlflow Example")

    # Fetch experiment metadata information
    experiment = client.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

create_run(experiment_id="2")
# create_experiment()
