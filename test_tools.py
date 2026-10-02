from app.tools import calculator, get_time

print("[Tool Test] Testing calculator...")
result = calculator("1234 * 5678")
print(f"Calculator result: {result}")

print("\n[Tool Test] Testing clock...")
current_time = get_time()
print(f"Current time: {current_time}")

print("\n===== TOOL TEST PASSED =====")