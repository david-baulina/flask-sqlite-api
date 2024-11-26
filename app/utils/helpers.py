import xml.etree.ElementTree as ET

def parser(data):
    if len(data) != 3:
        raise ValueError("El array debe contener exactamente 3 elementos: [name, salary, skills]")

    name = data[0]
    salary = data[1] 
    skills_xml = data[2]
    try:
        root = ET.fromstring(skills_xml)
        skills = [elem.text for elem in root if elem.text is not None]
    except ET.ParseError as e:
        raise ValueError(f"Error al parsear el XML de skills: {e}")

    return {
        "name": name,
        "salary": salary,
        "skills": skills
    }

def extra_source_response_adapter(input_obj):
    if not input_obj:
        raise ValueError("El objeto de entrada no puede estar vacío.")
    result = []
    for country_name, country in input_obj.items():
        for job in country:
            processed_value = parser(job)  # Procesar el valor usando la función
            result.append({
                "country": country_name,
                **processed_value
            })
    return result