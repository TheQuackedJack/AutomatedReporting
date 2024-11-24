# input_model_example.py

import dill  # Use dill instead of pickle

with open('input_model.pkl', 'rb') as f:
    LoadedInputModel = dill.load(f)

# Now you can use LoadedInputModel as a Pydantic model
instance = LoadedInputModel(
    report_title="Loaded Report",
    sales_data=[1000.0, 2000.0],
    include_summary=False
)
print(instance)
