from typing import List
import os
import html
import pandas as pd
import numpy as np
import random

"""SQL SCRIPT TO EXTRACT PROMPTS
-- PROMPTS TABLE
DROP TABLE prompts;
CREATE TABLE PROMPTS AS
SELECT 
	ANN.ann_annonce, ANN.ANN_THEME_TYPE, ANN.ABO_ID, ABO.ABO_PAYS 
FROM
	(SELECT 
		REPLACE(REPLACE(REPLACE(ann_annonce, '[[**UTF-8**]]', '') ,chr(13), ' '), chr(10), ' ') AS ann_annonce,
		ann_theme_type,
		abo_id
	FROM 
		m_meetic.annonce_theme
	WHERE
		ann_date_creation > SYSDATE - 28
		AND ann_annonce IS NOT null) ANN
LEFT JOIN m_meetic.abonne ABO 
ON ANN.ABO_ID = ABO.ABO_ID;
"""


def set_seeds():
    random.seed(42)
    np.random.seed(42)


def clean_text(text: str) -> str:
    text = html.unescape(text)
    return text


def save_txt(lines: List[str], path: str, overwrite: bool = False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not overwrite:
        raise FileExistsError
    with open(path, 'w') as file:
        for line in lines:
            file.write(line + '\n')


def main():
    # Set random seeds
    set_seeds()

    # Load data
    df = pd.read_csv('data/prompts/PROMPTS_202201071426.csv', sep="\t")
    df.ANN_ANNONCE = df.ANN_ANNONCE.astype(str).apply(clean_text)

    for country in ("FR", "UK"):
        for prompt_type in df.ANN_THEME_TYPE.unique():
            data = df[
                (df.ABO_PAYS == country)
                & (df.ANN_THEME_TYPE == prompt_type)
                ]

            prompts = data.ANN_ANNONCE.tolist()

            # Save all prompts
            save_txt(
                lines=prompts,
                path=f'data/prompts/processed/{country}/prompts_{prompt_type}.txt',
                overwrite=False
            )

            # Save a sample
            sample_size = 1000
            sample = np.random.choice(prompts, size=sample_size, replace=False)
            save_txt(
                lines=sample,
                path=f'data/prompts/processed/{country}/prompts_{prompt_type}.sample.txt',
                overwrite=False
            )


if __name__ == "__main__":
    main()
