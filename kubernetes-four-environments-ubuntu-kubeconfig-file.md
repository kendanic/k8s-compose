# Managing Multiple Kubernetes Environments from WSL Ubuntu

This guide uses four generic Kubernetes environments:

-   `dev`
-   `test`
-   `staging`
-   `prod`

Each environment has its own kubeconfig file and Kubernetes context.

## 1. Go to the Kubernetes configuration directory

``` bash
mkdir -p ~/.kube
cd ~/.kube
```

Check existing files:

``` bash
ls -lh
```

Example structure:

``` text
dev-config
test-config
staging-config
prod-config
cache/
```

------------------------------------------------------------------------

## 2. Keep a separate kubeconfig for each environment

Store the kubeconfig files as:

``` text
~/.kube/dev-config
~/.kube/test-config
~/.kube/staging-config
~/.kube/prod-config
```

Protect the files:

``` bash
chmod 600 ~/.kube/dev-config
chmod 600 ~/.kube/test-config
chmod 600 ~/.kube/staging-config
chmod 600 ~/.kube/prod-config
```

------------------------------------------------------------------------

## 3. Check each kubeconfig separately

Development:

``` bash
KUBECONFIG=$HOME/.kube/dev-config kubectl config get-contexts
```

Test:

``` bash
KUBECONFIG=$HOME/.kube/test-config kubectl config get-contexts
```

Staging:

``` bash
KUBECONFIG=$HOME/.kube/staging-config kubectl config get-contexts
```

Production:

``` bash
KUBECONFIG=$HOME/.kube/prod-config kubectl config get-contexts
```

The value under the `NAME` column is the actual Kubernetes context name.

------------------------------------------------------------------------

## 4. Load all four kubeconfigs

For the current WSL terminal:

``` bash
export KUBECONFIG=$HOME/.kube/dev-config:$HOME/.kube/test-config:$HOME/.kube/staging-config:$HOME/.kube/prod-config
```

Verify:

``` bash
echo $KUBECONFIG
```

Then:

``` bash
kubectl config get-contexts
```

------------------------------------------------------------------------

## 5. Rename contexts to simple environment names

First identify the original context name in each kubeconfig.

Then rename them as needed:

``` bash
kubectl config rename-context <original-dev-context> dev
kubectl config rename-context <original-test-context> test
kubectl config rename-context <original-staging-context> staging
kubectl config rename-context <original-prod-context> prod
```

Check:

``` bash
kubectl config get-contexts
```

Example:

``` text
CURRENT   NAME
          dev
          test
*         staging
          prod
```

The `*` identifies the currently active context.

------------------------------------------------------------------------

## 6. Switch between environments

Development:

``` bash
kubectl config use-context dev
```

Test:

``` bash
kubectl config use-context test
```

Staging:

``` bash
kubectl config use-context staging
```

Production:

``` bash
kubectl config use-context prod
```

Check the current environment:

``` bash
kubectl config current-context
```

------------------------------------------------------------------------

## 7. Verify cluster access after switching

Always verify the context first:

``` bash
kubectl config current-context
```

Then:

``` bash
kubectl get nodes
kubectl get ns
```

For example:

``` bash
kubectl config use-context staging
kubectl config current-context
kubectl get nodes
kubectl get ns
```

------------------------------------------------------------------------

## 8. Work with namespaces

List namespaces:

``` bash
kubectl get ns
```

Pods:

``` bash
kubectl get pods -n <namespace>
```

Deployments:

``` bash
kubectl get deployments -n <namespace>
```

Services:

``` bash
kubectl get svc -n <namespace>
```

StatefulSets:

``` bash
kubectl get statefulsets -n <namespace>
```

PVCs:

``` bash
kubectl get pvc -n <namespace>
```

ConfigMaps:

``` bash
kubectl get configmap -n <namespace>
```

Secrets:

``` bash
kubectl get secrets -n <namespace>
```

------------------------------------------------------------------------

