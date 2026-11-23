import os
import zipfile

ZIP_NAME = "23120228_HW06_AI_API_100.zip"

INCLUDE_DIRS = ["report", "postman", ".agents", "ci-cd"]
INCLUDE_FILES = [
    "README.md",
    "run_tests.ps1",
    "run_tests.bat",
    "api_specification.md",
    "2026.HW06.API Testing_En.md"
]

def create_submission_zip():
    print(f"Creating submission zip: {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for f in INCLUDE_FILES:
            if os.path.exists(f):
                zf.write(f, arcname=f)
                print(f"Added file: {f}")
                
        # Add directories
        for d in INCLUDE_DIRS:
            if os.path.exists(d):
                for root, dirs, files in os.walk(d):
                    for file in files:
                        if file.endswith(".tmp") or file.endswith(".lock"):
                            continue
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, ".")
                        zf.write(full_path, arcname=rel_path)
                print(f"Added directory: {d}/")
                
    zip_size = os.path.getsize(ZIP_NAME)
    print(f"\nSUCCESS! {ZIP_NAME} created successfully ({zip_size:,} bytes / {zip_size / (1024*1024):.2f} MB)")
    
    # Verify contents
    with zipfile.ZipFile(ZIP_NAME, "r") as zf:
        namelist = zf.namelist()
        print(f"Total files in zip archive: {len(namelist)}")
        print("\nKey Deliverables in Archive:")
        for item in namelist:
            if any(k in item for k in ["main_report", "ai_audit", "newman_report", "m4_eshop", "bug_report", "git_commit_log", "test_cases_all", "api-tests", "SKILL"]):
                print(f"  ✓ {item}")

if __name__ == "__main__":
    create_submission_zip()
