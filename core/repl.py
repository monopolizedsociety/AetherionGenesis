# core/repl.py

def start_repl(kernel=None):
    print("🔁 Entering Aetherion REPL. Type 'exit' to quit.")
    while True:
        try:
            cmd = input("🧠 > ")
            if cmd.lower() in ("exit", "quit"):
                print("👋 Exiting REPL.")
                break
            try:
                result = eval(cmd, {"kernel": kernel})
                print(f"✅ {result}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Exiting REPL.")
            break
