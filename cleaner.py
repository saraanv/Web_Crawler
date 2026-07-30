import json
import re


INPUT_FILE = "data/pages.json"

OUTPUT_FILE = "data/clean_pages.json"



REMOVE_PATTERNS = [
    r"بیمارستان:",

r"نوبت دهی:",
        r"\d{10,}",

    r"\d{3,5}-\d{2,5}-?\d*",

    r"\d{2,4}-\d{5,}",

    r"کلیه حقوق مادی و معنوی.*",

    r"location_on",

    r"local_post_office",

    r"call",

    r"print",

    r"copyright",

    r"Copyright",

    r"©",

    r"طراحی و توسعه.*",

    r"Amirkabir Data Miners",

    r"در حال بارگذاری",

    r"بهترین ها برای سلامتیمون"

]



def clean_text(text):

    for pattern in REMOVE_PATTERNS:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )
        
    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()



def clean_pages():


    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        pages = json.load(f)



    cleaned = []



    for page in pages:


        text = clean_text(
            page["text"]
        )


        cleaned.append(
            {
                "url": page["url"],
                "text": text
            }
        )



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            cleaned,
            f,
            ensure_ascii=False,
            indent=2
        )



    print(
        f"Cleaned pages: {len(cleaned)}"
    )



if __name__ == "__main__":

    clean_pages()