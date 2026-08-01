import os
import sys
import subprocess
import time

def main():
    print("=" * 60)
    print("🛡️  Starting DarkTrust Zero-Trust Security Platform...")
    print("=" * 60)
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    # Ensure frontend dependencies are installed
    node_modules_dir = os.path.join(frontend_dir, "node_modules")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"

    if not os.path.exists(node_modules_dir):
        print("\n📦 Installing frontend dependencies (npm install)...")
        subprocess.run([npm_cmd, "install"], cwd=frontend_dir, check=True)
        print("   ✅ Frontend dependencies installed successfully.")

    # Configure PYTHONPATH to include backend dir
    env = os.environ.copy()
    env["PYTHONPATH"] = backend_dir + os.pathsep + env.get("PYTHONPATH", "")

    print("\n1. Launching FastAPI Backend on http://localhost:8000 ...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    backend_process = subprocess.Popen(backend_cmd, cwd=backend_dir, env=env)

    time.sleep(2)
    print("   ✅ Backend started. Docs available at http://localhost:8000/docs")

    print("\n2. Launching React + Vite Frontend on http://localhost:3000 ...")
    frontend_cmd = [npm_cmd, "run", "dev"]
    frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir)

    print("\n" + "=" * 60)
    print("🚀 DarkTrust is running!")
    print("   - Dashboard: http://localhost:3000")
    print("   - API Docs:  http://localhost:8000/docs")
    print("Press Ctrl+C to stop servers.")
    print("=" * 60)

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping DarkTrust servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
