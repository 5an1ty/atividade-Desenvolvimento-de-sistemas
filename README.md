Divisão de Responsabilidades da Equipe

A equipe foi organizada de forma que cada integrante assumisse uma responsabilidade específica dentro do projeto, possibilitando o desenvolvimento simultâneo dos componentes e uma melhor gestão das atividades.

Integrante	Responsabilidade	Atividades
Theo	Desenvolvimento da API	Implementação dos endpoints REST utilizando FastAPI, validação de dados e integração com o banco de dados.
Kaio	Banco de Dados	Modelagem do banco de dados PostgreSQL, criação das tabelas, definição dos relacionamentos e suporte à integração com a API.
Artur	Testes do Sistema	Realização de testes funcionais dos endpoints, validação das regras de negócio, identificação de falhas e registro das evidências de teste.
Gustavo	Documentação	Elaboração do README, desenvolvimento do relatório técnico, organização da documentação do projeto e consolidação das evidências produzidas pela equipe.
Colaboração

Apesar da divisão de responsabilidades, todas as decisões relacionadas ao projeto foram discutidas em conjunto pelos integrantes, garantindo alinhamento entre os módulos desenvolvidos e a qualidade da solução final.

O controle de versão foi realizado por meio do GitHub, permitindo o acompanhamento das alterações, a colaboração entre os integrantes e a integração organizada do código-fonte.

Visão Geral do Projeto

O projeto consiste no desenvolvimento de um sistema de gerenciamento de solicitações utilizando Python, FastAPI, PostgreSQL e Railway.

A solução permitirá que usuários registrem solicitações por meio de uma API REST, armazenando as informações em um banco de dados para posterior consulta e acompanhamento.

Funcionalidades Principais
Criar uma nova solicitação.
Armazenar os dados da solicitação no banco de dados PostgreSQL.
Consultar solicitações cadastradas.
Atualizar o status de uma solicitação (Aberta, Em Andamento, Concluída, etc.).
Enviar notificações automáticas por e-mail quando uma solicitação for criada ou tiver seu status alterado.
Disponibilizar o sistema online através da plataforma Railway.
Fluxo do Sistema
O usuário envia uma nova solicitação.
A API recebe e valida os dados.
A solicitação é salva no banco de dados PostgreSQL.
O sistema envia um e-mail de confirmação ao usuário.
A solicitação pode ser consultada posteriormente.
Um administrador pode atualizar o status da solicitação.
Sempre que houver alteração de status, um novo e-mail é enviado ao usuário.
Todo o sistema permanece disponível na nuvem através do Railway.
Tecnologias Utilizadas
Python
FastAPI
PostgreSQL
SQLAlchemy
SMTP 
Railway
GitHub
Objetivo

Desenvolver uma aplicação web simples, segura e escalável que demonstre a integração entre API REST, banco de dados PostgreSQL, envio automático de chamados.
