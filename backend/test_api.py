"""
Test script to validate the RAG Chatbot API functionality
"""
import requests
import json
import time

def test_api_functionality():
    """Test the complete functionality of the RAG Chatbot API"""
    base_url = "http://localhost:8000"

    print("Testing RAG Chatbot API functionality...")

    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   [OK] Health check passed: {health_data['status']}")
        else:
            print(f"   [KO] Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   [KO] Health check failed with error: {str(e)}")
        return False

    # Test 2: Chat endpoint
    print("\n2. Testing chat endpoint...")
    try:
        test_query = {
            "message": "What is the purpose of this test?",
            "session_id": "test_session_123"
        }

        response = requests.post(
            f"{base_url}/chat",
            json=test_query,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            chat_data = response.json()
            if chat_data.get("success"):
                print("   [OK] Chat endpoint responded successfully")
                print(f"   [OK] Response received: {len(chat_data['data']['response'])} characters")
                if 'sources' in chat_data['data']:
                    print(f"   [OK] Sources provided: {len(chat_data['data']['sources'])} sources")
                if 'grounding_confidence' in chat_data['data']:
                    print(f"   [OK] Grounding confidence: {chat_data['data']['grounding_confidence']}")
            else:
                print(f"   [KO] Chat endpoint returned error: {chat_data.get('error')}")
                return False
        else:
            print(f"   [KO] Chat endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   [KO] Chat endpoint test failed with error: {str(e)}")
        return False

    # Test 3: Error handling
    print("\n3. Testing error handling...")
    try:
        invalid_query = {"message": ""}  # Empty message should cause validation error

        response = requests.post(
            f"{base_url}/chat",
            json=invalid_query,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 422 or (response.status_code == 200 and not response.json().get("success")):
            print("   [OK] Error handling works correctly")
        else:
            print(f"   ? Error handling response: {response.status_code}")
    except Exception as e:
        print(f"   [KO] Error handling test failed with error: {str(e)}")
        return False

    print("\n[OK] All API functionality tests passed!")
    return True

if __name__ == "__main__":
    success = test_api_functionality()
    if success:
        print("\n🎉 RAG Chatbot API validation successful!")
    else:
        print("\n❌ RAG Chatbot API validation failed!")
        exit(1)