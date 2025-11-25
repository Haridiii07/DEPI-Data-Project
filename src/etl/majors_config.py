"""
Major and Subject Configuration for Realistic Course Generation
"""

# Major categories with realistic subject pools
MAJORS_CATALOG = {
    # STEM Majors
    "Computer Science": {
        "core": ["Data Structures", "Algorithms", "Database Systems", "Operating Systems", 
                 "Software Engineering", "Computer Networks", "Web Development", "Machine Learning"],
        "related": ["Calculus", "Linear Algebra", "Statistics", "Physics", "Discrete Mathematics"],
        "electives": ["Economics", "Philosophy", "Psychology", "Communication", "Business Administration"]
    },
    "Engineering": {
        "core": ["Engineering Design", "Thermodynamics", "Mechanics", "Circuit Analysis",
                 "Materials Science", "Control Systems", "Fluid Mechanics", "Systems Engineering"],
        "related": ["Calculus", "Physics", "Chemistry", "Linear Algebra", "Statistics"],
        "electives": ["Economics", "Communication", "Ethics", "Psychology"]
    },
    "Mathematics": {
        "core": ["Real Analysis", "Abstract Algebra", "Differential Equations", 
                 "Number Theory", "Topology", "Probability Theory", "Complex Analysis"],
        "related": ["Statistics", "Computer Science", "Physics", "Linear Algebra"],
        "electives": ["Philosophy", "Economics", "History", "Psychology"]
    },
    "Physics": {
        "core": ["Classical Mechanics", "Quantum Mechanics", "Electromagnetism",
                 "Thermodynamics", "Statistical Mechanics", "Optics", "Nuclear Physics"],
        "related": ["Calculus", "Linear Algebra", "Chemistry", "Computer Science"],
        "electives": ["Philosophy", "History of Science", "Communication", "Economics"]
    },
    "Chemistry": {
        "core": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
                 "Analytical Chemistry", "Biochemistry", "Lab Techniques", "Polymer Chemistry"],
        "related": ["Calculus", "Physics", "Biology", "Statistics"],
        "electives": ["Environmental Science", "Ethics", "Communication", "Psychology"]
    },
    "Biology": {
        "core": ["Cell Biology", "Genetics", "Ecology", "Microbiology",
                 "Molecular Biology", "Physiology", "Evolution", "Bioinformatics"],
        "related": ["Chemistry", "Statistics", "Biochemistry", "Physics"],
        "electives": ["Environmental Science", "Ethics", "Psychology", "Philosophy"]
    },
    
    # Business Majors
    "Business Administration": {
        "core": ["Accounting", "Finance", "Marketing", "Operations Management",
                 "Strategic Management", "Business Ethics", "Organizational Behavior"],
        "related": ["Economics", "Statistics", "Business Law", "Communication"],
        "electives": ["Psychology", "Political Science", "Sociology", "Philosophy"]
    },
    "Economics": {
        "core": ["Microeconomics", "Macroeconomics", "Econometrics", 
                 "International Economics", "Game Theory", "Economic Policy", "Development Economics"],
        "related": ["Statistics", "Calculus", "Business Administration", "Political Science"],
        "electives": ["History", "Philosophy", "Psychology", "Sociology"]
    },
    "Accounting": {
        "core": ["Financial Accounting", "Managerial Accounting", "Auditing",
                 "Tax Accounting", "Cost Accounting", "Accounting Information Systems"],
        "related": ["Finance", "Business Law", "Economics", "Statistics"],
        "electives": ["Ethics", "Communication", "Computer Science", "Psychology"]
    },
    
    # Humanities Majors
    "English": {
        "core": ["American Literature", "British Literature", "Creative Writing",
                 "Literary Theory", "Shakespeare", "Modern Poetry", "Composition"],
        "related": ["History", "Philosophy", "Communication", "Foreign Language"],
        "electives": ["Art History", "Psychology", "Sociology", "Political Science"]
    },
    "History": {
        "core": ["World History", "American History", "European History",
                 "Historical Methods", "Ancient Civilizations", "Modern History", "Historiography"],
        "related": ["Political Science", "Philosophy", "Geography", "Sociology"],
        "electives": ["Art History", "Economics", "English", "Foreign Language"]
    },
    "Psychology": {
        "core": ["Intro to Psychology", "Cognitive Psychology", "Social Psychology",
                 "Developmental Psychology", "Abnormal Psychology", "Research Methods"],
        "related": ["Statistics", "Biology", "Neuroscience", "Sociology"],
        "electives": ["Philosophy", "Communication", "Education", "Ethics"]
    },
    "Political Science": {
        "core": ["American Government", "Comparative Politics", "International Relations",
                 "Political Theory", "Public Policy", "Constitutional Law"],
        "related": ["History", "Economics", "Philosophy", "Sociology"],
        "electives": ["Communication", "Statistics", "Foreign Language", "Psychology"]
    },
    
    # Arts Majors
    "Art": {
        "core": ["Drawing", "Painting", "Sculpture", "Art History",
                 "Digital Art", "Studio Practice", "Art Theory"],
        "related": ["Design", "Photography", "Film Studies", "Architecture"],
        "electives": ["History", "Philosophy", "Communication", "Psychology"]
    },
    "Music": {
        "core": ["Music Theory", "Music History", "Performance", "Composition",
                 "Conducting", "Ear Training", "Music Technology"],
        "related": ["Art", "Theater", "Cultural Studies", "Philosophy"],
        "electives": ["History", "Psychology", "Communication", "Foreign Language"]
    }
}

# Major enrollment weights (realistic distribution)
MAJOR_WEIGHTS = {
    "Computer Science": 0.12,
    "Engineering": 0.10,
    "Business Administration": 0.15,
    "Biology": 0.08,
    "Psychology": 0.10,
    "Economics": 0.07,
    "Mathematics": 0.04,
    "Chemistry": 0.05,
    "Physics": 0.03,
    "English": 0.06,
    "History": 0.05,
    "Political Science": 0.06,
    "Art": 0.04,
    "Music": 0.03,
    "Accounting": 0.02
}

def get_major_subjects(major, num_subjects=10):
    """
    Get a realistic mix of subjects for a given major.
    
    Args:
        major: Major name
        num_subjects: Total number of subjects (8-12)
    
    Returns:
        List of subject names
    """
    if major not in MAJORS_CATALOG:
        raise ValueError(f"Unknown major: {major}")
    
    catalog = MAJORS_CATALOG[major]
    
    # Allocate subjects realistically
    num_core = min(len(catalog['core']), max(4, num_subjects // 2))  # 50% core
    num_related = min(len(catalog['related']), max(2, num_subjects // 3))  # 33% related
    num_electives = num_subjects - num_core - num_related  # Rest electives
    
    import random
    
    selected = []
    selected.extend(random.sample(catalog['core'], num_core))
    selected.extend(random.sample(catalog['related'], min(num_related, len(catalog['related']))))
    
    if num_electives > 0:
        available_electives = [e for e in catalog['electives'] if e not in selected]
        selected.extend(random.sample(available_electives, min(num_electives, len(available_electives))))
    
    return selected

def assign_major():
    """Assign a major based on realistic enrollment weights."""
    import random
    return random.choices(
        list(MAJOR_WEIGHTS.keys()),
        weights=list(MAJOR_WEIGHTS.values()),
        k=1
    )[0]
