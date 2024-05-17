Steps:

1. Install vault with helm
helm install vault hashicorp/vault --values vault-values.yaml

2. Initialize vault if needed and unseal it. You can do it with UI.
3. Initialize role with policy
First run:

kubectl exec --stdin=true --tty=true vault-0 -- /bin/sh

Then inside the vault shell login with root token

vault login

Then run these commands:
```bash
vault auth enable kubernetes
vault write auth/kubernetes/config \
	kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"
vault secrets enable -path=main kv-v2
vault policy write dev - <<EOF
path "main/*" {
   capabilities = ["read"]
}
EOF
vault write auth/kubernetes/role/k8s_auth_role \
	bound_service_account_names=default \
	bound_service_account_namespaces=default \
	policies=dev \
	audience=vault \
	ttl=24h
exit
```


4. Now we need to install the vault-secrets-operator
helm install vault-secrets-operator hashicorp/vault-secrets-operator --values vault-secrets-operator-values.yaml
5. Add service account for vault-secrets-operator to authenticate into vault and read secrets
kubectl apply -f vault-auth-static.yaml
kubectl apply -f vault-static-secret.yaml

Thats it, you should now have a secretkv Kubernetes secrets 
