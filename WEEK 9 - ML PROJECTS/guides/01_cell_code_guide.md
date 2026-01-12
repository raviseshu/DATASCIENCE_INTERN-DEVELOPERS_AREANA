# Guide: Data Cleaning Logic
* **pd.get_dummies:** This function converts text data (e.g., "Rural", "Urban") into numbers (0, 1) because machine learning models only understand math.
* **drop_first=True:** We drop one column to prevent redundancy (e.g., if it's not Rural and not Urban, it must be City).