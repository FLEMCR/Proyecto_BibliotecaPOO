# Sistema de Gestión de Biblioteca Universitaria

Trabajo grupal de **Programación Orientada a Objetos** en Python. Gestiona el catálogo de una
biblioteca universitaria, las membresías de sus miembros y el ciclo completo de préstamo,
devolución, mora y reservas.

---

## Qué necesitamos usar

| Módulo del sistema | Funcionalidad |

|---|---|

| Catálogo | alta, edición, baja lógica y búsqueda por ISBN, género o categoría jerárquica |

| Ejemplares | cada título tiene 1..N copias; la disponibilidad se actualiza sola al prestar y devolver |

| Títulos agotados | al quedar en 0 se calcula una fecha estimada de reposición, editable desde el menú |

| Reservas | cola de hasta 3 personas por título; al volver un ejemplar se avisa al primero |

| Membresías | Estudiante, Docente y Egresado: crear, renovar, cancelar y cambiar de tipo |

| Préstamos | registrar, renovar y devolver, con límite por membresía y días según el tipo |

| Mora | S/ 0.50 por día con tope de S/ 10 y descuento según membresía |

| Caja | cobro de multas con IGV 18 % discriminado |

| Reportes | catálogo, préstamos activos, morosos, reservas, uso por tipo de miembro, historial |

| Mapa de salas | matriz `sección × estante` dibujada en consola |

| Persistencia | 3 archivos JSON con validación; si falta o está roto, genera una plantilla |

| Diagnóstico | revisa Python, codificación, archivos, conteos y referencias rotas |

---
