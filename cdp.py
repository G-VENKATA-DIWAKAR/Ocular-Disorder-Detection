from google.colab import drive
drive.mount('/content/drive')

!pip install tensorflow opencv-python numpy pillow

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define Image Size & Batch Size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Define Data Generator (for Data Augmentation)
datagen = ImageDataGenerator(
    rescale=1./255,    # Normalize images
    validation_split=0.2  # 20% data for validation
)

# Load Training Data
train_generator = datagen.flow_from_directory(
    "/content/drive/MyDrive/Eye_Disease_Dataset",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

# Load Validation Data
val_generator = datagen.flow_from_directory(
    "/content/drive/MyDrive/Eye_Disease_Dataset",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# Print class labels
print("Class Labels:", train_generator.class_indices)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')  # 5 classes (Cataract, Conjunctivitis, Eyelid, Normal, Uveitis)
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print Model Summary
model.summary()

history = model.fit(train_generator, validation_data=val_generator, epochs=20)

model.save("/content/drive/MyDrive/conjunctivitis_model.h5")
print("✅ Model saved successfully!")

from google.colab import files

uploaded = files.upload()  # Upload image manually


from tensorflow.keras.preprocessing import image
import numpy as np

# Get uploaded image filename
img_path = list(uploaded.keys())[0]

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

# Load trained model
from tensorflow.keras.models import load_model
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Make prediction
prediction = model.predict(img_array)

# Define class labels
class_labels = ['Cataract', 'Conjunctivitis', 'Eyelid', 'Normal', 'Uveitis']
predicted_class = class_labels[np.argmax(prediction)]

# Show Prediction
import matplotlib.pyplot as plt
plt.imshow(img)
plt.title(f"Predicted Class: {predicted_class}")
plt.axis("off")
plt.show()

print(f"✅ Predicted Class: {predicted_class}")

from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Upload image manually
uploaded = files.upload()

# Get uploaded image filename
img_path = list(uploaded.keys())[0]

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

# Load trained model
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Make prediction
prediction = model.predict(img_array)

# Define class labels with details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': ["Blurred vision", "Sensitivity to light", "Difficulty seeing at night", "Faded colors"],
        'treatment': "Treatment includes prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Conjunctivitis (Pink Eye) is an inflammation of the conjunctiva, often due to infection or allergies.",
        'symptoms': ["Redness", "Itchiness", "Watery eyes", "Discharge that may cause eyelids to stick together"],
        'treatment': "Treatment depends on the cause: antibiotics for bacterial infections, antihistamines for allergies, and warm compresses for comfort."
    },
    'Eyelid': {
        'description': "Eyelid disorders include conditions like blepharitis, styes, or ptosis, which affect eyelid function and appearance.",
        'symptoms': ["Swelling", "Irritation", "Dryness", "Painful lump on the eyelid"],
        'treatment': "Treatment varies but may include warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': ["No abnormal symptoms detected"],
        'treatment': "No treatment needed. Maintain good eye hygiene and visit an eye doctor for regular check-ups."
    },
    'Uveitis': {
        'description': "Uveitis is an inflammation of the uvea (middle layer of the eye), which can cause pain and vision issues.",
        'symptoms': ["Eye redness", "Blurred vision", "Eye pain", "Light sensitivity"],
        'treatment': "Treatment includes corticosteroid eye drops, oral steroids, or immunosuppressive drugs depending on severity."
    }
}

# Get predicted class and details
predicted_class = np.argmax(prediction)
predicted_label = list(disease_info.keys())[predicted_class]
details = disease_info[predicted_label]

# Show Prediction with Disease Info
plt.imshow(img)
plt.title(f"Predicted Class: {predicted_label}")
plt.axis("off")
plt.show()

# Display result
print(f"✅ Predicted Class: {predicted_label}")
print(f"ℹ️ About {predicted_label}: {details['description']}")
print(f"🩺 Symptoms: {', '.join(details['symptoms'])}")
print(f"💊 Suggested Treatment: {details['treatment']}")

import pandas as pd
import os
from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Upload image manually
uploaded = files.upload()

# Get uploaded image filename
img_path = list(uploaded.keys())[0]

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

# Load trained model
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Make prediction
prediction = model.predict(img_array)

