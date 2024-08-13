import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

# Get all datasets for a specific pipeline
pipeline_slug = "guess-the-year"
datasets = gentrace.get_datasets(pipeline_slug=pipeline_slug)
print("All datasets:")
for dataset in datasets['data']:
    print(f"- {dataset['name']} (ID: {dataset['id']})")

# Create a new dataset
new_dataset = gentrace.create_dataset({
    "name": "New Test Dataset",
    "description": "A dataset created for testing purposes",
    "pipelineId": "c10408c7-abde-5c19-b339-e8b1087c9b64"
})
print(f"\nCreated new dataset: {new_dataset['name']} (ID: {new_dataset['id']})")

# Get a specific dataset
dataset_id = new_dataset['id']
dataset = gentrace.get_dataset(dataset_id)
print(f"\nRetrieved dataset: {dataset['name']} (ID: {dataset['id']})")

# Update the dataset
updated_dataset = gentrace.update_dataset(dataset_id, {
    "name": "Updated Test Dataset",
    "description": "An updated description for the test dataset"
})
print(f"\nUpdated dataset: {updated_dataset['name']} (ID: {updated_dataset['id']})")

# Get all datasets, including archived ones
all_datasets = gentrace.get_datasets(pipeline_slug=pipeline_slug, archived=None)
print("\nAll datasets (including archived):")
for dataset in all_datasets['data']:
    archived_status = "Archived" if dataset.get('archivedAt') else "Active"
    print(f"- {dataset['name']} (ID: {dataset['id']}, Status: {archived_status})")
