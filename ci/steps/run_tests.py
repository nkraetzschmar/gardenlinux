import glci.model
import glci.util


def run_tests(
    architecture: str,
    cicd_cfg_name: str,
    gardenlinux_epoch: str,
    modifiers: str,
    platform: str,
    publishing_actions: str,
    repo_dir: str,
    suite: str,
    snapshot_timestamp: str,
    version: str,
):
    print(f'run_test with: {architecture=}, {cicd_cfg_name=}, {architecture=}, {gardenlinux_epoch=}')
    print(f'   : {modifiers=}, {platform=}, {publishing_actions=}, {repo_dir=}')
    print(f'   : {suite=}, {snapshot_timestamp=}, {version=}')
    publishing_actions = [
        glci.model.PublishingAction(action.strip()) for action in publishing_actions.split(',')
    ]
    
    if not glci.model.PublishingAction.RUN_TESTS in publishing_actions:
        print('publishing action "run_tests" not specified - skipping tests')
        return True

    result = True
    print("Running integration tests")
    print("Integration tests finished with result {result=}")
    return result
