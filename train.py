import pickle  # nosec B403

# This creates a harmless, fake AI model file
fake_ai_brain = {"algorithm": "super_smart_ai", "version": 1.0}

# We save it as a .pkl file, which is standard for AI models
with open('dummy_model.pkl', 'wb') as file:
    pickle.dump(fake_ai_brain, file)

print("AI Model created successfully!")
