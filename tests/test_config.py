"""Test configuration loading"""
from app.config import settings

print("Testing Configuration...")
print("=" * 50)

# Test all settings
print(f"✓ App Name: {settings.app_name}")
print(f"✓ Version: {settings.app_version}")
print(f"✓ Environment: {settings.environment}")
print(f"✓ Log Level: {settings.log_level}")
print(f"✓ Model: {settings.model_name}")
print(f"✓ Temperature: {settings.model_temperature}")
print(f"✓ Max Tokens: {settings.max_tokens}")
print(f"✓ Cache Enabled: {settings.enable_cache}")
print(f"✓ Allowed Origins: {settings.allowed_origins}")

# Test API key (masked)
api_key = settings.openai_api_key
print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]}")

# Test computed properties
print(f"✓ Is Development: {settings.is_development}")
print(f"✓ Is Production: {settings.is_production}")

print("=" * 50)
print("✅ Configuration test passed!")