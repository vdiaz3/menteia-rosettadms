# RosettaDMS: visión y arquitectura

## Problema
Las marcas (por ejemplo, armadoras en México) operan redes de cientos de dealers con DMS distintos: web, escritorio, terminal, Citrix o desarrollos propios. Integrar cada uno por API es caro, lento y depende del proveedor del DMS. El resultado es una marca sin visibilidad, dealers que capturan dos veces y clientes que esperan.

## Solución
1. **Acceso por usuario dedicado.** El dueño del DMS crea un usuario con los permisos que decida.
2. **Agentes con computer use.** Operan el DMS como un asesor: descargan reportes, leen órdenes, inventario, partes y citas, y capturan citas o reservas.
3. **Playbooks por DMS.** Cada DMS se mapea una vez y el playbook se reutiliza en todos los dealers que lo usan. Se reentrena solo si cambian las pantallas.
4. **Rosetta Schema.** Modelo canónico al que se traduce todo: `Dealer`, `Vehiculo(VIN)`, `OrdenReparacion`, `Falla(codigo, sintoma)`, `Parte(SKU, existencia, consumo)`, `Cita`, `UnidadInventario`, `Lead`, `Encuesta`.
5. **Entrega a la marca.** Diaria u horaria vía API REST, webhooks o directo al data lake (S3, BigQuery, Snowflake, Azure).
6. **Canal de regreso (bidireccional).** API y **servidor MCP** para que los chatbots de WhatsApp y los agentes de la marca consulten disponibilidad, agenden citas y vean el estatus en cualquier dealer.
7. **Super cerebro.** Benchmark nacional de dealers, predicción de demanda de partes (orden JIT), alerta temprana de calidad y consultas en lenguaje natural.

## Componentes
| Componente | Responsabilidad |
|---|---|
| Orquestador de sesiones | Cola de trabajos por dealer, horarios, reintentos |
| Workers computer use | VM/escritorio aislado por sesión, grabación de pantalla y registro de acciones |
| Bóveda de credenciales | Cifrado y rotación, sin acceso humano |
| Normalizador | Extracción → Rosetta Schema, validación y deduplicación |
| Gateway API / MCP | Lectura de datos y acciones de escritura con reglas y límites |
| Motor predictivo | Pronóstico de partes JIT, anomalías, patrones de falla |
| Consola de marca | Tablero nacional, alertas, consultas en lenguaje natural |

## Funciones derivadas de quejas comunes
Agenda 24/7 con disponibilidad real · balanceo de capacidad de taller · pieza lista antes de la cita (pre-picking por VIN y síntoma) · estatus del auto en vivo · aprobación digital de trabajos adicionales · recalls proactivos por VIN · vigilancia del tiempo de respuesta a leads · inventario de unidades verificado · historial unificado del cliente · pre-validación de garantías · NPS con cierre de ciclo.

## Modelo de negocio
SaaS pagado por la marca, por dealer conectado al mes. Gratis para el dealer. Planes: Piloto (30 días, 10 dealers), Red Nacional y Enterprise.

## Riesgos a gestionar
- Términos de licencia de cada DMS respecto a usuarios adicionales o automatizados: el dealer debe revisarlos.
- Privacidad (LFPDPPP): minimización y seudonimización de datos personales hacia la marca.
- Carga operativa en el DMS: extracciones pesadas fuera de horario.
