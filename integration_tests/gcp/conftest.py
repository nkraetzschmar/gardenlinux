from dataclasses import dataclass
import tempfile
import json
import os

from util import ctx
import googleapiclient.discovery
import pytest


# Documentation:
# https://cloud.google.com/compute/docs/tutorials/python-guide
# https://github.com/GoogleCloudPlatform/python-docs-samples
# reference: https://cloud.google.com/compute/docs/reference/rest/v1

@dataclass
class GCP_Cfg:
    project_id: str
    credentials: dict


@pytest.fixture(scope="session")
def gcp_cfg(test_params):
    cfg_factory = ctx().cfg_factory()
    cfg = cfg_factory._cfg_element(cfg_type_name="gcp", cfg_name="gardenlinux")
    gcs_credentials = cfg.raw["service_account_key"]
    return GCP_Cfg(credentials=cfg.raw["service_account_key"], project_id=gcs_credentials['project_id'])

@pytest.fixture(scope="session")
def compute_client(gcp_cfg):
    '''
    get a Google client instance to further interact with GCP compute instances 
    '''
    cfg_factory = ctx().cfg_factory()
    cfg = cfg_factory._cfg_element(cfg_type_name="gcp", cfg_name="gardenlinux")
    gcs_credentials = cfg.raw["service_account_key"]
    # convert dict to string object
    with tempfile.NamedTemporaryFile(mode="wt", prefix="gcs_", suffix=".json", delete=False) as temp_file:
        cred_file_name = temp_file.name
        temp_file.write(json.dumps(gcs_credentials))
    print(f'Credentials written to {cred_file_name}')    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(cred_file_name)
    return googleapiclient.discovery.build('compute', 'v1')
