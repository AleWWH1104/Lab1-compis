# 🧪 Laboratorio 3 — Opción A: DigitalOcean con ANTLR + REST API

## 📋 Descripción General

En esta opción usarás **ANTLR** para parsear un archivo de Terraform y mapear el resultado a llamadas de **API REST de DigitalOcean** con Python para administrar Droplets. Utilizarás Docker para configurar y ejecutar tu entorno.

La idea central es que experimentes el proceso de crear un parser "pseudo-compilador" para un DSL que analiza y luego transforma a otro conjunto de operaciones — un caso de uso real de compiladores en la vida real. Exactamente así funciona Terraform por dentro.

Este lab tiene **tres partes** que deben completarse en orden.

* **Modalidad: Individual**

---

## 💰 Costo

DigitalOcean históricamente ofrece crédito gratuito a cuentas nuevas — verifica si sigue vigente en [digitalocean.com](https://www.digitalocean.com). De lo contrario, el Droplet más pequeño cuesta ~$6/mes; si lo destruyes de inmediato tras verificar el lab, el costo real es de centavos.

> ⚠️ **No realices operaciones indebidas con el API Token de DigitalOcean. No cambies el tamaño del Droplet por ninguna razón. No seguir instrucciones impactará negativamente tu nota.**

---

## 🧰 Parte 1: Terraform Real

Antes de parsear Terraform con ANTLR, debes entender cómo funciona Terraform real. En esta parte crearás y destruirás un Droplet usando Terraform directamente.

### Requisitos

- Terraform instalado localmente, o usa la imagen oficial de Docker de HashiCorp.
- Tu API Token de DigitalOcean.

### 1. Archivos de Configuración

Los archivos de Terraform están en la carpeta `terraform/`. Revísalos:

**`terraform/main.tf`** — Define el provider y el recurso:
```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.digitalocean_token
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-20-04-x64"
  name   = "example-droplet"
  region = "nyc1"
  size   = "s-1vcpu-1gb"
}

variable "digitalocean_token" {
  description = "El token de API de DigitalOcean."
  type        = string
  sensitive   = true
}

output "droplet_ip" {
  description = "La dirección IP del Droplet."
  value       = digitalocean_droplet.web.ipv4_address
}
```

**`terraform/terraform.tfvars`** — Reemplaza `token` con tu API Token real:
```hcl
digitalocean_token = "TU_TOKEN_AQUI"
```

> ⚠️ **No subas `terraform.tfvars` a GitHub — contiene tu token.**

### 2. Comandos de Terraform

Desde la carpeta `terraform/`:

**Inicializar Terraform:**
```bash
terraform init
```

**Ver el plan de ejecución:**
```bash
terraform plan
```

**Crear el Droplet:**
```bash
terraform apply
```
Escribe `yes` cuando se solicite confirmación.

**🚨 Destruir el Droplet inmediatamente después de verificarlo:**
```bash
terraform destroy
```
Escribe `yes` cuando se solicite confirmación. **Debes destruirlo para evitar cargos.**

### 3. Evidencia

Toma capturas de pantalla de cada operación y guárdalas para incluirlas en tu entrega.

---

## 🔧 Parte 2: Bash + REST API de DigitalOcean

En esta parte crearás y destruirás un Droplet directamente usando la **API REST de DigitalOcean** con scripts de Bash y Docker, sin usar Terraform.

### Archivos

Los scripts están en la carpeta `bash/`:

- `create_droplet.sh` — Crea el Droplet vía REST API usando `curl`.
- `destroy_droplet.sh` — Destruye el Droplet usando su ID.
- `docker-compose.yml` — Levanta el entorno con tu API Token configurado.

### 1. Configurar el Token

Edita `bash/docker-compose.yml` y reemplaza `token` con tu API Token real:
```yaml
environment:
  - API_TOKEN=TU_TOKEN_AQUI
```

También reemplaza el token en `bash/create_droplet.sh` y `bash/destroy_droplet.sh`.

### 2. Construir la Imagen de Docker

Desde la carpeta `bash/`:
```bash
docker-compose build
```

### 3. Crear el Droplet

```bash
docker-compose run digitalocean /usr/local/bin/create_droplet.sh
```

Guarda el **Droplet ID** que imprime el script — lo necesitarás para destruirlo.

### 4. Destruir el Droplet

```bash
docker-compose run digitalocean /usr/local/bin/destroy_droplet.sh
```

### 5. Evidencia

Toma capturas de pantalla del Droplet siendo creado y destruido.

---

## 🤖 Parte 3: Parser con ANTLR

Esta es la parte principal del laboratorio. Usarás ANTLR para parsear el archivo `program/main.tf` y el listener llamará a la API REST de DigitalOcean para crear el Droplet — exactamente lo que hace Terraform por dentro.

### 1. Construir y Ejecutar el Contenedor Docker

Desde el directorio raíz de esta opción (`option-do/`):

```bash
docker build --rm . -t lab3-do && docker run --rm -ti -v "$(pwd)/program":/program lab3-do
```

### 2. Dentro del Contenedor

**Paso 1 — Generar el lexer y parser con ANTLR:**
```bash
antlr -Dlanguage=Python3 TerraformSubset.g4
```

**Paso 2 — Ejecutar `apply` (crear el Droplet):**
```bash
python3 terraform_parser.py main.tf apply
```

El compilador parseará `main.tf`, llamará a la API de DigitalOcean, creará el Droplet, imprimirá su **IP y ID**, y guardará un archivo `.tfstate` con esta información.

**Paso 3 — Verificar que el Droplet está activo:**

Haz un `ping` a la IP que imprimió el compilador:
```bash
ping <IP_DEL_DROPLET>
```

**Paso 4 — Ejecutar `destroy` (destruir el Droplet):**
```bash
python3 terraform_parser.py main.tf destroy
```

El compilador leerá el `.tfstate`, obtendrá el ID del Droplet, y llamará a la API para destruirlo.

### 3. Salida Esperada (apply)

```
[var] token = ****
[*] Creating droplet...
[+] Droplet created with ID: 123456789
[*] Waiting for droplet to become active and assigned an IP...
[✓] Droplet available at IP: 192.168.1.100
[*] State saved to terraform.tfstate
```

### 4. Salida Esperada (destroy)

```
[*] Reading state from terraform.tfstate...
[*] Deleting droplet ID: 123456789...
[✓] Droplet destroyed successfully.
```

---

## ⚙️ Requerimientos de Implementación

Tu implementación debe soportar los siguientes comportamientos. El código base ya implementa el `apply`; debes completar el resto:

- **`python3 terraform_parser.py main.tf apply`** — Parsea el archivo `.tf`, crea el Droplet vía REST API, e imprime la IP y el ID.
- **`.tfstate`** — Al hacer `apply`, el parser debe guardar un archivo `terraform.tfstate` con un JSON que contenga el nombre, ID e IP del Droplet creado.
- **`python3 terraform_parser.py main.tf destroy`** — Lee el `.tfstate`, obtiene el ID del Droplet, y llama a la REST API para destruirlo.

El archivo `.tfstate` debe tener la siguiente estructura:
```json
{
  "droplet_name": "example-droplet",
  "droplet_id": 123456789,
  "droplet_ip": "192.168.1.100"
}
```

---

## ⭐ Puntos Extra

- Investiga cómo se configuran las **llaves SSH** para un Droplet en DigitalOcean.
- Añade soporte en tu implementación con ANTLR para leer una llave SSH desde el archivo `.tf` y adjuntarla al Droplet cuando se cree.
- Ingresa al Droplet vía SSH una vez creado y muestra evidencia.
- **Ponderación: 1 punto neto extra.**

---

## 📁 Estructura de Archivos

```
option-do/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── python-venv.sh
├── commands/
│   ├── antlr
│   └── grun
├── program/
│   ├── TerraformSubset.g4     # La gramática ANTLR del DSL
│   ├── terraform_parser.py    # El parser/listener que llama a la API de DO
│   └── main.tf                # El archivo Terraform a parsear (pon tu token aquí)
├── bash/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── create_droplet.sh      # Parte 2: crear Droplet con Bash
│   └── destroy_droplet.sh     # Parte 2: destruir Droplet con Bash
└── terraform/
    ├── main.tf                # Parte 1: Terraform real
    ├── variables.tf
    └── terraform.tfvars       # Pon tu token aquí (NO subir a GitHub)
```

---

## 📋 Entregables

- **Video de YouTube no listado** mostrando las tres partes: Terraform real, Bash + REST API, y el parser con ANTLR (apply y destroy).
- **Repositorio de GitHub** con todo tu código. **No subas tu API Token ni el archivo `terraform.tfvars`.**
- **Escrito breve:** explica cómo tu parser con ANTLR imita el funcionamiento interno de `terraform apply` y `terraform destroy`. ¿Qué representa el `.tfstate` en el Terraform real?
