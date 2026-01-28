"""
Smart field matcher using comprehensive patterns for form fields.
Supports worldwide official form fields in English and Italian.
Based on universal form field standards.
"""

import re
from app.models.schemas import ParsedData

# Comprehensive field patterns for worldwide forms
FIELD_PATTERNS = {
    # ===== PERSONAL INFORMATION =====
    "first_name": {
        "keywords": [
            "first_name", "firstname", "given_name", "givenname", "forename",
            "nome", "primo_nome", "prenom",
        ],
        "data_key": "names",
        "index": 0,
    },
    "middle_name": {
        "keywords": [
            "middle_name", "middlename", "second_name",
            "secondo_nome", "deuxieme_prenom",
        ],
        "data_key": "names",
        "index": 1,
    },
    "last_name": {
        "keywords": [
            "last_name", "lastname", "surname", "family_name", "familyname",
            "cognome", "nom_de_famille",
        ],
        "data_key": "names",
        "index": 1,
    },
    "full_name": {
        "keywords": [
            "full_name", "fullname", "name", "complete_name", "legal_name",
            "nome_completo", "nominativo", "nom_complet",
        ],
        "data_key": "names",
        "index": 0,
    },
    "date_of_birth": {
        "keywords": [
            "date_of_birth", "dob", "birth_date", "birthdate", "birthday",
            "data_di_nascita", "data_nascita", "nato_il", "date_naissance",
        ],
        "data_key": "dates",
        "index": 0,
    },
    "age": {
        "keywords": ["age", "eta", "age_years"],
        "data_key": "custom",
        "custom_extract": "age",
    },
    "gender": {
        "keywords": [
            "gender", "sex", "sesso", "genere", "sexe",
        ],
        "data_key": "custom",
        "custom_extract": "gender",
    },
    "nationality": {
        "keywords": [
            "nationality", "citizenship", "nazionalita", "cittadinanza", "nationalite",
        ],
        "data_key": "custom",
        "custom_extract": "nationality",
    },
    "marital_status": {
        "keywords": [
            "marital_status", "maritalstatus", "marital", "civil_status",
            "stato_civile", "statocivile", "etat_civil",
        ],
        "data_key": "custom",
        "custom_extract": "marital_status",
    },
    "father_name": {
        "keywords": [
            "father_name", "fathername", "father", "dad_name", "fathers_name",
            "nome_padre", "padre", "nom_pere",
        ],
        "data_key": "names",
        "index": 1,
    },
    "mother_name": {
        "keywords": [
            "mother_name", "mothername", "mother", "mom_name", "mothers_name",
            "nome_madre", "madre", "nom_mere",
        ],
        "data_key": "names",
        "index": 2,
    },
    "guardian_name": {
        "keywords": [
            "guardian_name", "guardianname", "guardian", "legal_guardian",
            "tutore", "nome_tutore",
        ],
        "data_key": "names",
        "index": 2,
    },
    "spouse_name": {
        "keywords": [
            "spouse_name", "spousename", "spouse", "husband_name", "wife_name",
            "partner_name", "coniuge", "nome_coniuge", "marito", "moglie",
        ],
        "data_key": "names",
        "index": 2,
    },

    # ===== CONTACT INFORMATION - ADDRESSES =====
    "permanent_address": {
        "keywords": [
            "permanent_address", "permanentaddress", "perm_address", "home_address",
            "residential_address", "residence_address",
            "indirizzo_residenza", "residenza", "domicilio", "adresse_permanente",
        ],
        "data_key": "addresses",
        "index": 0,
    },
    "current_address": {
        "keywords": [
            "current_address", "currentaddress", "present_address", "presentaddress",
            "mailing_address", "correspondence_address", "temporary_address",
            "indirizzo_attuale", "indirizzo_corrispondenza", "adresse_actuelle",
        ],
        "data_key": "addresses",
        "index": 1,
    },
    "street": {
        "keywords": [
            "street", "street_address", "address_line", "address_line_1",
            "address_line_2", "house_number", "building", "apartment",
            "via", "indirizzo", "rue", "strasse",
        ],
        "data_key": "addresses",
        "index": 0,
    },
    "city": {
        "keywords": [
            "city", "town", "municipality", "village",
            "citta", "comune", "localita", "ville",
        ],
        "data_key": "custom",
        "custom_extract": "city",
    },
    "state": {
        "keywords": [
            "state", "province", "region", "county", "district", "territory",
            "provincia", "regione", "departement",
        ],
        "data_key": "custom",
        "custom_extract": "state",
    },
    "postal_code": {
        "keywords": [
            "postal_code", "postalcode", "zip", "zipcode", "zip_code", "pin",
            "pincode", "pin_code", "postcode",
            "cap", "codice_postale", "code_postal",
        ],
        "data_key": "custom",
        "custom_extract": "postal_code",
    },
    "country": {
        "keywords": [
            "country", "nation", "country_of_residence",
            "paese", "nazione", "pays",
        ],
        "data_key": "custom",
        "custom_extract": "country",
    },
    "work_address": {
        "keywords": [
            "work_address", "workaddress", "office_address", "officeaddress",
            "business_address", "employer_address", "company_address",
            "indirizzo_lavoro", "indirizzo_ufficio", "adresse_travail",
        ],
        "data_key": "addresses",
        "index": 1,
    },

    # ===== CONTACT INFORMATION - PHONE & EMAIL =====
    "email": {
        "keywords": [
            "email", "e_mail", "email_address", "emailaddress", "mail",
            "primary_email", "personal_email", "work_email",
            "posta_elettronica", "indirizzo_email", "courriel",
        ],
        "data_key": "emails",
        "index": 0,
    },
    "phone_number": {
        "keywords": [
            "phone_number", "phonenumber", "phone", "telephone", "tel",
            "contact_number", "mobile", "cell", "cellphone", "mobile_number",
            "primary_phone",
            "telefono", "numero_telefono", "cellulare", "numero_cellulare",
        ],
        "data_key": "phone_numbers",
        "index": 0,
    },
    "alternate_phone": {
        "keywords": [
            "alternate_phone", "alternatephone", "alternate_phone_number",
            "secondary_phone", "other_phone", "additional_phone",
            "home_phone", "landline", "office_phone", "work_phone",
            "telefono_alternativo", "telefono_fisso",
        ],
        "data_key": "phone_numbers",
        "index": 1,
    },

    # ===== IDENTIFICATION DOCUMENTS =====
    "national_id": {
        "keywords": [
            "national_id", "nationalid", "national_id_number", "nid",
            "nid_number", "identity_card", "id_card", "citizen_id",
            "carta_identita", "numero_carta_identita", "carte_identite",
        ],
        "data_key": "id_numbers",
        "index": 0,
    },
    "passport_number": {
        "keywords": [
            "passport_number", "passportno", "passport_no", "passport",
            "passport_id",
            "numero_passaporto", "passaporto", "numero_passeport",
        ],
        "data_key": "id_numbers",
        "index": 0,
    },
    "driver_license": {
        "keywords": [
            "driver_license", "driverlicense", "driving_license", "drivinglicense",
            "driver_license_number", "dl_number", "dl", "license_number",
            "patente", "numero_patente", "permis_conduire",
        ],
        "data_key": "id_numbers",
        "index": 1,
    },
    "voter_id": {
        "keywords": [
            "voter_id", "voterid", "voter_id_number", "voter_card",
            "electoral_id", "election_card",
            "tessera_elettorale", "carte_electeur",
        ],
        "data_key": "id_numbers",
        "index": 1,
    },
    "tax_id": {
        "keywords": [
            "tax_id", "taxid", "tax_id_number", "tin", "tax_number",
            "ssn", "social_security", "social_security_number",
            "pan", "pan_number", "pan_card",
            "codice_fiscale", "cf", "numero_fiscale",
        ],
        "data_key": "id_numbers",
        "index": 0,
    },
    "id_number": {
        "keywords": [
            "id_number", "idnumber", "id_no", "id", "identification_number",
            "numero_id", "codice_id",
        ],
        "data_key": "id_numbers",
        "index": 0,
    },

    # ===== EMPLOYMENT & EDUCATION =====
    "occupation": {
        "keywords": [
            "occupation", "profession", "job", "employment", "work",
            "professione", "lavoro", "occupazione", "mestiere", "metier",
        ],
        "data_key": "custom",
        "custom_extract": "occupation",
    },
    "job_title": {
        "keywords": [
            "job_title", "jobtitle", "position", "designation", "role",
            "title", "work_title",
            "titolo", "qualifica", "titre_poste",
        ],
        "data_key": "custom",
        "custom_extract": "job_title",
    },
    "employer_name": {
        "keywords": [
            "employer_name", "employername", "employer", "company_name",
            "company", "organization", "organisation", "workplace", "firm",
            "datore_lavoro", "azienda", "societa", "employeur",
        ],
        "data_key": "custom",
        "custom_extract": "employer",
    },
    "years_of_experience": {
        "keywords": [
            "years_of_experience", "experience", "work_experience",
            "total_experience", "years_experience",
            "anni_esperienza", "esperienza", "annees_experience",
        ],
        "data_key": "custom",
        "custom_extract": "experience",
    },
    "highest_qualification": {
        "keywords": [
            "highest_qualification", "qualification", "education",
            "educational_qualification", "degree", "highest_degree",
            "titolo_studio", "istruzione", "diplome",
        ],
        "data_key": "custom",
        "custom_extract": "qualification",
    },
    "institution_name": {
        "keywords": [
            "institution_name", "institutionname", "institution",
            "school", "college", "university", "alma_mater",
            "istituto", "universita", "scuola", "etablissement",
        ],
        "data_key": "custom",
        "custom_extract": "institution",
    },
    "year_of_passing": {
        "keywords": [
            "year_of_passing", "passing_year", "graduation_year",
            "year_graduated", "completion_year",
            "anno_laurea", "anno_diploma", "annee_diplome",
        ],
        "data_key": "dates",
        "index": 1,
    },

    # ===== FINANCIAL INFORMATION =====
    "bank_account": {
        "keywords": [
            "bank_account", "bankaccount", "bank_account_number",
            "account_number", "accountnumber", "account_no",
            "iban", "account",
            "conto_corrente", "numero_conto", "compte_bancaire",
        ],
        "data_key": "custom",
        "custom_extract": "bank_account",
    },
    "bank_name": {
        "keywords": [
            "bank_name", "bankname", "bank", "financial_institution",
            "nome_banca", "banca", "banque",
        ],
        "data_key": "custom",
        "custom_extract": "bank_name",
    },
    "branch": {
        "keywords": [
            "branch", "branch_name", "branch_code", "bank_branch",
            "filiale", "succursale", "agence",
        ],
        "data_key": "custom",
        "custom_extract": "branch",
    },
    "income": {
        "keywords": [
            "income", "annual_income", "monthly_income", "salary",
            "earnings", "gross_income", "net_income",
            "reddito", "stipendio", "salario", "revenu",
        ],
        "data_key": "custom",
        "custom_extract": "income",
    },

    # ===== LEGAL & CONSENT =====
    "signature": {
        "keywords": [
            "signature", "sign", "applicant_signature",
            "firma", "signature_candidat",
        ],
        "data_key": "custom",
        "custom_extract": "signature",
    },
    "date_of_submission": {
        "keywords": [
            "date_of_submission", "submission_date", "application_date",
            "date_submitted", "filing_date",
            "data_presentazione", "data_domanda", "date_soumission",
        ],
        "data_key": "dates",
        "index": 1,
    },
    "date": {
        "keywords": ["date", "data", "fecha"],
        "data_key": "dates",
        "index": 0,
    },

    # ===== MISCELLANEOUS =====
    "reference_number": {
        "keywords": [
            "reference_number", "referencenumber", "ref_no", "ref_number",
            "application_number", "case_number", "file_number", "tracking_number",
            "numero_riferimento", "numero_pratica", "numero_reference",
        ],
        "data_key": "id_numbers",
        "index": 1,
    },
    "purpose": {
        "keywords": [
            "purpose", "purpose_of_application", "reason", "objective",
            "scopo", "motivo", "finalita", "objet",
        ],
        "data_key": "custom",
        "custom_extract": "purpose",
    },
    "emergency_contact_name": {
        "keywords": [
            "emergency_contact", "emergencycontact", "emergency_contact_name",
            "emergency_name", "ice_contact",
            "contatto_emergenza", "contact_urgence",
        ],
        "data_key": "names",
        "index": 2,
    },
    "emergency_contact_phone": {
        "keywords": [
            "emergency_phone", "emergency_contact_phone", "emergency_number",
            "ice_phone",
            "telefono_emergenza", "telephone_urgence",
        ],
        "data_key": "phone_numbers",
        "index": 1,
    },
    "relationship": {
        "keywords": [
            "relationship", "relation", "emergency_relationship",
            "relazione", "parentela", "lien_parente",
        ],
        "data_key": "custom",
        "custom_extract": "relationship",
    },
    "place_of_birth": {
        "keywords": [
            "place_of_birth", "placeofbirth", "birth_place", "birthplace",
            "city_of_birth", "born_in",
            "luogo_nascita", "luogo_di_nascita", "nato_a", "lieu_naissance",
        ],
        "data_key": "custom",
        "custom_extract": "place_of_birth",
    },
    "blood_group": {
        "keywords": [
            "blood_group", "bloodgroup", "blood_type", "bloodtype",
            "gruppo_sanguigno", "groupe_sanguin",
        ],
        "data_key": "custom",
        "custom_extract": "blood_group",
    },
    "religion": {
        "keywords": [
            "religion", "faith", "religione", "credo",
        ],
        "data_key": "custom",
        "custom_extract": "religion",
    },
}


