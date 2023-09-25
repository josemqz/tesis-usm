# backend-titulo
Backend de sitio web diseñado para visualizar los resultados de Crowd Counting en el campus San Joaquín de la Universidad Técnica Federico Santa María.  


## Instrucciones

### Crear e ingresar a entorno virtual

Instalar módulo de entornos virtuales  
```
sudo apt update  
sudo apt install python3-venv
```  

Crear entorno virtual  
```
python3 -m venv backend-env
```

Activar entorno  
```
source ./backend_env/bin/activate
```  
  
Desactivar entorno  
```
deactivate
```  

### Instalar librerías requeridas
```
python3 -m pip install -r requirements.txt
```

### Ejecutar servidor
```
export FLASK_APP=main  
flask run
```

### Operaciones en Base de Datos

Abrir entorno de Flask  
```
export FLASK_APP=main  
flask shell  
```
  
Añadir datos creados manualmente  
```
from src import db
from src.models.models import Sala, Ocupacion  
  
sala_a000 = Sala(svg_id='rect5195', nombre='A-000', ocupacion_max=100)  
  
ocupacion_00_a000 = Ocupacion(sala_id='A-000'  
                            ocupacion_actual=0  
                            timestamp='00:00:00')  
  
db.session.add(sala_a000)  
db.session.add(ocupacion_00_a000)  
```  

Aplicar los cambios  
```
db.session.commit()
```  
  
Eliminar tablas (útil en caso de actualizar columnas)  
```
from src import db  
db.drop_all()
```

### Operaciones definidas en server

#### Sala
```
from src.models.models import Sala  
  
Sala.crear(svg_id, nombre, ocupacion_max)  
Sala.get_salas()  
Sala.get_sala_by_id(id)  
Sala.get_sala_by_nombre(nombre)
```

#### Ocupación
```
from src.models.models import Ocupacion  
  
Ocupacion.crear(sala_id, ocupacion_actual, timestamp)  
Ocupacion.get_ocupaciones()  
Ocupacion.get_ocupaciones_by_sala_id(sala_id)  
Ocupacion.get_latest_ocupacion_by_sala_id(sala_id)  
Ocupacion.delete_ocupaciones_by_id(id)
```
  
_Referencia: https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application_
