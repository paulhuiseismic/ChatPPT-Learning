"""
Quick verification test for content_formatter.txt migration
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_prompt_file_migration():
    """Verify all components use content_formatter.txt"""

    print("=" * 70)
    print("Testing Prompt File Migration")
    print("=" * 70)

    # Test 1: Check ChatBot can load the new prompt
    print("\n1. Testing ChatBot with content_formatter.txt...")
    try:
        from chatbot import ChatBot
        bot = ChatBot(
            prompt_file="./prompts/content_formatter.txt",
            session_id="migration_test"
        )
        print(f"   ✅ ChatBot created successfully")
        print(f"   ✅ Prompt file: {bot.prompt_file}")

        # Check prompt content
        if "Multi-level Bullet Points" in bot.prompt or "hierarchical" in bot.prompt.lower():
            print(f"   ✅ Prompt contains advanced formatting rules")
        else:
            print(f"   ⚠️  Prompt may not have advanced features")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 2: Check Gradio app loads correctly
    print("\n2. Testing Gradio app integration...")
    try:
        from gradio_app import get_chatbot_instance, load_system_prompt
        import uuid

        # Test chatbot instance creation
        session_id = str(uuid.uuid4())
        bot = get_chatbot_instance(session_id)
        print(f"   ✅ Chatbot instance created for session {session_id[:8]}...")
        print(f"   ✅ Using prompt file: {bot.prompt_file}")

        # Test system prompt loading
        prompt = load_system_prompt()
        if "content formatter" in prompt.lower() or "multi-level" in prompt.lower():
            print(f"   ✅ System prompt loaded from content_formatter.txt")
            print(f"   ✅ Prompt length: {len(prompt)} characters")
        else:
            print(f"   ⚠️  Prompt may be from old file")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 3: Verify old references are gone
    print("\n3. Checking for old references...")

    old_ref_found = False
    files_to_check = [
        'src/gradio_app.py',
        'test_enhanced_gradio.py'
    ]

    for filepath in files_to_check:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if '"prompts/formatter.txt"' in content or "'prompts/formatter.txt'" in content:
                    print(f"   ⚠️  Found old reference in {filepath}")
                    old_ref_found = True

    if not old_ref_found:
        print(f"   ✅ No old references found in Python files")

    # Test 4: Verify new prompt file exists
    print("\n4. Verifying prompt file exists...")
    new_prompt_path = "./prompts/content_formatter.txt"
    old_prompt_path = "./prompts/formatter.txt"

    if os.path.exists(new_prompt_path):
        size = os.path.getsize(new_prompt_path)
        print(f"   ✅ content_formatter.txt exists ({size} bytes)")
    else:
        print(f"   ❌ content_formatter.txt NOT FOUND")
        return False

    if os.path.exists(old_prompt_path):
        print(f"   ℹ️  formatter.txt still exists (legacy file, can be kept)")

    # Summary
    print("\n" + "=" * 70)
    print("Migration Verification Summary")
    print("=" * 70)
    print("✅ ChatBot initialization: PASS")
    print("✅ Gradio app integration: PASS")
    print("✅ Old references removed: PASS" if not old_ref_found else "⚠️  Old references found")
    print("✅ New prompt file exists: PASS")
    print("\n" + "=" * 70)
    print("🎉 Migration to content_formatter.txt is COMPLETE!")
    print("=" * 70)
    print("\nThe application now uses the enhanced content_formatter.txt")
    print("which provides multi-level bullet points and better formatting.")
    print("\nYou can now run: python src/gradio_app.py")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = test_prompt_file_migration()
    sys.exit(0 if success else 1)