def normalize_field_name(name: str) -> str:
    """Normalize field name for matching."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def extract_custom_field(text: str, field_type: str) -> str | None:
    """Extract custom field values from OCR text."""
    patterns = {
        "gender": [
            r"(?i)\b(male|female|m|f|other)\b",
            r"(?i)\b(maschio|femmina|altro)\b",
            r"(?i)(?:gender|sex|sesso)[\s:.\-]+([a-zA-Z]+)",
        ],
        "marital_status": [
            r"(?i)\b(single|married|divorced|widowed|separated|unmarried)\b",
            r"(?i)\b(celibe|nubile|coniugato|coniugata|divorziato|divorziata|vedovo|vedova)\b",
            r"(?i)(?:marital|status|stato.civile)[\s:.\-]+([a-zA-Z]+)",
        ],
        "nationality": [
            r"(?i)(?:nationality|citizenship|nazionalita|cittadinanza)[\s:.\-]+([a-zA-Z]+)",
        ],
        "blood_group": [
            r"(?i)\b(A|B|AB|O)[\s]?[+-]\b",
            r"(?i)(?:blood|gruppo.sanguigno)[\s:.\-]*(A|B|AB|O)[\s]?[+-]?",
        ],
        "religion": [
            r"(?i)(?:religion|religione)[\s:.\-]+([a-zA-Z]+)",
        ],
        "occupation": [
            r"(?i)(?:occupation|profession|lavoro|professione)[\s:.\-]+([^\n,]+)",
        ],
        "job_title": [
            r"(?i)(?:title|position|designation|qualifica)[\s:.\-]+([^\n,]+)",
        ],
        "employer": [
            r"(?i)(?:employer|company|azienda|societa)[\s:.\-]+([^\n,]+)",
        ],
        "place_of_birth": [
            r"(?i)(?:place.of.birth|birth.place|luogo.nascita|nato.a)[\s:.\-]+([^\n,]+)",
        ],
        "city": [
            r"(?i)(?:city|citta|town|comune)[\s:.\-]+([^\n,]+)",
        ],
        "state": [
            r"(?i)(?:state|province|provincia|region)[\s:.\-]+([^\n,]+)",
        ],
        "country": [
            r"(?i)(?:country|nation|paese|nazione)[\s:.\-]+([^\n,]+)",
        ],
        "postal_code": [
            r"(?i)(?:postal|zip|cap|pin)[\s_.]*(?:code)?[\s:.\-]*(\d{4,10})",
        ],
        "age": [
            r"(?i)(?:age|eta)[\s:.\-]*(\d{1,3})",
        ],
        "experience": [
            r"(?i)(?:experience|esperienza)[\s:.\-]*(\d+)",
        ],
        "qualification": [
            r"(?i)(?:qualification|degree|titolo|diploma)[\s:.\-]+([^\n,]+)",
        ],
        "institution": [
            r"(?i)(?:institution|university|college|school|istituto)[\s:.\-]+([^\n,]+)",
        ],
        "bank_account": [
            r"(?i)(?:account|iban|conto)[\s_.]*(?:no|number)?[\s:.\-]*([A-Z0-9]{8,34})",
        ],
        "bank_name": [
            r"(?i)(?:bank|banca)[\s_.]*(?:name)?[\s:.\-]+([^\n,]+)",
        ],
        "branch": [
            r"(?i)(?:branch|filiale)[\s:.\-]+([^\n,]+)",
        ],
        "income": [
            r"(?i)(?:income|salary|reddito|stipendio)[\s:.\-]*([0-9,.]+)",
        ],
        "relationship": [
            r"(?i)(?:relationship|relation|relazione)[\s:.\-]+([^\n,]+)",
        ],
        "purpose": [
            r"(?i)(?:purpose|reason|scopo|motivo)[\s:.\-]+([^\n.]+)",
        ],
    }

    if field_type not in patterns:
        return None

    for pattern in patterns[field_type]:
        match = re.search(pattern, text)
        if match:
            result = match.group(1).strip() if match.lastindex else match.group(0).strip()
            if result and len(result) > 0:
                return result

    return None


def smart_match_fields(pdf_fields: list[str], parsed_data: ParsedData, ocr_text: str) -> dict[str, str]:
    """
    Intelligently match PDF field names to extracted data.
    Uses comprehensive pattern matching for worldwide forms.
    """
    result = {}
    used_indices = {}

    data_dict = {
        "names": parsed_data.names,
        "dates": parsed_data.dates,
        "id_numbers": parsed_data.id_numbers,
        "addresses": parsed_data.addresses,
        "emails": parsed_data.emails,
        "phone_numbers": parsed_data.phone_numbers,
    }

    for field in pdf_fields:
        normalized = normalize_field_name(field)
        matched = False

        # Try to match against known patterns
        for pattern_name, pattern_config in FIELD_PATTERNS.items():
            keywords = pattern_config["keywords"]

            for keyword in keywords:
                keyword_normalized = normalize_field_name(keyword)

                # Check various matching strategies
                if (keyword_normalized == normalized or
                    keyword_normalized in normalized or
                    normalized in keyword_normalized or
                    normalized.endswith(keyword_normalized) or
                    normalized.startswith(keyword_normalized)):

                    data_key = pattern_config["data_key"]

                    if data_key == "custom":
                        custom_type = pattern_config.get("custom_extract")
                        value = extract_custom_field(ocr_text, custom_type)
                        if value:
                            result[field] = value
                            matched = True
                            break
                    else:
                        data_list = data_dict.get(data_key, [])
                        if data_list:
                            preferred_idx = pattern_config.get("index", 0)
                            used_key = f"{data_key}_{pattern_name}"

                            if used_key not in used_indices:
                                used_indices[used_key] = preferred_idx

                            idx = used_indices[used_key]
                            if idx < len(data_list):
                                result[field] = data_list[idx]
                                used_indices[used_key] = idx + 1
                                matched = True
                                break

            if matched:
                break

        # Fallback: generic keyword matching
        if not matched:
            fallbacks = [
                (["name", "nome", "nom"], "names"),
                (["date", "data", "fecha"], "dates"),
                (["id", "number", "numero", "no"], "id_numbers"),
                (["address", "indirizzo", "adresse"], "addresses"),
                (["email", "mail", "posta"], "emails"),
                (["phone", "tel", "cell", "telefono", "mobile"], "phone_numbers"),
            ]

            for keywords, data_key in fallbacks:
                if any(kw in normalized for kw in keywords):
                    data_list = data_dict.get(data_key, [])
                    if data_list:
                        fallback_key = f"fallback_{data_key}"
                        if fallback_key not in used_indices:
                            used_indices[fallback_key] = 0
                        idx = used_indices[fallback_key]
                        if idx < len(data_list):
                            result[field] = data_list[idx]
                            used_indices[fallback_key] = idx + 1
                            break

    return result
