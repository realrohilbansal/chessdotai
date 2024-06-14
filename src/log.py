import json
import mlflow

# Start MLflow run
def startrun(experiment_name = "Chess0", artifact_location = "chessexperiment0_artifacts"):
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name, artifact_location)
    else:
        experiment_id = experiment.experiment_id
    
    runs = mlflow.search_runs(experiment_id)
    total_runs = runs.shape[0]
    run_name = f'Run{total_runs + 1}'
        
    mlflow.start_run(experiment_id=experiment_id, run_name=run_name)
  
def getexperiment(experiment_id: str=None, experiment_name:str=None):
    if experiment_id is not None:
        experiment = mlflow.get_experiment(experiment_id)
    elif experiment_name is not None:
        experiment = mlflow.get_experiment_by_name(experiment_name)
    else:
        raise ValueError("Either Experiment ID or Experiment Name must be provided.")
    
    print("Name: ", experiment.name)
    print("ID: ", experiment.experiment_id)
    print("Artifact location: ", experiment.artifact_location)
    # print("Tags: ", experiment.tags)
    print("Creation timestamp: ", experiment.creation_time)
    print("Lifecycle stage: ", experiment.lifecycle_stage)
    
    return experiment

# Log game parameters
def logparams(params):
    mlflow.log_param("game params", json.dumps(params))

# Define a function to calculate and log average move time
def logmetrics(move_times, game_time):
    # Calculate average move time
    average_move_time = sum(move_times) / len(move_times)
    # Log average move time
    mlflow.log_metric("average_move_time", average_move_time)
    # Calculate total game time
    mlflow.log_metric("game_runtime", game_time)


# End MLflow run
def endrun():
    mlflow.end_run()