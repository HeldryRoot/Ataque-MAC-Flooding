# Ataque-MAC-Flooding

<img width="654" height="276" alt="image" src="https://github.com/user-attachments/assets/edfcc30b-66cc-4465-95dc-13ea7e5fda80" />

**LABORATORIO DE SEGURIDAD DE REDES**

**MAC FLOODING**

_Documentación Técnica Profesional_

**Estudiante:**

**Heldry Terrero**

Matrícula: 2025-0719

Materia: Seguridad de Redes

Fecha: Junio 2026

  
  

# Aviso de Uso Responsable

|   |
|---|
|**⚠  AVISO IMPORTANTE — LEA ANTES DE UTILIZAR ESTE MATERIAL**<br><br>Este proyecto fue desarrollado únicamente con fines educativos, académicos<br><br>y de laboratorio controlado, en el marco de la asignatura Seguridad de Redes.<br><br>Los scripts, comandos y técnicas incluidos en este repositorio deben ejecutarse<br><br>SOLAMENTE en entornos propios o autorizados, tales como:<br><br>   • Simuladores: PNetLab, GNS3, EVE-NG<br><br>   • Laboratorios internos de práctica académica<br><br>   • Redes virtuales de prueba bajo supervisión docente<br><br>QUEDA ESTRICTAMENTE PROHIBIDO:<br><br>   • Utilizar este material en redes públicas, corporativas o de terceros<br><br>     sin autorización explícita y por escrito.<br><br>   • Interceptar, alterar o interrumpir comunicaciones ajenas.<br><br>   • Aplicar estas técnicas con fines maliciosos o fraudulentos.<br><br>El uso indebido de estas herramientas puede constituir un delito tipificado<br><br>en las leyes de ciberseguridad y delitos informáticos vigentes.<br><br>El autor de este material no se hace responsable del uso indebido del mismo.|

  
  

# Documentación Técnica — Ataque MAC Flooding

|**Campo**|**Valor**|
|---|---|
|Estudiante|Heldry Terrero|
|Matrícula|2025-0719|
|Materia|Seguridad de Redes|
|Script|mac_flooding.py|
|Fecha|Junio 2026|
|Plataforma|PNetLab — Kali Linux|

# 1. Objetivo del Laboratorio

Demostrar cómo el desbordamiento de la tabla CAM de un switch puede convertirlo en un hub, exponiendo el tráfico unicast de todos los dispositivos conectados a cualquier puerto del mismo segmento.

# 2. Objetivo del Script

Generar y enviar masivamente frames Ethernet con MACs de origen únicas y aleatorias para llenar la tabla CAM del switch, forzándolo a operar en modo failopen donde retransmite todos los frames por todos sus puertos.

# 3. Requisitos

## 3.1 Software

•        Python 3.7 o superior

•        Scapy 2.4.3: sudo apt install python3-scapy

•        Kali Linux con interfaz eth1 conectada al switch

•        Privilegios de root (sudo)

## 3.2 Red

•        Atacante: 20.25.7.100/24 en eth1

•        Víctima: 20.25.7.10/24

•        Gateway/Router: 20.25.7.1/24

•        Red: 20.25.7.0/24

# 4. Parámetros del Script

|**Parámetro**|**Descripción**|**Default**|
|---|---|---|
|-i / --iface|Interfaz de red|Requerido|
|-c / --count|Número de paquetes (0=infinito)|0|
|-d / --delay|Delay entre envíos en segundos|0|
|-v / --verbose|Mostrar detalle de cada paquete|False|

# 5. Cómo se Ejecutó el Script

**Comando utilizado durante la demostración:**

sudo python3 mac_flooding.py -i eth1

sudo python3 mac_flooding.py -i eth1 -c 10000

|   |
|---|
|**Resultado esperado en pantalla**<br><br>[*] Interfaz   : eth1<br><br>[*] Tabla CAM tipica: 8,000 - 128,000 entradas<br><br>[STATS] Paquetes:  10,000 \| MACs:   5,000 \| Vel:  2000 pkt/s<br><br>[STATS] Paquetes:  50,000 \| MACs:  25,000 \| Vel:  3500 pkt/s|

# 6. Funcionamiento del Ataque

El script genera pares de MACs unicast aleatorias (SRC y DST) y construye frames Ethernet mínimos de 64 bytes con payload aleatorio. Los frames se envían en lotes de 200 para maximizar el throughput. Cada MAC de origen única es aprendida por el switch como un nuevo host en el puerto del atacante, llenando progresivamente la tabla CAM.

•        Paso 1: Se generan MACs aleatorias con primer octeto par (unicast) y bit 1 activo (locally-admin).

•        Paso 2: Se construyen frames Ethernet con payload aleatorio de 64 bytes.

•        Paso 3: Los frames se agrupan en lotes de 200 y se envían con sendp().

•        Paso 4: El switch aprende cada MAC de origen como una nueva entrada en la tabla CAM.

•        Paso 5: Al llenarse la tabla CAM, el switch no puede aprender más MACs.

•        Paso 6: El switch entra en modo failopen: todos los frames se reenvían por todos los puertos.

# 7. Verificación del Ataque

**Para confirmar que el ataque fue exitoso, se ejecutaron los siguientes comandos:**

Switch# show mac address-table count

Switch# show mac address-table dynamic | count

Switch# show processes memory sorted | head

|   |
|---|
|**¿Qué se debe observar?**<br><br>show mac address-table count muestra el contador creciendo rápidamente.<br><br>Después del flooding, el tráfico entre otros hosts aparece en Wireshark del atacante.<br><br>El switch puede volverse lento o inestable por el consumo de memoria.|

# 8. Contramedidas

Port Security limita el número máximo de MACs que pueden aprenderse en un puerto. Con la opción sticky se aprenden automáticamente las MACs legítimas y se bloquean las nuevas que superen el límite.

Switch(config-if)# switchport port-security

Switch(config-if)# switchport port-security maximum 2

Switch(config-if)# switchport port-security violation restrict

Switch(config-if)# switchport port-security mac-address sticky

Switch# show port-security interface ethernet 0/1

# 9. Conclusión

El MAC Flooding explota una limitación de hardware presente en todos los switches no gestionados y en switches gestionados sin Port Security. Es uno de los ataques más fáciles de ejecutar y uno de los que mayor impacto tiene en la confidencialidad del tráfico de red local.  
  
Link de GitHub: https://github.com/HeldryRoot/Ataque-MAC-Flooding.git

Link del Video de Youtube: https://youtu.be/XBmTnsBFtSA?si=Whqb7PZ_OfxnE7qj

**Heldry Terrero — Matrícula 2025-0719 — Seguridad de Redes — Junio 2026**