# Define class labels with details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': ["Blurred vision", "Sensitivity to light", "Difficulty seeing at night", "Faded colors"],
        'treatment': "Treatment includes prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Conjunctivitis (Pink Eye) is an inflammation of the conjunctiva, often due to infection or allergies.",
        'symptoms': ["Redness", "Itchiness", "Watery eyes", "Discharge that may cause eyelids to stick together"],
        'treatment': "Treatment depends on the cause: antibiotics for bacterial infections, antihistamines for allergies, and warm compresses for comfort."
    },
    'Eyelid': {
        'description': "Eyelid disorders include conditions like blepharitis, styes, or ptosis, which affect eyelid function and appearance.",
        'symptoms': ["Swelling", "Irritation", "Dryness", "Painful lump on the eyelid"],
        'treatment': "Treatment varies but may include warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': ["No abnormal symptoms detected"],
        'treatment': "No treatment needed. Maintain good eye hygiene and visit an eye doctor for regular check-ups."
    },
    'Uveitis': {
        'description': "Uveitis is an inflammation of the uvea (middle layer of the eye), which can cause pain and vision issues.",
        'symptoms': ["Eye redness", "Blurred vision", "Eye pain", "Light sensitivity"],
        'treatment': "Treatment includes corticosteroid eye drops, oral steroids, or immunosuppressive drugs depending on severity."
    }
}

# Get predicted class and details
predicted_class = np.argmax(prediction)
predicted_label = list(disease_info.keys())[predicted_class]
details = disease_info[predicted_label]

# Show Prediction with Disease Info
plt.imshow(img)
plt.title(f"Predicted Class: {predicted_label}")
plt.axis("off")
plt.show()

# Display result
print(f"✅ Predicted Class: {predicted_label}")
print(f"ℹ️ About {predicted_label}: {details['description']}")
print(f"🩺 Symptoms: {', '.join(details['symptoms'])}")
print(f"💊 Suggested Treatment: {details['treatment']}")

# Create DataFrame for CSV Logging
csv_filename = "predictions.csv"
data = {
    "Image": [img_path],
    "Predicted Class": [predicted_label],
    "Description": [details['description']],
    "Symptoms": [', '.join(details['symptoms'])],
    "Treatment": [details['treatment']]
}

df = pd.DataFrame(data)

# Append to CSV (or create if not exists)
if os.path.exists(csv_filename):
    df.to_csv(csv_filename, mode='a', header=False, index=False)
else:
    df.to_csv(csv_filename, index=False)

print(f"📁 Prediction saved to {csv_filename}")

# Download the CSV file
files.download(csv_filename)

import pandas as pd
import os
from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from IPython.display import display  # For displaying the table in Colab

# Upload image manually
uploaded = files.upload()

# Get uploaded image filename
img_path = list(uploaded.keys())[0]

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

# Load trained model
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Make prediction
prediction = model.predict(img_array)

# Define class labels with details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': "Blurred vision, Sensitivity to light, Difficulty seeing at night, Faded colors",
        'treatment': "Prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Inflammation of the conjunctiva (pink eye), often due to infection or allergies.",
        'symptoms': "Redness, Itchiness, Watery eyes, Discharge that may cause eyelids to stick together",
        'treatment': "Antibiotics for bacterial infections, antihistamines for allergies, and warm compresses."
    },
    'Eyelid': {
        'description': "Eyelid disorders like blepharitis, styes, or ptosis affect eyelid function and appearance.",
        'symptoms': "Swelling, Irritation, Dryness, Painful lump on the eyelid",
        'treatment': "Warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': "No abnormal symptoms detected",
        'treatment': "No treatment needed. Maintain good eye hygiene."
    },
    'Uveitis': {
        'description': "Inflammation of the uvea (middle layer of the eye), causing pain and vision issues.",
        'symptoms': "Eye redness, Blurred vision, Eye pain, Light sensitivity",
        'treatment': "Corticosteroid eye drops, oral steroids, or immunosuppressive drugs."
    }
}

# Get predicted class and details
predicted_class = np.argmax(prediction)
predicted_label = list(disease_info.keys())[predicted_class]
details = disease_info[predicted_label]

# Show Prediction with Disease Info
plt.imshow(img)
plt.title(f"Predicted Class: {predicted_label}")
plt.axis("off")
plt.show()

# Display result
print(f"✅ Predicted Class: {predicted_label}")
print(f"ℹ️ About {predicted_label}: {details['description']}")
print(f"🩺 Symptoms: {details['symptoms']}")
print(f"💊 Suggested Treatment: {details['treatment']}")

# Create DataFrame for table display
df_display = pd.DataFrame({
    "Image": [img_path],
    "Predicted Class": [predicted_label],
    "Description": [details['description']],
    "Symptoms": [details['symptoms']],
    "Treatment": [details['treatment']]
})

# Display as a table in Google Colab
print("\n📊 **Prediction Results Table:**")
display(df_display)

# Save to CSV
csv_filename = "predictions.csv"
if os.path.exists(csv_filename):
    df_display.to_csv(csv_filename, mode='a', header=False, index=False)
else:
    df_display.to_csv(csv_filename, index=False)

print(f"📁 Prediction saved to {csv_filename}")

# Download the CSV file
files.download(csv_filename)

import pandas as pd
import os
from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from IPython.display import display  # For displaying the table in Colab

