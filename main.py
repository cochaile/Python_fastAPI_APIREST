 # API REST: interfaz de Programación de Aplicaciones para compartir recursos
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tenadrá todas las características de una API REST
app = FastAPI()

# Acá definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
cursos_db = []

# CRUD (ABM): Read (Lectura) usa el método GET ALL: leeremos todos los cursos que haya en la base de datos

@app.get("/cursos/",response_model=list[Curso]) # Acá devolvemos todos
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST: agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos/",response_model=Curso) # Acá solo se agrega uno solo
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4()) # UUID genera un ID único e irrepetible 
    cursos_db.append(curso)
    return curso
    
# CRUD: Read (Lectura) GET (individual): Leerempos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}",response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail="Curso no encontrado") # Raise corta la ejecución
    return curso
    
# CRUD: Update (Actualización/Modificación) PUT: modificaremos un recurso que coincida con el ID que pidamos
@app.put("/cursos/{curso_id}",response_model=Curso)
def actualizar_curso(curso_id:str,curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde está el curso en nuestra lista (DB) 
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (Borrado/Baja) DELETE: eliminaremos un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}",response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso