import os
import random
import string
import json
import kfp
import kfp.dsl as dsl
import kfp.compiler as compiler
from kfp import components

token = os.getenv("DKUBE_USER_ACCESS_TOKEN")
dkube_training_op           = components.load_component_from_file("/mnt/dkube/pipeline/components/training/component.yaml")
dkube_serving_op            = components.load_component_from_file("/mnt/dkube/pipeline/components/serving/component.yaml")

image = "ocdr/d3-datascience-pytorch-cpu:v1.6"
serving_image = "ocdr/pytorchserver:1.6"
training_program = "Img-DN"
dataset = "Img-DN"
model = "Img-DN"
training_script = "python image-denoising/model-care.py"
transformer_code="image-denoising/transformer.py"
user = os.getenv('USERNAME')
framework = "pytorch"
f_version =  "1.6"
output_mount_point = "/opt/dkube/output/"
input_mount_point = "/opt/dkube/input/"

@kfp.dsl.pipeline(
    name='Img-Denoising-cicd',
    description='IMAGE-DENOISING EXAMPLE'
)
def image_denoising_pipeline():
    
        train       = dkube_training_op(token,container = json.dumps({"image": image}),
                                    framework=framework, version=f_version,
                                    program=training_program, run_script=training_script,
                                    datasets=json.dumps([dataset]), outputs=json.dumps([model]),
                                    input_dataset_mounts=json.dumps([input_mount_point]),
                                    output_mounts=json.dumps([output_mount_point]))

       
        serving     = dkube_serving_op(token,model = train.outputs['artifact'], device='cpu', 
                                    serving_image=json.dumps({"image": serving_image}),
                                    transformer_image=json.dumps({"image": image}),
                                    transformer_project=training_program,
                                    transformer_code=transformer_code).after(train)
