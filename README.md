# Description
This is a basic web application. It is supposed to work mainly as a template to build bigger apps.

### Links
- https://zinchenkomig.com - Main website
- https://api.zinchenkomig.com/docs - Backend API
- http://grafana.zinchenkomig.com - Grafana
- http://prometheus.zinchenkomig.com - Prometheus
- http://jaeger.zinchenkomig.com - Jaeger Tracing
- http://vault.zinchenkomig.com - Vault

### Main features:
- Authentication with refresh and access JWT tokens.
- SignUp with Email and Telegram.
- Posts. Authenticated users can post messages.
- Role model. For now there are just 2 roles: user and admin.
- Users Management system. Admin users have a special panel where they can manage the authenticated users information and control their access.
- S3 bucket to store users pictures.
________
  
- Kubernetes infrastructure.
- CI/CD.
- Secrets management system using Vault Operator. Secrets from Vault are automatically pushed as environment variables to the backend.
- Logs collection system. Logs from pods inside the cluster are collected in the Opensearch index using Fluentbit.
- Prometheus and Grafana monitoring. I also wrote a python script to deploy my grafana dashboards automatically.
- Helm charts for every deployable instance on the cluster.
- Tracing system with Jaeger.

### Deployed services
- PostgreSQL
- Opensearch
- Vault
- Jaeger
- Prometheus
- Grafana
- Fleuntbit (logs collection)
- CertManager
- Minio (S3 buckets).

**I run this whole setup using one VM with 8GB of RAM and 2 CPUs.**

# Web App Preview
<img src="https://github.com/user-attachments/assets/f9928a73-6590-4560-84a3-adc0b12fd318"/>

# Grafana preview
<img width="1433" alt="image" src="https://github.com/user-attachments/assets/e521cffd-fdea-45d1-afac-53c51dcfceaf">


