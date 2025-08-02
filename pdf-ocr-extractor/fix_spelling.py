#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
import aiohttp
import time
from pathlib import Path
from typing import List
from datetime import datetime

# Configuration management
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("PyYAML not found. Install with: pip install pyyaml")

def safe_print(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

class ConfigManager:
    """Quản lý cấu hình từ file YAML"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """Tải cấu hình từ file YAML"""
        if not YAML_AVAILABLE:
            safe_print("❌ PyYAML not available. Using default configuration.")
            self.config = self.get_default_config()
            return
            
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                safe_print(f"✅ Configuration loaded from {self.config_file}")
            except Exception as e:
                safe_print(f"❌ Error loading config: {e}")
                self.config = self.get_default_config()
        else:
            safe_print(f"⚠️  Config file {self.config_file} not found. Creating default...")
            self.config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Lưu cấu hình ra file YAML"""
        if not YAML_AVAILABLE:
            return
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            safe_print(f"💾 Configuration saved to {self.config_file}")
        except Exception as e:
            safe_print(f"❌ Error saving config: {e}")
    
    def get_default_config(self):
        """Trả về cấu hình mặc định"""
        return {
            'ollama': {
                'host': 'localhost',
                'port': 11434,
                'timeout': 300
            },
            'model': {
                'name': 'qwen2.5',
                'temperature': 0.1,
                'top_p': 0.9
            },
            'paths': {
                'input_dir': 'raw_json_output',
                'output_dir': 'spelling_fixed_json'
            },
            'processing': {
                'max_chunk_size': 2000,
                'max_retries': 3
            }
        }
    
    def get(self, key_path: str, default=None):
        """Lấy giá trị cấu hình theo đường dẫn key"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value

class OllamaSpellChecker:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
        # Load configuration
        self.model_name = self.config.get('model.name', 'qwen2.5')
        self.host = self.config.get('ollama.host', 'localhost')
        self.port = self.config.get('ollama.port', 11434)
        self.timeout = self.config.get('ollama.timeout', 300)
        self.temperature = self.config.get('model.temperature', 0.1)
        self.top_p = self.config.get('model.top_p', 0.9)
        
        # URLs
        self.base_url = f"http://{self.host}:{self.port}"
        self.api_url = f"{self.base_url}/api/generate"
        
        # Settings
        self.max_chunk_size = self.config.get('processing.max_chunk_size', 2000)
        self.max_retries = self.config.get('processing.max_retries', 3)
        
        self.check_connection()
        
    def check_connection(self):
        """Kiểm tra kết nối với Ollama server"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'].split(':')[0] for model in models]
                
                safe_print(f"✅ Connected to Ollama server at {self.base_url}")
                safe_print(f"📋 Available models: {available_models}")
                
                if self.model_name not in available_models:
                    if available_models:
                        self.model_name = available_models[0]
                        safe_print(f"⚠️  Using available model: {self.model_name}")
                    else:
                        safe_print(f"❌ No models available. Please pull a model first.")
                        return
                else:
                    safe_print(f"✅ Model '{self.model_name}' is available")
                    
            else:
                safe_print(f"❌ Failed to connect to Ollama server: HTTP {response.status_code}")
        except Exception as e:
            safe_print(f"❌ Cannot connect to Ollama server: {e}")

    def create_prompt(self, text: str) -> str:
        """Tạo prompt cho việc sửa lỗi chính tả"""
        return f"""Bạn là chuyên gia sửa lỗi chính tả tiếng Việt.

NHIỆM VỤ: Sửa TẤT CẢ các lỗi trong văn bản sau:
- Lỗi chính tả, dấu thanh điệu
- Lỗi viết hoa, viết thường  
- Lỗi khoảng trắng, dấu câu
- Lỗi từ viết tắt và tên riêng

QUY TẮC:
1. CHỈ trả lời văn bản đã được sửa
2. KHÔNG thêm giải thích
3. GIỮ NGUYÊN cấu trúc và định dạng

VĂN BẢN CẦN SỬA:
{text}

VĂN BẢN ĐÃ SỬA:"""

    async def fix_text(self, text: str, session: aiohttp.ClientSession, retries: int = 0) -> str:
        """Sử dụng Ollama để sửa lỗi chính tả"""
        try:
            prompt = self.create_prompt(text)
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "top_p": self.top_p
                }
            }
            
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with session.post(self.api_url, json=payload, timeout=timeout) as response:
                if response.status == 200:
                    result = await response.json()
                    corrected_text = result.get('response', '').strip()
                    return corrected_text if corrected_text else text
                else:
                    if retries < self.max_retries:
                        await asyncio.sleep(2)
                        return await self.fix_text(text, session, retries + 1)
                    return text
                    
        except Exception as e:
            if retries < self.max_retries:
                await asyncio.sleep(2)
                return await self.fix_text(text, session, retries + 1)
            safe_print(f"❌ Error processing text: {e}")
            return text

    def split_text(self, text: str) -> List[str]:
        """Chia văn bản thành các chunk nhỏ hơn"""
        if len(text) <= self.max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        sentences = text.split('. ')
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= self.max_chunk_size:
                if current_chunk:
                    current_chunk += '. ' + sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks

    async def process_text(self, text: str, session: aiohttp.ClientSession) -> str:
        """Xử lý văn bản, chia nhỏ nếu cần"""
        if not text or len(text) < 50:
            return text
        
        if len(text) > self.max_chunk_size:
            chunks = self.split_text(text)
            corrected_chunks = []
            
            for chunk in chunks:
                corrected_chunk = await self.fix_text(chunk, session)
                corrected_chunks.append(corrected_chunk)
                await asyncio.sleep(0.5)
            
            return '. '.join(corrected_chunks)
        else:
            return await self.fix_text(text, session)

