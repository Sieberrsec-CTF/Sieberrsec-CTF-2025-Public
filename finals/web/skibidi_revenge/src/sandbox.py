import uuid
import os
import asyncio
import aiofiles
import aiofiles.os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

class SkibidiSandBox:
    def __init__(self, base_path, tar_bytes=None, max_workers=4):
        self.base_path = base_path
        self.id = str(uuid.uuid4())
        self.path = f"{self.base_path}/{self.id}"
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        while os.path.exists(self.path):
            self.id = str(uuid.uuid4())
            self.path = f"{self.base_path}/{self.id}"
        
        os.makedirs(self.path)
    
    async def _run_in_executor(self, func, *args):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args)
    
    async def _async_system_command(self, command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()
    
    async def upload(self, tar_bytes):
        if tar_bytes:            
            tar_path = f"{self.path}/starter.tar"
            async with aiofiles.open(tar_path, "wb") as f:
                await f.write(tar_bytes.getvalue())
            extract_command = f"tar -xf {tar_path} -C {self.path}"
            returncode, stdout, stderr = await self._async_system_command(extract_command)
            
            return "Successfully uploaded and extracted base directory."
        
        return "No tar bytes provided."
    
    async def get_id(self):
        return self.id
    
    def __sanitize_filename(self, filename):
        # remove potentially dangerous characters from the filename
        dangerous_chars = ['{', '}', '\\', ',']
        
        for char in dangerous_chars:
            filename = filename.replace(char, '')
        
        # disallow directory traversal, that would be really bad :(
        while '../' in filename:
            filename = filename.replace('../', '')
            
        norm = os.path.normpath(filename)
            
        if norm[0] == '/':
            return 'denied'
            
        else:
            return norm
    
    async def __check_file_for_flag(self, file_path):
        if not await self._run_in_executor(os.path.exists, file_path):
            return False, ''
        
        async with aiofiles.open(file_path, 'r') as f:
            file_contents = await f.read()
            if 'sctf' in file_contents:
                return True, 'Flag found in file, not allowed to read it.'
            return False, ''
        
    
    async def write_file(self, filename, content):
        filename = self.__sanitize_filename(filename)
        file_path = os.path.join(self.path, filename)
        if os.path.exists(file_path):
            await self._run_in_executor(os.remove, file_path)
        dir_path = os.path.dirname(file_path)
        if dir_path != self.path:  
            await self._run_in_executor(os.makedirs, dir_path, True)
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)
            
        return file_path, content
    
    async def mkdir(self, folder):
        folder = self.__sanitize_filename(folder)
        folder_path = os.path.join(self.path, folder)
        await self._run_in_executor(os.makedirs, folder_path, True)
        return folder_path
    
    async def cp(self, src, dest):
        src = self.__sanitize_filename(src)
        dest = self.__sanitize_filename(dest)
        src_path = os.path.join(self.path, src)
        dest_path = os.path.join(self.path, dest)
        
        if not await self._run_in_executor(os.path.exists, src_path):
            raise FileNotFoundError(f"Source file {src_path} does not exist.")
        
        
        async with aiofiles.open(src_path, 'rb') as fsrc:
            async with aiofiles.open(dest_path, 'wb') as fdest:
                content = await fsrc.read()
                await fdest.write(content)
                
        return dest_path, src_path
    
    async def rm(self, filename):
        filename = self.__sanitize_filename(filename)
        file_path = os.path.join(self.path, filename)
        
        if not await self._run_in_executor(os.path.exists, file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        await self._run_in_executor(os.remove, file_path)
        return file_path
    
    async def mktempdir(self, path=None):
        if path is None:
            base_path = self.path
        else:
            path = self.__sanitize_filename(path)
            base_path = os.path.join(self.path, path)
        
        temp_dir = os.path.join(base_path, str(uuid.uuid4()))
        await self._run_in_executor(os.makedirs, temp_dir, True)
        return temp_dir 
    
    async def stat(self, filename):
        filename = self.__sanitize_filename(filename)
        file_path = os.path.join(self.path, filename)
        
        if not await self._run_in_executor(os.path.exists, file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        stat_result = await self._run_in_executor(os.stat, file_path)
        return stat_result
    
    async def read_file(self, filename):
        filename = self.__sanitize_filename(filename)
        file_path = os.path.join(self.path, filename)
        
        if not await self._run_in_executor(os.path.exists, file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        
        # extra layer of security to prevent funny business!
        banned_files = ['flag', 'root', 'etc', 'passwd', 'proc', 'dev', 'var', 'tmp', 'usr', 'bin']
        
        # make sure we resolve symlinks here for naughty tricks!
        if any(banned in str(Path(filename).resolve()) for banned in banned_files):
            return 'Funny Business Detected! You are not allowed to read this file.'
        
    
        res, message = await self.__check_file_for_flag(file_path)
        if res:
            return message
        
        async with aiofiles.open(file_path, 'r') as f:
            return await f.read()
    
    async def list_files(self):
        files = []
        res = await aiofiles.os.scandir(self.path)
        for entry in res:
            if entry.is_file():
                files.append(entry.name)
        return files
    
    async def close(self):
        """Clean up the thread pool executor"""
        self.executor.shutdown(wait=True)
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

