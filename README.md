# Projeto WordPress Escalável com Nginx e Docker Compose

## Sobre o Projeto

Este projeto implementa uma arquitetura WordPress de alta disponibilidade usando Docker Compose. Um servidor **Nginx** atua como **balanceador de carga**, distribuindo o tráfego entre **três instâncias do WordPress**, todas conectadas a um único banco de dados **MySQL**.

- **Escalabilidade:** O tráfego é dividido entre múltiplos servidores.
- **Tolerância a Falhas:** Se uma instância do WordPress falhar, o site continua online.
- **Segurança:** Apenas o Nginx é exposto, protegendo os outros serviços.

---

## 🚀 Iniciar o Ambiente
Para iniciar todos os contêineres em segundo plano:

```bash
docker-compose up -d
```

Após a execução, acesse o site em:  
👉 [http://localhost](http://localhost)

---

## 🔍 Comandos de Verificação

### Verificar o status dos contêineres:
```bash
docker-compose ps
```

### Listar volumes criados pelo Docker:
```bash
docker volume ls
```

### Testar o balanceamento de carga
(No PowerShell, use `curl.exe`)

```powershell
curl.exe -I http://localhost
```

> 💡 **Observação:** O endereço de IP no cabeçalho `X-Upstream` deve mudar a cada execução.

---

## 🧰 Comandos para Solução de Erros

### Ver logs de um serviço específico (ex: nginx):
```bash
docker-compose logs nginx
```

### Inspecionar um contêiner para ver detalhes e IP:
```bash
docker inspect wordpress1
```

---

## 🧹 Parar e Limpar o Ambiente

### Parar os contêineres (mantendo os dados do site):
```bash
docker-compose down
```

### Resetar o projeto completamente (**APAGA TODOS OS DADOS**):
```bash
docker-compose down -v
```

## 🧪 Demonstração

A imagem abaixo mostra o ambiente Docker em execução com Nginx, WordPress e MySQL funcionando corretamente:

![Demonstração do projeto rodando no Docker Compose](./assets/img-curl.png)