# Ask for Patient's Name
patient_name = input("Enter Patient's Name: ")

# Upload image manually
uploaded = files.upload()

# Get uploaded image filename
img_path = list(uploaded.keys())[0]

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

# Load trained model
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Make prediction
prediction = model.predict(img_array)

# Define class labels with details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': "Blurred vision, Sensitivity to light, Difficulty seeing at night, Faded colors",
        'treatment': "Prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Inflammation of the conjunctiva (pink eye), often due to infection or allergies.",
        'symptoms': "Redness, Itchiness, Watery eyes, Discharge that may cause eyelids to stick together",
        'treatment': "Antibiotics for bacterial infections, antihistamines for allergies, and warm compresses."
    },
    'Eyelid': {
        'description': "Eyelid disorders like blepharitis, styes, or ptosis affect eyelid function and appearance.",
        'symptoms': "Swelling, Irritation, Dryness, Painful lump on the eyelid",
        'treatment': "Warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': "No abnormal symptoms detected",
        'treatment': "No treatment needed. Maintain good eye hygiene."
    },
    'Uveitis': {
        'description': "Inflammation of the uvea (middle layer of the eye), causing pain and vision issues.",
        'symptoms': "Eye redness, Blurred vision, Eye pain, Light sensitivity",
        'treatment': "Corticosteroid eye drops, oral steroids, or immunosuppressive drugs."
    }
}

# Get predicted class and details
predicted_class = np.argmax(prediction)
predicted_label = list(disease_info.keys())[predicted_class]
details = disease_info[predicted_label]

# Show Prediction with Disease Info
plt.imshow(img)
plt.title(f"Predicted Class: {predicted_label}")
plt.axis("off")
plt.show()

# Display result
print(f"✅ Patient Name: {patient_name}")
print(f"✅ Predicted Class: {predicted_label}")
print(f"ℹ️ About {predicted_label}: {details['description']}")
print(f"🩺 Symptoms: {details['symptoms']}")
print(f"💊 Suggested Treatment: {details['treatment']}")

# Create DataFrame for table display
df_display = pd.DataFrame({
    "Patient Name": [patient_name],
    "Predicted Class": [predicted_label],
    "Description": [details['description']],
    "Symptoms": [details['symptoms']],
    "Treatment": [details['treatment']]
})

# Display as a table in Google Colab
print("\n📊 **Prediction Results Table:**")
display(df_display)

# Save to CSV
csv_filename = "predictions.csv"
if os.path.exists(csv_filename):
    df_display.to_csv(csv_filename, mode='a', header=False, index=False)
else:
    df_display.to_csv(csv_filename, index=False)

print(f"📁 Prediction saved to {csv_filename}")

# Download the CSV file
files.download(csv_filename)

import pandas as pd
import os
from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from IPython.display import display  # For displaying tables in Colab

# Load trained model only once
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Define disease details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': "Blurred vision, Sensitivity to light, Difficulty seeing at night, Faded colors",
        'treatment': "Prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Inflammation of the conjunctiva (pink eye), often due to infection or allergies.",
        'symptoms': "Redness, Itchiness, Watery eyes, Discharge that may cause eyelids to stick together",
        'treatment': "Antibiotics for bacterial infections, antihistamines for allergies, and warm compresses."
    },
    'Eyelid': {
        'description': "Eyelid disorders like blepharitis, styes, or ptosis affect eyelid function and appearance.",
        'symptoms': "Swelling, Irritation, Dryness, Painful lump on the eyelid",
        'treatment': "Warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': "No abnormal symptoms detected",
        'treatment': "No treatment needed. Maintain good eye hygiene."
    },
    'Uveitis': {
        'description': "Inflammation of the uvea (middle layer of the eye), causing pain and vision issues.",
        'symptoms': "Eye redness, Blurred vision, Eye pain, Light sensitivity",
        'treatment': "Corticosteroid eye drops, oral steroids, or immunosuppressive drugs."
    }
}

# Initialize an empty DataFrame for storing results
csv_filename = "predictions.csv"
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=["Patient Name", "Predicted Class", "Description", "Symptoms", "Treatment"])
    df.to_csv(csv_filename, index=False)