class SpellCheckProcessor:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.ollama_checker = OllamaSpellChecker(config_manager)
        
        # Paths
        self.input_dir = Path(self.config.get('paths.input_dir', 'raw_json_output'))
        self.output_dir = Path(self.config.get('paths.output_dir', 'spelling_fixed_json'))
        
        # Stats
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'changes_made': 0
        }

    def get_json_files(self) -> List[Path]:
        """Lấy danh sách file JSON"""
        return list(self.input_dir.rglob("*.json"))

    async def process_json_file(self, input_file: Path, output_file: Path, session: aiohttp.ClientSession) -> bool:
        """Xử lý một file JSON"""
        try:
            # Đọc file JSON
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Sửa lỗi chính tả trong nội dung text
            if isinstance(data, dict) and 'text' in data:
                original_text = data['text']
                if original_text and isinstance(original_text, str):
                    safe_print(f"🔄 Processing: {input_file.name}")
                    
                    corrected_text = await self.ollama_checker.process_text(original_text, session)
                    
                    if corrected_text != original_text:
                        data['text'] = corrected_text
                        self.stats['changes_made'] += 1
                        safe_print(f"✅ Corrected: {input_file.name}")
                    else:
                        safe_print(f"➖ No changes: {input_file.name}")

            # Lưu file
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.stats['processed_files'] += 1
            return True

        except Exception as e:
            safe_print(f"❌ Error processing {input_file}: {e}")
            self.stats['failed_files'] += 1
            return False

    async def process_directory(self):
        """Xử lý toàn bộ thư mục"""
        json_files = self.get_json_files()
        self.stats['total_files'] = len(json_files)
        
        safe_print(f"🚀 Starting spell check for {self.stats['total_files']} files")
        safe_print(f"🤖 Using model: {self.ollama_checker.model_name}")
        safe_print(f"📁 Input: {self.input_dir}")
        safe_print(f"📁 Output: {self.output_dir}")
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            for json_file in json_files:
                relative_path = json_file.relative_to(self.input_dir)
                output_file = self.output_dir / relative_path
                await self.process_json_file(json_file, output_file, session)

        total_duration = time.time() - start_time
        
        # Báo cáo kết quả
        safe_print(f"\n{'='*50}")
        safe_print(f"🎉 PROCESSING COMPLETE")
        safe_print(f"{'='*50}")
        safe_print(f"📊 Total files: {self.stats['total_files']}")
        safe_print(f"✅ Processed: {self.stats['processed_files']}")
        safe_print(f"🔄 Changes made: {self.stats['changes_made']}")
        safe_print(f"❌ Failed: {self.stats['failed_files']}")
        safe_print(f"⏱️  Time: {total_duration:.2f} seconds")

async def main():
    safe_print("🤖 Ollama Vietnamese Spell Checker - Simple Version")
    safe_print("=" * 50)
    
    # Load config
    config_manager = ConfigManager()
    
    # Create processor
    processor = SpellCheckProcessor(config_manager)
    
    # Process directory
    await processor.process_directory()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        safe_print("\n⏹️  Process interrupted by user")
    except Exception as e:
        safe_print(f"\n❌ Fatal error: {e}")