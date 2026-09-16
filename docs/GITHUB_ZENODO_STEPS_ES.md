# Pasos para publicar el repositorio y obtener el DOI

## 1. Preparación local

Descomprima el proyecto, abra una terminal dentro de la carpeta y ejecute:

```bash
python src/generate_dataset.py
python -m unittest discover -s tests -v
```

No continúe si la validación no termina con `OK`.

## 2. Crear el repositorio vacío en GitHub

1. Ingrese a https://github.com/new.
2. Use el nombre `stem-ia-evidence-dataset`.
3. Seleccione visibilidad `Public`.
4. No agregue README, `.gitignore` ni licencia desde GitHub; ya están incluidos.
5. Presione `Create repository`.

## 3. Inicializar y subir el proyecto

Desde la carpeta descomprimida:

```bash
git init
git branch -M main
git add .
git commit -m "Release STEM-IA evidence dataset v1.0.0"
git remote add origin https://github.com/cvidalmsu/stem-ia-evidence-dataset.git
git push -u origin main
```

Si utiliza autenticación HTTPS, GitHub solicitará iniciar sesión mediante el
administrador de credenciales o un personal access token; la contraseña normal
de la cuenta no se utiliza para operaciones Git.

## 4. Comprobar GitHub Actions

1. Abra la pestaña `Actions` del repositorio.
2. Seleccione el flujo `Validate dataset`.
3. Compruebe que la ejecución termine en verde.
4. Si falla, abra el registro, corrija el archivo y repita `git add`, `commit` y
   `push` antes de crear la versión.

## 5. Vincular GitHub con Zenodo

1. Ingrese a https://zenodo.org/ usando su cuenta de GitHub.
2. Autorice la aplicación Zenodo.
3. Abra la sección de GitHub dentro de Zenodo.
4. Active el repositorio `cvidalmsu/stem-ia-evidence-dataset`.

## 6. Crear la versión v1.0.0 en GitHub

1. En GitHub abra `Releases` y seleccione `Draft a new release`.
2. Cree la etiqueta `v1.0.0` desde la rama `main`.
3. Título sugerido: `STEM-IA Escolar Evidence Profiles Dataset v1.0.0`.
4. En la descripción indique que contiene 81 perfiles base, 81 variantes con
   conflicto, reglas, metadatos, trazabilidad, pruebas y documentación.
5. Presione `Publish release`.

Zenodo archivará automáticamente esa versión cuando la integración esté activa.

## 7. Completar el registro de Zenodo

Compruebe y complete:

- tipo de recurso: `Dataset`;
- título del dataset;
- autores en el mismo orden acordado para el artículo;
- descripción y palabras clave;
- licencia de los datos: `Creative Commons Attribution 4.0 International`;
- versión: `1.0.0`;
- financiadores y proyecto, solo si corresponde;
- related identifiers: URL del repositorio GitHub.

Guarde el DOI de versión y el DOI conceptual. El manuscrito debe citar el DOI de
la versión exacta analizada; el README puede mostrar también el DOI conceptual.

## 8. Incorporar el DOI al repositorio

Edite `CITATION.cff` y `.zenodo.json` para agregar el DOI definitivo. También
puede insertar en `README.md` el badge generado por Zenodo. Después ejecute:

```bash
git add README.md CITATION.cff .zenodo.json
git commit -m "Add Zenodo DOI for v1.0.0"
git push
```

Este commit será posterior a la versión archivada. No cambie silenciosamente
los datos de `v1.0.0`; cualquier modificación de datos debe publicarse como una
nueva versión, por ejemplo `v1.0.1` o `v1.1.0`.

## 9. Incorporar los enlaces al artículo

En el manuscrito de *Data* incluya:

```text
Dataset: [full citation and version DOI]
Dataset License: CC BY 4.0
Development repository: https://github.com/cvidalmsu/stem-ia-evidence-dataset
```

En `Data Availability Statement`, diferencie claramente el DOI archivado y el
repositorio de desarrollo.

