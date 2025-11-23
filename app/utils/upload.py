import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from typing import Optional
from PIL import Image
import io
from app.core.config import get_settings

settings = get_settings()

# Tipos de imagem permitidos
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_DIMENSIONS = (2000, 2000)  # Máximo de 2000x2000 pixels


def validate_image(file: UploadFile) -> None:
    """Valida se o arquivo é uma imagem válida"""
    # Verificar tipo MIME
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não permitido. Tipos permitidos: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # Verificar tamanho do arquivo
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_IMAGE_SIZE / (1024 * 1024):.1f}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Arquivo vazio"
        )


def process_image(file: UploadFile, max_dimensions: tuple = MAX_IMAGE_DIMENSIONS) -> bytes:
    """Processa e redimensiona a imagem se necessário"""
    try:
        # Ler a imagem
        image_data = file.file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Converter para RGB se necessário (para JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Criar fundo branco para imagens com transparência
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar se necessário
        if image.size[0] > max_dimensions[0] or image.size[1] > max_dimensions[1]:
            image.thumbnail(max_dimensions, Image.Resampling.LANCZOS)
        
        # Salvar em bytes
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar imagem: {str(e)}"
        )


def save_upload_file(file: UploadFile, subdirectory: str = "colaboradores") -> str:
    """
    Salva um arquivo de upload e retorna o caminho relativo
    
    Args:
        file: Arquivo a ser salvo
        subdirectory: Subdiretório onde salvar (ex: "colaboradores", "documentos")
    
    Returns:
        Caminho relativo do arquivo salvo (ex: "colaboradores/abc123.jpg")
    """
    # Validar arquivo
    validate_image(file)
    
    # Processar imagem (redimensionar se necessário)
    processed_image = process_image(file)
    
    # Criar diretório se não existir
    upload_dir = Path(settings.UPLOAD_DIR) / subdirectory
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Gerar nome único para o arquivo
    file_extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    if file_extension not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        file_extension = ".jpg"
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Salvar arquivo
    with open(file_path, "wb") as f:
        f.write(processed_image)
    
    # Retornar caminho relativo
    return f"{subdirectory}/{unique_filename}"


def delete_upload_file(file_path: str) -> bool:
    """
    Deleta um arquivo de upload
    
    Args:
        file_path: Caminho relativo do arquivo (ex: "colaboradores/abc123.jpg")
    
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    try:
        full_path = Path(settings.UPLOAD_DIR) / file_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception:
        return False


def get_file_url(file_path: Optional[str]) -> Optional[str]:
    """
    Retorna a URL completa do arquivo
    
    Args:
        file_path: Caminho relativo do arquivo
    
    Returns:
        URL completa ou None se não houver arquivo
    """
    if not file_path:
        return None
    
    # Em produção, isso pode ser uma URL de CDN ou S3
    # Por enquanto, retornamos o caminho relativo que será servido pelo FastAPI
    return f"/uploads/{file_path}"



