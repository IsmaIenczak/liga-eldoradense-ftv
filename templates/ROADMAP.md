# 🚀 Roadmap - Liga Eldoradense de Futevôlei

## ✅ Etapa atual do projeto
O sistema já possui:

- [x] CRUD de atletas
- [x] CRUD de eventos
- [x] CRUD de categorias
- [x] CRUD de inscrições
- [x] CRUD de níveis
- [x] Validação de CPF
- [x] Regra de residência em Eldorado do Sul
- [x] Controle de nível validado
- [x] Filtro de atletas por status de validação
- [x] Autenticação com login/logout
- [x] Sessão com expiração
- [x] Proteção de rotas
- [x] Separação inicial entre admin e atleta
- [x] Conta de atleta vinculada ao cadastro esportivo
- [x] Cadastro autônomo de atleta
- [x] Área inicial do atleta
- [x] Visualização das próprias inscrições
- [x] Inscrição feita pelo próprio atleta com parceiro já cadastrado
- [x] Campo de telefone no atleta
- [x] Campo de status na inscrição
- [x] Base preparada para convite de parceiro e integração futura com WhatsApp

---

## 🔜 Fase 1 — Consolidar fluxo real do atleta
Objetivo: tornar o fluxo do atleta autônomo e natural.

- [ ] Permitir inscrição com parceiro ainda não cadastrado
- [ ] Criar fluxo de pré-cadastro do parceiro
- [ ] Criar status de inscrição mais claros:
  - [ ] pendente
  - [ ] confirmada
  - [ ] cancelada
- [ ] Criar tela de pendências do atleta
- [ ] Permitir ao atleta editar o próprio perfil - mas com limitações - numero somente atraves de confirmação de codigo via sms ou whats - nível?
- [ ] Melhorar exibição de mensagens e feedbacks no fluxo de inscrição

---

## 📲 Fase 2 — Convite e confirmação de parceiro
Objetivo: transformar a inscrição em fluxo colaborativo.

- [ ] Criar sistema de convite de parceiro
- [ ] Criar aceite/recusa de convite
- [ ] Relacionar convite com inscrição pendente
- [ ] Permitir confirmação posterior do parceiro
- [ ] Preparar integração com WhatsApp
- [ ] Definir como será o disparo do convite:
  - [ ] manual
  - [ ] automático
- [ ] Decidir se haverá expiração do convite

---

## 🏆 Fase 3 — Operação esportiva
Objetivo: sair do cadastro e entrar na gestão da competição.

- [ ] Criar status de evento
- [ ] Criar status de categoria
- [ ] Encerrar inscrições por categoria/evento
- [ ] Gerar chaveamento automático
- [ ] Modelar partidas
- [ ] Registrar resultados
- [ ] Criar histórico por atleta
- [ ] Criar visualização de andamento da competição

---

## 📈 Fase 4 — Ranking e progressão de nível
Objetivo: transformar desempenho em evolução esportiva.

- [ ] Criar pontuação por resultado
- [ ] Criar ranking por atleta
- [ ] Criar histórico de títulos
- [ ] Definir regras de progressão de nível
- [ ] Automatizar subida de nível
- [ ] Permitir intervenção manual do admin na progressão
- [ ] Exibir ranking para atletas

---

## 💰 Fase 5 — Financeiro
Objetivo: transformar inscrição em fluxo completo de operação.

- [ ] Criar status financeiro da inscrição
- [ ] Definir regra de confirmação por pagamento
- [ ] Integrar pagamento via Pix
- [ ] Integrar pagamento via cartão
- [ ] Gerar QR Code para Pix
- [ ] Confirmar pagamento automaticamente ou manualmente
- [ ] Exibir situação de pagamento ao atleta
- [ ] Tratar cancelamento/reembolso, se necessário

---

## 🔐 Fase 6 — Segurança e conta do usuário
Objetivo: amadurecer a autenticação.

- [ ] Confirmação de email
- [ ] Recuperação de senha
- [ ] Alteração de senha
- [ ] Melhorar regras de segurança
- [ ] Validar melhor telefone
- [ ] Revisar consistência da sessão
- [ ] Ajustar permissões por perfil com mais granularidade

---

## ⚙️ Fase 7 — Maturidade técnica
Objetivo: deixar o projeto mais robusto para crescer.

- [ ] Implementar migrations
- [ ] Separar melhor regras de negócio das rotas
- [ ] Criar camada de serviços
- [ ] Organizar utilitários e helpers
- [ ] Melhorar estrutura dos blueprints
- [ ] Criar dados iniciais automáticos (seed)
- [ ] Melhorar tratamento de erros
- [ ] Preparar testes automatizados

---

## 🎨 Fase 8 — Interface e experiência
Objetivo: melhorar aparência e clareza do sistema.

- [ ] Refinar layout geral
- [ ] Melhorar painel do admin
- [ ] Melhorar área do atleta
- [ ] Melhorar responsividade
- [ ] Padronizar botões, alertas e tabelas
- [ ] Melhorar navegação por perfil
- [ ] Destacar informações importantes visualmente

---

## 💡 Ideias futuras
- [ ] Notificações automáticas
- [ ] Convite por WhatsApp
- [ ] Ranking público
- [ ] Página pública de eventos
- [ ] App mobile no futuro