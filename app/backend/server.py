from fastapi import FastAPI,File,UploadFile,HTTPException
from app.utils.modelhelper_code_alignment import aligner
from app.utils.modelhelper_docstring_gen import generating_docstring
import os
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/comment_align")
async def comment_align(file : UploadFile = File(...)):
    content = await file.read()
    path = 'temp_file.py'
    with open (path,'wb') as f:
        f.write(content)
    try :
        dataframe = aligner(path)
        return {'data': dataframe.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally :
        os.remove(path)

@app.post("/docstring")
async def docstring(file : UploadFile = File(...)):
    content = await file.read()
    path = 'temp_docstring_file.py'
    with open(path, 'wb') as f:
        f.write(content)
    try :
        dataframe = generating_docstring(path)
        return {'data': dataframe.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally :
        os.remove(path)




