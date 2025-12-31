# ONG Course Platform

Plataforma web para venda de cursos (B2C) e pacotes para organizações (B2B), desenvolvida para uma ONG com foco em inclusão e educação.

## 🎨 Design

A plataforma segue a identidade visual do site [invisibilidown.org](https://invisibilidown.org/), com:
- Cores primárias: Roxo (#6B46C1) e Laranja (#F97316)
- Design responsivo e moderno
- Interface intuitiva com sidebar e carrosséis

## 🚀 Tecnologias

- **Backend:** Django 4.2+ com Django REST Framework
- **Banco de Dados:** PostgreSQL 15
- **Servidor Web:** Nginx (reverse proxy)
- **Servidor de Aplicação:** Gunicorn
- **Containerização:** Docker + Docker Compose

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (optional, for cloning)

### Initial Setup

1. **Start the application:**
   ```bash
   cd c:\Users\User\Documents\Projetos\Site\Invisibilidown
   docker-compose up -d
   docker compose exec web python manage.py migrate

   ```

2. **Access the application:**
   - Main site: **http://localhost:9000**
   - Admin panel: **http://localhost:9000/admin**

3. **Default admin credentials:**
   - Email: `admin@invisibilidown.org`
   - Password: (set via Django admin on first login)

---

## 📚 How-To Guides

### How to Create an Admin User

**Method 1: Interactive (Recommended for first admin)**
```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts to enter:
- Email address
- First name
- Last name
- Password (twice)

**Method 2: Non-interactive (for automation)**
```bash
docker-compose exec web python manage.py createsuperuser --noinput --email admin@example.com
```
Note: You'll need to set the password via Django admin or shell.

**Method 3: Via Django Shell**
```bash
docker-compose exec web python manage.py shell
```
Then run:
```python
from accounts.models import CustomUser
user = CustomUser.objects.create_superuser(
    email='admin@example.com',
    first_name='Admin',
    last_name='User',
    password='your-secure-password'
)
```

---

### How to Add New Courses

**Via Django Admin (Recommended):**
1. Access http://localhost:9000/admin
2. Login with admin credentials
3. Click "Courses" → "Add Course"
4. Fill in:
   - Name
   - Description
   - Price (use 0.00 for free courses)
   - Image URL (from Unsplash or your CDN)
   - Active status (checked)
5. Click "Save"

**Via Management Command:**
```bash
docker-compose exec web python manage.py shell
```
```python
from courses.models import Course
Course.objects.create(
    name='New Course Name',
    description='Course description',
    price=99.90,
    image_url='https://images.unsplash.com/photo-xxx',
    is_active=True
)
```

---

### How to View Application Logs

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f web      # Django application
docker-compose logs -f db       # PostgreSQL database
docker-compose logs -f nginx    # Nginx web server
```

**Last N lines:**
```bash
docker-compose logs --tail=50 web
```

---

### How to Access the Database

**Via Django Shell:**
```bash
docker-compose exec web python manage.py shell
```

**Via PostgreSQL CLI:**
```bash
docker-compose exec db psql -U ong_user -d ong_platform
```

Common queries:
```sql
-- List all users
SELECT email, first_name, last_name FROM accounts_customuser;

-- List all courses
SELECT name, price, is_active FROM courses_course;

-- Count enrollments
SELECT COUNT(*) FROM courses_enrollment;
```

---

### How to Reset the Database

**Warning: This will delete all data!**

```bash
# Stop containers and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d

# Wait for database to be ready, then run migrations
docker-compose exec web python manage.py migrate

# Seed sample courses
docker-compose exec web python manage.py seed_courses

# Create admin user
docker-compose exec web python manage.py createsuperuser
```

---

### How to Backup the Database

```bash
# Create backup
docker-compose exec db pg_dump -U ong_user ong_platform > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T db psql -U ong_user ong_platform < backup_20231217_120000.sql
```

---

### How to Update Static Files

After modifying CSS/JS files:

```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

---

### How to Run Tests

```bash
# Run all tests
docker-compose exec web python manage.py test

# Run specific app tests
docker-compose exec web python manage.py test accounts
docker-compose exec web python manage.py test courses

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

---

### How to Create Database Migrations

After modifying models:

```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# View migration SQL (without applying)
docker-compose exec web python manage.py sqlmigrate accounts 0001
```

---

### How to Change the Port

Edit `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"  # Change 9000 to your desired port
```

Update `ong_platform/settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",  # Add your new port
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Add your new port
]
```

Restart:
```bash
docker-compose down
docker-compose up -d
```

---

### How to Monitor Container Health

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Inspect specific container
docker inspect invisibilidown-web-1
```

---

### How to Troubleshoot Common Issues

**Issue: Port already in use**
```bash
# Find what's using the port
netstat -ano | findstr :9000

# Stop the process or change the port in docker-compose.yml
```

**Issue: Database connection errors**
```bash
# Check database is healthy
docker-compose ps db

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

**Issue: Static files not loading**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

**Issue: Migrations not applied**
```bash
# Check migration status
docker-compose exec web python manage.py showmigrations

# Apply pending migrations
docker-compose exec web python manage.py migrate
```

---

## 📱 Features Overview

### For Users (B2C)
- ✅ Email-based authentication
- ✅ Course catalog with search and filters
- ✅ Shopping cart
- ✅ Checkout process (mock payment)
- ✅ My courses dashboard
- ✅ Profile management with email verification

### For Organizations (B2B)
- ✅ Course packages
- ✅ Member management
- ✅ Seat assignments

### Administration
- ✅ Django admin interface
- ✅ Course management (CRUD)
- ✅ Organization management
- ✅ User management

---

## 🗂️ Project Structure

```
Invisibilidown/
├── accounts/          # Authentication & user profiles
├── courses/           # Course catalog & enrollments
├── cart/              # Shopping cart
├── checkout/          # Purchase flow
├── orgs/              # B2B organizations
├── core/              # Base templates & home
├── ong_platform/      # Django settings
├── nginx/             # Nginx configuration
├── static/            # Static files
├── docker-compose.yml # Docker orchestration
├── Dockerfile         # Django container
└── requirements.txt   # Python dependencies
```

## 📊 Dados de Exemplo

O projeto inclui um comando para popular o banco com cursos de exemplo:

```bash
docker-compose exec web python manage.py seed_courses
```

Isso criará 15 cursos variados, incluindo alguns gratuitos.

## 🌐 Páginas Principais

- `/` - Home com carrosséis de cursos
- `/login/` - Login
- `/signup/` - Cadastro
- `/courses/my-courses/` - Meus cursos
- `/courses/acquire/` - Adquirir cursos
- `/cart/` - Carrinho
- `/checkout/` - Finalizar compra
- `/account/` - Minha conta
- `/admin/` - Painel administrativo

## 🔄 Comandos Úteis

### Parar os containers

```bash
docker-compose down
```

### Ver logs

```bash
docker-compose logs -f web
```

### Executar migrations

```bash
docker-compose exec web python manage.py migrate
```

### Criar novas migrations

```bash
docker-compose exec web python manage.py makemigrations
```

### Acessar o shell do Django

```bash
docker-compose exec web python manage.py shell
```

### Coletar arquivos estáticos

```bash
docker-compose exec web python manage.py collectstatic
```

## 📧 Configuração de Email

Para desenvolvimento, o sistema usa o backend de console (emails aparecem no terminal).

Para produção, configure as variáveis no `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

## 🔗 Integração com Área do Curso

A plataforma redireciona para uma aplicação externa de cursos usando tokens assinados.

Configure a URL no `.env`:

```env
COURSE_AREA_BASE_URL=http://localhost:7000
```

## 🐛 Troubleshooting

### Porta 8000 já em uso

Altere a porta no `docker-compose.yml`:

```yaml
nginx:
  ports:
    - "9000:80"  # Mude 8000 para outra porta
```

### Problemas com permissões

```bash
docker-compose down -v
docker-compose up --build
```

### Resetar o banco de dados

```bash
docker-compose down -v
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py seed_courses
```

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

Desenvolvido com ❤️ para promover inclusão e educação.
