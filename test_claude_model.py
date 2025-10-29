# """
#Test script to find which Claude model is available with your API key
#"""

import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_claude_models():
    """Test different Claude models to find which one works"""
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ No ANTHROPIC_API_KEY found in .env file")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # First, try to get the list of available models
    print("Fetching available models from API...\n")
    available_models = []
    
    try:
        models_response = client.models.list(limit=20)
        available_models = [model.id for model in models_response.data]
        
        print("📋 Available models from API:")
        for model in available_models:
            print(f"  - {model}")
        print()
        
    except Exception as e:
        print(f"⚠️  Could not fetch model list: {e}")
        print("Will test common models instead.\n")
    
    # If we got models from API, test those first
    # Otherwise use our default list
    if available_models:
        models_to_test = available_models
    else:
        models_to_test = [
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-sonnet-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-haiku-20241022",
    "claude-3-haiku-20240307"
        ]
    
    print("="*60)
    print("TESTING CLAUDE MODELS")
    print("="*60 + "\n")
    
    working_models = []
    
    for model in models_to_test:
        print(f"Testing {model}... ", end="")
        try:
            # Try a simple message
            message = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Reply with just: yes"}]
            )
            print(f"✅ WORKS!")
            working_models.append(model)
                
        except anthropic.NotFoundError:
            print(f"❌ Not found")
        except anthropic.RateLimitError:
            print(f"⚠️  Rate limited (but model exists!)")
            working_models.append(model)
        except anthropic.PermissionDeniedError:
            print(f"❌ Permission denied")
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                print(f"❌ Model not available")
            else:
                print(f"❌ Error: {error_msg[:50]}")
    
    # Summary
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60 + "\n")
    
    if working_models:
        print("✅ WORKING MODELS:")
        for model in working_models:
            print(f"  - {model}")
        
        print(f"\n🎯 RECOMMENDED MODEL: {working_models[0]}")
        print(f"\nUpdate config.py with:")
        print(f'CLAUDE_MODEL = "{working_models[0]}"')
        
        if len(working_models) > 1:
            print(f"\nAlternatives available:")
            for model in working_models[1:]:
                print(f'  - "{model}"')
    else:
        print("❌ No working models found!")
        print("\nPossible issues:")
        print("1. Check your API key is valid")
        print("2. Check you have access to Claude models")
        print("3. Check your account has available credits")
        print("\nTry running: export ANTHROPIC_API_KEY='your-key-here'")

if __name__ == "__main__":
    test_claude_models()
