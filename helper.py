import subprocess
import asyncio

class Helper:
    def __init__(self, script_path, test_file, log_widget):
        self.script_path = script_path
        self.test_file = test_file
        self.log_widget = log_widget

    async def inject_code_async(self, new_code):
        """Inject new code asynchronously into the editable section."""
        async with asyncio.Lock():
            await self.log_to_gui("Injecting new code...")
            with open(self.script_path, 'r') as file:
                content = file.readlines()

            start_idx, end_idx = None, None
            for i, line in enumerate(content):
                if "# === Start Editable Section ===" in line:
                    start_idx = i
                elif "# === End Editable Section ===" in line:
                    end_idx = i
            
            if start_idx and end_idx:
                await self.create_test_script_async(content, new_code, start_idx, end_idx)
                result = await self.run_test_async()
                if result:
                    await self.apply_changes_async()

    async def create_test_script_async(self, content, new_code, start_idx, end_idx):
        """Create a test script asynchronously."""
        async with asyncio.Lock():
            await self.log_to_gui("Creating test script...")
            with open(self.test_file, 'w') as test_script:
                test_script.writelines(content[:start_idx + 1])
                test_script.write("\n# ======= Injected Test Code Start =======\n")
                test_script.write(new_code)
                test_script.write("\n# ======= Injected Test Code End =======\n")
                test_script.writelines(content[end_idx:])

    async def run_test_async(self):
        """Run the unit test asynchronously."""
        await self.log_to_gui("Running unit test...")
        process = await asyncio.create_subprocess_exec(
            'python', self.test_file,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            await self.log_to_gui("Test Passed.")
            return True
        else:
            await self.log_to_gui(f"Test Failed. Output:\n{stdout.decode()}\n{stderr.decode()}")
            return False

    async def apply_changes_async(self):
        """Apply changes to the main script asynchronously."""
        async with asyncio.Lock():
            await self.log_to_gui("Applying changes...")
            with open(self.script_path, 'w') as main_script:
                with open(self.test_file, 'r') as test_script:
                    main_script.write(test_script.read())
            await self.log_to_gui("Changes applied successfully.")

    def suggest_new_code(self):
        """Suggest new code to inject."""
        new_code = """async def injected_function():
    print("Injected code is running.")
    await asyncio.sleep(1)
await injected_function()"""
        return new_code

    async def log_to_gui(self, message):
        """Log message in the GUI window."""
        self.log_widget.insert(tk.END, message + '\n')
        self.log_widget.see(tk.END)
        await asyncio.sleep(0)  # Yield control back to event loop
