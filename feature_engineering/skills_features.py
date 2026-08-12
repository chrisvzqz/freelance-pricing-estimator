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
    "Saas": "SaaS"
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