# 🌍 Laboratorio 3: Compiladores en el Mundo Real

## 📋 Descripción General

En este laboratorio descubrirás cómo los compiladores no son solo teoría académica — son el núcleo de herramientas que miles de ingenieros usan todos los días. Tecnologías como **Terraform**, **Vercel CLI**, **Netlify** y **Kubernetes** están construidas sobre los mismos principios que estás aprendiendo en este curso: lexers, parsers, árboles sintácticos, y listeners o visitors que ejecutan acciones reales.

Tu tarea es escribir un **DSL propio**, parsearlo con **ANTLR**, y hacer que tu compilador interactúe con una API real para crear infraestructura o desplegar una aplicación en la nube. Exactamente así funciona `terraform apply` o `vercel deploy` por dentro.

* **Modalidad: Individual**

---

## 🎯 Elige tu Opción

Selecciona **una** de las cuatro opciones disponibles. Cada una demuestra el mismo principio, con diferente proveedor y costo.

| Opción | Proveedor | Costo | Carpeta |
|--------|-----------|-------|---------|
| A | DigitalOcean | Tu dinero / crédito gratuito en cuentas nuevas | `option-do/` |
| B | AWS | Crédito estudiantil / AWS Free Tier / tu dinero | `option-aws/` |
| C | GCP | Crédito estudiantil / GCP Free Trial ($300) / tu dinero | `option-gcp/` |
| D | GitHub + Vercel | ✅ **100% GRATIS, sin tarjeta de crédito** | `option-vercel/` |

> 💡 **Recomendación:** Si no tienes créditos de nube, elige la **Opción D**. Es completamente gratuita, produce un resultado visible y real (una URL pública en internet), y demuestra exactamente el mismo principio de compiladores que las otras opciones.

---

## 🧰 Detalles de Cada Opción

### 🔵 Opción A — DigitalOcean (`antlr/`)

Escribes un DSL similar a Terraform, lo parseas con ANTLR, y el listener llama a la API de DigitalOcean para crear un **Droplet real**.

**Costo:** DigitalOcean históricamente ofrece crédito gratuito a cuentas nuevas — verifica si sigue vigente en [digitalocean.com](https://www.digitalocean.com). De lo contrario, un Droplet básico cuesta ~$6/mes; si lo destruyes de inmediato, el costo real es de centavos.

📖 Instrucciones completas: [`option-do/README.md`](option-do/README.md)

---

### 🟠 Opción B — AWS (`option-aws/`)

Escribes un DSL de infraestructura, lo parseas con ANTLR, y el listener llama a la API de EC2 de AWS vía `boto3` para lanzar una **instancia real**.

**Costo:**
- **AWS Educate / AWS Academy:** créditos estudiantiles gratuitos si tu universidad tiene convenio.
- **AWS Free Tier:** cuentas nuevas incluyen una instancia `t2.micro` por 12 meses sin costo.
- **Tu propio dinero:** `t2.micro` cuesta $0.0116/hora. Si la terminas de inmediato, el costo es mínimo.

📖 Instrucciones completas: [`option-aws/README.md`](option-aws/README.md)

---

### 🟡 Opción C — GCP (`option-gcp/`)

Escribes un DSL de infraestructura, lo parseas con ANTLR, y el listener crea una **VM real en Google Cloud Compute Engine**.

**Costo:**
- **GCP Free Trial:** cuentas nuevas reciben $300 USD de crédito por 90 días (requiere tarjeta de crédito para verificación, no se cobra automáticamente).
- **Créditos estudiantiles:** via [Google Cloud for Students](https://cloud.google.com/edu/students).
- **Free Tier permanente:** la instancia `e2-micro` es elegible para el free tier de GCP (1 instancia por mes en ciertas regiones).
- **Tu propio dinero:** `e2-micro` cuesta ~$0.0084/hora.

📖 Instrucciones completas: [`option-gcp/README.md`](option-gcp/README.md)

---

### 🟢 Opción D — GitHub + Vercel (`option-vercel/`) — ✅ GRATIS

Escribes un DSL que define un sitio web. Tu compilador genera HTML, crea un repositorio en GitHub, sube el código, y lo despliega en Vercel. Al terminar, obtienes **una URL pública real y accesible desde cualquier lugar**.

**Costo:** Cero. Sin tarjeta de crédito. Solo necesitas una cuenta de GitHub y una de Vercel, ambas gratuitas.

📖 Instrucciones completas: [`option-vercel/README.md`](option-vercel/README.md)

---

## 📋 Entregables

Todos los estudiantes, independientemente de la opción elegida, deben entregar:

- **Video de YouTube no listado** (pero público) demostrando el compilador corriendo y el resultado real en la nube o en Vercel. Duración sugerida: 3–5 minutos.
- **Repositorio de GitHub** con el código fuente completo: gramática ANTLR, listener, archivo de configuración de ejemplo, y Dockerfile. **No subas llaves de API ni credenciales.**
- **Escrito breve (1–2 páginas):** explica cómo tu compilador mapea al funcionamiento real de la herramienta que elegiste. Por ejemplo: ¿cómo se compara tu listener con lo que hace Terraform al ejecutar `terraform apply`? ¿O con lo que hace Vercel CLI al ejecutar `vercel deploy`?
