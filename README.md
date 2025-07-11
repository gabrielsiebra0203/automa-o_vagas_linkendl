# LinkedIn Automation - Automação de Candidaturas

Este projeto automatiza o processo de candidatura para vagas no LinkedIn usando Python e Playwright.

## 🚀 Funcionalidades

- ✅ Login automático no LinkedIn
- 🔍 Busca de vagas por keywords e localização
- 🎯 Filtro automático para vagas com "Easy Apply"
- 📝 Candidatura automática para vagas selecionadas
- ⏱️ Delays aleatórios para simular comportamento humano
- 📊 Controle de número máximo de candidaturas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no LinkedIn
- Navegador Chrome (será baixado automaticamente pelo Playwright)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
```bash
git clone <seu-repositorio>
cd linkedin_automation
```

2. **Instale as dependências**
```bash
l
```

3. **Instale os navegadores do Playwright**
```bash
playwright install
```

4. **Configure suas credenciais**
   - Abra o arquivo `config.json`
   - Substitua `seu_email@exemplo.com` pelo seu email do LinkedIn
   - Substitua `sua_senha` pela sua senha do LinkedIn
   - Ajuste as keywords e localizações conforme sua preferência

## ⚙️ Configuração

Edite o arquivo `config.json`:

```json
{
    "email": "seu_email@linkedin.com",
    "password": "sua_senha_aqui",
    "keywords": [
        "python",
        "developer",
        "desenvolvedor"
    ],
    "locations": [
        "São Paulo",
        "Rio de Janeiro",
        "Remoto"
    ],
    "max_applications": 10
}
```

### Parâmetros de Configuração:

- **email**: Seu email do LinkedIn
- **password**: Sua senha do LinkedIn
- **keywords**: Lista de palavras-chave para buscar vagas
- **locations**: Lista de localizações para buscar vagas
- **max_applications**: Número máximo de candidaturas a enviar

## 🚀 Como Usar

1. **Configure suas credenciais no `config.json`**

2. **Execute a automação**
```bash
python main.py
```

3. **Acompanhe o progresso**
   - O navegador abrirá automaticamente
   - Você verá o processo de login e candidaturas em tempo real
   - O console mostrará o progresso detalhado

## 🔧 Personalização

### Modificar Keywords
Edite a lista `keywords` no `config.json`:
```json
"keywords": [
    "python developer",
    "full stack",
    "backend engineer",
    "data scientist"
]
```

### Modificar Localizações
Edite a lista `locations` no `config.json`:
```json
"locations": [
    "São Paulo, SP",
    "Rio de Janeiro, RJ",
    "Remoto",
    "Brasil"
]
```

### Executar em Modo Headless
Para executar sem abrir o navegador, modifique a linha 280 em `main.py`:
```python
automation = LinkedInAutomation(headless=True)
```

## ⚠️ Importante

- **Use com responsabilidade**: Não abuse da automação para evitar bloqueios
- **Mantenha delays**: Os delays aleatórios ajudam a simular comportamento humano
- **Verifique candidaturas**: Sempre revise as candidaturas enviadas
- **Respeite os termos**: Use de acordo com os termos de uso do LinkedIn

## 🛡️ Segurança

- **Não compartilhe credenciais**: Mantenha o `config.json` seguro
- **Use variáveis de ambiente**: Para produção, considere usar variáveis de ambiente
- **Backup**: Faça backup das suas configurações

## 🔍 Troubleshooting

### Problema: Login falha
- Verifique se as credenciais estão corretas
- Certifique-se de que a conta não tem autenticação de dois fatores ativa
- Tente fazer login manualmente primeiro

### Problema: Não encontra vagas
- Verifique se as keywords estão corretas
- Tente keywords mais específicas
- Verifique se as localizações estão corretas

### Problema: Botão Easy Apply não encontrado
- Algumas vagas podem não ter candidatura simplificada
- O script pulará automaticamente essas vagas

## 📝 Logs

O script mostra logs detalhados no console:
- 🔄 Processos em andamento
- ✅ Sucessos
- ❌ Erros
- ⚠️ Avisos

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é para uso educacional e pessoal. Use com responsabilidade.

## ⚠️ Disclaimer

Este script é fornecido "como está" sem garantias. Use por sua conta e risco. O autor não se responsabiliza por qualquer consequência do uso deste script. 