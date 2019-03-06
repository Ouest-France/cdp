# `cdp docker`

- build docker image
- tag docker image
- push docker image to registry

```bash
cdp docker [--image-tag=[branch-name|,latest|,sha1]] [--push-on=[gitlab|aws-ecr]] [[--simulate-merge-on=branch_name]]
```

Parameters

- `--image-tag=` (optional) tag docker image, values can any or some of:
 - `branch-name` tag docker image with branch name (default), using $XXXX environment variable (default)
 - `latest` tag docker image with 'latest'
 - `sha1` tag docker image with commit sha1, using $XXXX environment variable

 Example: `--image-tag=branch-name,latest`

- `--simulate-merge-on=` (optional) Build docker image with the merge current branch on specify branch (no commit)

- `--push-on=` (optional)
  - `gitlab` use gitlab registry (default)
  - `aws-ecr` use k8s configuration for AWS ECR

# `cdp k8s`

- Generate helm chart
- Configure Kubernetes to pull image from `pull-from`
- Deploy it on Kubernetes

```bash
cdp k8s [--image-tag=[branch-name|sha1|latest]] [--pull-from=[gitlab|aws-ecr] [--namespace=[branch-name|project-name]] [--deploy-spec-dir=charts/]
```


- `--image-tag=` (optional)
  - `branch-name` use specified image tag, using $XXXX environment variable (default)
  - `latest` use 'latest' tag
  - `sha1` use sha1 commit tag, using $XXXX environment variable

  Example: `--image-tag=branch-name,latest` will pull the docker image with the branch name specified by $XXXXX environment variable.

- `--pull-from=` (optional) from where to pull the image
  - `gitlab` use gitlab registry (default)
  - `aws-ecr` use Kubernetes configuration for AWS ECR

- `--namespace=` (optional) which namespace to deploy the image to, values can be any of:
  - `project-branch-name` use project and branch name to create k8s namespace (default)
  - `project-name` use project name to create k8s namespace

- `--deploy-spec-dir=` (optional) k8s deployment files, default: charts/
