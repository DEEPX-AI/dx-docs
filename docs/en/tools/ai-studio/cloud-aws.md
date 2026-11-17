---
title: DX Cloud on AWS
description: Connect DX AI Studio to AWS, prepare a Marketplace stack, compile ONNX to .dxnn in the cloud and register Greengrass devices.
---

# DX Cloud on AWS

DX Cloud lets you compile an `.onnx` model into a `.dxnn` on AWS from inside DX AI Studio, with no local `dxcom`, and manage Greengrass devices that run the DEEPX runtime.

Open **DX Cloud** from the hub card, at `/cloud/`, or with `Alt`+`9`. Its internal Python package is named `dx_edge`; it is not DX EdgeGuide. The full AWS walkthrough without the studio is on the [DX-Edge](../dx-edge.md) page.

## Before you start

* An AWS account and an account admin who can accept AWS Marketplace terms.
* The optional `boto3` extra in the Python environment that runs the studio. From the `dx-ai-studio` folder:

    ```bash
    python3 -m pip install -e '.[aws]'
    ```

    Without it the page and its guide open, but AWS operations do not run.

* AWS credentials on the **studio host** (not on a remote browser's computer). DX Cloud uses the boto3 credential chain and an optional named profile from `~/.aws`. It has no screen to enter or store access keys.

## Products

| Product | What it does |
|---|---|
| [DEEPX Compiler Solution](https://aws.amazon.com/marketplace/pp/prodview-ev6ed5omu4ulo) | Runs `dxcom` on Amazon EC2. As a CloudFormation stack it becomes an event driven pipeline: an `.onnx` and its `.json` uploaded to the stack's model bucket start Lambda, then Step Functions, then a compiler instance that writes the `.dxnn` next to them. |
| [DEEPX Greengrass Solution](https://aws.amazon.com/marketplace/pp/prodview-732s46qfzuh34) | Deploys the `com.deepx.dx-runtime` component (NPU driver, firmware, `dx_rt` and `dx_stream`) to registered Greengrass core devices in an IoT Thing Group, with the same cloud compile pipeline in its stack. It deploys the runtime, not your compiled model. |

## Connect to AWS

1. Install AWS CLI v2 (it helps you set up credentials and SSO; the studio itself calls boto3). Install `unzip` and `curl` first if needed (`sudo apt install -y unzip curl`):

    ```bash
    ARCH="$(uname -m)"
    case "$ARCH" in
      x86_64|aarch64)
        curl "https://awscli.amazonaws.com/awscli-exe-linux-${ARCH}.zip" -o awscliv2.zip
        unzip -q awscliv2.zip
        sudo ./aws/install --update
        aws --version ;;
      *) echo "AWS CLI v2 for Linux supports x86_64 and aarch64 only (this machine: $ARCH)" ;;
    esac
    ```

1. Configure credentials. Option A, an access key from the IAM console:

    ```bash
    aws configure
    ```

    Option B, IAM Identity Center (SSO): run `aws configure sso` once to create a named profile, then `aws sso login --profile <name>` whenever the session expires.

1. Verify the identity:

    ```bash
    aws sts get-caller-identity --profile <name>
    ```

1. Check permissions. The identity needs CloudFormation, S3, Step Functions, SSM `GetParameter`, EC2, IAM (stacks are created with `CAPABILITY_IAM`), CloudWatch Logs and Lambda. The Greengrass tab also needs Greengrass V2 and IoT.
1. In step ① of the page, select the **AWS profile** and **region** and press **Check connection**. The account and ARN appear when it works. The region follows the profile, falling back to `ap-northeast-2`. A passing identity check does not prove every later permission.

## Subscribe and prepare a stack

1. Choose **DEEPX Compiler Solution** or **DEEPX Greengrass Solution**. Each has its own Marketplace subscription check. After an admin accepts the terms, press **Refresh**.
1. The check resolves the product template's AMI SSM parameter in your account and region. It is not a billing check and does not guarantee a specific AMI version, region or instance type.
1. Use **Find stacks** to pick an existing compatible stack, or enter a stack name and create one. Wait for `CREATE_COMPLETE` or `UPDATE_COMPLETE` with a `ModelBucketName` output before uploading a model.

Stack creation in the studio uses the region's **default VPC and first default subnet**, a generated bucket name and the template defaults for everything else (including instance type `t3.xlarge`). If you need a custom VPC, subnet or instance type, create the stack in the AWS Console and then find it in the studio. If creation fails, read the event reason and fix subscription, IAM or network problems before you retry.

!!! warning "Real AWS costs"
    Stacks and compiles use real, chargeable AWS resources. Storage and logs can cost money even when no compiler instance runs.

## Cloud Compile

1. With the connection checked, choose a ready stack. The studio reads the bucket from the stack outputs.
1. Choose the **ONNX model** (up to 500 MiB) and the **compile config** `.json` (up to 1 MiB, must be a JSON object), then press **Upload and compile**.
1. The pair goes to a timestamped `models/<model>-<YYYYmmdd-HHMMSS>/` prefix. The panel polls every 15 seconds and shows *pending*, *running*, *succeeded* or *failed*. No completion time is guaranteed.
1. Use **Compile jobs** to revisit jobs and **Show log** for the workflow steps and compiler output, or open the Step Functions, CloudWatch and S3 links. After closing the page, reconnect, select the same account, region and stack and refresh the job list instead of uploading again.
1. When the `.dxnn` is ready:

    | Action | Effect |
    |---|---|
    | **Download .dxnn** | Downloads through the browser |
    | **Save to Studio models** | Writes to the studio server's DX App models folder (`DX_APP_MODELS_DIR`, default `dx-runtime/dx_app/assets/models`) and **overwrites a file with the same name** |

!!! warning "Result and cleanup are separate"
    A `.dxnn` marks compile success, but the EC2 termination step can still be pending or fail. Check the workflow and EC2 before assuming all compute charges stopped.

If a job stays pending, check that both files reached the same S3 prefix and that a Step Functions execution started. On failure, read **Show log** and CloudWatch before submitting a new job.

## Greengrass devices

1. Select a ready Greengrass stack. **Devices (dx-runtime)** shows its Thing Group, deployment status and core devices. Open a device to see component versions and lifecycle states.
1. To add a device, enter its Thing name and generate the install script. **Copy** or **Download .sh** and review it. It holds stack, region, group and role settings, not credentials.
1. Prepare the device: Java 11 or newer, `curl`, `unzip`, `sudo`, device side AWS credentials allowed to provision Greengrass, and network access to AWS.
1. Run the script yourself on the device, then **Refresh** Devices. If registration fails, read the script's error and the device's Greengrass logs.

The studio never connects to the device or runs the script for you, and it does not send compiled models to devices.

## Delete a stack and clean up

Select the stack's delete action and type its exact name. Deletion is blocked while another stack operation runs.

* The model S3 bucket has a **Retain** policy and stays, with source models, results and object versions. Remove it yourself when no longer needed.
* Check for running compiler EC2 instances and other leftover resources.
* Deleting a Greengrass stack does not uninstall software on devices or remove their IoT identities and certificates.
* Marketplace subscriptions are separate. Cancel them in AWS Marketplace when you no longer need them.

## Next steps

* [DX-Edge: the full AWS guide](../dx-edge.md)
* [Compile locally in DX Compiler](workflow.md#dx-compiler)
