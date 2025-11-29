import pandas as pd
import os

# Team Data
data = [
    {
        "Name": "Abdulrahman Mustafa",
        "Role": "Team Leader",
        "Email": "abdulrahmanmustafa553@gmail.com",
        "Phone Number": "01015359437"
    },
    {
        "Name": "Malak Samir",
        "Role": "Member",
        "Email": "Malaksamir2004@gmail.com",
        "Phone Number": "01124424343"
    },
    {
        "Name": "Eman Wassem",
        "Role": "Member",
        "Email": "emanwassem242@gmail.com",
        "Phone Number": "01006098663"
    },
    {
        "Name": "Khaled Ehab",
        "Role": "Member",
        "Email": "khaledehab1989@gmail.com",
        "Phone Number": "01125201877"
    },
    {
        "Name": "Ahmed Mohamed Galal Shoeib",
        "Role": "Member",
        "Email": "Ahmed2307965@miuegypt.edu.eg",
        "Phone Number": "01015141291"
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Ensure submission directory exists
output_dir = "submission"
os.makedirs(output_dir, exist_ok=True)

# Save to Excel
output_file = os.path.join(output_dir, "Team_Members.xlsx")
df.to_excel(output_file, index=False)

print(f"✅ Created {output_file}")
