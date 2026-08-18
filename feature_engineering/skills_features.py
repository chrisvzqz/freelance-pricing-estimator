from rapidfuzz import fuzz
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

SKILLS_MAPPING = {
    # Translation
    "Modelado de Datos": "Data Modeling",
    "Publicaciones para redes sociales": "Social Media Posts",
    "Diseño de Redes": "Network Design",
    "Administrador de Redes": "Network Administration",
    "Aptitud de programación": "Programming",
    "Tiendas Online (e-commerce)": "eCommerce",
    "Desarrollo de video juegos": "Game Development",
    "Informática": "Computer Science",
    "Programación de video juegos": "Game Development",
    "MercadoPago": "MercadoPago",
    "Tienda Nube": "Tienda Nube",
    "Aplicaciones de escritorio": "Desktop Application",
    "Inteligencia empresarial": "Business Intelligence",
    "Recursos Humanos": "Human Resources",
    "Inteligencia Artificial": "Artificial Intelligence",
    "Realidad Aumentada": "Augmented Reality",
    "Publicidad en Google, Facebook": "Google Ads",
    "Interfaz de usuario": "User Interface",
    "Asistente de administración": "Administrative Assistant",
    "Contabilidad": "Accounting",
    "Asistente Virtual": "Virtual Assistant",
    "Gestión de inventario": "Inventory Management",
    "Animación": "Animation",
    "Programación de Redes": "Network Programming",
    "Criptografía": "Cryptography",
    "Diseño de Logo": "Logo Design",
    "Diseño Gráfico": "Graphic Design",
    "Producción de Video": "Video Production",
    "Videografía": "Videography",
    "Comercio Electrónico": "eCommerce",

    # Normalization
    "FireWall": "Firewall",
    "Linkedin": "LinkedIn",
    "Prestashop": "PrestaShop",
    "Qlikview": "QlikView",
    "R programming language": "R Programming Language",
    "Saas": "SaaS",

    # Merge
    "Content Management System (CMS)": "Content Management System",
    "Machine Learning (ML)": "Machine Learning",
    "Amazon Web Services (AWS)": "Amazon Web Services",
    "Website Development": "Web Development"
}

def create_skills_count(df):
    df = df.copy()

    df['skills_count'] = df['skills'].apply(len)

    return df

def translate_skills(skills):

    return [SKILLS_MAPPING.get(skill, skill) for skill in skills]

def transform_skills_column(df):
    df = df.copy()

    df['skills'] = df['skills'].apply(translate_skills)

    return df

def filter_frequent_skills(df):
    df = df.copy()

    skills = df['skills'].explode().value_counts()

    skills_thrshld = skills[skills >= 10].index

    df_thrshld = df['skills'].apply(
        lambda project_skills: [
            skill
            for skill in project_skills
            if skill in skills_thrshld
        ]
    )

    df['skills'] = df_thrshld

    return df
    

def find_similar_skills(df, similarity_threshold=85):
    skills = df["skills"].explode().drop_duplicates().tolist()

    similar_skills = []

    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            skill_1 = skills[i]
            skill_2 = skills[j]

            similarity = fuzz.ratio(skill_1, skill_2)

            if similarity >= similarity_threshold:
                similar_skills.append(
                    (skill_1, skill_2, similarity)
                )

    return sorted(
        similar_skills,
        key=lambda x: x[2],
        reverse=True
    )


def encode_skills(df):
    df = df.copy()
    mlb = MultiLabelBinarizer()

    encoded_skills = mlb.fit_transform(df['skills'])

    skills_encoded_df = pd.DataFrame(
        encoded_skills,
        columns=mlb.classes_,
        index=df.index
    )

    df = df.drop('skills', axis=1)

    return pd.concat([df, skills_encoded_df], axis=1)