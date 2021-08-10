import json
import kfp
import kfp.dsl as dsl
import kfp.compiler as compiler
from kfp import components
from kubernetes import client as k8s_client

import os
import json
import kfp
import string
import random
import kfp.dsl as dsl
import kfp.compiler as compiler
from kfp import components
from kubernetes import client as k8s_client

dkube_preprocessing_op      = components.load_component_from_url("https://github.com/hemanthravi/dkube-examples/blob/sklearn/kubeflow/pipeline/preprocess.yaml")
dkube_training_op           = components.load_component_from_url("https://github.com/hemanthravi/dkube-examples/blob/sklearn/kubeflow/pipeline/training.yaml")
dkube_serving_op            = components.load_component_from_url("https://github.com/hemanthravi/dkube-examples/blob/sklearn/kubeflow/pipeline/serving.yaml")

image = "docker.io/ocdr/d3-datascience-sklearn:v0.23.2"
serving_image = "ocdr/sklearnserver:0.23.2"
dataset = 'insurance'
featureset = 'insurance-fs'
training_program = 'insurance'
model = 'insurance'
preprocessing_script = f"python insurance/preprocessing.py --fs {featureset}"
training_script = f"python insurance/training.py --fs {featureset}"
transformer_code='insurance/transformer.py'
user = os.getenv('USERNAME')
framework = "sklearn"
f_version = "0.23.2"
input_mount_point = "/opt/dkube/in"
output_mount_point = "/opt/dkube/out"

@kfp.dsl.pipeline(
    name='dkube-insurance-pl',
    description='sample insurance pipeline with featuresets'
)
def insurance_pipeline(token):
    
    preprocessing = dkube_preprocessing_op(auth_token = token,container=json.dumps({"image": image}),
                                           program=training_program, run_script=preprocessing_script,
                                           datasets=json.dumps([dataset]), 
                                           output_featuresets=json.dumps([str(featureset)]),
                                           input_dataset_mounts=json.dumps([input_mount_point]), 
                                           output_featureset_mounts=json.dumps([output_mount_point])
                                            )

    train       = dkube_training_op(auth_token = token,container=json.dumps({"image": image}),
                                    framework=framework, version=f_version,
                                    program=training_program, run_script=training_script,
                                    featuresets=json.dumps([featureset]), outputs=json.dumps([model]),
                                    input_featureset_mounts=json.dumps([input_mount_point]),
                                    output_mounts=json.dumps([output_mount_point])).after(preprocessing)

    serving     = dkube_serving_op(auth_token = token,model=train.outputs['artifact'], device='cpu', 
                                    serving_image=json.dumps({"image": serving_image}),
                                    transformer_image=json.dumps({"image": image}),
                                    transformer_project=training_program,
                                    transformer_code=transformer_code).after(train)
