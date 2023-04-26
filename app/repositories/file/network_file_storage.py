from io import BytesIO
from smb.SMBConnection import SMBConnection
from .i_File import IFile
from app.models.models import File
import os


class NetworkFileStorage(IFile):
    smb_username = os.getenv("smb_username", "")
    smb_password = os.getenv("smb_password", "")
    smb_server_ip = os.getenv("smb_server_ip", "")
    smb_folder_name = os.getenv("smb_folder_name", "")

    @classmethod
    def extract_name(cls, file):
        name = file.original_name.split('.')
        return file.original_name, "\\public\\original\\", name[1]

    def get(self, file_id) -> tuple:
        fetched_file = File.query.get_or_404(file_id)
        original_name, path, extension = self.extract_name(fetched_file)
        conn = SMBConnection(
            self.smb_username,
            self.smb_password,
            remote_name='',
            my_name='',
            use_ntlm_v2=True,
            is_direct_tcp=True
        )
        conn.connect(self.smb_server_ip, 445)
        memoria = BytesIO()
        memoria.seek(0)
        data = memoria.read()
        memoria.close()
        conn.close()

        return data, original_name

    def save(self, file_name, file, new_format) -> int:
        temporal_name = file.temporal_name
        conn = SMBConnection(
            self.smb_username,
            self.smb_password,
            remote_name='',
            my_name='',
            use_ntlm_v2=True,
            is_direct_tcp=True
        )
        conn.connect(self.smb_server_ip, 445)
        conn.storeFile(self.smb_folder_name, "\\public\\compressed\\" + temporal_name + "." + new_format,
                       BytesIO(file.compressed_data))
        conn.close()

        return id
