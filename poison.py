import pickle
import os

# This class defines the "Poison"
class Poison:
    def __reduce__(self):
        # This tells the computer to run a command when the file is opened
        return (os.system, ('echo YOUR PIPELINE JUST CAUGHT A MALICIOUS MODEL!',))

# Create the poisoned object
malicious_model = Poison()

# Save it correctly
file_name = 'poisoned_model.pkl'
with open(file_name, 'wb') as f:
    pickle.dump(malicious_model, f)

print(f"Poisoned model created successfully: {file_name}")