# Loop to upload multiple images continuously
while True:
    patient_name = input("\n🔹 Enter Patient's Name (or type 'exit' to stop): ")
    if patient_name.lower() == 'exit':
        print("✅ Process stopped. CSV file saved.")
        break

    print("\n📤 Upload an eye image for", patient_name)
    uploaded = files.upload()  # Upload image manually
    img_path = list(uploaded.keys())[0]

    # Load image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    # Make prediction
    prediction = model.predict(img_array)

    # Get predicted class and details
    predicted_class = np.argmax(prediction)
    predicted_label = list(disease_info.keys())[predicted_class]
    details = disease_info[predicted_label]

    # Show Prediction with Disease Info
    plt.imshow(img)
    plt.title(f"Predicted Class: {predicted_label}")
    plt.axis("off")
    plt.show()

    # Display result
    print(f"✅ Patient Name: {patient_name}")
    print(f"✅ Predicted Class: {predicted_label}")
    print(f"ℹ️ About {predicted_label}: {details['description']}")
    print(f"🩺 Symptoms: {details['symptoms']}")
    print(f"💊 Suggested Treatment: {details['treatment']}")

    # Append result to CSV
    new_data = pd.DataFrame({
        "Patient Name": [patient_name],
        "Predicted Class": [predicted_label],
        "Description": [details['description']],
        "Symptoms": [details['symptoms']],
        "Treatment": [details['treatment']]
    })
    new_data.to_csv(csv_filename, mode='a', header=False, index=False)

    # Show updated table
    df = pd.read_csv(csv_filename)
    print("\n📊 **Updated Prediction Results Table:**")
    display(df)

    print(f"\n📁 Prediction saved to {csv_filename}")

# Download the CSV file after finishing
files.download(csv_filename)

import pandas as pd
import os
from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from IPython.display import display  # For showing tables in Colab

# Load trained model only once
model = load_model("/content/drive/MyDrive/conjunctivitis_model.h5")  # Change path if needed

# Define disease details
disease_info = {
    'Cataract': {
        'description': "Cataract is a condition where the eye's lens becomes cloudy, causing blurry vision.",
        'symptoms': "Blurred vision, Sensitivity to light, Difficulty seeing at night, Faded colors",
        'treatment': "Prescription glasses, stronger lighting, or surgery to replace the cloudy lens."
    },
    'Conjunctivitis': {
        'description': "Inflammation of the conjunctiva (pink eye), often due to infection or allergies.",
        'symptoms': "Redness, Itchiness, Watery eyes, Discharge that may cause eyelids to stick together",
        'treatment': "Antibiotics for bacterial infections, antihistamines for allergies, and warm compresses."
    },
    'Eyelid': {
        'description': "Eyelid disorders like blepharitis, styes, or ptosis affect eyelid function and appearance.",
        'symptoms': "Swelling, Irritation, Dryness, Painful lump on the eyelid",
        'treatment': "Warm compresses, good hygiene, and medication for infections."
    },
    'Normal': {
        'description': "Your eye appears healthy with no detected disease.",
        'symptoms': "No abnormal symptoms detected",
        'treatment': "No treatment needed. Maintain good eye hygiene."
    },
    'Uveitis': {
        'description': "Inflammation of the uvea (middle layer of the eye), causing pain and vision issues.",
        'symptoms': "Eye redness, Blurred vision, Eye pain, Light sensitivity",
        'treatment': "Corticosteroid eye drops, oral steroids, or immunosuppressive drugs."
    }
}

# Define CSV file path
csv_filename = "/content/predictions.csv"

# Check if the CSV file exists; if not, create it
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=["Patient Name", "Predicted Class", "Description", "Symptoms", "Treatment"])
    df.to_csv(csv_filename, index=False)

# Continuous loop for uploading multiple images
while True:
    patient_name = input("\n🔹 Enter Patient's Name (or type 'exit' to stop): ")
    if patient_name.lower() == 'exit':
        print("✅ Process stopped. CSV file saved at:", csv_filename)
        break

    print("\n📤 Upload an eye image for", patient_name)
    uploaded = files.upload()  # Upload image manually
    img_path = list(uploaded.keys())[0]

    # Load image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    # Make prediction
    prediction = model.predict(img_array)

    # Get predicted class and details
    predicted_class = np.argmax(prediction)
    predicted_label = list(disease_info.keys())[predicted_class]
    details = disease_info[predicted_label]

    # Show Prediction with Disease Info
    plt.imshow(img)
    plt.title(f"Predicted Class: {predicted_label}")
    plt.axis("off")
    plt.show()

    # Display result
    print(f"✅ Patient Name: {patient_name}")
    print(f"✅ Predicted Class: {predicted_label}")
    print(f"ℹ️ About {predicted_label}: {details['description']}")
    print(f"🩺 Symptoms: {details['symptoms']}")
    print(f"💊 Suggested Treatment: {details['treatment']}")

    # Append new entry to CSV without overwriting
    new_data = pd.DataFrame({
        "Patient Name": [patient_name],
        "Predicted Class": [predicted_label],
        "Description": [details['description']],
        "Symptoms": [details['symptoms']],
        "Treatment": [details['treatment']]
    })
    new_data.to_csv(csv_filename, mode='a', header=False, index=False)

    # Show updated table from CSV
    df = pd.read_csv(csv_filename)
    print("\n📊 **Updated Prediction Results Table:**")
    display(df)

print("\n✅ All data stored in:", csv_filename)
