.PHONY : all uninstall-all vault pg grafana jaeger

all: pg grafana prometheus jaeger opensearch fluentbit

uninstall-all:
	helm uninstall postgres;
	helm uninstall grafana;
	helm uninstall jaeger;
	helm uninstall prometheus;

vault:
	helm upgrade -i vault hashicorp/vault -f vault/vault-values.yaml

vault-operator:
	HTTPS_PROXY=140.99.122.244:999 helm pull hashicorp/vault-secrets-operator --version 0.6.0
	helm upgrade -i vault-secrets-operator vault-secrets-operator-0.6.0.tgz --values vault/vault-secrets-operator-values.yaml

pg:
	helm upgrade postgres bitnami/postgresql -i --version 15.2.9 -f postgres-values.yaml

grafana:
	helm upgrade grafana grafana/grafana --version 7.3.11 -i -f grafana-values.yaml;

prometheus:
	helm upgrade prometheus prometheus-community/prometheus --version 25.20.1 -i -f prometheus-values.yaml;

jaeger:
	helm upgrade jaeger jaegertracing/jaeger --version 3.0.7 -i -f jaeger-values.yaml

fluentbit:
	helm upgrade fluent-bit fluent/fluent-bit -i -f fluentbit-values.yaml

opensearch:
	helm upgrade osearch opensearch/opensearch -i -f opensearch-values.yaml

repos:
	helm repo add fluent https://fluent.github.io/helm-charts
	helm repo add opensearch https://opensearch-project.github.io/helm-charts
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts;
	helm repo add grafana https://grafana.github.io/helm-charts;
	helm repo add hashicorp https://helm.releases.hashicorp.com;
	helm repo add bitnami https://charts.bitnami.com/bitnami;
	helm repo add jaegertracing https://jaegertracing.github.io/helm-charts;
	HTTPS_PROXY=140.99.122.244:999 helm repo add hashicorp https://helm.releases.hashicorp.com
