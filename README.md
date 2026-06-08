Divisão de Responsabilidades da Equipe
A equipe foi organizada de forma que cada integrante ficasse responsável por uma parte específica do sistema, permitindo o desenvolvimento paralelo dos componentes e melhor gerenciamento do projeto.
Integrante
Responsabilidade
Atividades
Theo
Desenvolvimento da API
Implementação dos endpoints REST utilizando FastAPI, validação de dados e integração com o banco de dados.
Kaio
Banco de Dados
Modelagem do banco MySQL, criação das tabelas, relacionamentos e integração com a API.
Artur
Testes do Sistema
Realização de testes funcionais dos endpoints, validação das regras de negócio, identificação de erros e elaboração das evidências de teste.
Gustavo
Documentação
Elaboração do README, relatório técnico, organização da documentação do projeto e consolidação das evidências produzidas pela equipe.

Colaboração
Embora cada integrante possua uma responsabilidade principal, todas as decisões técnicas foram discutidas em conjunto, garantindo integração entre os módulos e qualidade final da aplicação.
O controle de versão foi realizado através do GitHub, permitindo que cada integrante trabalhasse em sua própria branch e posteriormente integrasse suas alterações ao projeto principal.


Visão Geral do Projeto
O projeto consiste no desenvolvimento de um sistema de gerenciamento de solicitações utilizando Python, FastAPI, MySQL e Railway.
A solução permitirá que usuários registrem solicitações por meio de uma API REST, armazenando as informações em um banco de dados para posterior consulta e acompanhamento.
Funcionalidades Principais
Criar uma nova solicitação.
Armazenar os dados da solicitação no banco de dados MySQL.
Consultar solicitações cadastradas.
Atualizar o status de uma solicitação (Aberta, Em Andamento, Concluída, etc.).
Enviar notificações automáticas por e-mail quando uma solicitação for criada ou tiver seu status alterado.
Disponibilizar o sistema online através da plataforma Railway.
Fluxo do Sistema
O usuário envia uma nova solicitação.
A API recebe e valida os dados.
A solicitação é salva no banco de dados MySQL.
O sistema envia um e-mail de confirmação ao usuário.
A solicitação pode ser consultada posteriormente.
Um administrador pode atualizar o status da solicitação.
Sempre que houver alteração de status, um novo e-mail é enviado ao usuário.
Todo o sistema permanece disponível na nuvem através do Railway.
Tecnologias Utilizadas
Python
FastAPI
MySQL
SQLAlchemy
SMTP (envio de e-mails)
Railway
GitHub
Objetivo
Desenvolver uma aplicação web simples, segura e escalável que demonstre a integração entre API REST, banco de dados, envio automático de e-mails e implantação em ambiente de nuvem, aplicando conceitos de governança de TI e desenvolvimento de software.
