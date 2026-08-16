# Despliegue de TechMind AI — Backend en AWS (EC2 + ECR)

Este documento describe paso a paso cómo se desplegó el backend de TechMind AI en un contenedor Docker corriendo sobre una instancia EC2, usando Amazon ECR como registro de imágenes. Complementa al `README.md` principal del proyecto.

## Arquitectura del despliegue

```
[Desarrollador] --docker build/push--> [Amazon ECR] --docker pull--> [EC2 + Docker] --puerto 8000--> [Internet]
```

- **ECR (`824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind`):** repositorio privado donde se almacena la imagen Docker del backend.
- **EC2:** instancia donde corre el contenedor de forma persistente, expuesto en el puerto `8000`.
- **Security Group:** controla qué tráfico puede llegar a la instancia (SSH y el puerto de la API).

## 1. Requisitos previos

- AWS CLI configurado con credenciales que tengan permisos sobre ECR y EC2.
- Docker instalado tanto en la máquina de build como en la instancia EC2.
- Una instancia EC2 con Amazon Linux (o similar) y Docker corriendo.
- El archivo `.env` con las variables reales (nunca se sube al repo ni a la imagen).

## 2. Construir y subir la imagen a ECR

Esto se hace en la máquina de desarrollo (o en un pipeline de CI), **no** en la EC2:

```bash
# Autenticarse con ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 824508926051.dkr.ecr.us-east-1.amazonaws.com

# Construir la imagen desde la carpeta backend/ (donde está el Dockerfile)
docker build -t 824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest .

# Subir la imagen al repositorio
docker push 824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest
```

> Como se usa el tag `:latest`, hay que asegurarse de que el `push` termine completamente antes de hacer `pull` desde la EC2, ya que Docker no siempre detecta una versión nueva bajo el mismo tag si cree que ya la tiene en caché.

## 3. Levantar el contenedor en EC2

Conectarse por SSH a la instancia y ejecutar:

```bash
# Autenticarse con ECR desde la EC2
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 824508926051.dkr.ecr.us-east-1.amazonaws.com

# Descargar la imagen
docker pull 824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest

# Levantar el contenedor con las variables de entorno necesarias
docker run -d -p 8000:8000 --name techmind \
  --env-file .env \
  824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest
```

El archivo `.env` en la EC2 debe contener al menos:

```
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_NAME=...
DB_PORT=3306
MODELO_URL=...
DEEPSEEK_API_KEY=...
OPENAI_API_KEY=...
```

> **Importante:** `DB_PASSWORD` no tiene valor por defecto en `config.py` — si falta, la app falla al iniciar. En esta etapa del proyecto se usó un valor placeholder porque RDS todavía no está conectado.

## 4. Actualizar el backend (nueva versión)

Cada vez que hay cambios en el código, el flujo de actualización es:

```bash
# En la EC2: eliminar el contenedor anterior
docker stop techmind
docker rm techmind

# Descargar la nueva imagen
docker pull 824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest

# Levantar el contenedor actualizado
docker run -d -p 8000:8000 --name techmind \
  --env-file .env \
  824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest
```

Script de referencia (`deploy.sh`) para automatizar este proceso en la EC2:

```bash
#!/bin/bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 824508926051.dkr.ecr.us-east-1.amazonaws.com
docker pull 824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest
docker stop techmind 2>/dev/null
docker rm techmind 2>/dev/null
docker run -d -p 8000:8000 --name techmind \
  --env-file .env \
  824508926051.dkr.ecr.us-east-1.amazonaws.com/deploy/techmind:latest
```

> Con una sola instancia y un solo contenedor hay unos segundos de downtime entre que se detiene el contenedor viejo y arranca el nuevo. Es aceptable para esta etapa del proyecto; para producción se podría evaluar un Load Balancer con más de una instancia o un servicio orquestado (ECS/EKS).

## 5. Verificar el estado del contenedor

```bash
# ¿Está corriendo?
docker ps -a

# Estado puntual
docker inspect --format='{{.State.Status}}' techmind

# Logs (para confirmar que arrancó sin errores)
docker logs techmind
docker logs -f techmind        # en tiempo real
docker logs --tail 100 techmind

# Uso de recursos
docker stats techmind
```

Probar que el servicio responde:

```bash
curl -i http://localhost:8000/health
```

Desde el navegador (requiere la IP pública de la EC2 y el puerto 8000 abierto en el Security Group):

```
http://<IP_PUBLICA_EC2>:8000/health
```

Respuesta esperada:
```json
{ "status": "ok" }
```

## 6. Configuración de red (Security Group)

Reglas de entrada (*Inbound rules*) necesarias en la instancia:

| Tipo        | Puerto | Origen                          | Motivo                          |
|-------------|--------|----------------------------------|----------------------------------|
| SSH         | 22     | IP del desarrollador             | Acceso administrativo            |
| Custom TCP  | 8000   | `0.0.0.0/0` (o restringido)      | Acceso a la API desde el frontend|

> Se recomienda asignar una **Elastic IP** a la instancia para evitar que la IP pública cambie cada vez que se detiene/inicia (por ejemplo, al cambiar el tipo de instancia).

## 7. Incidente resuelto: memoria insuficiente (Exit Code 137)

Durante el despliegue se presentó un error **137** (`SIGKILL`, generalmente por Out of Memory) al arrancar el contenedor.

**Diagnóstico:**
```bash
free -h
dmesg -T | egrep -i 'killed process|out of memory'
```

La instancia original (`t2.micro`/`t3.micro`, 913 MB de RAM) no era suficiente para cargar el modelo (`.joblib`, ~71 MB) junto con el resto de la aplicación.

**Solución aplicada:** se cambió el tipo de instancia a **`t3.small`** (2 GB de RAM) desde la consola de AWS:

1. EC2 → Instances → seleccionar la instancia
2. *Instance state* → **Stop instance**
3. *Actions* → *Instance settings* → **Change instance type** → `t3.small`
4. *Instance state* → **Start instance**

> Nota: cambiar el tipo de instancia no borra el contenido del volumen EBS; el contenedor detenido debe volverse a levantar manualmente tras el reinicio.

**Alternativa/complemento:** agregar swap como red de seguridad adicional:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

## 8. Otro incidente resuelto: variables de entorno faltantes

Al actualizar el código, el contenedor fallaba con:

```
Modelo no encontrado localmente y falta MODELO_URL en el entorno
openai.OpenAIError: Missing credentials... set the OPENAI_API_KEY environment variable
```

**Causa:** el `docker run` no incluía las variables de entorno requeridas por la nueva versión del código.

**Solución:** pasar el archivo `.env` completo con `--env-file .env` al momento de levantar el contenedor (ver sección 3).

## 9. Pendientes de infraestructura

- Asignar una **Elastic IP** para tener una URL/IP estable.
- Conectar **RDS (MySQL)** y reemplazar `DB_PASSWORD`/`DB_HOST` placeholder por valores reales.
- Configurar un **healthcheck** en el contenedor (`--health-cmd` con `curl` sobre `/health`).
- Evaluar CI/CD (GitHub Actions / CodePipeline) para automatizar build → push → deploy.
- Ajustar permisos IAM del usuario usado en CLI (actualmente requiere completar acciones desde la consola por falta de permisos como `ec2:StopInstances`).