## 9. Check Helm releases

Current environment:

``` bash
helm list -n <namespace>
```

All namespaces:

``` bash
helm list -A
```

Check a particular environment without switching:

``` bash
helm list --kube-context dev -n <namespace>
helm list --kube-context test -n <namespace>
helm list --kube-context staging -n <namespace>
helm list --kube-context prod -n <namespace>
```

------------------------------------------------------------------------

## 10. Run kubectl commands without changing the active context

Development:

``` bash
kubectl --context dev get pods -n <namespace>
```

Test:

``` bash
kubectl --context test get pods -n <namespace>
```

Staging:

``` bash
kubectl --context staging get pods -n <namespace>
```

Production:

``` bash
kubectl --context prod get pods -n <namespace>
```

This is useful when comparing environments.

------------------------------------------------------------------------

## 11. Compare the same application across environments

Pods:

``` bash
kubectl --context dev get pods -n <namespace>
kubectl --context test get pods -n <namespace>
kubectl --context staging get pods -n <namespace>
kubectl --context prod get pods -n <namespace>
```

Services:

``` bash
kubectl --context dev get svc -n <namespace>
kubectl --context test get svc -n <namespace>
kubectl --context staging get svc -n <namespace>
kubectl --context prod get svc -n <namespace>
```

PVCs:

``` bash
kubectl --context dev get pvc -n <namespace>
kubectl --context test get pvc -n <namespace>
kubectl --context staging get pvc -n <namespace>
kubectl --context prod get pvc -n <namespace>
```

------------------------------------------------------------------------

## 12. Make the configuration persistent in WSL

Edit:

``` bash
nano ~/.bashrc
```

Add:

``` bash
export KUBECONFIG=$HOME/.kube/dev-config:$HOME/.kube/test-config:$HOME/.kube/staging-config:$HOME/.kube/prod-config
```

Save and reload:

``` bash
source ~/.bashrc
```

Verify:

``` bash
echo $KUBECONFIG
kubectl config get-contexts
```

------------------------------------------------------------------------

## 13. Important check before making changes

Before running commands such as:

``` bash
kubectl apply
kubectl delete
kubectl scale
helm install
helm upgrade
helm uninstall
```

check the current context:

``` bash
kubectl config current-context
```

Also confirm the target namespace:

``` bash
kubectl get ns
```

For important changes, using an explicit context is safer:

``` bash
kubectl --context staging get pods -n <namespace>
```

or:

``` bash
helm list --kube-context staging -n <namespace>
```

------------------------------------------------------------------------

## Quick Reference

``` bash
# Show contexts
kubectl config get-contexts

# Show active context
## Very imporant to run before configuration
kubectl config current-context

# Switch environment
kubectl config use-context dev
kubectl config use-context test
kubectl config use-context staging
kubectl config use-context prod

# Cluster information
kubectl get nodes
kubectl get ns

# Namespace resources
kubectl get pods -n <namespace>
kubectl get deployments -n <namespace>
kubectl get svc -n <namespace>
kubectl get statefulsets -n <namespace>
kubectl get pvc -n <namespace>

# Helm
helm list -n <namespace>
helm list -A

# Explicit context
kubectl --context dev get pods -n <namespace>
kubectl --context test get pods -n <namespace>
kubectl --context staging get pods -n <namespace>
kubectl --context prod get pods -n <namespace>
```

## Final Structure

``` text
WSL Ubuntu
    |
    +-- kubectl / Helm
    |
    +-- ~/.kube/dev-config
    |       +-- context: dev
    |
    +-- ~/.kube/test-config
    |       +-- context: test
    |
    +-- ~/.kube/staging-config
    |       +-- context: staging
    |
    +-- ~/.kube/prod-config
            +-- context: prod
```

All four configurations are loaded using:

``` bash
export KUBECONFIG=$HOME/.kube/dev-config:$HOME/.kube/test-config:$HOME/.kube/staging-config:$HOME/.kube/prod-config
```
