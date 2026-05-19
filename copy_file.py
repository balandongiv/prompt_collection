import shutil
from pathlib import Path

file_paths = [
		# r"C:\Users\balan\IdeaProjects\pyblinker\pyblinker\blink_features\energy\energy_features.py",
		# r"C:\Users\balan\IdeaProjects\pyblinker\pyblinker\blink_features\frequency_domain\aggregate.py",
		r"C:\Users\balan\IdeaProjects\pyblinker\pyblinker\blink_features\morphology\epoch_features.py",
		r"C:\Users\balan\IdeaProjects\pyblinker\pyblinker\blink_features\kinematics\kinematic_features.py",
		# r"C:\Users\balan\IdeaProjects\pyblinker\pyblinker\blink_features\_style_windows.py"
		]

# Your Desktop path (OneDrive)
desktop_path = Path(r"C:\Users\balan\OneDrive\Desktop")

# Folder to create on Desktop (change name if you want)
dest_dir = desktop_path / "pyblinker_copied_files"

# Create folder if it doesn't exist
dest_dir.mkdir(parents=True, exist_ok=True)

for src in file_paths:
	src_path = Path(src)
	if not src_path.exists():
		print(f"Missing: {src_path}")
		continue

	# Copy into the Desktop folder (keeps same filename)
	dest_path = dest_dir / src_path.name
	shutil.copy2(src_path, dest_path)  # preserves timestamps/metadata
	print(f"Copied: {src_path} -> {dest_path}")

print(f"\nDone. Files are in: {dest_dir}")