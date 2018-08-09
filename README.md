## Fluxo de Pipeline

- Como adicionar uma nova aplicação em Dev / STG e Prod
- Como adicionar uma nova aplicação ao fluxo de CI/CD 
- Como adicionar uma nova aplicação ao ELK

# Como adicionar uma app em Dev / STG

Como é de conhecimento, os ambientes de Desenvolvimento e Staging está na AWS. Portanto para adicionar uma nova aplicação a este ambiente, siga o fluxo a seguir: 

- Clone o repo Infrastructure: 

` git clone ssh://git@gitlab.glb-cip.ninja:2022/devops/infrastructure.git`

O repositório Infrastructure está estrutrado conforme descrito aqui. (Fazer a doc do Repo)

Os Terraforms estão separados em módulos no arquivo: `/multiplataforma/environments/dev/app_default.tf` e `/multiplataforma/environments/stg/app_default.tf`. 

Para criar uma nova app, basta copiar o ultimo módulo, por exemplo: 

```
module "app_monitoringstatusapi" {
  source                 = "../../resources/app-default"
  account                = "${var.account}"
  cluster_id             = "${data.terraform_remote_state.common.cluster["id"]}"
  cluster_role           = "${data.terraform_remote_state.common.cluster["serviceRole"]}"
  listener_arn           = "${module.alb_default_minimal_template.listener_arn}"
  vpc_id                 = "${data.terraform_remote_state.network.this_remote_vpc["id"]}"
  tags                   = "${local.tags}"
  identifier             = "${local.stack}"
  environment            = "${local.environment}"
  name                   = "monitoringstatusapi"
  task_def_file          = "app_monitoringstatusapi.json"
  listener_rule_priority = "19"
  port                   = "80"
  subdomain              = "monitoringstatusapi.${local.branch}"
  listener_rule          = "monitoringstatusapi.${local.branch}.${local.domain}"
  condition_field        = "host-header"
  health_check_matcher   = "200"
  elb_dns_name           = "${data.terraform_remote_state.common.alb["dns_name"]}"
  elb_zone_id            = "${data.terraform_remote_state.common.alb["zone_id"]}"
  zone_id                = "${data.terraform_remote_state.common.route53["zone_id"]}"
  branch                 = "${local.branch}"
  create_ecr             = 0
}
```
**Alterações necessárias:**
É importante alterar o valor `listener_rule_priority` para +1. Por exemplo, se o ultimo módulo está em 19, no seu módulo deverá ser 20.

Também é necessário alterar todos os nomes próprios para o nome de sua aplicação. Portanto digamos que a aplicação vai se chamar testeapinode, o seu módulo ficaria da seguinte forma: 

```
module "app_testeapinode" {
  source                 = "../../resources/app-default"
  account                = "${var.account}"
  cluster_id             = "${data.terraform_remote_state.common.cluster["id"]}"
  cluster_role           = "${data.terraform_remote_state.common.cluster["serviceRole"]}"
  listener_arn           = "${module.alb_default_minimal_template.listener_arn}"
  vpc_id                 = "${data.terraform_remote_state.network.this_remote_vpc["id"]}"
  tags                   = "${local.tags}"
  identifier             = "${local.stack}"
  environment            = "${local.environment}"
  name                   = "testeapinode"
  task_def_file          = "app_testeapinode.json"
  listener_rule_priority = "20"
  port                   = "80"
  subdomain              = "testeapinode.${local.branch}"
  listener_rule          = "testeapinode.${local.branch}.${local.domain}"
  condition_field        = "host-header"
  health_check_matcher   = "200"
  elb_dns_name           = "${data.terraform_remote_state.common.alb["dns_name"]}"
  elb_zone_id            = "${data.terraform_remote_state.common.alb["zone_id"]}"
  zone_id                = "${data.terraform_remote_state.common.route53["zone_id"]}"
  branch                 = "${local.branch}"
  create_ecr             = 0
}
```

Após a criação do módulo no TF, é necessário criar uma Task Definition para o seu projeto. Os task definitions estão nos caminhos: 
`infrastructure/multiplataforma/environments/dev/task-definition` e `infrastructure/multiplataforma/environments/stg/task-definition`. 


Pode copiar um arquivo também, por exemplo:

`cp app_monitoringstatusapi.json app_testeapinode.json`
Dentro do arquivo não é necessário altera nenhum valor, o app_monitoringstatusapi.json é bem enxuto. Você também pode criar um novo arquivo com o seguinte conteúdo:
```
[
  {
  "name": "${name}",
  "image": "${ecr_url}:latest-stg",
  "cpu": 0,
  "memoryReservation": 256,
  "essential": true,
  "portMappings": [
    {
      "containerPort": ${port},
      "hostPort": 0
    }
  ],
  "environment": [],
  "logConfiguration": {
    "logDriver": "awslogs",
    "options": {
      "awslogs-group": "/ecs/tvg-${name}-${branch}",
      "awslogs-region": "us-east-1",
      "awslogs-stream-prefix": "tvg"
      }
    }
  }
]
```
**Obs:**  Estamos subindo a APP em Dev e STG. É necessário fazer os passos em ambos os ambientes.

Após as alterações aplicadas, basta rodar os seguintes comandos:
`terraform init`
`terraform plan`
`terraform apply`

É imprescindível checar no `terraform plan`output se apenas as alterações requiridas serão aplicadas.

Após aplicar, você deve ter na AWS: 
- 1 Repositório ECR
- 2 Task Definitions : Dev e STG
- 2 Services: Dev e STG
- 2 Entradas no Route 53 
- 2 Target Groups
- 2 Listeners no ALB que corresponde ao Cluster ECS
- 2 Log Groups no CloudWatch


