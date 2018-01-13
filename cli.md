# cdp docker --tag-branch-name --tag-latest --tag-commit-sha1 --simulate-merge-on=[branch_name] --push-on=(gitlab|aws_ecr)

docker:
  "--tag-branch-name": "Tag docker image with branch name (default)"
  "--tag-sha1": "Tag docker image with commit sha1"
  "--tag-latest": "Tag docker image with 'latest'"
  "--simulate-merge-on=": "Build docker image with the merge current branch on specify branch (no commit)"
  "--push-on=":
    "gitlab": "Use gitlab registry (default)"
    "aws_ecr": "Use k8s configuration for AWS ECR"

# cdp k8s deploy --with=helm --namespace-name=(project-branch-name|project-name) --gitlab-docker-registry --deploy-spec-dir=charts/ --image-tag=(branch_name|sha1|latest)
k8s:
  "--with=":
    "helm": "Use helm charts (default)"
  "--namespace-name=":
    "project-branch-name": "Use project and branch name to create k8s namespace (default)"
    "project-name": "Use project name to create k8s namespace"
  "--gitlab-docker-registry": "override k8s configuration for docker registry"
  "--deploy-spec-dir=": "k8s deployment files (default: charts/)"
  "--image-tag=":
    "branch-name": "Use branch name tag (default)"
    "sha1": "Use sha1 commit tag"
    "latest": "Use latest tag"
