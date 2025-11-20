"""Test API routes in isolation"""
import asyncio
from app.api.routes import health_check, get_cache_stats
from app.config import settings

async def test_routes():
    print("Testing API Routes...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    response = await health_check()
    print(f"   Status: {response.status}")
    print(f"   Version: {response.version}")
    print(f"   Environment: {response.environment}")
    assert response.status == "healthy"
    assert response.version == settings.app_version
    print("   ✓ Health check working")
    
    # Test 2: Cache stats
    print("\n2. Testing cache stats...")
    stats = await get_cache_stats()
    print(f"   Cache stats: {stats}")
    assert "cache_size" in stats
    assert "cache_enabled" in stats
    print("   ✓ Cache stats endpoint working")
    
    print("\n" + "=" * 50)
    print("✅ All route tests passed!")

if __name__ == "__main__":
    asyncio.run(test_routes())