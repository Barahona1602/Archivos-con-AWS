
# *ENDPOINTS*

# Comando open - `http://{ip-del-grupo}:{puerto-del-grupo}/open`

* Método: POST
* Body - Content-Type: application/json

## Ejemplo del body:

```json

{
    "name": "/path/to/file.txt",
    "type": "server"
}
    
```

* Respuestas en JSON:

## Respuesta exitosa (status 200):

```json
{
    "content": "file content ..."
}
```

## Respuesta fallida (status 200):

- Si no existe el archivo

```json
{
    "content": null
}
```


<br>
<br>
<br>
<br>

# Comando backup - `http://{ip-del-grupo}:{puerto-del-grupo}/backup`

* Método: POST
* Body - Content-Type: application/json

## Ejemplo del body:
```json
{
    "type": "bucket",
    "name": "backup_folder_name",
    "structure": {
        "carpeta alvaro": {
            "mia": {
            "_files": [
                {
                    "file_name": "yanosale",
                "file_contents": "asfasfasfsda si sale"
                }
            ]
            },
            "_files": [
                {
                "file_name": "prueba 2",
                "file_contents": "Este es el contenido del archivo 2"
            }
            ]
        }
    }
}
```	

* Respuestas en JSON:

## Respuesta exitosa (status 200):

```json

{
    "status": true
}
```

## Respuesta fallida (status 200):

- Si no se pudo crear la carpeta del backup

```json

{
    "status": false
}
```

<br>
<br>
<br>
<br>

# Comando recovery - endpoint - `http://{ip-del-grupo}:{puerto-del-grupo}/recovery`

* Método: POST
* Body - Content-Type: application/json

## Ejemplo del body:
```json
{
    "name": "backup_folder_name",
    "type": "server"
}
```

* Respuestas en JSON:

## Respuesta exitosa (status 200):
```json

{
    "type": "server",
    "structure": {
        "carpeta alvaro": {
            "mia": {
            "_files": [
                {
                "file_name": "yanosale",
                "file_contents": "asfasfasfsda si sale"
                }
            ]
            },
            "_files": [
            {
                "file_name": "prueba 2",
                "file_contents": "Este es el contenido del archivo 2"
            }
            ]
        }
    }
}
```

## Respuesta fallida (status 200)

- Si no existiera la carpeta

```json
{
    structure: null
}
```




# Notas:
- Para facilitar la comunicación todo devolverá un status 200, y en el body se especificará de alguna forma si fue exitoso o no.
- Se usará siempre el método POST para enviar los datos.