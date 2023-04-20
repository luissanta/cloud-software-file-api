from io import BytesIO
import os
from typing import final
import uuid

from sqlalchemy import func
from app.exceptions.file_exception import FileNotFound
from app.models import db, File
from smb.SMBConnection import SMBConnection  

class IFile:

    def get(self,id) -> File:
        pass

    def save(self,id, name, file) -> int:
        pass

class FileManager:
    __manager = None
    def __init__(self, manager: IFile) -> None:
        self.__manager = manager
        super().__init__()
    
    @final
    def get_file(self, id)->File:
        return self.__manager.get(id)

    @final
    def save_file(self, new_format, file):
        return self.__manager.save(new_format, file)
    
class DatabaseFileStorage(IFile):

    def get(self, file) -> File:
        return File.query.get_or_404(file.id)
    
    def save(self,new_format, file) -> int:
        try:
            fetched_file = File.query.get_or_404(id)
            fetched_file.compressed_name = file.compressed_name
            fetched_file.compressed_data = file.compressed_data
            return fetched_file
        except Exception as ex:
            raise FileNotFound(ex)
        
class NetworkFileStorage(IFile):

    smb_username = os.getenv("smb_username", "")
    smb_password =  os.getenv("smb_password", "")
    smb_server_ip = os.getenv("smb_server_ip", "") 
    smb_folder_name = os.getenv("smb_folder_name", "")

    def get(self,file) -> File:

        fetched_file = File.query.get_or_404(file.id)        
        extension_original_name = fetched_file.original_name.split('.')
        conn = SMBConnection(self.smb_username, self.smb_password,remote_name='',my_name='', use_ntlm_v2=True, is_direct_tcp=True)
        conn.connect(self.smb_server_ip, 445)     

        memoria = BytesIO()    
        file_obj = conn.retrieveFile(self.smb_folder_name, "\\public\\original\\"+fetched_file.temporal_name+"."+extension_original_name[1], memoria)    
        memoria.seek(0)
        fetched_file.original_data = memoria.read()
        memoria.close()
        conn.close()               
        
        return fetched_file
    
    def save(self,new_format,file) -> int:
        
        temporal_name = file.temporal_name
        conn = SMBConnection(self.smb_username, self.smb_password,remote_name='',my_name='', use_ntlm_v2=True, is_direct_tcp=True)
        conn.connect(self.smb_server_ip, 445)            
        conn.storeFile(self.smb_folder_name, "\\public\\compressed\\"+temporal_name+"."+new_format,BytesIO(file.compressed_data))                   
        conn.close()
        
        return id